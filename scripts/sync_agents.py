#!/usr/bin/env python3
"""Sync AGENTS.md from central AGENTS fragments."""

from __future__ import annotations

import logging
import subprocess
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from scripts.logging_utils import configure_logger

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
LOGGER = logging.getLogger(__name__)


def download_text(url: str) -> str:
    with urlopen(url, timeout=15) as response:
        return response.read().decode("utf-8")


def build_agents_content() -> str:
    parts = []
    for fragment in FRAGMENTS:
        url = f"{RAW_BASE_URL}/{fragment}"
        LOGGER.info("Downloading %s", url)
        parts.append(download_text(url).rstrip())
    return "\n\n".join(parts) + "\n"


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
    configure_logger("agents-sync")
    repo_root = Path.cwd()
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

    local_content = agents_path.read_text(encoding="utf-8") if agents_path.exists() else ""
    if local_content == remote_content:
        LOGGER.info("AGENTS.md already up to date.")
        return 0

    agents_path.write_text(remote_content, encoding="utf-8")
    LOGGER.info("Updated AGENTS.md from central fragments.")
    stage_agents_file(repo_root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
