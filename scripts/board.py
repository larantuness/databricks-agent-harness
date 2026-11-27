#!/usr/bin/env python3
"""The agile board of the project: set up its columns and view, list it, and move issues.

Dry run by default for `setup` and `move`. Agents never move an issue to Done: GitHub does it
when the pull request is merged. The script checks the order of the steps; it cannot check
that a person approved. See skill github-board-flow.

Usage:
  python scripts/board.py setup  --repo you/your-fork [--apply]
  python scripts/board.py status --repo you/your-fork
  python scripts/board.py move   --repo you/your-fork --issue 3 --to Refinement [--apply]
"""

import argparse
import json
import re
import subprocess
import sys

PROJECT_TITLE = "Contratos PT"
VIEW_NAME = "Quadro"

# name, color, description. The order is the order of the columns.
COLUMNS = [
    ("Backlog", "GRAY", "Ainda não analisada"),
    ("Refinement", "PINK", "A esclarecer: critérios, dúvidas, tamanho e dependências"),
    ("Ready", "BLUE", "História aprovada por uma pessoa, pronta para começar"),
    ("Spec", "ORANGE", "spec, clarify, plan e tasks, antes do código"),
    ("In Progress", "YELLOW", "Código e testes numa branch"),
    ("Testing", "RED", "Testes, lint e validação em dev contra os critérios de aceite"),
    ("In Review", "PURPLE", "Pull request aberto, à espera de revisão e merge"),
    ("Done", "GREEN", "Merge feito. Só o GitHub ou uma pessoa move para aqui"),
]
# Old default names kept as the same option, so cards and built-in workflows are preserved.
RENAMED = {"Todo": "Backlog"}

ALLOWED = {
    "Backlog": {"Refinement"},
    "Refinement": {"Ready", "Backlog"},
    "Ready": {"Spec", "In Progress", "Refinement"},
    "Spec": {"In Progress", "Refinement"},
    "In Progress": {"Testing", "Spec", "Refinement"},
    "Testing": {"In Review", "In Progress"},
    "In Review": {"In Progress", "Testing"},
    "Done": set(),
}
# Work starts here, so the issue must belong to whoever moves it.
CLAIMS = {"Spec", "In Progress"}


def gh(*args, stdin=None):
    done = subprocess.run(
        ["gh", *args], input=stdin, capture_output=True, text=True, encoding="utf-8"
    )
    if done.returncode != 0:
        raise RuntimeError(done.stderr.strip() or "gh failed")
    return done.stdout


def graphql(query, **variables):
    body = json.dumps({"query": query, "variables": variables})
    return json.loads(gh("api", "graphql", "--input", "-", stdin=body))["data"]


def find_project(owner):
    listed = json.loads(
        gh("project", "list", "--owner", owner, "--limit", "100", "--format", "json")
    )
    for project in listed["projects"]:
        if project["title"] == PROJECT_TITLE:
            return project
    raise RuntimeError(
        "board '{}' not found. Run publish_backlog.py first.".format(PROJECT_TITLE)
    )


def read_board(project_id):
    query = """query($id: ID!) { node(id: $id) { ... on ProjectV2 {
      views(first: 50) { nodes { name layout } }
      field(name: "Status") { ... on ProjectV2SingleSelectField {
        id options { id name color description } } } } } }"""
    return graphql(query, id=project_id)["node"]


def planned_options(current):
    """Return the new column list, keeping the id of every option that already exists."""
    existing = {RENAMED.get(o["name"], o["name"]): o["id"] for o in current}
    unknown = sorted(set(existing) - {name for name, _, _ in COLUMNS})
    if unknown:
        # Replacing the list would delete these and clear the cards in them.
        raise RuntimeError("columns not in this workflow, not touched: " + ", ".join(unknown))
    options = []
    for name, color, description in COLUMNS:
        option = {"name": name, "color": color, "description": description}
        if name in existing:
            option["id"] = existing[name]
        options.append(option)
    return options


def list_items(owner, number):
    listed = json.loads(
        gh("project", "item-list", str(number), "--owner", owner, "--limit", "1000",
           "--format", "json")  # fmt: skip
    )
    return listed["items"]


def in_repo(item, repo):
    url = (item.get("content") or {}).get("url") or ""
    return re.match(r"https://github\.com/{}/(issues|pull)/".format(re.escape(repo)), url)


def set_status(project_id, field_id, item_id, option_id):
    gh("project", "item-edit", "--project-id", project_id, "--field-id", field_id,
       "--id", item_id, "--single-select-option-id", option_id)  # fmt: skip


def setup(repo, apply):
    owner = repo.split("/")[0]
    project = find_project(owner)
    board = read_board(project["id"])
    current = board["field"]["options"]
    options = planned_options(current)
    keys = ("name", "color", "description")
    columns_ok = [[o[k] for k in keys] for o in current] == [[o[k] for k in keys] for o in options]
    view_ok = any(v["name"] == VIEW_NAME for v in board["views"]["nodes"])
    print("Columns: " + ("already set" if columns_ok else " > ".join(o["name"] for o in options)))
    print("View '{}': {}".format(VIEW_NAME, "already exists" if view_ok else "will be created"))
    if not apply:
        print("Dry run. Nothing was changed.")
        return 0
    if not columns_ok:
        graphql(
            """mutation($field: ID!, $options: [ProjectV2SingleSelectFieldOptionInput!]) {
              updateProjectV2Field(input: {fieldId: $field, singleSelectOptions: $options}) {
                clientMutationId } }""",
            field=board["field"]["id"],
            options=options,
        )
    if not view_ok:
        graphql(
            """mutation($project: ID!, $name: String!) {
              createProjectV2View(input: {projectId: $project, name: $name,
                layout: BOARD_LAYOUT}) { clientMutationId } }""",
            project=project["id"],
            name=VIEW_NAME,
        )
    field = read_board(project["id"])["field"]
    backlog = next(o["id"] for o in field["options"] if o["name"] == "Backlog")
    loose = [i for i in list_items(owner, project["number"]) if not i.get("status")]
    for item in loose:
        set_status(project["id"], field["id"], item["id"], backlog)
    print("Done. Cards without a column moved to Backlog: {}.".format(len(loose)))
    return 0


def show(repo):
    owner = repo.split("/")[0]
    items = [i for i in list_items(owner, find_project(owner)["number"]) if in_repo(i, repo)]
    for name, _, _ in COLUMNS:
        cards = [i for i in items if i.get("status") == name]
        print("{} ({})".format(name, len(cards)))
        for item in sorted(cards, key=lambda i: i["content"]["number"]):
            print("  #{} {}".format(item["content"]["number"], item["content"]["title"]))
    return 0


def move(repo, issue, target, apply):
    if target == "Done":
        print("Refused: Done is set by GitHub on merge, or by a person.", file=sys.stderr)
        return 2
    owner = repo.split("/")[0]
    project = find_project(owner)
    item = next(
        (i for i in list_items(owner, project["number"])
         if in_repo(i, repo) and i["content"]["number"] == issue),  # fmt: skip
        None,
    )
    if item is None:
        raise RuntimeError("issue #{} is not on the board".format(issue))
    source = item.get("status") or "Backlog"
    if target not in ALLOWED.get(source, set()):
        allowed = ", ".join(sorted(ALLOWED.get(source, set()))) or "nothing"
        print("Refused: from {} you can go to: {}.".format(source, allowed), file=sys.stderr)
        return 2
    claim = False
    if target in CLAIMS:
        data = json.loads(gh("issue", "view", str(issue), "--repo", repo, "--json", "assignees"))
        assignees = [a["login"] for a in data["assignees"]]
        me = json.loads(gh("api", "user"))["login"]
        if assignees and me not in assignees:
            print("Refused: assigned to {}.".format(", ".join(assignees)), file=sys.stderr)
            return 2
        claim = not assignees
    print("#{}: {} -> {}{}".format(issue, source, target, ", assign to you" if claim else ""))
    if not apply:
        print("Dry run. Nothing was changed.")
        return 0
    if claim:
        gh("issue", "edit", str(issue), "--repo", repo, "--add-assignee", "@me")
    field = read_board(project["id"])["field"]
    option = next((o["id"] for o in field["options"] if o["name"] == target), None)
    if option is None:
        raise RuntimeError("column '{}' missing. Run board.py setup.".format(target))
    set_status(project["id"], field["id"], item["id"], option)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="The project's agile board.")
    parser.add_argument("action", choices=["setup", "status", "move"])
    parser.add_argument("--repo", required=True, help="owner/name of YOUR fork")
    parser.add_argument("--issue", type=int)
    parser.add_argument("--to", choices=[name for name, _, _ in COLUMNS])
    parser.add_argument("--apply", action="store_true", help="make the changes")
    args = parser.parse_args(argv)
    if not re.match(r"^[\w.-]+/[\w.-]+$", args.repo):
        parser.error("--repo must look like owner/name")
    if args.action == "move" and (args.issue is None or args.to is None):
        parser.error("move needs --issue and --to")
    try:
        if args.action == "setup":
            return setup(args.repo, args.apply)
        if args.action == "status":
            return show(args.repo)
        return move(args.repo, args.issue, args.to, args.apply)
    except (RuntimeError, FileNotFoundError) as error:
        print("Stopped: {}".format(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
