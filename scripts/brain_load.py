#!/usr/bin/env python3
"""Flatten a markdown map and its @imports into one prompt.

Follows the same rules Claude Code uses: relative, absolute or ~ paths,
at most 5 hops deep, and nothing inside code fences or `inline code`.
Only .md targets are expanded, so emails and @handles are left alone.
"""
import re
import sys
from pathlib import Path

MAX_DEPTH = 5
IMPORT = re.compile(r"(?<![\w`])@((?:~/|\.{1,2}/|/)?[\w./-]+\.md)\b")


def load(path, depth=0, seen=frozenset()):
    path = Path(path).expanduser().resolve()
    if path in seen:
        return f"<!-- skipped {path.name}: import cycle -->"
    if depth > MAX_DEPTH:
        return f"<!-- skipped {path.name}: more than {MAX_DEPTH} hops -->"
    seen = seen | {path}
    out, in_fence = [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
        if in_fence or "@" not in line:
            out.append(line)
            continue
        parts = line.split("`")          # odd indexes are inline code
        for i in range(0, len(parts), 2):
            parts[i] = IMPORT.sub(lambda m: _expand(m, path, depth, seen), parts[i])
        out.append("`".join(parts))
    return "\n".join(out)


def _expand(match, parent, depth, seen):
    target = Path(match.group(1)).expanduser()
    if not target.is_absolute():
        target = parent.parent / target
    if not target.exists():
        return f"{match.group(0)} (missing)"
    body = load(target, depth + 1, seen)
    return f'\n<file path="{match.group(1)}">\n{body}\n</file>\n'


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: brain_load.py MAP.md > prompt.txt")
    print(load(sys.argv[1]))
