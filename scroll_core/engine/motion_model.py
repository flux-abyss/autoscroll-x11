"""Motion model: pointer displacement to scroll velocity."""

from __future__ import annotations

import logging
import math

from scroll_core.config import ACTIVATION_RADIUS_PX

log = logging.getLogger(__name__)

# Pixels of total displacement (from press point) that produce max velocity.
# At ACTIVATION_RADIUS_PX displacement, velocity = 0.
# At _FULL_SCALE_PX displacement, velocity = _MAX_LINES_PER_TICK.
_FULL_SCALE_PX: int = 120

# Lines emitted per poll tick at full deflection.
_MAX_LINES_PER_TICK: float = 5.0


class MotionModel:
    """Converts pointer displacement from the press point into scroll velocity.

    The activation radius acts as the zero-scroll center: below it velocity
    is 0.0; above it velocity scales linearly up to _MAX_LINES_PER_TICK.

    Only vertical velocity is produced. Horizontal is always 0.0.
    """

    def compute_velocity(self, dx: int, dy: int) -> tuple[float, float]:
        """Return (vx, vy) in lines-per-tick for the given displacement.

        dx, dy are relative to the original press point (the anchor).
        dy > 0 → scroll down; dy < 0 → scroll up.
        Total distance within ACTIVATION_RADIUS_PX → returns (0.0, 0.0).
        """
        distance = math.hypot(dx, dy)
        if distance <= ACTIVATION_RADIUS_PX:
            return (0.0, 0.0)

        # Scale vertically using only the y component of the overshoot.
        overshoot = distance - ACTIVATION_RADIUS_PX
        # Use dy/distance to project overshoot onto the vertical axis.
        vertical_overshoot = overshoot * (abs(dy) / distance)
        raw = (vertical_overshoot / _FULL_SCALE_PX) * _MAX_LINES_PER_TICK
        vy = math.copysign(min(raw, _MAX_LINES_PER_TICK), dy)
        log.debug("MotionModel: dy=%d dist=%.1f vy=%.3f", dy, distance, vy)
        return (0.0, vy)
