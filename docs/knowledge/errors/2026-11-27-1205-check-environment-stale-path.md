---
date: 2026-11-27 12:05
area: environment-setup
status: open
seen: 1
---

# Environment verification inherited a stale PATH

- Symptom: `py scripts/check_environment.py` reported the Databricks CLI and GitHub CLI as missing although both had been installed and their versions had previously been verified.
- Cause: likely the PowerShell process did not inherit the updated machine/user PATH after installation.
- Fix: refreshed the process PATH from machine and user environment values; the verifier then found both CLIs and uv.
- Prevention: after installing command-line tools, refresh or reopen the terminal before running the environment verifier.
