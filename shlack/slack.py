"""Utilities for interacting with the slack API."""
import copy
import os
import subprocess
import time

from slacker import Slacker

MAX_TEXT_LENGTH = 750


class SlackError(Exception):
    """Custom error for slack issues."""

    pass


def slacker_factory(api_key=None):
    """Return a slacker object, getting the API key from the user or env."""
    if api_key is None:
        api_key = os.getenv("SLACK_OAUTH_API_TOKEN")
        if api_key is None:
            raise EnvironmentError("No Oauth API key provided!")

    return Slacker(api_key)


def upload_file_get_permalink(slacker, raise_error=False, *args, **kwargs):
    """Upload a file and return the permalink.

    Option to raise SlackError is there is a problem, or silently return None.

    This simply handles the return value of slacker.files.upload. The signature for 
    slacker.files.upload is:

    file_=None,
    content=None,
    filetype=None,
    filename=None,
    title=None,
    initial_comment=None,
    channels=None,
    thread_ts=None
    """
    out = slacker.files.upload(*args, **kwargs).body

    if raise_error and not out["ok"]:
        raise SlackError("Unable to upload file.")

    return out.get("file", {}).get("permalink")


def attachment_formatter(attachment, color="#DCDEE0"):
    """Format a dict or string to become a slack attachment.

    If attachment is a dict, it will gave one item per key, titled by the name of the 
    key. If a string, there will be one item with an empty title.
    
    Basically copied verbatim from jarjar. Thx jeff :-)
    """
    result = dict(fallback="", color=color, fields=[], ts=time.time())
    attachment_dict = attachment if hasattr(attachment, "keys") else {"": attachment}
    for key in attachment_dict:

        if isinstance(attachment_dict[key], str):
            outval = attachment_dict[key]
        else:
            try:
                outval = str(attachment_dict[key])
            except UnicodeEncodeError:
                outval = unicode(attachment_dict[key])

        result["fields"].append(dict(title=key, value=outval, short=len(outval) < 20))
    return result


def attach_text_data(slacker, text_data, name, data_format, color):
    """Create an attachment for a blob of text data.

    Creates a monospace formatted attachment OR text file depending on user input
    and data length.

    - Attach a permalink to a file if asked or on auto and the data are too big.
    - Attach plain text if asked or if on auto and the data are small.
    - If attaching text explicitly and data are too big, text will be clipped.
    - Return None otherwise.
    """
    if data_format not in ("auto", "text", "file"):
        return

    is_long = len(text_data) > MAX_TEXT_LENGTH

    # if asked for a file, or if auto and the text are long, return a permalink to
    # the file
    if data_format == "file" or (data_format == "auto" and is_long):
        permalink = upload_file_get_permalink(
            slacker, content=text_data, filetype="text", filename=name, title=name
        )
        content = permalink or "error uploading file."
        title = "%s upload" % name
        return attachment_formatter({title: content}, color=color)

    # attach if the user asked or auto and the text are short
    if data_format == "text" or (data_format == "auto" and not is_long):
        content = text_data[:MAX_TEXT_LENGTH] + "\n[ ... ]" if is_long else text_data
        return attachment_formatter({"": "```%s```" % (content)}, color=color)
