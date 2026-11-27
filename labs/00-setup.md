# Lab 00: setup

You need Git, VS Code, a GitHub account, a Databricks Free Edition workspace and an agent (see `docs/no-paid-claude.md`).

1. Fork this repository to your GitHub account. A fork of a public repository is public: never commit credentials or private notes.
2. Clone your fork and open it in VS Code:
   ```
   git clone https://github.com/<you>/<your-fork>
   cd <your-fork>
   code .
   ```
   If `code` is not found, use File, Open Folder in VS Code.
3. Open your agent chat and ask: "Set up my environment following the `environment-setup` skill." In Claude Code or Copilot you can run `/setup`. Read the plan before you say yes.
4. Run the logins yourself when the agent asks. Never paste a token into the chat.
5. Check that `gh repo set-default --view` shows **your fork**, and that Issues and Actions are enabled in it.
6. Delete the skill folders you do not need. Keep `skills/core`. Then run `python scripts/sync_agent_folders.py`.
7. Commit on a branch and open a pull request inside your fork. CI should pass.

Done when: `python scripts/check_environment.py` reports all tools, and tests, lint and CI are green. If a tool is blocked on your machine, record it with `/log-error` and tell the instructor.
