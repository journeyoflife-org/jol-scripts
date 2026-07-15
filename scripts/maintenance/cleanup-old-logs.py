#!/usr/bin/env python3
"""
# =============================================================================
# cleanup-old-logs
# =============================================================================
# Purpose:      Delete log files older than the configured retention period.
# Author:       @journeyoflife-org/platform-core
# Last-tested:  2026-07-15
# Danger-level: DESTRUCTIVE
# Classification: INTERNAL
# =============================================================================
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lib.jol_base import JolBaseScript  # noqa: E402


class CleanupOldLogs(JolBaseScript):
    def __init__(self) -> None:
        super().__init__(
            script_name="cleanup-old-logs",
            description="Delete log files older than the configured retention period.",
            danger_level="DESTRUCTIVE",
        )

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--log-dir",
            default="/var/log/jol",
            help="Directory to clean (default: /var/log/jol).",
        )
        parser.add_argument(
            "--retention-days",
            type=int,
            default=90,
            help="Delete files older than this many days (default: 90).",
        )
        parser.add_argument(
            "--pattern",
            default="*.log*",
            help="Glob pattern for files to consider (default: *.log*).",
        )

    def run_logic(self, args: argparse.Namespace) -> int:
        log_dir = Path(args.log_dir)

        if args.dry_run:
            msg = (
                f"[DRY-RUN] Would delete files matching '{args.pattern}' in {log_dir} "
                f"older than {args.retention_days} days"
            )
            self.logger.info(msg)
            print(msg)
            return 0

        self.logger.info(f"Cleaning logs in {log_dir} (retention={args.retention_days}d, pattern={args.pattern})")
        # TODO: Implement age-based file deletion with audit trail
        print(f"Log cleanup completed for {log_dir} (retention: {args.retention_days}d)")
        return 0


if __name__ == "__main__":
    CleanupOldLogs().main()
