from IPython.display import Markdown, HTML
import pytest
from xdmod_data.report import set_styles, header, footer


def test_set_styles():
    style_html = set_styles()
    assert isinstance(style_html, HTML)


@pytest.mark.parametrize(
    'docmeta',
    [
        [None],
        [
            {
                'title': 'ACCESS Utilization',
                'version': 3,
                'description': (
                    'This report describes utilization information for'
                    + ' ACCESS-allocated compute resources.'
                ),
                'history': [
                    ['1', '2024-10-23', 'Initial Version.'],
                    ['2', '2025-01-15', 'Updated time range for plots.'],
                    [
                        '3',
                        '2025-04-03',
                        'Fix typographic errors, update plot times and'
                        + ' resource specification for Stampede2.',
                    ],
                ],
            },
        ],
    ],
    ids=['without_docmeta', 'with_docmeta'],
)
def test_header(docmeta):
    header_html = header(docmeta)
    assert isinstance(header_html, HTML)


def test_footer():
    footer_markdown = footer()
    assert isinstance(footer_markdown, Markdown)
