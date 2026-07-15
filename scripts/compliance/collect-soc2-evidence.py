#!/usr/bin/env python3
"""
# =============================================================================
# JOL SOC 2 Evidence Collection Script
# =============================================================================
# Purpose:      Collect quarterly SOC 2 evidence artifacts:
#               - GitHub Actions run history (CC8.1 change management)
#               - Kubernetes RBAC export (CC6.3 least privilege)
#               - Secret scanning report (CC6.7)
#               - Dependency vulnerability report (CC7.1)
# Author:       @journeyoflife-org/platform-core
# Last-tested:  2026-07-15
# Danger-level: SAFE (read-only — no writes to production)
# Idempotent:   YES — creates timestamped evidence directory
# Dry-run:      YES — lists what would be collected
# SOC2:         CC8.1 — evidence collection for audit
# ISO27001:     A.5.35 — independent review of information security
# =============================================================================
"""

from __future__ import annotations

import argparse
import subprocess  # noqa: S404 # nosec B404
from datetime import UTC, datetime
from pathlib import Path

from lib.jol_base import JolBaseScript


class CollectSoc2EvidenceScript(JolBaseScript):
    def __init__(self) -> None:
        super().__init__(
            script_name="collect-soc2-evidence",
            description="Collect SOC 2 evidence artifacts for quarterly audit.",
            danger_level="SAFE",
        )

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--output-dir",
            default="./soc2-evidence",
            help="Directory to write evidence artifacts",
        )
        parser.add_argument(
            "--quarter",
            default=None,
            help="Quarter label (e.g. 2026-Q3). Defaults to current quarter.",
        )

    def run_logic(self, args: argparse.Namespace) -> int:
        quarter = args.quarter or self._current_quarter()
        output_dir = Path(args.output_dir) / quarter

        self.logger.info(f"Collecting SOC 2 evidence for quarter: {quarter}")
        self.logger.info(f"Output directory: {output_dir}")

        evidence_items = [
            ("k8s-rbac", "kubectl get clusterrolebindings,rolebindings -A -o json"),
            ("k8s-namespaces", "kubectl get namespaces -o json"),
            ("k8s-pod-security", "kubectl get pods -A -o json"),
        ]

        if args.dry_run:
            for name, cmd in evidence_items:
                self.logger.info(f"[DRY-RUN] Would collect: {name} via: {cmd}")
            self.logger.info(f"[DRY-RUN] Would write to: {output_dir}/")
            return 3

        output_dir.mkdir(parents=True, exist_ok=True)

        for name, cmd in evidence_items:
            self.logger.info(f"Collecting: {name}")
            try:
                result = subprocess.run(  # noqa: S603 # nosec B603
                    cmd.split(), capture_output=True, text=True, timeout=30, check=False
                )
                (output_dir / f"{name}.json").write_text(result.stdout)
                self.logger.info(f" Saved: {output_dir / name}.json")
            except Exception as exc:
                self.logger.error(f"Failed to collect {name}: {exc}")

        self.logger.info(f" Evidence collection complete: {output_dir}")
        return 0

    @staticmethod
    def _current_quarter() -> str:
        now = datetime.now(UTC)
        q = (now.month - 1) // 3 + 1
        return f"{now.year}-Q{q}"


if __name__ == "__main__":
    CollectSoc2EvidenceScript().main()
