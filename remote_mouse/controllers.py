"""Input controllers for remote-mouse."""

import sys
from typing import Optional

from .common import logger
from .actions import Action

# Cross platform input controller interface and implementations. 
# 
# The controller abstracts away platform-specific details of simulating mouse 
# and keyboard input, allowing the rest of the code
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key


class InputController:
    """Abstract base class for input controllers."""

    def move(self, dx: int, dy: int) -> None:
        raise NotImplementedError

    def click(self, button: str = "left") -> None:
        raise NotImplementedError

    def scroll(self, amount: int) -> None:
        raise NotImplementedError

    def mousedown(self) -> None:
        raise NotImplementedError

    def mouseup(self) -> None:
        raise NotImplementedError

    def alt_down(self) -> None:
        raise NotImplementedError

    def alt_up(self) -> None:
        raise NotImplementedError

    def tab_press(self) -> None:
        raise NotImplementedError

    def shift_tab_press(self) -> None:
        raise NotImplementedError

    def handle_action(self, action: Action, data: dict) -> None:
        """Dispatch an `Action` with the provided `data` to the appropriate method.

        This centralizes action handling so callers (e.g., websocket handlers)
        can pass an enum and let the controller perform the necessary work.
        """
        try:
            if action is Action.MOVE:
                dx = int(data.get("dx", 0))
                dy = int(data.get("dy", 0))
                self.move(dx, dy)

            elif action is Action.CLICK:
                button = data.get("button", "left")
                self.click(button)

            elif action is Action.SCROLL:
                amount = int(data.get("amount", 0))
                self.scroll(amount)

            elif action in {
                Action.MOUSEDOWN,
                Action.MOUSEUP,
                Action.ALT_DOWN,
                Action.ALT_UP,
                Action.TAB_PRESS,
                Action.SHIFT_TAB_PRESS,
            }:
                getattr(self, action.value)()

            else:
                logger.debug("Unhandled action in controller: %s", action.value)

        except Exception:
            logger.exception("Controller failed handling action: %s", action.value)


class WindowsController(InputController):
    """Controller that invokes Windows API via ctypes."""

    def __init__(self) -> None:
        import ctypes

        self._ct = ctypes

    def move(self, dx: int, dy: int) -> None:
        self._ct.windll.user32.mouse_event(0x0001, dx, dy, 0, 0)

    def click(self, button: str = "left") -> None:
        if button == "left":
            self._ct.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            self._ct.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
        else:
            self._ct.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
            self._ct.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)

    def scroll(self, amount: int) -> None:
        self._ct.windll.user32.mouse_event(0x0800, 0, 0, amount * 120, 0)

    def mousedown(self) -> None:
        self._ct.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)

    def mouseup(self) -> None:
        self._ct.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)

    def alt_down(self) -> None:
        self._ct.windll.user32.keybd_event(0x12, 0, 0, 0)

    def alt_up(self) -> None:
        self._ct.windll.user32.keybd_event(0x12, 0, 2, 0)

    def tab_press(self) -> None:
        self._ct.windll.user32.keybd_event(0x09, 0, 0, 0)
        self._ct.windll.user32.keybd_event(0x09, 0, 2, 0)

    def shift_tab_press(self) -> None:
        self._ct.windll.user32.keybd_event(0x10, 0, 0, 0)
        self._ct.windll.user32.keybd_event(0x09, 0, 0, 0)
        self._ct.windll.user32.keybd_event(0x09, 0, 2, 0)
        self._ct.windll.user32.keybd_event(0x10, 0, 2, 0)


class PynputController(InputController):
    """Controller that uses the `pynput` library for cross-platform input control."""

    def __init__(self) -> None:

        self._mouse = MouseController()
        self._button = Button
        self._keyboard = KeyboardController()
        self._key = Key

    def move(self, dx: int, dy: int) -> None:
        self._mouse.move(dx, dy)

    def click(self, button: str = "left") -> None:
        if button == "left":
            self._mouse.click(self._button.left, 1)
        else:
            self._mouse.click(self._button.right, 1)

    def scroll(self, amount: int) -> None:
        self._mouse.scroll(0, amount)

    def mousedown(self) -> None:
        self._mouse.press(self._button.left)

    def mouseup(self) -> None:
        self._mouse.release(self._button.left)

    def alt_down(self) -> None:
        self._keyboard.press(self._key.alt)

    def alt_up(self) -> None:
        self._keyboard.release(self._key.alt)

    def tab_press(self) -> None:
        self._keyboard.press(self._key.tab)
        self._keyboard.release(self._key.tab)

    def shift_tab_press(self) -> None:
        self._keyboard.press(self._key.shift)
        self._keyboard.press(self._key.tab)
        self._keyboard.release(self._key.tab)
        self._keyboard.release(self._key.shift)


def create_controller() -> Optional[InputController]:
    """Return a platform-appropriate controller or None if unavailable."""
    if sys.platform.startswith("win"):
        try:
            return WindowsController()
        except Exception:
            logger.exception("Failed to initialize Windows input controller")
            return None

    try:
        return PynputController()
    except ImportError:
        logger.warning("`pynput` not available; input control disabled")
        return None
    except Exception:
        logger.exception("Failed to initialize input controller")
        return None


controller = create_controller()
if controller is None:
    logger.warning("No input controller available — mouse/keyboard actions disabled")
