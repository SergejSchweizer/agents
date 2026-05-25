## Python Tooling

## Scope

Applies to Python quality tooling, typing, formatting, and local validation commands.

## Rules

- [MUST] Python code is fully typed.
- [MUST] Public functions have explicit parameter and return types.
- [MUST] Implicit `Any` is not allowed.
- [MUST] Untyped public APIs are not allowed.
- [MUST] Every `# type: ignore` includes a precise explanation.
- [MUST] Runtime data crossing boundaries uses typed DTOs, dataclasses, Pydantic models, TypedDicts, or explicit schemas.
- [MUST] Prefer making invalid states unrepresentable.
- [MUST] Configure Python tooling primarily in `pyproject.toml`.
- [SHOULD] Configure `ruff`, `pyright`, `pytest`, `coverage`, and docstring tooling via `pyproject.toml` when supported.
- [SHOULD] Avoid scattered configuration files unless a tool does not support `pyproject.toml`.
- [MUST] Keep code compatible with the configured formatter, linter, type checker, and test runner.
- [MUST] Pyright and other configured Python quality tools must run in strict mode where supported.
- [MUST] Do not relax tool strictness or suppress failures globally to make checks pass.
- [MUST] Use type hints consistently, including explicit return types for public interfaces.
- [MUST] Public modules, public classes, public functions, CLIs, and architectural boundaries have concise docstrings.
- [MUST] Keep import boundaries compatible with repository rules when boundary tooling is configured.
- [SHOULD] Prefer one canonical command sequence for local validation to reduce drift across contributors.

## Agent Action Checklist

- Run lint and format checks before finalizing changes.
- Run type checks for modified modules.
- Run targeted tests first, then broader tests when practical.
- Report any tool that could not be run and why.

## Definition of Done

- Lint, format, typing, and test signals are green or explicitly documented.
- Public interfaces stay typed and understandable.

## Verification Commands

- `ruff check .`
- `ruff format --check .`
- `mypy .` or `pyright`
- `pytest -q`
