# Markdown PDF Renderer

Convert Markdown files to beautifully styled PDF documents.

## Features

- GitHub Flavored Markdown (GFM) support
- Code syntax highlighting
- Table of contents generation
- Local image embedding (base64)
- Custom headers and footers
- Page numbering
- Custom CSS theming

## Installation

```bash
pip install markdown-pdf-renderer
```

Or install from source:

```bash
git clone https://github.com/cracklings3d/markdown-pdf-renderer.git
cd markdown-pdf-renderer
pip install -e .
```

## CLI Usage

```bash
md-pdf input.md output.pdf
```

### Options

| Option | Description |
|--------|-------------|
| `--css FILE` | Custom CSS file for styling |
| `--header TEXT` | Header text on each page |
| `--footer TEXT` | Footer text on each page |
| `--no-page-numbers` | Disable page numbers |
| `--debug` | Output intermediate HTML |

### Examples

Basic conversion:
```bash
md-pdf document.md document.pdf
```

With custom header:
```bash
md-pdf document.md document.pdf --header "My Document"
```

Disable page numbers:
```bash
md-pdf document.md document.pdf --no-page-numbers
```

Custom styling:
```bash
md-pdf document.md document.pdf --css custom.css
```

## Python API

```python
from markdown_pdf_renderer import render, PDFRenderer, MarkdownParser

# Simple function
render("input.md", "output.pdf")

# With options
render(
    "input.md",
    "output.pdf",
    header="My Document",
    footer="Copyright 2024",
    page_numbers=True,
)

# Or use classes directly
parser = MarkdownParser(header="Header", footer="Footer")
renderer = PDFRenderer(parser)
renderer.render_file("input.md", "output.pdf")
```

## Themes

### Default Theme

Clean, professional styling with:
- Source Sans Pro font
- Code syntax highlighting
- Tables with alternating row colors

### Dark Theme (coming soon)

Dark background with light text for different use cases.

## Supported Markdown

- Headers (h1-h6)
- Paragraphs, bold, italic, strikethrough
- Code blocks with syntax highlighting
- Tables (GFM)
- Task lists
- Blockquotes
- Links and images
- Horizontal rules
- Table of contents (`[TOC]`)

## Requirements

- Python 3.10+
- WeasyPrint
- Pygments
- Click
- markdown

## License

MIT
