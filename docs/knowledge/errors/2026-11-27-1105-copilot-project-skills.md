---
date: 2026-11-27 11:05
area: databricks-official-skills
status: open
seen: 1
---

# GitHub Copilot rejects project-scoped Databricks skills

- Symptom: `databricks aitools install --scope project --agents copilot --skills-only ...` skipped GitHub Copilot and returned `does not support project-scoped skills`.
- Cause: the installed Databricks CLI 1.28.0 reports that GitHub Copilot supports skills only in global scope.
- Fix: none without a scope change. No global installation was performed because project initialization rules require project scope.
- Prevention: update the official-skills procedure to distinguish GitHub Copilot project support, and ask before any global installation.
