"""Entrypoint for remote-mouse server."""

import sys

# signal handling for graceful shutdown
import signal

# registers websocket routes
import remote_mouse.handlers

# creates Flask app and Sock
from remote_mouse.app import app

# import logger for signal handler
from remote_mouse.common import logger


def _shutdown(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Received signal %s; shutting down", signum)
    sys.exit(0)

# Register signal handlers for graceful shutdown on SIGTERM and SIGINT (e.g., Ctrl+C)
#    - SIGTERM = termination signal
#    - SIGINT = interrupt signal
signal.signal(signal.SIGTERM, _shutdown)
signal.signal(signal.SIGINT, _shutdown)


if __name__ == "__main__":
    logger.info("Starting server on 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, use_reloader=False)