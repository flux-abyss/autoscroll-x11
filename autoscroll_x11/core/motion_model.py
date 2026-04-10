"""Motion model stub.

Converts a pointer offset from the anchor point into a (vx, vy) velocity
vector, applying dead-zone clamping and a configurable acceleration curve.
"""

from __future__ import annotations

import logging

from autoscroll_x11.config import DEAD_ZONE_PX, MAX_SCROLL_VELOCITY

log = logging.getLogger(__name__)


class MotionModel:
    """Maps pointer displacement to scroll velocity.

    This is a stub. The acceleration curve is not yet implemented.
    """

    def compute_velocity(self, dx: int, dy: int) -> tuple[float, float]:
        """Return (vx, vy) scroll velocity for the given pointer displacement.

        Displacement within ``DEAD_ZONE_PX`` returns (0.0, 0.0).
        Values are clamped to ±``MAX_SCROLL_VELOCITY``.

        Args:
            dx: Horizontal displacement from anchor (pixels).
            dy: Vertical displacement from anchor (pixels).

        Returns:
            A (vx, vy) tuple in lines-per-second.
        """
        log.debug("MotionModel.compute_velocity(%d, %d) — stub", dx, dy)
        return (0.0, 0.0)
