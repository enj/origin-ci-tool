# I like to organize my imports by where they come from

from __main__ import display

import click  # Try to stick with 1 import type
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager

from ..config.options import default_options, default_inventory
from ..config.vars import default_vars


# double quotes in docstrings...
# all your classes need to inherit from object in python 2, else you get an old style class
# OR you can do this for easier python3 (copied from ansible code):

# Make coding more python3-ish
# from __future__ import (absolute_import, division, print_function)
# __metaclass__ = type

class PlaybookRunner:
    '''
    This class allows for a simple abstraction around the loading
    and execution of an Ansible playbook given an inventory and
    variables to expose to the playbook.
    '''

    def __init__(self,  # Don't put mutable objects in defaults, they get shared by all class instances
                 variable_manager=VariableManager(), data_loader=DataLoader(),
                 # options that we can default from config    ## maybe use **kwargs
                 become=None,
                 become_method=None,
                 become_user=None,
                 check=None,
                 connection=None,
                 forks=None,
                 host_list=None,
                 module_path=None,
                 passwords=None,
                 verbosity=None
                 ):
        """
        Initialize a PlaybookRunner.

        :param verbosity: verbosity level with which to run Ansible
        :param variable_manager: instance of an Ansible variable manager
        :param data_loader: instance of an Ansible data loader
        :param host_list: either a literal list of hosts or the path to an inventory file
        :param passwords: passwords to use when connection to remote hosts
        :param connection: what type of connection to use to connect to the host, one of ssh, local, docker
        :param module_path: path to third-party modules to load
        :param forks: number of parallel processes to spawn when communicating with remote hosts
        :param become: determine if privilege escalation should be activated
        :param become_method: method to use for privilege escalation
        :param become_user: user to assume in order to escalate priviliges
        :param check: do a dry run, simulating actions Ansible would take on a remote host
        """
        self._variable_manager = variable_manager
        self._data_loader = data_loader

        self._ansible_options = default_options(
            dict(
                connection=connection,
                module_path=module_path,
                forks=forks,
                become=become,
                become_method=become_method,
                become_user=become_user,
                check=check,
                verbosity=verbosity,
                # listing options, which we won't use here
                listhosts=None,
                listtasks=None,
                listtags=None,
                syntax=None
            )
        )

        display.verbosity = self._ansible_options.verbosity

        self._passwords = passwords
        self._inventory = Inventory(
            loader=self._data_loader,
            variable_manager=self._variable_manager,
            host_list=default_inventory(host_list)
        )
        self._variable_manager.set_inventory(self._inventory)

    def run(self, playbook_source, vars=None):  # maybe use **kwargs, don't use vars since vars() is a bultin
        """
        Run a playbook defined in the file at playbook_source with the variables provided.

        :param playbook_source: the location of the playbook to run
        :param vars: a dictionary of variables to pass to the playbook
        """
        vars = default_vars(vars)
        self._variable_manager.extra_vars = vars

        result = PlaybookExecutor(
            playbooks=[playbook_source],
            inventory=self._inventory,
            variable_manager=self._variable_manager,
            loader=self._data_loader,
            options=self._ansible_options,
            passwords=self._passwords
        ).run()

        if result is not TaskQueueManager.RUN_OK:  # don't use `is` when comparing integers, use `==`
            raise click.ClickException('Playbook execution failed with code ' + str(result))
            # I like to use `str.format` where possible but for a simple case like this `+` is probably fine
