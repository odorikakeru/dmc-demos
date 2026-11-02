"""Interactive FloatingWindow documentation built with Dash Mantine Components."""

import json
from collections.abc import Callable
from typing import Any

import dash_mantine_components as dmc
from dash import (
    MATCH,
    Dash,
    Input,
    Output,
    _dash_renderer,
    ctx,
    html,
)
from dash.development.base_component import Component

from demo_page import Section, page_layout

_dash_renderer._set_react_version('19.2.4')

app = Dash(__name__, title='FloatingWindow | Dash Mantine Components')

MOVES = {
    'move-top-left': {'top': 100, 'left': 24},
    'move-top-right': {'top': 100, 'right': 24},
    'move-bottom-left': {'bottom': 24, 'left': 24},
    'move-bottom-right': {'bottom': 24, 'right': 24},
}


def window_id(name: str) -> dict[str, str]:
    """Identify the FloatingWindow of an example."""
    return {'type': 'window', 'demo': name}


def host(name: str) -> Component:
    """Provide a button that opens the example window and a live state readout."""
    return dmc.Stack(
        [
            dmc.Button(
                'Show window',
                id={'type': 'toggle', 'demo': name},
                variant='light',
                w='fit-content',
            ),
            html.Div(id={'type': 'host', 'demo': name}),
            html.Pre(id={'type': 'state', 'demo': name}, className='value-output'),
        ]
    )


def usage_window() -> Component:
    """Drag the whole window by any part of its surface."""
    return dmc.FloatingWindow(
        [dmc.Text('Drag me', fw=600), dmc.Text('Move this window anywhere.', size='sm')],
        id=window_id('usage'),
        initialPosition={'top': 120, 'right': 40},
        w=260,
        p='md',
        withBorder=True,
        shadow='md',
        radius='md',
    )


def handle_window() -> Component:
    """Drag only by a header, leaving the body for interaction."""
    return dmc.FloatingWindow(
        [
            html.Div(
                dmc.Text('Drag from here', fw=600, size='sm'),
                className='drag-handle',
                style={
                    'cursor': 'move',
                    'padding': 8,
                    'background': 'var(--mantine-color-blue-light)',
                },
            ),
            dmc.Stack(
                [
                    dmc.Text('The body does not start a drag.', size='sm'),
                    dmc.Button('Button in the body', size='xs'),
                ],
                p='md',
                gap='xs',
            ),
        ],
        id=window_id('handle'),
        initialPosition={'top': 120, 'right': 40},
        dragHandleSelector='.drag-handle',
        w=260,
        withBorder=True,
        shadow='md',
        radius='md',
    )


def axis_window() -> Component:
    """Restrict movement to a single axis."""
    return dmc.FloatingWindow(
        dmc.Text('I only move horizontally.', size='sm'),
        id=window_id('axis'),
        initialPosition={'top': 200, 'left': 80},
        axis='x',
        w=240,
        p='md',
        withBorder=True,
        shadow='md',
        radius='md',
    )


def constrain_window() -> Component:
    """Keep the window inside the viewport with an offset."""
    return dmc.FloatingWindow(
        dmc.Text('Try dragging me past the edges.', size='sm'),
        id=window_id('constrain'),
        initialPosition={'top': 160, 'right': 80},
        constrainToViewport=True,
        constrainOffset=24,
        w=240,
        p='md',
        withBorder=True,
        shadow='md',
        radius='md',
    )


def resize_window() -> Component:
    """Add a FloatingWindowResizeHandle and configure size limits."""
    return dmc.FloatingWindow(
        [
            dmc.Text('Resizable', fw=600),
            dmc.Text('Drag the corner, or focus it and use the arrow keys.', size='sm'),
            dmc.FloatingWindowResizeHandle(
                '◢',
                pos='absolute',
                bottom=0,
                right=0,
                px=4,
                c='dimmed',
                style={'cursor': 'nwse-resize', 'lineHeight': 1},
            ),
        ],
        id=window_id('resize'),
        initialPosition={'top': 140, 'right': 40},
        dimensions={
            'initialWidth': 280,
            'minWidth': 200,
            'maxWidth': 500,
            'initialHeight': 160,
            'minHeight': 100,
            'maxHeight': 400,
        },
        p='md',
        withBorder=True,
        shadow='md',
        radius='md',
    )


def position_window() -> Component:
    """Move the window from a Dash callback."""
    return dmc.FloatingWindow(
        [
            dmc.Text('Move to a corner', fw=600, size='sm'),
            dmc.SimpleGrid(
                [
                    dmc.Button(id=key, children=key[5:], size='xs', variant='default')
                    for key in MOVES
                ],
                cols=2,
                mt='xs',
            ),
        ],
        id=window_id('position'),
        initialPosition={'top': 200, 'left': 200},
        excludeDragHandleSelector='button',
        w=280,
        p='md',
        withBorder=True,
        shadow='md',
        radius='md',
    )


def disabled_window() -> Component:
    """Disable dragging with enabled=False."""
    return dmc.FloatingWindow(
        dmc.Text('Dragging is disabled.', size='sm'),
        id=window_id('disabled'),
        initialPosition={'top': 200, 'right': 80},
        enabled=False,
        w=240,
        p='md',
        withBorder=True,
        shadow='md',
        radius='md',
    )


WINDOWS: dict[str, Callable[[], Component]] = {
    'usage': usage_window,
    'handle': handle_window,
    'axis': axis_window,
    'constrain': constrain_window,
    'resize': resize_window,
    'position': position_window,
    'disabled': disabled_window,
}


@app.callback(
    Output({'type': 'host', 'demo': MATCH}, 'children'),
    Output({'type': 'toggle', 'demo': MATCH}, 'children'),
    Input({'type': 'toggle', 'demo': MATCH}, 'n_clicks'),
)
def toggle_window(clicks: int | None) -> tuple[Component | None, str]:
    """Show or hide the window belonging to the clicked example."""
    opened = clicks is not None and clicks % 2 == 1
    name = ctx.outputs_list[0]['id']['demo']
    return (WINDOWS[name]() if opened else None), ('Hide window' if opened else 'Show window')


@app.callback(
    Output({'type': 'state', 'demo': MATCH}, 'children'),
    Input({'type': 'window', 'demo': MATCH}, 'currentPosition'),
    Input({'type': 'window', 'demo': MATCH}, 'currentSize'),
    Input({'type': 'window', 'demo': MATCH}, 'dragging'),
    Input({'type': 'window', 'demo': MATCH}, 'resizing'),
)
def show_state(
    position: dict[str, Any] | None,
    size: dict[str, Any] | None,
    dragging: bool | None,
    resizing: bool | None,
) -> str:
    """Display the state reported by the window."""
    state = {
        'currentPosition': position,
        'currentSize': size,
        'dragging': dragging,
        'resizing': resizing,
    }
    return '\n'.join(f'{key}: {json.dumps(value)}' for key, value in state.items())


@app.callback(
    Output(window_id('position'), 'position'),
    *[Input(key, 'n_clicks') for key in MOVES],
    prevent_initial_call=True,
)
def move_window(*_clicks: int | None) -> dict[str, int]:
    """Move the window to the corner of the clicked button."""
    return MOVES[ctx.triggered_id]


SECTIONS = [
    Section(
        'usage',
        'Usage',
        'Use `FloatingWindow` for draggable panels that float above the page, such as '
        'inspectors, tool palettes or chat windows. Place the window anywhere in the layout: '
        'it renders in a portal and is positioned relative to the viewport with '
        '`initialPosition`. Click the button to show or hide each example. The readout shows '
        '`currentPosition`, `currentSize`, `dragging` and `resizing` as reported to Dash '
        'callbacks.',
        usage_window,
        (toggle_window, show_state),
        preview=lambda: host('usage'),
    ),
    Section(
        'drag-handle',
        'Drag handle',
        'By default the whole window drags. Set `dragHandleSelector` to a CSS selector to '
        'drag only from that element. Use `excludeDragHandleSelector` to exclude '
        'interactive elements inside the handle.',
        handle_window,
        preview=lambda: host('handle'),
    ),
    Section(
        'axis',
        'Axis',
        'Set `axis` to `x` or `y` to restrict movement to one direction.',
        axis_window,
        preview=lambda: host('axis'),
    ),
    Section(
        'constrain',
        'Constrain to viewport',
        'Set `constrainToViewport=True` to keep the window within the viewport. '
        '`constrainOffset` adds a margin in pixels from each edge.',
        constrain_window,
        preview=lambda: host('constrain'),
    ),
    Section(
        'resize',
        'Resizable window',
        'Add a `FloatingWindowResizeHandle` as a child to make the window resizable. '
        'Position and style the handle with Box props. Configure `dimensions` with initial, '
        'minimum and maximum sizes in pixels. The handle also supports keyboard resizing: '
        'focus it and use the arrow keys. `resizing` is `True` only during pointer resizing.',
        resize_window,
        preview=lambda: host('resize'),
    ),
    Section(
        'position',
        'Set position from a callback',
        'Return a dict with one horizontal (`left` or `right`) and one vertical (`top` or '
        '`bottom`) edge, in pixels, to the `position` prop to move the window. '
        '`currentPosition` reports the resulting `x` and `y`.',
        position_window,
        (move_window,),
        preview=lambda: host('position'),
    ),
    Section(
        'disabled',
        'Disable dragging',
        'Set `enabled=False` to prevent dragging.',
        disabled_window,
        preview=lambda: host('disabled'),
    ),
]

app.layout = page_layout(
    'FloatingWindow',
    'Overlays',
    'Display content in a draggable, optionally resizable window.',
    'This page demonstrates the DMC FloatingWindow feature in the `dev` branch of the fork. '
    'Refer to [Mantine FloatingWindow](https://mantine.dev/core/floating-window/) for the '
    'underlying component API. Each example uses the shared `host`, `toggle_window` and '
    '`show_state` helpers; the source panels show the window and its callbacks. Windows '
    'also accept Paper props such as `withBorder`, `shadow` and `radius`, plus '
    '`withinPortal`, `portalProps` and `zIndex`.',
    SECTIONS,
)
# Windows are mounted by toggle_window, but their IDs must be known before they open.
# Dash 4.5 incorrectly infers this public attribute's type as None.
app.validation_layout = html.Div(  # type: ignore[assignment]
    [app.layout, *[factory() for factory in WINDOWS.values()]]
)

if __name__ == '__main__':
    app.run(debug=True)
