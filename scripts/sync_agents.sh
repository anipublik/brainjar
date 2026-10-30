#!/usr/bin/env bash
# One source of truth (BRAIN.md), one entry file per tool.
# Run after editing BRAIN.md, or let the pre-commit hook do it.
set -euo pipefail
cd "$(dirname "$0")/.."
banner='<!-- Generated from BRAIN.md by scripts/sync_agents.sh. Edit BRAIN.md, not this file. -->'

# Claude Code and Gemini CLI resolve @imports themselves, so a pointer is enough.
printf '%s\n\n@BRAIN.md\n' "$banner" > CLAUDE.md
printf '%s\n\n@./BRAIN.md\n' "$banner" > GEMINI.md

# Codex, Cursor, Copilot and most others read AGENTS.md but do not expand
# @imports, so they get one flattened file with everything inlined.
{ echo "$banner"; echo; python3 scripts/brain_load.py BRAIN.md; } > AGENTS.md

echo "synced: CLAUDE.md GEMINI.md AGENTS.md"
