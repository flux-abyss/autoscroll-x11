# Roadmap

## Phase 1 — Skeleton (current)

- [x] Debian package structure
- [x] Python package wiring and entry point
- [x] FSM state dataclass
- [x] Stub interfaces for all core/UI/platform modules
- [x] Smoke tests
- [x] Dev launcher and local install script

## Phase 2 — Core Input

- [ ] XInput2 passive grab on button 2 (all windows)
- [ ] Hold-threshold timer using GLib timeout
- [ ] Normal middle-click replay on short press
- [ ] Pointer position queries via Xlib

## Phase 3 — Scrolling

- [ ] MotionModel: dead-zone clamping + linear acceleration curve
- [ ] ScrollEngine: XTest button 4/5/6/7 injection at poll rate
- [ ] Sub-pixel accumulation for smooth low-speed scrolling

## Phase 4 — UI

- [ ] AnchorOverlay: transparent GTK window at anchor position
- [ ] Directional arrow: 8-direction SVG or Cairo drawing
- [ ] Input-shape carve-out so overlay does not capture clicks
- [ ] TrayIcon: AppIndicator3 with idle/active icons
- [ ] ScrollIndicator: optional pointer-adjacent direction hint

## Phase 5 — Polish

- [ ] Per-application velocity overrides (config file)
- [ ] Horizontal scroll support
- [ ] Diagonal scroll
- [ ] Wayland/XWayland investigation
- [ ] Accessibility review
