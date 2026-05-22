## Core Rules

## Scope

Always active across all modules and workflows.

## Rules

- [MUST] Prefer the smallest safe change that fully resolves the issue.
- [MUST] Preserve backward compatibility by default.
- [MUST] Keep business logic separate from framework/storage details.
- [MUST] Isolate side effects behind explicit interfaces and adapters.
- [MUST] Keep execution deterministic where feasible.
- [MUST] Keep operational docs aligned with behavior changes.
- [MUST] Use one shared logfile path defined in `config.yaml`.
- [MUST] Use one consistent log structure across modules.
- [SHOULD] Add comments for non-obvious decisions, invariants, and tradeoffs.
- [SHOULD] Avoid comments that only restate obvious code.
- [MUST] Enforce deny-by-default `.gitignore` patterns, with minimal explicit allowlist.

## Agent Action Checklist

- Before edit: identify contract boundaries and side effects.
- During edit: keep module responsibilities cohesive.
- After edit: confirm logging path and format consistency plus docs alignment.

## Definition of Done

- Boundaries remain explicit.
- Logging is centralized and consistent.
- Documentation reflects behavior.

## Verification Commands

- `rg -n "logfile|logging|config.yaml" .`
- `ruff check .`
- `pytest -q`

## Exceptions and Escalation

- Escalate if a required change introduces unavoidable compatibility break.
