# Error log

Append only. Newest at the bottom. Format and rules: skill `self-improvement`.
Do not store secrets or personal data here.

Entry template:

```
## YYYY-MM-DD HH:MM · <skill or area> · <open|fixed>
- Symptom:
- Cause:
- Fix:
- Prevention: (which file should change)
- Status: open | fixed-in-skill | wont-fix
- Seen: 1
```

---

## 2026-11-27 00:00 · example · fixed
- Symptom: `databricks: command not found` right after installing the CLI.
- Cause: the terminal was opened before the install, so PATH was stale.
- Fix: open a new terminal.
- Prevention: `skills/databricks/databricks-cli-auth` lists it under typical errors.
- Status: fixed-in-skill
- Seen: 1

## 2026-11-27 12:00 · environment-setup · open
- Symptom: `uv tool install specify-cli` failed: `Failed to fetch: https://pypi.org/simple/specify-cli/ ... Connection refused`.
- Cause: the machine's hosts file points the public package index to 127.0.0.1. It looks like an intentional block on a managed machine (inferred).
- Fix: none yet. Not bypassed. Needs an approved package source from whoever manages the machine.
- Prevention: `skills/core/environment-setup` tells the agent to stop and report blocks, never bypass them.
- Status: open
- Seen: 1

## 2026-11-27 12:30 · harness-scripts · open
- Symptom: `python scripts/quick_validate.py <skill>` failed with `ModuleNotFoundError: No module named 'yaml'`.
- Cause: PyYAML is not installed. It is not listed in `requirements-dev.txt`, and the package index is unreachable on this machine.
- Fix: none yet.
- Prevention: add `pyyaml` to `requirements-dev.txt` (needs approval). `skills/core/environment-setup` already installs it explicitly.
- Status: open
- Seen: 1

## 2026-11-27 13:00 · environment-setup · fixed
- Symptom: follow-up to the two open entries of 2026-11-27 (package index unreachable, `yaml` module missing).
- Cause: same as in those entries.
- Fix: the machine owner allowed the package index. `uv tool install specify-cli` worked (1.4.5); dev requirements and pyyaml installed in `.venv`; skill validation passed. `pyyaml` is still not listed in `requirements-dev.txt`.
- Prevention: add `pyyaml` to `requirements-dev.txt` (needs approval).
- Status: open
- Seen: 1

## 2026-11-27 14:00 · databricks-cli-auth · fixed
- Symptom: `databricks auth login` failed with `lookup dbc-xxxxxxxx-xxxx: no such host`.
- Cause: only the first part of the workspace address was given as host, without the domain. The skill did not say how to find the host.
- Fix: use the full address, `https://dbc-xxxxxxxx-xxxx.cloud.databricks.com`.
- Prevention: `skills/databricks/databricks-cli-auth` explains how to find the host and lists the error.
- Status: fixed-in-skill
- Seen: 1

## 2026-11-27 15:00 · databricks-sql-query · fixed
- Symptom: the user had to run SQL checks by hand and paste the results; the harness had no way for the agent to query Databricks.
- Cause: no skill or agent covered querying.
- Fix: added skill `databricks-sql-query`, agent `data-analyst` and `scripts/dbquery.py` (read-only).
- Prevention: `AGENTS.md` now tells agents to query instead of guessing.
- Status: fixed-in-skill
- Seen: 1

## 2026-11-27 15:10 · tests · fixed
- Symptom: plain `pytest` failed with `ModuleNotFoundError: No module named 'scripts'` (and the same for `src`), while `python -m pytest` passed.
- Cause: the repository root was not on the import path. CI runs plain `pytest`.
- Fix: `pythonpath = ["."]` in `pyproject.toml`.
- Prevention: run tests with the same command as CI.
- Status: fixed-in-skill
- Seen: 1
