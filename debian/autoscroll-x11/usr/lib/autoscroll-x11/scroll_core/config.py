"""Application-wide constants and configuration defaults."""

# Display name used in UI and desktop files
APP_NAME = "autoscroll-x11"
APP_ID = "io.github.jwiley.AutoscrollX11"

# Pixels from the press point that define both the activation gate
# and the zero-scroll center region while ACTIVE.
# Inside this radius: no action. Outside: autoscroll activates and scrolls.
ACTIVATION_RADIUS_PX = 10

# Polling interval for motion tracking (milliseconds).
POLL_INTERVAL_MS = 16  # ~60 Hz

# Aspect-ratio band for diagonal glyph selection.
# When abs(dx)/abs(dy) is within [DIAGONAL_RATIO_MIN, DIAGONAL_RATIO_MAX]
# (and both axes are outside the activation radius), a diagonal arrow is shown.
DIAGONAL_RATIO_MIN: float = 0.5
DIAGONAL_RATIO_MAX: float = 2.0
