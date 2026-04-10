"""Application-wide constants and configuration defaults."""

# Display name used in UI and desktop files
APP_NAME = "autoscroll-x11"
APP_ID = "io.github.jwiley.AutoscrollX11"

# Pixels the pointer must move from the press point to activate autoscroll.
ACTIVATION_RADIUS_PX = 8

# Dead zone radius (pixels) around the anchor; no scrolling within this area.
DEAD_ZONE_PX = 10

# Maximum scroll velocity (lines per second) at full deflection.
MAX_SCROLL_VELOCITY = 60

# Polling interval for motion tracking (milliseconds).
POLL_INTERVAL_MS = 16  # ~60 Hz
