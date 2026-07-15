# Script Inventory — Danger Register

Per-script classification of operational risk.

## Database (`scripts/db/`)

| Script | Danger Level | Confirmation Required | Dry-run |
|---|---|---|---|
| `db-backup.py` | DESTRUCTIVE-ADJACENT | No | Yes |
| `db-rotate-credentials.py` | SECURITY-CRITICAL | Yes | Yes |

## Kubernetes (`scripts/kubernetes/`)

| Script | Danger Level | Confirmation Required | Dry-run |
|---|---|---|---|
| `k8s-drain-node.py` | DESTRUCTIVE | Yes | Yes |
| `k8s-collect-rbac-evidence.py` | Safe (read-only) | No | Yes |

## Backup (`scripts/backup/`)

| Script | Danger Level | Confirmation Required | Dry-run |
|---|---|---|---|
| `verify-backups.py` | Safe (read-only) | No | Yes |

## Maintenance (`scripts/maintenance/`)

| Script | Danger Level | Confirmation Required | Dry-run |
|---|---|---|---|
| `cleanup-old-logs.py` | DESTRUCTIVE | Yes | Yes |
| `rotate-ssh-keys.py` | SECURITY-CRITICAL | Yes | Yes |

## Compliance (`scripts/compliance/`)

| Script | Danger Level | Confirmation Required | Dry-run |
|---|---|---|---|
| `collect-soc2-evidence.py` | Safe (read-only) | No | Yes |

## Secrets (`scripts/secrets/`)

| Script | Danger Level | Confirmation Required | Dry-run |
|---|---|---|---|
| `rotate-github-token.py` | SECURITY-CRITICAL | Yes | Yes |
