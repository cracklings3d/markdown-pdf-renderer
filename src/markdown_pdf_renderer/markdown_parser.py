"""Markdown parsing with syntax highlighting and local image embedding."""

import base64
import re
from pathlib import Path
from typing import Optional

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.tables import TableExtension
from markdown.extensions.toc import TocExtension

from typing import Literal

from .styles import get_default_css, get_dark_css


class MarkdownParser:
    def __init__(
        self,
        extensions: Optional[list[str]] = None,
        css: Optional[str] = None,
        header: Optional[str] = None,
        footer: Optional[str] = None,
        page_numbers: bool = True,
        theme: Literal["default", "dark"] = "default",
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
        if css is not None:
            self.css = css
        elif theme == "dark":
            self.css = get_dark_css()
        else:
            self.css = get_default_css()
        self.header = header
        self.footer = footer
        self.page_numbers = page_numbers
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
        self._base_path: Optional[Path] = None

    def parse(self, content: str) -> str:
        html = self.md.convert(content)
        self.md.reset()
        html = self._embed_local_images(html)
        return self._wrap_html(html)

    def parse_file(self, path: Path) -> str:
        self._base_path = path.parent.resolve()
        content = path.read_text(encoding="utf-8")
        return self.parse(content)

    def _embed_local_images(self, html: str) -> str:
        def replace_image(match: re.Match) -> str:
            img_tag = match.group(0)
            src_match = re.search(r'src="([^"]+)"', img_tag)
            if not src_match:
                return img_tag

            src = src_match.group(1)

            if src.startswith(("http://", "https://", "data:")):
                return img_tag

            try:
                if self._base_path:
                    image_path = self._base_path / src
                else:
                    image_path = Path(src)

                if not image_path.exists():
                    return self._placeholder_image(img_tag, f"File not found: {src}")

                mime_types = {
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".gif": "image/gif",
                    ".webp": "image/webp",
                    ".svg": "image/svg+xml",
                    ".bmp": "image/bmp",
                }
                ext = image_path.suffix.lower()
                mime_type = mime_types.get(ext, "application/octet-stream")

                with open(image_path, "rb") as f:
                    data = base64.b64encode(f.read()).decode("ascii")

                return f'<img src="data:{mime_type};base64,{data}" alt="{match.group("alt") or ""}"'
            except Exception:
                return self._placeholder_image(img_tag, f"Failed to load: {src}")

        pattern = re.compile(r'<img\s+(?P<attrs>[^>]+)>', re.IGNORECASE)
        return pattern.sub(replace_image, html)

    def _placeholder_image(self, original_tag: str, message: str) -> str:
        return original_tag

    def _wrap_html(self, body: str) -> str:
        header_html = ""
        if self.header:
            header_html = f'<div class="header">{self.header}</div>'

        footer_html = ""
        if self.footer:
            footer_html = f'<div class="footer">{self.footer}</div>'

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
{header_html}
{body}
{footer_html}
</body>
</html>"""
