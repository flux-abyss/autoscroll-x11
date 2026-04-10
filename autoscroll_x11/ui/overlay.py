"""Anchor-point overlay stub.

A small, click-through GTK window drawn at the anchor position while
autoscroll is active. Will render the directional arrow graphic.
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class AnchorOverlay:
    """Transparent overlay that marks the autoscroll anchor point.

    This is a stub. Cairo drawing and input-shape carve-out are deferred.
    """

    def show_at(self, x: int, y: int) -> None:
        """Position and display the overlay at root-window coordinates (x, y)."""
        log.debug("AnchorOverlay.show_at(%d, %d) — stub", x, y)

    def update_direction(self, dx: int, dy: int) -> None:
        """Redraw the directional arrow for the given displacement vector."""
        log.debug("AnchorOverlay.update_direction(%d, %d) — stub", dx, dy)

    def hide(self) -> None:
        """Hide the overlay without destroying the window."""
        log.debug("AnchorOverlay.hide() — stub")
