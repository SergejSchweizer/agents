## Agent Workflow

## Scope

Applies to day-to-day agent execution flow for implementation, debugging, and delivery.

## Rules

- [MUST] Before changing code, inspect relevant files.
- [MUST] Before changing code, identify the smallest safe change.
- [MUST] Never commit directly to `main`.
- [MUST] Always create a short-lived, task-specific feature branch from latest `main` using `codex/<scope>-<short-description>`.
- [MUST] Use lowercase letters, numbers, and hyphens only in branch names.
- [MUST] Do not use vague branch names such as `codex/fixes`, `codex/update`, `codex/big-change`, `codex/refactor-all`, or `codex/work`.
- [MUST] Keep one branch to one logical change.
- [MUST] Before starting a task, run `git status`, `git branch --show-current`, `git fetch origin`, `git checkout main`, and `git pull --ff-only origin main`.
- [MUST] If the working tree is not clean before starting, stop and report changed files.
- [MUST] Do not overwrite, delete, stash, reset, or otherwise discard user changes unless explicitly instructed.
- [MUST] Before committing, run `ruff check .`, `pyright`, `pytest`, and `coverage run -m pytest`.
- [MUST] For stacked PRs, replace full-suite `pytest` and coverage runs on intermediate PRs with the smallest meaningful related test set, plus static checks that cover the changed files.
- [MUST] Before the final squash merge of a stacked PR series into `main`, run the full configured validation suite, including full tests and coverage when practical.
- [MUST] If configured, also run `pre-commit run --all-files` and include repository-specific typing or import boundary checks.
- [MUST] If a required check fails, fix it before commit or clearly report why it is unrelated and safe to defer.
- [MUST] Before committing, inspect `git diff` and `git status` and ensure only task-relevant changes are included.
- [MUST] Use concise imperative commit messages.
- [MUST] Push the feature branch and open a pull request into `main`.
- [MUST] Never self-merge a pull request unless explicitly instructed.
- [SHOULD] Prefer squash merge and delete the feature branch after merge.
- [MUST] If rebasing requires history rewrite, only use `git push --force-with-lease`, never plain `git push --force`.
- [MUST] After merge, sync with `git checkout main` and `git pull --ff-only origin main`.
- [MUST] Do not weaken tests to make them pass.
- [MUST] Do not remove type hints.
- [MUST] Do not introduce hidden network calls.
- [MUST] Never commit secrets, credentials, tokens, `.env` files, or private paths.
- [MUST] Do not commit generated local artifacts unless explicitly required by the task.
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
- [MUST] Do not run destructive commands without explicit instruction, including `git reset --hard`, `git clean -fd`, `git clean -fdx`, `git checkout -- .`, `git restore .`, `git stash`, `git push --force`, and `rm -rf`.

## Pull Request Body Template

Remove checks that do not exist in the repository.

```markdown
## Summary

- Describe what changed.
- Describe why it changed.

## Dataset / Pipeline Impact

- State affected datasets, layers, or commands.
- State whether Bronze, Silver, or Gold behavior changed.

## Targeted Validation

- [ ] ruff check .
- [ ] ruff format .
- [ ] mypy .
- [ ] pyright
- [ ] ty check
- [ ] lint-imports --config .importlinter
- [ ] Related pytest subset
- [ ] Related coverage subset, if coverage is impacted

## Full Final Validation

- [ ] Full pytest
- [ ] Full pytest coverage
- [ ] pre-commit run --all-files

## Risk

- Low / Medium / High
- Explain possible breakage or migration concerns.

## Notes

- Mention follow-up work.
- Mention known limitations.
```

## Agent Action Checklist

- Reproduce issue with deterministic inputs.
- Verify clean working tree before branch creation.
- Create focused branch from latest `main`.
- Identify impacted contracts, side effects, and test scope.
- Implement minimal fix or focused improvement.
- Inspect diff to keep only task-related files.
- Push branch and open PR targeting `main`.
- Validate with quality gates and tests.
- Do not merge without explicit instruction.
- Summarize risks, residual gaps, and follow-up work.

## Definition of Done

- Requested change is implemented and validated.
- Work enters `main` only through a pull request from a focused feature branch.
- Debug and failure paths are observable.
- Docs and tests match the updated behavior.

## Verification Commands

- `pytest -q`
- `ruff check .`
- `ruff format --check .`
- `git status`
- `git branch --show-current`
- `git fetch origin`
- `git checkout main`
- `git pull --ff-only origin main`
- `git checkout -b codex/<task-name>`
- `git diff`
- `gh pr create --base main --head codex/<task-name> --fill`
- `gh pr checks`
