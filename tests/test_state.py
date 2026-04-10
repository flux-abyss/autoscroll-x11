"""Smoke tests for ScrollState and ScrollMode."""

from autoscroll_x11.core.state import ScrollMode, ScrollState


def test_import() -> None:
    assert ScrollMode is not None
    assert ScrollState is not None


def test_default_state_is_idle() -> None:
    state = ScrollState()
    assert state.mode == ScrollMode.IDLE


def test_reset_returns_to_idle() -> None:
    state = ScrollState()
    state.mode = ScrollMode.ACTIVE
    state.anchor_x = 400
    state.anchor_y = 300
    state.reset()
    assert state.mode == ScrollMode.IDLE
    assert state.anchor_x == 0
    assert state.anchor_y == 0


def test_scroll_mode_values_are_distinct() -> None:
    assert ScrollMode.IDLE != ScrollMode.ARMED
    assert ScrollMode.ARMED != ScrollMode.ACTIVE
    assert ScrollMode.IDLE != ScrollMode.ACTIVE
