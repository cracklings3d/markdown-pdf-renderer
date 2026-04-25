"""Test CLI interface."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from markdown_pdf_renderer.cli import main


class TestCLI:
    @pytest.fixture
    def runner(self):
        return CliRunner()

    @pytest.fixture
    def temp_dir(self, tmp_path):
        return tmp_path

    def test_cli_help(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "INPUT_FILE" in result.output
        assert "OUTPUT_FILE" in result.output

    def test_cli_file_not_found(self, runner, temp_dir):
        result = runner.invoke(main, [temp_dir / "nonexistent.md", temp_dir / "out.pdf"])
        assert result.exit_code == 1
        assert "Error" in result.output

    def test_cli_success(self, runner, temp_dir):
        input_file = temp_dir / "input.md"
        output_file = temp_dir / "output.pdf"
        input_file.write_text("# Hello\n\nWorld")

        result = runner.invoke(main, [str(input_file), str(output_file)])
        assert result.exit_code == 0
        assert output_file.exists()

    def test_cli_creates_output(self, runner, temp_dir):
        input_file = temp_dir / "input.md"
        output_file = temp_dir / "output.pdf"
        input_file.write_text("# Test")

        runner.invoke(main, [str(input_file), str(output_file)])
        assert output_file.exists()
        assert output_file.stat().st_size > 0
