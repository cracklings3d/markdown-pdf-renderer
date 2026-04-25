"""Test local image embedding."""

import base64
from pathlib import Path

import pytest
from markdown_pdf_renderer.markdown_parser import MarkdownParser


class TestLocalImages:
    @pytest.fixture
    def parser(self):
        return MarkdownParser()

    @pytest.fixture
    def temp_dir(self, tmp_path):
        return tmp_path

    def test_external_image_unchanged(self, parser):
        md = '![alt](https://example.com/image.png)'
        html = parser.parse(md)
        assert "https://example.com/image.png" in html
        assert "data:" not in html

    def test_data_uri_unchanged(self, parser):
        md = '![alt](data:image/png;base64,abc123)'
        html = parser.parse(md)
        assert "data:image/png;base64,abc123" in html

    def test_local_image_embedded(self, parser, temp_dir):
        img_path = temp_dir / "test.png"
        img_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        img_path.write_bytes(img_data)

        md_file = temp_dir / "test.md"
        md_file.write_text(f'![alt](test.png)')

        html = parser.parse_file(md_file)
        assert "data:image/png;base64," in html
        assert base64.b64encode(img_data).decode("ascii") in html

    def test_missing_local_image_shows_placeholder(self, parser, temp_dir):
        md_file = temp_dir / "test.md"
        md_file.write_text('![alt](nonexistent.png)')
        html = parser.parse_file(md_file)
        assert "nonexistent.png" in html

    def test_relative_path_from_cwd(self, parser):
        md = '![alt](relative.png)'
        html = parser.parse(md)
        assert '![alt](relative.png)' in html

    def test_absolute_path_embedded(self, parser, temp_dir):
        img_path = temp_dir / "test.jpg"
        img_data = b"\xff\xd8\xff\xe0"
        img_path.write_bytes(img_data)

        md = f'![alt]({img_path})'
        html = parser.parse(md)
        assert "data:image/jpeg;base64," in html

    def test_image_with_title(self, parser):
        md = '![alt](image.png "title")'
        html = parser.parse(md)
        assert "data:image" in html
