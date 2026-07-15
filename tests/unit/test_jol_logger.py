"""Unit tests for jol_logger — JolLogger class."""

from __future__ import annotations

import json
from pathlib import Path

from lib.jol_logger import JolLogger


def _make_logger(tmp_path: Path, monkeypatch=None) -> JolLogger:
    """Create a JolLogger writing to a unique temp directory."""
    import pytest

    log_dir = tmp_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    if monkeypatch is not None:
        monkeypatch.setattr(JolLogger, "LOG_DIR", log_dir)
    else:
        JolLogger.LOG_DIR = log_dir

    return JolLogger("test-logger")


def test_jol_logger_creates_log_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    logger = _make_logger(tmp_path, monkeypatch)
    logger.info("hello world")

    for h in logger._logger.handlers:
        h.flush()

    log_files = list(JolLogger.LOG_DIR.glob("test-logger-*.log"))
    assert len(log_files) == 1


def test_jol_logger_audit_header(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    logger = _make_logger(tmp_path, monkeypatch)
    logger.audit_header(
        script="test-script",
        danger="SAFE",
        dry_run=True,
        args={"foo": "bar"},
    )

    for h in logger._logger.handlers:
        h.flush()

    log_files = list(JolLogger.LOG_DIR.glob("test-logger-*.log"))
    content = log_files[0].read_text().strip()
    # Each line is a single JSON entry from _entry()
    found = False
    for line in content.splitlines():
        record = json.loads(line)
        if record.get("msg") == "SCRIPT_START":
            assert record["script"] == "test-script"
            assert record["danger_level"] == "SAFE"
            assert record["dry_run"] is True
            found = True
            break
    assert found, "SCRIPT_START event not found in log"


def test_jol_logger_audit_footer(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    logger = _make_logger(tmp_path, monkeypatch)
    logger.audit_footer(script="test-script", exit_code=0)

    for h in logger._logger.handlers:
        h.flush()

    log_files = list(JolLogger.LOG_DIR.glob("test-logger-*.log"))
    content = log_files[0].read_text().strip()
    found = False
    for line in content.splitlines():
        record = json.loads(line)
        if record.get("msg") == "SCRIPT_END":
            assert record["script"] == "test-script"
            assert record["exit_code"] == 0
            assert record["status"] == "SUCCESS"
            found = True
            break
    assert found, "SCRIPT_END event not found in log"


def test_jol_logger_json_format(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    logger = _make_logger(tmp_path, monkeypatch)
    logger.info("test message")

    for h in logger._logger.handlers:
        h.flush()

    log_files = list(JolLogger.LOG_DIR.glob("test-logger-*.log"))
    content = log_files[0].read_text().strip()
    # At least one line should be valid JSON with the expected fields
    found = False
    for line in content.splitlines():
        record = json.loads(line)
        if record.get("msg") == "test message":
            assert "ts" in record
            assert "script" in record
            assert record["level"] == "INFO"
            found = True
            break
    assert found, "No log line with msg='test message' found"
