#!/bin/sh
# install-local.sh — per-user install mirroring the Debian layout.
# Does NOT build a .deb; use dpkg-buildpackage for that.
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL_LIB="$HOME/.local/lib/autoscroll-x11"
INSTALL_BIN="$HOME/.local/bin"
AUTOSTART_DIR="$HOME/.config/autostart"

install -d "$INSTALL_LIB" "$INSTALL_BIN" "$AUTOSTART_DIR"

cp -r "$REPO_ROOT/autoscroll_x11" "$INSTALL_LIB/"

cat > "$INSTALL_BIN/autoscroll-x11" << SCRIPT
#!/usr/bin/python3
import sys
sys.path.insert(0, "$INSTALL_LIB")
from autoscroll_x11.app import main
main()
SCRIPT
chmod 0755 "$INSTALL_BIN/autoscroll-x11"

cp "$REPO_ROOT/data/autostart/autoscroll-x11.desktop" "$AUTOSTART_DIR/"

echo "Installed to $HOME/.local"
echo "Make sure $INSTALL_BIN is in your PATH."
