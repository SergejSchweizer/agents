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
- Prefer `polars` over `pandas` for dataframe processing when it fits the task and ecosystem constraints.
- Prioritize long-term maintainability over short-term convenience.

### Interface and Contract Practices

- Define contract shape first (types, schema, invariants), then implement.
- Make invalid states unrepresentable with DTOs, enums/literals, and validation.
- Keep backward compatibility by default; version only intentional breaking changes.
- Keep ownership explicit for each module (inputs, outputs, side effects).

### Design Patterns Policy

Use patterns pragmatically only when they reduce duplication, improve clarity, or improve safe extensibility.

Preferred usage:

- Strategy pattern for interchangeable behaviors.
- Template Method for shared orchestration with well-defined variant steps.
- Factory pattern for constructing typed clients/services.
- Repository/DAO boundaries for storage access and persistence isolation.

Rules:

- Do not introduce patterns as ceremony.
- Keep pattern boundaries explicit and discoverable.
- Prefer small pure helper functions before introducing classes.
- Pattern-introducing refactors must preserve behavior and include regression tests.

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

### Architecture Review Checklist

- Are layering boundaries preserved?
- Does dependency direction flow from policy to implementation?
- Are contracts explicit, typed, and validated?
- Is the change idempotent and restart-safe where required?
- Are tradeoffs, risks, and migration implications documented?

---
