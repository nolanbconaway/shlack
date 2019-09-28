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
