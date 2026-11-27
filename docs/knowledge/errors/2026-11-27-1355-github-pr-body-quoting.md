---
date: 2026-11-27 13:55
area: github-pr-flow
status: open
seen: 1
---

# PowerShell split the multiline pull request body

- Symptom: `gh pr create --body $body` rejected pieces of the multiline body as unknown arguments.
- Cause: PowerShell's native command argument handling did not pass the multiline value as one argument.
- Fix: used `gh pr create --body-file <path>` successfully for US00 PR #19.
- Prevention: pass multiline pull request bodies with `gh pr create --body-file <path>` from Windows PowerShell.
