# agents

Lightweight AGENTS.md installer and updater for any existing Git repository.
Test coverage: 96.67%

This repository provides:

- a central `AGENTS.md` built from source fragments
- `fragments/*.md` as editable source files
- `install_agents.py` to install/update it in a target project
- an optional pre-commit sync mechanism
- centralized logging configured via `config.yaml` (`logfile` key)

## Install in any project

Run this from the root of your target project:

```bash
curl -fsSL https://raw.githubusercontent.com/SergejSchweizer/agents/main/install_agents.py | python3
```

### Step-by-step in a project repository

```bash
git init my-project
cd my-project
curl -fsSL https://raw.githubusercontent.com/SergejSchweizer/agents/main/install_agents.py | python3
```

Check installation:

```bash
ls -la AGENTS.md
ls -la scripts/sync_agents.py
ls -la .git/hooks/pre-commit
```

### Alternative: run installer from a local clone

```bash
git clone https://github.com/SergejSchweizer/agents.git
cd my-project
python ../agents/install_agents.py
```

What it does:

1. Detects the current Git repository root.
2. Downloads the latest central AGENTS fragments.
3. Builds and writes/updates `<project-root>/AGENTS.md`.
4. Creates/updates `<project-root>/scripts/sync_agents.py`.
5. Creates/updates shared logging helpers:
   - `<project-root>/scripts/runtime_config.py`
   - `<project-root>/scripts/logging_utils.py`
6. Creates/updates `<project-root>/config.yaml` with the shared logfile path.
7. Adds or updates a managed block in `<project-root>/.git/hooks/pre-commit`.

The managed hook block runs:

- `python scripts/sync_agents.py` if available
- otherwise `python3 scripts/sync_agents.py`

If network access is unavailable, sync prints a warning and continues so commits are not blocked.

## Manual update command

From your target project root:

```bash
python scripts/sync_agents.py
```

## Logging configuration

All modules write to the same logfile configured in `config.yaml`:

```yaml
logfile: logs/agents.log
```

## Idempotency

- Running the installer multiple times is safe.
- The hook managed block is not duplicated.
- `AGENTS.md` is overwritten only when the built content changed.

## Source layout in this repository

- `fragments/*.md` are the source-of-truth sections.
- `AGENTS.md` is the concatenated output of those fragments.
- Installer and sync script both build `AGENTS.md` from the same fragment list.

## Expected target project files

After installation:

- `AGENTS.md`
- `scripts/sync_agents.py`
- `.git/hooks/pre-commit` (with a managed AGENTS sync block)
