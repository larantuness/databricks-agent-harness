# REPO_MAP

Start here. Everything an agent can use is listed below. Keep this file in sync with `python scripts/check_repo_map.py`.

## Instruction files

- `AGENTS.md`: rules for every agent (single source).
- `CLAUDE.md`: imports `AGENTS.md`, adds Claude Code notes.
- `.github/copilot-instructions.md`: points Copilot to `AGENTS.md`.

## Agents (`agents/`)

| Agent | Use it for |
|---|---|
| `requirements-analyst` | Turn an idea into user stories and acceptance criteria as GitHub issues |
| `pipeline-engineer` | Build and test Lakeflow / Spark Declarative Pipelines and transformation code |
| `notebook-engineer` | Develop notebooks and Python modules locally, keep them testable |
| `docs-writer` | Write and refresh living documentation from the code |
| `reviewer` | Review a branch or pull request against the rules and tests |
| `harness-improver` | Read the error log, find repeated problems, propose edits to instructions, skills and agents |

## Skills (`skills/<group>/<name>/SKILL.md`)

Grouped by tool. Delete the groups you do not use.

| Group | Skill | What it covers |
|---|---|---|
| core | `environment-setup` | Check and install the tools, logins, fork settings |
| core | `self-improvement` | The error log, learnings and the improvement loop |
| core | `repo-orientation` | How to find your way around this repository |
| core | `write-contract` | Dry-run-first rule for anything that writes |
| databricks | `databricks-cli-auth` | Install the CLI, OAuth login, profiles |
| databricks | `databricks-free-edition` | What works and what does not on Free Edition |
| databricks | `databricks-pipelines` | Declarative pipelines and medallion layers |
| databricks | `databricks-bundles-dev` | Asset Bundles with a dev target only |
| github | `github-issues-flow` | Issues as stories, labels, branches |
| github | `github-pr-flow` | Branch, commit, pull request, CI |

## Prompts (`prompts/`)

| Prompt | Use it for |
|---|---|
| `setup` | Check this machine and install the tools the labs need |
| `retro` | End-of-task review: log errors, update skills |
| `log-error` | Record one error in the log right now |
| `new-skill` | Create a new skill from a repeated task |
| `memory-review` | Clean the knowledge files, mark stale entries |
| `start-story` | Take a GitHub issue from "To do" to a branch with a plan |

## Knowledge (`docs/knowledge/`)

- `docs/knowledge/errors/LOG.md`, `docs/knowledge/decisions/LOG.md`, `docs/knowledge/learnings/`.

## Docs and labs

- `docs/architecture.md`, `docs/no-paid-claude.md`, `docs/shared-memory.md`, `docs/gotchas/databricks.md`.
- `labs/README.md` lists labs 00 to 06.

## Scripts

- `scripts/check_environment.py` (read-only tool check), `scripts/sync_agent_folders.py`, `scripts/check_repo_map.py`, `scripts/quick_validate.py`.
