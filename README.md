# remote-mouse

Control your laptop mouse from your phone browser over WiFi.

## Requirements

- Windows only
- Python 3.10+

## Installation

Clone the repo, create a virtual environment named `.venv`, and install the dependencies into it.

### PowerShell/Command Prompt

```powershell
git clone https://github.com/Hembugs/remote-mouse.git
cd remote-mouse
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in the current shell and try again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## How to Run

1. Start the server on your laptop from the activated virtual environment:

   ```powershell
   python server.py
   ```

2. Find your laptop's local IP address. Open Command Prompt and run:

   ```bat
   ipconfig
   ```

   Look for the IPv4 Address under your WiFi adapter.

3. Open your phone browser and go to:

   ```text
   http://<your-ip>:5000
   ```

Make sure your phone is on the same WiFi network as your laptop.

## Usage

- Drag on the dark area to move the cursor
- Tap for left click
- Double tap, then drag to click and drag
- Two-finger drag to scroll
- Three-finger swipe to switch windows with Alt+Tab

## Notes

- Only works on your local WiFi network
- Do not run this on public WiFi because no authentication is implemented
- To leave the virtual environment later, run `deactivate`
