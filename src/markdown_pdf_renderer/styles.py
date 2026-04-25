"""Default CSS styles for PDF output."""

from pathlib import Path


def get_default_css() -> str:
    css_path = Path(__file__).parent / "styles" / "default.css"
    return css_path.read_text(encoding="utf-8")
