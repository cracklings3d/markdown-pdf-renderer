"""CLI interface for markdown-pdf-renderer."""

import sys
from pathlib import Path

import click

from .renderer import render


@click.command()
@click.argument("input_file", type=click.Path(exists=True, path_type=Path))
@click.argument("output_file", type=click.Path(path_type=Path))
@click.option(
    "--css",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help="Custom CSS file for styling",
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
def main(
    input_file: Path,
    output_file: Path,
    css: Path | None,
    header: str | None,
    footer: str | None,
    no_page_numbers: bool,
) -> None:
    """Convert a Markdown file to PDF.

    INPUT_FILE: Path to the input Markdown file.

    OUTPUT_FILE: Path to the output PDF file.
    """
    try:
        click.echo(f"Converting {input_file} to {output_file}...")
        render(
            input_file,
            output_file,
            header=header,
            footer=footer,
            page_numbers=not no_page_numbers,
        )
        click.echo("Done!")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
