#!/usr/bin/env python3
"""
# =============================================================================
# JOL Structured Audit Logger
# =============================================================================
# Purpose:      SOC 2 CC8-compliant structured logger for all jol-scripts.
#               Writes JSON-structured log entries to logs/ directory.
#               Every script execution produces an immutable audit trail.
# Author:       @journeyoflife-org/platform-core
# Last-tested:  2026-07-15
# Danger-level: NONE
# Classification: INTERNAL
# =============================================================================
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path


class JolLogger:
    """Structured audit logger. Writes to both stdout and logs/ directory."""

    LOG_DIR = Path(__file__).parent.parent / "logs"

    def __init__(self, script_name: str) -> None:
        self.script_name = script_name
        self.LOG_DIR.mkdir(exist_ok=True)

        date_str = datetime.now(UTC).strftime("%Y%m%d")
        log_file = self.LOG_DIR / f"{script_name}-{date_str}.log"

        self._logger = logging.getLogger(script_name)
        self._logger.setLevel(logging.DEBUG)

        # File handler — JSON structured
        fh = logging.FileHandler(log_file)
        fh.setFormatter(logging.Formatter("%(message)s"))
        self._logger.addHandler(fh)

        # Console handler — human-readable
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        self._logger.addHandler(ch)

    def _entry(self, level: str, message: str, **extra: object) -> str:
        entry = {
            "ts": datetime.now(UTC).isoformat(),
            "script": self.script_name,
            "level": level,
            "msg": message,
            "user": os.environ.get("USER", "unknown"),
            "host": os.uname().nodename,
            **extra,
        }
        return json.dumps(entry)

    def info(self, msg: str, **kw: object) -> None:
        self._logger.info(self._entry("INFO", msg, **kw))

    def warning(self, msg: str, **kw: object) -> None:
        self._logger.warning(self._entry("WARNING", msg, **kw))

    def error(self, msg: str, **kw: object) -> None:
        self._logger.error(self._entry("ERROR", msg, **kw))

    def debug(self, msg: str, **kw: object) -> None:
        self._logger.debug(self._entry("DEBUG", msg, **kw))

    def audit_header(self, script: str, danger: str, dry_run: bool, args: dict) -> None:  # noqa: FBT001
        msg = self._entry(
            "AUDIT",
            "SCRIPT_START",
            script=script,
            danger_level=danger,
            dry_run=dry_run,
            args={k: v for k, v in args.items() if "secret" not in k.lower() and "password" not in k.lower()},
        )
        self._logger.info(msg)
        if dry_run:
            self._logger.info(self._entry("INFO", "  DRY-RUN MODE — no changes will be made"))

    def audit_footer(self, script: str, exit_code: int) -> None:
        status = "SUCCESS" if exit_code == 0 else "FAILURE"
        self._logger.info(self._entry("AUDIT", "SCRIPT_END", script=script, exit_code=exit_code, status=status))
