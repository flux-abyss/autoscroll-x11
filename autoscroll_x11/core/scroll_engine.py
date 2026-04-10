"""Scroll engine: accumulates velocity and fires XTest scroll events."""

from __future__ import annotations

import logging

from autoscroll_x11.config import POLL_INTERVAL_MS
from autoscroll_x11.platform.x11 import (
    BUTTON_SCROLL_DOWN,
    BUTTON_SCROLL_UP,
    X11Display,
)

log = logging.getLogger(__name__)

# Seconds per poll tick.
_TICK_S = POLL_INTERVAL_MS / 1000.0


class ScrollEngine:
    """Converts velocity (lines/sec) into XTest button events each tick.

    Sub-pixel remainders are accumulated so slow speeds still produce
    smooth scrolling over multiple ticks.
    """

    def __init__(self, display: X11Display) -> None:
        self._display = display
        self._remainder: float = 0.0

    def tick(self, vx: float, vy: float) -> None:
        """Fire scroll events for one poll interval.

        vx is ignored (horizontal not implemented yet).
        Positive vy = scroll down; negative vy = scroll up.
        """
        lines = vy * _TICK_S + self._remainder
        whole = int(lines)
        self._remainder = lines - whole

        if whole == 0:
            return

        button = BUTTON_SCROLL_DOWN if whole > 0 else BUTTON_SCROLL_UP
        count = abs(whole)
        for _ in range(count):
            self._display.send_scroll_event(button)
        log.debug("ScrollEngine: sent %d x button%d", count, button)

    def flush(self) -> None:
        """Discard accumulated remainder."""
        self._remainder = 0.0
