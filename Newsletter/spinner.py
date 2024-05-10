# vim: fileencoding=utf-8

#
# Qubes OS Tweak Tools, https://github.com/alimirjamali/personal-qubesos
#
# Copyright (C) 2024  Ali Mirjamali <ali@mirjamali.com>
# Imporved Tweak Tool edition based on Qubes OS spinner by Wojtek Porczyk
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

'''Tweak Tool CLI spinner

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

SPINNERSET = '-\\|/'

TWEAKTOOL_SPINNERSET = ['    ▢     ',
                        '>   ◰    <',
                        ' >  ◳   < ',
                        '  > ◲  <  ',
                        '   >◱ <   ',
                        '    ▣     ',
                        '    ◾    ']

class AbstractSpinner(object):
    '''The base class for all Spinners

    :param stream: file-like object with ``.write()`` method
    :param str spinnerset: the sequence of characters to display

    The spinner should be used as follows:
        1. exactly one call to :py:meth:`show()`
        2. zero or more calls to :py:meth:`update()`
        3. exactly one call to :py:meth:`hide()`
    '''
    def __init__(self, stream, spinnerset=SPINNERSET):
        self.stream = stream
        self.spinnerset = itertools.cycle(spinnerset)

    def show(self, prompt):
        '''Show the spinner, with a prompt

        :param str prompt: prompt, like "please wait"
        '''
        raise NotImplementedError()

    def hide(self):
        '''Hide the spinner and the prompt'''
        raise NotImplementedError()

    def unhide(self):
        '''Unhide the spinner and the prompt'''
        raise NotImplementedError()

    def update(self):
        '''Show next spinner character'''
        raise NotImplementedError()


class DummySpinner(AbstractSpinner):
    '''Dummy spinner, does not do anything'''
    def show(self, prompt):
        pass

    def hide(self):
        pass

    def unhide(self):
        pass

    def update(self):
        pass


class SpinnerTweakToolEdition(AbstractSpinner):
    '''TweakTool spinner

    This is tty- and terminfo-aware spinner. Recommended.
    '''
    def __init__(self, stream, spinnerset=None, interleave=0):
        # our Enterprise + Tweak Tool logic follows
        self.counter = 0
        self.hidelen = 0
        self.cub1 = '\b'
        self.stream_isatty = stream.isatty()
        self.interleave = interleave
        if spinnerset is None:
            spinnerset = TWEAKTOOL_SPINNERSET if self.stream_isatty else '.'

        self.spinnerlen = len(spinnerset[0])
        super().__init__(stream, spinnerset)

        if self.stream_isatty:
            try:
                curses.setupterm()
                self.has_terminfo = True
                self.cub1 = curses.tigetstr('cub1').decode()
            except (curses.error, io.UnsupportedOperation):
                # we are in very non-Enterprise environment
                self.has_terminfo = False
        else:
            self.cub1 = ''

    def show(self, prompt):
        self.prompt = prompt
        self.hidelen = len(prompt) + 1 + self.spinnerlen
        self.unhide()

    def hide(self):
        if self.stream_isatty:
            hideseq = '\r' + ' ' * self.hidelen + '\r'
            if self.has_terminfo:
                hideseq_l = (curses.tigetstr('cr'), curses.tigetstr('clr_eol'))
                if all(seq is not None for seq in hideseq_l):
                    hideseq = ''.join(seq.decode() for seq in hideseq_l)
        else:
            hideseq = '\n'

        self.stream.write(hideseq)
        self.stream.flush()

    def unhide(self):
        self.counter = 0
        self.stream.write('{} {}'.format(self.prompt, next(self.spinnerset)))
        self.stream.flush()

    def update(self):
        ''' updating spinner very 20 lines '''
        if self.counter != self.interleave:
            self.counter += 1
            return
        else:
            self.counter = 0
        self.stream.write(self.cub1 * self.spinnerlen + next(self.spinnerset))
        self.stream.flush()

