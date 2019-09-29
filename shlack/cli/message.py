"""CLI handler for running a task."""
import click

from shlack.slack import attachment_formatter, slacker_factory

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
@common_options
def main(oauth_api_token, channel, message, attach):
    """Send a message and/or attachments from the command line.

    Attachments can be provided as key-value pairs
    
    $ shlack message 'Look!' -a greet 'Hi!' -a date $(date) -c ... -t ...

    """
    # define messenger
    slacker = slacker_factory(api_key=oauth_api_token)

    # format message elements
    if not attach:
        attachments = None
    else:
        attachments = [attachment_formatter(dict(attach))]

    if message == "":
        message = None

    slacker.chat.post_message(channel, text=message, attachments=attachments)


if __name__ == "__main__":
    main()
