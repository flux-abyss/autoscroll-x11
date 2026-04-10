"""Scroll engine: accumulates lines-per-tick and fires XTest scroll events."""

from __future__ import annotations

import logging
import math

from scroll_core.platform.x11 import (
    BUTTON_SCROLL_DOWN,
    BUTTON_SCROLL_UP,
    X11Display,
)

log = logging.getLogger(__name__)


class ScrollEngine:
    """Converts lines-per-tick velocity into XTest button events.

    MotionModel returns velocity already scaled to lines-per-tick so no
    time conversion is needed here.  Sub-whole-line remainders are
    accumulated across ticks for smooth low-speed scrolling.

    Positive vy = scroll down (button 5).
    Negative vy = scroll up (button 4).
    """

    def __init__(self, display: X11Display) -> None:
        self._display = display
        self._remainder: float = 0.0

    def tick(self, vx: float, vy: float) -> None:
        """Accumulate *vy* and emit scroll button events for whole steps.

        Guarantees at least one event per tick when vy is nonzero,
        so that light but intentional motion always produces visible scroll.
        vx is accepted for forward-compatibility but ignored.
        """
        if vy == 0.0:
            return

        accumulated = vy + self._remainder
        steps = int(accumulated)

        # Guarantee at least one step per tick when vy is nonzero.
        if steps == 0:
            steps = math.copysign(1, vy)
            steps = int(steps)

        self._remainder = accumulated - steps

        log.debug(
            "ScrollEngine: vy=%.3f accumulated=%.3f steps=%d rem=%.3f",
            vy, accumulated, steps, self._remainder,
        )

        button = BUTTON_SCROLL_DOWN if steps > 0 else BUTTON_SCROLL_UP
        count = abs(steps)
        for _ in range(count):
            self._display.send_scroll_event(button)

    def flush(self) -> None:
        """Discard accumulated remainder."""
        self._remainder = 0.0
        log.debug("ScrollEngine: flushed")
