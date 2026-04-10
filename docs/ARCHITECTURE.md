# Architecture

## Overview

autoscroll-x11 provides Windows-style middle-click autoscroll on X11.
When the middle mouse button is held past a short threshold, the pointer
position at that moment becomes the anchor point. Moving the pointer away
from the anchor scrolls the active window in that direction, with speed
proportional to the distance. Releasing the button stops scrolling
immediately. A brief press is forwarded as a normal middle click.

The application is tray-first: it runs as a background process with a
system-tray icon and no main window.

## Component Map

```
┌─────────────────────────────────────────────────┐
│           app.py / __main__.py                   │  CLI, wiring, Gtk.main()
└───────────┬─────────────────────────────────────┘
            │
   ┌────────▼────────┐        ┌──────────────────┐
   │  InputMonitor   │───────▶│   ScrollState    │
   │  (core/)        │        │   (core/state)   │
   └────────┬────────┘        └──────────────────┘
            │
   ┌────────▼────────┐
   │  MotionModel    │  dead-zone + linear velocity curve
   └────────┬────────┘
            │ (0.0, vy)
   ┌────────▼────────┐        ┌──────────────────┐
   │  ScrollEngine   │───────▶│   X11Display     │  XTest events
   └─────────────────┘        └──────────────────┘

   ┌────────────────────────────────┐
   │  AnchorOverlay  (ui/)          │  POPUP window, Cairo crosshair
   └────────────────────────────────┘

   ┌────────────────────────────────┐
   │  TrayIcon  (ui/)               │  Gtk.StatusIcon + menu
   └────────────────────────────────┘
```

## Data Flow

1. `InputMonitor.start()` grabs button 2 on the root window via Xlib.
2. `GLib.io_add_watch` wakes `_on_x_event` when the X fd has data.
3. **ButtonPress(2):** state → ARMED, press time recorded.
4. **MotionNotify or poll tick:** if ARMED and elapsed ≥ threshold → ACTIVE;
   anchor position frozen; `AnchorOverlay.show_at()` called.
5. **Poll tick while ACTIVE:** `MotionModel.compute_velocity(dx, dy)` called;
   result forwarded to `ScrollEngine.tick(0, vy)`.
6. **ScrollEngine.tick:** accumulates sub-line remainder, fires
   `X11Display.send_scroll_event(button)` for each whole line.
7. **ButtonRelease(2):** if ACTIVE → flush engine, hide overlay, reset state.
   If ARMED (quick click) → replay synthetic middle click.

## Tray Lifecycle

```
app._run_tray()
  X11Display.open()
  build: state, motion, engine, overlay, monitor
  TrayIcon.show()
  InputMonitor.start()        ← installs GLib watches
  Gtk.main()                  ← event loop
  [Quit selected in menu]
  Gtk.main_quit()
  InputMonitor.stop()         ← removes watches, ungrab
  X11Display.close()
```

## Key Source Files

| File | Role |
|------|------|
| `autoscroll_x11/app.py` | CLI, component wiring, tray run loop |
| `autoscroll_x11/config.py` | Tuneable constants |
| `autoscroll_x11/core/state.py` | FSM enum + mutable runtime state |
| `autoscroll_x11/core/input_monitor.py` | X11 button grab, FSM transitions |
| `autoscroll_x11/core/motion_model.py` | Displacement → velocity |
| `autoscroll_x11/core/scroll_engine.py` | XTest scroll event injection |
| `autoscroll_x11/ui/tray.py` | Gtk.StatusIcon, context menu |
| `autoscroll_x11/ui/overlay.py` | POPUP anchor marker window |
| `autoscroll_x11/platform/x11.py` | Xlib display wrapper |
| `autoscroll_x11/platform/wm.py` | EWMH queries (stub) |
