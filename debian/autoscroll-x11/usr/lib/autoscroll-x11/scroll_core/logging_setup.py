"""Logging configuration."""

import logging
import os


def setup_logging(debug: bool = False) -> None:
    """Configure root logger.

    Level is overridden to DEBUG when *debug* is True or when the environment
    variable ``AUTOSCROLL_DEBUG`` is set to a non-empty value.
    """
    level = logging.DEBUG if (
        debug or os.getenv("AUTOSCROLL_DEBUG")) else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(levelname)s %(name)s: %(message)s",
    )
