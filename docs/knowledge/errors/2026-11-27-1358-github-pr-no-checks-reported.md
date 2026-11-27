---
date: 2026-11-27 13:58
area: github-pr-flow
status: open
seen: 1
---

# GitHub reported no checks for the new pull request

- Symptom: `gh pr checks 19 --watch` returned `no checks reported` and exit code 1 after the PR was created. The Actions API listed zero workflows and returned 404 for `ci.yml`, although the workflow file is present on `main`.
- Cause: unknown; the GitHub Actions run may not have been queued or associated yet.
- Fix: none yet.
- Prevention: inspect the PR's workflow runs and report CI as unverified when no checks are available; do not infer success.
