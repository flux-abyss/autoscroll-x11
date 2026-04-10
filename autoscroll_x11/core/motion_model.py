"""Motion model: pointer displacement to scroll velocity."""

from __future__ import annotations

import math

from autoscroll_x11.config import DEAD_ZONE_PX, MAX_SCROLL_VELOCITY


class MotionModel:
    """Converts pointer displacement from the anchor into scroll velocity.

    Only vertical velocity is produced in this pass. Horizontal is zero.

    The curve is linear beyond the dead zone, capped at MAX_SCROLL_VELOCITY.
    The scaling factor is chosen so that a moderate deflection (~100 px beyond
    the dead zone) produces a comfortable mid-range speed.
    """

    # Pixels of deflection beyond dead zone that map to MAX_SCROLL_VELOCITY.
    _FULL_SCALE_PX: int = 200

    def compute_velocity(self, dx: int, dy: int) -> tuple[float, float]:
        """Return (vx, vy) scroll velocity for the given displacement.

        dx and dy are the pointer's distance from the anchor in pixels.
        Positive dy means the pointer is below the anchor (scroll down).

        Returns:
            (vx, vy) in lines per second. vx is always 0.0 in this pass.
        """
        abs_dy = abs(dy)
        if abs_dy <= DEAD_ZONE_PX:
            return (0.0, 0.0)

        deflection = abs_dy - DEAD_ZONE_PX
        raw = (deflection / self._FULL_SCALE_PX) * MAX_SCROLL_VELOCITY
        vy = math.copysign(min(raw, MAX_SCROLL_VELOCITY), dy)
        return (0.0, vy)
