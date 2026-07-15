#!/usr/bin/env python3
"""
# =============================================================================
# JOL Destructive Action Confirmation Guard
# =============================================================================
# Purpose:      Prevents accidental execution of destructive scripts.
#               Requires typed confirmation for DESTRUCTIVE and SECURITY-CRITICAL
#               danger levels. Cannot be bypassed except with --yes flag (CI only).
# Author:       @journeyoflife-org/platform-core
# Last-tested:  2026-07-15
# Danger-level: NONE
# Classification: INTERNAL
# =============================================================================
"""

from __future__ import annotations

import sys


def require_confirmation(script_name: str, danger_level: str) -> None:
    """
    Require the operator to type the script name to confirm execution.
    This prevents accidental runs of destructive operations.

    Raises SystemExit if confirmation is not provided.
    """
    print(f"\n{'=' * 60}")
    print(f"  DANGER LEVEL: {danger_level}")
    print(f"    Script: {script_name}")
    print("    This operation modifies production systems.")
    print(f"    To confirm, type the script name exactly: {script_name}")
    print(f"{'=' * 60}")

    try:
        user_input = input("Confirm script name: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(130)

    if user_input != script_name:
        print(f" Confirmation failed. Expected '{script_name}', got '{user_input}'.")
        print("  Use --dry-run to preview what this script would do.")
        sys.exit(1)

    print(f" Confirmed. Proceeding with {script_name}...\n")
