# Decisions

## 2026-10-12 Moved per-folder lists into INDEX.md files
What: BRAIN.md lists folders only; scripts/build_index.py writes each INDEX.md.
Why: the map was eating 4k tokens every session for a list the agent read once.
Rejected: one giant index in BRAIN.md.

## 2026-10-20 BRAIN.md is the source, tool files are generated
What: CLAUDE.md, GEMINI.md and AGENTS.md come from scripts/sync_agents.sh.
Why: three hand-edited copies drifted within a week.
Rejected: symlinks (break on Windows checkouts and in some sync tools).
