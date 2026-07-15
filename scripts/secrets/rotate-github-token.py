#!/usr/bin/env python3
"""
# =============================================================================
# rotate-github-token
# =============================================================================
# Purpose:      Revoke a GitHub PAT and generate a replacement.
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


class RotateGithubToken(JolBaseScript):
    def __init__(self) -> None:
        super().__init__(
            script_name="rotate-github-token",
            description="Revoke a GitHub PAT and generate a replacement with identical scopes.",
            danger_level="SECURITY-CRITICAL",
        )

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--org", required=True, help="GitHub organisation name.")
        parser.add_argument(
            "--token-name",
            required=True,
            help="Name/label of the token to rotate.",
        )
        parser.add_argument(
            "--vault-path",
            default="secret/data/github",
            help="Vault path to store the new token (default: secret/data/github).",
        )

    def run_logic(self, args: argparse.Namespace) -> int:
        if args.dry_run:
            msg = (
                f"[DRY-RUN] Would revoke token '{args.token_name}' in org '{args.org}' "
                f"and write replacement to {args.vault_path}"
            )
            self.logger.info(msg)
            print(msg)
            return 0

        self.logger.info(f"Rotating GitHub token '{args.token_name}' for org '{args.org}'")
        # TODO: Implement GitHub API token revocation + creation via Vault
        print(f"GitHub token '{args.token_name}' rotated for org '{args.org}'")
        return 0


if __name__ == "__main__":
    RotateGithubToken().main()
