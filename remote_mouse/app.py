"""Flask application and Sock instance for remote_mouse package."""

import os
from flask_sock import Sock
from flask import Flask, send_file

from .common import logger


app = Flask(__name__)
sock = Sock(app)

# Determine the directory of this file (the package) and the project root
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# Serve trackpad.html from the parent directory of the package (project root)
ROOT_DIR = os.path.abspath(os.path.join(PACKAGE_DIR, os.pardir))


@app.route("/")
def index():
    logger.debug("Serving trackpad.html from %s", ROOT_DIR)
    return send_file(os.path.join(ROOT_DIR, "trackpad.html"))
