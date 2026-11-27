import json

import pytest

from scripts import board

DEFAULT = [
    {"id": "1", "name": "Todo", "color": "GREEN", "description": ""},
    {"id": "2", "name": "In Progress", "color": "YELLOW", "description": ""},
    {"id": "3", "name": "Done", "color": "PURPLE", "description": ""},
]


def test_existing_options_keep_their_ids():
    ids = {o["name"]: o.get("id") for o in board.planned_options(DEFAULT)}
    assert (ids["Backlog"], ids["In Progress"], ids["Done"]) == ("1", "2", "3")
    assert ids["Refinement"] is None


def test_unknown_column_is_never_deleted():
    with pytest.raises(RuntimeError):
        board.planned_options(DEFAULT + [{"id": "4", "name": "Mine"}])


def test_workflow_only_uses_existing_columns_and_never_reaches_done():
    names = {name for name, _, _ in board.COLUMNS}
    assert set(board.ALLOWED) == names
    assert all(targets <= names - {"Done"} for targets in board.ALLOWED.values())


def test_done_is_refused_without_calling_github(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("gh must not be called")

    monkeypatch.setattr(board, "gh", fail)
    assert board.main(["move", "--repo", "a/b", "--issue", "1", "--to", "Done", "--apply"]) == 2


def fake_github(status, assignees, calls):
    def gh(*args, stdin=None):
        calls.append(args)
        if args[:2] == ("project", "list"):
            return json.dumps({"projects": [{"title": "Contratos PT", "number": 3, "id": "P"}]})
        if args[:2] == ("project", "item-list"):
            content = {"number": 1, "url": "https://github.com/a/b/issues/1", "title": "t"}
            return json.dumps({"items": [{"id": "I", "status": status, "content": content}]})
        if args[:2] == ("issue", "view"):
            return json.dumps({"assignees": [{"login": x} for x in assignees]})
        if args == ("api", "user"):
            return json.dumps({"login": "me"})
        return ""

    return gh


def wrote(calls):
    return any(c[:2] in {("project", "item-edit"), ("issue", "edit")} for c in calls)


@pytest.mark.parametrize(
    "status, assignees, target",
    [("Backlog", [], "In Progress"), ("Ready", ["someone-else"], "Spec")],
)
def test_skipping_steps_or_taking_others_work_is_refused(monkeypatch, status, assignees, target):
    calls = []
    monkeypatch.setattr(board, "gh", fake_github(status, assignees, calls))
    command = ["move", "--repo", "a/b", "--issue", "1", "--to", target, "--apply"]
    assert board.main(command) == 2
    assert not wrote(calls)


def test_dry_run_move_changes_nothing(monkeypatch):
    calls = []
    monkeypatch.setattr(board, "gh", fake_github("Ready", [], calls))
    assert board.main(["move", "--repo", "a/b", "--issue", "1", "--to", "Spec"]) == 0
    assert not wrote(calls)


def test_issue_of_another_repo_is_not_moved(monkeypatch):
    calls = []
    monkeypatch.setattr(board, "gh", fake_github("Backlog", [], calls))
    command = ["move", "--repo", "a/other", "--issue", "1", "--to", "Refinement", "--apply"]
    assert board.main(command) == 1
    assert not wrote(calls)
