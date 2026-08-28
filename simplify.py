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
        wire_name = f"Wire_{wire_id}"
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

def print_element_as_json(name, port_wire_map, wire_port_map, wire_to_alias, segment_to_wire, inputs, outputs):

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
    ret["segment_to_wire"] = segment_to_wire
    ret["possible_inputs"] = list(inputs)
    ret["possible_outputs"] = list(outputs)


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

def get_wire_name(wirename, wire_to_alias):
    tmp = wire_to_alias.get(wirename, wirename)
    tmp = tmp.replace(":", "_")
    tmp = tmp.replace("[","")
    tmp = tmp.replace("]","")
    return tmp

def print_element_as_verilog(name, port_wire_map, wire_port_map, inputs, outputs, wire_to_alias):
    """
    I sort the outputs as it makes it easier to compare changes
    """

    inputs = {get_wire_name(x, wire_to_alias) for x in inputs}
    outputs = {get_wire_name(x, wire_to_alias) for x in outputs}

    print(f"{inputs=} {outputs=}")

    element_to_ports = {}
    for port in port_wire_map:
        el = element(port)
        element_to_ports[el] = element_to_ports.get(el, list())
        element_to_ports[el].append(port)


    # Start writing the file
    lines = [f"// {name.upper()}"]
    lines.append(f"module {name}(")

    io_lines = []
    for wirename in sorted(inputs):
        io_lines.append(f"  input wire {wirename}")
    for wirename in sorted(outputs):
        io_lines.append(f"  output wire {wirename}")

    lines.append(",\n".join(io_lines))
    lines.append(f");")

    lines.append("")

    for wire in sorted(wire_port_map):
        wirename = get_wire_name(wire, wire_to_alias)
        if wirename in inputs: continue
        if wirename in outputs: continue
        lines.append(f"  wire {wirename};")

    lines.append("")

    for nodename, ports in sorted(element_to_ports.items()):
        if 'diode' in nodename: continue # Not sure why this is necessary
        node_type = nodename.split(":")[0]
        node_name = "_".join(nodename.split(":"))
        lines.append("")
        lines.append(f"  // ref component/{node_type}.v")
        if 'conb' in node_type:
            lines.append("/* verilator lint_off PINMISSING */")
        lines.append(f"  {node_type} {node_name} (")

        port_lines = []
        for port in sorted(ports):
            pinname = port.split(":")[-1]
            wirename = port_to_wire[port]
            wirename = get_wire_name(wirename, wire_to_alias)
            port_lines.append(f"    .{pinname}({wirename})")

        if 'conb' in node_type:
            lines.append("/* verilator lint_on PINMISSING */")

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
            print("WARNING ", ports[0], "is unconnected")

def get_possible_inputs_and_outputs(name, subcircuit, port_to_wire, wire_to_ports, aliases):
    """
    Heuristic should be
    * If all references to the wire are in this circuit, it cannot be an output
    * if anyone in this circuit is driving the wire it cannot be an input
    * If no-one in this circuit is driving the wire it _must_ be an input
    """
    inputs = set()
    outputs = set()
    print(aliases)
    for cell, wire in subcircuit.items():

        if alias := aliases.get(wire):
            print(f"HAVE ALIAS {alias=}, {name=}")
            # TODO: This is very hard-coded, we should fix this
            if 'success' in alias and 'output' in name:
                print("ASDDING")
                outputs.add(alias)
                continue
            if alias.startswith('O') and 'part9a' in name:
                print("ASDDING")
                outputs.add(alias)
                continue
            if alias in {"clk", "rst_n", "enable", "I"}:
                print("ASDDING")
                inputs.add(alias)
                continue



        # All references are internal - it must be an internal wire
        if all([ port in subcircuit for port in wire_to_ports[wire]]):
            print(f"{wire} is internal")
            continue

        # If we get here it must be an input or an output
        # Find whatever pin is driving it. If that pin is
        # in this subcircuit, it is an output. Otherwise,
        # It is an input
        for port in wire_to_ports[wire]:
            _, _, _, _, cname, cnt, pname = port.split(":")
            if pname not in IO_PORTS[cname][1]: continue

            # We have an output. If it's in the circuit it's an output
            if port in subcircuit:
                # port is an output
                outputs.add(aliases.get(wire, wire))
            else:
                # port is an input
                inputs.add(aliases.get(wire,wire))

    return inputs, outputs

def print_possible_inputs_and_outputs(subcircuit, port_to_wire, wire_to_ports, aliases):
    print()
    print("---------------")
    print()

    inputs, outputs = get_possible_inputs_and_outputs("unknown", subcircuit, port_to_wire, wire_to_ports, aliases)

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

def check_all_wires_driven(wire_to_ports, wire_to_alias):
    for wire, ports in wire_to_ports.items():
        found = False
        for port in ports:
            _, _, _, _, cname, _, pname = port.split(":")
            assert cname in IO_PORTS, f"Don't have io ports for {cname}"
            if pname in IO_PORTS[cname][1]:
                found = True
                break

        if not found and wire not in wire_to_alias:
            # assert False, f"No pin is driving {wire} out of {ports}"
            print(f"WARNING: No pin is driving {wire} out of {ports}")


def print_wire_aliases(segment_aliases, segment_to_wire):
    for segment, alias in segment_aliases:
        print(f"ALIAS {segment_to_wire[segment]} -> {alias}")

def compare_io(name, computed, written):
    input_computed, output_computed = computed
    input_written, output_written = written

    assert input_computed == input_written, f"ERROR in {name}: {input_computed-input_written=} {input_written-input_computed=}"

    assert output_computed == output_written, f"ERROR in {name}: {output_computed-output_written=} {output_written-output_computed=}"

if __name__ == '__main__':
    # for port, wire in port_to_wire.items():
    #     print(port, wire)

    sr1_out = set(["Wire_1","Wire_31","Wire_12","Wire_14","Wire_13","Wire_23","Wire_10","Wire_9"])#  All the Q outputs
    sr2_out = set(["Wire_19", "Wire_20", "Wire_24", "Wire_25", "Wire_26", "Wire_27", "Wire_28", "Wire_29"])

    warmup_io_map = {
        "comparitor": (
            set(["Wire_101","Wire_111","Wire_96","success","Wire_68","Wire_109","Wire_102","Wire_100","Wire_69"]),
            set(["Wire_33"])
            ),
        "adder": (
            # Possibly wrong here
            # set(["Wire_12","Wire_14","Wire_10","Wire_1","Wire_28","Wire_21","Wire_25","Wire_27","Wire_32","Wire_30","Wire_20","Wire_26","Wire_24","Wire_13","Wire_29","Wire_9"]),
            sr1_out | sr2_out,
            set(["Wire_101","Wire_111","Wire_96","success","Wire_68","Wire_109","Wire_102","Wire_100","Wire_69"])
            ),
        "sr1": (
            set(["Wire_11", "Wire_3", "Wire_8", "Wire_32"]), # RESET_B, CLK, EN, A
            sr1_out
            ),
        "sr2": (
            set(["Wire_11", "Wire_3", "Wire_8", "Wire_30"]), # RESET_B, CLK, EN, B
            sr2_out
            ),
        "all": (
            set(["Wire_11", "Wire_3", "Wire_8", "Wire_32", "Wire_30"]), # RESET_B, CLK, EN, A, B
            set(["Wire_33"]), # Output is a bool
            )
    }

    puzzle_io_map = {
            # TODO: This is all computed now, not really needed
        "part1": (
            {"rst_n", "clk", "enable", "FROM_PART2[4]", "FROM_PART3[4]"}, # rst:n, clk, enable, input0, input1
            {"TO_OUTPUT[0]", "S"}),
        "part2": (
            {"rst_n", "clk", "S"}, # rst_n, clk, S
            {"FROM_PART2[3]", "FROM_PART2[1]", "FROM_PART2[0]", "FROM_PART2[2]", "FROM_PART2[4]"}),
        "part3": (
            {"rst_n", "clk", "S", "FROM_PART2[4]"}, # rst_n, clk, S, A
            {"FROM_PART3[3]", "FROM_PART3[0]", "FROM_PART3[2]", "FROM_PART3[4]", "FROM_PART3[1]"}),
        "part4": (
            {"rst_n", "clk", "I", "S",
                "FROM_PART7A[0]", "FROM_PART7A[1]", "FROM_PART7A[2]",
                 "FROM_PART5[0]", "FROM_PART5[2]", "FROM_PART5[1]",
                 "FROM_PART7B[7]", "FROM_PART7B[6]", "FROM_PART7B[5]", "FROM_PART7B[4]", "FROM_PART7B[3]", "FROM_PART7B[2]", "FROM_PART7B[1]", "FROM_PART7C[0]",
             },
            { "TO_OUTPUT[2]", "TO_OUTPUT[1]" }),
        "part5": (
            { "FROM_PART2[2]", "FROM_PART2[0]", "FROM_PART2[4]", "FROM_PART2[3]", "FROM_PART2[1]", "S", "rst_n", "clk", "I" },
            { "TO_OUTPUT[3]", "FROM_PART5[0]", "FROM_PART5[1]", "FROM_PART5[2]" }),
        "part6": (
            {"I", "clk", "rst_n", "S", "FROM_PART8[6]", "FROM_PART8[7]", "FROM_PART8[2]", "FROM_PART8[9]", "FROM_PART8[1]", "FROM_PART8[5]", "FROM_PART8[3]", "FROM_PART8[10]", "FROM_PART8[0]", "FROM_PART8[4]", "FROM_PART8[8]"},
            {"MSG[0]", "MSG[1]", "TO_OUTPUT[5]", "TO_OUTPUT[4]"}),
        "part7a": (
            {"clk", "I", "rst_n", "S", "FROM_PART2[1]", "FROM_PART2[2]", "FROM_PART2[3]", "FROM_PART2[0]"},
            {"FROM_PART7A[2]", "FROM_PART7A[0]", "FROM_PART7A[1]"}),
        "part7b": (
            {"FROM_PART2[2]", "I", "clk", "rst_n", "S", "FROM_PART2[0]", "FROM_PART2[3]", "FROM_PART2[1]"},
            {"FROM_PART7B[0]", "FROM_PART7B[5]", "FROM_PART7B[3]", "FROM_PART7B[2]", "FROM_PART7B[6]", "FROM_PART7B[1]", "FROM_PART7B[4]", "FROM_PART7B[7]"}),
        "part7c": (
            {"S", "I", "clk", "rst_n", "FROM_PART7B[0]"},
            {"FROM_PART7C[0]"}),
        "part8": (
            {"rst_n", "I", "S", "clk", "FROM_BLOB[0]", "FROM_BLOB[1]", "FROM_BLOB[2]", "FROM_BLOB[3]" },
            {"FROM_PART8[6]", "FROM_PART8[4]", "FROM_PART8[0]", "FROM_PART8[9]", "FROM_PART8[1]", "FROM_PART8[8]", "FROM_PART8[5]", "FROM_PART8[3]", "FROM_PART8[10]", "FROM_PART8[7]", "FROM_PART8[2]"}),
        "part9a": (
            {
                "clk", "success",
                "FROM_PART9B[0]", "FROM_PART9B[1]", "FROM_PART9B[2]", "FROM_PART9B[3]", "FROM_PART9B[4]", "FROM_PART9B[5]", "FROM_PART9B[6]", "FROM_PART9B[7]",
                "MSG[2]", "MSG[3]", "MSG[0]",  "MSG[1]"
            },
            { "O[0]", "O[1]", "O[2]", "O[3]", "O[4]", "O[5]", "O[6]", "O[7]",
              "FROM_PART9A[1]", "FROM_PART9A[2]", "FROM_PART9A[3]", "FROM_PART9A[4]",
              "FROM_PART9A[5]", "FROM_PART9A[6]", "FROM_PART9A[7]", "FROM_PART9A[8]" }),
        "part9b": (
            {
                "clk", "I", "rst_n", "S",
                "FROM_PART9A[1]", "FROM_PART9A[2]", "FROM_PART9A[3]", "FROM_PART9A[4]", "FROM_PART9A[8]", "FROM_PART9A[5]", "FROM_PART9A[6]", "FROM_PART9A[7]",
                "FROM_PART9C[0]", "FROM_PART9C[1]", "FROM_PART9C[10]", "FROM_PART9C[11]", "FROM_PART9C[12]", "FROM_PART9C[13]", "FROM_PART9C[14]", "FROM_PART9C[15]",
                "FROM_PART9C[2]", "FROM_PART9C[3]", "FROM_PART9C[4]", "FROM_PART9C[5]", "FROM_PART9C[6]", "FROM_PART9C[7]", "FROM_PART9C[8]", "FROM_PART9C[9]",
                "FROM_PART9D[0]", "FROM_PART9D[1]", "FROM_PART9D[2]", "FROM_PART9D[3]", "FROM_PART9D[4]", "FROM_PART9D[5]", "FROM_PART9D[6]", "FROM_PART9D[7]",
                "FROM_PART9E[0]", "FROM_PART9E[1]", "FROM_PART9E[2]", "FROM_PART9E[3]", "FROM_PART9E[4]", "FROM_PART9E[5]", "FROM_PART9E[6]", "FROM_PART9E[7]",
             },
            {"FROM_PART9B[4]", "FROM_PART9B[3]", "FROM_PART9B[0]", "FROM_PART9B[2]", "FROM_PART9B[1]", "FROM_PART9B[5]", "FROM_PART9B[6]", "FROM_PART9B[7]"}),
        "part9c": (
            { "FROM_PART9A[1]", "FROM_PART9A[2]", "FROM_PART9A[3]", "FROM_PART9A[4]" },
            {"FROM_PART9C[15]", "FROM_PART9C[14]", "FROM_PART9C[13]", "FROM_PART9C[12]", "FROM_PART9C[11]", "FROM_PART9C[10]", "FROM_PART9C[9]", "FROM_PART9C[8]", "FROM_PART9C[7]", "FROM_PART9C[6]", "FROM_PART9C[5]", "FROM_PART9C[4]", "FROM_PART9C[3]", "FROM_PART9C[2]", "FROM_PART9C[1]", "FROM_PART9C[0]"}),
        "part9d": (
            { "FROM_PART9A[1]", "FROM_PART9A[2]", "FROM_PART9A[3]", "FROM_PART9A[4]" },
            { "FROM_PART9D[7]", "FROM_PART9D[6]", "FROM_PART9D[5]", "FROM_PART9D[4]", "FROM_PART9D[3]", "FROM_PART9D[2]", "FROM_PART9D[1]", "FROM_PART9D[0]" }),
        "part9e": (
            { "FROM_PART9A[1]", "FROM_PART9A[2]", "FROM_PART9A[3]", "FROM_PART9A[4]" },
            { "FROM_PART9E[7]", "FROM_PART9E[3]", "FROM_PART9E[2]", "FROM_PART9E[5]", "FROM_PART9E[0]", "FROM_PART9E[6]", "FROM_PART9E[4]", "FROM_PART9E[1]" }),
        "output_section": (
            { "TO_OUTPUT[0]", "TO_OUTPUT[4]", "TO_OUTPUT[1]", "TO_OUTPUT[3]", "TO_OUTPUT[2]", "TO_OUTPUT[5]", "rst_n", "clk"},
            { "MSG[2]", "MSG[3]", "success" }),
        "blob": (
            {"FROM_PART2[0]", "FROM_PART3[1]", "FROM_PART3[3]", "FROM_PART2[1]", "FROM_PART2[2]", "FROM_PART3[2]", "FROM_PART2[3]", "FROM_PART3[0]"},
            { "FROM_BLOB[0]", "FROM_BLOB[1]", "FROM_BLOB[2]", "FROM_BLOB[3]" }),
        "puzzle": (
            {"I","clk","enable","rst_n"},
            {"O[0]","O[1]","O[2]","O[3]","O[4]","O[5]","O[6]","O[7]","success"}),
    }

    puzzle_extra_aliases = {

        "Wire_8": "S",

        # This is the wierd 'output bus' on part9 that does ... something
        "Wire_95" : "FROM_PART9A[1]",
        "Wire_99" : "FROM_PART9A[2]",
        "Wire_100": "FROM_PART9A[3]",
        "Wire_84" : "FROM_PART9A[4]",
        "Wire_461": "FROM_PART9A[5]",
        "Wire_462": "FROM_PART9A[6]",
        "Wire_463": "FROM_PART9A[7]",
        "Wire_459": "FROM_PART9A[8]",

        # The blob only generates a single output
        "Wire_44": "FROM_BLOB[0]",
        "Wire_46": "FROM_BLOB[1]",
        "Wire_58": "FROM_BLOB[2]",
        "Wire_66": "FROM_BLOB[3]",

        "Wire_42":  "TO_OUTPUT[0]",
        "Wire_490": "TO_OUTPUT[1]",
        "Wire_221": "TO_OUTPUT[2]",
        "Wire_161": "TO_OUTPUT[3]",
        "Wire_437": "TO_OUTPUT[4]",
        "Wire_395": "TO_OUTPUT[5]",

        'Wire_183': "FROM_PART7A[0]",
        'Wire_188': "FROM_PART7A[1]",
        'Wire_288': "FROM_PART7A[2]",

        "Wire_110": "FROM_PART2[0]",
        "Wire_129": "FROM_PART2[1]",
        "Wire_79":  "FROM_PART2[2]",
        "Wire_80":  "FROM_PART2[3]",
        "Wire_427": "FROM_PART2[4]",

        "Wire_448": "FROM_PART5[0]",
        "Wire_446": "FROM_PART5[1]",
        "Wire_447": "FROM_PART5[2]",

        "Wire_28" : "FROM_PART3[0]",
        "Wire_309": "FROM_PART3[1]",
        "Wire_315": "FROM_PART3[2]",
        "Wire_71" : "FROM_PART3[3]",
        "Wire_394": "FROM_PART3[4]",

        'Wire_1'  : "FROM_PART8[10]",
        'Wire_165': "FROM_PART8[9]",
        'Wire_196': "FROM_PART8[8]",
        'Wire_216': "FROM_PART8[7]",
        'Wire_31' : "FROM_PART8[6]",
        'Wire_33' : "FROM_PART8[5]",
        'Wire_37' : "FROM_PART8[4]",
        'Wire_38' : "FROM_PART8[3]",
        'Wire_41' : "FROM_PART8[2]",
        'Wire_458': "FROM_PART8[1]",
        'Wire_650': "FROM_PART8[0]",

        "Wire_396": "FROM_PART9E[7]",
        "Wire_397": "FROM_PART9E[6]",
        "Wire_45" : "FROM_PART9E[5]",
        "Wire_47" : "FROM_PART9E[4]",
        "Wire_48" : "FROM_PART9E[3]",
        "Wire_49" : "FROM_PART9E[2]",
        "Wire_50" : "FROM_PART9E[1]",
        "Wire_51" : "FROM_PART9E[0]",


        "Wire_62" : "FROM_PART9D[7]",
        "Wire_101": "FROM_PART9D[6]",
        "Wire_83" : "FROM_PART9D[5]",
        "Wire_82" : "FROM_PART9D[4]",
        "Wire_65" : "FROM_PART9D[3]",
        "Wire_61" : "FROM_PART9D[2]",
        "Wire_67" : "FROM_PART9D[1]",
        "Wire_63" : "FROM_PART9D[0]",


        'Wire_103': "FROM_PART9C[15]",
        'Wire_398': "FROM_PART9C[14]",
        'Wire_399': "FROM_PART9C[13]",
        'Wire_465': "FROM_PART9C[12]",
        'Wire_466': "FROM_PART9C[11]",
        'Wire_467': "FROM_PART9C[10]",
        'Wire_52' : "FROM_PART9C[9]",
        'Wire_54' : "FROM_PART9C[8]",
        'Wire_55' : "FROM_PART9C[7]",
        'Wire_56' : "FROM_PART9C[6]",
        'Wire_57' : "FROM_PART9C[5]",
        'Wire_59' : "FROM_PART9C[4]",
        'Wire_60' : "FROM_PART9C[3]",
        'Wire_68' : "FROM_PART9C[2]",
        'Wire_69' : "FROM_PART9C[1]",
        'Wire_70' : "FROM_PART9C[0]",

        "Wire_623": "FROM_PART7B[7]",
        "Wire_631": "FROM_PART7B[6]",
        "Wire_370": "FROM_PART7B[5]",
        "Wire_624": "FROM_PART7B[4]",
        "Wire_191": "FROM_PART7B[3]",
        "Wire_649": "FROM_PART7B[2]",
        "Wire_648": "FROM_PART7B[1]",
        "Wire_536": "FROM_PART7B[0]",

        "Wire_647": "FROM_PART7C[0]",

        "Wire_393": "MSG[0]",
        "Wire_392": "MSG[1]",
        "Wire_138": "MSG[2]",
        "Wire_3"  : "MSG[3]",

        "Wire_509": "FROM_PART9B[0]",
        "Wire_507": "FROM_PART9B[1]",
        "Wire_460": "FROM_PART9B[2]",
        "Wire_483": "FROM_PART9B[3]",
        "Wire_510": "FROM_PART9B[4]",
        "Wire_495": "FROM_PART9B[5]",
        "Wire_494": "FROM_PART9B[6]",
        "Wire_493": "FROM_PART9B[7]",

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

        with measure_time("check all wires are driven"):
            check_all_wires_driven(wire_to_ports, wire_to_alias)

        with measure_time("Validations"):
            check_only_single_output_on_wire(wire_to_ports)
            check_all_ports_filled(port_to_wire)

        for name, box in [
                    ('comparitor', ((50, 40), (100, 60))), # Bit of a guess
                    ('adder',      ((50, 0),  (100, 40))), # Bit of a guess
                    ('sr1',        ((0,  45), (50,  100))),
                    ('sr2',        ((0,  0),  (50,  45))),
                    ('all',        ((0,  0),  (100, 100))),
                    ]:
            sub_circuit = find_bounding(port_to_wire, box)
            revd = reverse_map(sub_circuit)
            print_unconnected_elements(revd)
            print_element(name.upper(), sub_circuit)
            print_possible_inputs_and_outputs(sub_circuit, port_to_wire, wire_to_ports, wire_to_alias)
            inputs, outputs = get_possible_inputs_and_outputs(name, sub_circuit, port_to_wire, wire_to_ports, wire_to_alias)
            print_element_as_json(name, sub_circuit, revd, wire_to_alias, segment_to_wire, inputs, outputs)
            print_element_as_verilog(name, sub_circuit, revd, warmup_io_map[name][0], warmup_io_map[name][1], wire_to_alias)
            print_wire_aliases(segment_aliases, segment_to_wire)

    elif sys.argv[1] == 'puzzle':
        name = sys.argv[1]

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

            for wire, alias in puzzle_extra_aliases.items():
                wire_to_alias[wire] = alias

        with measure_time("reverse map"):
            wire_to_ports = reverse_map(port_to_wire)

        with measure_time("check all wires are driven"):
            check_all_wires_driven(wire_to_ports, wire_to_alias)

        with measure_time("Validations"):
            check_only_single_output_on_wire(wire_to_ports)
            check_all_ports_filled(port_to_wire)
        with measure_time("Print as json"):
            print_element_as_json('puzzle', port_to_wire, wire_to_ports, wire_to_alias, segment_to_wire, [], [])
        print_wire_aliases(segment_aliases, segment_to_wire)
        print_element_as_verilog(name, port_to_wire, wire_to_ports, puzzle_io_map[name][0], puzzle_io_map[name][1], wire_to_alias)

        total_io = {}
        for name, box in [
                ('part1', ((23, 190), (48, 212))),
                ('part2', ((23, 136), (48, 170))),
                ('part3', ((23, 87),  (48, 120))),
                ('part4', ((61, 125), (100, 170))),
                ('part5', ((61, 87),  (100, 125))),
                ('part6', ((61, 10),  (100, 67))),
                ('part7a', ((100, 266), (138, 300))),
                ('part7b', ((100, 195), (138, 266))),
                ('part7c', ((100, 179), (138, 195))),
                ('part8', ((100, 34), (138, 174))),
                ('output_section', ((151, 266), (200, 300))), # Checked and this looks to be correct
                ('part9b', ((138, 163), (200, 235))),
                ('part9c', ((138, 120), (200, 163))),
                ('part9d', ((138, 105), (200, 120))),
                ('part9e', ((138, 70), (200, 105))),
                ('blob', ((138, 5), (200, 70))),
                ('part9a', ((138, 235), (200, 266))),
                ]:
            sub_circuit = find_bounding(port_to_wire, box)
            revd = reverse_map(sub_circuit)
            print_unconnected_elements(revd)
            print_element(name.upper(), sub_circuit)
            print_possible_inputs_and_outputs(sub_circuit, port_to_wire, wire_to_ports, wire_to_alias)
            inputs, outputs = get_possible_inputs_and_outputs(name, sub_circuit, port_to_wire, wire_to_ports, wire_to_alias)
            print_element_as_json(name, sub_circuit, revd, wire_to_alias, segment_to_wire, inputs, outputs)
            print_element_as_verilog(name, sub_circuit, revd, puzzle_io_map[name][0], puzzle_io_map[name][1], wire_to_alias)
            print_wire_aliases(segment_aliases, segment_to_wire)

            compare_io(name, (inputs, outputs), puzzle_io_map[name])

            total_io[name] = {}
            total_io[name]['in'] = [wire_to_alias.get(_in,_in) for _in in sorted(inputs)]
            total_io[name]['out'] = [wire_to_alias.get(_out,_out) for _out in sorted(outputs)]

        with open("outputs/total_io.json", "w") as fp:
            json.dump(total_io, fp, indent=2)


    else:
        print(f"Unknown object '{sys.argv[1]}'", file=sys.stderr)
        sys.exit(1)

