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
- [MUST] Use one shared log root path defined in `config.yaml`, and it must point to the `.logs` directory.
- [MUST] Every module writes to its own logfile under the shared `.logs` directory.
- [MUST] Use one consistent log message structure across all modules.
- [MUST] Do not comment obvious code.
- [SHOULD] Add comments for non-obvious decisions, invariants, and tradeoffs.
- [MUST] Comments and docstrings explain non-obvious decisions, invariants, edge cases, tradeoffs, external system assumptions, and failure handling.
- [MUST] Add inline comments for important non-obvious data logic, including forward-fill, interpolation, resampling, timestamp normalization, timezone handling, rolling windows, and numerical stability safeguards.
- [MUST] For market-data and derivatives workflows, inline comments must document funding normalization, open-interest reconstruction, option-surface reconstruction, feature engineering decisions, leakage prevention, and exchange-specific behavior.
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

- `rg -n "logfile|logging|config.yaml|\\.logs" .`
- `ruff check .`
- `pytest -q`

## Exceptions and Escalation

- Escalate if a required change introduces unavoidable compatibility break.
