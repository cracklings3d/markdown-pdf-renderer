"""PDF rendering using WeasyPrint."""

from pathlib import Path

import weasyprint

from .markdown_parser import MarkdownParser


class PDFRenderer:
    def __init__(self, parser: MarkdownParser) -> None:
        self.parser = parser

    def render(self, markdown_content: str, output_path: Path) -> None:
        html = self.parser.parse(markdown_content)
        pdf = weasyprint.HTML(string=html).write_pdf()
        output_path.write_bytes(pdf)

    def render_file(self, input_path: Path, output_path: Path) -> None:
        html = self.parser.parse_file(input_path)
        pdf = weasyprint.HTML(string=html).write_pdf()
        output_path.write_bytes(pdf)


def render(markdown_file: Path, output_file: Path) -> None:
    renderer = PDFRenderer(MarkdownParser())
    renderer.render_file(markdown_file, output_file)
