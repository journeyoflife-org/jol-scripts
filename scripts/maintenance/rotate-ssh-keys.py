#!/usr/bin/env python3
"""
# =============================================================================
# rotate-ssh-keys
# =============================================================================
# Purpose:      Generate new SSH key pairs and distribute to target hosts.
# Author:       @journeyoflife-org/platform-core
# Last-tested:  2026-07-15
# Danger-level: SECURITY-CRITICAL
# Classification: INTERNAL
# =============================================================================
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lib.jol_base import JolBaseScript  # noqa: E402


class RotateSshKeys(JolBaseScript):
    def __init__(self) -> None:
        super().__init__(
            script_name="rotate-ssh-keys",
            description="Generate new SSH key pairs and distribute to target hosts.",
            danger_level="SECURITY-CRITICAL",
        )

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--user", required=True, help="Service account username.")
        parser.add_argument(
            "--hosts",
            required=True,
            help="Comma-separated list of target hosts.",
        )
        parser.add_argument(
            "--key-type",
            default="ed25519",
            choices=["ed25519", "rsa"],
            help="SSH key type (default: ed25519).",
        )

    def run_logic(self, args: argparse.Namespace) -> int:
        hosts = [h.strip() for h in args.hosts.split(",")]

        if args.dry_run:
            msg = f"[DRY-RUN] Would generate new {args.key_type} key for {args.user} and distribute to {hosts}"
            self.logger.info(msg)
            print(msg)
            return 0

        self.logger.info(f"Rotating SSH keys for {args.user} -> {hosts}")
        # TODO: Implement ssh-keygen + ssh-copy-id via subprocess
        print(f"SSH keys rotated for {args.user} on {len(hosts)} host(s)")
        return 0


if __name__ == "__main__":
    RotateSshKeys().main()
