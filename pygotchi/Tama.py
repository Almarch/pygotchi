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
        bin_data = []
        j = 0
        for i in range(len(obj) + len(obj) // 3):
            if (i + 3) % 4 == 0:
                bin_data.append("0")
            else:
                bin_data.append(obj[j])
                j += 1
        bin_data = "".join(bin_data)
        bin_data = bytes.fromhex(bin_data)
        return bin_data

    def flash(self, bin):
        obj = "".join(f"{byte:02X}" for byte in bin)
        filtered_obj = []
        for i in range(len(obj)):
            if(i % 4 == 0):
                continue
            else:
                filtered_obj.append(obj[i])
        filtered_obj
        obj = "".join(filtered_obj)
        obj = [int(obj[2 * i: 2 * i + 2], 16) for i in range(len(obj) // 2)]
        self.SetROM(obj)
        



