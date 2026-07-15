# Operational Runbook

## Prerequisites

- Python 3.11+
- Virtual environment activated (`source .venv/bin/activate`)
- Appropriate infrastructure access for the target script

## Common Flags

All scripts inherit from `JolBaseScript` and support:

| Flag | Purpose |
|---|---|
| `--dry-run` / `-n` | Preview actions without making changes |
| `--yes` / `-y` | Skip interactive confirmation (CI only) |
| `--verbose` / `-v` | Enable verbose output |

## Running Scripts

### Database Backup

```bash
# Preview
python scripts/db/db-backup.py --dry-run --db-host prod-db --db-name myapp

# Execute
python scripts/db/db-backup.py --db-host prod-db --db-name myapp
```

### Rotate DB Credentials

```bash
# Preview
python scripts/db/db-rotate-credentials.py --dry-run --db-host prod-db --username app_user

# Execute (requires confirmation)
python scripts/db/db-rotate-credentials.py --db-host prod-db --username app_user
```

### Drain Kubernetes Node

```bash
# Preview
python scripts/kubernetes/k8s-drain-node.py --dry-run --node worker-03

# Execute (requires confirmation)
python scripts/kubernetes/k8s-drain-node.py --node worker-03
```

### Collect RBAC Evidence

```bash
python scripts/kubernetes/k8s-collect-rbac-evidence.py --namespace production
```

### Verify Backups

```bash
python scripts/backup/verify-backups.py --backup-dir /var/backups --max-age-hours 24
```

### Cleanup Old Logs

```bash
# Preview
python scripts/maintenance/cleanup-old-logs.py --dry-run --log-dir /var/log/jol --retention-days 90

# Execute (requires confirmation)
python scripts/maintenance/cleanup-old-logs.py --log-dir /var/log/jol --retention-days 90
```

### Rotate SSH Keys

```bash
# Execute (requires confirmation)
python scripts/maintenance/rotate-ssh-keys.py --user deploy --hosts "web01,web02,web03"
```

### Collect SOC 2 Evidence

```bash
python scripts/compliance/collect-soc2-evidence.py --controls CC6,CC7,CC8
```

### Rotate GitHub Token

```bash
# Execute (requires confirmation)
python scripts/secrets/rotate-github-token.py --org myorg --token-name ci-deploy
```

## Audit Logs

All scripts write structured JSON-lines audit records to `logs/SCRIPT_NAME-YYYYMMDD.log`.

To view recent entries:
```bash
cat logs/*.log | jq .
```

## Emergency Abort

- Press `Ctrl+C` during confirmation prompt to abort
- Set `JOL_CONFIRM=""` (empty) to ensure prompts are never bypassed
- Use `--dry-run` first to verify expected behaviour
