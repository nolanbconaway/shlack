"""CLI handler for running a task."""
import sys
from io import StringIO

import click

from shlack import runner, slack

from . import common_options

_detach_help = (
    "Option to run the task in a detached process. "
    + "This is useful when you want to close your terminal / ssh session and let a "
    + "long task run. Default --detach."
)
_format_help = (
    "Format of stdout and stderr messages to send. If 'text', the data will be "
    + "sent as an attachment. If 'file' the data will be uploaded as a file. If "
    + "'auto', shlack will choose between file and text depending on the content "
    + "length. If 'none', nothing will be sent. Default 'auto'."
)


@click.command()
@click.argument("task", nargs=-1, type=str)
@click.option("--detach/--no-detach", "detach", default=True, help=_detach_help)
@click.option(
    "-f",
    "--out-format",
    "out_format",
    type=click.Choice({"text", "file", "auto", "none"}),
    default="auto",
    help=_format_help,
)
@common_options
def main(oauth_api_token, channel, detach, out_format, task):
    """Run a task and send a slack message after.
    
    $ shlack task 'sleep 5 && echo "FROM THE PAST!"' -c ... -t ...

    Wait 5 seconds and you should see a nicely formatted message in your slack 
    workspace.

    By default the task runs in a detached process and you'll only know its complete 
    when the slack message comes in. You can 

    """
    # if task is not defined, we are done
    if not task:
        click.echo("shlack task called without a task!")
        sys.exit(0)

    # define messenger
    slacker = slack.slacker_factory(api_key=oauth_api_token)
    command_joined = " ".join(task)

    def f():
        out, err = runner.shell_command(command_joined)

        # always attach a copy of the command
        attachments = [
            slack.attachment_formatter(
                {"": "```$ %s```" % (command_joined)}, color="#000000"
            )
        ]

        # add more attachments if asked for
        if out and out_format != "none":
            attachments.append(
                slack.attach_text_data(slacker, out, "stdout", out_format, "#439FE0")
            )

        if err and out_format != "none":
            attachments.append(
                slack.attach_text_data(slacker, err, "stderr", out_format, "danger")
            )

        # send the data
        slacker.chat.post_message(channel, "", attachments=attachments)

        # echo out if not detached
        if not detach:
            if out:
                click.echo(out)
            if err:
                click.echo(err)

        return 0 if err is None else 1

    if detach:
        runner.detachify(f)()
        sys.exit(0)

    # otherwise run in non-detached and exit if error
    sys.exit(f())


if __name__ == "__main__":
    main()
