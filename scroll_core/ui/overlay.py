"""Anchor-point overlay: a small GTK popup window at the scroll anchor."""

from __future__ import annotations

import logging

from scroll_core.config import (
    ACTIVATION_RADIUS_PX,
    DIAGONAL_RATIO_MAX,
    DIAGONAL_RATIO_MIN,
)

log = logging.getLogger(__name__)

_SIZE = 24

# Glyphs shown depending on displacement from anchor.
_GLYPH_NEUTRAL = "+"
_GLYPH_UP = "↑"
_GLYPH_DOWN = "↓"
_GLYPH_LEFT = "←"
_GLYPH_RIGHT = "→"
_GLYPH_UP_LEFT = "↖"
_GLYPH_UP_RIGHT = "↗"
_GLYPH_DOWN_RIGHT = "↘"
_GLYPH_DOWN_LEFT = "↙"


class AnchorOverlay:
    """Small undecorated GTK window shown at the anchor point.

    Displays a directional glyph updated live while autoscroll is active.
    No cairo, no region APIs.
    """

    def __init__(self) -> None:
        self._window: object | None = None
        self._label: object | None = None

    def show_at(self, x: int, y: int) -> None:
        """Position and display the overlay centred on (x, y)."""
        if self._window is None:
            self._window, self._label = self._build_window()

        self._set_glyph(_GLYPH_NEUTRAL)
        half = _SIZE // 2
        self._window.move(x - half, y - half)
        self._window.show_all()
        log.debug("AnchorOverlay shown at (%d, %d)", x, y)

    def update_direction(self, dx: int, dy: int) -> None:
        """Update the displayed glyph based on displacement (dx, dy).

        Near center (within ACTIVATION_RADIUS_PX on both axes): +
        Both axes outside radius and ratio in diagonal band: ↖ ↗ ↘ ↙
        Otherwise dominant axis: ← → ↑ ↓
        """
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        x_outside = abs_dx > ACTIVATION_RADIUS_PX
        y_outside = abs_dy > ACTIVATION_RADIUS_PX

        if not x_outside and not y_outside:
            self._set_glyph(_GLYPH_NEUTRAL)
            return

        if x_outside and y_outside:
            ratio = abs_dx / abs_dy
            if DIAGONAL_RATIO_MIN <= ratio <= DIAGONAL_RATIO_MAX:
                if dx < 0 and dy < 0:
                    self._set_glyph(_GLYPH_UP_LEFT)
                elif dx > 0 and dy < 0:
                    self._set_glyph(_GLYPH_UP_RIGHT)
                elif dx > 0 and dy > 0:
                    self._set_glyph(_GLYPH_DOWN_RIGHT)
                else:
                    self._set_glyph(_GLYPH_DOWN_LEFT)
                return

        # Dominant-axis fallback.
        if abs_dx >= abs_dy:
            self._set_glyph(_GLYPH_RIGHT if dx > 0 else _GLYPH_LEFT)
        else:
            self._set_glyph(_GLYPH_DOWN if dy > 0 else _GLYPH_UP)

    def hide(self) -> None:
        """Hide the overlay."""
        if self._window is not None:
            self._window.hide()
        log.debug("AnchorOverlay hidden")

    def _set_glyph(self, glyph: str) -> None:
        if self._label is not None:
            self._label.set_text(glyph)

    def _build_window(self) -> tuple[object, object]:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

        win = Gtk.Window(type=Gtk.WindowType.POPUP)
        win.set_default_size(_SIZE, _SIZE)
        win.set_decorated(False)
        win.set_keep_above(True)
        win.set_skip_taskbar_hint(True)
        win.set_skip_pager_hint(True)
        win.set_accept_focus(False)

        css = Gtk.CssProvider()
        css.load_from_data(
            b"window {"
            b"  background-color: rgba(40, 40, 40, 0.85);"
            b"  border: 1px solid rgba(255, 255, 255, 0.7);"
            b"  border-radius: 2px;"
            b"}"
            b"label {"
            b"  color: rgba(255, 255, 255, 0.95);"
            b"  font-size: 12px;"
            b"  font-weight: bold;"
            b"}"
        )
        win.get_style_context().add_provider(
            css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        label = Gtk.Label(label=_GLYPH_NEUTRAL)
        win.add(label)

        return win, label
