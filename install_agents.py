#!/usr/bin/env python3
"""Install and maintain AGENTS.md in the current Git repository."""

from __future__ import annotations

import os
import re
import stat
import subprocess
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

RAW_BASE_URL = "https://raw.githubusercontent.com/SergejSchweizer/agents/main"
FRAGMENTS = [
    "fragments/00_purpose.md",
    "fragments/10_core_rules.md",
    "fragments/20_architecture.md",
    "fragments/30_code_review.md",
    "fragments/40_testing.md",
    "fragments/50_security_and_end_goal.md",
]
SYNC_SCRIPT_RELATIVE_PATH = Path("scripts") / "sync_agents.py"
HOOK_RELATIVE_PATH = Path(".git") / "hooks" / "pre-commit"
HOOK_BLOCK_START = "# >>> agents-sync (managed) >>>"
HOOK_BLOCK_END = "# <<< agents-sync (managed) <<<"

SYNC_SCRIPT_CONTENT = f"""#!/usr/bin/env python3
\"\"\"Sync AGENTS.md from central AGENTS fragments.\"\"\"

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

RAW_BASE_URL = "{RAW_BASE_URL}"
FRAGMENTS = {FRAGMENTS!r}


def download_text(url: str) -> str:
    with urlopen(url, timeout=15) as response:
        return response.read().decode("utf-8")


def build_agents_content() -> str:
    parts = []
    for fragment in FRAGMENTS:
        url = f"{{RAW_BASE_URL}}/{{fragment}}"
        print(f"[agents-sync] Downloading {{url}}")
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
        print(f"[agents-sync] Warning: Could not stage AGENTS.md: {{message}}")
    else:
        print("[agents-sync] Staged updated AGENTS.md")


def main() -> int:
    repo_root = Path.cwd()
    agents_path = repo_root / "AGENTS.md"

    try:
        remote_content = build_agents_content()
    except URLError as exc:
        print(f"[agents-sync] Warning: Could not download AGENTS fragments: {{exc}}")
        print("[agents-sync] Continuing without updates.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[agents-sync] Warning: Unexpected download error: {{exc}}")
        print("[agents-sync] Continuing without updates.")
        return 0

    local_content = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    if local_content == remote_content:
        print("[agents-sync] AGENTS.md already up to date.")
        return 0

    agents_path.write_text(remote_content, encoding="utf-8")
    print("[agents-sync] Updated AGENTS.md from central fragments.")
    stage_agents_file(repo_root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""


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
        return response.read().decode("utf-8")


def build_agents_content() -> str:
    """Build AGENTS.md by concatenating central fragments."""
    parts: list[str] = []
    for fragment in FRAGMENTS:
        url = f"{RAW_BASE_URL}/{fragment}"
        print(f"[install-agents] Downloading {url}")
        parts.append(download_text(url).rstrip())
    return "\n\n".join(parts) + "\n"


def write_file(path: Path, content: str) -> bool:
    """Write file only when content differs. Return True if updated."""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


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
        '  echo "[agents-sync] Warning: python/python3 not found, skipping AGENTS.md sync."\n'
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
        print(f"[install-agents] Error: {exc}")
        return 1

    try:
        agents_content = build_agents_content()
    except URLError as exc:
        print(f"[install-agents] Error: Could not download AGENTS fragments: {exc}")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"[install-agents] Error: Unexpected download error: {exc}")
        return 1

    agents_updated = write_file(repo_root / "AGENTS.md", agents_content)
    sync_updated = write_file(repo_root / SYNC_SCRIPT_RELATIVE_PATH, SYNC_SCRIPT_CONTENT)
    make_executable(repo_root / SYNC_SCRIPT_RELATIVE_PATH)
    hook_status = upsert_pre_commit_hook(repo_root)

    print(f"[install-agents] Repository: {repo_root}")
    print(
        "[install-agents] "
        + ("Installed/updated AGENTS.md" if agents_updated else "AGENTS.md already up to date")
    )
    print(
        "[install-agents] "
        + (
            "Installed/updated scripts/sync_agents.py"
            if sync_updated
            else "scripts/sync_agents.py already up to date"
        )
    )
    print(f"[install-agents] pre-commit hook {hook_status}")
    print("[install-agents] Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
