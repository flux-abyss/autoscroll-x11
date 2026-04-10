"""X11 display: pointer queries and synthetic scroll event injection."""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)

# X button numbers for scroll directions.
BUTTON_SCROLL_UP = 4
BUTTON_SCROLL_DOWN = 5


class X11Display:
    """Wraps python3-xlib for pointer queries and XTest scroll injection."""

    def __init__(self) -> None:
        self._display = None
        self._root = None

    def open(self) -> None:
        """Open connection to the running X display.

        Raises:
            RuntimeError: if the display cannot be opened.
        """
        try:
            import Xlib.display
        except ImportError as exc:
            raise RuntimeError("python3-xlib is not installed") from exc

        try:
            self._display = Xlib.display.Display()
        except Exception as exc:
            raise RuntimeError(
                f"Cannot open X display: {exc}"
            ) from exc

        self._root = self._display.screen().root
        log.debug("X11Display opened")

    def close(self) -> None:
        """Close the display connection."""
        if self._display is not None:
            self._display.close()
            self._display = None
            self._root = None
        log.debug("X11Display closed")

    def get_pointer_position(self) -> tuple[int, int]:
        """Return current pointer position in root-window coordinates."""
        if self._root is None:
            return (0, 0)
        p = self._root.query_pointer()
        return (p.root_x, p.root_y)

    def send_scroll_event(self, button: int) -> None:
        """Inject a synthetic XTest scroll button press+release.

        Args:
            button: X button number (4=up, 5=down).
        """
        if self._display is None:
            return
        import Xlib.X
        import Xlib.ext.xtest as xtest
        xtest.fake_input(self._display, Xlib.X.ButtonPress, button)
        xtest.fake_input(self._display, Xlib.X.ButtonRelease, button)
        self._display.sync()

    def fileno(self) -> int:
        """Return the X connection file descriptor.

        Suitable for use with GLib.io_add_watch.
        """
        if self._display is None:
            raise RuntimeError("Display not open")
        return self._display.fileno()
