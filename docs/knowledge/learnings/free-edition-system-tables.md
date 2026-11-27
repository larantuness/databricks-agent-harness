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

- The user is not an admin of the system tables on this workspace.
- A working query does not show that the data is complete or that our own runs will appear. `unverified` until a pipeline has run.
- Other workspaces may differ. Test before relying on a table.
- For pipeline run history, try the `update_progress` events in `pipeline_events` (`unverified`).
