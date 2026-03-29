from flask import Flask, send_file
from flask_sock import Sock
import json
import os
import ctypes

app = Flask(__name__)
sock = Sock(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user32 = ctypes.windll.user32

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800

KEYEVENTF_KEYUP = 0x0002

VK_TAB = 0x09
VK_ENTER = 0x0D
VK_SHIFT = 0x10
VK_ALT = 0x12
VK_ESCAPE = 0x1B
VK_SPACE = 0x20
VK_LWIN = 0x5B

SUPPORTED_KEYS = {
    "esc": VK_ESCAPE,
    "enter": VK_ENTER,
    "space": VK_SPACE,
}


def mouse(flags, dx=0, dy=0, data=0):
    user32.mouse_event(flags, dx, dy, data, 0)


def key_down(vk_code):
    user32.keybd_event(vk_code, 0, 0, 0)


def key_up(vk_code):
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def tap_key(vk_code):
    key_down(vk_code)
    key_up(vk_code)

@app.route('/')
def index():
    return send_file(os.path.join(BASE_DIR, 'trackpad.html'))

@sock.route('/ws')
def websocket(ws):
    while True:
        try:
            data = json.loads(ws.receive())
            action = data.get('action')

            if action == 'move':
                dx, dy = int(data['dx']), int(data['dy'])
                mouse(MOUSEEVENTF_MOVE, dx=dx, dy=dy)
            elif action == 'click':
                button = data.get('button', 'left')
                if button == 'left':
                    mouse(MOUSEEVENTF_LEFTDOWN)
                    mouse(MOUSEEVENTF_LEFTUP)
                elif button == 'right':
                    mouse(MOUSEEVENTF_RIGHTDOWN)
                    mouse(MOUSEEVENTF_RIGHTUP)
                elif button == 'middle':
                    mouse(MOUSEEVENTF_MIDDLEDOWN)
                    mouse(MOUSEEVENTF_MIDDLEUP)
            elif action == 'scroll':
                mouse(MOUSEEVENTF_WHEEL, data=int(data['amount']) * 120)
            elif action == 'mousedown':
                mouse(MOUSEEVENTF_LEFTDOWN)
            elif action == 'mouseup':
                mouse(MOUSEEVENTF_LEFTUP)
            elif action == 'alt_down':
                key_down(VK_ALT)
            elif action == 'alt_up':
                key_up(VK_ALT)
            elif action == 'tab_press':
                tap_key(VK_TAB)
            elif action == 'shift_tab_press':
                key_down(VK_SHIFT)
                tap_key(VK_TAB)
                key_up(VK_SHIFT)
            elif action == 'key_tap':
                key_name = data.get('key')
                if key_name in SUPPORTED_KEYS:
                    tap_key(SUPPORTED_KEYS[key_name])
                elif key_name == 'win_d':
                    key_down(VK_LWIN)
                    tap_key(ord('D'))
                    key_up(VK_LWIN)
        except Exception:
            break

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
