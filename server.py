from flask import Flask, send_file
from flask_sock import Sock
import ctypes
import json
import os
import socket
import threading
import time
import tkinter as tk

import qrcode
from PIL import ImageTk
from werkzeug.serving import make_server

app = Flask(__name__)
sock = Sock(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
user32 = ctypes.windll.user32
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

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


def get_local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def build_connection_url():
    return f"http://{get_local_ip()}:{SERVER_PORT}"


def build_qr_popup(url):
    root = tk.Tk()
    root.title("Remote Mouse QR Code")
    root.geometry("420x560")
    root.resizable(False, False)
    root.configure(bg="#0f172a")

    qr_image = qrcode.make(url).resize((280, 280))
    qr_photo = ImageTk.PhotoImage(qr_image)

    frame = tk.Frame(root, bg="#0f172a", padx=24, pady=24)
    frame.pack(fill="both", expand=True)

    title = tk.Label(
        frame,
        text="Scan to Connect",
        font=("Segoe UI", 20, "bold"),
        fg="#e2e8f0",
        bg="#0f172a",
    )
    title.pack(pady=(0, 10))

    subtitle = tk.Label(
        frame,
        text="Open your phone camera and scan this code while both devices are on the same WiFi network.",
        font=("Segoe UI", 10),
        fg="#94a3b8",
        bg="#0f172a",
        wraplength=340,
        justify="center",
    )
    subtitle.pack(pady=(0, 18))

    qr_label = tk.Label(frame, image=qr_photo, bg="#ffffff", bd=0)
    qr_label.image = qr_photo
    qr_label.pack(pady=(0, 18))

    url_label = tk.Label(
        frame,
        text=url,
        font=("Consolas", 11),
        fg="#5eead4",
        bg="#0f172a",
        wraplength=340,
        justify="center",
    )
    url_label.pack(pady=(0, 18))

    def copy_url():
        root.clipboard_clear()
        root.clipboard_append(url)
        copied_label.config(text="Copied to clipboard")

    copy_button = tk.Button(
        frame,
        text="Copy URL",
        command=copy_url,
        font=("Segoe UI", 10, "bold"),
        bg="#14b8a6",
        fg="#082f49",
        activebackground="#2dd4bf",
        activeforeground="#082f49",
        relief="flat",
        padx=18,
        pady=10,
        cursor="hand2",
    )
    copy_button.pack()

    copied_label = tk.Label(
        frame,
        text="",
        font=("Segoe UI", 9),
        fg="#94a3b8",
        bg="#0f172a",
    )
    copied_label.pack(pady=(12, 0))

    return root


def run_server(http_server):
    http_server.serve_forever()

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
    connection_url = build_connection_url()
    print(f"Remote Mouse is running at {connection_url}")

    http_server = make_server(SERVER_HOST, SERVER_PORT, app, threaded=True)
    server_thread = threading.Thread(target=run_server, args=(http_server,), daemon=False)
    server_thread.start()
    qr_root = None

    try:
        qr_root = build_qr_popup(connection_url)
    except tk.TclError:
        print("QR popup could not be displayed. Use the printed URL instead.")

    try:
        while server_thread.is_alive():
            if qr_root is not None:
                try:
                    qr_root.update_idletasks()
                    qr_root.update()
                except tk.TclError:
                    qr_root = None
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nStopping Remote Mouse...")
    finally:
        http_server.shutdown()
        server_thread.join()
        if qr_root is not None:
            try:
                qr_root.destroy()
            except tk.TclError:
                pass
