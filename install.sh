#!/usr/bin/env bash

set -e

echo "================================"
echo "       WineShield Installer"
echo "================================"
echo

# Check supported package manager
if ! command -v apt >/dev/null 2>&1; then
    echo "Error: This installer currently supports Ubuntu/Debian systems only."
    exit 1
fi

missing_packages=()

# Check Python 3
if ! command -v python3 >/dev/null 2>&1; then
    missing_packages+=("python3")
else
    echo "[OK] Python 3 found."
fi

# Check Wine
if ! command -v wine >/dev/null 2>&1; then
    missing_packages+=("wine")
else
    echo "[OK] Wine found."
fi

# Check pipx
if ! command -v pipx >/dev/null 2>&1; then
    missing_packages+=("pipx")
else
    echo "[OK] pipx found."
fi

# Install missing dependencies
if [ ${#missing_packages[@]} -gt 0 ]; then
    echo
    echo "Missing dependencies:"
    printf '  - %s\n' "${missing_packages[@]}"
    echo
    echo "Installing missing dependencies..."

    sudo apt update
    sudo apt install -y "${missing_packages[@]}"

    echo
    echo "[OK] Missing dependencies installed."
fi

# Ensure pipx applications are added to PATH
echo
echo "Configuring pipx..."
pipx ensurepath

# Install WineShield
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
echo

echo "Note:"
echo "If the 'wineshield' command is not found,"
echo "close and reopen your terminal, then try again."