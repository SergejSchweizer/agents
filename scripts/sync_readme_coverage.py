#!/usr/bin/env python3
"""Sync README coverage from coverage.xml and enforce minimum coverage."""

from __future__ import annotations

import argparse
import logging
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.logging_utils import configure_logger

COVERAGE_PATTERN = re.compile(r"(?m)^Test coverage:\s*\d+(?:\.\d+)?%$")
LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--coverage-file", default="coverage.xml", help="Path to coverage XML report"
    )
    parser.add_argument("--readme", default="README.md", help="Path to README file")
    parser.add_argument(
        "--min-coverage",
        type=float,
        default=90.0,
        help="Minimum required coverage percent",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Do not modify README; fail if coverage line is out of sync",
    )
    return parser.parse_args()


def read_coverage_percent(coverage_file: Path) -> float:
    if not coverage_file.exists():
        raise FileNotFoundError(f"Coverage file not found: {coverage_file}")

    root = ET.fromstring(coverage_file.read_text(encoding="utf-8"))
    line_rate = root.attrib.get("line-rate")
    if line_rate is None:
        raise ValueError("Could not find line-rate in coverage.xml")

    return round(float(line_rate) * 100, 2)


def sync_readme(readme_path: Path, coverage_percent: float, check_only: bool) -> bool:
    if not readme_path.exists():
        raise FileNotFoundError(f"README not found: {readme_path}")

    content = readme_path.read_text(encoding="utf-8")
    expected_line = f"Test coverage: {coverage_percent:.2f}%"

    match = COVERAGE_PATTERN.search(content)
    if match is None:
        raise ValueError(
            "README.md is missing a coverage line. "
            "Add a line like: 'Test coverage: 90.00%'"
        )

    current_line = match.group(0)
    if current_line == expected_line:
        LOGGER.info("README already in sync (%s).", expected_line)
        return False

    if check_only:
        LOGGER.error("README coverage line is out of sync.")
        LOGGER.error("Current:  %s", current_line)
        LOGGER.error("Expected: %s", expected_line)
        raise RuntimeError("README coverage line must be updated")

    updated = content[: match.start()] + expected_line + content[match.end() :]
    readme_path.write_text(updated, encoding="utf-8")
    LOGGER.info("Updated README coverage line to %s.", expected_line)
    return True


def main() -> int:
    configure_logger("coverage-sync")
    args = parse_args()

    coverage_file = Path(args.coverage_file)
    readme_path = Path(args.readme)

    try:
        coverage_percent = read_coverage_percent(coverage_file)
        LOGGER.info("Measured coverage: %.2f%%", coverage_percent)

        if coverage_percent < args.min_coverage:
            LOGGER.error(
                "Coverage %.2f%% is below minimum %.2f%%",
                coverage_percent,
                args.min_coverage,
            )
            return 1

        sync_readme(readme_path, coverage_percent, args.check_only)
    except Exception as exc:  # noqa: BLE001
        LOGGER.error("Error: %s", exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
