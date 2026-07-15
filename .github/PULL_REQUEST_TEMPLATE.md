## Summary
<!-- Describe the change and why -->

## Script(s) Affected
- [ ] New script
- [ ] Modified existing script: `___`
- [ ] Library change only

## Danger Classification
- [ ] Safe (read-only)
- [ ] Destructive-adjacent
- [ ] Destructive
- [ ] Security-critical

## Dry-run behaviour verified?
- [ ] `--dry-run` produces expected output with no side-effects
- [ ] Integration test updated / added

## Checklist
- [ ] `make validate` passes locally
- [ ] Structured audit logging via `jol_logger`
- [ ] Destructive actions gated by `jol_confirm`
- [ ] `--dry-run` flag implemented (if applicable)
- [ ] No secrets, tokens, or credentials in code
- [ ] CHANGELOG.md updated
