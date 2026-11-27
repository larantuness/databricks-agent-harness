# Lab 01: connect to Databricks

1. Install the Databricks CLI (official instructions for your OS). Check `databricks --version`.
2. Log in with OAuth using the host of your Free Edition workspace:
   ```
   databricks auth login --host https://<your-workspace-host> --profile free
   databricks current-user me --profile free
   ```
3. Put the host into `databricks.yml`.
4. Create your own schema (in the workspace SQL editor): `CREATE SCHEMA IF NOT EXISTS <your_catalog>.<your_name>_agents;`
5. Write what worked and what did not in `docs/knowledge/learnings/free-edition.md`.

Never paste a token anywhere. If the login fails, log it with `/log-error` and read `skills/databricks/databricks-cli-auth`.
