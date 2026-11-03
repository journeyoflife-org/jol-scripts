# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `mise.toml` + `mise.lock`: pin python 3.11.18 / 3.12.16 and uv 0.13.6 with per-platform SHA256 checksums and GitHub-attestation provenance; mise tasks mirror the Makefile gates (lint, scan, typecheck, test).
- CI bootstrap via pinned `jdx/mise-action` (commit SHA + `version: 2026.11.0`).

### Changed
- `.github/workflows/ci.yml`: per-cell interpreter now set with `MISE_PYTHON_VERSION` (was `actions/setup-python`); ruff lint+format consolidated into one step. Job name `lint-and-test` and the `["3.11","3.12"]` matrix are preserved, so required-check names are unchanged.

## [0.1.0] - 2024-01-01

### Added
- Initial project scaffold with SOC 2 CC8 audit logging (`lib/jol_logger.py`)
- Destructive-action confirmation gate (`lib/jol_confirm.py`)
- Base script class with `--dry-run` support (`lib/jol_base.py`)
- Scripts: `db-backup`, `db-rotate-credentials`, `k8s-drain-node`, `k8s-collect-rbac-evidence`, `verify-backups`, `cleanup-old-logs`, `rotate-ssh-keys`, `collect-soc2-evidence`, `rotate-github-token`
- Unit tests for all lib modules
- Integration test for dry-run across all scripts
- CI pipeline: ruff lint, bandit scan, mypy, pytest
- Compliance pipeline: TruffleHog + gitleaks full-history scan
- CodeQL static analysis
- Pre-commit hooks: ruff, bandit, mypy, gitleaks
- Script inventory and operational runbook
