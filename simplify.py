import sys
import json
import os
from common import IO_PORTS, measure_time

def get_wire_segments(conns):
    list_of_wire_segments = []
    for l, r in conns:
        if 'wire' in l:
            list_of_wire_segments.append(l)
        if 'wire' in r:
            list_of_wire_segments.append(r)
        if 'buf' in l:
            list_of_wire_segments.append(l)
        if 'buf' in r:
            list_of_wire_segments.append(r)
        if 'diode' in l:
            list_of_wire_segments.append(l)
        if 'diode' in r:
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
    set_of_wire_segments = set(list_of_wire_segments)
    set_of_wire_segments_copy = set(list_of_wire_segments)
    seen = set()
    while set_of_wire_segments:
        wire_id = set_of_wire_segments.pop()
        collected = set()
        wires = [wire_id]
        while wires:
            curr = wires.pop()
            if 'buf' in curr:
                A = curr.replace("X","A")
                X = curr.replace("A","X")
                seen.add(A)
                seen.add(X)
                set_of_wire_segments.discard(A)
                set_of_wire_segments.discard(X)
                if A in conn_mapping:
                    for n in conn_mapping[A]:
                        if n not in seen:
                            wires.append(n)
                if X in conn_mapping:
                    for n in conn_mapping[X]:
                        if n not in seen:
                            wires.append(n)
                collected.add(A)
                collected.add(X)
            else:
                seen.add(curr)
                set_of_wire_segments.discard(curr)
                for n in conn_mapping[curr]:
                    if n not in seen:
                        wires.append(n)
                if 'wire' in curr:
                    collected.add(curr)
        all_wire_segments.add(tuple(sorted(collected))) # Sort so wires are predictably named


    n_collected = sum([len(wires) for wires in all_wire_segments])
    all_collected = set()
    for wires in all_wire_segments:
        for wire in wires:
            all_collected.add(wire)
    print("ALL", all_collected - set(list_of_wire_segments))
    print()
    print("LST", set(list_of_wire_segments) - all_collected)
    print()



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
        if 'buf' in port: continue
        if port in port_to_wire:
            # This can happen (AND BE DIFFERENT) if a port has two pins on it I guess
            # print(f" duplicate {port} -> {segment_to_wire[wire_segment]}")
            # print(f" and       {port} -> {port_to_wire[port]}")
            assert segment_to_wire[wire_segment] == port_to_wire[port]
        port_to_wire[port] = segment_to_wire[wire_segment]

    return port_to_wire, segment_to_wire


def find_bounding(port_to_wire, box):
    ret = {}

    (xmin, ymin), (xmax, ymax) = box
    for port, wire in port_to_wire.items():
        """ eg 'x:26.220:y:70.720:mux2_1:12:A0 """
        _, x, _, y, name, _, _ = port.split(":")
        x, y = float(x), float(y)

        # It seems clocks don't always keep within domains
        # so just add them in
        if 'buf' in name:
            ret[port] = wire

        if x < xmin or x > xmax or y < ymin or y > ymax:
            continue

        ret[port] = wire

    return ret

def prettify(port):
    port_pretty = ":".join(port.split(":")[4:])
    port_pretty = port_pretty.replace("_1","").replace("_2","")
    return port_pretty

def print_element(name, port_wire_map):
    print()
    print(f"---------------------{name.upper()}--------------------")
    print()
    old = ""
    for port, wire in sorted(port_wire_map.items(), key=lambda x: x[0]):
        port_pretty = prettify(port)
        if old != port_pretty:
            old = port_pretty
            print(port_pretty, '->')
        print("    ", wire)

    print()
    print(f"-----------------------------------------")
    print()
    old = ""
    for port, wire in sorted(port_wire_map.items(), key=lambda x: x[1]):
        port_pretty = prettify(port)
        if old != wire:
            old = wire
            print(wire, '->')
        print("    ", port_pretty)

    print()

def element(port):
    return ":".join(port.split(":")[4:6]).replace("_1","").replace("_2","")

def print_element_as_json(name, port_wire_map, wire_port_map, wire_to_alias):

    ret = {}

    ret["wires"] = list(sorted(wire_port_map.keys()))
    ret["elements"] = list(sorted(set([element(port) for port in port_wire_map.keys()])))

    element_position = {}
    for port in port_wire_map:
        # Take the minimal position as the canonical position
        pretty = element(port)
        _, x, _, y, _, _, _ = port.split(":")
        x, y = float(x), float(y)
        element_position[pretty] = element_position.get(pretty, (10_000, 10_000))
        if element_position[pretty] > (x, y):
            element_position[pretty] = (x, y)

    ret["element_position"] = element_position

    ret["port_to_wire"] = {prettify(port): wire for port, wire in port_wire_map.items()}
    ret["wire_to_ports"] = {wire: [prettify(port) for port in ports] for wire, ports, in wire_port_map.items()}
    ret["wire_to_alias"] = wire_to_alias


    name = f"outputs/{name}.json"
    with open(name, "w") as fp:
        json.dump(ret, fp, indent=2)


def get_output_port_from_list(ports):
    data = IO_PORTS
    for port in ports:
        _, _, _, _, cname, _, pname = port.split(":")
        if pname in data[cname][1]:
            return port

def prettify1(port):
    _type, _id, _pin = port.split(":")[4:]
    _type = _type.replace("_1","").replace("_2","")
    return f"{_type}:{_id}.{_pin}"

def print_element_as_verilog(name, port_wire_map, wire_port_map, inputs, outputs, wire_to_alias):
    """
    I sort the outputs as it makes it easier to compare changes
    """

    element_to_ports = {}
    for port in port_wire_map:
        el = element(port)
        element_to_ports[el] = element_to_ports.get(el, list())
        element_to_ports[el].append(port)


    # Start writing the file
    lines = [f"// {name.upper()}"]
    lines.append(f"module {name}(")

    io_lines = []
    for _in in sorted(inputs):
        _in = wire_to_alias.get(_in, _in)
        io_lines.append(f"  input wire {_in.replace(":","_")}")
    for _out in sorted(outputs):
        _out = wire_to_alias.get(_out, _out)
        io_lines.append(f"  output wire {_out.replace(":","_")}")

    lines.append(",\n".join(io_lines))
    lines.append(f");")

    lines.append("")

    for wire in sorted(wire_port_map):
        if wire in inputs: continue
        if wire in outputs: continue
        wire = wire_to_alias.get(wire, wire)
        lines.append(f"  wire {wire.replace(":","_")};")

    lines.append("")

    for nodename, ports in sorted(element_to_ports.items()):
        node_type = nodename.split(":")[0]
        node_name = "_".join(nodename.split(":"))
        lines.append(f"  {node_type} {node_name} (")

        port_lines = []
        for port in sorted(ports):
            pinname = port.split(":")[-1]
            wirename = port_to_wire[port]
            wirename = wire_to_alias.get(wirename, wirename).replace(":", "_")
            line = f"    .{pinname}({wirename})"
            port_lines.append(line)
        lines.append(",\n".join(port_lines))
        lines.append("  );")

    lines.append("endmodule")

    with open(f"outputs/{name}.v", "w") as fp:
        fp.write("\n".join(lines))





def check_only_single_output_on_wire(wire_to_ports):
    """ eg 'x:26.220:y:70.720:mux2_1:12:A0 """
    # _, x, _, y, name, _, _ = port.split(":")

    data = IO_PORTS

    for wire, ports in wire_to_ports.items():
        output_count = 0

        for port in ports:
            _, _, _, _, cname, _, pname = port.split(":")
            if pname in data[cname][1]:
                output_count += 1
                assert output_count <=1, f"More than one output feeding {wire} -> {pname=} -> {data[cname][1]=}"

def check_all_ports_filled(port_to_wire):
    all_cells = {}
    for port in port_to_wire:
        _, _, _, _, cname, cnt, pname = port.split(":")

        cell_name = f"{cname}:{cnt}"
        all_cells[cell_name] = all_cells.get(cell_name, set())
        all_cells[cell_name].add(pname)

    data = IO_PORTS
    for cell, ports in all_cells.items():
        cellname = cell.split(":")[0]
        expected = set.union(IO_PORTS[cellname][0], IO_PORTS[cellname][1])
        if 'conb' in cellname and expected != ports:
            print(f"Maybe warning? {expected=} {ports=} but probably fine for conb")
        else:
            assert expected == ports, f"{expected=} {ports=}"


def reverse_map(port_to_wire):
    wire_to_ports = {}
    for port, wire in port_to_wire.items():
        if wire in wire_to_ports:
            wire_to_ports[wire].append(port)
        else:
            wire_to_ports[wire] = [port]
    return wire_to_ports

def print_unconnected_elements(revd):
    print()
    for wire, ports in revd.items():
        if len(ports) == 1:
            print("print", ports[0], "is unconnected")

def get_possible_inputs_and_outputs(subcircuit, port_to_wire, wire_to_ports):
    inputs = set()
    outputs = set()
    for cell, wire in subcircuit.items():
        for port in wire_to_ports[wire]:
            if port not in subcircuit:
                _, _, _, _, cname, cnt, pname = cell.split(":")
                if pname in IO_PORTS[cname][1]:
                    # port is an output
                    outputs.add(wire)
                else:
                    # port is an input
                    inputs.add(wire)

    return inputs, outputs

def print_possible_inputs_and_outputs(subcircuit, port_to_wire, wire_to_ports):
    print()
    print("---------------")
    print()

    inputs, outputs = get_possible_inputs_and_outputs(subcircuit, port_to_wire, wire_to_ports)

    for wire in outputs:
        print(f"Output: [inside] -> {wire} -> [outside]")
    for wire in inputs:
        print(f"Input: [outside] -> {wire} -> [inside]")

def read_wire_segments(filename):
    all_wire_segments = []
    with open(filename) as fp:
        for line in fp:
            l, _, r = line.split()
            all_wire_segments.append((l, r))
    return all_wire_segments

def check_ports(segments):
    data = IO_PORTS
    for segment in segments:
        for x in segment:
            if 'wire' in x: continue
            _, _, _, _, cname, _, pname = x.split(":")
            assert cname in IO_PORTS, f"Don't have io ports for {cname}"
            all_pins = IO_PORTS[cname][0] | IO_PORTS[cname][1]
            assert pname in all_pins, f"{pname} not in {all_pins} for {cname}"

def print_wire_aliases(segment_aliases, segment_to_wire):
    for segment, alias in segment_aliases:
        print(f"ALIAS {segment_to_wire[segment]} -> {alias}")

if __name__ == '__main__':
    # for port, wire in port_to_wire.items():
    #     print(port, wire)

    sr1_out = set(["Wire:1","Wire:31","Wire:12","Wire:14","Wire:13","Wire:23","Wire:10","Wire:9"])#  All the Q outputs
    sr2_out = set(["Wire:19", "Wire:20", "Wire:24", "Wire:25", "Wire:26", "Wire:27", "Wire:28", "Wire:29"])

    warmup_io_map = {
        "comparitor": (
            set(["Wire:101","Wire:111","Wire:96","Wire:2","Wire:68","Wire:109","Wire:102","Wire:100","Wire:69"]),
            set(["Wire:33"])
            ),
        "adder": (
            # Possibly wrong here
            # set(["Wire:12","Wire:14","Wire:10","Wire:1","Wire:28","Wire:21","Wire:25","Wire:27","Wire:32","Wire:30","Wire:20","Wire:26","Wire:24","Wire:13","Wire:29","Wire:9"]),
            sr1_out | sr2_out,
            set(["Wire:101","Wire:111","Wire:96","Wire:2","Wire:68","Wire:109","Wire:102","Wire:100","Wire:69"])
            ),
        # TODO: These seem a bit odd - sr1 and sr2 should have the same clock!
        "sr1": (
            set(["Wire:11", "Wire:3", "Wire:8", "Wire:32"]), # RESET_B, CLK, EN, A
            sr1_out
            ),
        "sr2": (
            set(["Wire:11", "Wire:3", "Wire:8", "Wire:30"]), # RESET_B, CLK, EN, B
            sr2_out
            ),
        "all": (
            # TODO:
            set(["Wire:11", "Wire:3", "Wire:8", "Wire:32", "Wire:30"]), # RESET_B, CLK, EN, A, B
            set(["Wire:33"]), # Output is a bool
            )
    }

    if sys.argv[1] == 'warmup':

        with measure_time("read segments"):
            all_wire_segments = read_wire_segments(f"outputs/{sys.argv[1]}.txt")

        with measure_time("read aliases"):
            segment_aliases = read_wire_segments(f"outputs/{sys.argv[1]}-aliases.txt")

        with measure_time("check ports"):
            check_ports(all_wire_segments)

        with measure_time("Find wires and aliases"):
            port_to_wire, segment_to_wire = find_wires(all_wire_segments)
            wire_to_alias = {
                segment_to_wire[segment]: alias for segment, alias in segment_aliases
            }


        with measure_time("reverse map"):
            wire_to_ports = reverse_map(port_to_wire)

        with measure_time("Validations"):
            check_only_single_output_on_wire(wire_to_ports)
            check_all_ports_filled(port_to_wire)

        for name, box in [
                    ('comparitor', ((50, 40), (100,60))), # Bit of a guess
                    ('adder', ((50, 0), (100,40))), # Bit of a guess
                    ('sr1', ((0, 45), (50, 100))),
                    ('sr2', ((0, 0), (50, 45))),
                    ('all', ((0, 0), (100, 100))),
                    ]:
            sub_circuit = find_bounding(port_to_wire, box)
            revd = reverse_map(sub_circuit)
            print_unconnected_elements(revd)
            print_element(name.upper(), sub_circuit)
            print_possible_inputs_and_outputs(sub_circuit, port_to_wire, wire_to_ports)
            print_element_as_json(name, sub_circuit, revd, wire_to_alias)
            inputs, outputs = get_possible_inputs_and_outputs(sub_circuit, port_to_wire, wire_to_ports)
            print_element_as_verilog(name, sub_circuit, revd, warmup_io_map[name][0], warmup_io_map[name][1], wire_to_alias)
            print_wire_aliases(segment_aliases, segment_to_wire)

    elif sys.argv[1] == 'puzzle':

        with measure_time("read segments"):
            all_wire_segments = read_wire_segments(f"outputs/{sys.argv[1]}.txt")

        with measure_time("read aliases"):
            segment_aliases = read_wire_segments(f"outputs/{sys.argv[1]}-aliases.txt")

        with measure_time("check ports"):
            check_ports(all_wire_segments)

        with measure_time("Find wires"):
            port_to_wire, segment_to_wire = find_wires(all_wire_segments)

            wire_to_alias = {
                segment_to_wire[segment]: alias for segment, alias in segment_aliases
            }

        with measure_time("reverse map"):
            wire_to_ports = reverse_map(port_to_wire)

        with measure_time("Validations"):
            check_only_single_output_on_wire(wire_to_ports)
            check_all_ports_filled(port_to_wire)
        with measure_time("Print as json"):
            print_element_as_json('puzzle', port_to_wire, wire_to_ports, wire_to_alias)
        print_wire_aliases(segment_aliases, segment_to_wire)
    else:
        print(f"Unknown object '{sys.argv[1]}'", file=sys.stderr)
        sys.exit(1)

