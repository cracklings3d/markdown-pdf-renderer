"""Test PDF rendering functionality."""

import tempfile
from pathlib import Path

import pytest
from markdown_pdf_renderer.renderer import PDFRenderer
from markdown_pdf_renderer.markdown_parser import MarkdownParser


class TestPDFRenderer:
    @pytest.fixture
    def renderer(self):
        return PDFRenderer(MarkdownParser())

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as d:
            yield Path(d)

    def test_render_creates_file(self, renderer, temp_dir):
        md = "# Test\n\nContent here."
        output = temp_dir / "output.pdf"
        renderer.render(md, output)
        assert output.exists()

    def test_render_produces_valid_pdf(self, renderer, temp_dir):
        md = "# Test"
        output = temp_dir / "output.pdf"
        renderer.render(md, output)
        content = output.read_bytes()
        assert content.startswith(b"%PDF")
        assert len(content) > 100

    def test_render_empty_markdown(self, renderer, temp_dir):
        md = ""
        output = temp_dir / "output.pdf"
        renderer.render(md, output)
        assert output.exists()

    def test_render_with_code_block(self, renderer, temp_dir):
        md = "```python\nprint('hello')\n```"
        output = temp_dir / "output.pdf"
        renderer.render(md, output)
        assert output.exists()

    def test_render_with_table(self, renderer, temp_dir):
        md = "| A | B |\n|---|---|\n| 1 | 2 |"
        output = temp_dir / "output.pdf"
        renderer.render(md, output)
        assert output.exists()

    def test_render_file(self, renderer, temp_dir):
        md_file = temp_dir / "input.md"
        output = temp_dir / "output.pdf"
        md_file.write_text("# Test File\n\nContent")
        renderer.render_file(md_file, output)
        assert output.exists()
