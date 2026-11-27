# Windows CLI path after installation

Status: verified

Last checked: 2026-11-27

- In a PowerShell process that predates a CLI installation, refresh `$env:Path` from the machine and user environment values or open a new terminal before running the environment checker.
- On Windows, run the SQL wrapper with `py scripts/dbquery.py` from the repository root when `python` is not available as a command.
