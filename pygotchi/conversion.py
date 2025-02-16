
def int2bin(obj):
    obj = [f"{num:02X}" for num in obj]
    obj = "".join(obj)
    unfiltered_obj = []
    for i in range(len(obj)):
        if(i % 3 == 0):
            unfiltered_obj.append("0")
        unfiltered_obj.append(obj[i])
    bin = "".join(unfiltered_obj)
    bin = bytes.fromhex(bin)
    return bin

def bin2int(bin):
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
    return obj