"""Scroll engine stub.

Translates velocity vectors from ``MotionModel`` into X11 synthetic scroll
events (XTest / XSendEvent) at a fixed polling rate.
"""

from __future__ import annotations

import logging

from autoscroll_x11.config import POLL_INTERVAL_MS

log = logging.getLogger(__name__)


class ScrollEngine:
    """Fires synthetic scroll events at ``POLL_INTERVAL_MS`` intervals.

    This is a stub. XTest event injection is deferred to the next phase.
    """

    def tick(self, vx: float, vy: float) -> None:
        """Inject scroll events proportional to *vx* and *vy*.

        Called once per ``POLL_INTERVAL_MS`` while autoscroll is active.

        Args:
            vx: Horizontal velocity (lines/second).
            vy: Vertical velocity (lines/second).
        """
        log.debug("ScrollEngine.tick(vx=%.2f, vy=%.2f) — stub", vx, vy)

    def flush(self) -> None:
        """Discard any accumulated sub-pixel remainder and reset state."""
        log.debug("ScrollEngine.flush() — stub")
