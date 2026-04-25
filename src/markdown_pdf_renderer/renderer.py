"""PDF rendering using WeasyPrint."""

from pathlib import Path
from typing import Literal, Optional

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


def render(
    markdown_file: Path,
    output_file: Path,
    header: Optional[str] = None,
    footer: Optional[str] = None,
    page_numbers: bool = True,
    theme: Literal["default", "dark"] = "default",
) -> str:
    parser = MarkdownParser(
        header=header,
        footer=footer,
        page_numbers=page_numbers,
        theme=theme,
    )
    renderer = PDFRenderer(parser)
    renderer.render_file(markdown_file, output_file)
    return renderer.parser.parse_file(markdown_file)
