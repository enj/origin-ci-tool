import click
from cli.sync.git_options import git_options
from cli.sync.sync_options import sync_destination_option
from cli.util.common_options import ansible_output_options
from cli.util.repository_options import repository_argument, Repository

_short_help = 'Synchronize a repository using remote servers.'


@click.command(
    short_help=_short_help,
    help=_short_help + '''

text
'''
)
@repository_argument
@sync_destination_option
@click.option(
    '--remote', '-r',
    default='origin',
    show_default=True,
    help='Git remote to use.'
)
@click.option(
    '--new-remote', '-n',
    'new_remote',
    nargs=2,
    help='Git remote to install and use.'
)
@git_options
@ansible_output_options
def remote(repository, sync_source, sync_destination, tag, remote, new_remote, refspec, branch, commit):
    """
    Synchronize the repository on the remote host from a
    remote server.

    :param repository:
    :param remote:
    :param new_remote:
    :param refspec:
    :param branch:
    :param commit:
    """
    validate_repository(repository)


def validate_repository(repository):
    """
    Validate that the repository can be synchronized
    using remote servers. Private repositories that
    exist on servers that require authentication cannot
    be synchronized from their remotes and must be updated
    using a local push instead.

    :param repository: repository to validate
    """
    if repository == Repository.enterprise:
        raise click.UsageError('Synchronizing the %s repository using remote servers is not supported.' % repository)
