"""X11 display: pointer queries and synthetic scroll event injection."""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)

# X button numbers for scroll directions.
BUTTON_SCROLL_UP = 4
BUTTON_SCROLL_DOWN = 5

# Button mask for middle button (button 2).
_BUTTON2_MASK = 512  # Xlib.X.Button2Mask


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

    def query_pointer(self) -> tuple[int, int, bool]:
        """Return (x, y, button2_held) from a live pointer query."""
        if self._root is None:
            return (0, 0, False)
        p = self._root.query_pointer()
        return (p.root_x, p.root_y, bool(p.mask & _BUTTON2_MASK))

    def ungrab_pointer(self) -> None:
        """Release the active pointer grab.

        Called on autoscroll activation so that XTest scroll events
        are delivered to the target window rather than redirected back
        to this client by the active Button2 grab.
        """
        if self._display is None:
            return
        import Xlib.X
        self._display.ungrab_pointer(Xlib.X.CurrentTime)
        self._display.flush()
        log.debug("X11Display: pointer ungrabbed")

    def send_scroll_event(self, button: int) -> None:
        """Inject a synthetic XTest scroll button press+release.

        button 4 = scroll up, button 5 = scroll down.
        """
        if self._display is None:
            return
        import Xlib.X
        import Xlib.ext.xtest as xtest
        log.debug("X11Display: send_scroll_event button=%d", button)
        xtest.fake_input(self._display, Xlib.X.ButtonPress, button)
        xtest.fake_input(self._display, Xlib.X.ButtonRelease, button)
        self._display.flush()

    def fileno(self) -> int:
        """Return the X connection file descriptor.

        Suitable for use with GLib.io_add_watch.
        """
        if self._display is None:
            raise RuntimeError("Display not open")
        return self._display.fileno()
