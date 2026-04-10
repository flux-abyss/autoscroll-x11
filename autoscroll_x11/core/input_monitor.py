"""Input monitor stub.

Responsible for grabbing the middle mouse button via XInput2 and dispatching
press/release/motion events to the rest of the pipeline.
"""

from __future__ import annotations

import logging
from typing import Callable

log = logging.getLogger(__name__)


class InputMonitor:
    """Grabs pointer events from X11 and forwards them to registered handlers.

    This is a stub. Full XInput2 integration is deferred to the next phase.
    """

    def __init__(self) -> None:
        self._on_press: Callable[[], None] | None = None
        self._on_release: Callable[[], None] | None = None
        self._on_motion: Callable[[int, int], None] | None = None

    def set_handlers(
        self,
        on_press: Callable[[], None],
        on_release: Callable[[], None],
        on_motion: Callable[[int, int], None],
    ) -> None:
        """Register event callbacks."""
        self._on_press = on_press
        self._on_release = on_release
        self._on_motion = on_motion

    def start(self) -> None:
        """Begin listening for pointer events.

        Acquires an XInput2 passive grab on button 2 (middle) for all windows.
        Raises ``RuntimeError`` if the X display cannot be opened.
        """
        log.debug("InputMonitor.start() — not yet implemented")

    def stop(self) -> None:
        """Release the pointer grab and stop the event loop."""
        log.debug("InputMonitor.stop() — not yet implemented")
