"""Main module."""

from . import cli, message, task

cli.add_command(message.main, name="message")
cli.add_command(task.main, name="task")

if __name__ == "__main__":

    cli()
