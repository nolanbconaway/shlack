"""Init the shlack cli module."""
import click

from shlack.cli import task


@click.group()
def entry_point():
    """Command line handlers for MTA realtime data."""


entry_point.add_command(task.main, name="task")
