#!/usr/bin/env python3
"""A small agent that runs on bot.md and nothing else.

    pip install anthropic
    export ANTHROPIC_API_KEY=...
    python3 scripts/bot.py "what is the backup setup on the VPS?"
"""
import os
import sys
from pathlib import Path

import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brain_load import load  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MODEL = os.environ.get("BRAIN_MODEL", "claude-sonnet-5-5")
MAX_TURNS = 12


def safe(rel):
    p = (ROOT / rel).resolve()
    if ROOT not in p.parents and p != ROOT:
        raise ValueError("path is outside the brain")
    return p


def list_files(folder="."):
    return "\n".join(str(p.relative_to(ROOT)) for p in sorted(safe(folder).rglob("*.md")))


def read_file(path):
    return safe(path).read_text(encoding="utf-8")


def search(text):
    hits = []
    for p in sorted(ROOT.rglob("*.md")):
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if text.lower() in line.lower():
                hits.append(f"{p.relative_to(ROOT)}:{n}: {line.strip()}")
    return "\n".join(hits[:50]) or "no matches"


def append_fact(path, fact):
    p = safe(path)
    if p.suffix != ".md" or not p.exists():
        return "refused: append only to an existing .md file (create files by hand or via /remember)"
    with p.open("a", encoding="utf-8") as f:
        f.write(f"\n- {fact.strip()}")
    return f"appended to {path}"


HANDLERS = {f.__name__: f for f in (list_files, read_file, search, append_fact)}
TOOLS = [
    {"name": "list_files", "description": "List .md files under a folder of the brain.",
     "input_schema": {"type": "object", "properties": {"folder": {"type": "string"}}}},
    {"name": "read_file", "description": "Read one file, path relative to the brain root.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}},
    {"name": "search", "description": "Case-insensitive text search across every file.",
     "input_schema": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}},
    {"name": "append_fact", "description": "Append one bullet to an existing file.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}, "fact": {"type": "string"}},
                      "required": ["path", "fact"]}},
]


def ask(question):
    client = anthropic.Anthropic()
    system = load(ROOT / "bot.md")          # the map, with @imports inlined
    messages = [{"role": "user", "content": question}]
    for _ in range(MAX_TURNS):
        resp = client.messages.create(model=MODEL, max_tokens=2000, system=system,
                                      tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                try:
                    out = HANDLERS[block.name](**block.input)
                except Exception as e:  # hand the error back, let the model recover
                    out = f"error: {e}"
                results.append({"type": "tool_result", "tool_use_id": block.id, "content": out})
        messages.append({"role": "user", "content": results})
    return "stopped: too many tool calls"


if __name__ == "__main__":
    print(ask(" ".join(sys.argv[1:]) or "What is in the brain?"))
