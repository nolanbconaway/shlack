"""CLI handler for running a task."""
import sys

import click

from shlack import slack

from . import common_options

_attach_help = (
    "A key value pair, where the key is the title of the attachment ('' "
    + "if not needed) and the value is the attachment body. Can be provided multiple "
    + "times, such as in -a key1 val1 -a key2 val2."
)


@click.command()
@click.argument("message", nargs=1, default="", type=str)
@click.option(
    "-a", "--attach", "attach", nargs=2, multiple=True, type=str, help=_attach_help
)
@click.option(
    "-u",
    "--upload",
    "upload",
    type=click.Path(exists=True),
    help="Option to upload a file.",
)
@common_options
def main(oauth_api_token, channel, message, attach, upload):
    """Send a message and/or attachments from the command line.

    Attachments can be provided as key-value pairs
    
    $ shlack message 'Look!' -a greet 'Hi!' -a date $(date) -c ... -t ...

    """
    # define messenger
    slacker = slack.slacker_factory(api_key=oauth_api_token)

    # format message elements
    if not attach:
        attachments = None
    else:
        attachments = [slack.attachment_formatter(dict(attach))]

    if message == "":
        message = None

    if upload is not None:

        if attachments is None:
            attachments = []

        permalink = slack.upload_file_get_permalink(slacker, file_=upload)
        attachments.append(slack.attachment_formatter({upload: permalink}))

    # exit if nothing to do
    if (None, None, None) == (message, attachments, upload):
        sys.exit(0)

    slacker.chat.post_message(
        channel, text=message, attachments=attachments, unfurl_links=True
    )


if __name__ == "__main__":
    main()
