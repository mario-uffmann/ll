#!/usr/bin/env sh
# Self-bootstrapping launcher: creates .venv on first run, then executes ll.py.
set -e

REPO="$(cd "$(dirname "$0")" && pwd)"
VENV="$REPO/.venv"
PY="$VENV/bin/python"

if [ ! -x "$PY" ]; then
    python3 -m venv "$VENV"
    "$PY" -m pip install --quiet --disable-pip-version-check -r "$REPO/requirements.txt"
fi

exec "$PY" "$REPO/ll.py" "$@"
