import numpy as np
import os
import re
from texttable import *


def search_for_hex(bin, hex, hex_len):
    poses = []
    started = 0
    current_pos = 0
    for k in range(0, len(bin)):
        to_shift = (hex_len - current_pos - 1) * 8
        byte = (hex >> to_shift) & 0xFF
        if bin[k] == byte:
            current_pos += 1
        else:
            started = k + 1
            current_pos = 0
        if current_pos == hex_len:
            poses.append(started)
            current_pos = 0
    return poses


path = "D:\Downloads\MCU_IDE_0.81\Project2\\"

files = [f for f in os.listdir(path) if re.match(r"\w+.PDK(_[0-9]{2})?", f)]

dict = {}
for file in files:
    dict[path + file] = np.fromfile(path + file, dtype=np.uint8)

not_equls = []

for i in range(0, len(list(dict.values())[0])):
    init = list(dict.values())[0][i]
    equl = True
    for arr in dict.values():
        if arr[i] == init:
            continue
        else:
            equl = False
            break
    if not equl:
        not_equls.append(i)

tbl = Texttable(500000)

tbl.set_deco(Texttable.HEADER)
tbl.set_cols_align(["l"] * (len(list(dict.values())[0]) + 1))
tbl.set_cols_dtype(["t"] * (len(list(dict.values())[0]) + 1))

hdr = []

for n in range(0, len(list(dict.values())[0])):
    if n in not_equls:
        hdr.append(str(n))
    else:
        hdr.append(str(n) + "(EQUAL)")

tbl.header(["0"] + hdr)

for key in dict:
    arr = dict[key]
    row = [key]
    for i in range(0, len(arr)):
        row.append(str('{:08b}'.format(arr[i])))
    tbl.add_row(row)

print(tbl.draw())

search_map = {0x03:1}

for key in dict:
    for search_key in search_map:
        string = ""
        pos = search_for_hex(dict[key], search_key, search_map.get(search_key))
        if len(pos) > 0:
            string += "Found " + str(hex(search_key)) + " in " + key + " at: ["
            for p in pos:
                string += str(p) + ", "
            string = string[:-2]
            string += "]"
            print(string)
