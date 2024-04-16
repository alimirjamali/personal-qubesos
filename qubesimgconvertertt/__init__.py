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
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height, self.width, 4)
        for row in pixels:
            for pixel in row:
                r, g, b = pixel[:3]
                print("\033[48;2;%d;%d;%dm  " % (r, g, b), end='')
            print("\033[0m")

    def alphacompositor(self, back):
        ''' Compositing self on top of another Image. See: '''
        ''' https://en.wikipedia.org/wiki/Alpha_compositing for more info '''
        tPixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height, self.width, 4).astype(numpy.single)
        bPixels = numpy.frombuffer(back._rgba, dtype=numpy.uint8).reshape(\
                back.height, back.width, 4).astype(numpy.single)
        ''' If top image and back image dimensions are different: '''
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

    def overlay(self, colour):
        ''' Overlay image on a solid block of color, using its Alpha channel '''
        rb, gb, bb = hex_to_int(colour)
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height * self.width, 4).astype(numpy.uint32)
        r = pixels[:, 0]
        g = pixels[:, 1]
        b = pixels[:, 2]
        a = pixels[:, 3]
        r = (((a * r) + (255 - a) * rb) / 255).astype(numpy.uint8)
        g = (((a * g) + (255 - a) * gb) / 255).astype(numpy.uint8)
        b = (((a * b) + (255 - a) * bb) / 255).astype(numpy.uint8)
        a.fill(255)
        pixelso = numpy.column_stack((r, g, b, a.astype(numpy.uint8)))
        return self.__class__(rgba=pixelso.tobytes(), size=self._size)

    def border(self, colour, percent):
        ''' Apply a border to image at the border width of percent of  '''
        ''' minimum of image width & height. Assuming (0. < percent < 100.) '''
        ''' Even though border with over 50.% percent would be meaningless '''
        rb, gb, bb = hex_to_int(colour)
        mindim = min(self.height, self.width)
        ''' 8x8 icons do not need borders. 16x16 icons could have only 1 pix'''
        if mindim <= 8:
            return self
        elif mindim <= 16:
            width = 1; ab = 0
        else:
            width = int(mindim * percent / 100.)
            ''' Anti-aliasing border edges. We need alpha of border at edges '''
            ab = int(((mindim * percent) % 100.) * 255. / 100.)

        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height, self.width, 4).astype(numpy.uint32)

        if ab>0:
            border=numpy.array([rb, gb, bb, ab])
            pixels[0:width+1, :] = (pixels[0:width+1, :] + border) / 2
            pixels[:, 0:width+1] = (pixels[:, 0:width+1] + border) / 2
            pixels[-width-1:, :] = (pixels[-width-1:, :] + border) / 2
            pixels[:, -width-1:] = (pixels[:, -width-1:] + border) / 2

        pixels[0:width, :] = rb, gb, bb, 255
        pixels[:, 0:width] = rb, gb, bb, 255
        pixels[-width:, :] = rb, gb, bb, 255
        pixels[:, -width:] = rb, gb, bb, 255
        return self.__class__(rgba=pixels.astype(numpy.uint8).tobytes(), \
                size=self._size)

    def thin_border(self, color):
        """ 1.5 Pixel border is nice for thin borders of 32x32 icons """
        return self.border(color, 4.6875)

    def thick_border(self, color):
        """ 2 Pixel border is nice for thick borders of 32x32 icons """
        return self.border(color, 6.25)

    def untouched(self):
        ''' Returning the untouched image '''
        return self

    def invert(self):
        ''' Inverting image for a paranoid effect '''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height * self.width, 4).astype(numpy.uint32)
        pixels[:, :3] = 255 - pixels[:, :3]
        return self.__class__(rgba=pixels.astype(numpy.uint8).tobytes(), \
                size=self._size)

    def mirror(self, axes):
        ''' Mirror/flip image. I guess no one would use this'''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height, self.width, 4)
        pixels = numpy.flip(pixels, axes)
        return self.__class__(rgba=pixels.tobytes(), \
                size=self._size)

# vim: ft=python sw=4 ts=4 et
