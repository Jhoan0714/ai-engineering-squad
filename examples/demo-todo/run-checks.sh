#!/usr/bin/env bash
# Reference run-checks adapter for examples/demo-todo (Python + pytest).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  # shellcheck disable=SC1091
  source .venv/bin/activate
  pip install -q -r requirements.txt
else
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
pytest -q
