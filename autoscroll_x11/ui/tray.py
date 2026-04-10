"""System tray icon using Gtk.StatusIcon."""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class TrayIcon:
    """System-tray icon backed by Gtk.StatusIcon.

    Right-click shows the context menu.
    Left-click (activate signal) also shows the menu safely.
    """

    def __init__(self) -> None:
        self._enabled: bool = True
        self._icon: object | None = None

    def show(self) -> None:
        """Create and display the tray icon."""
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

        icon = Gtk.StatusIcon()
        icon.set_from_icon_name("autoscroll-x11")
        icon.set_tooltip_text("Autoscroll X11")
        icon.set_visible(True)

        icon.connect("activate", self._on_activate)
        icon.connect("popup-menu", self._on_popup_menu)

        self._icon = icon
        log.debug("TrayIcon shown")

    def destroy(self) -> None:
        """Remove the tray icon."""
        if self._icon is not None:
            from gi.repository import Gtk
            if isinstance(self._icon, Gtk.StatusIcon):
                self._icon.set_visible(False)
            self._icon = None
        log.debug("TrayIcon destroyed")

    def _on_activate(self, _icon: object) -> None:
        # Left-click: open menu at pointer position.
        self._popup_at_pointer()

    def _on_popup_menu(
        self, _icon: object, button: int, time: int
    ) -> None:
        # Right-click: open menu with button/time from the event.
        self._popup_with(button=button, time=time)

    def _popup_at_pointer(self) -> None:
        menu = self._build_menu()
        menu.popup_at_pointer(None)

    def _popup_with(self, button: int, time: int) -> None:
        from gi.repository import Gtk
        menu = self._build_menu()
        menu.popup(
            None, None,
            Gtk.StatusIcon.position_menu,
            self._icon,
            button, time,
        )

    def _build_menu(self) -> object:
        from gi.repository import Gtk

        menu = Gtk.Menu()

        item_enabled = Gtk.CheckMenuItem(label="Enabled")
        item_enabled.set_active(self._enabled)
        item_enabled.connect("toggled", self._on_toggle_enabled)
        menu.append(item_enabled)

        menu.append(Gtk.SeparatorMenuItem())

        item_prefs = Gtk.MenuItem(label="Preferences")
        item_prefs.connect("activate", self._on_preferences)
        menu.append(item_prefs)

        menu.append(Gtk.SeparatorMenuItem())

        item_quit = Gtk.MenuItem(label="Quit")
        item_quit.connect("activate", self._on_quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def _on_toggle_enabled(self, item: object) -> None:
        from gi.repository import Gtk
        if isinstance(item, Gtk.CheckMenuItem):
            self._enabled = item.get_active()
        log.debug("autoscroll enabled: %s", self._enabled)

    def _on_preferences(self, _item: object) -> None:
        log.debug("Preferences: not yet implemented")

    def _on_quit(self, _item: object) -> None:
        from gi.repository import Gtk
        self.destroy()
        Gtk.main_quit()
