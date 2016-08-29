import __main__
import click
from ansible.utils.display import Display
from cli.build.group import build
from cli.config.group import config
from cli.install.group import install
from cli.prepare.group import prepare
from cli.provision.group import provision
from cli.sync.group import sync
from cli.test.group import test

__main__.display = Display(verbosity=10)


@click.group(
    help='''
A CLI tool for building, testing and composing OpenShift repositories.
'''
)
def oct():
    """
    Do nothing -- this group should never be called without a sub-command.
    """

    pass


oct.add_command(build)
oct.add_command(config)
oct.add_command(install)
oct.add_command(prepare)
oct.add_command(provision)
oct.add_command(sync)
oct.add_command(test)
