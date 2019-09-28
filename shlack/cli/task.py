"""CLI handler for running a task."""
import sys

import click

from shlack.runner import detachify, shell_command
from shlack.slack import attachment_formatter, slacker_factory

from . import common_options

_detach_help = (
    "Option to run the task in a detached process. "
    + "This is useful when you want to close your terminal / ssh session and let a "
    + "long task run. Default --detach."
)


@click.command()
@click.argument("task", nargs=-1, type=str)
@click.option("--detach/--no-detach", "detach", default=True, help=_detach_help)
@common_options
def main(oauth_api_token, channel, detach, task):
    """Run a task and send a slack message after.
    
    $ shlack task 'sleep 5 && echo "FROM THE PAST!"' -c ... -t ...

    Wait 5 seconds and you should see a nicely formatted message in your slack 
    workspace.

    By default the task runs in a detached process and you'll only know its complete 
    when the slack message comes in. You can 

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

        # echo out if not detached
        if not detach:
            if out is not None:
                click.echo(out)
            if err is not None:
                click.echo(err)

        return 0 if err is None else 1

    if detach:
        detachify(f)()
        sys.exit(0)

    # otherwise run in non-detached and exit if error
    sys.exit(f())


if __name__ == "__main__":
    main()
