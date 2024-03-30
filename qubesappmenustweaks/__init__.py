#!/usr/bin/python3
#
# The Qubes OS Project, http://www.qubes-os.org
# Ali's personal Qubes OS improvements, http://www.mirjamali.com
#
# Copyright (C) 2010  Joanna Rutkowska <joanna@invisiblethingslab.com>
# Copyright (C) 2013  Marek Marczykowski <marmarek@invisiblethingslab.com>
# Copyright (C) 2024  Ali Mirjamai <ali@mirjamali.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

""" My tweaks: Handle menu entries for starting applications in qubes"""

import os
import os.path
import itertools

import xdg.BaseDirectory
 
import qubesadmin
import qubesadmin.exc
import qubesadmin.tools
import qubesadmin.vm

import qubesimgconvertertweaks
from qubesimgconvertertweaks import Image
import qubesappmenus

basedir = os.path.join(xdg.BaseDirectory.xdg_data_home, 'qubes-appmenus')

class Appmenus(qubesappmenus.Appmenus):
    """Derived class for tweaked menu entries handling"""

    def appicons_create(self, vm, srcdirs=(), force=False):
        """Create/update applications icons"""
        if not srcdirs:
            srcdirs = self.template_icons_dirs(vm)
        if not srcdirs:
            return

        if vm.features.get('internal', False):
            return
        if vm.klass == 'DispVM' and vm.auto_cleanup:
            return

        whitelist = self.whitelist_path(vm)
        if 'menu-items' in vm.features:
            whitelist = vm.features['menu-items'].split(' ')
        elif os.path.exists(whitelist):
            with open(whitelist, encoding='utf-8') as whitelist_f:
                whitelist = [line.strip() for line in whitelist_f]
        else:
            whitelist = None

        dstdir = self.icons_dir(vm)
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        elif not os.path.isdir(dstdir):
            os.unlink(dstdir)
            os.makedirs(dstdir)

        if whitelist:
            expected_icons = [os.path.splitext(x)[0] + '.png'
                              for x in whitelist]
        else:
            expected_icons = list(itertools.chain.from_iterable(
                os.listdir(srcdir)
                for srcdir in srcdirs
                if os.path.exists(srcdir)))

        for icon in expected_icons:
            src_icon = self.template_for_file(srcdirs, icon)
            if not src_icon:
                continue

            dst_icon = os.path.join(dstdir, icon)
            if not os.path.exists(dst_icon) or force or \
                    os.path.getmtime(src_icon) > os.path.getmtime(dst_icon):

                img = Image.load_from_file_pil(src_icon)
                filter = vm.features.get("imgfilter", "tint")
                ''' Python 3.11 is nicely shipped with Qubes OS 4.2 ''' 
                ''' so we use match statement '''
                match filter:
                    case "tint":
                        img=img.tint(vm.label.color)
                    case "overlay":
                        img=img.overlay(vm.label.color)
                    case "thin-border":
                        img=img.border(vm.label.color, 10./3.)
                    case "thick-border":
                        img=img.border(vm.label.color, 20./3.)
                    case "untouched":
                        img=img.untouched()
                    case "invert":
                        img=img.invert()
                    case "mirror":
                        img=img.mirror(1)
                    case "flip":
                        img=img.mirror(0)
                    case _:
                        img=img.tint(args.colour)
                img.save_pil(dst_icon)

        for icon in os.listdir(dstdir):
            if icon not in expected_icons:
                os.unlink(os.path.join(dstdir, icon))


