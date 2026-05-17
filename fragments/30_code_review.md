## Code Review

Apply these rules when reviewing changes, preparing PRs, or running quality gate validation before merge.

### Review Priorities

- Bugs and behavioral regressions.
- Contract and schema integrity.
- Architectural boundary violations.
- Missing tests for risk-heavy logic.
- Operational risk (idempotency, restartability, observability).

### Severity Model

- High: correctness, data loss/corruption, security, broken contracts, runtime failure.
- Medium: maintainability hazards, missing edge-case handling, observability gaps.
- Low: style/documentation polish, non-blocking improvements.

### Code Quality Rules

- Use type hints consistently, including explicit return types.
- Require docstrings for non-trivial modules/functions and concise usage notes for public interfaces.
- Keep code compatible with explicit quality tooling.

Preferred tooling:

- Linting: `ruff` (or configured equivalent).
- Formatting: `ruff format` (or configured equivalent).
- Type checking: `mypy` or `pyright` (project standard).
- Tests: `pytest` (or configured equivalent).
- Import boundaries: `lint-imports` (or configured equivalent).

Pre-commit quality gates must include lint, format, typing, import-boundary checks, tests, and coverage.

### Review Workflow

1. Understand intended behavior and scope.
2. Validate correctness and contract compatibility first.
3. Check failure paths, error messaging, and observability.
4. Verify tests and coverage for changed risk areas.
5. Check documentation, configuration, and schema alignment.
6. Report findings ordered by severity with actionable guidance.

### Anti-Patterns To Flag

- Silent fallback that hides broken state.
- Broad exception handling without context or re-raise strategy.
- Hidden side effects across module boundaries.
- Untyped public interfaces.
- Contract changes without migration notes.

### PR Guidance

- Keep scope focused.
- Add/update tests.
- Update relevant docs.
- Note architectural implications and rollback/mitigation notes for operational risk.

---
