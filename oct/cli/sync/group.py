import click
from cli.sync.local import local
from cli.sync.remote import remote

_short_help = 'Update the Git state of repositories on the virtual machine.'


@click.group(
    short_help=_short_help,
    help=_short_help + '''

text
'''
)
def sync():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


sync.add_command(local)
sync.add_command(remote)