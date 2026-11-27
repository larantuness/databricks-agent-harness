#!/usr/bin/env python3
"""Fail if REPO_MAP.md and the repository disagree.

Checks that every agent, prompt and skill that exists is named in REPO_MAP.md, and that
every backticked path in REPO_MAP.md that looks like a repo file really exists.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    text = (ROOT / "REPO_MAP.md").read_text(encoding="utf-8")
    problems = []
    for f in sorted((ROOT / "agents").glob("*.md")):
        if f"`{f.stem}`" not in text:
            problems.append(f"agent not in REPO_MAP: {f.stem}")
    for f in sorted((ROOT / "prompts").glob("*.md")):
        if f"`{f.stem}`" not in text:
            problems.append(f"prompt not in REPO_MAP: {f.stem}")
    for d in sorted((ROOT / "skills").glob("*/*/")):
        if f"`{d.name}`" not in text:
            problems.append(f"skill not in REPO_MAP: {d.name}")
    for ref in re.findall(r"`([\w./-]+\.(?:md|py|json|yml|yaml))`", text):
        if "/" in ref and not (ROOT / ref).exists():
            problems.append(f"REPO_MAP mentions a missing file: {ref}")
    for p in problems:
        print(p)
    if problems:
        return 1
    print("REPO_MAP.md matches the repository.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
