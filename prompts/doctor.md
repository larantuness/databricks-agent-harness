---
description: Read-only health check of tools, logins and the Databricks workspace.
---

Run a read-only health check. Change nothing. Do not stop at the first failure.

1. `python scripts/check_environment.py`.
2. GitHub: `gh auth status` (is the `project` scope there?) and `gh repo set-default --view` (is it my fork?).
3. Databricks: `databricks auth profiles`, then `databricks current-user me --profile free`. Never use `--sensitive` with any auth command.
4. SQL: `python scripts/dbquery.py "SELECT 1"`.

Report a short table: check, result (`ok`, `failed`, `unknown`), what to do. Show no tokens, workspace addresses or user names. To fix something, point to `INIT.md` or the matching skill.
