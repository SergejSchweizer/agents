## Release and Sync

## Scope

Applies to pre-commit synchronization, release readiness, and repository-wide instruction consistency.

## Rules

- [MUST] `AGENTS.md` is generated from `fragments/*.md`.
- [MUST] Agents must not edit `AGENTS.md` directly.
- [MUST] All durable instruction changes must be made in the corresponding fragment file.
- [MUST] After modifying fragments, regenerate `AGENTS.md` and verify generated output is deterministic.
- [MUST] Keep `AGENTS.md` synchronized with fragment source files.
- [MUST] Keep pre-commit sync behavior non-blocking when network access is unavailable.
- [MUST] Keep generated repository instructions deterministic and reproducible.
- [SHOULD] Keep release scope focused and include rollback or mitigation notes for operational risk.
- [MUST] Disclose skipped quality checks and unresolved risks before release.

## Agent Action Checklist

- Confirm fragments are the source of truth.
- Never edit `AGENTS.md` directly for durable policy updates.
- Regenerate or sync `AGENTS.md` after fragment updates.
- Verify determinism by re-running generation and confirming no diff.
- Verify pre-commit sync hook still points to the managed sync script.
- Validate release notes include testing status and known gaps.

## Definition of Done

- `AGENTS.md` matches current fragment set.
- Sync path is operational and documented.
- Release state includes quality-gate and risk visibility.

## Verification Commands

- `python scripts/sync_agents.py`
- `git diff -- AGENTS.md fragments`
- `pytest -q`
