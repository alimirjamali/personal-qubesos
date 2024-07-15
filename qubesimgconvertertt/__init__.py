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
import math
import numpy
import shutil
from sys import stdout

'''Note to self: qubesimgconverter.Image.tint is using numpy's old- '''
'''deprecated binary mode of fromstring. as it behaves surprisingly-'''
'''on unicode inputs. Use of frombuffer is recommended. However,-   '''
'''this should  not be a security hazard here. No need for patches. '''

class Image(qubesimgconverter.Image):
    def __init__(self, rgba, size):
          super().__init__(rgba, size) 

    def alphacomposite(self, back):
        ''' Compositing Image on top of another Image. See:                  '''
        ''' https://en.wikipedia.org/wiki/Alpha_compositing for more info    '''
        tPixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height, self.width, 4).astype(numpy.single)
        bPixels = numpy.frombuffer(back._rgba, dtype=numpy.uint8).reshape(\
                back.height, back.width, 4).astype(numpy.single)
        # Top image and back image dimensions might be different. Use largest
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
        outAlpha = tAlpha + bAlpha * (1. - tAlpha)

        numpy.seterr(all='ignore')
        outRGB = (tRGB * tAlpha[..., numpy.newaxis] + bRGB * \
                bAlpha[..., numpy.newaxis] * (1 - tAlpha[..., numpy.newaxis])) \
                / outAlpha[..., numpy.newaxis]

        outRGBA = numpy.dstack((outRGB, outAlpha * 255)).astype(numpy.uint8)
        numpy.seterr(all='warn')

        return self.__class__(rgba=outRGBA.tobytes(), size=[w, h])

    def overlay(self, color):
        ''' Overlay image on a solid block of color, using its Alpha channel.'''
        ''' Alpha Compositor is not used here for performance related reasons'''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape( \
                self.height * self.width, 4).astype(numpy.uint32)
        back = numpy.array(hex_to_int(color))
        alpha = pixels[..., 3]
        pixels[..., :3] = (pixels[..., :3] * alpha[..., numpy.newaxis] + \
                back[numpy.newaxis, ...] * \
                (255 - alpha[..., numpy.newaxis])) / 255
        pixels[..., 3].fill(255)
        return self.__class__(rgba=pixels.astype(numpy.uint8).tobytes(), \
                size=self._size)

    def border(self, color, percent):
        ''' Apply a border to image. Border width in pixels as percent of    '''
        ''' minimum of image width & height. Assuming (0. < percent < 50.)   '''
        mindim = min(self.height, self.width)
        # 8x8 or smaller icons do not need borders.
        if mindim <= 8: return self
        r, g, b = hex_to_int(color)
        border = numpy.full((self.width, self.height, 4), [r, g, b, 255])
        # Proper passe-partout technique for best quality
        edge = int(mindim * percent / 100.)
        antialias = int(((mindim * percent) % 100.) * 255. / 100.)
        border[edge:-edge, edge:-edge]=numpy.array([r, g, b, antialias])
        back = math.ceil(mindim * percent / 100.)
        border[back:-back, back:-back]=numpy.array([255, 255, 255, 0])
        return self.__class__(rgba=border.astype(numpy.uint8).tobytes(), \
                size=self._size).alphacomposite(self)

    def thin_border(self, color):
        ''' 1.536 Pixel border is nice for thin borders of 32x32 icons       '''
        return self.border(color, 4.8)

    def thick_border(self, color):
        ''' 2.048 Pixel border is nice for thick borders of 32x32 icons      '''
        return self.border(color, 6.4)

    def untouched(self):
        ''' Returning the untouched image                                    '''
        return self

    def invert(self):
        ''' Inverting image for a paranoid effect                            '''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height * self.width, 4).astype(numpy.uint32)
        pixels[..., :3] = 255 - pixels[..., :3]
        return self.__class__(rgba=pixels.astype(numpy.uint8).tobytes(), \
                size=self._size)

    def mirror(self, axes):
        ''' Mirror/flip image. I guess no one would ever use this            '''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape(\
                self.height, self.width, 4)
        pixels = numpy.flip(pixels, axes)
        return self.__class__(rgba=pixels.tobytes(), \
                size=self._size)

    def rot90(self, times):
        ''' Rotate image 90 degrees X times '''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint32).reshape(\
                self.height, self.width)
        pixels = numpy.rot90(pixels)
        return self.__class__(rgba=pixels.tobytes(), \
                size=(pixels[0].size, pixels[..., 0].size))

    def resize(self, output_size):
        ''' Resize image to new size with numpy's numeric interpolation '''
        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint8).reshape( \
                self.height,  self.width, 4).astype(numpy.uint32)
        iw, ih = self._size
        ow, oh = output_size

        def _x_resize(pixels, iw, ow):
            r = pixels[..., 0]
            g = pixels[..., 1]
            b = pixels[..., 2]
            a = pixels[..., 3]
            xv = numpy.interp(range(iw), [0, iw], [0, ow])
            r = [numpy.interp(range(ow), xv, row) for row in r]
            g = [numpy.interp(range(ow), xv, row) for row in g]
            b = [numpy.interp(range(ow), xv, row) for row in b]
            a = [numpy.interp(range(ow), xv, row) for row in a]
            return numpy.dstack((r, g, b, a)).astype(numpy.uint8)

        pixels = _x_resize(pixels, iw=iw, ow=ow)
        pixels = numpy.rot90(pixels)
        pixels = _x_resize(pixels, iw=ih, ow=oh)
        outRGBA = numpy.rot90(pixels, 3)

        return self.__class__(rgba=outRGBA.tobytes(), size=output_size)

    def pad(self, left: int, top: int = None, right: int = None,
             buttom: int = None):
        ''' Adding / removing pixels at edges (no color, transparent) '''
        if top is None:
            top = left
        if right is None:
            right = left
        if buttom is None:
            buttom = top

        pixels = numpy.frombuffer(self._rgba, dtype=numpy.uint32).reshape(\
                self.height, self.width)

        pixels = pixels[
                -top if top < 0 else None: buttom if buttom < 0 else None,
                -left if left < 0 else None: right if right < 0 else None]

        pixels = numpy.pad(pixels, [
            (0 if top <0 else top, 0 if buttom <0 else buttom),
            (0 if left <0 else left, 0 if right <0 else right)],
                           mode='constant', constant_values=(0,0))
        return self.__class__(rgba=pixels.tobytes(), \
                size=(self.width + left + right, self.height + top + buttom))

    def resize_canvas(self, newsize, horizontal = 'center', vertical = 'center'):
        ''' Easier to use than pad '''
        l = 0
        r = 0
        t = 0
        b = 0
        h = newsize[0] - self.width
        v = newsize[1] - self.height
        if horizontal == 'center':
            l = int(h / 2)
            r = h - l
        elif horizontal == 'left':
            r = h
        elif horizontal == 'right':
            l = h

        if vertical == 'center':
            t = int(v / 2)
            b = v - t
        elif vertical == 'top':
            b = v
        elif vertical == 'buttom':
            t = v

        return self.pad(l, t, r, b)

    def ANSI(self, background="pattern"):
        ''' Representation of image with ANSI esc codes. Default on GIMP-like'''
        ''' grid to imply transparency of the image. '''
        if not stdout.isatty():
            print("ANSI representation of Image is available only via "
                  "Interactive Terminals.")
            return

        screen_width = shutil.get_terminal_size().columns

        img = self
        if (screen_width / 2) < img.width:
            aspect = (screen_width / 2) / img.width
            img = img.resize([int(img.width * aspect), int(img.height * aspect)])

        match background:
            case "white":
                img = img.overlay('0xffffff')
            case "black":
                img = img.overlay('0x000000')
            case "pattern":
                # x86 uint32 is little-endian, So Aplha values come first.
                # To be fixed if Qubes is ported to IBM/360 or OpenRISC.
                pattern = numpy.full((img.height, img.width), 0xff777777, \
                        dtype=numpy.uint32)
                pattern[::2, ::2].fill(0xffc0c0c0)
                pattern[1::2, 1::2].fill(0xffc0c0c0)
                img = img.alphacomposite(img.__class__(rgba=pattern.astype( \
                        numpy.uint32).tobytes(), size=img._size))
            case _:
                img = img.overlay(background)

        pixels = numpy.frombuffer(img._rgba, dtype=numpy.uint8).reshape(\
                img.height, img.width, 4)

        for row in pixels:
            for col, pixel in enumerate(row):
                if (col * 2) > (screen_width - 2):
                    break
                r, g, b = pixel[:3]
                print("\033[48;2;%d;%d;%dm  " % (r, g, b), end='')
            print("\033[0m")

# vim: ft=python sw=4 ts=4 et
