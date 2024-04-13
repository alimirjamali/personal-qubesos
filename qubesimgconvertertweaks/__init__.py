#!/usr/bin/python3 -O

# The Qubes OS Project, http://www.qubes-os.org
#
# Ali's personal Qubes OS improvements, http://www.mirjamali.com
#
# Copyright (C) 2013  Wojciech Porczyk <wojciech@porczyk.eu>
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import qubesimgconverter
from qubesimgconverter import hex_to_int
import numpy

'''Note to self: qubesimgconverter.Image.tint is using numpy's old- '''
'''deprecated binary mode of fromstring. as it behaves surprisingly-'''
'''on unicode inputs. Use of frombuffer is recommended. However,-   '''
'''this should  not be a security hazard here. No need for patches. '''

class Image(qubesimgconverter.Image):
    def __init__(self, rgba, size):
          super().__init__(rgba, size) 

    def ANSI(self):
        '''Printing representation of image with ANSI escape codes'''

        pixels = numpy.frombuffer(self._rgba, dtype='B').reshape(\
                self.height, self.width, 4)
        for row in pixels:
            for pixel in row:
                r, g, b, a = pixel[:]
                print("\033[48;2;%d;%d;%dm  " % (r, g, b), end='')
            print("\033[0m")

    def overlay(self, colour):
        ''' Overlay image on a solid block of color, using its Alpha channel '''

        rb, gb, bb = hex_to_int(colour)

        pixels = numpy.frombuffer(self._rgba, dtype='B').reshape(\
                self.height * self.width, 4)
        r = pixels[:, 0].astype('u4')
        g = pixels[:, 1].astype('u4')
        b = pixels[:, 2].astype('u4')
        a = pixels[:, 3].astype('u4')
        r = (((a * r) + (255 - a) * rb) / 256).astype('B')
        g = (((a * g) + (255 - a) * gb) / 256).astype('B')
        b = (((a * b) + (255 - a) * bb) / 256).astype('B')
        a[:] = 255
        pixelso = numpy.column_stack((r, g, b, a.astype('B')))
        return self.__class__(rgba=pixelso.tobytes(), size=self._size)

    def border(self, colour, percent):
        ''' Apply a border of colour to image. No antialiasing for now '''
        ''' percent if minimum of (width, height) '''

        rb, gb, bb = hex_to_int(colour)
        if  min(self.height, self.width) <= 16:
            width = 1
        else:
            width = int(min(self.height, self.width) * percent / 100.)

        pixels = numpy.frombuffer(self._rgba, dtype='B').reshape(\
                self.height, self.width, 4)
        pixelsb = pixels.astype('u4')
        pixelsb[0:width, :] = rb, gb, bb, 255
        pixelsb[:, 0:width] = rb, gb, bb, 255
        pixelsb[-width:, :] = rb, gb, bb, 255
        pixelsb[:, -width:] = rb, gb, bb, 255
        return self.__class__(rgba=pixelsb.astype('B').tobytes(), \
                size=self._size)

    def thin_border(self, color):
        return self.border(color, 3.125)

    def thick_border(self, color):
        return self.border(color, 6.25)

    def untouched(self):
        ''' Returning the untouched image '''
        return self

    def invert(self):
        ''' Inverting image for a paranoid effect '''

        pixels = numpy.frombuffer(self._rgba, dtype='B').reshape(\
                self.height * self.width, 4)
        ri = 255 - pixels[:, 0]
        gi = 255 - pixels[:, 1]
        bi = 255 - pixels[:, 2]
        a = pixels[:, 3]
        pixelst = numpy.column_stack((ri, gi, bi, a))
        return self.__class__(rgba=pixelst.tobytes(), size=self._size)

    def mirror(self, axes):
        ''' Mirror/flip image vertically. I guess no one would use this'''

        pixels = numpy.frombuffer(self._rgba, dtype='B').reshape(\
                self.height, self.width, 4)
        pixels = numpy.flip(pixels, axes)
        return self.__class__(rgba=pixels.astype('B'), size=self._size)

# vim: ft=python sw=4 ts=4 et
