"""Smoke tests for ScrollEngine."""

from autoscroll_x11.core.scroll_engine import ScrollEngine


def test_import() -> None:
    assert ScrollEngine is not None


def test_tick_does_not_raise() -> None:
    engine = ScrollEngine()
    engine.tick(0.0, 0.0)


def test_flush_does_not_raise() -> None:
    engine = ScrollEngine()
    engine.flush()
