import click
from cli.sync.git_options import git_options
from cli.sync.sync_options import sync_options
from cli.util.common_options import ansible_output_options
from cli.util.repository_options import repository_argument

_short_help = 'Synchronize a repository using local sources.'


@click.command(
    short_help=_short_help,
    help=_short_help + '''

text
'''
)
@repository_argument
@sync_options
@git_options
@ansible_output_options
def local(repository, sync_source, sync_destination, tag, refspec, branch, commit):
    pass
