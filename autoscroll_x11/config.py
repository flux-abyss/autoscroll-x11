"""Application-wide constants and configuration defaults."""

# Display name used in UI and desktop files
APP_NAME = "autoscroll-x11"
APP_ID = "io.github.jwiley.AutoscrollX11"

# Milliseconds the middle button must be held before activating autoscroll.
# A release before this threshold is treated as a normal middle click.
HOLD_THRESHOLD_MS = 250

# Dead zone radius (pixels) around the anchor; no scrolling within this area.
DEAD_ZONE_PX = 10

# Maximum scroll velocity (lines per second) at full deflection.
MAX_SCROLL_VELOCITY = 60

# Polling interval for motion tracking (milliseconds).
POLL_INTERVAL_MS = 16  # ~60 Hz
