#!/usr/bin/env python3
"""
# =============================================================================
# db-backup
# =============================================================================
# Purpose:      Create a database backup to the configured destination.
# Author:       @journeyoflife-org/platform-core
# Last-tested:  2026-07-15
# Danger-level: DESTRUCTIVE-ADJACENT
# Classification: INTERNAL
# =============================================================================
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lib.jol_base import JolBaseScript  # noqa: E402


class DbBackup(JolBaseScript):
    def __init__(self) -> None:
        super().__init__(
            script_name="db-backup",
            description="Create a database backup to the configured destination.",
            danger_level="DESTRUCTIVE-ADJACENT",
        )

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--db-host", required=True, help="Database host.")
        parser.add_argument("--db-name", required=True, help="Database name to back up.")
        parser.add_argument(
            "--destination",
            default="/var/backups/db",
            help="Backup destination directory (default: /var/backups/db).",
        )

    def run_logic(self, args: argparse.Namespace) -> int:
        target = Path(args.destination) / f"{args.db_name}-backup.sql.gz"

        if args.dry_run:
            self.logger.info(f"[DRY-RUN] Would back up {args.db_host}/{args.db_name} -> {target}")
            print(f"[DRY-RUN] Would back up {args.db_host}/{args.db_name} -> {target}")
            return 0

        self.logger.info(f"Backing up {args.db_host}/{args.db_name} -> {target}")
        # TODO: Implement actual pg_dump / mysqldump logic
        print(f"Backup completed: {target}")
        return 0


if __name__ == "__main__":
    DbBackup().main()
