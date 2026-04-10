"""Anchor-point overlay: a small GTK popup window at the scroll anchor."""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)

_SIZE = 18


class AnchorOverlay:
    """Small undecorated GTK window shown at the anchor point.

    Uses a CSS-colored box with a cross drawn via two GTK labels.
    No cairo, no region APIs.
    """

    def __init__(self) -> None:
        self._window: object | None = None

    def show_at(self, x: int, y: int) -> None:
        """Position and display the overlay centred on (x, y)."""
        if self._window is None:
            self._window = self._build_window()

        half = _SIZE // 2
        self._window.move(x - half, y - half)
        self._window.show_all()
        log.debug("AnchorOverlay shown at (%d, %d)", x, y)

    def hide(self) -> None:
        """Hide the overlay."""
        if self._window is not None:
            self._window.hide()
        log.debug("AnchorOverlay hidden")

    def _build_window(self) -> object:
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
            b"  color: rgba(255, 255, 255, 0.9);"
            b"  font-size: 10px;"
            b"  font-weight: bold;"
            b"}"
        )
        win.get_style_context().add_provider(
            css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        label = Gtk.Label(label="+")
        win.add(label)

        return win
