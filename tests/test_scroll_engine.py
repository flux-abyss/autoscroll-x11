"""Tests for ScrollEngine."""

from unittest.mock import MagicMock, call

from autoscroll_x11.config import POLL_INTERVAL_MS
from autoscroll_x11.core.scroll_engine import ScrollEngine
from autoscroll_x11.platform.x11 import BUTTON_SCROLL_DOWN, BUTTON_SCROLL_UP

_TICK_S = POLL_INTERVAL_MS / 1000.0


def _engine() -> tuple[ScrollEngine, MagicMock]:
    display = MagicMock()
    return ScrollEngine(display), display


def test_zero_velocity_sends_no_events() -> None:
    engine, display = _engine()
    engine.tick(0.0, 0.0)
    display.send_scroll_event.assert_not_called()


def test_positive_vy_sends_scroll_down() -> None:
    engine, display = _engine()
    # velocity high enough to produce at least one event per tick
    vy = 1.0 / _TICK_S + 1.0
    engine.tick(0.0, vy)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_DOWN)


def test_negative_vy_sends_scroll_up() -> None:
    engine, display = _engine()
    vy = -(1.0 / _TICK_S + 1.0)
    engine.tick(0.0, vy)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_UP)


def test_remainder_accumulates_across_ticks() -> None:
    # A small velocity that produces <1 line per tick should eventually fire.
    engine, display = _engine()
    # 0.5 lines per tick means every 2 ticks we get 1 event.
    vy = 0.5 / _TICK_S
    engine.tick(0.0, vy)
    engine.tick(0.0, vy)
    assert display.send_scroll_event.call_count >= 1


def test_flush_resets_remainder() -> None:
    engine, display = _engine()
    # Prime remainder without crossing a whole line.
    engine.tick(0.0, 0.4 / _TICK_S)
    engine.flush()
    # After flush, another partial tick should not add to old remainder.
    engine.tick(0.0, 0.4 / _TICK_S)
    display.send_scroll_event.assert_not_called()
