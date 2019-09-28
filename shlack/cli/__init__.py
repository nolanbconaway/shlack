"""Init the shlack cli module."""
import click


def common_options(func):
    """Append common args to the command."""
    for option in reversed(
        [
            click.option(
                "-c",
                "--channel",
                "channel",
                type=str,
                envvar="SLACK_CHANNEL",
                help=(
                    "Channel to post within. Read from $SLACK_CHANNEL if not provided. "
                    "This can be a slack @username (though that is now deprecated), #channel or "
                    "user/channel ID."
                ),
            ),
            click.option(
                "-t",
                "--api-token",
                "oauth_api_token",
                default=None,
                type=str,
                envvar="SLACK_OAUTH_API_TOKEN",
                help="Oauth API Token. Read from $SLACK_OAUTH_API_TOKEN if not provided.",
            ),
        ]
    ):
        func = option(func)
    return func


@click.group()
def cli():
    """Send slack messages from the command line.
    
    This command line tool does nothing in tself, call one of the below described 
    subcommands to get started!
    """
    # Do nothing. All function is in the subcommands.
    pass
