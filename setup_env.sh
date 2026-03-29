#!/usr/bin/env bash
set -euo pipefail

# setup_env.sh — create a Python virtualenv, install requirements,
# and create .vscode/settings.json if missing (idempotent).

echo ""
echo "Setting up virtual environment and VS Code workspace settings..."

PYTHON_CMD=python3
VENV_DIR=.venv
VENV_PY="$VENV_DIR/bin/python"

# Ensure Python is available
echo ""
if ! command -v "$PYTHON_CMD" >/dev/null 2>&1; then
  echo "Error: $PYTHON_CMD not found. Install Python 3 and re-run this script."
  exit 1
fi

# Create virtual environment if it doesn't exist
echo ""
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtualenv at $VENV_DIR..."
  "$PYTHON_CMD" -m venv "$VENV_DIR"
else
  echo "Virtualenv $VENV_DIR already exists — will reuse it."
fi

# Upgrade pip in the virtualenv
echo ""
echo "Upgrading pip in the virtualenv..."
"$VENV_PY" -m pip install --upgrade pip

# Install requirements if requirements.txt exists
echo ""
if [ -f requirements.txt ]; then
  echo "Installing requirements from requirements.txt..."
  "$VENV_PY" -m pip install -r requirements.txt
else
  echo "No requirements.txt found — skipping pip install."
fi


# Create .vscode settings if missing
VSCODE_DIR=.vscode
SETTINGS_FILE="$VSCODE_DIR/settings.json"

echo ""
if [ ! -d "$VSCODE_DIR" ]; then
  mkdir -p "$VSCODE_DIR"
  echo "Created $VSCODE_DIR"
fi

echo ""
if [ ! -f "$SETTINGS_FILE" ]; then
  cat > "$SETTINGS_FILE" <<'JSON'
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.pythonPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.extraPaths": [
    "./remote_mouse"
  ]
}
JSON
  echo "Wrote $SETTINGS_FILE"
else
  echo "$SETTINGS_FILE already exists — not overwriting."
fi

echo ""
echo "Setup finished. Activate the virtualenv with:"
echo ""
echo -e "\tsource $VENV_DIR/bin/activate"
echo ""
# echo "To use this interpreter in VS Code: open the workspace and select the interpreter at: $VENV_PY"
# echo ""