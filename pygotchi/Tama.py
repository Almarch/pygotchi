from ._tamalib import Tama as CppTama

class Tama(CppTama):
    def is_alive(self):
        return True
    
    def display(self):
        pass

    def click(self):
        pass

    def poke(self): # new
        pass

    def reset(self):
        pass

    def glimpse(self):
        pass
    
    def save(self):
        pass
    
    def load(self):
        pass

    def dump(self):
        obj = self.GetROM()
        obj = [f"{num:02X}" for num in obj]
        obj = "".join(obj)
        bin = []
        j = 0
        for i in range(len(obj) + len(obj) // 3):
            if (i + 3) % 4 == 0:
                bin.append("0")
            else:
                bin.append(obj[j])
                j += 1
        bin = "".join(bin)
        bin = bytes.fromhex(bin)
        return(bin)

    def flash(self, bin):
        obj = "".join(f"{byte:02X}" for byte in bin)
        obj = "".join(obj[i] for i in range(len(obj)) if (i + 3) % 4)
        obj = [obj[2 * i: 2 * i + 2] for i in range(len(obj) // 2)]
        obj = [int(hex_str, 16) for hex_str in obj]
        self.SetROM(obj)

    



