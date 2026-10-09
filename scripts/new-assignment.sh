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

# Rewrite the list between the markers in README.md from the assignment folders.
update_readme() {
  local readme="README.md" start="<!-- assignments:start -->" end="<!-- assignments:end -->"
  if ! grep -qF "$start" "$readme" || ! grep -qF "$end" "$readme"; then
    echo "warning: assignment markers not found in $readme, skipping index update" >&2
    return
  fi
  local list
  list="$(mktemp)"
  find assignments -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort -V \
    | sed 's|.*|- [&](assignments/&)|' > "$list"
  awk -v s="$start" -v e="$end" -v f="$list" '
    $0 == s { print; while ((getline line < f) > 0) print line; skip = 1; next }
    $0 == e { skip = 0 }
    !skip   { print }' "$readme" > "$readme.tmp"
  mv "$readme.tmp" "$readme"
  rm -f "$list"
}

mkdir -p "$dest/src"
cp templates/writeup/writeup.qmd templates/writeup/preamble.tex "$dest/"
cp templates/code/main.py "$dest/src/"

update_readme

echo "Created $dest"
