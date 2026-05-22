## Code Quality Gates

## Scope

Applies to review readiness, PR preparation, and pre-merge quality-gate validation.

## Rules

- [MUST] All repositories using this baseline enforce quality gates through pre-commit and CI.
- [MUST] Pre-commit and CI enforce the same logical checks.
- [SHOULD] A change that passes locally also passes in CI without additional manual steps.
- [MUST] CI is the final authority for merge readiness.
- [MUST] Prioritize correctness and regression risk over style.
- [MUST] Validate contract and schema integrity and boundary discipline.
- [MUST] Flag operational risk (idempotency, restartability, observability).
- [MUST] Require tests for risk-heavy behavior changes.
- [MUST] Use explicit typing and return types on public interfaces.
- [SHOULD] Require docstrings for non-trivial modules and functions.
- [MUST] Run lint, format, typing, tests, and coverage checks before merge when practical.
- [MUST] Required quality-gate checks include Ruff linting, Ruff formatting check, Pyright strict type checking, Pytest, coverage threshold, docstring checks, import boundary checks, and architecture tests.
- [MUST] Agents must not bypass checks with `--no-verify` unless explicitly instructed by the human maintainer.

## Review Findings Format

- Severity: `High` | `Medium` | `Low`
- Location: `path:line`
- Risk: what can break
- Recommendation: concrete fix

## Anti-Patterns To Flag

- [MUST] Silent fallback masking broken state.
- [MUST] Broad exception handling without context or re-raise strategy.
- [MUST] Hidden side effects across module boundaries.
- [MUST] Untyped public interfaces.
- [MUST] Contract changes without migration notes.

## Agent Action Checklist

- Read intended behavior and scope first.
- Validate happy path and failure paths.
- Verify tests for changed risk areas.
- Report findings ordered by severity.

## Definition of Done

- Findings are actionable and severity-ranked.
- Risks and missing tests are explicit.
- Documentation, config, and schema impacts are called out.

## Verification Commands

- `ruff check .`
- `ruff format --check .`
- `pyright --level error`
- `pytest -q`
