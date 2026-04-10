"""System tray icon stub.

Uses AppIndicator3 (libayatana-appindicator3) when available, falling back to
Gtk.StatusIcon for environments that lack the indicator stack.
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class TrayIcon:
    """Manages the system-tray presence of autoscroll-x11.

    This is a stub. Indicator initialisation is deferred to the next phase.
    """

    def show(self) -> None:
        """Add the tray icon to the notification area."""
        log.debug("TrayIcon.show() — stub")

    def hide(self) -> None:
        """Remove the tray icon."""
        log.debug("TrayIcon.hide() — stub")

    def set_active(self, active: bool) -> None:
        """Switch icon between idle and active visual state."""
        log.debug("TrayIcon.set_active(%s) — stub", active)
