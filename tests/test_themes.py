"""Test theme support."""

import pytest
from markdown_pdf_renderer.markdown_parser import MarkdownParser
from markdown_pdf_renderer.styles import get_default_css, get_dark_css


class TestThemes:
    def test_default_theme(self):
        parser = MarkdownParser(theme="default")
        assert parser.css == get_default_css()

    def test_dark_theme(self):
        parser = MarkdownParser(theme="dark")
        assert parser.css == get_dark_css()

    def test_custom_css_overrides_theme(self):
        custom_css = "body { background: red; }"
        parser = MarkdownParser(css=custom_css, theme="dark")
        assert parser.css == custom_css

    def test_dark_theme_colors(self):
        parser = MarkdownParser(theme="dark")
        css = parser.css
        assert "#1e1e1e" in css
        assert "#d4d4d4" in css

    def test_default_theme_colors(self):
        parser = MarkdownParser(theme="default")
        css = parser.css
        assert "#ffffff" in css or "#333333" in css
