## Testing

Apply these rules when adding/changing tests, fixing bugs, refactoring behavior, adding CLI commands, or validating release readiness.

### Testing Rules

- Run targeted tests for changed areas.
- Run full test suite before finalization when practical.
- Disclose any checks that could not run and why.
- Add regression tests for every bug fix.
- Test happy path, edge cases, and failure paths.
- Keep tests deterministic.

### Test Design Practices

- Prefer behavior-focused tests over implementation-coupled tests.
- Use small, named fixtures with explicit setup intent.
- Cover boundary values, empty inputs, and malformed inputs.
- Validate outcomes and failure modes (error types/messages).

### Coverage Policy (MANDATORY)

- Target repository test coverage is 90%.
- Preserve or improve coverage for meaningful changes.
- Prioritize highest-risk paths first: correctness, persistence, contracts, orchestration, failure handling.
- If measured coverage is below 90%, disclose the gap and required follow-up work.

### Refactoring Validation

For large changes:

1. Split work into small, testable steps.
2. Run targeted tests after each step.
3. Keep behavior stable between steps.
4. Re-run full tests and quality gates at the end.
5. Update docs in the same change set when behavior/process changed.

### CLI Validation

- Every new or modified CLI command must have dedicated automated tests.
- CLI commands must run autonomously as standalone invocations.

---
