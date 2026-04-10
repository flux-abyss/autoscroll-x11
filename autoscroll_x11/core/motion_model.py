"""Motion model: pointer displacement to scroll velocity."""

from __future__ import annotations

import logging
import math

from autoscroll_x11.config import DEAD_ZONE_PX

log = logging.getLogger(__name__)

# Pixels of deflection beyond the dead zone that produce _MAX_LINES_PER_TICK.
_FULL_SCALE_PX: int = 80

# Lines emitted per poll tick at full deflection.
_MAX_LINES_PER_TICK: float = 5.0


class MotionModel:
    """Converts pointer displacement from the anchor into scroll velocity.

    Returns velocity in lines-per-tick so that ScrollEngine can accumulate
    and emit whole wheel steps without a time-unit conversion.

    Only vertical velocity is produced. Horizontal is always 0.0.
    """

    def compute_velocity(self, dx: int, dy: int) -> tuple[float, float]:
        """Return (vx, vy) in lines-per-tick for the given displacement.

        dy > 0 means pointer is below anchor (scroll down, positive vy).
        dy < 0 means pointer is above anchor (scroll up, negative vy).
        Within DEAD_ZONE_PX both components are 0.0.
        """
        abs_dy = abs(dy)
        if abs_dy <= DEAD_ZONE_PX:
            return (0.0, 0.0)

        deflection = abs_dy - DEAD_ZONE_PX
        raw = (deflection / _FULL_SCALE_PX) * _MAX_LINES_PER_TICK
        vy = math.copysign(min(raw, _MAX_LINES_PER_TICK), dy)
        log.debug("MotionModel: dy=%d vy=%.3f lines/tick", dy, vy)
        return (0.0, vy)
