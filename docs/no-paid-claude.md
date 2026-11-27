# No paid Claude? You can still do every lab

The harness is plain files (Markdown and a little YAML). Several tools read them.

| Option | Cost | Reads our files | Status |
|---|---|---|---|
| Genie Code (in the Databricks workspace) | Included with the workspace | Reads `AGENTS.md`/`CLAUDE.md` and skills in the workspace; skills only in agent mode | `from-docs`; test in lab 03 |
| GitHub Copilot in VS Code | A free plan exists, with monthly limits | `AGENTS.md`, `.github/copilot-instructions.md`, `.github/agents`, `.github/skills`, `.github/prompts` | `from-docs`; check current plan limits |
| Claude Code (VS Code extension or CLI) | Needs a paid Claude plan or API credits; the free Claude plan does not include it | `CLAUDE.md`, `.claude/` | `from-docs` |
| Any other agent that reads `AGENTS.md` | Varies | `AGENTS.md` | Not tested |

## What changes between them

- Slash commands: Claude Code uses `.claude/commands`; Copilot uses `.github/prompts`. Same prompts, generated for both.
- Hooks (the prod blocker) are a Claude Code feature. With other tools the guardrail is your dev-only profile and the pull request review.
- Quality of results differs by model. The workflow does not.

## Suggested path

1. Everyone: do labs 00, 01 and 02 (CLI, repo, first agent run).
2. Pick the agent you can use: Copilot (VS Code) or Genie Code, or Claude Code if you have it.
3. The labs use the words "your agent". Where a step is tool specific, the lab shows each variant.
