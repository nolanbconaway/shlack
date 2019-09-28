"""CLI handler for running a task."""
import sys

import click

from shlack.runner import detachify, shell_command
from shlack.slack import attachment_formatter, slacker_factory

from . import common_options


@click.command()
@click.argument("task", nargs=-1, type=str)
@common_options
def main(oauth_api_token, channel, task):
    """Run a task detachedly and send a slack message after.
    
    $ shlack task 'sleep 5 && echo "FROM THE PAST!"' -c ... -t ...

    Wait 5 seconds and you should see a nicely formatted message in your slack 
    workspace.

    """
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
