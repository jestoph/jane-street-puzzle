import json
import sys
import schemdraw
import schemdraw.elements as elm

def get_io():

    with open("cell-to-pins.txt") as fp:
        data = fp.read()

    ret = {}
    lines = data.splitlines()[2:]
    for line in lines:
        port, ins, outs = line.split("|")
        port = port.strip().replace('sky130_fd_sc_hd__','').replace("_1","").replace("_2","")
        ins = ins.strip().split(',')
        outs = outs.strip().split(',')
        ret[port] = (list(ins), list(outs))

    return ret

IO_PORTS=get_io()


def el_to_elm(elname, position):
    cellname = elname.split(":")[0]
    print(position)
    el = elm.Ic(pinspacing=1).at(tuple(position))
    for in_port in IO_PORTS[cellname][0]:
        el.pin(name=in_port, side='left')
    for out_port in IO_PORTS[cellname][1]:
        el.pin(name=out_port, side='right')

    el.label(elname, font="bold")
    return el


def name_to_pin(pinname, el_map):
    cellname = ":".join(pinname.split(":")[:2])
    _,_,port = pinname.split(":")
    elm = el_map[cellname]
    ret = elm.__getattr__(port)
    return ret


def draw_circuit(circuit, filename, show=False):
    with schemdraw.Drawing(show=show) as d:
        el_map = {}
        for el in circuit['elements']:
            tmp = el_to_elm(el, circuit['element_position'][el])
            el_map[el] = tmp

        for wire, els in circuit['wire_to_ports'].items():
            pins = [name_to_pin(el, el_map) for el in els]
            if len(els) > 1:
                for i in range(len(els)-2):
                    elm.Line().endpoints(pins[i], pins[i+1]).dot()

        # d.draw()
        if filename:
            d.save(filename)


example = """
{
  "wires": [
    "Wire:101",
    "Wire:72",
    "Wire:71",
    "Wire:2",
    "Wire:103",
    "Wire:112",
    "Wire:99",
    "Wire:116",
    "Wire:105",
    "Wire:114",
    "Wire:104",
    "Wire:36"
  ],
  "elements": [
    "and4bb:2",
    "and4bb:1",
    "and3:1"
  ],
  "port_to_wire": {
    "and3:1:X": "Wire:101",
    "and3:1:B": "Wire:72",
    "and3:1:A": "Wire:71",
    "and3:1:C": "Wire:2",
    "and4bb:1:B_N": "Wire:103",
    "and4bb:2:A_N": "Wire:112",
    "and4bb:2:B_N": "Wire:99",
    "and4bb:1:X": "Wire:116",
    "and4bb:1:D": "Wire:105",
    "and4bb:1:C": "Wire:114",
    "and4bb:1:A_N": "Wire:104",
    "and4bb:2:C": "Wire:101",
    "and4bb:2:D": "Wire:116",
    "and4bb:2:X": "Wire:36"
  },
  "wire_to_ports": {
    "Wire:101": [
      "and3:1:X",
      "and4bb:2:C"
    ],
    "Wire:72": [
      "and3:1:B"
    ],
    "Wire:71": [
      "and3:1:A"
    ],
    "Wire:2": [
      "and3:1:C"
    ],
    "Wire:103": [
      "and4bb:1:B_N"
    ],
    "Wire:112": [
      "and4bb:2:A_N"
    ],
    "Wire:99": [
      "and4bb:2:B_N"
    ],
    "Wire:116": [
      "and4bb:1:X",
      "and4bb:2:D"
    ],
    "Wire:105": [
      "and4bb:1:D"
    ],
    "Wire:114": [
      "and4bb:1:C"
    ],
    "Wire:104": [
      "and4bb:1:A_N"
    ],
    "Wire:36": [
      "and4bb:2:X"
    ]
  }
}
"""


if __name__ == '__main__':
    with open(sys.argv[1]) as fp:
        data = json.load(fp)
    draw_circuit(data, filename="", show=True)

