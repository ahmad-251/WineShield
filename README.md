# WineShield

WineShield is a command-line tool for managing and running Windows applications through Wine.

The project is currently in an early development stage.

## Features

Current commands:

- `wineshield wine` — Pass arguments directly to Wine.
- `wineshield run` — Run a Windows application by name.
- `wineshield list` — Show applications known to WineShield.
- `wineshield update-appslist` — Scan the Wine registry and update the local application list.

## Requirements

WineShield currently requires:

- Linux
- Python 3
- Wine
- pipx

On Ubuntu/Debian:

```bash
sudo apt update
sudo apt install wine pipx
pipx ensurepath