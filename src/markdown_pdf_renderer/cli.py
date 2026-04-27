"""CLI interface for markdown-pdf-renderer."""

import sys
from pathlib import Path
from typing import Literal, Optional

import click

from . import __version__


@click.command()
@click.version_option(__version__)
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "--css",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Custom CSS file for styling",
)
@click.option(
    "--theme",
    type=click.Choice(["default", "dark"]),
    default="default",
    help="Color theme for the PDF",
)
@click.option(
    "--header",
    default=None,
    help="Header text to display on each page",
)
@click.option(
    "--footer",
    default=None,
    help="Footer text to display on each page",
)
@click.option(
    "--no-page-numbers",
    is_flag=True,
    default=False,
    help="Disable page numbers",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Output intermediate HTML to stdout",
)
def main(
    input_file: Path,
    output_file: Path,
    css: Optional[Path],
    theme: Literal["default", "dark"],
    header: Optional[str],
    footer: Optional[str],
    no_page_numbers: bool,
    debug: bool,
) -> None:
    """Convert a Markdown file to PDF.

    INPUT_FILE: Path to the input Markdown file.

    OUTPUT_FILE: Path to the output PDF file.
    """
    try:
        click.echo(f"Converting {input_file} to {output_file}...")

        if css:
            css_content = css.read_text(encoding="utf-8")
        else:
            css_content = None

        parser_theme: Literal["default", "dark"] = theme if not css else "default"

        from .markdown_parser import MarkdownParser
        from .renderer import PDFRenderer

        parser = MarkdownParser(
            css=css_content,
            header=header,
            footer=footer,
            page_numbers=not no_page_numbers,
            theme=parser_theme,
        )
        renderer = PDFRenderer(parser)

        if debug:
            html = parser.parse_file(input_file)
            click.echo(html)
        else:
            renderer.render_file(input_file, output_file)

        if not debug:
            click.echo("Done!")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
