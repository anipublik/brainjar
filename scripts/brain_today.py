#!/usr/bin/env python3
"""SessionStart hook: print a short briefing. Claude Code adds
whatever this prints to the session's context."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_index import ROOT, frontmatter  # noqa: E402

print("## Today's brain briefing")
for f in sorted((ROOT / "projects").glob("*.md")):
    meta = frontmatter(f)
    if meta.get("status") == "active":
        print(f"- projects/{f.name}: next = {meta.get('next', 'not set')}")

log = ROOT / "DECISIONS.md"
if log.exists():
    heads = [l for l in log.read_text(encoding="utf-8").splitlines() if l.startswith("## ")]
    if heads:
        print("\nLast decisions:")
        for h in heads[-3:]:
            print("-", h[3:])

inbox = [p.name for p in (ROOT / "inbox").glob("*") if p.is_file()]
if inbox:
    print(f"\n{len(inbox)} item(s) waiting in inbox/. Offer to file them.")
