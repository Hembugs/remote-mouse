# remote-mouse

Control your laptop mouse from your phone browser over WiFi.

## Requirements

- Windows only
- Python 3

## Installation

Clone the repo and install dependencies:

git clone https://github.com/Hembugs/remote-mouse.git
cd remote-mouse
pip install flask flask-sock

## How to run

1. Start the server on your laptop:
python server.py

2. Find your laptop's local IP — open Command Prompt and run:
ipconfig

Look for IPv4 Address under your WiFi adapter.

3. Open your phone browser and go to:
http://<your-ip>:5000

Make sure your phone is on the same WiFi as your laptop.

## Usage

- **Drag** on the dark area to move the cursor
- **Left Click / Right Click** buttons for clicking
- **Hold Scroll** and drag to scroll

## Notes

- Only works on your local WiFi network
- Don't run on public WiFi — no authentication is implemented
