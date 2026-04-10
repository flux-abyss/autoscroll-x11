#!/bin/sh
# install-local.sh — install autoscroll-x11 for the current user only.
# This does NOT build a .deb; use `dpkg-buildpackage` for that.
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL_LIB="$HOME/.local/lib/autoscroll-x11"
INSTALL_BIN="$HOME/.local/bin"
AUTOSTART_DIR="$HOME/.config/autostart"

echo "Installing autoscroll-x11 to $HOME/.local ..."

install -d "$INSTALL_LIB" "$INSTALL_BIN" "$AUTOSTART_DIR"

cp -r "$REPO_ROOT/autoscroll_x11" "$INSTALL_LIB/"

# Write a per-user launcher that points at the local lib.
cat > "$INSTALL_BIN/autoscroll-x11" << EOF
#!/usr/bin/python3
import sys
sys.path.insert(0, "$INSTALL_LIB")
from autoscroll_x11.app import main
main()
EOF
chmod 0755 "$INSTALL_BIN/autoscroll-x11"

cp "$REPO_ROOT/data/autostart/autoscroll-x11.desktop" "$AUTOSTART_DIR/"

echo "Done. Make sure $INSTALL_BIN is in your PATH."
echo "Run: autoscroll-x11 --tray"
