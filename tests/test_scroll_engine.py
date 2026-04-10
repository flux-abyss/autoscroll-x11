"""Tests for ScrollEngine."""

from unittest.mock import MagicMock

from scroll_core.engine.scroll_engine import ScrollEngine
from scroll_core.platform.x11 import BUTTON_SCROLL_DOWN, BUTTON_SCROLL_UP


def _engine() -> tuple[ScrollEngine, MagicMock]:
    display = MagicMock()
    return ScrollEngine(display), display


def test_zero_velocity_sends_no_events() -> None:
    engine, display = _engine()
    engine.tick(0.0, 0.0)
    display.send_scroll_event.assert_not_called()


def test_positive_vy_sends_scroll_down() -> None:
    engine, display = _engine()
    engine.tick(0.0, 1.5)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_DOWN)
    assert display.send_scroll_event.call_count >= 1


def test_negative_vy_sends_scroll_up() -> None:
    engine, display = _engine()
    engine.tick(0.0, -1.5)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_UP)
    assert display.send_scroll_event.call_count >= 1


def test_nonzero_vy_always_fires() -> None:
    # Any nonzero vy must produce at least one event per tick.
    for vy in (0.1, 0.3, 0.5, 0.9, -0.1, -0.5, -0.99):
        engine, display = _engine()
        engine.tick(0.0, vy)
        assert display.send_scroll_event.call_count >= 1, (
            f"Expected event for vy={vy}"
        )


def test_direction_down_for_positive_vy() -> None:
    engine, display = _engine()
    engine.tick(0.0, 0.3)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_DOWN)


def test_direction_up_for_negative_vy() -> None:
    engine, display = _engine()
    engine.tick(0.0, -0.3)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_UP)


def test_multiple_events_per_tick() -> None:
    engine, display = _engine()
    engine.tick(0.0, 3.0)
    assert display.send_scroll_event.call_count == 3
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_DOWN)


def test_flush_resets_remainder() -> None:
    engine, display = _engine()
    engine.tick(0.0, 2.5)
    engine.flush()
    display.reset_mock()
    engine.tick(0.0, 2.5)
    assert display.send_scroll_event.call_count >= 2
