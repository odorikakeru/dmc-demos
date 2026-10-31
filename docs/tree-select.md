# TreeSelect

`TreeSelect` lets users choose values from hierarchical data. It supports single
selection, multiple selection, and checkbox selection with parent-child cascading.
See the [Mantine TreeSelect documentation](https://mantine.dev/core/tree-select/) for
the underlying component.

## Usage

Pass `data` as a list of nodes. Each node needs a unique string `value` and a `label`;
nodes can contain nested `children`.

```python
import dash_mantine_components as dmc

data = [
    {
        'value': 'fruits',
        'label': 'Fruits',
        'children': [
            {'value': 'apple', 'label': 'Apple'},
            {'value': 'banana', 'label': 'Banana'},
        ],
    },
    {'value': 'milk', 'label': 'Milk'},
]

dmc.TreeSelect(
    data=data,
    label='Favorite item',
    placeholder='Pick a value',
)
```

In single mode, `value` is a string or `None`. In multiple and checkbox modes, it is a
list of strings. The value can be controlled with a Dash callback:

```python
import dash_mantine_components as dmc
from dash import Dash, Input, Output, callback, html

app = Dash()
app.layout = html.Div(
    [
        dmc.TreeSelect(id='tree-select', data=data),
        html.Div(id='selected-value'),
    ]
)


@callback(Output('selected-value', 'children'), Input('tree-select', 'value'))
def show_value(value):
    return str(value)
```

## Selection modes

Set `mode` to choose how values are selected:

- `"single"` (default) selects one node and displays it as an input value.
- `"multiple"` selects multiple nodes and displays them as pills.
- `"checkbox"` displays checkboxes and cascades parent selections to descendants.

In checkbox mode, a parent is indeterminate when only some of its descendants are
checked. `checkStrictly=True` disables cascading. `checkedStrategy` controls which
checked nodes are included in `value` and the pills: `"child"` (default) includes leaf
nodes, `"all"` includes checked parents and children, and `"parent"` includes the
highest fully checked parents. With `checkStrictly=True`, only `"child"` is reliable.

In DMC, a parent node can be selected in single mode when `expandOnClick` is disabled.
With `expandOnClick` enabled, Mantine documents parent clicks as expanding or collapsing
the node instead.

Use `maxValues` to limit selections in multiple and checkbox modes. Use
`maxDisplayedValues` to limit the number of visible pills; `maxDisplayedValuesContent`
customizes the overflow indicator.

## Search

Set `searchable=True` to filter nodes. Matching nodes and their ancestors remain visible.
Set `nothingFoundMessage` to show content when no nodes match. `searchValue` can be
controlled with callbacks, and `clearSearchOnChange` and `clearSearchOnFocus` control
when the search text is cleared.

The `filter` function receives `(query, node)` and returns whether that node matches.
Parents of matching nodes are kept. Function props use the
[DMC functions-as-props convention](https://www.dash-mantine-components.com/functions-as-props).

## Expansion and navigation

`expandedValues` controls which nodes are expanded and is updated when the user expands
or collapses nodes. Set `defaultExpandAll=True` to expand every node initially.
`expandOnClick=True` also toggles a parent when its label is clicked. `withLines` shows
connecting lines between parent and child nodes (enabled by default).

When the dropdown is open, keyboard navigation supports arrow keys to move through
nodes and expand or collapse parents, and Enter to select the highlighted node.

## Custom node and pill content

`renderNode` customizes each node in the dropdown. It receives the node and its state,
including `level`, `expanded`, `hasChildren`, `selected`, `checked`, `indeterminate`,
and an `expand` function.

`renderPill` customizes pills in multiple and checkbox modes. Its payload includes the
node, value, `onRemove`, and disabled state. It does not customize the overflow pill;
use `maxDisplayedValuesContent` for that. These props accept functions using the
[DMC functions-as-props convention](https://www.dash-mantine-components.com/functions-as-props).

## Dropdown

The dropdown uses `ScrollArea.Autosize` by default. Set `maxDropdownHeight` or
`scrollAreaProps` to control its scrolling area. `comboboxProps` passes options to the
underlying Combobox and Popover, including `withinPortal`, `position`, `middlewares`,
`width`, `offset`, `transitionProps`, padding, and shadow.

`dropdownOpened` controls and reports whether the dropdown is open. `onDropdownOpen`
and `onDropdownClose` can also be used in callbacks.

## Input options

TreeSelect supports the standard Mantine input props, including `label`, `description`,
`placeholder`, `leftSection`, `rightSection`, `error`, `disabled`, and `readOnly`.
`clearable=True` displays a button to clear the selection. `allowDeselect` controls
whether the selected value can be deselected in single mode.

**Known limitation:** Mantine 9.7 can trigger a value change for a selected pill when
Backspace is pressed even if `readOnly` is set. DMC guards the value update, but this
interaction is not fully supported.

## Styling

Use the standard DMC `styles` and `classNames` props to customize TreeSelect styles.
The [Mantine TreeSelect documentation](https://mantine.dev/core/tree-select/) lists the
underlying component's styles API.
