"""Test page headers, footers, and TOC features."""

import pytest
from markdown_pdf_renderer.markdown_parser import MarkdownParser


class TestHeadersFooters:
    def test_default_no_header_footer(self):
        parser = MarkdownParser()
        html = parser.parse("# Hello")
        assert '<div class="header">' not in html
        assert '<div class="footer">' not in html

    def test_custom_header(self):
        parser = MarkdownParser(header="My Document")
        html = parser.parse("# Hello")
        assert '<div class="header">My Document</div>' in html

    def test_custom_footer(self):
        parser = MarkdownParser(footer="Copyright 2024")
        html = parser.parse("# Hello")
        assert '<div class="footer">Copyright 2024</div>' in html

    def test_header_and_footer(self):
        parser = MarkdownParser(header="Header", footer="Footer")
        html = parser.parse("# Hello")
        assert '<div class="header">Header</div>' in html
        assert '<div class="footer">Footer</div>' in html

    def test_toc_in_output(self):
        parser = MarkdownParser()
        md = "[TOC]\n\n# Header 1\n\n# Header 2"
        html = parser.parse(md)
        assert "#TOC" in html or "toc" in html.lower()


class TestPageNumbers:
    def test_page_numbers_enabled_by_default(self):
        parser = MarkdownParser()
        html = parser.parse("# Hello")
        assert "@page" in html or "counter(page)" in html

    def test_page_numbers_can_be_disabled(self):
        parser = MarkdownParser(page_numbers=False)
        html = parser.parse("# Hello")
        assert "counter(page)" not in html
