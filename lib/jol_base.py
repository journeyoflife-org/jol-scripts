#!/usr/bin/env python3
"""
# =============================================================================
# JOL Base Script Class
# =============================================================================
# Purpose:      Mandatory base class for all jol-scripts operational scripts.
#               Enforces: --dry-run flag, audit logging, idempotency guard,
#               structured exit codes, and SOC 2 CC8 execution trail.
# Author:       @journeyoflife-org/platform-core
# Last-tested:  2026-07-15
# Danger-level: NONE (base class — no side effects)
# Classification: INTERNAL
# =============================================================================
"""

from __future__ import annotations

import argparse
import sys
from abc import ABC, abstractmethod

from lib.jol_logger import JolLogger


class JolBaseScript(ABC):
    """
    Mandatory base class for all JOL operational scripts.

    Every concrete script must:
    1. Inherit from JolBaseScript
    2. Implement `run_logic(args)` — the actual work
    3. Call `self.main()` in `if __name__ == "__main__"`

    Enforced standards:
    - --dry-run flag on every script (argparse action='store_true')
    - --verbose flag for debug output
    - Structured audit log written to logs/SCRIPT_NAME-YYYYMMDD.log
    - SOC 2 CC8 execution header logged on every run
    - Idempotency: run_logic() must be safe to call multiple times
    """

    def __init__(self, script_name: str, description: str, danger_level: str) -> None:
        self.script_name = script_name
        self.description = description
        self.danger_level = danger_level  # SAFE | DESTRUCTIVE-ADJACENT | DESTRUCTIVE | SECURITY-CRITICAL
        self.logger = JolLogger(script_name)

    def build_parser(self) -> argparse.ArgumentParser:
        """Build base argument parser. Override to add script-specific args."""
        parser = argparse.ArgumentParser(
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=f"Danger level: {self.danger_level}\nAudit log: logs/{self.script_name}-*.log",
        )
        parser.add_argument(
            "--dry-run",
            "-n",
            action="store_true",
            help="Simulate execution. No changes are made. ALWAYS test with --dry-run first.",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Enable verbose output",
        )
        parser.add_argument(
            "--yes",
            "-y",
            action="store_true",
            help="Skip interactive confirmation prompt (use in CI only)",
        )
        return parser

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:  # noqa: B027
        """Override to add script-specific arguments."""

    @abstractmethod
    def run_logic(self, args: argparse.Namespace) -> int:
        """
        Implement script logic here.

        IDEMPOTENCY CONTRACT:
        - This method MUST be safe to call multiple times on the same target.
        - Check current state before applying changes.
        - Return 0 on success, non-zero on failure.

        DRY-RUN CONTRACT:
        - When args.dry_run is True, log what would happen but make NO changes.
        - Every destructive operation must check: if args.dry_run: log_and_return

        Args:
            args: Parsed CLI arguments

        Returns:
            Exit code (0 = success, 1 = error, 2 = partial, 3 = dry-run-only)
        """

    def main(self) -> None:
        """Entry point. Builds parser, logs execution header, calls run_logic."""
        parser = self.build_parser()
        self.add_arguments(parser)
        args = parser.parse_args()

        # SOC 2 CC8 — Execution audit trail
        self.logger.audit_header(
            script=self.script_name,
            danger=self.danger_level,
            dry_run=args.dry_run,
            args=vars(args),
        )

        if self.danger_level in ("DESTRUCTIVE", "SECURITY-CRITICAL") and not args.dry_run and not args.yes:
            from lib.jol_confirm import require_confirmation

            require_confirmation(self.script_name, self.danger_level)

        try:
            exit_code = self.run_logic(args)
        except KeyboardInterrupt:
            self.logger.warning("Script interrupted by user (KeyboardInterrupt)")
            exit_code = 130
        except Exception as exc:  # noqa: BLE001
            self.logger.error(f"Unhandled exception: {exc}")
            raise

        self.logger.audit_footer(script=self.script_name, exit_code=exit_code)
        sys.exit(exit_code)
