#!/usr/bin/env python3
"""PostToolUse hook for Write|Edit. If Claude just touched a brain file,
rebuild the indexes and lint. Exit code 2 sends stderr back to Claude
so it fixes its own mess before moving on."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
event = json.load(sys.stdin)
target = Path(event.get("tool_input", {}).get("file_path", ""))

if target.suffix != ".md" or ROOT not in target.resolve().parents:
    sys.exit(0)

here = Path(__file__).resolve().parent
subprocess.run([sys.executable, str(here / "build_index.py")], check=False)
lint = subprocess.run([sys.executable, str(here / "brain_lint.py")], capture_output=True, text=True)
if lint.returncode != 0:
    print("Brain lint failed after your edit. Fix these:\n" + lint.stderr, file=sys.stderr)
    sys.exit(2)
