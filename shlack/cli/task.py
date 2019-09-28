"""CLI handler for running a task."""
import subprocess
import sys

import click

from shlack.runner import detachify, shell_command
from shlack.slack import attachment_formatter, slacker_factory


@click.command()
@click.argument("task", nargs=-1, type=str)
@click.option(
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
)
@click.option(
    "-t",
    "--api-token",
    "oauth_api_token",
    default=None,
    type=str,
    envvar="SLACK_OAUTH_API_TOKEN",
    help="Oauth API Token. Read from $SLACK_OAUTH_API_TOKEN if not provided.",
)
def main(task, channel, oauth_api_token):
    """Run a task detachedly and send a slack message after."""
    # if task is not defined, we are done
    if not task:
        sys.exit(0)

    # define messenger
    slacker = slacker_factory(api_key=oauth_api_token)
    command_joined = " ".join(task)

    def f():
        out, err = shell_command(command_joined)

        attachments = []
        if out is not None:
            attachments.append(
                attachment_formatter({"": "```$ %s\n%s```" % (command_joined, out)})
            )

        if err is not None:
            attachments.append(
                attachment_formatter(
                    {"": "```$ %s\n%s```" % (command_joined, err)}, color="danger"
                )
            )

        status_message = (
            "succeeded" if err is None else "exited with nonzero exit status"
        )

        slacker.chat.post_message(
            channel,
            "Command `%s` %s." % (command_joined, status_message),
            attachments=attachments,
        )

    detachify(f)()


if __name__ == "__main__":
    main()
