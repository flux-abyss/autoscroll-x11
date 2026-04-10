#!/bin/sh
# scripts/install-local.sh — per-user install from the source tree.
#
# Installs to ~/.local without building a .deb.
# Use this for rapid local iteration.
# Re-run after any source change to update the installed copy.
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
INSTALL_LIB="$HOME/.local/lib/autoscroll-x11"
INSTALL_BIN="$HOME/.local/bin"
AUTOSTART_DIR="$HOME/.config/autostart"

install -d "$INSTALL_LIB" "$INSTALL_BIN" "$AUTOSTART_DIR"

# Copy the Python package.
rm -rf "$INSTALL_LIB/scroll_core"
cp -r "$REPO_ROOT/scroll_core" "$INSTALL_LIB/"

# Write the launcher.
cat > "$INSTALL_BIN/autoscroll-x11" << LAUNCHER
#!/usr/bin/python3
import sys
sys.path.insert(0, "$INSTALL_LIB")
from scroll_core.app import main
main()
LAUNCHER
chmod 0755 "$INSTALL_BIN/autoscroll-x11"

# Copy the autostart entry.
cp "$REPO_ROOT/data/autostart/autoscroll-x11.desktop" "$AUTOSTART_DIR/"

echo "Installed to $HOME/.local"
echo "Ensure $INSTALL_BIN is in PATH."
