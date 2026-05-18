#!/usr/bin/env python3
"""Runtime configuration loading utilities."""

from __future__ import annotations

from pathlib import Path


def read_logfile_from_config(config_path: Path | None = None) -> Path:
    """Read the logfile path from config.yaml."""
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
        cleaned = value.strip().strip("'\"")
        if not cleaned:
            raise ValueError("config.yaml key 'logfile' must not be empty")
        return Path(cleaned)

    raise ValueError("config.yaml must define a top-level 'logfile' key")
