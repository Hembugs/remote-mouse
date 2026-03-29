"""Shared Action enum for remote_mouse."""

from enum import Enum


class Action(Enum):
    """Enum representing possible actions from the client."""
    MOVE = "move"
    CLICK = "click"
    SCROLL = "scroll"
    MOUSEDOWN = "mousedown"
    MOUSEUP = "mouseup"
    ALT_DOWN = "alt_down"
    ALT_UP = "alt_up"
    TAB_PRESS = "tab_press"
    SHIFT_TAB_PRESS = "shift_tab_press"
