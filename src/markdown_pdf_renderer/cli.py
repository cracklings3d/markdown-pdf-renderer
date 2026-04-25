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
def main(input_file: Path, output_file: Path, css: Path | None) -> None:
    """Convert a Markdown file to PDF.

    INPUT_FILE: Path to the input Markdown file.

    OUTPUT_FILE: Path to the output PDF file.
    """
    try:
        click.echo(f"Converting {input_file} to {output_file}...")
        render(input_file, output_file)
        click.echo("Done!")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
