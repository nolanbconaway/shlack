"""Tests for the slack module."""
import pytest
from shlack.slack import attachment_formatter


@pytest.mark.parametrize(
    "attachment,formatted",
    [
        (
            "non-dict is made into one",
            dict(
                fallback="",
                color="",
                fields=[dict(title="", value="non-dict is made into one", short=False)],
                ts=0,
            ),
        ),
        (
            {1: "int key left alone"},
            dict(
                fallback="",
                color="",
                fields=[dict(title=1, value="int key left alone", short=True)],
                ts=0,
            ),
        ),
        (
            {"int value is stringed": 1},
            dict(
                fallback="",
                color="",
                fields=[dict(title="int value is stringed", value="1", short=True)],
                ts=0,
            ),
        ),
        (
            {"int value is stringed": 1},
            dict(
                fallback="",
                color="",
                fields=[dict(title="int value is stringed", value="1", short=True)],
                ts=0,
            ),
        ),
        (
            {1: 1, 2: 2},
            dict(
                fallback="",
                color="",
                fields=[
                    dict(title=1, value="1", short=True),
                    dict(title=2, value="2", short=True),
                ],
                ts=0,
            ),
        ),
    ],
)
def test_attachment_formatter(monkeypatch, attachment, formatted):
    """Test the attachment formatter."""
    monkeypatch.setattr("time.time", lambda: 0)
    assert attachment_formatter(attachment, color="") == formatted
