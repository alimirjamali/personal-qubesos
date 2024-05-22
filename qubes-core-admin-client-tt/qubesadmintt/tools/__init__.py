# encoding=utf-8
#
# The Qubes OS Project, https://www.qubes-os.org/
#
# Copyright (C) 2015  Joanna Rutkowska <joanna@invisiblethingslab.com>
# Copyright (C) 2015  Wojtek Porczyk <woju@invisiblethingslab.com>
# Copyright (C) 2024  Ali Mirjamali <ali@mirjamali.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2.1 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

''' Qubes' command line Tweak Tools '''

''' Removing or commenting as many as possible unused dependencies '''
import argparse
import logging
import os
import sys

import qubesadmin.log
import qubesadmin

''' importing methods and classes from original qubesadmin.tools'''
from qubesadmin.tools import get_parser_for_command, print_table
from qubesadmin.tools import QubesAction, PropertyAction, SinglePropertyAction,\
        RunningVmNameAction, VolumeAction, VMVolumeAction, PoolsAction,\
        SubParsersHelpAction, AliasedSubParsersAction
''' Only overriding whatever we want to change: '''
from qubesadmin.tools import VmNameAction, VmNameGroup
''' QubesArgumentParser is totally modifed to allow our own VmNameAction '''

''' importing fnmatch for Unix like wildcard support for destination VMs '''
import fnmatch

#: constant returned when some action should be performed on all qubes
VM_ALL = object()


class VmNameAction(qubesadmin.tools.VmNameAction):
    ''' Action for parsing one or multiple domains from provided VMNAMEs '''
    def __init__(self, option_strings, nargs=1, dest='vmnames', help=None,
                 **kwargs):
        super().__init__(option_strings, nargs=nargs, dest=dest, help=help,
                       **kwargs)

    ''' Only overriding parse_qubes_app method to add Unix like wildcards '''
    def parse_qubes_app(self, parser, namespace):
        assert hasattr(namespace, 'app')
        setattr(namespace, 'domains', [])
        app = namespace.app
        if hasattr(namespace, 'all_domains') and namespace.all_domains:
            namespace.domains = [
                vm
                for vm in app.domains
                if not vm.klass == 'AdminVM' and
                   vm.name not in namespace.exclude
            ]
        else:
            if hasattr(namespace, 'exclude') and namespace.exclude:
                parser.error('--exclude can only be used with --all')

            ''' Adding Unix like Wildcard support to destinations '''
            domains_names = [domain.name for domain in app.domains]
            destinations=set()
            for domain_name in domains_names:
                for vm_name in getattr(namespace, self.dest, None):
                    if vm_name is not None:
                        if fnmatch.fnmatch(domain_name, vm_name):
                            destinations.add(domain_name)
            setattr(namespace, self.dest, list(destinations))

            if self.nargs == argparse.OPTIONAL:
                if getattr(namespace, 'dispvm', None) is not None:
                    return
                vm_name = getattr(namespace, self.dest, None)
                if vm_name is not None:
                    try:
                        namespace.domains += [app.domains[vm_name]]
                    except KeyError:
                        parser.error('no such domain: {!r}'.format(vm_name))
            else:
                for vm_name in getattr(namespace, self.dest):
                    try:
                        namespace.domains += [app.domains[vm_name]]
                    except KeyError:
                        parser.error('no such domain: {!r}'.format(vm_name))

class QubesArgumentParser(argparse.ArgumentParser):
    '''Parser preconfigured for use in most of the Qubes command-line tools.

    :param mixed vmname_nargs: The number of ``VMNAME`` arguments that should be
        consumed. Values include:
        * N (an integer) consumes N arguments (and produces a list)
        * '?' consumes zero or one arguments
        * '*' consumes zero or more arguments (and produces a list)
        * '+' consumes one or more arguments (and produces a list)

    :param show_forceroot: don't hide --force-root parameter, prevent running
        as root unless it is given

    *kwargs* are passed to :py:class:`argparser.ArgumentParser`.

    Currenty supported options:
        ``--force-root`` (optional, ignored, help is suppressed)
        ``--offline-mode`` do not talk to hypervisor (help is suppressed)
        ``--verbose`` and ``--quiet``
    '''

    def __init__(self, vmname_nargs=None, show_forceroot=False, **kwargs):

        super().__init__(add_help=False, **kwargs)

        self._vmname_nargs = vmname_nargs

        self.add_argument('--verbose', '-v', action='count',
                          help='increase verbosity')

        self.add_argument('--quiet', '-q', action='count',
                          help='decrease verbosity')

        if show_forceroot:
            self.add_argument(
                '--force-root', action='store_true',
                default=False,
                help="Force running the tool even if called as root")
        else:
            self.add_argument('--force-root', action='store_true',
                              default=False, help=argparse.SUPPRESS)
        self._complain_if_root = show_forceroot

        self.add_argument('--help', '-h', action=SubParsersHelpAction,
                          help='show this help message and exit')

        if self._vmname_nargs in [argparse.ZERO_OR_MORE, argparse.ONE_OR_MORE]:
            vm_name_group = VmNameGroup(self,
                required=(self._vmname_nargs
                          not in [argparse.ZERO_OR_MORE, argparse.OPTIONAL]))
            self._mutually_exclusive_groups.append(vm_name_group)
        elif self._vmname_nargs is not None:
            self.add_argument('VMNAME', nargs=self._vmname_nargs,
                              action=VmNameAction)

        self.set_defaults(verbose=1, quiet=0)

    def parse_args(self, *args, **kwargs):
        # pylint: disable=arguments-differ,signature-differs
        # hack for tests
        app = kwargs.pop('app', None)
        namespace = super().parse_args(*args, **kwargs)

        if self._complain_if_root and \
                os.getuid() == 0 and \
                not namespace.force_root:
            self.error('refusing to run as root; add --force-root to override')

        self.set_qubes_verbosity(namespace)
        if app is not None:
            namespace.app = app
        else:
            namespace.app = qubesadmin.Qubes()

        for action in self._actions:
            # pylint: disable=protected-access
            if issubclass(action.__class__, QubesAction):
                action.parse_qubes_app(self, namespace)
            elif issubclass(action.__class__,
                    argparse._SubParsersAction):  # pylint: disable=no-member
                assert hasattr(namespace, 'command')
                command = namespace.command
                if command is None:
                    continue
                subparser = action._name_parser_map[command]
                for subaction in subparser._actions:
                    if issubclass(subaction.__class__, QubesAction):
                        subaction.parse_qubes_app(self, namespace)

        return namespace

    def error_runtime(self, message, exit_code=1):
        '''Runtime error, without showing usage.

        :param str message: message to show
        '''
        self.exit(exit_code, '{}: error: {}\n'.format(self.prog, message))


    @staticmethod
    def get_loglevel_from_verbosity(namespace):
        ''' Return loglevel calculated from quiet and verbose arguments '''
        return (namespace.quiet - namespace.verbose) * 10 + logging.WARNING


    @staticmethod
    def set_qubes_verbosity(namespace):
        '''Apply a verbosity setting.

        This is done by configuring global logging.
        :param argparse.Namespace args: args as parsed by parser
        '''

        verbose = namespace.verbose - namespace.quiet

        if verbose >= 2:
            qubesadmin.log.enable_debug()
        elif verbose >= 1:
            qubesadmin.log.enable()

    def print_error(self, *args, **kwargs):
        ''' Print to ``sys.stderr``'''
        print(*args, file=sys.stderr, **kwargs)


class VmNameGroup(qubesadmin.tools.VmNameGroup):
    def __init__(self, container, required, vm_action=VmNameAction, help=None):
        super().__init__(container=container, required=required,\
                vm_action=vm_action, help=help)

