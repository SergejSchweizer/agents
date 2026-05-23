## Agent Workflow

## Scope

Applies to day-to-day agent execution flow for implementation, debugging, and delivery.

## Rules

- [MUST] Before changing code, inspect relevant files.
- [MUST] Before changing code, identify the smallest safe change.
- [MUST] Never commit directly to `main`.
- [MUST] Always create a feature branch.
- [MUST] Before committing, run `ruff check .`, `pyright`, `pytest`, and `coverage run -m pytest`.
- [MUST] Do not weaken tests to make them pass.
- [MUST] Do not remove type hints.
- [MUST] Do not introduce hidden network calls.
- [MUST] Keep architecture boundaries explicit.
- [SHOULD] Prefer small, reviewable commits.
- [MUST] Preserve existing public contracts unless explicitly asked to change them.
- [MUST] Add or update tests for behavioral changes.
- [MUST] Run relevant quality gates.
- [MUST] Report any checks that could not be executed.
- [MUST] Do not introduce large rewrites when a targeted change is sufficient.
- [MUST] Understand intended behavior and scope before editing.
- [MUST] Prefer the smallest safe change that resolves the issue.
- [MUST] Keep behavior stable during refactors unless a change is intentional and documented.
- [MUST] Update tests and documentation in the same change set for behavior changes.
- [MUST] During debugging, run CLI commands with `--debug` where available and analyze logfile output while scripts run.
- [SHOULD] Add targeted diagnostic logs when they improve failure isolation.

## Agent Action Checklist

- Reproduce issue with deterministic inputs.
- Identify impacted contracts, side effects, and test scope.
- Implement minimal fix or focused improvement.
- Validate with quality gates and tests.
- Summarize risks, residual gaps, and follow-up work.

## Definition of Done

- Requested change is implemented and validated.
- Debug and failure paths are observable.
- Docs and tests match the updated behavior.

## Verification Commands

- `pytest -q`
- `ruff check .`
- `ruff format --check .`
