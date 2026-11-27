# Lab 02: first agent run

Open the agent chat in VS Code, in this folder. Try, in order:

1. "Read REPO_MAP.md and tell me which skill you would use to log in to Databricks." (checks that the agent finds our instructions)
2. "Using the databricks-cli-auth skill, check which user my profile `free` is. Show the command first." (read-only)
3. "List what is in my schema `<your_name>_agents`." (read-only)

Look for: did it read `AGENTS.md`? Did it propose the command instead of guessing? Did it use `--profile`?

If it ignored the instructions, that is your first error. Run `/log-error` and describe it.
