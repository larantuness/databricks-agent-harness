---
description: Create a new skill from a task we repeated.
---

Create a skill for: $ARGUMENTS

1. Pick the group folder under `skills/` (`core`, `databricks`, `github`, or a new tool folder). Name the skill in kebab-case.
2. Write `skills/<group>/<name>/SKILL.md` with frontmatter `name` and a `description` that says when to use it. Keep the body under about 60 lines: steps, rules, typical errors.
3. Use only facts we verified or documented. Mark the rest `from-docs` or `unverified`.
4. Add it to `REPO_MAP.md`.
5. Run `python scripts/quick_validate.py skills/<group>/<name>`, `python scripts/sync_agent_folders.py` and `python scripts/check_repo_map.py`.
6. Show me the diff before committing.
