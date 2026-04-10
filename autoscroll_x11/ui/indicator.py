"""Scroll-mode indicator stub.

Optional secondary widget showing the current scroll direction while
autoscroll is active (e.g. an arrow cursor replacement or HUD element).
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class ScrollIndicator:
    """Displays scroll direction feedback near the pointer.

    This is a stub. Visual design is deferred to the next phase.
    """

    def update(self, dx: int, dy: int) -> None:
        """Refresh the indicator for the given displacement from anchor.

        Args:
            dx: Horizontal displacement (pixels).
            dy: Vertical displacement (pixels).
        """
        log.debug("ScrollIndicator.update(%d, %d) — stub", dx, dy)

    def hide(self) -> None:
        """Hide the indicator."""
        log.debug("ScrollIndicator.hide() — stub")
