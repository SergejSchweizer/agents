# AGENTS.md

## Purpose

This repository provides a generic, reusable agent instruction baseline for integration into other repositories (for example via `git subtree`).

All coding agents must optimize for:

- maintainability
- modularity
- reproducibility
- testability
- documentation quality
- scientific/technical rigor (when applicable)
- future extensibility

The codebase must be understandable by another engineer without tribal knowledge.

---

## Core Rules (Always Active)

### Minimum Change Principle

- Prefer the smallest safe change that fully resolves the problem.
- Prefer clarity over cleverness.
- Preserve backward compatibility unless a breaking change is intentional and documented.

### Modularity And Interfaces

- Keep module boundaries explicit and cohesive.
- Keep side effects isolated behind adapters/interfaces.
- Keep business logic separate from framework/storage details.

### Reproducibility

- Keep execution paths deterministic where feasible.
- Version important artifacts and schemas.
- Preserve seeds and runtime configuration needed for reproducible runs.

### Documentation

- Keep operational docs aligned with code behavior.
- Do not leave critical behavior changes undocumented.

---

## Architecture

Apply these rules when a task involves system design, module boundaries, refactoring strategy, scalability, reliability, or technical tradeoffs.

### Architecture Goals

- Preserve clear modular separation and explicit interfaces.
- Optimize for maintainability, extensibility, and reproducibility.
- Keep business logic separated from infrastructure and framework details.

### Definition Of Done (Architecture)

- Boundaries and responsibilities are explicit in code structure and naming.
- New/changed contracts are documented and validated at boundaries.
- Scalability and reliability implications are addressed (not deferred implicitly).
- Refactor behavior is covered by regression tests.

### Architecture Rules

- Keep modules isolated and cohesive.
- Avoid monolithic scripts for core logic.
- Move reusable notebook logic into versioned modules.
- Prefer composable designs and separation of concerns.
- Prioritize long-term maintainability over short-term convenience.

### Interface and Contract Practices

- Define contract shape first (types, schema, invariants), then implement.
- Make invalid states unrepresentable with DTOs, enums/literals, and validation.
- Keep backward compatibility by default; version only intentional breaking changes.
- Keep ownership explicit for each module (inputs, outputs, side effects).

### Design Patterns Policy

Use patterns pragmatically only when they reduce duplication, improve clarity, or improve safe extensibility.

Preferred usage:

- Strategy pattern for interchangeable behaviors (provider adapters, fetch policies, serialization policies).
- Template Method for shared orchestration with small, well-defined variant steps.
- Factory pattern for constructing typed clients/services without leaking wiring details.
- Repository/DAO boundaries for storage access to avoid persistence logic in domain workflows.

Rules:

- Do not introduce patterns as ceremony; justify with concrete simplification.
- Keep pattern boundaries explicit and discoverable in module structure and naming.
- Prefer small pure helper functions before introducing classes.
- Refactors that introduce patterns must preserve behavior and include regression tests.

### Scalability and Reliability Policy

Technical decisions must account for growth in data volume, entities/users/traffic, history size, job frequency, and integrations/providers.

Required implications:

- Prefer incremental/delta processing over full rescans when feasible.
- Keep operations idempotent.
- Use bounded, configurable concurrency.
- Keep schema changes backward compatible and versioned.
- Preserve observability (progress, throughput, error isolation).
- Use storage/index strategies that remain efficient as volume grows.

### Operational Design Practices

- Design workflows to be restart-safe and idempotent by default.
- Bound memory and concurrency with explicit configuration knobs.
- Isolate external dependencies with adapters to support retries, fallback, and test doubles.
- Prefer deterministic ordering and deduplication in persistent outputs.

### Additional Architecture Best Practices

- Prefer layered architecture with clear boundaries: interface (CLI/API), application/service, domain, infrastructure.
- Enforce dependency direction: higher-level policy must not depend on lower-level implementation details.
- Make module ownership explicit (who reads/writes which dataset or contract).
- Use contract-first development for pipelines: schema, keys, partitioning, and invariants are part of the interface.
- Favor backward-compatible evolution for contracts; version breaking changes.
- Keep side effects isolated behind adapters (HTTP client, parquet IO, filesystem, clock, random source).
- Design idempotency and restartability as first-class requirements.

### Development Heuristics for Architecture Work

- Optimize for the smallest safe change that fully resolves the problem.
- Prefer clarity over cleverness.
- Keep one concern per commit/PR whenever practical.
- Preserve externally observable behavior during refactors unless a breaking change is intentional and documented.

### Architecture Review Checklist

- Are layering boundaries preserved (interface/application/domain/infrastructure)?
- Does dependency direction flow from policy to implementation?
- Are contracts explicit, typed, and validated?
- Is the change idempotent and restart-safe where required?
- Are tradeoffs, risks, and migration implications documented?

---

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

#### Type Safety

- Use type hints consistently.
- Functions should have explicit return types.

#### Documentation

- Non-trivial functions/modules require docstrings.
- Public interfaces should include concise usage guidance.

#### Formatting and Static Checks

Code must remain compatible with explicit quality tooling. Use the project's configured tool for each category:

- Linting: `ruff` (or `flake8`/`pylint` if that is the configured project standard).
- Formatting: `ruff format` (or `black` if that is the configured project standard).
- Type checking: `mypy` or `pyright` (use the one configured by the project, or both if required).
- Tests: `pytest` (or the project's configured equivalent test runner).
- Import boundaries: `lint-imports` or an equivalent architecture-boundary checker.

#### Pre-Commit Quality Gates (MANDATORY)

Run explicit tooling commands for all quality gates:

- Lint command (for example `ruff check .`).
- Format check command (for example `ruff format --check .`).
- Static type command(s) (for example `mypy .` and/or `pyright`).
- Import boundary command (for example `lint-imports`).
- Configuration validation command.
- Test suite command (for example `pytest`).
- Coverage-enabled test command (for example `pytest --cov`).

Rules:

- Prefer full hook-equivalent set before finalizing meaningful changes.
- If narrower runs are used during iteration, run full set before completion whenever practical.
- If a required check cannot run, explicitly state which command and why.
- Do not claim completion while mandatory checks fail.
- Report coverage measurement in final summary.

### Review Workflow

1. Understand the intended behavior and scope.
2. Validate correctness and contract compatibility first.
3. Check failure paths, error messaging, and observability.
4. Verify tests and coverage for changed risk areas.
5. Check docs/config/schema alignment.
6. Report findings ordered by severity with actionable fix guidance.

### Error Handling and Contracts

- Fail fast on invalid inputs and invariant violations.
- Raise specific exceptions; avoid broad `except Exception` without structured handling.
- Error messages must include actionable context (symbol, exchange, date range, dataset).
- Public interfaces must document expected inputs/outputs and failure modes.
- Validate I/O boundaries (API payloads, schema fields, config keys).

### Common Anti-Patterns To Flag

- Silent fallback that hides broken state.
- Broad exception handling without context or re-raise strategy.
- Hidden side effects across module boundaries.
- Untyped/loosely typed public interfaces.
- Contract changes without migration notes.

### Observability and Performance

- Use structured, context-rich logs for batch and long-running tasks.
- Include progress indicators for backfills (task index, symbol, time range, row count, elapsed time).
- Warn on partial/fallback behavior and hard limits (pagination caps, retries, truncation).
- Avoid repeated full scans when incremental strategy exists.
- Keep memory usage bounded for large backfills.
- Make expensive operations configurable (timeouts, concurrency, page sizes).
- Prefer deterministic deduplication and stable ordering.

### Git Hygiene and Commits

- Do not track local-only artifacts or caches in version control.
- If local-only files are tracked accidentally, remove from git index while preserving local copies.
- Use Conventional Commits: `type(scope): short summary`.
- Allowed types: feat, fix, refactor, test, docs, chore, ci, build, perf.

### Documentation Consistency (MANDATORY)

- For essential code changes, compare project documentation against actual behavior.
- Fix inconsistencies in the same change set.

### PR / Change Guidance

For meaningful changes:

- Keep scope focused.
- Add/update tests.
- Update relevant docs.
- Note architectural implications.

For non-trivial changes, include:

- Rationale and tradeoffs.
- Rollback/mitigation notes for operational risk.
- Explicit note of config/schema/doc updates (or confirmation none were required).

### Review Output Format (Recommended)

- Findings: ordered by severity, with file/path context and impact.
- Open questions/assumptions: only where behavior is ambiguous.
- Summary: brief change quality assessment and merge readiness.

### Failure Conditions

Do not:

- Leave undocumented critical behavior changes.
- Skip validation without disclosure.
- Introduce unverifiable claims in docs/reports.
- Leave stale docs after essential code changes.

---

## Testing

Apply these rules when adding/changing tests, fixing bugs, refactoring behavior, adding CLI commands, or validating release readiness.

### Testing Rules

After meaningful code changes, run relevant checks and tests.

Minimum expectation:

- Run targeted tests for changed areas.
- Run full test suite before finalization when practical.

If checks cannot be run, explicitly state what was not run and why.

Additional expectations:

- Add regression tests for every bug fix.
- Test happy path, edge cases, and failure path for changed logic.
- Keep tests deterministic (fixed timestamps/seeds/fixtures; no flaky external dependencies).
- For pipeline logic, validate idempotency and rerun behavior where relevant.

### Test Design Practices

- Prefer behavior-focused tests over implementation-coupled tests.
- Use small, named fixtures with explicit setup intent.
- Cover boundary values, empty inputs, and malformed inputs.
- Validate both positive outcomes and failure modes (error types/messages).
- Use stable clocks/random seeds via injection or fixed fixtures.

### Coverage Policy (MANDATORY)

- Target repository test coverage is 90%.
- For meaningful changes, preserve or improve coverage and avoid uncovered critical paths.
- For core pipeline code (bronze/silver/gold transforms, fetch/gap-fill, CLI orchestration), keep tests near or above target.
- If measured coverage is below 90%, disclose the gap and list follow-up test work.

Risk-prioritized closure:

1. Cover highest-risk paths first: data correctness, persistence, schema/contract integrity, CLI orchestration, failure handling.
2. Then medium-risk: adapter pagination/retry logic, transformation edge cases, idempotency/rerun behavior.
3. Then lower-risk: presentation/plotting helpers and thin wrappers.
4. Continue iteratively until measured coverage is at least 90%.

### Regression Policy

- Every bug fix must include a regression test that fails before the fix and passes after.
- For refactors, keep behavior-lock tests in place before structural changes.
- For data contracts, add tests for schema evolution and backward compatibility.

### Stepwise Refactoring Procedure (MANDATORY after large changes)

For architecture updates, cross-module behavior changes, medallion pipeline changes, or schema-affecting updates:

1. Split work into small, testable steps.
2. After each step, run targeted tests for the changed area.
3. Keep behavior stable between steps; do not mix refactor + feature + broad cleanup.
4. Commit only when current step is green and reversible.
5. Re-run full tests and quality gates after final step.
6. Update documentation in the same change set when behavior/process changed.

Rules:

- Do not execute all-at-once refactors without intermediate validation.
- If a step cannot be validated, stop and report blocker/risks before continuing.
- Preserve backward compatibility unless a breaking contract is intentional and documented.

### CLI Command Validation (MANDATORY)

- Every newly added CLI command must work autonomously as a standalone command invocation.
- Every newly added CLI command must have dedicated automated tests validating independent execution path and expected behavior.
- CLI command tests must run whenever a CLI command is added or modified.

### Test Pyramid Guidance

- Unit tests: majority of coverage, fast, deterministic.
- Integration tests: validate module boundaries and infrastructure adapters.
- End-to-end tests: critical user flows and orchestration only.

### Definition Of Done (Testing)

- Relevant targeted tests executed for changed areas.
- Full suite executed before finalization when practical.
- Coverage result reported and gap disclosed if below target.
- No known flaky tests introduced by the change.

---

## Security

Apply these rules when touching configuration, credentials, secrets handling, runtime environment, or sensitive data paths.

### Security Rules

- Never commit secrets or credentials.
- Use environment variables and local config files for sensitive values.
- Keep sensitive config out of version control unless explicitly designed otherwise.
- Keep required runtime variables documented in the canonical runtime configuration.
- Do not place live secret values in docs.

### Security Engineering Practices

- Apply least privilege to runtime identities, tokens, and file permissions.
- Validate and sanitize all external inputs at trust boundaries.
- Prefer explicit allowlists over implicit trust.
- Keep dependency and supply-chain risk visible (pin versions, review updates).
- Treat logs, metrics, and traces as potential data exfiltration paths.

### Configuration Security Policy (MANDATORY)

- Use one canonical runtime configuration source for the repository.
- Runtime usage without that canonical configuration source is not allowed.
- Ad-hoc local environment files must not be used as the runtime source of truth.
- If canonical configuration keys change, update configuration structure and docs in the same change set.

### Secrets Management

- Never hardcode credentials in source, tests, notebooks, or scripts.
- Use environment-specific secret stores/injection at runtime.
- Rotate compromised or exposed credentials immediately.
- Redact secrets in all developer tooling output and captured logs.

### Logging and Data Safety

- Never log secrets or sensitive values.
- Log only the minimum required operational context.
- Validate external I/O boundaries (payload shape, schema fields, config keys) before usage.

### Security Review Checklist

- Are secrets excluded from code, docs, and committed artifacts?
- Are config and runtime contracts explicit and validated?
- Are permissions and access scopes minimized?
- Are error messages actionable without leaking sensitive data?
- Are third-party interactions bounded by timeouts/retries and input validation?

---

## End Goal

Any repository using these instructions should remain:

- production-grade for engineers
- reproducible for operators/researchers
- understandable for reviewers
- extensible for future contributors and agents
