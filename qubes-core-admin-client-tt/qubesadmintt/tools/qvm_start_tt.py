# -*- encoding: utf8 -*-
#
# The Qubes OS Project, http://www.qubes-os.org
#
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
# with this program; if not, see <http://www.gnu.org/licenses/>.

'''qvm-start-tt - start a domain'''
import argparse
import string
import sys

import subprocess

import time

import qubesadmin.devices
import qubesadmin.exc
''' Only Tweak is Wildcard support '''
import qubesadmintt.tools
from qubesadmin.tools.qvm_start import DriveAction, get_drive_assignment


parser = qubesadmintt.tools.QubesArgumentParser(
    description='start a domain', vmname_nargs='+')

parser.add_argument('--skip-if-running',
    action='store_true', default=False,
    help='Do not fail if the qube is already runnning')

parser_drive = parser.add_mutually_exclusive_group()

parser_drive.add_argument('--drive', metavar='DRIVE',
    help='temporarily attach specified drive as CD/DVD or hard disk (can be'
        ' specified with prefix "hd:" or "cdrom:", default is cdrom)')

parser_drive.add_argument('--hddisk',
    action=DriveAction, dest='drive', prefix='hd:',
    help='temporarily attach specified drive as hard disk')

parser_drive.add_argument('--cdrom', metavar='IMAGE',
    action=DriveAction, dest='drive', prefix='cdrom:',
    help='temporarily attach specified drive as CD/DVD')

parser_drive.add_argument('--install-windows-tools',
    action='store_const', dest='drive', default=False,
    const='cdrom:dom0:/usr/lib/qubes/qubes-windows-tools.iso',
    help='temporarily attach Windows tools CDROM to the domain')


def main(args=None, app=None):
    '''Main routine of :program:`qvm-start`.

    :param list args: Optional arguments to override those delivered from \
        command line.
    '''

    args = parser.parse_args(args, app=app)

    exit_code = 0
    for domain in args.domains:
        if domain.is_running():
            if args.skip_if_running:
                continue
            exit_code = 1
            parser.print_error(
                    'domain {} is already running'.format(domain.name))
            return exit_code
        drive_assignment = None
        try:
            if args.drive:
                drive_assignment = get_drive_assignment(args.app, args.drive)
                try:
                    domain.devices['block'].attach(drive_assignment)
                except:
                    drive_assignment = None
                    raise

            domain.start()

            if drive_assignment:
                # don't reconnect this device after VM reboot
                domain.devices['block'].update_persistent(
                    drive_assignment.device, False)
        except (IOError, OSError, qubesadmin.exc.QubesException,
                ValueError) as e:
            if drive_assignment:
                try:
                    domain.devices['block'].detach(drive_assignment)
                except qubesadmin.exc.QubesException:
                    pass
            exit_code = 1
            parser.print_error(str(e))

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
