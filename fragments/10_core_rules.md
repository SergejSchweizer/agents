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
