#!/bin/sh
# scripts/build-deb.sh — build the Debian package from the source tree.
#
# Run from the project root or any subdirectory.
# The resulting .deb is written to the parent directory of the project root.
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

dpkg-buildpackage -us -uc -b

echo ""
echo "Package built. To install:"
echo "  sudo dpkg -i ../autoscroll-x11_*.deb"
echo ""
echo "If dpkg reports deferred triggers, that is normal."
echo "System triggers (icon cache, desktop database) run in the background"
echo "or can be completed immediately with:"
echo "  sudo dpkg --configure -a"
