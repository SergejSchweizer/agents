## Purpose

This repository provides a reusable AGENTS.md baseline for integration into other repositories.

## Scope

Applies to all agent-assisted implementation, refactoring, review, testing, and documentation work.

## Rules

- [MUST] Optimize for maintainability, modularity, reproducibility, testability, documentation quality, and extensibility.
- [MUST] Keep behavior understandable without tribal knowledge.
- [MUST] Prefer explicit contracts, deterministic behavior, and clear ownership of side effects.
- [SHOULD] Favor simple, composable designs over clever abstractions.
- [SHOULD] Preserve backward compatibility unless a breaking change is intentional and documented.

## Agent Action Checklist

- Confirm task scope and expected behavior.
- Identify affected contracts, tests, and docs before editing.
- Apply smallest safe change first.
- Validate behavior and update docs in the same change set.

## Definition of Done

- Change is correct, testable, and understandable.
- Contracts and behavior are explicit.
- Relevant docs and tests are aligned.

## Verification Commands

- `ruff check .`
- `ruff format --check .`
- `pytest -q`

## Exceptions and Escalation

- Ask for confirmation before intentional breaking changes.
- Escalate when requirements conflict or risk data correctness.
