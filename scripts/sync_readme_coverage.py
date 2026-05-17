#!/usr/bin/env python3
"""Sync README coverage from coverage.xml and enforce minimum coverage."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET

COVERAGE_PATTERN = re.compile(r"(?m)^Test coverage:\s*\d+(?:\.\d+)?%$")


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
            "README.md is missing a coverage line. Add a line like: 'Test coverage: 90.00%'"
        )

    current_line = match.group(0)
    if current_line == expected_line:
        print(f"[coverage-sync] README already in sync ({expected_line}).")
        return False

    if check_only:
        print("[coverage-sync] README coverage line is out of sync.")
        print(f"[coverage-sync] Current:  {current_line}")
        print(f"[coverage-sync] Expected: {expected_line}")
        raise RuntimeError("README coverage line must be updated")

    updated = content[: match.start()] + expected_line + content[match.end() :]
    readme_path.write_text(updated, encoding="utf-8")
    print(f"[coverage-sync] Updated README coverage line to {expected_line}.")
    return True


def main() -> int:
    args = parse_args()

    coverage_file = Path(args.coverage_file)
    readme_path = Path(args.readme)

    try:
        coverage_percent = read_coverage_percent(coverage_file)
        print(f"[coverage-sync] Measured coverage: {coverage_percent:.2f}%")

        if coverage_percent < args.min_coverage:
            print(
                f"[coverage-sync] Coverage {coverage_percent:.2f}% is below minimum "
                f"{args.min_coverage:.2f}%"
            )
            return 1

        sync_readme(readme_path, coverage_percent, args.check_only)
    except Exception as exc:  # noqa: BLE001
        print(f"[coverage-sync] Error: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
