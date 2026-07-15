# jol-scripts

Operational scripts for infrastructure management with structured audit logging, destructive-action confirmation, and `--dry-run` safety controls.

## Quick Start

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run validation suite
make validate
```

## Project Structure

| Directory | Purpose |
|---|---|
| `lib/` | Shared library: `JolLogger`, `require_confirmation`, `JolBaseScript` |
| `scripts/` | Operational scripts organised by domain |
| `tests/` | Unit and integration tests |
| `docs/` | Script inventory and operational runbook |
| `logs/` | Audit log output (gitignored except `.gitkeep`) |

## Script Danger Levels

Every script declares a `danger_level` passed to `JolBaseScript.__init__()`:

| Level | Behaviour |
|---|---|
| `SAFE` | Read-only; no side-effects |
| `DESTRUCTIVE-ADJACENT` | Writes to non-production targets (e.g. backup files) |
| `DESTRUCTIVE` | Irreversible changes; requires operator confirmation |
| `SECURITY-CRITICAL` | Modifies authentication material; requires operator confirmation |

## Dry-run

All scripts support `--dry-run` / `-n` to preview actions without making changes:

```bash
python scripts/db/db-backup.py --dry-run --db-host prod-db --db-name myapp
```

## Audit Logging

All scripts emit structured JSON-lines audit records to `logs/SCRIPT_NAME-YYYYMMDD.log` (SOC 2 CC8). Each execution is bracketed by `execution_start` and `execution_end` audit events.

## Writing a New Script

```python
from lib.jol_base import JolBaseScript

class MyScript(JolBaseScript):
    def __init__(self):
        super().__init__(
            script_name="my-script",
            description="Does something useful.",
            danger_level="SAFE",
        )

    def add_arguments(self, parser):
        parser.add_argument("--target", required=True)

    def run_logic(self, args) -> int:
        if args.dry_run:
            print(f"[DRY-RUN] Would process {args.target}")
            return 0
        # ... actual work ...
        return 0

if __name__ == "__main__":
    MyScript().main()
```

## Validation

```bash
make validate   # lint + bandit + pytest
make audit      # full audit: lint + bandit + mypy + pytest
```

## CI/CD

GitHub Actions workflows:
- **ci.yml** — Lint, bandit, mypy, pytest on every push/PR
- **compliance-check.yml** — TruffleHog + gitleaks secret scanning
- **codeql.yml** — CodeQL static analysis
