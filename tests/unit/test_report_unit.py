from IPython.display import HTML
from xdmod_data.report import set_styles, header, footer


def test_set_styles():
    style_html = set_styles()
    assert isinstance(style_html, HTML)


def test_header():
    header_html = header()
    assert isinstance(header_html, HTML)


def test_footer():
    footer_html = footer()
    assert isinstance(footer_html, HTML)
