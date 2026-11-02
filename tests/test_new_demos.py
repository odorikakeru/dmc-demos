"""Smoke tests for the DataList and FloatingWindow demos."""

import json
import re

import pytest

import data_list_demo
import floating_window_demo
from floating_window_demo import MOVES, WINDOWS


def walk(node):
    """Yield every component in a serialized Dash layout."""
    if isinstance(node, dict):
        if 'namespace' in node and 'props' in node:
            yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


@pytest.fixture
def floating_client():
    """Initialize the demo without relying on other apps importing its callbacks."""
    with floating_window_demo.app.server.test_client() as client:
        assert client.get('/').status_code == 200
        yield client


@pytest.mark.parametrize('module', [data_list_demo, floating_window_demo])
def test_pages_render(module):
    """Every section serves and has a unique anchor."""
    with module.app.server.test_client() as client:
        assert client.get('/').status_code == 200
        assert client.get('/_dash-layout').status_code == 200
    slugs = [section.slug for section in module.SECTIONS]
    assert len(slugs) == len(set(slugs))


def test_floating_window_callbacks():
    """Windows can be built and moving returns valid position dicts."""
    assert all(window().id['demo'] == name for name, window in WINDOWS.items())
    assert all(len(move) == 2 for move in MOVES.values())
    assert floating_window_demo.show_state({'x': 1, 'y': 2}, None, False, None).startswith(
        'currentPosition: {"x": 1, "y": 2}'
    )


def test_dynamic_windows_are_in_validation_layout(floating_client):
    """The renderer knows all dynamic IDs even when the windows start closed."""
    index = floating_client.get('/').get_data(as_text=True)
    match = re.search(r'<script id="_dash-config"[^>]*>(.*?)</script>', index, re.DOTALL)
    assert match is not None
    config = json.loads(match.group(1))
    assert config['suppress_callback_exceptions'] is False
    components = list(walk(config['validation_layout']))
    ids = [node['props']['id'] for node in components if 'id' in node['props']]
    assert len(ids) == len({json.dumps(value, sort_keys=True) for value in ids})
    assert set(MOVES) <= {value for value in ids if isinstance(value, str)}
    for name in WINDOWS:
        assert floating_window_demo.window_id(name) in ids
    initial = list(walk(floating_client.get('/_dash-layout').get_json()))
    assert not any(node['type'] == 'FloatingWindow' for node in initial)
    dependencies = floating_client.get('/_dash-dependencies').get_json()
    assert len(dependencies) == 3


@pytest.mark.parametrize('name', WINDOWS)
@pytest.mark.parametrize('clicks', [1, 2, 3])
def test_toggle_dynamic_window(floating_client, name, clicks):
    """Opening, closing and reopening each example uses the registered callback."""
    output = next(key for key in floating_window_demo.app.callback_map if key.startswith('..'))
    response = floating_client.post(
        '/_dash-update-component',
        json={
            'output': output,
            'outputs': [
                {'id': {'type': 'host', 'demo': name}, 'property': 'children'},
                {'id': {'type': 'toggle', 'demo': name}, 'property': 'children'},
            ],
            'inputs': [
                {'id': {'type': 'toggle', 'demo': name}, 'property': 'n_clicks', 'value': clicks}
            ],
            'state': [],
            'changedPropIds': [
                json.dumps({'type': 'toggle', 'demo': name}, sort_keys=True, separators=(',', ':'))
                + '.n_clicks'
            ],
        },
    )
    assert response.status_code == 200
    result = response.get_json()['response']
    host_id = json.dumps({'type': 'host', 'demo': name}, sort_keys=True, separators=(',', ':'))
    window = result[host_id]['children']
    if clicks % 2:
        assert window['type'] == 'FloatingWindow'
        assert window['props']['id'] == floating_window_demo.window_id(name)
    else:
        assert window is None


@pytest.mark.parametrize('trigger, expected', MOVES.items())
def test_move_dynamic_window(floating_client, trigger, expected):
    """All four corner buttons update the dynamically mounted window."""
    window_id = json.dumps(
        floating_window_demo.window_id('position'), sort_keys=True, separators=(',', ':')
    )
    response = floating_client.post(
        '/_dash-update-component',
        json={
            'output': window_id + '.position',
            'outputs': {'id': floating_window_demo.window_id('position'), 'property': 'position'},
            'inputs': [
                {'id': key, 'property': 'n_clicks', 'value': int(key == trigger)} for key in MOVES
            ],
            'state': [],
            'changedPropIds': [trigger + '.n_clicks'],
        },
    )
    assert response.status_code == 200
    assert response.get_json()['response'][window_id]['position'] == expected
