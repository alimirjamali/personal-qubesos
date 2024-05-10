# vim: fileencoding=utf-8

#
# Qubes OS Tweak Tools, https://github.com/alimirjamali/personal-qubesos
#
# Copyright (C) 2017  Wojtek Porczyk <woju@invisiblethingslab.com>
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
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#

'''Qubes CLI spinner Tweaks

A novice asked the master: “In the east there is a great tree-structure that
men call 'Corporate Headquarters'. It is bloated out of shape with vice
presidents and accountants. It issues a multitude of memos, each saying 'Go,
Hence!' or 'Go, Hither!' and nobody knows what is meant. Every year new names
are put onto the branches, but all to no avail. How can such an unnatural
entity be?"

The master replied: “You perceive this immense structure and are disturbed that
it has no rational purpose. Can you not take amusement from its endless
gyrations? Do you not enjoy the untroubled ease of programming beneath its
sheltering branches? Why are you bothered by its uselessness?”

(Geoffrey James, “The Tao of Programming”, 7.1)
'''

import curses
import io
import itertools

from qubesadmin.spinner import QubesSpinnerEnterpriseEdition

BRAILLE_CHARSET = "⠁⠉⠈⠘⠸⠰⠠⠤⠄⠆⠇⠃"

class QubesSpinnerTweakToolEdition(QubesSpinnerEnterpriseEdition):
    '''Tweak Tool spinner

    Currently it uses the QubesSpinnerEnterpriseEdition code. To be improved...
    '''
    def __init__(self, stream, charset=None):
        self.stream_isatty = stream.isatty()
        if charset is None:
            charset = BRAILLE_CHARSET if self.stream_isatty else '.'

        super().__init__(stream, charset)


