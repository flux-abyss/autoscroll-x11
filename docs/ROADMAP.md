# Roadmap

## Phase 1 — Skeleton

- [x] Debian package structure
- [x] Python package wiring and entry point
- [x] FSM state dataclass
- [x] Stub interfaces for core/UI/platform modules
- [x] Smoke tests
- [x] Dev launcher and local install script

## Phase 2 — Tray and CLI

- [x] `--version` flag
- [x] `--tray` flag with honest error for normal mode
- [x] Gtk.StatusIcon tray icon with enabled toggle and quit
- [x] CLI smoke tests
- [x] Desktop files consistent with implemented behavior

## Phase 3 — Core Autoscroll (current)

- [x] Left-click tray crash fixed
- [x] Xlib display open/close with real error handling
- [x] XTest synthetic scroll events (button 4/5)
- [x] Root-window button-2 grab
- [x] GLib.io_add_watch on X fd (integrates with Gtk.main)
- [x] IDLE → ARMED → ACTIVE → IDLE FSM transitions
- [x] Hold-threshold detection (motion events + poll timer)
- [x] Quick-click replay as synthetic middle click
- [x] MotionModel: dead zone, linear velocity, direction sign, cap
- [x] ScrollEngine: sub-line accumulation, per-tick event injection
- [x] AnchorOverlay: POPUP window with Cairo crosshair, click-through
- [x] Clean shutdown: ungrab, flush, hide overlay
- [ ] Enabled/disabled toggle wired to InputMonitor
- [ ] Icon assets (placeholder SVG)

## Phase 4 — Polish

- [ ] Horizontal scrolling (button 6/7)
- [ ] Directional arrow overlay (8 directions)
- [ ] Enabled toggle respected during active scroll
- [ ] Per-application velocity overrides via config file
- [ ] Preferences dialog
- [ ] Wayland/XWayland investigation
