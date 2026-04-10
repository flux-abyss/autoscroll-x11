"""Application entry point."""

import argparse
import sys

from autoscroll_x11 import __version__
from autoscroll_x11.logging_setup import setup_logging


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="autoscroll-x11",
        description="Windows-like middle-click autoscroll for X11.",
    )
    p.add_argument(
        "--version",
        action="version",
        version=f"autoscroll-x11 {__version__}",
    )
    p.add_argument(
        "--tray",
        action="store_true",
        help="Run as tray-only application.",
    )
    p.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging.",
    )
    return p


def main() -> None:
    args = _build_parser().parse_args()
    setup_logging(debug=args.debug)

    if args.tray:
        _run_tray()
    else:
        print(
            "autoscroll-x11: normal mode is not implemented yet.\n"
            "Run with --tray to start the tray application.",
            file=sys.stderr,
        )
        sys.exit(1)


def _run_tray() -> None:
    try:
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk
    except (ImportError, ValueError) as exc:
        print(
            f"autoscroll-x11: GTK not available: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

    from autoscroll_x11.core.input_monitor import InputMonitor
    from autoscroll_x11.core.motion_model import MotionModel
    from autoscroll_x11.core.scroll_engine import ScrollEngine
    from autoscroll_x11.core.state import ScrollState
    from autoscroll_x11.platform.x11 import X11Display
    from autoscroll_x11.ui.overlay import AnchorOverlay
    from autoscroll_x11.ui.tray import TrayIcon

    display = X11Display()
    try:
        display.open()
    except RuntimeError as exc:
        print(f"autoscroll-x11: {exc}", file=sys.stderr)
        sys.exit(1)

    state = ScrollState()
    motion = MotionModel()
    engine = ScrollEngine(display)
    overlay = AnchorOverlay()
    monitor = InputMonitor(state, display, motion, engine, overlay)

    tray = TrayIcon()
    tray.show()

    monitor.start()

    try:
        Gtk.main()
    finally:
        monitor.stop()
        display.close()
