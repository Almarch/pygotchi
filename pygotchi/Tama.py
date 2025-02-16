from ._tamalib import Tama as CppTama

class Tama(CppTama):
    def is_alive(self):
        return True
