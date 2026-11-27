# Gotchas

Format: symptom, cause, what to do. Add yours (they come from the error log).

- Symptom: `databricks` works in your terminal but not when the agent runs it. Cause: the agent runs each command in a fresh shell, so your exported profile is gone. What to do: pass `--profile <name>` in every command.
- Symptom: "invalid access token" after a while. Cause: OAuth tokens are short lived. What to do: `databricks auth login` again.
- Symptom: a test passes locally and fails in CI. Cause: different Python or package versions. What to do: pin versions in `requirements-dev.txt`.
