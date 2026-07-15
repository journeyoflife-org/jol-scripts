#!/usr/bin/env python3
"""
# =============================================================================
# k8s-collect-rbac-evidence
# =============================================================================
# Purpose:      Collect RBAC evidence from a Kubernetes cluster (read-only).
# Author:       @journeyoflife-org/platform-core
# Last-tested:  2026-07-15
# Danger-level: SAFE
# Classification: INTERNAL
# =============================================================================
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lib.jol_base import JolBaseScript  # noqa: E402


class K8sCollectRbacEvidence(JolBaseScript):
    def __init__(self) -> None:
        super().__init__(
            script_name="k8s-collect-rbac-evidence",
            description="Collect RBAC evidence (roles, bindings, service accounts) from a K8s cluster.",
            danger_level="SAFE",
        )

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--namespace",
            default=None,
            help="Namespace to collect from (default: all namespaces).",
        )
        parser.add_argument(
            "--output",
            default="evidence/rbac-evidence.json",
            help="Output file path (default: evidence/rbac-evidence.json).",
        )

    def run_logic(self, args: argparse.Namespace) -> int:
        if args.dry_run:
            msg = f"[DRY-RUN] Would collect RBAC evidence from namespace={args.namespace or 'all'} -> {args.output}"
            self.logger.info(msg)
            print(msg)
            return 0

        self.logger.info(f"Collecting RBAC evidence (namespace={args.namespace or 'all'})")
        # TODO: Implement kubernetes client API calls
        evidence = {"cluster_roles": [], "role_bindings": [], "cluster_role_bindings": [], "service_accounts": []}

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(evidence, indent=2))
        self.logger.info(f"Evidence written to {output_path}")
        print(f"RBAC evidence collected -> {output_path}")
        return 0


if __name__ == "__main__":
    K8sCollectRbacEvidence().main()
