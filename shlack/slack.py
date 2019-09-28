"""Utilities for interacting with the slack API."""
import copy
import os
import subprocess
import time

from slacker import Slacker


def slacker_factory(api_key=None):
    """Return a slacker object, getting the API key from the user or env."""
    if api_key is None:
        api_key = os.getenv("SLACK_OAUTH_API_TOKEN")
        if api_key is None:
            raise EnvironmentError("No Oauth API key provided!")

    return Slacker(api_key)


def attachment_formatter(attachment_dict, color="#DCDEE0"):
    """Format a dict to become a slack attachment.
    
    Basically copied verbatim from jarjar. Thx jeff :-)
    """
    attachments = dict(fallback="", color=color, fields=[], ts=time.time())

    for key in attachment_dict:

        if isinstance(attachment_dict[key], str):
            outval = attachment_dict[key]
        else:
            try:
                outval = str(attachment_dict[key])
            except UnicodeEncodeError:
                outval = unicode(attachment_dict[key])

        attachments["fields"].append(
            dict(title=key, value=outval, short=len(outval) < 20)
        )
    return [attachments]
