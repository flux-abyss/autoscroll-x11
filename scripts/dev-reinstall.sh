#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if pgrep -x autoscroll-x11 >/dev/null 2>&1; then
  echo "Stopping running autoscroll-x11..."
  pkill -x autoscroll-x11 || true
  sleep 1
fi

echo "========================================"
echo "Building Debian package"
echo "========================================"
dpkg-buildpackage -us -uc -b

DEB_FILE="$(ls -1 ../autoscroll-x11_*_all.deb | sort | tail -n1)"

echo ""
echo "========================================"
echo "Installing package (deferred triggers)"
echo "========================================"
sudo dpkg -i --no-triggers "$DEB_FILE"

echo ""
echo "Installed: $DEB_FILE"
echo ""
echo "Note:"
echo "  Deferred trigger processing is normal during rapid iteration."
echo "  To process pending triggers later, run:"
echo "    sudo dpkg --configure -a"
echo ""
echo "Run:"
echo "  autoscroll-x11 --tray"
echo "========================================"
