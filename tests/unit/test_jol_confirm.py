"""Unit tests for jol_confirm — require_confirmation."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from lib.jol_confirm import require_confirmation


def test_require_confirmation_correct_token() -> None:
    with patch("builtins.input", return_value="my-script"):
        require_confirmation("my-script", "DESTRUCTIVE")  # should not raise


def test_require_confirmation_wrong_token_raises() -> None:
    with patch("builtins.input", return_value="no"):
        with pytest.raises(SystemExit) as exc_info:
            require_confirmation("my-script", "DESTRUCTIVE")
        assert exc_info.value.code == 1


def test_require_confirmation_eof_raises() -> None:
    with patch("builtins.input", side_effect=EOFError):
        with pytest.raises(SystemExit) as exc_info:
            require_confirmation("my-script", "DESTRUCTIVE")
        assert exc_info.value.code == 130


def test_require_confirmation_keyboard_interrupt_raises() -> None:
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        with pytest.raises(SystemExit) as exc_info:
            require_confirmation("my-script", "DESTRUCTIVE")
        assert exc_info.value.code == 130
