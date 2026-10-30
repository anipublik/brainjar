#!/usr/bin/env python3
"""Keep the brain honest. Errors exit 1, warnings only print."""
import difflib
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_index import FOLDERS, ROOT, frontmatter  # noqa: E402
from brain_load import IMPORT  # noqa: E402

NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")
MAP_LINE_BUDGET = 200
STALE_AFTER = timedelta(days=30)


def lint():
    errors, warnings = [], []
    for folder in FOLDERS:
        files = [f for f in sorted((ROOT / folder).glob("*.md")) if f.name != "INDEX.md"]
        stems = [f.stem for f in files]
        for f in files:
            rel = f.relative_to(ROOT)
            meta = frontmatter(f)
            if not NAME.match(f.name):
                errors.append(f"{rel}: name must be lowercase-with-hyphens.md")
            if "description" not in meta:
                errors.append(f"{rel}: missing 'description' in frontmatter")
            twins = difflib.get_close_matches(f.stem, [s for s in stems if s != f.stem], n=1, cutoff=0.88)
            if twins and f.stem < twins[0]:
                warnings.append(f"{rel}: looks like a duplicate of {folder}/{twins[0]}.md")
            if folder == "projects" and meta.get("status") == "active":
                try:
                    if date.today() - date.fromisoformat(meta.get("updated", "")) > STALE_AFTER:
                        warnings.append(f"{rel}: active but not updated in 30+ days")
                except ValueError:
                    errors.append(f"{rel}: active project needs 'updated: YYYY-MM-DD'")

    brain = ROOT / "BRAIN.md"
    if brain.exists():
        lines = brain.read_text(encoding="utf-8").splitlines()
        if len(lines) > MAP_LINE_BUDGET:
            warnings.append(f"BRAIN.md is {len(lines)} lines; budget is {MAP_LINE_BUDGET}")
        in_fence = False
        for n, line in enumerate(lines, 1):
            if line.lstrip().startswith(("```", "~~~")):
                in_fence = not in_fence
            if in_fence:
                continue
            for part in line.split("`")[::2]:
                for m in IMPORT.finditer(part):
                    if not (ROOT / m.group(1)).expanduser().exists():
                        errors.append(f"BRAIN.md:{n}: broken import @{m.group(1)}")
    else:
        errors.append("BRAIN.md is missing")
    return errors, warnings


if __name__ == "__main__":
    errors, warnings = lint()
    for w in warnings:
        print("warn ", w)
    for e in errors:
        print("error", e, file=sys.stderr)
    sys.exit(1 if errors else 0)
