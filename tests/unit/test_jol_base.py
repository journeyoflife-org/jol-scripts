"""Unit tests for JolBaseScript — validates dry-run, logging, exit codes."""
from __future__ import annotations

import argparse
import sys
from unittest.mock import MagicMock, patch

import pytest

from lib.jol_base import JolBaseScript


class ConcreteScript(JolBaseScript):
    """Minimal concrete implementation for testing."""
    def __init__(self, return_code: int = 0) -> None:
        super().__init__("test-script", "Test script", "SAFE")
        self.return_code = return_code
        self.run_was_called = False

    def run_logic(self, args: argparse.Namespace) -> int:
        self.run_was_called = True
        return self.return_code


class TestDryRunFlag:
    def test_dry_run_flag_default_false(self):
        script = ConcreteScript()
        parser = script.build_parser()
        args = parser.parse_args([])
        assert args.dry_run is False

    def test_dry_run_flag_true_when_set(self):
        script = ConcreteScript()
        parser = script.build_parser()
        args = parser.parse_args(["--dry-run"])
        assert args.dry_run is True

    def test_dry_run_short_flag(self):
        script = ConcreteScript()
        parser = script.build_parser()
        args = parser.parse_args(["-n"])
        assert args.dry_run is True

    def test_yes_flag(self):
        script = ConcreteScript()
        parser = script.build_parser()
        args = parser.parse_args(["--yes"])
        assert args.yes is True


class TestExitCodes:
    def test_success_exit_zero(self):
        script = ConcreteScript(return_code=0)
        with patch.object(sys, "exit") as mock_exit, \
             patch.object(sys, "argv", ["test-script"]):
            script.main()
            mock_exit.assert_called_once_with(0)

    def test_dry_run_exit_three(self):
        class DryRunScript(JolBaseScript):
            def run_logic(self, args):
                return 3 if args.dry_run else 0

        script = DryRunScript("dry-test", "Test", "SAFE")
        with patch.object(sys, "exit") as mock_exit, \
             patch.object(sys, "argv", ["dry-test", "--dry-run"]):
            script.main()
            mock_exit.assert_called_once_with(3)
