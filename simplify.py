
def find_wires(conns):
    wire_mapping = {}
    wire_segment_mapping = {}
    for l, r in conns:
        if 'wire' not in l:
            wire_segment_mapping[l] = r
        elif 'wire' not in r:
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
    for wire in all_wires:
        canonical_id += 1
        canonical_name = f"Canonical:{canonical_id}"
        for wire_segment in wire:
            segment_mapping[wire_segment] = canonical_name

    for port, wire_segment in wire_segment_mapping.items():
        print(port, '->', segment_mapping[wire_segment])



if __name__ == '__main__':
    _all = []
    with open('graph.txt') as fp:
        for line in fp:
            l, _, r = line.split()
            _all.append((l, r))

    find_wires(_all)



