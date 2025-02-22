from ._tamalib import Tama as Tamalib
from .conversion import int2bin, bin2int
import time
from threading import Lock, Thread

class Tama():
    def __init__(self):
        self.__tamalib__ = Tamalib()
        self.__lock__ = Lock() 
        self.__0ROM__ = [0 for i in range(9216)]
        self.__0CPU__ = [0 for i in range(384)]
        self.__0CPU__[ 1] = 1
        self.__0CPU__[ 8] = 1
        self.__0CPU__[32] = 96
        self.__0CPU__[33] = 219
        self.__0CPU__[34] = 127
        self.__0CPU__[35] = 42
        self.__0CPU__[36] = 203
        self.__0CPU__[37] = 113
        self.__0CPU__[43] = 12
        self.__0CPU__[47] = 10
        self.__0CPU__[51] = 8
        self.__0CPU__[55] = 6
        self.__0CPU__[59] = 4
        self.__0CPU__[63] = 2
    
    def __wait__(self):
        time.sleep(.1)

    def runs(self):
        with self.__lock__:
            res = self.__tamalib__.Runs()
        return res

    def start(self):
        if not self.runs():
            with self.__lock__:
                self.__tamalib__.Start()

    def stop(self):
        with self.__lock__:
            self.__tamalib__.Stop()        

    def matrix(self):
        with self.__lock__:
            res = self.__tamalib__.GetMatrix()
        return res
    
    def freq(self):
        with self.__lock__:
            res = self.__tamalib__.GetFreq()
        return res
    
    def icons(self):
        with self.__lock__:
            res = self.__tamalib__.GetIcons()
        return res

    def __click__(self, button, delay):
        with self.__lock__:
            for b in button:
                self.__tamalib__.SetButton({"A": 0, "B": 1, "C": 2}[b], True)
        time.sleep(delay)
        with self.__lock__:
            for b in [0, 1, 2]:
                self.__tamalib__.SetButton(b, False)

    def click(self, button, delay=0.1):
        
        Thread(target=self.__click__, args=(button, delay)).start()

    def poke(self): # new
        pass

    def reset(self, what):
        with self.__lock__:
            self.__tamalib__.Stop()
            self.__wait__()
            if what=="CPU":
                self.__tamalib__.SetCPU(self.__0CPU__)
            elif what == "ROM":
                self.__tamalib__.SetROM(self.__0ROM__)
                self.__wait__()
                self.__tamalib__.SetCPU(self.__0CPU__)

    def dump(self, what):
        with self.__lock__:
            running = self.__tamalib__.Runs()
            self.__tamalib__.Stop()
            self.__wait__()
            if what=="CPU":
                obj = self.__tamalib__.GetCPU()
            elif what == "ROM":
                obj = self.__tamalib__.GetROM()
            self.__wait__()
            if running:
                self.__tamalib__.Start()
        return int2bin(obj)
    
    def load(self, what, bin):
        obj = bin2int(bin)
        with self.__lock__:
            running = self.__tamalib__.Runs()
            self.__tamalib__.Stop()
            self.__wait__()
            if what=="CPU":
                self.__tamalib__.SetCPU(obj)
            elif what == "ROM":
                self.__tamalib__.SetROM(obj)
            self.__wait__()
        if what=="CPU" and running:
            self.start()
        elif what == "ROM":
            self.reset("CPU")

