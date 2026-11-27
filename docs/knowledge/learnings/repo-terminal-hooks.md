# Repository terminal hooks

Status: unverified

Last checked: 2026-11-27

- A repository hook may deny a terminal tool call before the command runs.
- In that case, treat the command as blocked and do not substitute an unauthorized execution route or bypass the hook.
