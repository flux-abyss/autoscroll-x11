"""Application state machine."""

from dataclasses import dataclass, field
from enum import Enum, auto


class ScrollMode(Enum):
    """Autoscroll FSM states."""

    IDLE = auto()  # No middle-button activity.
    ARMED = auto()  # Middle button pressed; within hold threshold.
    ACTIVE = auto()  # Hold threshold exceeded; autoscroll running.


@dataclass
class ScrollState:
    """Mutable runtime state passed between components."""

    mode: ScrollMode = ScrollMode.IDLE

    # Anchor position in root-window coordinates.
    anchor_x: int = 0
    anchor_y: int = 0

    # Current pointer position in root-window coordinates.
    pointer_x: int = 0
    pointer_y: int = 0

    # Millisecond timestamp of the button-press that armed the session.
    press_time_ms: int = 0

    # Accumulated sub-pixel scroll deltas for smooth scrolling.
    _delta_x: float = field(default=0.0, repr=False)
    _delta_y: float = field(default=0.0, repr=False)

    def reset(self) -> None:
        """Return to IDLE and clear transient state."""
        self.mode = ScrollMode.IDLE
        self.anchor_x = 0
        self.anchor_y = 0
        self.pointer_x = 0
        self.pointer_y = 0
        self.press_time_ms = 0
        self._delta_x = 0.0
        self._delta_y = 0.0
