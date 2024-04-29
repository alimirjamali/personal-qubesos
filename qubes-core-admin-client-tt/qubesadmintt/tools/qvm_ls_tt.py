# pylint: disable=too-few-public-methods

#
# The Qubes OS Project, https://www.qubes-os.org/
#
# Copyright (C) 2015  Joanna Rutkowska <joanna@invisiblethingslab.com>
# Copyright (C) 2015  Wojtek Porczyk <woju@invisiblethingslab.com>
# Copyright (C) 2017 Marek Marczykowski-Górecki
#                               <marmarek@invisiblethingslab.com>
# Copyright (C) 2024 Ali Mirjamali <ali@mirjamali.com>
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
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

''' qvm-ls-tt - List available domains Tweak Tool '''

''' Removing or commenting as many as possible unused dependencies '''
import argparse
import sys
import textwrap
import qubesadmin
import qubesadmintt.tools
import qubesadmin.utils
import qubesadmin.vm
import qubesadmin.exc

''' importing as few as possible methods and classes from original qvm-ls    '''
''' Only overriding whatever we want to change                               '''
from qubesadmin.tools.qvm_ls import Column, PropertyColumn, FlagsColumn,\
    calc_size, calc_usage, calc_used, Table, _HelpColumnsAction,\
    _HelpFormatsAction, matches_power_states, formats

''' Importing our own Tweak Tool libraries '''
import qubesadmintt.spinner

# todo maxmem: DONE
Column('MAXMEM',
    attr=(lambda vm: vm.maxmem if vm.virt_mode=="pvh" else None),
    doc='Memory currently used by VM')

Column('STATE',
    attr=(lambda vm: vm.get_power_state()),
    doc='Current power state.')

Column('CLASS',
    attr=(lambda vm: vm.klass),
    doc='Class of the qube.')

Column('GATEWAY',
    attr='netvm.gateway',
    doc='Network gateway.')

Column('MEMORY',
    attr=(lambda vm: vm.get_mem() // 1024 if vm.is_running() else None),
    doc='Memory currently used by VM')

Column('INITIALMEM',
    attr=(lambda vm: vm.memory),
    doc='Memory currently used by VM')

Column('DISK',
    attr=(lambda vm: vm.get_disk_utilization() // 1024 // 1024),
    doc='Total disk utilisation.')

Column('PRIV-CURR',
    attr=(lambda vm: calc_usage(vm, 'private')),
    doc='Disk utilisation by private image (/home, /usr/local).')

Column('PRIV-MAX',
    attr=(lambda vm: calc_size(vm, 'private')),
    doc='Maximum available space for private image.')

Column('PRIV-USED',
    attr=(lambda vm: calc_used(vm, 'private')),
    doc='Disk utilisation by private image as a percentage of available space.')

Column('ROOT-CURR',
    attr=(lambda vm: calc_usage(vm, 'root')),
    doc='Disk utilisation by root image (/usr, /lib, /etc, ...).')

Column('ROOT-MAX',
    attr=(lambda vm: calc_size(vm, 'root')),
    doc='Maximum available space for root image.')

Column('ROOT-USED',
    attr=(lambda vm: calc_used(vm, 'root')),
    doc='Disk utilisation by root image as a percentage of available space.')

FlagsColumn()

#: Additional Tweak Tool formats. Main ones are in qvm_ls.py.
formats['perf']=('name', 'label', 'template', 'netvm', 'vcpus', 'initialmem', 
         'maxmem', 'virt_mode')

# common VM power states for easy command-line filtering
DOMAIN_POWER_STATES = ['running', 'paused', 'halted']

def get_parser():
    '''Create :py:class:`argparse.ArgumentParser` suitable for
    :program:`qvm-ls`.
    '''
    # parser creation is delayed to get all the columns that are scattered
    # thorough the modules

    wrapper = textwrap.TextWrapper(width=80, break_on_hyphens=False,
        initial_indent='  ', subsequent_indent='  ')

    parser = qubesadmintt.tools.QubesArgumentParser(
        vmname_nargs=argparse.ZERO_OR_MORE,
        formatter_class=argparse.RawTextHelpFormatter,
        description='List Qubes domains and their parameters.',
        epilog='available formats (see --help-formats):\n{}\n\n'
               'available columns (see --help-columns):\n{}'.format(
                wrapper.fill(', '.join(sorted(formats.keys()))),
                wrapper.fill(', '.join(sorted(sorted(Column.columns.keys()))))))

    parser.add_argument('--help-columns', action=_HelpColumnsAction)
    parser.add_argument('--help-formats', action=_HelpFormatsAction)

    parser_formats = parser.add_mutually_exclusive_group()

    parser_formats.add_argument('--format', '-o', metavar='FORMAT',
        action='store', choices=formats.keys(), default='simple',
        help='preset format')

    parser_formats.add_argument('--fields', '-O', metavar='FIELD,...',
        action='store',
        help='user specified format (see available columns below)')

    parser.add_argument('--tags', nargs='+', metavar='TAG',
        help='show only VMs having specific tag(s)')

    for pwrstate in DOMAIN_POWER_STATES:
        parser.add_argument('--{}'.format(pwrstate), action='store_true',
            help='show {} VMs'.format(pwrstate))

    parser.add_argument('--class', metavar='AppVM,TemplateVM,...', dest='klass',
        action='store',
        help='show only VMs with specific class(es)')

    parser.add_argument('--label', metavar='red,green,...',
        action='store',
        help='show only VMs with specific label(s)')

    parser.add_argument('--internal', metavar='<yes|no|both>', default='both',
        action='store', choices=['y', 'yes', 'n', 'no', 'both'],
            help='show only internal VMs or option to hide them. '
                'default is showing both regular & internal VMs.')

    parser.add_argument('--servicevm', metavar='<yes|no|both>', default='both',
        action='store', choices=['y', 'yes', 'n', 'no', 'both'],
            help='show only Service VMs or option to hide them. '
                'default is showing both regular & Service VMs.')

    parser.add_argument('--raw-data', action='store_true',
        help='Display specify data of specified VMs. Intended for '
             'bash-parsing.')

    parser.add_argument('--tree', '-t',
        action='store_const', const='tree',
        help='sort domain list as network tree')

    parser.add_argument('--spinner',
        action='store_true', dest='spinner',
        help='reenable spinner')

    parser.add_argument('--no-spinner',
        action='store_false', dest='spinner',
        help='disable spinner')

    # shortcuts, compatibility with Qubes 3.2
    parser.add_argument('--raw-list', action='store_true',
        help='Same as --raw-data --fields=name')

    parser.add_argument('--disk', '-d',
        action='store_const', dest='format', const='disk',
        help='Same as --format=disk')

    parser.add_argument('--network', '-n',
        action='store_const', dest='format', const='network',
        help='Same as --format=network')

    parser.add_argument('--kernel', '-k',
        action='store_const', dest='format', const='kernel',
        help='Same as --format=kernel')

    parser.set_defaults(spinner=True)

#   parser.add_argument('--conf', '-c',
#       action='store', metavar='CFGFILE',
#       help='Qubes config file')

    return parser


def main(args=None, app=None):
    '''Main routine of :program:`qvm-ls`.

    :param list args: Optional arguments to override those delivered from \
        command line.
    :param app: Operate on given app object instead of instantiating new one.
    '''

    parser = get_parser()
    try:
        args = parser.parse_args(args, app=app)
    except qubesadmin.exc.QubesException as e:
        parser.print_error(str(e))
        return 1

    # fetch all the properties with one Admin API call, instead of issuing
    # one call per property
    args.app.cache_enabled = True

    if args.raw_list:
        args.raw_data = True
        args.fields = 'name'

    if args.fields:
        columns = [col.strip() for col in args.fields.split(',')]
    else:
        columns = formats[args.format]

    # assume unknown columns are VM properties
    for col in columns:
        if col.upper() not in Column.columns:
            PropertyColumn(col.lower())

    if args.spinner and not args.raw_data:
        # we need Enterprise Edition™, since it's the only one that detects TTY
        # and uses dots if we are redirected somewhere else
        spinner = qubesadmintt.spinner.QubesSpinnerTweakToolEdition(sys.stderr)
    else:
        spinner = qubesadmin.spinner.DummySpinner(sys.stderr)

    if args.domains:
        domains = args.domains
    else:
        domains = args.app.domains

    if args.all_domains:
        # Normally, --all means "all domains except for AdminVM".
        # However, in the case of qvm-ls it does not make sense to exclude
        # AdminVMs, so we override the list from parser.
        domains = [
            vm for vm in args.app.domains if vm.name not in args.exclude
        ]

    if args.tags:
        # filter only VMs having at least one of the specified tags
        domains = [dom for dom in domains
                   if set(dom.tags).intersection(set(args.tags))]

    pwrstates = {state: getattr(args, state) for state in DOMAIN_POWER_STATES}
    domains = [d for d in domains
               if matches_power_states(d, **pwrstates)]

    if args.klass:
        domains = [d for d in domains if d.klass in args.klass.split(',')]

    ''' ToDo: Move to Tables class for acceleration '''
    if args.label:
        domains_labeled = list()
        spinner.show('Filtering based on labels...')
        for d in domains:
            if d.label.name in args.label.split(','):
                domains_labeled.append(d)
            spinner.update()
        domains = domains_labeled
        spinner.hide()

    if args.internal in ['y', 'yes', 'true', '1']:
        domains = [d for d in domains if d.features.get('internal', None)
                   in ['1', 'true', 'True']]
    elif args.internal in ['n', 'no', 'false', '0']:
        domains = [d for d in domains if not d.features.get('internal', None)
                   in ['1', 'true', 'True']]

    if args.servicevm in ['y', 'yes', 'true', '1']:
        domains = [d for d in domains if d.features.get('servicevm', None)
                   in ['1', 'true', 'True']]
    elif args.internal in ['n', 'no', 'false', '0']:
        domains = [d for d in domains if not d.features.get('servicevm', None)
                   in ['1', 'true', 'True']]

    table = Table(domains, columns, spinner, args.raw_data, args.tree)
    table.write_table(sys.stdout)

    return 0

if __name__ == '__main__':
    sys.exit(main())
