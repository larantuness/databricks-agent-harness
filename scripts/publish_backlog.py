#!/usr/bin/env python3
"""Create the stories in BACKLOG.md as GitHub issues, and optionally a project board.

Dry run by default. Every GitHub call names the target, so nothing goes to the repository a
fork came from. Safe to run again: published stories and board items are skipped. Existing
issues are never edited or closed.

Usage:
  python scripts/publish_backlog.py --repo you/your-fork --project "Contratos PT"
  python scripts/publish_backlog.py --repo you/your-fork --project "Contratos PT" --apply
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

BACKLOG = Path(__file__).resolve().parent.parent / "BACKLOG.md"
REPO_NAME = re.compile(r"^[\w.-]+/[\w.-]+$")
STORY_HEADING = re.compile(r"^(US\d{2}): (.+)$")
STORY_ID = re.compile(r"\[(US\d{2})\]")


def parse_backlog(text):
    stories = []
    for section in re.split(r"^## ", text, flags=re.MULTILINE)[1:]:
        heading, _, rest = section.partition("\n")
        match = STORY_HEADING.match(heading.strip())
        if not match:
            continue
        story_id, title = match.groups()
        labels = re.search(r"^- Labels: (.+)$", rest, re.MULTILINE)
        depends = re.search(r"^- Depende de: (.+)$", rest, re.MULTILINE)
        if not labels or not depends:
            raise ValueError("{}: needs the Labels and Depende de lines".format(story_id))
        stories.append(
            {
                "id": story_id,
                "title": "[{}] {}".format(story_id, title),
                "labels": [x.strip() for x in labels.group(1).split(",") if x.strip()],
                "depends": re.findall(r"US\d{2}", depends.group(1)),
                "body": rest.strip() + "\n",
            }
        )
    ids = [story["id"] for story in stories]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate story id in the backlog")
    return stories


def load_backlog(path=BACKLOG):
    return parse_backlog(path.read_text(encoding="utf-8"))


def issues_by_story(issues):
    """Map story id to the issue that already has it in its title."""
    found = {}
    for issue in issues:
        match = STORY_ID.match(issue["title"])
        if match:
            found.setdefault(match.group(1), issue)
    return found


def gh(*args):
    done = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8")
    if done.returncode != 0:
        raise RuntimeError(done.stderr.strip() or "gh failed")
    return done.stdout


def publish_issues(repo, stories):
    """Create the missing issues. Return the URL of every backlog issue."""
    listed = gh("issue", "list", "--repo", repo, "--state", "all", "--limit", "1000",
                "--json", "title,url")  # fmt: skip
    published = issues_by_story(json.loads(listed))
    urls = {story_id: issue["url"] for story_id, issue in published.items()}
    todo = [story for story in stories if story["id"] not in published]
    for label in sorted({label for story in todo for label in story["labels"]}):
        gh("label", "create", label, "--repo", repo, "--force")
    for story in todo:
        command = ["issue", "create", "--repo", repo,
                   "--title", story["title"], "--body", story["body"]]  # fmt: skip
        for label in story["labels"]:
            command += ["--label", label]
        urls[story["id"]] = gh(*command).strip()
        print(urls[story["id"]])
    print("Issues: created {}, skipped {}.".format(len(todo), len(stories) - len(todo)))
    return [urls[story["id"]] for story in stories]


def publish_board(repo, title, urls):
    """Create or reuse a project board of the repository owner and add the issues."""
    owner = repo.split("/")[0]
    listed = json.loads(gh("project", "list", "--owner", owner, "--limit", "100",
                           "--format", "json"))  # fmt: skip
    board = next((p for p in listed["projects"] if p["title"] == title), None)
    if board is None:
        board = json.loads(gh("project", "create", "--owner", owner, "--title", title,
                              "--format", "json"))  # fmt: skip
    number = str(board["number"])
    items = json.loads(gh("project", "item-list", number, "--owner", owner, "--limit", "1000",
                          "--format", "json"))  # fmt: skip
    present = {(item.get("content") or {}).get("url") for item in items["items"]}
    missing = [url for url in urls if url not in present]
    for url in missing:
        gh("project", "item-add", number, "--owner", owner, "--url", url)
    # Linking comes last: if it fails, the board and its items are already there.
    gh("project", "link", number, "--owner", owner, "--repo", repo)
    print("Board '{}' (number {}): added {} items.".format(title, number, len(missing)))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Publish the backlog to GitHub.")
    parser.add_argument("--repo", required=True, help="owner/name of YOUR fork")
    parser.add_argument("--project", help="title of the project board to create or reuse")
    parser.add_argument("--apply", action="store_true", help="make the changes")
    args = parser.parse_args(argv)
    if not REPO_NAME.match(args.repo):
        parser.error("--repo must look like owner/name")

    stories = load_backlog()
    if not args.apply:
        print("Dry run. Target: {}. Nothing was contacted or created.".format(args.repo))
        for story in stories:
            print("  " + story["title"])
        print("{} stories. Already published ones are skipped with --apply.".format(len(stories)))
        if args.project:
            print("Board: '{}' would be created or reused.".format(args.project))
        return 0

    try:
        urls = publish_issues(args.repo, stories)
        if args.project:
            publish_board(args.repo, args.project, urls)
    except (RuntimeError, FileNotFoundError) as error:
        print("Stopped: {}".format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
