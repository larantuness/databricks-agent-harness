---
date: 2026-11-27 13:38
area: skill-validation
status: open
seen: 1
---

# Skill validation used a Python without PyYAML

- Symptom: both `py scripts/quick_validate.py ...` runs failed with `ModuleNotFoundError: No module named 'yaml'`.
- Cause: the Windows `py` launcher selected the global interpreter, while PyYAML is installed in the repository virtual environment.
- Fix: reran both validators with `.venv\Scripts\python.exe`; both passed without installing dependencies.
- Prevention: run project validation scripts with the repository virtual environment's Python on Windows.
