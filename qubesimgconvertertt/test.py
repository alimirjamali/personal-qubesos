from __future__ import absolute_import

import asyncio

try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO
import unittest

import qubesimgconvertertt
import numpy as np
from colorsys import hsv_to_rgb

class TestCaseTweakTool(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        dim = 32
        ''' Performing tests on a 32x32 image. Horizontally filled with      '''
        ''' rainbow colors, vertical transparent 100% top, 0% bottom.        '''
        img = np.full((dim, dim, 4), 0, dtype=np.uint8)
        img[..., 3] = np.arange(0, 255, 255/dim, dtype=np.uint8)
        img = np.rot90(img, 2)
        for hue in range(0,dim):
            (r, g, b) = hsv_to_rgb(hue/dim, 1.0, 1.0)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            img[hue, ..., :3] = [R, G, B]
        img = np.rot90(img)
        self.img = img
        self.rgba = img.tobytes()
        self.size = (dim, dim)
        self.image = qubesimgconvertertt.Image(rgba=self.rgba, size=self.size)
    
    def test_00_init(self):
        self.assertEqual(self.image._rgba, self.rgba)
        self.assertEqual(self.image._size, self.size)

    def test_01_ANSI(self):
        print ("ANSI print of original image:")
        self.image.ANSI()

    def test_02_alphacomposite(self):
        back = qubesimgconvertertt.Image(rgba=np.rot90(self.img[::2, ::2])\
                .tobytes(), size=(int(self.size[0]/2), int(self.size[1]/2)))
        image = self.image.alphacomposite(back)
        print ("Alpha Compositor:")
        image.ANSI()

    def test_03_overlay(self):
        image = self.image.overlay('#0000ff')
        print ("Overlay:")
        image.ANSI()

    def test_04_border(self):
        image = self.image.border('#0000ff',7.23)
        print ("Border:")
        image.ANSI()

    def test_05_invert(self):
        image = self.image.invert()
        print ("Invert:")
        image.ANSI()

    def test_06_mirror(self):
        image = self.image.mirror((0,1))
        print ("Mirror:")
        image.ANSI()

if __name__ == '__main__':
    unittest.main()
