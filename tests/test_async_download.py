#!/usr/bin/env python

"""Tests for `async_download` package."""


import unittest

from async_download import cli
from click.testing import CliRunner


class TestAsync_download(unittest.TestCase):
    """Tests for `async_download` package."""

    def setUp(self):
        self.runner = CliRunner()

    def tearDown(self):
        pass

    def test_main_command_line_interface(self):
        """Test the CLI."""
        result = self.runner.invoke(cli.main)
        assert result.exit_code == 0

    def test_headers_command(self):
        result = self.runner.invoke(cli.main, ["headers"])
        assert result.exit_code != 0
        help_result = self.runner.invoke(cli.main, ["headers", "--help"])
        assert help_result.exit_code == 0

    def test_downalod_command(self):
        result = self.runner.invoke(cli.main, ["download"])
        assert result.exit_code != 0
        help_result = self.runner.invoke(cli.main, ["download", "--help"])
        assert help_result.exit_code == 0
