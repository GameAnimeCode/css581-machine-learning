#!/usr/bin/env bash
# Create assignments/<name>/ from the templates.
# Usage: scripts/new-assignment.sh a1-linear-regression
set -euo pipefail
cd "$(dirname "$0")/.."

name="${1:?usage: $0 <assignment-name>}"
dest="assignments/$name"

if [[ -e "$dest" ]]; then
  echo "error: $dest already exists" >&2
  exit 1
fi

mkdir -p "$dest/src"
cp templates/writeup/writeup.qmd templates/writeup/preamble.tex "$dest/"
cp templates/code/main.py "$dest/src/"

echo "Created $dest"
