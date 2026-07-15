# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | Yes |

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

1. Email the security team at `security@jol.example.com`
2. Include: affected script, description of the vulnerability, and reproduction steps
3. Expect acknowledgement within 48 hours
4. A fix will be coordinated before public disclosure

## Security Controls

- All scripts emit structured audit logs (JSON-lines) for SOC 2 CC8 traceability
- Destructive and security-critical scripts require explicit operator confirmation
- All scripts support `--dry-run` to preview actions without side-effects
- Pre-commit hooks enforce: linting (ruff), security scanning (bandit), type checking (mypy), secret detection (gitleaks)
- CI pipelines run TruffleHog + gitleaks against full git history on every push
- No secrets, tokens, or credentials are permitted in source code (`.gitignore` enforces `.env`, `*.pem`, `*.key`)

## Dependency Management

- Dependabot monitors pip and GitHub Actions dependencies weekly
- All dependencies are pinned via `pyproject.toml`
