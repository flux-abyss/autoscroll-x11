"""X11 display helpers stub.

Wraps Xlib (python3-xlib) for display connection, pointer queries, and
XTest event injection. All methods are stubs pending Phase 2 implementation.
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


class X11Display:
    """Thin wrapper around Xlib display operations.

    This is a stub. Full Xlib/XInput2 integration is deferred to Phase 2.
    """

    def __init__(self) -> None:
        self._display = None  # Will hold Xlib.display.Display instance.

    def open(self) -> None:
        """Open connection to the running X display (uses DISPLAY env var).

        Raises:
            RuntimeError: if no X display is available.
        """
        log.debug("X11Display.open() — stub")

    def close(self) -> None:
        """Close the X display connection."""
        log.debug("X11Display.close() — stub")

    def get_pointer_position(self) -> tuple[int, int]:
        """Return current pointer position in root-window coordinates.

        Returns:
            (x, y) pixel coordinates.
        """
        log.debug("X11Display.get_pointer_position() — stub")
        return (0, 0)

    def warp_pointer(self, x: int, y: int) -> None:
        """Move the pointer to root-window coordinates (x, y)."""
        log.debug("X11Display.warp_pointer(%d, %d) — stub", x, y)

    def send_scroll_event(self, button: int) -> None:
        """Inject a synthetic XTest scroll button event.

        Args:
            button: X button number (4=up, 5=down, 6=left, 7=right).
        """
        log.debug("X11Display.send_scroll_event(button=%d) — stub", button)
