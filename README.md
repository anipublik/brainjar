# brainjar

A second brain your AI agents can actually read: plain markdown files, one map,
and a few scripts that keep it tidy. Works with Claude Code, Codex, Gemini CLI,
Cursor, Copilot, and your own bot.

## Quick start

1. Edit BRAIN.md and CORE.md. Delete the sample notes.
2. git init && cp scripts/pre-commit .git/hooks/pre-commit
3. Open the folder in Claude Code, Codex, Gemini CLI or Cursor. Each finds its own entry file.
4. Your own bot: pip install anthropic && python3 scripts/bot.py "question"

Full write-up on anisri.dev.
