"""Tests for the cli module."""
import subprocess

import pytest
from click.testing import CliRunner

from shlack import slack
from shlack.cli import message as message_cli
from shlack.cli import task as task_cli


class MockChat:
    """Mock chat class for slacker."""

    @staticmethod
    def post_message(*args, **kwargs):
        """Mock the post message method."""
        return None


@pytest.mark.parametrize(
    "command, is_valid",
    [
        (["echo", "1"], True),
        (["INVALD_COMMAND"], False),
        (["echo", "1", "-f", "text"], True),
        (["echo", "1", "-f", "auto"], True),
        (["echo", "1", "-f", "file"], True),
        (["echo", "1", "-f", "none"], True),
        (["echo", "1", "-f", "invalid"], False),
    ],
)
def test_task(monkeypatch, command, is_valid):
    """Test that the task logic does not except out.
    
    This is NOT a test of the slack message content. I have no idea how to test that.
    """
    monkeypatch.setattr("slacker.Chat", lambda *args, **kw: MockChat())
    monkeypatch.setattr(
        "shlack.slack.upload_file_get_permalink", lambda *a, **kw: "URL"
    )
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")
    monkeypatch.setenv("SLACK_CHANNEL", "ALSO_FAKE")

    runner = CliRunner()
    result = runner.invoke(task_cli.main, command + ["--no-detach"])

    if is_valid:
        assert result.exit_code == 0
    else:
        assert result.exit_code != 0


@pytest.mark.parametrize(
    "args",
    [
        ("OK",),
        ("OK", "-a", "1", "2"),
        ("OK", "-a", "1", "2", "-a", "3", "4"),
        ("OK", "-u", "readme.md"),
        ("OK", "-a", "1", "2", "-u", "readme.md"),
        ("OK", "-a", "1", "2", "-a", "3", "4", "-u", "readme.md"),
        ("-a", "1", "2"),
        ("-a", "1", "2", "-a", "3", "4"),
        ("-u", "readme.md"),
        ("-a", "1", "2", "-u", "readme.md"),
        ("-a", "1", "2", "-a", "3", "4", "-u", "readme.md"),
    ],
)
def test_message(monkeypatch, args):
    """Test that the message logic does not except out.
    
    This is NOT a test of the slack message content. I have no idea how to test that.
    """
    monkeypatch.setattr("slacker.Chat", lambda *args, **kw: MockChat())
    monkeypatch.setattr(
        "shlack.slack.upload_file_get_permalink", lambda *a, **kw: "URL"
    )
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
        ("python", "-m", "shlack", "--help"),
        ("python", "-m", "shlack", "task", "--help"),
        ("python", "-m", "shlack", "message", "--help"),
        ("python", "-m", "shlack.cli", "--help"),
        ("python", "-m", "shlack.cli", "task", "--help"),
        ("python", "-m", "shlack.cli", "message", "--help"),
    ],
)
def test_cli_installed(args):
    """Test that the CLI has been installed."""
    subprocess.check_output(args)
