"""CLI handler for running a task."""
import sys
from io import StringIO

import click

from shlack import runner, slack

from . import common_options

MAX_TEXT_LENGTH = 750

_detach_help = (
    "Option to run the task in a detached process. "
    + "This is useful when you want to close your terminal / ssh session and let a "
    + "long task run. Default --detach."
)
_format_help = (
    "Format of stdout and stderr messages to send. If 'attach', the data will be "
    + "sent as an attachment. If 'file' the data will be uploaded as a file. If "
    + "'auto', shlack will choose between file and text depending on the content "
    + "length. If 'none', nothing will be sent. Default 'auto'."
)


def attach_output(slacker, text_data, name, out_format, color):
    """Get the attachment the user wants :-).

    Attach a permalink to a file if asked or on auto and appropriate.
    Attach plain text otherwise, clipping at 1k characters if too long.
    Return None if the user did not ask for output
    """
    # do nothing if no output
    if out_format == "none":
        return

    is_long = len(text_data) > MAX_TEXT_LENGTH

    # if asked for a file, or if auto and the text are long, return a permalink to
    # the file
    if out_format == "file" or (out_format == "auto" and is_long):
        permalink = slack.upload_file_get_permalink(
            slacker, content=text_data, filetype="text", filename=name, title=name
        )
        content = permalink or "`SlackError` raised."
        title = "%s upload" % name
        return slack.attachment_formatter({title: content}, color=color)

    # attach if the user asked or auto and the text are short
    if out_format == "text" or (out_format == "auto" and not is_long):
        content = text_data[:MAX_TEXT_LENGTH] + "\n[ ... ]" if is_long else text_data
        return slack.attachment_formatter({"": "```%s```" % (content)}, color=color)


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
                attach_output(slacker, out, "stdout", out_format, "#439FE0")
            )

        if err and out_format != "none":
            attachments.append(
                attach_output(slacker, err, "stderr", out_format, "danger")
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
