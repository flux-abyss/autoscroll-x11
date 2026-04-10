#!/bin/sh
# scripts/run-dev.sh — launch autoscroll-x11 directly from the source tree.
set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

export AUTOSCROLL_DEBUG="${AUTOSCROLL_DEBUG:-1}"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

exec python3 -m scroll_core "$@"
