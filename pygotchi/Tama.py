from ._tamalib import Tama as CppTama
from .conversion import int2bin, bin2int
from .images import background
import numpy as np
import matplotlib.pyplot as plt
class Tama(CppTama):
    
    def display(self, background = background):

        raster = np.zeros((16,32,4))
        raster[..., 3] = np.array(self.GetMatrix())
        
        fig, ax = plt.subplots()
        ax.imshow(background , extent=[-1, 33, -1, 33])
        ax.imshow(raster, interpolation = None , extent=[0, 32, 8, 24])

        ax.axis('off')
        plt.show()

    def click(self):
        pass

    def poke(self): # new
        pass

    def reset(self):
        self.stop()
        obj = [0 for i in range(384)]
        obj[ 1] = 1
        obj[ 8] = 1
        obj[32] = 96
        obj[33] = 219
        obj[34] = 127
        obj[35] = 42
        obj[36] = 203
        obj[37] = 113
        obj[43] = 12
        obj[47] = 10
        obj[51] = 8
        obj[55] = 6
        obj[59] = 4
        obj[63] = 2
        self.SetCPU(obj)

    def save(self):
        self.stop()
        obj = self.GetCPU()
        return int2bin(obj)
    
    def load(self, bin):
        self.stop()
        obj = bin2int(bin)
        self.SetCPU(obj)

    def dump(self):
        self.stop()
        obj = self.GetROM()
        return int2bin(obj)

    def flash(self, bin):
        self.stop()
        obj = bin2int(bin)
        self.SetROM(obj)
        



