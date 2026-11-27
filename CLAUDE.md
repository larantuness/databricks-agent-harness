@AGENTS.md

# Claude Code notes

- Hooks live in `.claude/hooks/` and are registered in `.claude/settings.json`. `block_prod.py` blocks prod targets, force pushes and direct pushes to main.
- Skills, agents and commands in `.claude/` are generated. Edit `skills/`, `agents/` and `prompts/` and run `python scripts/sync_agent_folders.py`.
- Slash commands come from `prompts/` (for example `/retro`, `/new-skill`).
