<!-- Generated from BRAIN.md by scripts/sync_agents.sh. Edit BRAIN.md, not this file. -->

# Brain

Ani's personal knowledge base. You answer from these files, not from
your training data. If it is not written down here, it does not exist.

## Always loaded

<file path="CORE.md">
# Core

- Platform engineer. Thinks in reliability signals, cost, and blast radius.
- Writes in plain words. No em dashes, no filler.
- Prefers open standards and self-hosting over SaaS lock-in.
</file>


## Where things live
- notes/      one topic per file. Start at notes/INDEX.md
- people/     one card per person or company. Start at people/INDEX.md
- projects/   one file per project, with status. Start at projects/INDEX.md
- DECISIONS.md   what was decided and why, newest at the bottom
- LEARNINGS.md   lessons and post-mortems
- inbox/      raw drops waiting to be filed

## How to answer
1. Read the INDEX.md of the folder that fits, then open only the files you need.
2. Cite every claim as (path/file.md).
3. If nothing covers it, say "not in the brain" and stop. Do not guess.
4. If two files disagree, show both and say which is newer.

## How to write
- Append to an existing file before creating a new one. Search first.
- New file names: lowercase-with-hyphens.md, named after the subject.
- Every file starts with frontmatter: description, updated (YYYY-MM-DD).
  Projects also carry status (active, paused, done) and next.
- Never delete a line. Mark it "(superseded YYYY-MM-DD)" and add the new one.
- Decisions go in DECISIONS.md as "## YYYY-MM-DD title", then what, why, and what was rejected.
- Never store passwords, keys, tokens, or regulated data. Store where they live instead.
