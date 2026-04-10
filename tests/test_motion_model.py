"""Tests for MotionModel."""

import math

from scroll_core.config import ACTIVATION_RADIUS_PX
from scroll_core.engine.motion_model import (
    MotionModel,
    _FULL_SCALE_PX,
    _MAX_LINES_PER_TICK,
)


def test_inside_activation_radius_returns_zero() -> None:
    model = MotionModel()
    vx, vy = model.compute_velocity(0, 0)
    assert vx == 0.0
    assert vy == 0.0


def test_at_activation_boundary_returns_zero() -> None:
    # At exactly ACTIVATION_RADIUS_PX distance, still no scroll.
    model = MotionModel()
    vx, vy = model.compute_velocity(0, ACTIVATION_RADIUS_PX)
    assert vx == 0.0
    assert vy == 0.0


def test_just_outside_activation_produces_nonzero() -> None:
    model = MotionModel()
    _vx, vy = model.compute_velocity(0, ACTIVATION_RADIUS_PX + 1)
    assert vy > 0.0


def test_above_center_scrolls_up() -> None:
    model = MotionModel()
    _vx, vy = model.compute_velocity(0, -(ACTIVATION_RADIUS_PX + 1))
    assert vy < 0.0


def test_below_center_scrolls_down() -> None:
    model = MotionModel()
    _vx, vy = model.compute_velocity(0, ACTIVATION_RADIUS_PX + 1)
    assert vy > 0.0


def test_velocity_increases_with_distance() -> None:
    model = MotionModel()
    _vx, vy_near = model.compute_velocity(0, ACTIVATION_RADIUS_PX + 10)
    _vx, vy_far = model.compute_velocity(0, ACTIVATION_RADIUS_PX + 80)
    assert vy_far > vy_near


def test_velocity_capped_at_max() -> None:
    model = MotionModel()
    _vx, vy = model.compute_velocity(0, 10_000)
    assert vy <= _MAX_LINES_PER_TICK


def test_full_scale_produces_max_velocity() -> None:
    # At ACTIVATION_RADIUS_PX + _FULL_SCALE_PX pure vertical, overshoot
    # equals _FULL_SCALE_PX and dy/distance == 1.0, so vy == _MAX_LINES_PER_TICK.
    model = MotionModel()
    dy = ACTIVATION_RADIUS_PX + _FULL_SCALE_PX
    _vx, vy = model.compute_velocity(0, dy)
    assert abs(vy - _MAX_LINES_PER_TICK) < 1e-9


def test_horizontal_only_displacement_returns_zero_vy() -> None:
    # Pure horizontal movement produces no vertical scroll.
    model = MotionModel()
    _vx, vy = model.compute_velocity(ACTIVATION_RADIUS_PX + 50, 0)
    assert vy == 0.0


def test_diagonal_velocity_less_than_vertical_at_same_distance() -> None:
    # At the same total distance, 45-degree diagonal produces lower vy
    # than pure vertical because only the vertical component is used.
    dist = ACTIVATION_RADIUS_PX + 30
    dy_pure = dist
    dy_diag = int(dist / math.sqrt(2))
    dx_diag = dy_diag
    model = MotionModel()
    _vx, vy_pure = model.compute_velocity(0, dy_pure)
    _vx, vy_diag = model.compute_velocity(dx_diag, dy_diag)
    assert vy_pure > vy_diag > 0.0


def test_right_of_center_scrolls_right() -> None:
    model = MotionModel()
    vx, _vy = model.compute_velocity(ACTIVATION_RADIUS_PX + 1, 0)
    assert vx > 0.0


def test_left_of_center_scrolls_left() -> None:
    model = MotionModel()
    vx, _vy = model.compute_velocity(-(ACTIVATION_RADIUS_PX + 1), 0)
    assert vx < 0.0


def test_horizontal_only_displacement_returns_zero_vy_and_nonzero_vx() -> None:
    model = MotionModel()
    vx, vy = model.compute_velocity(ACTIVATION_RADIUS_PX + 50, 0)
    assert vy == 0.0
    assert vx > 0.0


def test_horizontal_velocity_capped_at_max() -> None:
    model = MotionModel()
    vx, _vy = model.compute_velocity(10_000, 0)
    assert vx <= _MAX_LINES_PER_TICK


def test_diagonal_produces_nonzero_vx_and_vy() -> None:
    # A 45-degree displacement well outside the activation radius should
    # yield nonzero velocity on both axes simultaneously.
    offset = ACTIVATION_RADIUS_PX + 40
    model = MotionModel()
    vx, vy = model.compute_velocity(offset, offset)
    assert vx > 0.0
    assert vy > 0.0


def test_diagonal_axes_symmetric() -> None:
    # Equal dx and dy should produce equal magnitude velocities on both axes.
    offset = ACTIVATION_RADIUS_PX + 60
    model = MotionModel()
    vx, vy = model.compute_velocity(offset, offset)
    assert abs(vx - vy) < 1e-9

