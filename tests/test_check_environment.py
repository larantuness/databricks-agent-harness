import subprocess
from types import SimpleNamespace

import pytest

from scripts import check_environment


@pytest.mark.parametrize(
    "error", [OSError("token=do-not-print"), subprocess.TimeoutExpired("git", 60)]
)
def test_command_error_is_reported_without_exposing_its_message(
    monkeypatch, capsys, error
):
    sensitive_message = "token=do-not-print"

    def fake_which(command):
        return "mock-" + command if command == "git" else None

    def fake_run(*args, **kwargs):
        raise error

    monkeypatch.setattr(check_environment.shutil, "which", fake_which)
    monkeypatch.setattr(check_environment.subprocess, "run", fake_run)

    assert check_environment.main() == 1
    output = capsys.readouterr().out
    git_line = next(line for line in output.splitlines() if line.startswith("git "))
    assert git_line.split()[1] == "error"
    assert sensitive_message not in output


def test_uv_probe_exception_is_missing_without_exposing_its_message(monkeypatch, capsys):
    sensitive_message = "workspace=do-not-print"

    def fake_which(command):
        return "mock-uv" if command == "uv" else None

    def fake_run(*args, **kwargs):
        raise OSError(sensitive_message)

    monkeypatch.setattr(check_environment.shutil, "which", fake_which)
    monkeypatch.setattr(check_environment.subprocess, "run", fake_run)
    monkeypatch.setattr(check_environment.sys, "version_info", (3, 10))

    assert check_environment.main() == 1
    output = capsys.readouterr().out
    python_line = next(line for line in output.splitlines() if line.startswith("Python"))
    assert python_line.split()[2] == "missing"
    assert sensitive_message not in output


def test_nonzero_command_output_is_not_printed(monkeypatch, capsys):
    sensitive_message = "token=do-not-print"

    def fake_which(command):
        return "mock-" + command if command == "git" else None

    class FakeCompletedProcess:
        returncode = 1
        stdout = sensitive_message

    monkeypatch.setattr(check_environment.shutil, "which", fake_which)
    monkeypatch.setattr(
        check_environment.subprocess, "run", lambda *args, **kwargs: FakeCompletedProcess()
    )

    assert check_environment.main() == 1
    output = capsys.readouterr().out
    git_line = next(line for line in output.splitlines() if line.startswith("git "))
    assert git_line.split()[1] == "error"
    assert sensitive_message not in output


def test_spec_kit_is_never_probed(monkeypatch, capsys):
    located = []
    executed = []

    def fake_which(command):
        located.append(command)
        return "mock-" + command

    def fake_run(command, **kwargs):
        executed.append(command)
        return SimpleNamespace(returncode=0, stdout="tool version 1.2.3")

    monkeypatch.setattr(check_environment.shutil, "which", fake_which)
    monkeypatch.setattr(check_environment.subprocess, "run", fake_run)
    monkeypatch.setattr(check_environment.sys, "version_info", (3, 11, 0))

    assert check_environment.main() == 0
    capsys.readouterr()

    assert not any("specify" in command.lower() for command in located)
    assert not any(
        "specify" in str(argument).lower()
        for command in executed
        for argument in command
    )


def test_missing_spec_kit_is_optional_and_not_exposed(monkeypatch, capsys):
    sensitive_message = "workspace=do-not-print"

    def fake_which(command):
        return None if command == "specify" else "mock-" + command

    def fake_run(*args, **kwargs):
        return SimpleNamespace(
            returncode=0, stdout="tool version 1.2.3 " + sensitive_message
        )

    monkeypatch.setattr(check_environment.shutil, "which", fake_which)
    monkeypatch.setattr(check_environment.subprocess, "run", fake_run)
    monkeypatch.setattr(check_environment.sys, "version_info", (3, 11, 0))

    assert check_environment.main() == 0
    output = capsys.readouterr().out

    spec_kit_line = next(
        line for line in output.splitlines() if line.startswith("Spec Kit")
    )
    assert spec_kit_line.rstrip() == "{:<16} {}".format(
        "Spec Kit", "optional/skipped"
    )
    assert sensitive_message not in output
