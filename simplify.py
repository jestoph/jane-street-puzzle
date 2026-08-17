
def get_wire_segments(conns):
    list_of_wire_segments = []
    for l, r in conns:
        if 'wire' in l:
            list_of_wire_segments.append(l)
        if 'wire' in r:
            list_of_wire_segments.append(r)
        if 'clkbuf' in l:
            list_of_wire_segments.append(l)
        if 'clkbuf' in r:
            list_of_wire_segments.append(r)
    return list(set(list_of_wire_segments))


def find_wires(conns):
    conn_mapping = {}
    list_of_wire_segments = get_wire_segments(conns)
    for l, r in conns:
        if l in conn_mapping:
            conn_mapping[l].append(r)
        else:
            conn_mapping[l] = [r]
        if r in conn_mapping:
            conn_mapping[r].append(l)
        else:
            conn_mapping[r] = [l]


    all_wire_segments = set()
    for wire_id in list_of_wire_segments:
        collected = set()
        seen = set()
        wires = [wire_id]
        while wires:
            curr = wires.pop()
            seen.add(curr)
            for n in conn_mapping[curr]:
                if n not in seen:
                    wires.append(n)
            if 'wire' in curr or 'clkbuf' in curr:
                collected.add(curr)
        all_wire_segments.add(tuple(sorted(collected))) # Sort so wires are predictably named


    n_collected = sum([len(wires) for wires in all_wire_segments])
    assert n_collected == len(list_of_wire_segments), f"{n_collected=} {len(list_of_wire_segments)=}"


    wire_id = 0
    segment_to_wire = {}
    print(f"Total number of wires: {len(all_wire_segments)=}")
    for wire_cluster in sorted(all_wire_segments): # Sort so wires are predictably named
        wire_id += 1
        wire_name = f"Wire:{wire_id}"
        for wire_segment in wire_cluster:
            segment_to_wire[wire_segment] = wire_name

    port_to_wire = {}
    for port, wire_segment in conns:
        if 'wire' in port: continue
        if 'clkbuf' in port: continue
        if port in port_to_wire:
            # This can happen (AND BE DIFFERENT) if a port has two pins on it I guess
            print(f" duplicate {port} -> {segment_to_wire[wire_segment]}")
            print(f" and       {port} -> {port_to_wire[port]}")
            assert segment_to_wire[wire_segment] == port_to_wire[port]
        port_to_wire[port] = segment_to_wire[wire_segment]

    return port_to_wire


def find_bounding(port_to_wire, box):
    ret = {}

    (xmin, ymin), (xmax, ymax) = box
    for port, wire in port_to_wire.items():
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

    port_to_wire = find_wires(all_wire_segments)
    # for port, wire in port_to_wire.items():
    #     print(port, wire)

    comparitor_box = ((50, 40), (100,60)) # Bit of a guess
    adder_box = ((50, 0), (100,40)) # Bit of a guess
    sr_1_box = ((0, 45), (50, 100))
    sr_2_box = ((0, 0), (50, 45))

    comparitor = find_bounding(port_to_wire, comparitor_box)
    adder = find_bounding(port_to_wire, adder_box)
    sr_1 = find_bounding(port_to_wire, sr_1_box)
    sr_2 = find_bounding(port_to_wire, sr_2_box)

    all_els = find_bounding(port_to_wire, ((0,0),(100,100)))

    # print_element("Comparitor", comparitor)
    print_element("Shift Register 1", sr_1)
    # print_element("ALL THE THINGS", all_els)
