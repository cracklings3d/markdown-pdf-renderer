"""Test markdown parsing functionality."""

import pytest
from markdown_pdf_renderer.markdown_parser import MarkdownParser


class TestMarkdownParser:
    @pytest.fixture
    def parser(self):
        return MarkdownParser()

    def test_headers(self, parser):
        md = "# Header 1\n## Header 2\n### Header 3"
        html = parser.parse(md)
        assert "<h1" in html
        assert "Header 1" in html
        assert "<h2" in html
        assert "Header 2" in html
        assert "<h3" in html
        assert "Header 3" in html

    def test_paragraphs(self, parser):
        md = "This is a paragraph.\n\nThis is another."
        html = parser.parse(md)
        assert "<p>" in html
        assert "paragraph" in html

    def test_code_block(self, parser):
        md = "```python\nprint('hello')\n```"
        html = parser.parse(md)
        assert "<code" in html
        assert "print('hello')" in html

    def test_inline_code(self, parser):
        md = "Use `print()` function"
        html = parser.parse(md)
        assert "<code" in html
        assert "print()" in html

    def test_bold_italic(self, parser):
        md = "**bold** and *italic*"
        html = parser.parse(md)
        assert "<strong>" in html or "<b>" in html
        assert "<em>" in html or "<i>" in html

    def test_links(self, parser):
        md = "[Click here](https://example.com)"
        html = parser.parse(md)
        assert '<a href="https://example.com"' in html
        assert "Click here" in html

    def test_table(self, parser):
        md = "| Header | Header |\n|--------|--------|\n| Cell   | Cell   |"
        html = parser.parse(md)
        assert "<table" in html
        assert "<th>" in html
        assert "<td>" in html

    def test_blockquote(self, parser):
        md = "> This is a quote"
        html = parser.parse(md)
        assert "<blockquote" in html

    def test_list(self, parser):
        md = "- Item 1\n- Item 2"
        html = parser.parse(md)
        assert "<ul>" in html
        assert "<li>" in html

    def test_horizontal_rule(self, parser):
        md = "Some text\n\n---\n\nMore text"
        html = parser.parse(md)
        assert "<hr" in html

    def test_html_wrapped(self, parser):
        md = "# Hello"
        html = parser.parse(md)
        assert html.startswith("<!DOCTYPE html>")
        assert "<html" in html
        assert "<body>" in html
        assert "</html>" in html
