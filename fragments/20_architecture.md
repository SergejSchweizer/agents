## Architecture

## Scope

Applies to system design, module boundaries, refactors, scalability, reliability, and technical tradeoffs.

## Rules

- [SHOULD] Enforce architecture rules with automated tests.
- [MUST] Required architecture checks include forbidden dependency directions.
- [MUST] Required architecture checks include circular imports.
- [MUST] Required architecture checks include infrastructure leaking into domain logic.
- [MUST] Required architecture checks include presentation or API layers importing persistence internals.
- [MUST] Required architecture checks include shared utilities becoming dependency-heavy.
- [SHOULD] Use `import-linter` or dedicated architecture tests to enforce architecture constraints.
- [MUST] Define contract shape first (types, schema, invariants), then implement.
- [MUST] Keep dependency direction from policy and domain to implementation details.
- [MUST] Keep ownership explicit for each module (inputs, outputs, side effects).
- [MUST] Keep operations idempotent and restart-safe by default.
- [MUST] Use bounded, configurable concurrency.
- [MUST] Keep schema changes backward compatible unless versioned intentionally.
- [SHOULD] Prefer incremental and delta processing over full rescans.
- [SHOULD] Prefer composable functions before introducing pattern-heavy class hierarchies.
- [MAY] Use Strategy, Template Method, Factory, and Repository patterns when they reduce duplication and improve extensibility.
- [SHOULD] Prefer `polars` over `pandas` when ecosystem constraints allow.

## Agent Action Checklist

- Identify architecture impact level (none, local, cross-module).
- If contract changes: define compatibility and migration plan.
- If refactor: preserve behavior and add regression coverage.
- If scalability-sensitive: validate idempotency, ordering, and memory and concurrency bounds.

## Definition of Done

- Module boundaries are explicit.
- Contracts are typed and validated.
- Scalability and reliability implications are addressed.
- Regression tests cover changed behavior.

## Verification Commands

- `pytest -q`
- `ruff check .`
- `mypy .` or `pyright`

## Exceptions and Escalation

- Escalate before large boundary shifts or contract versioning decisions.
