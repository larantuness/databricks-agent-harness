---
name: environment-setup
description: Use when someone has just cloned or forked this repository, asks to install or set up the tools, runs /setup, or a required command such as databricks, gh, uv or specify is not found. Checks the machine, installs only what is missing after approval, and verifies the result.
---

# Environment setup

Goal: leave the student's machine ready for the labs. Commands are `from-docs` (official install pages, read 2026-11-27) unless marked otherwise.

## Rules

1. **Check before installing.** Install only what is missing or too old.
2. **Show the plan and wait for a yes** (skill `write-contract`): tools, exact commands, and whether any needs admin rights.
3. **Never bypass a block.** If a download is refused, or a hosts file, proxy, certificate or company policy stops it, stop. Do not edit the hosts file, switch to another mirror, disable certificate checks or fetch the same package another way. Report the exact error and tell the student to ask whoever manages the machine for the approved source. On Windows, if Application Control blocks an installed executable, do not retry it through another launcher or path; ask the administrator for an approved resolution.
4. **The student does every login.** Browser sign-ins and secrets are never typed into the chat, and you never print or store tokens.
5. **Admin rights:** if a command needs `sudo` or an administrator prompt, give it to the student to run.
6. **One tool at a time.** Verify each before the next. Log every failure (skill `self-improvement`).

## 1. Check the machine (read-only)

```
python3 scripts/check_environment.py      # Windows: py scripts/check_environment.py
```

If Python is not available yet, run `git --version`, `databricks -v`, `gh --version` and `uv --version`. Do not run Spec Kit as part of US00.

| Tool | Needed for | Minimum |
|---|---|---|
| git | everything | any recent |
| Databricks CLI | login, bundles, deploy | 1.0.0 |
| GitHub CLI `gh` | issues and pull requests | any recent |
| uv | Python and Python tools | any recent |
| Python (through uv) | tests and scripts | 3.11 |
| Spec Kit `specify` | Optional for spec-driven workflows; not required for US00 | any recent |

## 2. Install what is missing

Detect the operating system first. If a command here fails because it changed, read the official page instead of guessing.

### macOS (Homebrew)

If `brew` is missing, send the student to https://brew.sh to install it.

```
brew install git gh uv
brew install databricks/tap/databricks
```

### Windows (WinGet, in PowerShell)

```
winget install --id Git.Git -e
winget install --id GitHub.cli --source winget
winget install --id=astral-sh.uv -e
winget install Databricks.DatabricksCLI
```

After installing tools on Windows, open a fresh terminal or refresh the process `PATH` before running the environment checker. A stale `PATH` can make installed tools appear missing.

### Linux

- git: the distribution's package manager.
- gh: follow https://github.com/cli/cli/blob/trunk/docs/install_linux.md for the distribution.
- uv and Databricks CLI use install scripts. Download the script, show the student what it does, then run it after a yes:
  - https://astral.sh/uv/install.sh
  - https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh

Official pages: https://docs.databricks.com/aws/en/dev-tools/cli/install and https://docs.astral.sh/uv/getting-started/installation/

### All systems, after uv

```
uv python install 3.12
```

Spec Kit is optional and is not installed or used for US00. For a separate spec-driven workflow only:

```
uv tool install specify-cli
```

From the repository root:

```
uv venv --python 3.12
uv pip install -r requirements-dev.txt pyyaml
```

For optional spec-driven workflows only, if `specify` is not found, run `uv tool update-shell` (`unverified`) and open a new terminal.

**Do not run `specify init` during setup.** It writes into agent folders and may replace files. It belongs to a reviewed change on its own branch. (`scripts/sync_agent_folders.py` only removes files it generated; Spec Kit with this script is `unverified`.)

## 3. Verify

Open a new terminal, activate the environment (`source .venv/bin/activate`, Windows `.venv\Scripts\activate`), then:

```
python scripts/check_environment.py
pytest
ruff check .
```

## 4. Logins (the student runs these)

```
gh auth login
databricks auth login --host https://<your-workspace-host> --profile free
databricks current-user me --profile free
```

For problems, see skill `databricks-cli-auth`.

## 5. Fork settings (students work in their own fork)

1. Fork on GitHub, then clone the fork. `gh repo fork <template-owner>/<template-repo> --clone` does both (`unverified`).
2. **Make `gh` target the fork**, or pull requests and issues may go to the teacher's repository:
   ```
   gh repo set-default <student-user>/<fork-name>
   gh repo set-default --view
   ```
3. Check on GitHub that **Issues** is enabled (Settings, General, Features) and that workflows are enabled in the **Actions** tab. Forks may start with both off (`unverified`).
4. A fork of a public repository is public and its visibility cannot be changed on its own. Never commit credentials, workspace URLs or private notes.

Before the first `gh issue create` or `gh pr create`, confirm that the default repository is the student's fork.

## 6. Report

End with a table: tool, version, status (`ok`, `installed`, `blocked`, `skipped`). Say which logins are still pending and what you did not verify.
