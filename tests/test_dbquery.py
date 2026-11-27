import pytest

from scripts.dbquery import check_read_only, main


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT 1",
        "select * from a.b.c limit 5;",
        "WITH t AS (SELECT 1 AS x) SELECT x FROM t",
        "SHOW TABLES IN system.lakeflow",
        "SHOW CREATE TABLE a.b.c",
        "DESCRIBE TABLE system.billing.usage",
        "-- drop table x\nSELECT 'delete; update' AS note",
        "/* insert */ SELECT `create` FROM t",
        "SELECT details:update_progress.state, update_id FROM t",
    ],
)
def test_accepts_reads(sql):
    assert check_read_only(sql) is None


@pytest.mark.parametrize(
    "sql",
    [
        "",
        "DROP TABLE a",
        "UPDATE a SET x = 1",
        "SELECT 1; DROP TABLE a",
        "WITH t AS (SELECT 1) INSERT INTO a SELECT * FROM t",
        "EXPLAIN DELETE FROM a",
        "SET spark.sql.ansi.enabled = false",
        "-- SELECT\nTRUNCATE TABLE a",
        "SELECT 'a' /* x */ ; DELETE FROM a",
        "SELECT http_request(conn => 'c')",
        "SELECT ai_query ('model', 'text')",
        "SELECT `http_request`(conn => 'c')",
        "SELECT 'unterminated",
    ],
)
def test_refuses_everything_else(sql):
    assert check_read_only(sql) is not None


def test_refused_statement_never_reaches_the_cli(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("the CLI must not be called")

    monkeypatch.setattr("scripts.dbquery.subprocess.run", fail)
    assert main(["DELETE FROM a"]) == 2


def test_sql_is_passed_after_separator(monkeypatch):
    seen = {}

    class Done:
        returncode = 0

    def fake_run(command):
        seen["command"] = command
        return Done()

    monkeypatch.setattr("scripts.dbquery.subprocess.run", fake_run)
    assert main(["-- note\nSELECT 1"]) == 0
    assert seen["command"][-2:] == ["--", "-- note\nSELECT 1"]
    assert "free" in seen["command"]
