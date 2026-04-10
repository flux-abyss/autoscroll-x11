"""Scroll engine: accumulates lines-per-tick and fires XTest scroll events."""

from __future__ import annotations

import logging

from scroll_core.platform.x11 import (
    BUTTON_SCROLL_DOWN,
    BUTTON_SCROLL_LEFT,
    BUTTON_SCROLL_RIGHT,
    BUTTON_SCROLL_UP,
    X11Display,
)

log = logging.getLogger(__name__)


class ScrollEngine:
    """Converts lines-per-tick velocity into XTest button events.

    Sub-whole-line remainders accumulate across ticks for smooth
    low-speed scrolling on both axes independently.

    Positive vx = scroll right (button 7). Negative vx = scroll left (6).
    Positive vy = scroll down  (button 5). Negative vy = scroll up   (4).
    """

    def __init__(self, display: X11Display) -> None:
        self._display = display
        self._rem_x: float = 0.0
        self._rem_y: float = 0.0

    def tick(self, vx: float, vy: float) -> None:
        """Accumulate vx/vy and emit scroll button events for whole steps."""
        self._emit_axis(vx, self._rem_x, BUTTON_SCROLL_RIGHT, BUTTON_SCROLL_LEFT)
        self._emit_axis(vy, self._rem_y, BUTTON_SCROLL_DOWN, BUTTON_SCROLL_UP)

    def _emit_axis(
        self,
        v: float,
        remainder: float,
        btn_pos: int,
        btn_neg: int,
    ) -> None:
        if v == 0.0:
            # Remainder decays only when velocity is nonzero on this axis.
            return
        accumulated = v + remainder
        steps = int(accumulated)
        new_remainder = accumulated - steps

        # Update the instance remainder for this axis.
        if btn_pos == BUTTON_SCROLL_RIGHT:
            self._rem_x = new_remainder
        else:
            self._rem_y = new_remainder

        log.debug(
            "ScrollEngine: v=%.3f acc=%.3f steps=%d rem=%.3f btn+=%d",
            v, accumulated, steps, new_remainder, btn_pos,
        )

        if steps == 0:
            return

        button = btn_pos if steps > 0 else btn_neg
        for _ in range(abs(steps)):
            self._display.send_scroll_event(button)

    def flush(self) -> None:
        """Discard accumulated remainders on both axes."""
        self._rem_x = 0.0
        self._rem_y = 0.0
        log.debug("ScrollEngine: flushed")
