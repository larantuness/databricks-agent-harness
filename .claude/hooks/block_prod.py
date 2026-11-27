#!/usr/bin/env python3
"""Claude Code PreToolUse hook: stop shell commands that target production.

Claude Code sends the pending tool call as JSON on stdin. Exiting with code 2 blocks the call and
shows stderr to the agent. This is a guardrail for the lab, not a security boundary: the real
boundary is your Databricks permissions (use a dev-only profile).
"""

import json
import re
import sys

BLOCKED = [
    (r"(-t|--target)[ =]+prod", "deploying or running against the prod target is not allowed here"),
    (r"databricks\s+bundle\s+destroy", "bundle destroy needs a human to run it"),
    (r"git\s+push\s+.*--force", "force push is not allowed"),
    (r"git\s+push\s+\S+\s+(HEAD:)?main\b", "never push directly to main; open a pull request"),
]

try:
    event = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

command = (event.get("tool_input") or {}).get("command", "")
for pattern, reason in BLOCKED:
    if re.search(pattern, command):
        print(f"Blocked by .claude/hooks/block_prod.py: {reason}.", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
