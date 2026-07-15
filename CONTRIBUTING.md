# Contributing

## Getting Started

```bash
git clone <repo-url> && cd jol-scripts
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Development Workflow

1. Create a feature branch from `main`
2. Implement changes following the patterns in `lib/` and `scripts/`
3. Run `make validate` before committing
4. Open a PR using the provided template

## Adding a New Script

1. Create the script under the appropriate `scripts/<domain>/` directory
2. Inherit from `JolBase` and set `SCRIPT_NAME`, `DESCRIPTION`, `DANGER_LEVEL`
3. Implement `run()` — use `self.dry_run` and `self.dry_run_print()` for dry-run support
4. Use `self.log` for all audit-relevant operations
5. Add the script to `docs/script-inventory.md`
6. Add integration test coverage (automatic via `test_dry_run_all_scripts.py`)

## Code Standards

- **Linting**: ruff (configured in `pyproject.toml`)
- **Security**: bandit (no hardcoded secrets, no unsafe subprocess usage)
- **Type checking**: mypy strict mode
- **Line length**: 120 characters
- **Python version**: 3.11+

## PR Requirements

- `make validate` must pass
- All destructive actions gated by `jol_confirm`
- Structured audit logging via `jol_logger`
- `--dry-run` support for any script with side-effects
- CHANGELOG.md updated for user-facing changes
