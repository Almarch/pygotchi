from ._tamalib import Tama as CppTama
from .conversion import int2bin, bin2int

class Tama(CppTama):
    
    def display(self):
        pass

    def click(self):
        pass

    def poke(self): # new
        pass

    def reset(self):
        self.stop()
        obj = [0 for i in range(9216)]
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
        obj = self.GetROM()
        return int2bin(obj)

    def flash(self, bin):
        obj = bin2int(bin)
        self.SetROM(obj)
        



