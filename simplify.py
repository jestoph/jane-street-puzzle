

def find_wires(conns):
    wire_mapping = {}
    wire_segment_mapping = {}
    for l, r in conns:
        # We're going to treat clkbufs as wierd wires
        if ('wire' not in l) and ('clkbuf' not in l):
            wire_segment_mapping[l] = r
        elif ('wire' not in r) and ('clkbuf' not in r):
            wire_segment_mapping[r] = l
        else:

            if l in wire_mapping:
                wire_mapping[l].append(r)
            else:
                wire_mapping[l] = [r]
            if r in wire_mapping:
                wire_mapping[r].append(l)
            else:
                wire_mapping[r] = [l]


    all_wires = set()
    for wire_id in wire_mapping:
        collected = set()
        seen = set()
        wires = [wire_id]
        while wires:
            curr = wires.pop()
            seen.add(curr)
            for n in wire_mapping[curr]:
                if n not in seen:
                    wires.append(n)
            collected.add(curr)
        all_wires.add(tuple(sorted(collected)))


    assert sum([len(wires) for wires in all_wires]) == len(wire_mapping)


    canonical_id = 0
    segment_mapping = {}
    print(f"Total number of wires: {len(all_wires)=}")
    for wire in sorted(all_wires): # Sort so wires are predictably named
        canonical_id += 1
        canonical_name = f"Wire:{canonical_id}"
        for wire_segment in wire:
            segment_mapping[wire_segment] = canonical_name

    port_wire_mapping = {}
    for port, wire_segment in wire_segment_mapping.items():
        port_wire_mapping[port] = segment_mapping[wire_segment]

    return port_wire_mapping


def find_bounding(port_wire_mapping, box):
    ret = {}

    (xmin, ymin), (xmax, ymax) = box
    for port, wire in port_wire_mapping.items():
        """ eg 'x:26.220:y:70.720:mux2_1:12:A0 """
        _, x, _, y, name, _, _ = port.split(":")
        x, y = float(x), float(y)

        # It seems clocks don't always keep within domains
        # so just add them in
        if 'clkbuf' in name:
            ret[port] = wire

        if x < xmin or x > xmax or y < ymin or y > ymax:
            continue

        ret[port] = wire

    return ret

def print_element(name, port_wire_map):
    print()
    print(f"---------------------{name.upper()}--------------------")
    for port, wire in sorted(port_wire_map.items(), key=lambda x: x[0]):
        port_pretty = ":".join(port.split(":")[4:])
        port_pretty = port_pretty.replace("_1","").replace("_2","")
        print(port_pretty, '->', wire)

    print(f"-----------------------------------------")
    for port, wire in sorted(port_wire_map.items(), key=lambda x: x[1]):
        port_pretty = ":".join(port.split(":")[4:])
        port_pretty = port_pretty.replace("_1","").replace("_2","")
        print(wire, '<-', port_pretty)

    print()

if __name__ == '__main__':
    all_wire_segments = []
    with open('graph.txt') as fp:
        for line in fp:
            l, _, r = line.split()
            all_wire_segments.append((l, r))

    port_wire_mapping = find_wires(all_wire_segments)
    # for port, wire in port_wire_mapping.items():
    #     print(port, wire)

    comparitor_box = ((50, 40), (100,60)) # Bit of a guess
    adder_box = ((50, 0), (100,40)) # Bit of a guess
    sr_1_box = ((0, 45), (50, 100))
    sr_2_box = ((0, 0), (50, 45))

    comparitor = find_bounding(port_wire_mapping, comparitor_box)
    adder = find_bounding(port_wire_mapping, adder_box)
    sr_1 = find_bounding(port_wire_mapping, sr_1_box)
    sr_2 = find_bounding(port_wire_mapping, sr_2_box)

    # print_element("Comparitor", comparitor)
    print_element("Shift Register 1", sr_1)
