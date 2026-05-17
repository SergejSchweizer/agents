from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

import scripts.sync_readme_coverage as coverage_sync
from scripts.sync_readme_coverage import main, read_coverage_percent, sync_readme


def write_coverage_xml(path: Path, line_rate: str) -> None:
    path.write_text(f'<coverage line-rate="{line_rate}"></coverage>', encoding="utf-8")


def test_install_agents_module_loads() -> None:
    spec = importlib.util.spec_from_file_location("install_agents", "install_agents.py")
    assert spec is not None
    assert spec.loader is not None


def test_read_coverage_percent_parses_value(tmp_path: Path) -> None:
    coverage_file = tmp_path / "coverage.xml"
    write_coverage_xml(coverage_file, "0.9234")
    assert read_coverage_percent(coverage_file) == 92.34


def test_read_coverage_percent_raises_when_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        read_coverage_percent(tmp_path / "missing.xml")


def test_read_coverage_percent_raises_when_line_rate_missing(tmp_path: Path) -> None:
    coverage_file = tmp_path / "coverage.xml"
    coverage_file.write_text("<coverage></coverage>", encoding="utf-8")

    with pytest.raises(ValueError, match="line-rate"):
        read_coverage_percent(coverage_file)


def test_sync_readme_updates_coverage_line(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Title\nTest coverage: 90.00%\n", encoding="utf-8")

    changed = sync_readme(readme, 95.55, check_only=False)

    assert changed is True
    assert "Test coverage: 95.55%" in readme.read_text(encoding="utf-8")


def test_sync_readme_noop_when_already_in_sync(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Title\nTest coverage: 90.00%\n", encoding="utf-8")

    changed = sync_readme(readme, 90.0, check_only=False)

    assert changed is False


def test_sync_readme_check_only_raises_when_out_of_sync(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Title\nTest coverage: 90.00%\n", encoding="utf-8")

    with pytest.raises(RuntimeError, match="must be updated"):
        sync_readme(readme, 91.00, check_only=True)


def test_sync_readme_raises_when_line_missing(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("Title\nNo coverage line\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing a coverage line"):
        sync_readme(readme, 91.00, check_only=False)


def test_main_returns_one_when_coverage_below_threshold(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    coverage_file = tmp_path / "coverage.xml"
    readme = tmp_path / "README.md"
    write_coverage_xml(coverage_file, "0.40")
    readme.write_text("Title\nTest coverage: 90.00%\n", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "sync_readme_coverage.py",
            "--coverage-file",
            str(coverage_file),
            "--readme",
            str(readme),
            "--min-coverage",
            "90",
        ],
    )

    assert main() == 1


def test_main_updates_readme_on_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    coverage_file = tmp_path / "coverage.xml"
    readme = tmp_path / "README.md"
    write_coverage_xml(coverage_file, "0.98")
    readme.write_text("Title\nTest coverage: 90.00%\n", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "sync_readme_coverage.py",
            "--coverage-file",
            str(coverage_file),
            "--readme",
            str(readme),
            "--min-coverage",
            "90",
        ],
    )

    assert main() == 0
    assert "Test coverage: 98.00%" in readme.read_text(encoding="utf-8")


def test_main_returns_one_for_check_only_mismatch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    coverage_file = tmp_path / "coverage.xml"
    readme = tmp_path / "README.md"
    write_coverage_xml(coverage_file, "0.98")
    readme.write_text("Title\nTest coverage: 90.00%\n", encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        [
            "sync_readme_coverage.py",
            "--coverage-file",
            str(coverage_file),
            "--readme",
            str(readme),
            "--min-coverage",
            "90",
            "--check-only",
        ],
    )

    assert main() == 1
