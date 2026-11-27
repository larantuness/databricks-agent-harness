---
date: 2026-11-27 11:58
area: databricks-sql-query
status: open
seen: 2
---

# Data analyst could not find the Python command

- Symptom: the delegated read-only query attempt failed with `Python was not found` and `databricks` was not recognized.
- Cause: the agent invoked global `python`/`databricks` commands without using the Windows `py` launcher or the existing project virtual environment and refreshed PATH.
- Fix: the coordinator completed the approved read-only queries using `py scripts/dbquery.py`; the delegated agent did not execute SQL. The skill and agent instructions still need a Windows-specific command.
- Prevention: run read-only SQL through `py scripts/dbquery.py` from the repository root, and use the repository's existing `.venv` or refresh PATH when needed.
- Seen again: 2026-11-27, notebook-engineer used the existing `.venv` after the global `python` command was unavailable.
