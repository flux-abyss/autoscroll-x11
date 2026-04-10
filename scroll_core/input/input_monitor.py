"""Input monitor: grabs middle-button events from X11 and drives the FSM."""

from __future__ import annotations

import logging
import math

import Xlib.X
import Xlib.ext.xtest as xtest

from scroll_core.config import ACTIVATION_RADIUS_PX, POLL_INTERVAL_MS
from scroll_core.engine.motion_model import MotionModel
from scroll_core.engine.scroll_engine import ScrollEngine
from scroll_core.input.state import ScrollMode, ScrollState
from scroll_core.platform.x11 import X11Display
from scroll_core.ui.overlay import AnchorOverlay

log = logging.getLogger(__name__)


class InputMonitor:
    """Grabs button-2 events from X11 and drives the autoscroll FSM.

    Uses GLib.io_add_watch on the X connection file descriptor so the event
    loop integrates cleanly with Gtk.main().

    On activation the active pointer grab is released so that XTest scroll
    events (buttons 4/5) reach the target window rather than being redirected
    back to this client.  While ACTIVE, pointer position and button state are
    polled via query_pointer() each tick.
    """

    def __init__(
        self,
        state: ScrollState,
        display: X11Display,
        motion: MotionModel,
        engine: ScrollEngine,
        overlay: AnchorOverlay,
    ) -> None:
        self._state = state
        self._display = display
        self._motion = motion
        self._engine = engine
        self._overlay = overlay
        self._watch_id: int | None = None
        self._timer_id: int | None = None
        self._running: bool = False

    def start(self) -> None:
        """Install GLib watches for X events and the poll timer."""
        from gi.repository import GLib

        self._grab_button()

        fd = self._display.fileno()
        self._watch_id = GLib.io_add_watch(
            fd,
            GLib.IOCondition.IN,
            self._on_x_event,
        )
        self._timer_id = GLib.timeout_add(
            POLL_INTERVAL_MS,
            self._on_poll_tick,
        )
        self._running = True
        log.debug("InputMonitor started")

    def stop(self) -> None:
        """Remove GLib watches and release the button grab."""
        self._running = False
        from gi.repository import GLib

        watch_id = self._watch_id
        self._watch_id = None
        if watch_id is not None:
            GLib.source_remove(watch_id)

        timer_id = self._timer_id
        self._timer_id = None
        if timer_id is not None:
            GLib.source_remove(timer_id)

        self._ungrab_button()
        log.debug("InputMonitor stopped")

    # ------------------------------------------------------------------
    # Grab helpers
    # ------------------------------------------------------------------

    def _grab_button(self) -> None:
        root = self._display._root
        if root is None:
            return
        root.grab_button(
            Xlib.X.Button2,
            Xlib.X.AnyModifier,
            True,
            Xlib.X.ButtonPressMask
            | Xlib.X.ButtonReleaseMask
            | Xlib.X.PointerMotionMask,
            Xlib.X.GrabModeAsync,
            Xlib.X.GrabModeAsync,
            Xlib.X.NONE,
            Xlib.X.NONE,
        )
        self._display._display.flush()

    def _ungrab_button(self) -> None:
        root = self._display._root
        if root is None:
            return
        try:
            root.ungrab_button(Xlib.X.Button2, Xlib.X.AnyModifier)
            self._display._display.flush()
        except Exception:
            pass

    # ------------------------------------------------------------------
    # GLib callbacks
    # ------------------------------------------------------------------

    def _on_x_event(self, fd: int, condition: object) -> bool:
        """Called by GLib when X fd is readable.

        Returns True to keep the watch active.
        """
        if not self._running:
            self._watch_id = None
            return False
        display = self._display._display
        while display.pending_events():
            event = display.next_event()
            if event.type == Xlib.X.ButtonPress and event.detail == 2:
                self._handle_press(event.root_x, event.root_y)
            elif event.type == Xlib.X.ButtonRelease and event.detail == 2:
                self._handle_release(armed_release=True)
            elif event.type == Xlib.X.MotionNotify:
                self._handle_motion(event.root_x, event.root_y)
        return True

    def _on_poll_tick(self) -> bool:
        """Called by GLib every POLL_INTERVAL_MS. Returns True to repeat."""
        if not self._running:
            self._timer_id = None
            return False

        if self._state.mode == ScrollMode.ACTIVE:
            x, y, b2_held = self._display.query_pointer()
            self._state.pointer_x = x
            self._state.pointer_y = y

            if not b2_held:
                log.debug("Button2 released (detected by poll)")
                self._handle_release(armed_release=False)
                return True

            dx = x - self._state.anchor_x
            dy = y - self._state.anchor_y
            vx, vy = self._motion.compute_velocity(dx, dy)
            self._engine.tick(vx, vy)
            self._overlay.update_direction(dx, dy)

        return True

    # ------------------------------------------------------------------
    # FSM
    # ------------------------------------------------------------------

    def _handle_press(self, x: int, y: int) -> None:
        if self._state.mode != ScrollMode.IDLE:
            return
        self._state.mode = ScrollMode.ARMED
        self._state.press_x = x
        self._state.press_y = y
        self._state.pointer_x = x
        self._state.pointer_y = y
        log.debug("ARMED at (%d, %d)", x, y)

    def _handle_release(self, *, armed_release: bool) -> None:
        mode = self._state.mode
        was_quick = mode == ScrollMode.ARMED

        if mode == ScrollMode.ACTIVE:
            self._engine.flush()
            self._overlay.hide()
            # Passive grab was removed on activation; reinstall it.
            self._grab_button()

        self._state.reset()
        log.debug("IDLE (was %s)", mode)

        if was_quick and armed_release:
            self._replay_middle_click()

    def _handle_motion(self, x: int, y: int) -> None:
        if self._state.mode == ScrollMode.IDLE:
            return
        self._state.pointer_x = x
        self._state.pointer_y = y

        if self._state.mode == ScrollMode.ARMED:
            dx = x - self._state.press_x
            dy = y - self._state.press_y
            if math.hypot(dx, dy) >= ACTIVATION_RADIUS_PX:
                self._activate()

    def _activate(self) -> None:
        self._state.mode = ScrollMode.ACTIVE
        self._state.anchor_x = self._state.press_x
        self._state.anchor_y = self._state.press_y
        self._overlay.show_at(self._state.anchor_x, self._state.anchor_y)
        # Release the active pointer grab so XTest scroll events (buttons 4/5)
        # reach the target window instead of being redirected to this client.
        self._display.ungrab_pointer()
        log.debug(
            "ACTIVE anchor (%d, %d)",
            self._state.anchor_x,
            self._state.anchor_y,
        )

    # ------------------------------------------------------------------
    # Middle-click replay
    # ------------------------------------------------------------------

    def _replay_middle_click(self) -> None:
        """Forward a synthetic button-2 click to the window under the pointer.

        The passive grab on Button2 would re-intercept any XTest Button2 press
        we inject while it is installed.  Remove it first, inject the click,
        then reinstall it so subsequent presses are grabbed again.
        """
        self._ungrab_button()

        d = self._display._display
        xtest.fake_input(d, Xlib.X.ButtonPress, 2)
        xtest.fake_input(d, Xlib.X.ButtonRelease, 2)
        d.sync()

        self._grab_button()
        log.debug("Middle click replayed and grab reinstalled")
