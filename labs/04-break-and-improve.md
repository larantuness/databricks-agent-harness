# Lab 04: break something, log it, improve the harness

The goal is to feel the loop in `docs/architecture.md`.

1. Cause an error on purpose: ask the agent to run a Databricks command without `--profile` in a new terminal, or paste a wrong host.
2. Make sure the agent creates an error file in `docs/knowledge/errors/`. If it does not, tell it to, and note that the instructions need a fix.
3. Repeat the same error once. The file's `seen` should become 2.
4. Run the `harness-improver` agent. It must propose a diff to a skill or to `AGENTS.md`.
5. Read the diff. Approve it, or ask for a smaller one.
6. Run `python scripts/sync_agent_folders.py`, commit on `harness/<topic>`, open a pull request.
7. Try the same task again. Does the agent now avoid the error?

Done when: an error file is marked `fixed-in-skill` and the agent behaves differently.
