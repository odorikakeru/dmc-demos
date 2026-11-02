"""Interactive TreeSelect documentation built with Dash Mantine Components."""

import inspect
import json
from collections.abc import Callable
from pathlib import Path
from pprint import pformat
from typing import Literal, TypedDict

import dash_mantine_components as dmc
from dash import ALL, Dash, Input, Output, _dash_renderer, callback, ctx, dcc, html
from dash.development.base_component import Component

_dash_renderer._set_react_version('19.2.4')

AriaLabel = TypedDict('AriaLabel', {'aria-label': str})
STRATEGIES: tuple[Literal['child', 'all', 'parent'], ...] = ('child', 'all', 'parent')
DATA: list[dmc.TreeSelect.Data] = [
    {
        'value': 'produce',
        'label': 'Produce',
        'children': [
            {
                'value': 'fruit',
                'label': 'Fruit',
                'children': [
                    {'value': 'apple', 'label': 'Apple'},
                    {'value': 'banana', 'label': 'Banana'},
                    {'value': 'orange', 'label': 'Orange'},
                ],
            },
            {
                'value': 'vegetables',
                'label': 'Vegetables',
                'children': [
                    {'value': 'carrot', 'label': 'Carrot'},
                    {'value': 'broccoli', 'label': 'Broccoli'},
                ],
            },
        ],
    },
    {
        'value': 'bakery',
        'label': 'Bakery',
        'children': [
            {'value': 'bread', 'label': 'Bread'},
            {'value': 'croissant', 'label': 'Croissant'},
        ],
    },
    {'value': 'milk', 'label': 'Milk'},
]
BRANCHES = ['produce', 'fruit', 'vegetables', 'bakery']
ASSETS = Path(__file__).parent / 'assets'


def selection_id(name: str) -> dict[str, str]:
    """Identify a demo whose selected value is shown below the input."""
    return {'type': 'selection', 'demo': name}


def value_output(name: str) -> Component:
    """Show the actual JSON value published by a TreeSelect."""
    return html.Div(
        [
            dmc.Text('Selected value', size='xs', c='dimmed'),
            html.Pre(id={'type': 'value', 'demo': name}, className='value-output'),
        ],
        className='value-panel',
        role='status',
    )


def simple_example() -> Component:
    """Single selection with a Dash value callback."""
    return dmc.Stack(
        [
            dmc.TreeSelect(
                id=selection_id('simple'),
                data=DATA,
                label='Your favorite item',
                placeholder='Pick an item',
                value='apple',
                expandedValues=['produce', 'fruit'],
            ),
            value_output('simple'),
        ]
    )


def multiple_example() -> Component:
    """Select multiple nodes and display them as removable pills."""
    return dmc.Stack(
        [
            dmc.TreeSelect(
                id=selection_id('multiple'),
                data=DATA,
                mode='multiple',
                label='Shopping list',
                placeholder='Pick items',
                value=['apple', 'bread'],
                defaultExpandAll=True,
                clearable=True,
            ),
            value_output('multiple'),
        ]
    )


def checkbox_example() -> Component:
    """Compare cascading checkbox selection and independent checks."""
    return dmc.SimpleGrid(
        [
            dmc.Stack(
                [
                    dmc.TreeSelect(
                        id=selection_id('cascade'),
                        data=DATA,
                        mode='checkbox',
                        label='Cascading selection',
                        description='Check Fruit to select all its descendants.',
                        value=['apple'],
                        defaultExpandAll=True,
                        clearable=True,
                    ),
                    value_output('cascade'),
                ]
            ),
            dmc.Stack(
                [
                    dmc.TreeSelect(
                        id=selection_id('strict'),
                        data=DATA,
                        mode='checkbox',
                        checkStrictly=True,
                        checkedStrategy='child',
                        label='Independent selection',
                        description='Parent and child checks are independent.',
                        value=['fruit'],
                        defaultExpandAll=True,
                        clearable=True,
                    ),
                    value_output('strict'),
                ]
            ),
        ],
        cols={'base': 1, 'sm': 2},
    )


def strategy_example() -> Component:
    """Compare the three checkbox value strategies side by side."""
    return dmc.SimpleGrid(
        [
            dmc.Stack(
                [
                    dmc.TreeSelect(
                        id=selection_id(strategy),
                        data=DATA,
                        mode='checkbox',
                        checkedStrategy=strategy,
                        label=f"checkedStrategy='{strategy}'",
                        placeholder='Check a parent',
                        defaultExpandAll=True,
                        value=[],
                    ),
                    value_output(strategy),
                ]
            )
            for strategy in STRATEGIES
        ],
        cols={'base': 1, 'md': 3},
    )


def search_example() -> Component:
    """Search the tree while preserving ancestors of matching nodes."""
    return dmc.Stack(
        [
            dmc.TreeSelect(
                id=selection_id('search'),
                data=DATA,
                label='Search items',
                placeholder='Try apple, or a name that does not exist',
                searchable=True,
                nothingFoundMessage='No matching items',
                clearSearchOnChange=True,
                clearSearchOnFocus=False,
                clearable=True,
            ),
            value_output('search'),
            dmc.Text(id='search-state', size='sm', c='dimmed'),
        ]
    )


def clearable_example() -> Component:
    """Clear a selection or prevent deselection of the selected node."""
    return dmc.SimpleGrid(
        [
            dmc.TreeSelect(
                data=DATA,
                label='Clearable selection',
                value='apple',
                clearable=True,
            ),
            dmc.TreeSelect(
                data=DATA,
                label='Deselect disabled',
                description='Selecting Milk again keeps it selected.',
                value='milk',
                allowDeselect=False,
            ),
        ],
        cols={'base': 1, 'sm': 2},
    )


def limits_example() -> Component:
    """Limit selection count separately from the visible pill count."""
    return dmc.Stack(
        [
            dmc.TreeSelect(
                id=selection_id('limits'),
                data=DATA,
                mode='multiple',
                label='Pick up to 4 items',
                description='Only 2 pills are visible; remove one to make room.',
                value=['apple', 'banana', 'bread'],
                maxValues=4,
                maxDisplayedValues=2,
                maxDisplayedValuesContent={'function': 'treeOverflow'},
                defaultExpandAll=True,
                clearable=True,
            ),
            value_output('limits'),
        ]
    )


def expansion_example() -> Component:
    """Control expansion from Dash and display the reported expanded nodes."""
    return dmc.Stack(
        [
            dmc.Group(
                [
                    dmc.Button('Expand all', id='expand-all', variant='light', size='xs'),
                    dmc.Button('Collapse all', id='collapse-all', variant='default', size='xs'),
                ]
            ),
            dmc.TreeSelect(
                id='expansion-tree',
                data=DATA,
                label='Browse the hierarchy',
                placeholder='Click a branch label to expand it',
                expandedValues=[],
                expandOnClick=True,
                withLines=True,
            ),
            dmc.Text(id='expansion-state', size='sm', c='dimmed'),
            dmc.TreeSelect(
                data=DATA,
                label='Without connecting lines',
                withLines=False,
                defaultExpandAll=True,
            ),
        ]
    )


def custom_example() -> Component:
    """Use JavaScript functions for node content and removable pills."""
    return dmc.Stack(
        [
            dmc.TreeSelect(
                id=selection_id('custom'),
                data=DATA,
                mode='multiple',
                label='Custom nodes and pills',
                description='Branches show item counts; pills use a custom remove button.',
                value=['apple', 'bread'],
                defaultExpandAll=True,
                renderNode={'function': 'treeNode'},
                renderPill={'function': 'treePill'},
            ),
            value_output('custom'),
            dmc.TreeSelect(
                data=DATA,
                label='Custom filter',
                description='Match the start of a label or its internal value.',
                placeholder='Try veg',
                searchable=True,
                filter={'function': 'treeFilter'},
                nothingFoundMessage='No matching items',
            ),
        ]
    )


def dropdown_example() -> Component:
    """Configure scrolling, placement and the controlled dropdown state."""
    # Mantine supplies mounted; DMC's generated type incorrectly requires it.
    transition: dmc.TreeSelect.ComboboxPropsTransitionProps = {  # type: ignore[typeddict-item]
        'transition': 'pop',
        'duration': 150,
    }
    return dmc.Stack(
        [
            dmc.Switch(id='dropdown-toggle', label='Dropdown open', checked=False),
            dmc.TreeSelect(
                id='dropdown-tree',
                data=DATA,
                label='Configured dropdown',
                placeholder='Browse items',
                defaultExpandAll=True,
                maxDropdownHeight=180,
                scrollAreaProps={'type': 'always', 'scrollbarSize': 6},
                dropdownOpened=False,
                comboboxProps={
                    'withinPortal': False,
                    'position': 'bottom-start',
                    'offset': 8,
                    'width': 300,
                    'shadow': 'md',
                    'dropdownPadding': 8,
                    'zIndex': 200,
                    'transitionProps': transition,
                },
            ),
            dmc.Text(id='dropdown-state', size='sm', c='dimmed'),
        ]
    )


def input_example() -> Component:
    """Demonstrate input styling, sections and validation states."""
    return dmc.SimpleGrid(
        [
            dmc.TreeSelect(
                data=DATA,
                label='Input label',
                description='Standard Input and Input.Wrapper props are supported.',
                placeholder='Choose an item',
                withAsterisk=True,
                size='md',
                radius='md',
                variant='filled',
                leftSection=dmc.Text('#', c='blue', size='sm'),
                leftSectionPointerEvents='none',
                rightSection=dmc.Text('kg', size='xs', c='dimmed'),
                rightSectionWidth=36,
                rightSectionPointerEvents='none',
            ),
            dmc.TreeSelect(
                data=DATA,
                label='Error state',
                placeholder='Choose an item',
                error='Select an item before continuing.',
            ),
            dmc.TreeSelect(data=DATA, label='Read only', value='apple', readOnly=True),
            dmc.TreeSelect(data=DATA, label='Disabled', value='apple', disabled=True),
            dmc.TreeSelect(
                data=DATA,
                label='Custom styles',
                value='milk',
                success='Looks good!',
                styles={'input': {'borderColor': 'var(--mantine-color-teal-6)'}},
                description='Use styles or classNames to target component parts.',
            ),
            dmc.TreeSelect(
                data=DATA,
                placeholder='Accessible without a visible label',
                **AriaLabel({'aria-label': 'Item without a visible label'}),
            ),
        ],
        cols={'base': 1, 'sm': 2},
    )


@callback(
    Output({'type': 'value', 'demo': ALL}, 'children'),
    Input({'type': 'selection', 'demo': ALL}, 'value'),
)
def show_values(values: list[str | list[str] | None]) -> list[str]:
    """Publish JSON without converting empty selections into placeholder values."""
    return [json.dumps(value) for value in values]


@callback(Output('search-state', 'children'), Input(selection_id('search'), 'searchValue'))
def show_search(query: str | None) -> str:
    """Display search text reported by the component."""
    return f'searchValue: {json.dumps(query)}'


@callback(
    Output('expansion-tree', 'expandedValues'),
    Input('expand-all', 'n_clicks'),
    Input('collapse-all', 'n_clicks'),
    prevent_initial_call=True,
)
def set_expansion(_expand: int | None, _collapse: int | None) -> list[str]:
    """Expand or collapse the same controlled TreeSelect."""
    return BRANCHES if ctx.triggered_id == 'expand-all' else []


@callback(Output('expansion-state', 'children'), Input('expansion-tree', 'expandedValues'))
def show_expansion(values: list[str]) -> str:
    """Display expansion changes from both the tree and the buttons."""
    return f'expandedValues: {json.dumps(values)}'


@callback(
    Output('dropdown-tree', 'dropdownOpened'),
    Output('dropdown-toggle', 'checked'),
    Input('dropdown-toggle', 'checked'),
    Input('dropdown-tree', 'dropdownOpened'),
)
def set_dropdown(checked: bool, opened: bool) -> tuple[bool, bool]:
    """Keep the external control synchronized with the actual dropdown state."""
    value = opened if ctx.triggered_id == 'dropdown-tree' else checked
    return value, value


@callback(Output('dropdown-state', 'children'), Input('dropdown-tree', 'dropdownOpened'))
def show_dropdown(opened: bool) -> str:
    """Report actual dropdown state, including clicks outside and Escape."""
    return f'dropdownOpened: {json.dumps(opened)}'


def markdown(text: str) -> Component:
    """Render concise documentation with Python syntax highlighting."""
    return dcc.Markdown(text, className='docs-markdown')


def example_section(
    slug: str,
    title: str,
    description: str,
    factory: Callable[[], Component],
    callbacks: tuple[Callable, ...] = (),
    javascript: bool = False,
) -> Component:
    """Pair a live example with the exact source used to construct it."""
    source = '\n\n'.join(inspect.getsource(function) for function in (factory, *callbacks))
    sources = [markdown(f'```python\n{source}\n```')]
    if javascript:
        sources.append(
            markdown(
                f'```javascript\n{(ASSETS / "tree-select.js").read_text(encoding="utf-8")}\n```'
            )
        )
    return html.Section(
        [
            dmc.Title(dmc.Anchor(title, href=f'#{slug}', c='inherit'), order=2),
            markdown(description),
            dmc.Paper(
                [
                    html.Div(factory(), className='demo-preview'),
                    dmc.Accordion(
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl('View source'),
                                dmc.AccordionPanel(sources),
                            ],
                            value='source',
                        ),
                        variant='default',
                        className='demo-source',
                    ),
                ],
                withBorder=True,
                radius='md',
            ),
        ],
        id=slug,
        className='doc-section',
    )


SECTIONS: list[tuple[str, str, str, Callable[[], Component], tuple[Callable, ...], bool]] = [
    (
        'usage',
        'Simple example',
        'Select an item from nested data. The value below updates through a Dash callback. '
        'Single mode returns a string or `None`; multiple and checkbox modes return a list.',
        simple_example,
        (show_values,),
        False,
    ),
    (
        'multiple',
        'Multiple selection',
        'Set `mode="multiple"` to select several items. Remove a pill with its close button '
        'or Backspace. `clearable=True` clears the complete selection.',
        multiple_example,
        (),
        False,
    ),
    (
        'checkbox',
        'Checkbox selection',
        'Set `mode="checkbox"` for parent-child cascading. A partially selected parent is '
        'indeterminate. Use `checkStrictly=True` with `checkedStrategy="child"` for independent '
        'checks; other strategies recompute the hierarchy and are not reliable in strict mode.',
        checkbox_example,
        (),
        False,
    ),
    (
        'strategies',
        'Checked strategy',
        '`checkedStrategy` controls the returned values and pills. Check Fruit in each example: '
        '`child` returns its leaves, `all` includes checked parents and children, and `parent` '
        'returns only the highest fully checked parents.',
        strategy_example,
        (),
        False,
    ),
    (
        'search',
        'Searchable',
        'Set `searchable=True` to filter nodes while retaining matching ancestors. '
        '`nothingFoundMessage` handles empty results. `searchValue` can be controlled through '
        'callbacks; `clearSearchOnChange` and `clearSearchOnFocus` control when text is cleared.',
        search_example,
        (show_search,),
        False,
    ),
    (
        'clearable',
        'Clearable and deselection',
        '`clearable` adds a clear button. `allowDeselect=False` prevents selecting the same '
        'node again from removing it in single mode.',
        clearable_example,
        (),
        False,
    ),
    (
        'limits',
        'Selection and pill limits',
        '`maxValues` limits selected values in multiple and checkbox modes. '
        '`maxDisplayedValues` only limits visible pills; the full value is preserved. '
        '`maxDisplayedValuesContent` customizes the overflow indicator.',
        limits_example,
        (),
        True,
    ),
    (
        'expansion',
        'Expansion and connecting lines',
        '`expandedValues` controls and reports expanded branches. Use `defaultExpandAll=True` '
        'for initial expansion when no controlled expansion is supplied. `expandOnClick=True` '
        'makes branch labels toggle expansion instead of selection. `withLines=False` hides '
        'the connecting lines.',
        expansion_example,
        (set_expansion, show_expansion),
        False,
    ),
    (
        'custom',
        'Custom nodes, pills and filtering',
        'Use named JavaScript functions for `renderNode`, `renderPill`, and `filter`. '
        '`renderNode` receives the node and its state, including `level`, `expanded`, '
        '`hasChildren`, `selected`, `checked`, `indeterminate`, and `expand`. '
        '`renderPill` receives `node`, `value`, `onRemove`, and `disabled`. '
        'Call `onRemove` from the custom pill. The filter receives `(query, node)`.\n\n'
        'See [Functions as Props](https://www.dash-mantine-components.com/functions-as-props).',
        custom_example,
        (),
        True,
    ),
    (
        'dropdown',
        'Dropdown configuration',
        'Use `maxDropdownHeight` and `scrollAreaProps` for scrolling. `comboboxProps` configures '
        'portal rendering, position, width, offset, z-index, padding, shadow and transitions. '
        'The switch controls `dropdownOpened` and stays synchronized when the dropdown '
        'closes with Escape or a click outside. The readout reports the actual state.',
        dropdown_example,
        (set_dropdown, show_dropdown),
        False,
    ),
    (
        'input',
        'Input props and styles',
        'TreeSelect supports standard input props, including labels, descriptions, sections, '
        'size, radius, variant, error, success, disabled, and readOnly. '
        'Use `styles` or `classNames` for customization. '
        'Always provide a `label` or an `aria-label`.\n\n'
        '**Read-only note:** DMC guards value updates, but Mantine 9.7 does not fully support '
        'Backspace interaction with read-only pills.',
        input_example,
        (),
        False,
    ),
]

app = Dash(__name__, title='TreeSelect | Dash Mantine Components')
app.layout = dmc.MantineProvider(
    html.Div(
        [
            html.Header(
                dmc.Group(
                    [
                        html.Div('D', className='brand-mark'),
                        dmc.Text('Dash Mantine Components', fw=700),
                        dmc.Badge('Component demos', variant='light'),
                    ]
                ),
                className='topbar',
            ),
            html.Div(
                [
                    html.Main(
                        [
                            dmc.Text('Components / Combobox', c='dimmed', size='sm'),
                            dmc.Title('TreeSelect', order=1, mt='md'),
                            dmc.Text(
                                'Select one or more values from hierarchical data.',
                                c='dimmed',
                                size='lg',
                                mt='xs',
                                mb='xl',
                            ),
                            dmc.Alert(
                                markdown(
                                    'This page demonstrates the DMC TreeSelect feature branch. '
                                    'Start with the examples below, then refer to '
                                    '[Mantine TreeSelect](https://mantine.dev/core/tree-select/) '
                                    'for the underlying component API.'
                                ),
                                title='About this component',
                                variant='light',
                                mb='xl',
                            ),
                            html.Section(
                                [
                                    dmc.Title('Data format', order=2),
                                    markdown(
                                        'Use a list of nodes with a unique string `value` and a '
                                        '`label`. Nest nodes with `children`. All examples use '
                                        '`DATA` below. Import `dash_mantine_components as dmc` '
                                        'and `from dash import Input, Output, callback`.\n\n'
                                        'The source panels show the actual example functions. '
                                        '`selection_id` and `value_output` are shared helpers '
                                        'for the live JSON readouts; see the app source for '
                                        'their definitions.'
                                    ),
                                    dmc.Accordion(
                                        dmc.AccordionItem(
                                            [
                                                dmc.AccordionControl('View shared data'),
                                                dmc.AccordionPanel(
                                                    markdown(
                                                        '```python\nDATA = '
                                                        + pformat(DATA, width=80, sort_dicts=False)
                                                        + '\n```'
                                                    )
                                                ),
                                            ],
                                            value='data',
                                        ),
                                        variant='contained',
                                    ),
                                ],
                                id='data',
                                className='doc-section',
                            ),
                            *[example_section(*section) for section in SECTIONS],
                            html.Section(
                                [
                                    dmc.Title('Keyboard navigation', order=2),
                                    markdown(
                                        'Focus an input with Tab and open its dropdown. '
                                        'Use **Up / Down** to move between nodes, **Right** '
                                        'to expand a branch, **Left** to collapse it or move '
                                        'to its parent, **Enter** to select, and **Escape** '
                                        'to close. Try these controls in any example above.'
                                    ),
                                ],
                                id='keyboard',
                                className='doc-section',
                            ),
                        ],
                        className='page-content',
                        id='component-docs',
                    ),
                    html.Aside(
                        [
                            dmc.Text('On this page', fw=600, size='sm', mb='sm'),
                            dmc.Anchor('Data format', href='#data', size='sm'),
                            *[
                                dmc.Anchor(title, href=f'#{slug}', size='sm')
                                for slug, title, *_ in SECTIONS
                            ],
                            dmc.Anchor('Keyboard navigation', href='#keyboard', size='sm'),
                        ],
                        className='table-of-contents',
                    ),
                ],
                className='docs-layout',
            ),
            html.Footer(
                dmc.Text('TreeSelect / Dash Mantine Components', size='sm', c='dimmed'),
                className='page-footer',
            ),
        ]
    )
)

if __name__ == '__main__':
    app.run(debug=True)
