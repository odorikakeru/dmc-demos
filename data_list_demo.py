"""Interactive DataList documentation built with Dash Mantine Components."""

import dash_mantine_components as dmc
from dash import Dash, _dash_renderer
from dash.development.base_component import Component

from demo_page import Section, page_layout

_dash_renderer._set_react_version('19.2.4')

ORDER = [
    ('Order number', '#10482'),
    ('Customer', 'Ada Lovelace'),
    ('Shipping method', 'Express'),
    ('Total', '$128.40'),
]


def order_items() -> list[Component]:
    """Build one DataListItem per label and value pair."""
    return [
        dmc.DataListItem([dmc.DataListItemLabel(label), dmc.DataListItemValue(value)])
        for label, value in ORDER
    ]


def usage_example() -> Component:
    """Pair each label with a value."""
    return dmc.DataList(order_items())


def orientation_example() -> Component:
    """Place labels beside or above their values."""
    return dmc.SimpleGrid(
        [
            dmc.Stack([dmc.Text('horizontal', size='sm', c='dimmed'), dmc.DataList(order_items())]),
            dmc.Stack(
                [
                    dmc.Text('vertical', size='sm', c='dimmed'),
                    dmc.DataList(order_items(), orientation='vertical'),
                ]
            ),
        ],
        cols={'base': 1, 'sm': 2},
    )


def divider_example() -> Component:
    """Separate items with a border."""
    return dmc.DataList(order_items(), withDivider=True)


def size_example() -> Component:
    """Compare the available sizes."""
    return dmc.Stack(
        [
            dmc.Stack(
                [
                    dmc.Text(f"size='{size}'", size='sm', c='dimmed'),
                    dmc.DataList(order_items()[:2], size=size),
                ],
                gap='xs',
            )
            for size in ('xs', 'sm', 'md', 'lg', 'xl')
        ]
    )


def gap_example() -> Component:
    """Control spacing with a theme key or any CSS value."""
    return dmc.SimpleGrid(
        [
            dmc.Stack(
                [
                    dmc.Text(f'gap={gap!r}', size='sm', c='dimmed'),
                    dmc.DataList(order_items(), gap=gap),
                ]
            )
            for gap in ('xs', 'xl', 40)
        ],
        cols={'base': 1, 'md': 3},
    )


def label_width_example() -> Component:
    """Align values by setting the minimum label width."""
    return dmc.DataList(order_items(), labelWidth=200, withDivider=True)


def content_example() -> Component:
    """Use any Dash component as a label or value."""
    return dmc.DataList(
        [
            dmc.DataListItem(
                [
                    dmc.DataListItemLabel('Status'),
                    dmc.DataListItemValue(dmc.Badge('Shipped', color='green', variant='light')),
                ]
            ),
            dmc.DataListItem(
                [
                    dmc.DataListItemLabel('Customer'),
                    dmc.DataListItemValue(
                        dmc.Group(
                            [dmc.Avatar('AL', size='sm', radius='xl'), dmc.Text('Ada Lovelace')],
                            gap='xs',
                        )
                    ),
                ]
            ),
            dmc.DataListItem(
                [
                    dmc.DataListItemLabel('Tracking'),
                    dmc.DataListItemValue(
                        dmc.Anchor('1Z999AA10123456784', href='https://www.ups.com/track')
                    ),
                ]
            ),
        ],
        withDivider=True,
    )


def styles_example() -> Component:
    """Customize parts with style props and the Styles API."""
    return dmc.DataList(
        order_items(),
        withDivider=True,
        styles={
            'itemLabel': {'color': 'var(--mantine-color-blue-6)', 'fontWeight': 600},
            'itemValue': {'fontFamily': 'monospace'},
        },
        p='md',
        bg='var(--mantine-color-gray-0)',
        bdrs='md',
    )


SECTIONS = [
    Section(
        'usage',
        'Usage',
        'Wrap `DataListItemLabel` and `DataListItemValue` in a `DataListItem`, then place the '
        'items in a `DataList`. The component renders semantic `dl`, `dt` and `dd` elements '
        'and is a good fit for key-value details.',
        usage_example,
    ),
    Section(
        'orientation',
        'Orientation',
        'Set `orientation` to `horizontal` (default) to show labels beside values, or '
        '`vertical` to stack each label above its value.',
        orientation_example,
    ),
    Section(
        'divider',
        'With divider',
        'Set `withDivider=True` to add a border between items.',
        divider_example,
    ),
    Section(
        'size',
        'Size',
        '`size` controls `font-size` and `line-height`. Use `xs`, `sm` (default), `md`, `lg` '
        'or `xl`.',
        size_example,
    ),
    Section(
        'gap',
        'Gap',
        '`gap` sets the space between items. Use a key of `theme.spacing`, or any CSS value '
        'such as a number of pixels.',
        gap_example,
    ),
    Section(
        'label-width',
        'Label width',
        '`labelWidth` sets the minimum width of the label so that values line up. The default '
        'is `120px`. Numbers are treated as pixels.',
        label_width_example,
    ),
    Section(
        'content',
        'Custom content',
        'Labels and values accept any Dash component, such as badges, avatars and links.',
        content_example,
    ),
    Section(
        'styles',
        'Styles API',
        'Use `styles` or `classNames` with the `root`, `item`, `itemLabel` and `itemValue` '
        'selectors, or pass style props such as `p`, `bg` and `bdrs` to the root.',
        styles_example,
    ),
]

app = Dash(__name__, title='DataList | Dash Mantine Components')
app.layout = page_layout(
    'DataList',
    'Data display',
    'Display key-value pairs as a semantic description list.',
    'This page demonstrates the DMC DataList feature in the `dev` branch of the fork. '
    'Refer to [Mantine DataList](https://mantine.dev/core/data-list/) for the underlying '
    'component API. Import `dash_mantine_components as dmc`; the source panels show the '
    'actual example functions, which share the `ORDER` data and `order_items` helper.',
    SECTIONS,
)

if __name__ == '__main__':
    app.run(debug=True)
