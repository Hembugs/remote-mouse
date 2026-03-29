"""WebSocket handlers for remote-mouse (package)."""


import json

from .app import sock
from .common import logger
from .actions import Action
from .controllers import controller

@sock.route("/ws")
def websocket(ws):
    """WebSocket endpoint accepting JSON action messages.

    Expected messages: {"action": "move", "dx": 10, "dy": -3}
    """

    while True:
        msg = ws.receive()
        if msg is None:
            logger.debug("WebSocket closed by client")
            break

        try:
            data = json.loads(msg)
        except json.JSONDecodeError:
            logger.warning("Received invalid JSON: %s", msg)
            continue

        action_str = data.get("action")
        if not action_str:
            continue

        try:
            action = Action(action_str)
        except ValueError:
            logger.debug("Unknown action received: %s", action_str)
            continue

        # Delegate action handling to the controller for centralized dispatch.
        if controller:
            try:
                controller.handle_action(action, data)
            except Exception:
                logger.exception("Error handling action: %s", getattr(action, "value", action_str))
