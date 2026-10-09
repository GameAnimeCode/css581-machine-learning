#!/usr/bin/env bash
# Create the course virtual environment (.venv) and install requirements.txt.
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

echo "Done. Activate with: source .venv/bin/activate"
