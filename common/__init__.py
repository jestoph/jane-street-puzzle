import gdstk
import sys
import time
from contextlib import contextmanager

labels_i_care_about = {
    "A",
    "A_N",
    "A0",
    "A1",
    "A2",
    "A2",
    "A3",
    "A4",
    "A1_N",
    "A2_N",
    "B",
    "B_N",
    "B1",
    "B1_N",
    "B0",
    "B1",
    "B2",
    "B3",
    "C",
    "C1",
    "C2",
    "CLK",
    "C_N",
    "D",
    "D1",
    "D2",
    "D_N",
    "RESET_B",
    "X",
    "Y",
    "S",
    "Q",
    "LO",
    "HI",
    "SET_B"
}


def increase_view(svgfile):
    """
    My apologies for how stupid this is.
    """

    with open(svgfile) as fp:
        lines = fp.readlines()

    line = lines[1]

    assert '<svg xmlns' in line, f'{line=}'

    """
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="34.6" height="35.2" viewBox="-3.5 -31.2 34.6 35.2">

    to

    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="346" height="352" viewBox="-3.5 -31.2 34.6 35.2">
    """

    h = line.find("height=")
    s = line.find('"', h+1)
    e = line.find('"', s+1)

    print(f"{line[s+1:]=}")

    height = float(line[s+1:e])*10

    line = line[:s+1] + str(height) + line[e:]

    w = line.find("width=")
    s = line.find('"', w+1)
    e = line.find('"', s+1)

    width = float(line[s+1:e])*10

    line = line[:s+1] + str(width) + line[e:]

    lines = [lines[0], line] + lines[2:]

    with open(svgfile, "w") as fp:
        for line in lines:
            print(line, file=fp, end='')


name_to_layer = {
    "li1" :(67,20),
    "mcon":(67,44),
    "met1":(68,20),
    "via" :(68,44),
    "met2":(69,20),
    "via2":(69,44),
    "met3":(70,20),
    "via3":(70,44),
    "met4":(71,20),
}

layer_to_name = {val:key for key,val in name_to_layer.items()}

layer_ordering = [
    "li1",
    "mcon",
    "met1",
    "via",
    "met2",
    "via2",
    "met3",
    "via3",
    "met4",
]

layers_i_care_about = set(name_to_layer.values())

def read_layers():
    # Headers are layer_name,purpose,layer,datatype,description
    import csv
    with open('common/gds_layers.csv') as fp:
        list_of_dicts = list(csv.DictReader(fp))
    return list_of_dicts

def mdtable(data):
    """
    Added as a convenience - my vim tool will do this for me
    """
    if not data: return
    maxlens = {k: len(k) for k in data[0]}
    header_list = list(data[0].keys()) # To ensure consistent sorting

    for dat in data:
        for key, val in dat.items():
            maxlens[key] = max(maxlens[key], len(str(val)))

    headers = [f"{header:{maxlens[header]}}" for header in header_list]
    header_str = " | ".join(headers)
    horiz = "-"*len(header_str)

    print(header_str)
    print(horiz)

    for dat in data:
        vals = [(str(dat[key]) + " "*100)[:maxlens[key]] for key in header_list]
        vals_str = " | ".join(vals)
        print(vals_str)

def get_io():

    with open("common/cell-to-pins.txt") as fp:
        data = fp.read()

    ret = {}
    lines = data.splitlines()[2:]
    for line in lines:
        port, ins, outs = line.split("|")
        port = port.strip().replace('sky130_fd_sc_hd__','')
        ins = ins.strip().split(',')
        outs = outs.strip().split(',')
        ret[port] = (set(ins), set(outs))

    return ret

IO_PORTS=get_io()

@contextmanager
def measure_time(name):
    t = time.time()
    try:
        yield
    finally:
        s = time.time()
        print(f"> {name} - {s - t}")


