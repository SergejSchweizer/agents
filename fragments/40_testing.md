## Testing

## Scope

Applies when adding or changing tests, fixing bugs, refactoring behavior, adding CLI commands, or validating release readiness.

## Rules

- [MUST] Run targeted tests for changed areas.
- [SHOULD] Run full test suite before finalization when practical.
- [MUST] Disclose checks that could not run and why.
- [MUST] Add regression tests for every bug fix.
- [MUST] Test happy path, edge cases, and failure paths.
- [MUST] Keep tests deterministic.
- [MUST] Run `coverage run -m pytest` and `coverage report` for release-ready validation when practical.

## Coverage Policy

- [MUST] Target repository coverage is 90%.
- [MUST] Preserve or improve coverage for meaningful changes.
- [MUST] If coverage is below 90%, disclose the gap and follow-up work.

## CLI Validation

- [MUST] Every new or modified CLI command has dedicated automated tests.
- [MUST] CLI commands run autonomously as standalone invocations.
- [MUST] Every CLI exposes a `--debug` flag for extensive logging.
- [MUST] Treat logs as a primary debug source for CLI diagnosis.
- [MUST] When debugging, run CLI commands with `--debug` where available and or add targeted log messages.
- [MUST] While a script is running, actively analyze logfile output.

## Agent Action Checklist

- Reproduce with deterministic inputs.
- Execute CLI with `--debug` during diagnosis.
- Analyze logfile output while process runs.
- Add or refine logs only where they improve failure isolation.
- Add or adjust tests before finalizing the fix.
- Run the documented pre-commit command sequence before finalizing: Ruff, `interrogate`, `pydoclint`, type checks, tests, and coverage.

## Definition of Done

- Bug and feature behavior is covered by tests.
- Debug path is observable from logs.
- Coverage impact is reported.

## Verification Commands

- `pytest -q`
- `pytest --maxfail=1 -q`
- `pytest --cov --cov-report=term-missing`
- `coverage run -m pytest`
- `coverage report`

## Exceptions and Escalation

- Escalate if deterministic reproduction is not possible without production-only dependencies.
