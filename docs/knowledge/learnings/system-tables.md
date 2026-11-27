# Databricks system-table access

Status: verified

Last checked: 2026-11-27

Read-only access was confirmed by listing each table and running `SELECT 1 ... LIMIT 1`. No row values were retrieved.

Accessible billing tables:

- `system.billing.account_prices`
- `system.billing.attributed_usage`
- `system.billing.list_prices`
- `system.billing.usage`

Accessible Lakeflow tables:

- `system.lakeflow.job_run_timeline`
- `system.lakeflow.job_task_run_timeline`
- `system.lakeflow.job_tasks`
- `system.lakeflow.jobs`
- `system.lakeflow.pipeline_update_timeline`
- `system.lakeflow.pipelines`
- `system.lakeflow.zerobus_ingest`
- `system.lakeflow.zerobus_stream`

This records table visibility and query permission only; it does not establish that the tables contain rows or that their data is current.
