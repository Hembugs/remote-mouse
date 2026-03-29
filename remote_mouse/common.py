"""Common utilities (logging) for remote_mouse."""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("remote_mouse")
