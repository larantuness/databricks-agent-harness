# Free Edition: system tables

Status: `verified` for access on one workspace (reported by the repository owner, SQL editor, `SELECT ... LIMIT 5`)
Last checked: 2026-11-27

| Table | Result |
|---|---|
| `system.lakeflow.pipelines` | query worked |
| `system.lakeflow.job_task_run_timeline` | query worked |
| `system.lakeflow_pipeline_events_preview.pipeline_events` (Beta) | query worked |
| `system.billing.usage` | query worked |
| `system.billing.list_prices` | query worked |
| `system.lakeflow.pipeline_update_timeline` | failed: no access or table not found (cause not confirmed) |

- `SHOW TABLES IN system.lakeflow` listed `jobs`, `job_tasks`, `job_run_timeline`, `job_task_run_timeline` and `pipelines`; `pipeline_update_timeline` is not listed (`verified`).
- `pipeline_events` contains runs from this workspace: `update_progress` gives run history, and some `flow_progress` events carry expectation results and `num_output_rows`. Not every `flow_progress` event has them (`verified`).
- `system.billing.usage` has pipeline usage with `usage_metadata.dlt_pipeline_id` (`verified`). Attribution to jobs is `unverified`.
- The user is not an admin of the system tables on this workspace.
- This does not show that the data is complete, or how long new runs take to appear (`unverified`).
- Other workspaces may differ. Test before relying on a table.
