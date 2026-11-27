---
date: 2026-11-27 10:50
area: repo-settings
status: open
seen: 1
---

# The repository terminal hook denied environment commands

- Symptom: `py scripts/check_environment.py` and the subsequent read-only Git command were denied by the preToolUse hook with `Denied by preToolUse hook from "repo settings" (hook errored)`.
- Cause: unknown; the hook or its configuration prevented the tool call before the command could run.
- Fix: none yet. The initialization stopped without bypassing the block.
- Prevention: provide the repository terminal hook with a functioning local execution policy, or add a verified read-only command path that the hook permits.
