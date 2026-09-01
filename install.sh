#!/usr/bin/env bash

set -e

echo "================================"
echo "       WineShield Installer"
echo "================================"
echo

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

echo "[OK] Python 3 found."

# Check Wine
if ! command -v wine >/dev/null 2>&1; then
    echo "Error: Wine is not installed."
    echo
    echo "On Ubuntu/Debian, install it with:"
    echo "  sudo apt install wine"
    exit 1
fi

echo "[OK] Wine found."

# Check pipx
if ! command -v pipx >/dev/null 2>&1; then
    echo "Error: pipx is not installed."
    echo
    echo "On Ubuntu/Debian, install it with:"
    echo "  sudo apt install pipx"
    echo "  pipx ensurepath"
    exit 1
fi

echo "[OK] pipx found."

echo
echo "Installing WineShield..."

pipx install -e . --force

echo
echo "================================"
echo " WineShield installed successfully"
echo "================================"
echo
echo "Try:"
echo "  wineshield --help"
echo "  wineshield --version"
echo "  wineshield update-appslist"
echo "  wineshield list"