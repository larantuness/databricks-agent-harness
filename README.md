# Databricks agent harness (template)

A starter kit for doing data engineering on Databricks with an AI agent in VS Code. It gives the agent instructions, skills, roles and reusable prompts, and it makes the agent log its errors and improve the harness over time.

Individual and hands-on: your VS Code, your Databricks Free Edition, your GitHub repository.

## Quick start

1. Fork this repository to your GitHub account, then clone your fork and open it in VS Code.
2. Ask your agent: "Set up my environment following the `environment-setup` skill" (or run `/setup`). It checks your machine, shows what it will install and waits for your yes.
3. Delete the skill folders you do not need under `skills/` (`core` stays).
4. Follow `labs/00-setup.md`, then the labs in order.

## What is inside

- `AGENTS.md`: the rules every agent follows, including the improvement protocol.
- `skills/<tool>/`: procedures by tool (`core`, `databricks`, `github`).
- `agents/`: roles. `prompts/`: reusable commands (`/retro`, `/log-error`, `/new-skill`, `/memory-review`, `/start-story`, `/setup`).
- `docs/knowledge/`: error log, decision log, learnings.
- `.claude/` and `.github/`: generated copies for each tool. Edit the sources, then run `python scripts/sync_agent_folders.py`.
- `docs/`: architecture, options without paid Claude, shared team memory.

## Which agent can I use?

Genie Code (in Databricks), GitHub Copilot in VS Code, or Claude Code. See `docs/no-paid-claude.md`.

## Status

Written to be tested. Anything marked `from-docs` or `unverified` has not been run on every setup. Your job in the labs is to verify it and update the files.

Based on the structure of the public DataEngAgents repository (Fabric and Azure DevOps).
