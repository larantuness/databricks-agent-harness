import json
import subprocess
import sys
from pathlib import Path

import pytest

HOOK = Path(__file__).resolve().parent.parent / ".claude" / "hooks" / "block_prod.py"


def exit_code(command):
    event = json.dumps({"tool_input": {"command": command}})
    done = subprocess.run([sys.executable, str(HOOK)], input=event, capture_output=True, text=True)
    return done.returncode


@pytest.mark.parametrize(
    "command",
    [
        'databricks experimental aitools tools query "SELECT 1"',
        "cd x && databricks experimental aitools tools query --file q.sql",
        "export A=1\ndatabricks experimental aitools tools query 'SELECT 1'",
        "databricks experimental aitools tools statement submit 'DROP TABLE a'",
        "databricks --profile free experimental aitools tools discover-schema a.b.c",
        "databricks api post /api/2.0/sql/statements --json @body.json",
        "databricks bundle destroy -t dev",
        "databricks bundle deploy -t prod",
    ],
)
def test_blocked(command):
    assert exit_code(command) == 2


@pytest.mark.parametrize(
    "command",
    [
        'python scripts/dbquery.py "SELECT 1"',
        "databricks experimental aitools tools query --help",
        'grep -rn "databricks experimental aitools tools query" skills/',
        "databricks bundle plan -t dev",
        "databricks pipelines dry-run -t dev",
    ],
)
def test_allowed(command):
    assert exit_code(command) == 0
