#!/bin/bash
set -e

sudo apt update
sudo apt install -y firejail wine xserver-xephyr

echo "WineShield sandbox dependencies installed."
echo "Verify: firejail --version && wine --version"
