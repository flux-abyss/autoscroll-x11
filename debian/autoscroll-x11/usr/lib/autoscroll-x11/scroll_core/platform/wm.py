"""Window manager integration stub.

Queries the active window and its scroll capabilities via EWMH/ICCCM.
Used to determine per-window scroll sensitivity overrides in later phases.
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class WMInterface:
    """Queries WM state relevant to autoscroll behaviour.

    This is a stub. EWMH property parsing is deferred to Phase 2.
    """

    def get_active_window_id(self) -> int | None:
        """Return the XID of the currently focused window, or None.

        Uses the ``_NET_ACTIVE_WINDOW`` root property.
        """
        log.debug("WMInterface.get_active_window_id() — stub")
        return None

    def get_window_class(self, window_id: int) -> str | None:
        """Return the WM_CLASS string for *window_id*, or None."""
        log.debug("WMInterface.get_window_class(%d) — stub", window_id)
        return None
