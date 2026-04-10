"""Motion model: pointer displacement to scroll velocity."""

from __future__ import annotations

import logging
import math

from scroll_core.config import ACTIVATION_RADIUS_PX

log = logging.getLogger(__name__)

# Pixels of total displacement (from press point) that produce max velocity.
# At ACTIVATION_RADIUS_PX displacement velocity = 0;
# at _FULL_SCALE_PX displacement velocity = _MAX_LINES_PER_TICK.
_FULL_SCALE_PX: int = 120

# Lines emitted per poll tick at full deflection.
_MAX_LINES_PER_TICK: float = 5.0


class MotionModel:
    """Converts pointer displacement from the press point into scroll velocity.

    The activation radius acts as the zero-scroll center: within it both
    components are 0.0. Outside it, each axis is scaled independently using
    its own projected overshoot on the radial direction from center.
    """

    def compute_velocity(self, dx: int, dy: int) -> tuple[float, float]:
        """Return (vx, vy) in lines-per-tick for the given displacement.

        dx, dy are relative to the original press point.
        dx > 0 → scroll right; dx < 0 → scroll left.
        dy > 0 → scroll down;  dy < 0 → scroll up.
        Within ACTIVATION_RADIUS_PX of center returns (0.0, 0.0).
        """
        distance = math.hypot(dx, dy)
        if distance <= ACTIVATION_RADIUS_PX:
            return (0.0, 0.0)

        overshoot = distance - ACTIVATION_RADIUS_PX
        # Project overshoot onto each axis using the unit vector components.
        ratio = overshoot / distance
        raw_vx = ratio * abs(dx) / _FULL_SCALE_PX * _MAX_LINES_PER_TICK
        raw_vy = ratio * abs(dy) / _FULL_SCALE_PX * _MAX_LINES_PER_TICK

        vx = math.copysign(min(raw_vx, _MAX_LINES_PER_TICK), dx)
        vy = math.copysign(min(raw_vy, _MAX_LINES_PER_TICK), dy)

        log.debug(
            "MotionModel: dx=%d dy=%d dist=%.1f vx=%.3f vy=%.3f",
            dx, dy, distance, vx, vy,
        )
        return (vx, vy)
