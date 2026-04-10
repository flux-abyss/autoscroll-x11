# Architecture

## Overview

autoscroll-x11 provides Windows-style middle-click autoscroll on X11.
When the middle mouse button is held past a short threshold, the pointer
position at that moment becomes the **anchor point**.  Moving the pointer
away from the anchor scrolls the active window in that direction at a speed
proportional to the distance.  Releasing the button immediately stops
scrolling; a brief press is forwarded as a normal middle click.

## Component Map

```
┌─────────────────────────────────────────────────┐
│                   app.py / __main__.py           │  CLI entry, GTK main loop
└───────────┬─────────────────────────────────────┘
            │
   ┌────────▼────────┐        ┌──────────────────┐
   │  InputMonitor   │───────▶│   ScrollState    │
   │  (core/)        │        │   (core/state)   │
   └────────┬────────┘        └──────────────────┘
            │ motion events
   ┌────────▼────────┐
   │  MotionModel    │  dead-zone + velocity curve
   └────────┬────────┘
            │ (vx, vy)
   ┌────────▼────────┐
   │  ScrollEngine   │  XTest synthetic events
   └─────────────────┘

   ┌──────────────────────────────────────────────┐
   │  UI layer  (ui/)                              │
   │   TrayIcon · AnchorOverlay · ScrollIndicator  │
   └──────────────────────────────────────────────┘

   ┌──────────────────────────────────────────────┐
   │  Platform layer  (platform/)                  │
   │   X11Display · WMInterface                    │
   └──────────────────────────────────────────────┘
```

## Data Flow

1. `InputMonitor` passively grabs button 2 via XInput2.
2. On press, `ScrollState` transitions `IDLE → ARMED` and starts a timer.
3. If the button is released before `HOLD_THRESHOLD_MS`, state resets to
   `IDLE` and the press is replayed as a normal click.
4. On threshold expiry, state transitions `ARMED → ACTIVE`; the anchor is
   recorded and `AnchorOverlay` is shown.
5. Each `POLL_INTERVAL_MS` tick: `MotionModel.compute_velocity` is called
   with the current displacement, and `ScrollEngine.tick` injects events.
6. On release in ACTIVE state, `ScrollEngine.flush`, overlay hidden, state
   resets to `IDLE`.

## Key Source Files

| File | Role |
|------|------|
| `autoscroll_x11/app.py` | Entry point, CLI parsing, GTK app lifecycle |
| `autoscroll_x11/config.py` | Tuneable constants |
| `autoscroll_x11/core/state.py` | FSM enum + mutable runtime state |
| `autoscroll_x11/core/input_monitor.py` | XInput2 grab + event dispatch |
| `autoscroll_x11/core/motion_model.py` | Displacement → velocity |
| `autoscroll_x11/core/scroll_engine.py` | XTest event injection |
| `autoscroll_x11/ui/overlay.py` | Anchor point GTK overlay |
| `autoscroll_x11/ui/tray.py` | System-tray icon |
| `autoscroll_x11/platform/x11.py` | Xlib display wrapper |
| `autoscroll_x11/platform/wm.py` | EWMH window queries |
