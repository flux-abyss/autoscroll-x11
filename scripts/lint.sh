#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo "Running lint checks (STRICT MODE)"
echo "========================================"

echo ""
echo "==> YAPF (format check)"
python3 -m yapf --style google --diff --recursive autoscroll_x11 tests

echo ""
echo "==> Flake8 (style + errors)"
python3 -m flake8 autoscroll_x11 tests

echo ""
echo "==> Pylint (static analysis)"
python3 -m pylint autoscroll_x11

echo ""
echo "==> Compile check (syntax validation)"
python3 -m compileall autoscroll_x11 tests

echo ""
echo "========================================"
echo "All lint checks passed cleanly"
echo "========================================"