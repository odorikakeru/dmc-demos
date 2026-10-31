"""Local documentation app for Dash Mantine Components demos."""

from pathlib import Path

from dash import Dash, dcc, html

DOCS_PATH = Path(__file__).parent / 'docs' / 'tree-select.md'

app = Dash(__name__, title='TreeSelect | Dash Mantine Components')
app.layout = html.Div(
    [
        html.Header(
            [
                html.Div('D', className='brand-mark'),
                html.Div(
                    [
                        html.Strong('Dash Mantine Components'),
                        html.Span('Component demos', className='brand-subtitle'),
                    ],
                    className='brand-copy',
                ),
            ],
            className='topbar',
        ),
        html.Main(
            [
                html.Nav(
                    [
                        html.A('Components', href='#component-docs'),
                        html.Span('/'),
                        html.Span('TreeSelect'),
                    ],
                    className='breadcrumbs',
                ),
                html.Div(
                    [
                        html.H1('TreeSelect'),
                        html.Span('New', className='new-badge'),
                    ],
                    className='title-row',
                ),
                html.P(
                    'Select one or more values from hierarchical data.',
                    className='page-description',
                ),
                html.Section(
                    [
                        html.Div(
                            [
                                html.H2('Interactive preview'),
                                html.P(
                                    [
                                        'Unavailable: the DMC feature branch currently '
                                        'fails to import because its generated ',
                                        html.Code('_imports_'),
                                        ' module is missing. This is a package issue; '
                                        'the component has not been patched or replaced.',
                                    ],
                                    className='warning-copy',
                                ),
                            ],
                            className='preview-warning',
                        ),
                        html.Pre(
                            html.Code(
                                'dmc.TreeSelect(\n'
                                '    data=data,\n'
                                "    label='Favorite item',\n"
                                "    placeholder='Pick a value',\n"
                                ')',
                                className='language-python',
                            ),
                            className='preview-code',
                        ),
                    ],
                    className='preview-panel',
                ),
                html.Article(
                    dcc.Markdown(
                        DOCS_PATH.read_text(encoding='utf-8'),
                        className='docs-markdown',
                        link_target='_blank',
                    ),
                    id='component-docs',
                ),
            ],
            className='page-content',
        ),
        html.Footer(
            'TreeSelect · Dash Mantine Components',
            className='page-footer',
        ),
    ],
    className='site-shell',
)

if __name__ == '__main__':
    app.run(debug=True)
