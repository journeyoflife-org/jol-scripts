"""Integration test: verify every script supports --dry-run without side-effects."""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"

# Discover all script files
SCRIPT_FILES = sorted(SCRIPTS_DIR.rglob("*.py"))
SCRIPT_IDS = [str(p.relative_to(SCRIPTS_DIR)) for p in SCRIPT_FILES]


@pytest.mark.parametrize("script_path", SCRIPT_FILES, ids=SCRIPT_IDS)
def test_script_supports_dry_run(script_path: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Every script must accept --dry-run and exit 0 without performing side-effects."""
    from lib.jol_logger import JolLogger

    log_dir = tmp_path / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(JolLogger, "LOG_DIR", log_dir)

    # Add project root to sys.path for imports
    project_root = str(script_path.parents[2]) if "scripts" in str(script_path) else str(script_path.parents[1])
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Read the script and check it has a class
    source = script_path.read_text()
    if "class " not in source:
        pytest.skip(f"No class found in {script_path}")

    # Import the module
    spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]

    # Find the JolBaseScript subclass
    from lib.jol_base import JolBaseScript

    script_classes = [
        obj
        for name in dir(mod)
        if isinstance((obj := getattr(mod, name)), type) and issubclass(obj, JolBaseScript) and obj is not JolBaseScript
    ]
    assert len(script_classes) == 1, f"Expected exactly one JolBaseScript subclass in {script_path}"

    cls = script_classes[0]
    instance = cls()

    # Build parser and find required arguments
    parser = instance.build_parser()
    instance.add_arguments(parser)

    required_actions = []
    for action in parser._actions:
        if action.required and action.option_strings:
            required_actions.append((action.option_strings[0], "test-value"))

    argv = ["--dry-run"]
    for flag, value in required_actions:
        argv.extend([flag, value])

    args = parser.parse_args(argv)
    rc = instance.run_logic(args)
    # Exit codes: 0 = success, 3 = dry-run-only (both valid for --dry-run mode)
    assert rc in (0, 3), f"{script_path.name} --dry-run exited with code {rc}"
