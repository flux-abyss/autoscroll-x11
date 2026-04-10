"""Smoke tests for CLI argument parsing."""

import subprocess
import sys


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "scroll_core", *args],
        capture_output=True,
        text=True,
    )


def test_version_exits_zero() -> None:
    result = _run("--version")
    assert result.returncode == 0


def test_version_output() -> None:
    from scroll_core import __version__
    result = _run("--version")
    assert __version__ in result.stdout


def test_no_args_exits_nonzero() -> None:
    result = _run()
    assert result.returncode != 0


def test_no_args_mentions_tray() -> None:
    result = _run()
    assert "--tray" in result.stderr
