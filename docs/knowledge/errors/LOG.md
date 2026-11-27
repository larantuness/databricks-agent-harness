# Error log (history format)

New errors go in one file each in this folder (see skill `self-improvement`). This file only keeps older entries; do not add to it.
Do not store secrets or personal data here.

Example of an entry in the old format:

## example · fixed
- Symptom: `databricks: command not found` right after installing the CLI.
- Cause: the terminal was opened before the install, so PATH was stale.
- Fix: open a new terminal.
- Prevention: `skills/databricks/databricks-cli-auth` lists it under typical errors.
