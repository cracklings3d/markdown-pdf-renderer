"""CSS styles for PDF output."""

from pathlib import Path
from typing import Literal


def get_default_css() -> str:
    css_path = Path(__file__).parent / "styles" / "default.css"
    return css_path.read_text(encoding="utf-8")


def get_dark_css() -> str:
    css_path = Path(__file__).parent / "styles" / "dark.css"
    return css_path.read_text(encoding="utf-8")


def get_theme_css(theme: Literal["default", "dark"]) -> str:
    if theme == "dark":
        return get_dark_css()
    return get_default_css()
