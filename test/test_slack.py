"""Tests for the slack module."""
import pytest

from shlack import slack


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
    assert slack.attachment_formatter(attachment, color="") == formatted


def test_slacker_factor_no_key_error(monkeypatch):
    """Test that an error is raise if there is no API key."""
    monkeypatch.delenv("SLACK_OAUTH_API_TOKEN", raising=False)
    with pytest.raises(EnvironmentError):
        slack.slacker_factory()


def test_upload_file_get_permalink(monkeypatch):
    """Test the file uploader behaves."""
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")

    class Object(object):
        pass

    slacker = Object()
    setattr(slacker, "files", Object())
    resp = Object()
    setattr(resp, "body", dict(ok=True, file=dict(permalink="URL")))
    setattr(slacker.files, "upload", lambda *a, **kw: resp)

    assert slack.upload_file_get_permalink(slacker) == "URL"


def test_upload_file_get_permalink_error(monkeypatch):
    """Test the file uploader behaves."""
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")

    class Object(object):
        pass

    slacker = Object()
    setattr(slacker, "files", Object())
    resp = Object()
    setattr(resp, "body", dict(ok=False))
    setattr(slacker.files, "upload", lambda *a, **kw: resp)

    print(resp.body.get("file", {}).get("permalink"))
    with pytest.raises(slack.SlackError):
        slack.upload_file_get_permalink(slacker, raise_error=True)


def test_attach_text_data_file(monkeypatch):
    """Test the task output attchment logic when a file is expected."""
    monkeypatch.setattr(
        "shlack.slack.upload_file_get_permalink", lambda *a, **kw: "URL"
    )
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")
    monkeypatch.setenv("SLACK_CHANNEL", "ALSO_FAKE")
    field = slack.attach_text_data(
        slacker="fake", text_data="data", name="name", data_format="file", color=""
    )["fields"][0]
    assert "name" in field["title"]
    assert "URL" in field["value"]

    # add auto format test
    field = slack.attach_text_data(
        slacker="fake", text_data="1" * 1001, name="name", data_format="auto", color=""
    )["fields"][0]
    assert "name" in field["title"]
    assert "URL" in field["value"]


def test_attach_text_data_text(monkeypatch):
    """Test the task output attchment logic when text is expected."""
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")
    monkeypatch.setenv("SLACK_CHANNEL", "ALSO_FAKE")
    field = slack.attach_text_data(
        slacker="fake", text_data="data", name="name", data_format="text", color=""
    )["fields"][0]
    assert not field["title"]
    assert "data" in field["value"]

    # auto format test
    field = slack.attach_text_data(
        slacker="fake", text_data="data", name="name", data_format="auto", color=""
    )["fields"][0]
    assert not field["title"]
    assert "data" in field["value"]


def test_attach_text_data_none(monkeypatch):
    """Test the task output attchment logic when nothing is expected."""
    monkeypatch.setenv("SLACK_OAUTH_API_TOKEN", "FAKE")
    monkeypatch.setenv("SLACK_CHANNEL", "ALSO_FAKE")
    assert None is slack.attach_text_data(
        slacker="fake", text_data="data", name="name", data_format="none", color=""
    )
