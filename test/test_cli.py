"""Tests for the cli module."""
import subprocess

import pytest
from click.testing import CliRunner

from shlack import slack
from shlack.cli import message as message_cli
from shlack.cli import task as task_cli
from shlack.cli.task import attach_output


class MockChat:
    """Mock chat class for slacker."""

    @staticmethod
    def post_message(*args, **kwargs):
        """Mock the post message method."""
        return None


@pytest.mark.parametrize(
    "command, is_valid", [(["echo", "1"], True), (["INVALD_COMMAND"], False)]
)
def test_task(monkeypatch, command, is_valid):
    """Test that the task logic does not except out.
    
    This is NOT a test of the slack message content. I have no idea how to test that.
    """
    monkeypatch.setattr("slacker.Chat", lambda *args, **kw: MockChat())
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")
    monkeypatch.setenv("SLACK_CHANNEL", "ALSO_FAKE")

    runner = CliRunner()
    result = runner.invoke(task_cli.main, command + ["--no-detach", "-f", "text"])

    if is_valid:
        assert result.exit_code == 0
    else:
        assert result.exit_code != 0


@pytest.mark.parametrize(
    "args", [("OK",), ("OK", "-a", "1", "2"), ("OK", "-a", "1", "2", "-a", "3", "4")]
)
def test_message(monkeypatch, args):
    """Test that the message logic does not except out.
    
    This is NOT a test of the slack message content. I have no idea how to test that.
    """
    monkeypatch.setattr("slacker.Chat", lambda *args, **kw: MockChat())
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")
    monkeypatch.setenv("SLACK_CHANNEL", "ALSO_FAKE")

    runner = CliRunner()
    result = runner.invoke(message_cli.main, args)

    assert result.exit_code == 0


@pytest.mark.parametrize(
    "args",
    [
        ("shlack", "--help"),
        ("shlack", "task", "--help"),
        ("shlack", "message", "--help"),
    ],
)
def test_cli_installed(args):
    """Test that the CLI has been installed."""
    subprocess.check_output(args)


def test_task_attach_file(monkeypatch):
    """Test the task output attchment logic when a file is expected."""
    monkeypatch.setattr(
        "shlack.slack.upload_file_get_permalink", lambda *a, **kw: "URL"
    )
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")
    monkeypatch.setenv("SLACK_CHANNEL", "ALSO_FAKE")
    field = attach_output(
        slacker="fake", text_data="data", name="name", out_format="file", color=""
    )["fields"][0]
    assert "name" in field["title"]
    assert "URL" in field["value"]

    # add auto format test
    field = attach_output(
        slacker="fake", text_data="1" * 1001, name="name", out_format="auto", color=""
    )["fields"][0]
    assert "name" in field["title"]
    assert "URL" in field["value"]


def test_task_attach_text(monkeypatch):
    """Test the task output attchment logic when text is expected."""
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")
    monkeypatch.setenv("SLACK_CHANNEL", "ALSO_FAKE")
    field = attach_output(
        slacker="fake", text_data="data", name="name", out_format="text", color=""
    )["fields"][0]
    assert not field["title"]
    assert "data" in field["value"]

    # auto format test
    field = attach_output(
        slacker="fake", text_data="data", name="name", out_format="auto", color=""
    )["fields"][0]
    assert not field["title"]
    assert "data" in field["value"]


def test_task_attach_none(monkeypatch):
    """Test the task output attchment logic when nothing is expected."""
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")
    monkeypatch.setenv("SLACK_CHANNEL", "ALSO_FAKE")
    assert None is attach_output(
        slacker="fake", text_data="data", name="name", out_format="none", color=""
    )
