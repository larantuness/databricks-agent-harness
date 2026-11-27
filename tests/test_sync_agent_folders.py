import sys

import pytest

from scripts import sync_agent_folders as sync


@pytest.fixture
def repo(tmp_path, monkeypatch):
    skill = tmp_path / "skills" / "core" / "mine"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: mine\n---\nbody\n", encoding="utf-8")
    (skill / "extra.md").write_text("extra\n", encoding="utf-8")
    monkeypatch.setattr(sync, "ROOT", tmp_path)
    return tmp_path


def run(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["sync", *args])
    return sync.main()


def add(path, text="from another tool\n"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_files_from_other_tools_are_kept(repo, monkeypatch):
    others = [
        add(repo / ".claude/skills/official/SKILL.md"),
        add(repo / ".claude/commands/other.md"),
        add(repo / ".github/prompts/other.prompt.md"),
    ]
    assert run(monkeypatch) == 0
    assert run(monkeypatch, "--check") == 0
    assert all(path.exists() for path in others)


def test_removed_sources_remove_only_their_copies(repo, monkeypatch):
    assert run(monkeypatch) == 0
    for name in ("SKILL.md", "extra.md"):
        (repo / "skills/core/mine" / name).unlink()
    assert run(monkeypatch, "--check") == 1
    assert run(monkeypatch) == 0
    assert not (repo / ".claude/skills/mine").exists()


def test_a_foreign_skill_with_the_same_name_is_not_overwritten(repo, monkeypatch):
    foreign = add(repo / ".claude/skills/mine/SKILL.md")
    assert run(monkeypatch) == 1
    assert foreign.read_text(encoding="utf-8") == "from another tool\n"
