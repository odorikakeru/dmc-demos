"""Regression tests for the documentation layout and Dash callbacks."""

import json

import pytest

from tree_select_demo import (
    BRANCHES,
    DATA,
    SECTIONS,
    app,
    show_dropdown,
    show_expansion,
    show_search,
    show_values,
)


@pytest.fixture
def client():
    """Initialize Dash callbacks and return its Flask test client."""
    with app.server.test_client() as client:
        assert client.get('/').status_code == 200
        yield client


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


def test_layout_contains_real_examples_and_matching_readouts(client):
    """Every documented section contains a real component and readable source."""
    response = client.get('/_dash-layout')
    assert response.status_code == 200
    components = list(walk(response.get_json()))
    assert any(node['type'] == 'MantineProvider' for node in components)
    trees = [node for node in components if node['type'] == 'TreeSelect']
    assert len(trees) == 22
    ids = [node['props']['id'] for node in components if 'id' in node['props']]
    assert len(ids) == len({json.dumps(value, sort_keys=True) for value in ids})
    selections = [
        value['demo']
        for value in ids
        if isinstance(value, dict) and value.get('type') == 'selection'
    ]
    readouts = [
        value['demo']
        for value in ids
        if isinstance(value, dict) and value.get('type') == 'value'
    ]
    assert selections == readouts
    assert len(selections) == 10
    for slug, _, _, factory, *_ in SECTIONS:
        assert slug in ids
        assert factory.__name__ in response.get_data(as_text=True)
    for tree in trees:
        props = tree['props']
        assert props.get('label') or props.get('aria-label')
        value = props.get('value')
        if props.get('mode', 'single') == 'single':
            assert value is None or isinstance(value, str)
        else:
            assert isinstance(value, list)
    assert 'Unavailable:' not in response.get_data(as_text=True)


def test_data_has_unique_string_values():
    """All nodes use globally unique values and all expansion IDs exist."""
    values = []

    def collect(nodes):
        for node in nodes:
            assert isinstance(node['value'], str)
            assert node['label']
            values.append(node['value'])
            collect(node.get('children', []))

    collect(DATA)
    assert len(values) == len(set(values))
    assert set(BRANCHES) <= set(values)


@pytest.mark.parametrize(
    'values', [[None, [], 'apple', ['bread', 'milk']], ['fruit'], [[]]]
)
def test_value_readouts_preserve_json_types(values):
    """Readouts preserve null, strings and lists without success-shaped defaults."""
    assert [json.loads(value) for value in show_values(values)] == values


@pytest.mark.parametrize('query', [None, '', 'apple', '"quoted"'])
def test_search_readout(query):
    """Search readouts escape arbitrary text as JSON."""
    assert show_search(query) == f'searchValue: {json.dumps(query)}'


@pytest.mark.parametrize(
    ('output', 'input_id', 'prop', 'value', 'expected'),
    [
        ('dropdown-state.children', 'dropdown-tree', 'dropdownOpened', True, show_dropdown(True)),
        ('search-state.children', '{"demo":"search","type":"selection"}',
         'searchValue', 'apple', show_search('apple')),
        ('expansion-state.children', 'expansion-tree', 'expandedValues',
         ['fruit'], show_expansion(['fruit'])),
    ],
)
def test_dash_callbacks(client, output, input_id, prop, value, expected):
    """Exercise serialized Dash callback requests, not only direct Python calls."""
    component_id, output_prop = output.rsplit('.', 1)
    response = client.post(
        '/_dash-update-component',
        json={
            'output': output,
            'outputs': {'id': component_id, 'property': output_prop},
            'inputs': [{'id': input_id, 'property': prop, 'value': value}],
            'state': [],
            'changedPropIds': [f'{input_id}.{prop}'],
        },
    )
    assert response.status_code == 200
    assert response.get_json()['response'][component_id][output_prop] == expected


@pytest.mark.parametrize('trigger', ['expand-all', 'collapse-all'])
def test_expansion_buttons(client, trigger):
    """Both buttons update the controlled component using Dash trigger context."""
    response = client.post(
        '/_dash-update-component',
        json={
            'output': 'expansion-tree.expandedValues',
            'outputs': {'id': 'expansion-tree', 'property': 'expandedValues'},
            'inputs': [
                {'id': 'expand-all', 'property': 'n_clicks', 'value': 1},
                {'id': 'collapse-all', 'property': 'n_clicks', 'value': 1},
            ],
            'state': [],
            'changedPropIds': [f'{trigger}.n_clicks'],
        },
    )
    assert response.status_code == 200
    expected = BRANCHES if trigger == 'expand-all' else []
    assert response.get_json()['response']['expansion-tree']['expandedValues'] == expected


@pytest.mark.parametrize(
    ('trigger', 'checked', 'opened', 'expected'),
    [
        ('dropdown-toggle', True, False, True),
        ('dropdown-toggle', False, True, False),
        ('dropdown-tree', True, False, False),
        ('dropdown-tree', False, True, True),
    ],
)
def test_dropdown_control_stays_synchronized(client, trigger, checked, opened, expected):
    """Opening, outside clicks and Escape keep both controlled props in sync."""
    response = client.post(
        '/_dash-update-component',
        json={
            'output': '..dropdown-tree.dropdownOpened...dropdown-toggle.checked..',
            'outputs': [
                {'id': 'dropdown-tree', 'property': 'dropdownOpened'},
                {'id': 'dropdown-toggle', 'property': 'checked'},
            ],
            'inputs': [
                {'id': 'dropdown-toggle', 'property': 'checked', 'value': checked},
                {'id': 'dropdown-tree', 'property': 'dropdownOpened', 'value': opened},
            ],
            'state': [],
            'changedPropIds': [
                f'{trigger}.{"checked" if trigger == "dropdown-toggle" else "dropdownOpened"}'
            ],
        },
    )
    assert response.status_code == 200
    result = response.get_json()['response']
    assert result['dropdown-tree']['dropdownOpened'] is expected
    assert result['dropdown-toggle']['checked'] is expected


def test_local_assets_and_react_version(client):
    """The app serves its functions locally and loads the DMC-compatible React."""
    index = client.get('/').get_data(as_text=True)
    assert 'react@19' in index
    for path in ['/assets/style.css', '/assets/tree-select.js']:
        assert client.get(path).status_code == 200
    functions = client.get('/assets/tree-select.js').get_data(as_text=True)
    for name in ['treeOverflow', 'treeNode', 'treePill', 'treeFilter']:
        assert f'dmcfuncs.{name}' in functions
