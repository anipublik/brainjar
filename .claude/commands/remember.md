---
description: File a fact into the brain without creating duplicates
argument-hint: the fact, in plain words
allowed-tools: Read, Glob, Grep, Edit, Write
---
File this into the brain: $ARGUMENTS

1. Pick the home. A topic goes in notes/, a person or company in people/,
   project status in projects/, a choice with a reason in DECISIONS.md,
   a lesson in LEARNINGS.md.
2. Grep for an existing file on the same subject. Append there if one exists.
   Create a new file only when nothing fits.
3. New files get a lowercase-with-hyphens name and frontmatter with
   description and updated. Bump updated on any file you touch.
4. Never rewrite old lines. If the new fact contradicts one, mark the old
   line "(superseded YYYY-MM-DD)" and add the new line under it.
5. Reply with one line: the path you touched and what you added.
