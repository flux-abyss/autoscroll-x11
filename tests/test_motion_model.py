"""Smoke tests for MotionModel."""

from autoscroll_x11.core.motion_model import MotionModel


def test_import() -> None:
    assert MotionModel is not None


def test_stub_returns_zero_velocity() -> None:
    model = MotionModel()
    vx, vy = model.compute_velocity(0, 0)
    assert vx == 0.0
    assert vy == 0.0


def test_stub_accepts_nonzero_displacement() -> None:
    model = MotionModel()
    # Stub always returns zero; verify it does not raise.
    result = model.compute_velocity(100, -50)
    assert len(result) == 2
