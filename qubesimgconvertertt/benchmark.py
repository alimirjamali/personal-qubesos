from qubesimgconvertertt import Image
import numpy as np
from colorsys import hsv_to_rgb
from timeit import timeit

class Benchmark(object):
    def __init__(self, dim):
        self.dim=dim
    def setUp(self):
        dim=self.dim
        img = np.full((dim, dim, 4), 0, dtype=np.uint8)
        img[..., 3] = np.arange(0, 255, 255/dim, dtype=np.uint8)
        img = np.rot90(img, 2)
        for hue in range(0,dim):
            (r, g, b) = hsv_to_rgb(hue/dim, 1.0, 1.0)
            R, G, B = int(255 * r), int(255 * g), int(255 * b)
            img[hue, ..., :3] = [R, G, B]
        img = np.rot90(img)
        self.Image1 = Image(rgba=img.tobytes(), size=(dim, dim))
        img = np.rot90(img)
        self.Image2 = Image(rgba=img.tobytes(), size=(dim, dim))
    def testUntouched(self):
        self.Image1.untouched()
    def testTint(self):
        self.Image1.tint('0x0000ff')
    def testOverlay(self):
        self.Image1.overlay('0x0000ff')
    def testBorder(self):
        self.Image1.border('0x0000ff',6.666)
    def testInvert(self):
        self.Image1.invert()
    def testMirror(self):
        self.Image1.mirror((0,1))
    def testAlphacompositor(self):
        self.Image1.alphacompositor(self.Image2)

def cpuinfo():
    cpudetails={}
    with open('/proc/cpuinfo', 'r') as f:
        for line in f.readlines():
            if line.startswith("vendor_id") or \
                    line.startswith("model name") or \
                    line.startswith("cpu MHz") or \
                    line.startswith("cpu cores"):
                key_value = line.replace('\n','').split(':')
                cpudetails[key_value[0]]=key_value[1]
    for key, value in cpudetails.items():
        print ("{} : {}".format(key, value))
                    
def main():
    dim = 32
    n = 10000
    cpuinfo()
    print ('Performing benchmarks on a {}x{} image for {} times...'.format(\
            dim, dim, n))
    b = Benchmark(dim)
    b.setUp()
    print ("Untouched Image (no effect): ", \
            timeit("b.testUntouched()",         globals=locals(), number=n))
    print ("The original tint effect:    ", \
            timeit("b.testTint()",              globals=locals(), number=n))
    print ("Alpha Compositor:            ", \
            timeit("b.testAlphacompositor()",   globals=locals(), number=n))
    print ("Overlay Effect:              ", \
            timeit("b.testOverlay()",           globals=locals(), number=n))
    print ("Border Effects:              ", \
            timeit("b.testBorder()",            globals=locals(), number=n))
    print ("Invert Effect:               ", \
            timeit("b.testInvert()",            globals=locals(), number=n))
    print ("Mirror Effect:               ", \
            timeit("b.testMirror()",            globals=locals(), number=n))

if __name__ == '__main__':
    main()

