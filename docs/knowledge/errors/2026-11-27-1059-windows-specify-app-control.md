---
date: 2026-11-27 10:59
area: environment-setup
status: open
seen: 4
---

# Windows blocked the installed Spec Kit executable

- Symptom: `specify version` failed with `Uma política de Controlo de Aplicações bloqueou este ficheiro`.
- Cause: unknown; Windows Application Control blocked the executable installed by `uv tool install specify-cli`.
- Fix: none yet. The package and executable were installed, but execution is blocked.
- Prevention: pause and ask the machine administrator for the approved source or application-control exception.
- Seen again: 2026-11-27, US00 environment verification still reports Spec Kit as an error after PATH refresh.
- Seen again: 2026-11-27, resuming US00 confirmed Spec Kit remains blocked by Application Control.
- Seen again: 2026-11-27, latest US00 environment check returned `Spec Kit error`; other tools passed.
