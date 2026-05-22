#!/usr/bin/env python3
"""Install and maintain AGENTS.md in the current Git repository."""

from __future__ import annotations

import logging
import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from typing import cast
from urllib.error import URLError
from urllib.request import urlopen

RAW_BASE_URL = "https://raw.githubusercontent.com/SergejSchweizer/agents/main"
FRAGMENTS = [
    "fragments/00_purpose.md",
    "fragments/10_core_rules.md",
    "fragments/20_architecture.md",
    "fragments/30_code_quality_gates.md",
    "fragments/40_testing.md",
    "fragments/50_python_tooling.md",
    "fragments/60_agent_workflow.md",
    "fragments/70_security.md",
    "fragments/80_release_and_sync.md",
]
CONFIG_RELATIVE_PATH = Path("config.yaml")
SYNC_SCRIPT_RELATIVE_PATH = Path("scripts") / "sync_agents.py"
RUNTIME_CONFIG_RELATIVE_PATH = Path("scripts") / "runtime_config.py"
LOGGING_UTILS_RELATIVE_PATH = Path("scripts") / "logging_utils.py"
HOOK_RELATIVE_PATH = Path(".git") / "hooks" / "pre-commit"
HOOK_BLOCK_START = "# >>> agents-sync (managed) >>>"
HOOK_BLOCK_END = "# <<< agents-sync (managed) <<<"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
BOOTSTRAP_LOGFILE = Path("logs") / "agents.log"

CONFIG_YAML_CONTENT = "logfile: logs/agents.log\n"
RUNTIME_CONFIG_SCRIPT_CONTENT = """#!/usr/bin/env python3
\"\"\"Runtime configuration loading utilities.\"\"\"

from __future__ import annotations

from pathlib import Path


def read_logfile_from_config(config_path: Path | None = None) -> Path:
    \"\"\"Read the logfile path from config.yaml.\"\"\"
    path = config_path or Path("config.yaml")
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() != "logfile":
            continue
        cleaned = value.strip().strip("'\\\"")
        if not cleaned:
            raise ValueError("config.yaml key 'logfile' must not be empty")
        return Path(cleaned)

    raise ValueError("config.yaml must define a top-level 'logfile' key")
"""

LOGGING_UTILS_SCRIPT_CONTENT = """#!/usr/bin/env python3
\"\"\"Shared logging configuration for scripts.\"\"\"

from __future__ import annotations

import logging
from pathlib import Path

from scripts.runtime_config import read_logfile_from_config

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def configure_logger(name: str, config_path: Path | None = None) -> logging.Logger:
    \"\"\"Configure and return a module logger using shared config.yaml logfile.\"\"\"
    logfile_path = read_logfile_from_config(config_path)
    logfile_path.parent.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    if not getattr(root_logger, "_agents_logging_configured", False):
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler = logging.FileHandler(logfile_path, encoding="utf-8")
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        root_logger.handlers.clear()
        root_logger.addHandler(file_handler)
        root_logger.addHandler(stream_handler)
        root_logger.setLevel(logging.INFO)
        setattr(root_logger, "_agents_logging_configured", True)

    return logging.getLogger(name)
"""

SYNC_SCRIPT_CONTENT = f"""#!/usr/bin/env python3
\"\"\"Sync AGENTS.md from central AGENTS fragments.\"\"\"

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path
from typing import cast
from urllib.error import URLError
from urllib.request import urlopen

# Ensure repository root is importable, even when invoked from hook contexts.
SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.logging_utils import configure_logger

RAW_BASE_URL = "{RAW_BASE_URL}"
FRAGMENTS = [
    "fragments/00_purpose.md",
    "fragments/10_core_rules.md",
    "fragments/20_architecture.md",
    "fragments/30_code_quality_gates.md",
    "fragments/40_testing.md",
    "fragments/50_python_tooling.md",
    "fragments/60_agent_workflow.md",
    "fragments/70_security.md",
    "fragments/80_release_and_sync.md",
]
LOGGER = logging.getLogger(__name__)


def download_text(url: str) -> str:
    with urlopen(url, timeout=15) as response:
        return cast(str, response.read().decode("utf-8"))


def build_agents_content() -> str:
    parts = []
    for fragment in FRAGMENTS:
        url = f"{{RAW_BASE_URL}}/{{fragment}}"
        LOGGER.info("Downloading %s", url)
        parts.append(download_text(url).rstrip())
    return "\\n\\n".join(parts) + "\\n"


def stage_agents_file(repo_root: Path) -> None:
    result = subprocess.run(
        ["git", "add", "AGENTS.md"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "unknown error"
        LOGGER.warning("Could not stage AGENTS.md: %s", message)
    else:
        LOGGER.info("Staged updated AGENTS.md")


def main() -> int:
    configure_logger("agents-sync", REPO_ROOT / "config.yaml")
    repo_root = REPO_ROOT
    agents_path = repo_root / "AGENTS.md"

    try:
        remote_content = build_agents_content()
    except URLError as exc:
        LOGGER.warning("Could not download AGENTS fragments: %s", exc)
        LOGGER.info("Continuing without updates.")
        return 0
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("Unexpected download error: %s", exc)
        LOGGER.info("Continuing without updates.")
        return 0

    local_content = (
        agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    )
    if local_content == remote_content:
        LOGGER.info("AGENTS.md already up to date.")
        return 0

    agents_path.write_text(remote_content, encoding="utf-8")
    LOGGER.info("Updated AGENTS.md from central fragments.")
    stage_agents_file(repo_root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""
def configure_bootstrap_logger(name: str) -> logging.Logger:
    """Configure process-wide logger for installer runtime."""
    logfile_path = BOOTSTRAP_LOGFILE
    logfile_path.parent.mkdir(parents=True, exist_ok=True)
    root_logger = logging.getLogger()
    if not getattr(root_logger, "_agents_logging_configured", False):
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler = logging.FileHandler(logfile_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        root_logger.handlers.clear()
        root_logger.addHandler(file_handler)
        root_logger.addHandler(stream_handler)
        root_logger.setLevel(logging.INFO)
        setattr(root_logger, "_agents_logging_configured", True)
    return logging.getLogger(name)


LOGGER = configure_bootstrap_logger("install-agents")


def get_git_repo_root() -> Path:
    """Return Git repository root for the current working directory."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or "Not inside a Git repository."
        raise RuntimeError(message)
    return Path(result.stdout.strip())


def download_text(url: str) -> str:
    """Download text file from URL."""
    with urlopen(url, timeout=15) as response:
        return cast(str, response.read().decode("utf-8"))


def build_agents_content() -> str:
    """Build AGENTS.md by concatenating central fragments."""
    parts: list[str] = []
    for fragment in FRAGMENTS:
        url = f"{RAW_BASE_URL}/{fragment}"
        LOGGER.info("Downloading %s", url)
        parts.append(download_text(url).rstrip())
    return "\n\n".join(parts) + "\n"


def write_file(path: Path, content: str) -> bool:
    """Write file only when content differs. Return True if updated."""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def write_managed_files(repo_root: Path) -> dict[str, bool]:
    """Write generated files managed by this installer."""
    return {
        "AGENTS.md": write_file(repo_root / "AGENTS.md", build_agents_content()),
        "scripts/sync_agents.py": write_file(
            repo_root / SYNC_SCRIPT_RELATIVE_PATH, SYNC_SCRIPT_CONTENT
        ),
        "scripts/runtime_config.py": write_file(
            repo_root / RUNTIME_CONFIG_RELATIVE_PATH, RUNTIME_CONFIG_SCRIPT_CONTENT
        ),
        "scripts/logging_utils.py": write_file(
            repo_root / LOGGING_UTILS_RELATIVE_PATH, LOGGING_UTILS_SCRIPT_CONTENT
        ),
        "config.yaml": write_file(repo_root / CONFIG_RELATIVE_PATH, CONFIG_YAML_CONTENT),
    }


def log_update_status(path_label: str, updated: bool) -> None:
    """Log a consistent status line for managed files."""
    status = "Installed/updated" if updated else "already up to date"
    LOGGER.info("%s %s", status, path_label)


def make_executable(path: Path) -> None:
    """Set executable bit on POSIX systems."""
    if os.name == "nt":
        return
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def sync_hook_block() -> str:
    """Return managed pre-commit hook block."""
    return (
        f"{HOOK_BLOCK_START}\n"
        "if command -v python >/dev/null 2>&1; then\n"
        "  python scripts/sync_agents.py || true\n"
        "elif command -v python3 >/dev/null 2>&1; then\n"
        "  python3 scripts/sync_agents.py || true\n"
        "else\n"
        '  echo "[agents-sync] Warning: python/python3 not found, '
        'skipping AGENTS.md sync."\n'
        "fi\n"
        f"{HOOK_BLOCK_END}\n"
    )


def upsert_pre_commit_hook(repo_root: Path) -> str:
    """Insert or replace managed hook block in pre-commit hook."""
    hook_path = repo_root / HOOK_RELATIVE_PATH
    existing = hook_path.read_text(encoding="utf-8") if hook_path.exists() else ""
    block = sync_hook_block()

    if HOOK_BLOCK_START in existing and HOOK_BLOCK_END in existing:
        pattern = re.compile(
            re.escape(HOOK_BLOCK_START) + r".*?" + re.escape(HOOK_BLOCK_END) + r"\n?",
            re.DOTALL,
        )
        replacement = pattern.sub(block, existing, count=1)
        changed = replacement != existing
        content = replacement
        status = "updated" if changed else "already up to date"
    elif existing:
        content = existing.rstrip() + "\n\n" + block
        status = "appended"
    else:
        content = "#!/usr/bin/env sh\nset -e\n\n" + block
        status = "created"

    hook_path.parent.mkdir(parents=True, exist_ok=True)
    hook_path.write_text(content, encoding="utf-8")
    make_executable(hook_path)
    return status


def main() -> int:
    """Install AGENTS.md sync into current Git repository."""
    try:
        repo_root = get_git_repo_root()
    except RuntimeError as exc:
        LOGGER.error("Error: %s", exc)
        return 1

    try:
        managed_file_updates = write_managed_files(repo_root)
    except URLError as exc:
        LOGGER.error("Error: Could not download AGENTS fragments: %s", exc)
        return 1
    except Exception as exc:  # noqa: BLE001
        LOGGER.error("Error: Unexpected download error: %s", exc)
        return 1

    make_executable(repo_root / SYNC_SCRIPT_RELATIVE_PATH)
    make_executable(repo_root / RUNTIME_CONFIG_RELATIVE_PATH)
    make_executable(repo_root / LOGGING_UTILS_RELATIVE_PATH)
    hook_status = upsert_pre_commit_hook(repo_root)

    LOGGER.info("Repository: %s", repo_root)
    for path_label, updated in managed_file_updates.items():
        log_update_status(path_label, updated)
    LOGGER.info("pre-commit hook %s", hook_status)
    LOGGER.info("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
