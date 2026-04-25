"""Markdown parsing with syntax highlighting."""

import re
from pathlib import Path
from typing import Optional

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

from .styles import get_default_css


class MarkdownParser:
    def __init__(
        self,
        extensions: Optional[list[str]] = None,
        css: Optional[str] = None,
    ) -> None:
        if extensions is None:
            extensions = [
                "tables",
                "fenced_code",
                "codehilite",
                "toc",
                "nl2br",
                "sane_lists",
            ]

        self.extensions = extensions
        self.css = css if css is not None else get_default_css()
        self.md = markdown.Markdown(
            extensions=self.extensions,
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "guess_lang": False,
                },
                "toc": {
                    "title": "Table of Contents",
                },
            },
        )

    def parse(self, content: str) -> str:
        html = self.md.convert(content)
        self.md.reset()
        return self._wrap_html(html)

    def parse_file(self, path: Path) -> str:
        content = path.read_text(encoding="utf-8")
        return self.parse(content)

    def _wrap_html(self, body: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
{self.css}
    </style>
</head>
<body>
{body}
</body>
</html>"""
