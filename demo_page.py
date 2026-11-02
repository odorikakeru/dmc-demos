"""Shared documentation page layout for the component demo scripts."""

import inspect
from collections.abc import Callable
from typing import NamedTuple

import dash_mantine_components as dmc
from dash import dcc, html
from dash.development.base_component import Component


class Section(NamedTuple):
    """A documented example and the functions shown as its source.

    `preview` renders the live example when it differs from the `factory` shown as source.
    """

    slug: str
    title: str
    description: str
    factory: Callable[[], Component]
    callbacks: tuple[Callable, ...] = ()
    preview: Callable[[], Component] | None = None


def markdown(text: str) -> Component:
    """Render concise documentation with Python syntax highlighting."""
    return dcc.Markdown(text, className='docs-markdown')


def example_section(section: Section) -> Component:
    """Pair a live example with the exact source used to construct it."""
    source = '\n\n'.join(
        inspect.getsource(function) for function in (section.factory, *section.callbacks)
    )
    return html.Section(
        [
            dmc.Title(dmc.Anchor(section.title, href=f'#{section.slug}', c='inherit'), order=2),
            markdown(section.description),
            dmc.Paper(
                [
                    html.Div((section.preview or section.factory)(), className='demo-preview'),
                    dmc.Accordion(
                        dmc.AccordionItem(
                            [
                                dmc.AccordionControl('View source'),
                                dmc.AccordionPanel(markdown(f'```python\n{source}\n```')),
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
        id=section.slug,
        className='doc-section',
    )


def page_layout(
    name: str,
    category: str,
    summary: str,
    about: str,
    sections: list[Section],
) -> Component:
    """Build a documentation page with a table of contents."""
    return dmc.MantineProvider(
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
                                dmc.Text(f'Components / {category}', c='dimmed', size='sm'),
                                dmc.Title(name, order=1, mt='md'),
                                dmc.Text(summary, c='dimmed', size='lg', mt='xs', mb='xl'),
                                dmc.Alert(
                                    markdown(about),
                                    title='About this component',
                                    variant='light',
                                    mb='xl',
                                ),
                                *[example_section(section) for section in sections],
                            ],
                            className='page-content',
                            id='component-docs',
                        ),
                        html.Aside(
                            [
                                dmc.Text('On this page', fw=600, size='sm', mb='sm'),
                                *[
                                    dmc.Anchor(section.title, href=f'#{section.slug}', size='sm')
                                    for section in sections
                                ],
                            ],
                            className='table-of-contents',
                        ),
                    ],
                    className='docs-layout',
                ),
                html.Footer(
                    dmc.Text(f'{name} / Dash Mantine Components', size='sm', c='dimmed'),
                    className='page-footer',
                ),
            ]
        )
    )
