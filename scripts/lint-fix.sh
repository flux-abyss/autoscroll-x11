#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo "Running lint auto-fix (YAPF)"
echo "========================================"

python3 -m yapf --style google --in-place --recursive autoscroll_x11 tests

echo ""
echo "========================================"
echo "Formatting applied."
echo "Now run: bash scripts/lint.sh"
echo "========================================"