---
name: databricks-pipelines
description: Use when building bronze, silver and gold tables with Spark Declarative Pipelines (Lakeflow) or plain PySpark/SQL notebooks, including naming, data quality expectations and tests.
---

# Pipelines and medallion layers

Status: `from-docs`. Confirm syntax in the official docs before generating code; names have changed across releases.

## Layers

- bronze: raw data as received, plus load metadata. No business rules.
- silver: cleaned, typed, deduplicated. One table per entity.
- gold: business-ready tables for a question or a dashboard.

## Rules

- Put transformation logic in plain Python functions under `src/` that take a DataFrame and return a DataFrame. The pipeline or notebook only wires them. That makes them unit-testable without a cluster.
- Every function has a test in `tests/` with a tiny in-memory input.
- Add data quality checks (expectations) for keys, nulls and ranges. A failing check must be visible, not silent.
- Name tables `<layer>_<entity>`, for example `silver_orders`.
- Do not hardcode catalog or schema. Take them from a bundle variable or widget.
- Write the table list and column meaning in `docs/` as you build, not at the end.

## Workflow

1. Specify the table (grain, keys, source, rules) in the issue.
2. Write the test first, then the function.
3. Wire it into the pipeline or notebook.
4. Validate with a dry run (skill `write-contract`), run in dev, check row counts.
5. Log anything that surprised you (skill `self-improvement`).
