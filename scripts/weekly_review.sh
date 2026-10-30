#!/usr/bin/env bash
# Headless weekly review. Works on a branch so you review a diff, not a surprise.
set -euo pipefail
cd "$(dirname "$0")/.."
branch="review/$(date +%F)"
git switch -c "$branch"

claude -p "$(cat prompts/weekly-review.md)" \
  --allowedTools "Read,Glob,Grep,Edit,Write,Bash(python3 scripts/build_index.py),Bash(python3 scripts/brain_lint.py)"

python3 scripts/build_index.py
python3 scripts/brain_lint.py
git add -A && git commit -qm "weekly review $(date +%F)" || echo "nothing to commit"
git switch -
echo "review ready on $branch: git diff main...$branch"
