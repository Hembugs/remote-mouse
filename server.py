from flask import Flask, send_file
from flask_sock import Sock
import json
import os
import ctypes

app = Flask(__name__)
sock = Sock(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
                ctypes.windll.user32.mouse_event(0x0001, dx, dy, 0, 0)
            elif action == 'click':
                button = data.get('button', 'left')
                if button == 'left':
                    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
                    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
                elif button == 'right':
                    ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
                    ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)
            elif action == 'scroll':
                ctypes.windll.user32.mouse_event(0x0800, 0, 0, int(data['amount']) * 120, 0)
            elif action == 'mousedown':
                ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            elif action == 'mouseup':
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            elif action == 'alt_down':
                ctypes.windll.user32.keybd_event(0x12, 0, 0, 0)
            elif action == 'alt_up':
                ctypes.windll.user32.keybd_event(0x12, 0, 2, 0)
            elif action == 'tab_press':
                ctypes.windll.user32.keybd_event(0x09, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0x09, 0, 2, 0)
            elif action == 'shift_tab_press':
                ctypes.windll.user32.keybd_event(0x10, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0x09, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0x09, 0, 2, 0)
                ctypes.windll.user32.keybd_event(0x10, 0, 2, 0)
        except Exception:
            break

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)