from ._tamalib import Tama as CppTama
from .conversion import int2bin, bin2int
from .images import background, icons
import numpy as np
import matplotlib.pyplot as plt
import time
import threading

class Tama(CppTama):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock() 
    
    def display(self, background = background):

        raster = np.zeros((16,32,4))
        raster[..., 3] = np.array(self.GetMatrix())
        ics = self.GetIcon()
        
        fig, ax = plt.subplots()
        ax.imshow(background , extent=[-1, 33, -1, 33])
        ax.imshow(raster, interpolation = None , extent=[0, 32, 8, 24])
        if ics[0]: ax.imshow(icons["food"]     , interpolation = None, extent=[ 2, 6,26.25,29.75])
        if ics[1]: ax.imshow(icons["lights"]   , interpolation = None, extent=[10,14,26.25,29.75])
        if ics[2]: ax.imshow(icons["game"]     , interpolation = None, extent=[18,22,26.25,29.75])
        if ics[3]: ax.imshow(icons["medicine"] , interpolation = None, extent=[26,30,26.5 ,29.75])
        if ics[4]: ax.imshow(icons["bathroom"] , interpolation = None, extent=[ 2, 6, 2.5 , 5.5 ])
        if ics[5]: ax.imshow(icons["status"]   , interpolation = None, extent=[10,14, 2.5,  5.25])
        if ics[6]: ax.imshow(icons["training"] , interpolation = None, extent=[18,22, 2.5,  5.5 ])
        if ics[7]: ax.imshow(icons["attention"], interpolation = None, extent=[26,30, 2.5,  5   ])
        ax.axis('off')
        ax.set_xlim(0,32)
        ax.set_ylim(0,32)
        plt.show()


    def click(self, button, delay=0.1):
        assert all(b in ["A", "B", "C"] for b in button)
        assert delay > 0

        with self.lock:
            for b in button:
                self.SetButton({"A": 0, "B": 1, "C": 2}[b], True)
            time.sleep(delay)
            for b in [0, 1, 2]:
                self.SetButton(b, False)

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
        



