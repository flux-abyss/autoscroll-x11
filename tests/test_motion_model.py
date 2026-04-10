"""Tests for MotionModel."""

from autoscroll_x11.config import DEAD_ZONE_PX
from autoscroll_x11.core.motion_model import (
    MotionModel,
    _FULL_SCALE_PX,
    _MAX_LINES_PER_TICK,
)


def test_dead_zone_returns_zero() -> None:
    model = MotionModel()
    vx, vy = model.compute_velocity(0, 0)
    assert vx == 0.0
    assert vy == 0.0


def test_within_dead_zone_returns_zero() -> None:
    model = MotionModel()
    vx, vy = model.compute_velocity(0, DEAD_ZONE_PX)
    assert vx == 0.0
    assert vy == 0.0


def test_above_anchor_scrolls_up() -> None:
    model = MotionModel()
    _vx, vy = model.compute_velocity(0, -(DEAD_ZONE_PX + 1))
    assert vy < 0.0


def test_below_anchor_scrolls_down() -> None:
    model = MotionModel()
    _vx, vy = model.compute_velocity(0, DEAD_ZONE_PX + 1)
    assert vy > 0.0


def test_velocity_increases_with_distance() -> None:
    model = MotionModel()
    _vx, vy_near = model.compute_velocity(0, DEAD_ZONE_PX + 10)
    _vx, vy_far = model.compute_velocity(0, DEAD_ZONE_PX + 100)
    assert vy_far > vy_near


def test_velocity_capped_at_max() -> None:
    model = MotionModel()
    _vx, vy = model.compute_velocity(0, 10_000)
    assert vy <= _MAX_LINES_PER_TICK


def test_full_scale_produces_max_velocity() -> None:
    model = MotionModel()
    _vx, vy = model.compute_velocity(0, DEAD_ZONE_PX + _FULL_SCALE_PX)
    assert abs(vy - _MAX_LINES_PER_TICK) < 1e-9


def test_horizontal_displacement_ignored() -> None:
    model = MotionModel()
    vx, _vy = model.compute_velocity(500, 0)
    assert vx == 0.0


def test_velocity_usable_per_tick() -> None:
    # At 30px beyond dead zone, velocity should be nonzero.
    # Accumulator reaches 1.0 within a small number of ticks.
    model = MotionModel()
    _vx, vy = model.compute_velocity(0, DEAD_ZONE_PX + 30)
    assert vy > 0.0
    ticks_to_fire = 1.0 / vy
    # Should fire within 10 ticks (160ms at 16ms/tick).
    assert ticks_to_fire < 10
