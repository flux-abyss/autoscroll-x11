"""Tests for ScrollEngine."""

from unittest.mock import MagicMock

from scroll_core.engine.scroll_engine import ScrollEngine
from scroll_core.platform.x11 import (
    BUTTON_SCROLL_DOWN,
    BUTTON_SCROLL_LEFT,
    BUTTON_SCROLL_RIGHT,
    BUTTON_SCROLL_UP,
)


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
    assert display.send_scroll_event.call_count == 1


def test_negative_vy_sends_scroll_up() -> None:
    engine, display = _engine()
    engine.tick(0.0, -1.5)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_UP)
    assert display.send_scroll_event.call_count == 1


def test_direction_down_for_positive_vy() -> None:
    engine, display = _engine()
    engine.tick(0.0, 2.0)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_DOWN)


def test_direction_up_for_negative_vy() -> None:
    engine, display = _engine()
    engine.tick(0.0, -2.0)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_UP)


def test_sub_one_vy_accumulates_across_ticks() -> None:
    engine, display = _engine()
    engine.tick(0.0, 0.4)
    display.send_scroll_event.assert_not_called()
    engine.tick(0.0, 0.4)
    display.send_scroll_event.assert_not_called()
    engine.tick(0.0, 0.4)
    # 0.4 * 3 = 1.2 → one event
    display.send_scroll_event.assert_called_once_with(BUTTON_SCROLL_DOWN)


def test_multiple_events_per_tick() -> None:
    engine, display = _engine()
    engine.tick(0.0, 3.0)
    assert display.send_scroll_event.call_count == 3
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_DOWN)


def test_remainder_carries_forward() -> None:
    engine, display = _engine()
    engine.tick(0.0, 1.7)
    assert display.send_scroll_event.call_count == 1
    display.reset_mock()
    # remainder ≈ 0.7; next tick: 0.7 + 1.7 = 2.4 → 2 events
    engine.tick(0.0, 1.7)
    assert display.send_scroll_event.call_count == 2


def test_flush_discards_remainder() -> None:
    engine, display = _engine()
    engine.tick(0.0, 0.6)
    display.send_scroll_event.assert_not_called()
    engine.flush()
    engine.tick(0.0, 0.6)
    display.send_scroll_event.assert_not_called()


def test_positive_vx_sends_scroll_right() -> None:
    engine, display = _engine()
    engine.tick(1.5, 0.0)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_RIGHT)
    assert display.send_scroll_event.call_count == 1


def test_negative_vx_sends_scroll_left() -> None:
    engine, display = _engine()
    engine.tick(-1.5, 0.0)
    display.send_scroll_event.assert_called_with(BUTTON_SCROLL_LEFT)
    assert display.send_scroll_event.call_count == 1


def test_sub_one_vx_accumulates_across_ticks() -> None:
    engine, display = _engine()
    engine.tick(0.4, 0.0)
    display.send_scroll_event.assert_not_called()
    engine.tick(0.4, 0.0)
    display.send_scroll_event.assert_not_called()
    engine.tick(0.4, 0.0)
    # 0.4 * 3 = 1.2 → one event
    display.send_scroll_event.assert_called_once_with(BUTTON_SCROLL_RIGHT)


def test_horizontal_remainder_independent_of_vertical() -> None:
    engine, display = _engine()
    # Accumulate 0.6 on x only; y remainder stays separate.
    engine.tick(0.6, 0.0)
    display.send_scroll_event.assert_not_called()
    engine.flush()
    engine.tick(0.6, 0.0)
    display.send_scroll_event.assert_not_called()


def test_both_axes_emit_independently() -> None:
    engine, display = _engine()
    engine.tick(2.0, 2.0)
    calls = [c.args[0] for c in display.send_scroll_event.call_args_list]
    assert BUTTON_SCROLL_RIGHT in calls
    assert BUTTON_SCROLL_DOWN in calls
