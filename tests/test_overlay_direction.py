"""Tests for AnchorOverlay direction selection logic.

The overlay's _set_glyph call is intercepted via a mock so GTK is never
imported or instantiated.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from scroll_core.config import ACTIVATION_RADIUS_PX
from scroll_core.ui.overlay import (
    AnchorOverlay,
    _GLYPH_DOWN,
    _GLYPH_DOWN_LEFT,
    _GLYPH_DOWN_RIGHT,
    _GLYPH_LEFT,
    _GLYPH_NEUTRAL,
    _GLYPH_RIGHT,
    _GLYPH_UP,
    _GLYPH_UP_LEFT,
    _GLYPH_UP_RIGHT,
)

R = ACTIVATION_RADIUS_PX


def _overlay_with_label() -> tuple[AnchorOverlay, MagicMock]:
    """Return an AnchorOverlay whose label is a MagicMock (no GTK)."""
    overlay = AnchorOverlay.__new__(AnchorOverlay)
    overlay._window = MagicMock()
    overlay._label = MagicMock()
    return overlay, overlay._label


def _glyph(dx: int, dy: int) -> str:
    overlay, label = _overlay_with_label()
    overlay.update_direction(dx, dy)
    return label.set_text.call_args[0][0]


def test_center_shows_neutral() -> None:
    assert _glyph(0, 0) == _GLYPH_NEUTRAL


def test_within_radius_shows_neutral() -> None:
    assert _glyph(R - 1, R - 1) == _GLYPH_NEUTRAL


def test_pure_up() -> None:
    assert _glyph(0, -(R + 20)) == _GLYPH_UP


def test_pure_down() -> None:
    assert _glyph(0, R + 20) == _GLYPH_DOWN


def test_pure_left() -> None:
    assert _glyph(-(R + 20), 0) == _GLYPH_LEFT


def test_pure_right() -> None:
    assert _glyph(R + 20, 0) == _GLYPH_RIGHT


def test_diagonal_down_right() -> None:
    # Equal offsets → ratio 1.0 → diagonal band.
    off = R + 30
    assert _glyph(off, off) == _GLYPH_DOWN_RIGHT


def test_diagonal_down_left() -> None:
    off = R + 30
    assert _glyph(-off, off) == _GLYPH_DOWN_LEFT


def test_diagonal_up_right() -> None:
    off = R + 30
    assert _glyph(off, -off) == _GLYPH_UP_RIGHT


def test_diagonal_up_left() -> None:
    off = R + 30
    assert _glyph(-off, -off) == _GLYPH_UP_LEFT


def test_steep_vertical_falls_back_to_cardinal() -> None:
    # abs(dx)/abs(dy) = 0.1 → below DIAGONAL_RATIO_MIN → dominant axis (y).
    off = R + 30
    assert _glyph(off // 10, off) == _GLYPH_DOWN


def test_steep_horizontal_falls_back_to_cardinal() -> None:
    # abs(dx)/abs(dy) = 10 → above DIAGONAL_RATIO_MAX → dominant axis (x).
    off = R + 30
    assert _glyph(off, off // 10) == _GLYPH_RIGHT


def test_only_x_outside_radius_shows_cardinal() -> None:
    # y inside radius → not both outside → dominant-axis fallback.
    assert _glyph(R + 20, R - 1) == _GLYPH_RIGHT


def test_only_y_outside_radius_shows_cardinal() -> None:
    assert _glyph(R - 1, R + 20) == _GLYPH_DOWN
