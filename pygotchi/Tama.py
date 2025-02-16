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
        self.SetROM(obj_nums)
        obj_list = [f"{num:02X}" for num in obj_nums]
        tmp = "".join(obj_list)
        obj = []
        j = 0
        for i in range(len(tmp) + len(tmp) // 3):
            if (i + 3) % 4 == 0:
                obj.append("0")
            else:
                obj.append(tmp[j])
                j += 1
        hex_string = "".join(obj)
        byte_data = bytes.fromhex(hex_string)
        file_handle = open(bin_file, "wb")  
        file_handle.write(byte_data)  
        file_handle.close()

    def flash(self):
        file_handle = open(bin_file, "rb")
        obj = file_handle.read() 
        obj = "".join(f"{byte:02X}" for byte in obj)
        tmp = "".join(obj[i] for i in range(len(obj)) if (i + 3) % 4)
        obj_list = [tmp[2 * i: 2 * i + 2] for i in range(len(tmp) // 2)]
        obj_nums = [int(hex_str, 16) for hex_str in obj_list]
        self.SetROM(obj_nums)

    



