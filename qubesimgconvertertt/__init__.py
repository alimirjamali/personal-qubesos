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
import math

'''Note to self: qubesimgconverter.Image.tint is using numpy's old- '''
'''deprecated binary mode of fromstring. as it behaves surprisingly-'''
'''on unicode inputs. Use of frombuffer is recommended. However,-   '''
'''this should  not be a security hazard here. No need for patches. '''

class Image(qubesimgconverter.Image):
    def __init__(self, rgba, size):
          super().__init__(rgba, size) 

    def ANSI(self):
        '''Printing representation of image with ANSI escape codes'''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height, self.width, 4)
        for row in pixels:
            for pixel in row:
                r, g, b = pixel[:3]
                print("\033[48;2;%d;%d;%dm  " % (r, g, b), end='')
            print("\033[0m")

    def alphacompositor(self, back):
        ''' Compositing Image on top of another Image. See: '''
        ''' https://en.wikipedia.org/wiki/Alpha_compositing for more info '''
        tPixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height, self.width, 4).astype(numpy.single)
        bPixels = numpy.frombuffer(back._rgba, dtype=numpy.uint8).reshape(\
                back.height, back.width, 4).astype(numpy.single)
        ''' Top image and back image dimensions might be different: '''
        w = max(self.width, back.width)
        h = max(self.height, back.height)
        tPixels = numpy.pad(tPixels, [(0, w - self.width), \
                (0, h - self.height), (0, 0)], mode = 'constant') 
        bPixels = numpy.pad(bPixels, [(0, w - back.width), \
                (0, h - back.height), (0, 0)], mode = 'constant')
        tRGB = tPixels[...,:3]
        bRGB = bPixels[...,:3]
        tAlpha = tPixels[...,3] / 255.0
        bAlpha = bPixels[...,3] / 255.0
        outAlpha = tAlpha + bAlpha * (1 - tAlpha)

        numpy.seterr(all='ignore')
        outRGB = (tRGB * tAlpha[..., numpy.newaxis] + bRGB * \
                bAlpha[..., numpy.newaxis] * (1 - tAlpha[..., numpy.newaxis])) \
                / outAlpha[..., numpy.newaxis]

        outRGBA = numpy.dstack((outRGB, outAlpha * 255)).astype(numpy.uint8)
        numpy.seterr(all='warn')

        return self.__class__(rgba=outRGBA.tobytes(), size=[w, h])

    def overlay(self, color):
        ''' Overlay image on a solid block of color, using its Alpha channel '''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape( \
                self.height * self.width, 4).astype(numpy.integer)
        back = numpy.array(hex_to_int(color))
        alpha = pixels[..., 3]
        pixels[..., :3] = (pixels[..., :3] * alpha[..., numpy.newaxis] + \
                back[numpy.newaxis, ...] * \
                (255 - alpha[..., numpy.newaxis])) / 255
        pixels[..., 3].fill(255)
        return self.__class__(rgba=pixels.astype(numpy.uint8).tobytes(), \
                size=self._size)

    def border(self, color, percent):
        ''' Apply a border to image. Border width in pxiels as percent of    '''
        ''' minimum of image width & height. Assuming (0. < percent < 50.) '''
        mindim = min(self.height, self.width)
        ''' 8x8 or smaller icons do not need borders. '''
        if mindim <= 8: return self
        r, g, b = hex_to_int(color)
        border = numpy.full((self.width, self.height, 4), [r, g, b, 255])
        ''' Proper passe-partout technique for best quality '''
        edge = int(mindim * percent / 100.)
        antialias = int(((mindim * percent) % 100.) * 255. / 100.)
        border[edge:-edge, edge:-edge]=numpy.array([r, g, b, antialias])
        back = math.ceil(mindim * percent / 100.)
        border[back:-back, back:-back]=numpy.array([255, 255, 255, 0])
        return self.__class__(rgba=border.astype(numpy.uint8).tobytes(), \
                size=self._size).alphacompositor(self)

    def thin_border(self, color):
        """ 1.536 Pixel border is nice for thin borders of 32x32 icons """
        return self.border(color, 4.8)

    def thick_border(self, color):
        """ 2.048 Pixel border is nice for thick borders of 32x32 icons """
        return self.border(color, 6.4)

    def untouched(self):
        ''' Returning the untouched image '''
        return self

    def invert(self):
        ''' Inverting image for a paranoid effect '''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height * self.width, 4).astype(numpy.integer)
        pixels[..., :3] = 255 - pixels[..., :3]
        return self.__class__(rgba=pixels.astype(numpy.uint8).tobytes(), \
                size=self._size)

    def mirror(self, axes):
        ''' Mirror/flip image. I guess no one would ever use this'''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height, self.width, 4)
        pixels = numpy.flip(pixels, axes)
        return self.__class__(rgba=pixels.tobytes(), \
                size=self._size)

# vim: ft=python sw=4 ts=4 et
