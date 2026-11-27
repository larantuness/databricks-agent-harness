---
name: databricks-bundles-dev
description: Use when defining or deploying Databricks Asset Bundles (Declarative Automation Bundles) for jobs, pipelines, dashboards or apps. Enforces a dev target only with validate and plan before deploy.
---

# Asset Bundles, dev only

Status: `from-docs`; the commands exist in CLI 1.28.0. `bundle validate` was `verified` on this repository (2026-11-27). For resource syntax use the official skill `databricks-dabs` (skill `databricks-official-skills`); these rules win over it.

## Rules

- `databricks.yml` defines one target: `dev`, with `mode: development`. Do not add a production target in this repository, even if an official example shows one.
- Pass `--profile` and `-t dev` explicitly.
- Order, every time:
  1. `databricks bundle validate --strict -t dev`
  2. `databricks bundle plan -t dev`: shows what would be created, changed or deleted, without changing anything. This is the dry run of skill `write-contract`.
  3. Show the plan and wait for a yes. If it deletes or recreates something, name each object.
  4. `databricks bundle deploy -t dev`
  5. Run what needs running: `databricks bundle run <resource> -t dev`. For an app, deploy alone does not restart it.
- Never destroy the bundle. A human does that.
- Bundle variables hold catalog, schema and warehouse; do not hardcode them. No workspace host in the file: it comes from the profile.
- Keep resources in `resources/`, one file per resource, named `<name>.<type>.yml`.
- App names are shared by the whole workspace: include the user in the name, keep it to 30 characters or fewer, lowercase letters, digits and hyphens. Check the resolved name in the validate output: validation does not catch every bad name (`from-docs`, official `databricks-dabs` skill).

## Common problems

- Validation error about a missing field: read the message, fix the YAML, validate again.
- Permission error on create: you are probably not using the right profile. Check `databricks current-user me`.
- Free Edition may not support every resource type. Test one small resource first and record the result.
