# remote-mouse

Control your computer's mouse from a phone browser over your local Wi‑Fi.

## Requirements

- Python 3.8+
- `pip` (or another installer) to install dependencies
- On macOS: Accessibility / Input Monitoring permissions for the Python
  interpreter used to run the server

## Installation

Clone the repository and run the included setup script which creates the
virtual environment, installs dependencies, and prepares VS Code settings:

```bash
git clone https://github.com/Hembugs/remote-mouse.git
cd remote-mouse
<<<<<<< Updated upstream
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
=======
./setup_env.sh
```

If the script is not executable, run it with `bash`:

```bash
bash setup_env.sh
```

After the script completes, activate the virtualenv:

```bash
source .venv/bin/activate
```

## Run the server

Start the server in the foreground (recommended for development):

```bash
python3 server.py
```

Then open the trackpad UI on your phone at:

```
http://<your-ip>:5000
```

Find your local IP:
- macOS: `ipconfig getifaddr en0`
- Linux: `hostname -I` or `ip addr show`
- Windows: `ipconfig`

## Stop the server

- If the server runs in the foreground: press <kbd>Ctrl</kbd>+<kbd>C</kbd> in the terminal.
- If it was started in the background or detached, find and kill the process:

```bash
# find the PID listening on port 5000
lsof -t -iTCP:5000 -sTCP:LISTEN
# then kill it
kill <PID>
# one-liner
kill $(lsof -t -iTCP:5000 -sTCP:LISTEN)
```

If you used `nohup` or a service manager, stop the service the same way you started it (e.g., `kill`, `brew services stop`, or `launchctl remove`).

## macOS permissions

On macOS you must grant Accessibility (and sometimes Input Monitoring) to the Terminal or the Python executable that runs the server. Add either the Terminal app or the `.venv/bin/python` executable under System Settings → Privacy & Security → Accessibility / Input Monitoring, then restart the server.

## Security

- This is an unauthenticated development server. Do not run it on public networks.

## Troubleshooting

- Mouse actions not working on macOS — ensure Accessibility/Input Monitoring permissions are granted and restart the process.

## Development notes

- The server serves `trackpad.html` at `/` and accepts JSON messages over a WebSocket at `/ws`.
- Core code lives in the `remote_mouse` package; the entrypoint is `server.py` at the project root.

To push changes back to your repo:

```bash
git add README.md
git commit -m "Update README with proper instructions"
git push
```
>>>>>>> Stashed changes
