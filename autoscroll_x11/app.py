"""Application entry point."""

import sys

from autoscroll_x11.logging_setup import setup_logging


def main() -> None:
    """Initialise logging and start the application."""
    setup_logging()

    # TODO: parse CLI args (--tray, --debug, --version)
    # TODO: instantiate GTK application and run main loop
    print("autoscroll-x11: not yet implemented", file=sys.stderr)
    sys.exit(0)
