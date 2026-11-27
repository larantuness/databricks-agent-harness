import json

from scripts import publish_backlog as pb


def test_backlog_has_all_stories_and_known_dependencies():
    stories = pb.load_backlog()
    ids = [story["id"] for story in stories]
    assert ids == ["US{:02d}".format(n) for n in range(18)]
    assert all(set(story["depends"]) <= set(ids) for story in stories)
    assert all("Critérios de aceite" in story["body"] for story in stories)


def test_requests_without_story_are_not_published():
    assert all("ajuste direto" not in story["body"] for story in pb.load_backlog())


def test_dry_run_never_calls_gh(monkeypatch):
    def fail(*args):
        raise AssertionError("gh must not be called")

    monkeypatch.setattr(pb, "gh", fail)
    assert pb.main(["--repo", "someone/fork", "--project", "Board"]) == 0


class FakeGitHub:
    """Keeps issues and one board in memory."""

    def __init__(self):
        self.issues, self.boards, self.items, self.calls = [], [], [], []

    def __call__(self, *args):
        self.calls.append(args)
        value = {flag: args[i + 1] for i, flag in enumerate(args[:-1]) if flag.startswith("--")}
        command = args[:2]
        if command == ("issue", "list"):
            return json.dumps(self.issues)
        if command == ("issue", "create"):
            url = "https://example.invalid/issues/{}".format(len(self.issues) + 1)
            self.issues.append({"title": value["--title"], "url": url})
            return url + "\n"
        if command == ("project", "list"):
            return json.dumps({"projects": self.boards})
        if command == ("project", "create"):
            self.boards.append({"title": value["--title"], "number": 1})
            return json.dumps(self.boards[-1])
        if command == ("project", "item-list"):
            return json.dumps({"items": [{"content": {"url": u}} for u in self.items]})
        if command == ("project", "item-add"):
            self.items.append(value["--url"])
        return ""


def test_running_twice_creates_nothing_new(monkeypatch):
    fake = FakeGitHub()
    monkeypatch.setattr(pb, "gh", fake)
    command = ["--repo", "someone/fork", "--project", "Board", "--apply"]
    assert pb.main(command) == 0
    assert pb.main(command) == 0
    assert (len(fake.issues), len(fake.boards), len(fake.items)) == (18, 1, 18)


def test_every_call_names_the_students_account(monkeypatch):
    fake = FakeGitHub()
    monkeypatch.setattr(pb, "gh", fake)
    assert pb.main(["--repo", "someone/fork", "--project", "Board", "--apply"]) == 0
    for call in fake.calls:
        if call[0] == "project":
            assert call[call.index("--owner") + 1] == "someone"
        else:
            assert call[call.index("--repo") + 1] == "someone/fork"
