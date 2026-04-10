"""Tests for MotionModel."""

from autoscroll_x11.config import DEAD_ZONE_PX, MAX_SCROLL_VELOCITY
from autoscroll_x11.core.motion_model import MotionModel


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
    # Negative dy = pointer is above anchor.
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
    assert vy <= MAX_SCROLL_VELOCITY


def test_horizontal_displacement_ignored() -> None:
    model = MotionModel()
    vx, _vy = model.compute_velocity(500, 0)
    assert vx == 0.0
