import gdstk
import os
import sys
from common import labels_i_care_about, increase_view, name_to_layer, layer_to_name, layer_ordering, layers_i_care_about, measure_time

"""
We build up the network like this:
    1. Filter out all the non-wire things from the design
    2. Attach the cell name and port name to the geometry as a 'property'
    3. Flatten the design in a custom way so that we can also attach the reference id
"""

def write_files(library, cell, name):
    filename = f"{name}.svg"
    cell.write_svg(filename)
    # Turns out the svg includes labels by default but
    # I find the original size quite hard to see, so I'll
    # fudge it here
    increase_view(filename)
    try:
        os.unlink(f"{name}.gds")
    except:
        pass
    library.write_gds(f"{name}.gds")


def filter_layers(library):

    # Dumb, but labels don't have a datatype
    layers_i_care_about_1 = set(x[0] for x in layers_i_care_about)
    for cell in library.cells:

        for label in cell.labels:
            if (label.layer) not in layers_i_care_about_1:
                # print(f"Removing {label.layer=}")
                cell.remove(label)

        for polygon in cell.polygons:
            if (polygon.layer, polygon.datatype) not in layers_i_care_about:
                # print(f"Removing {polygon.layer=} {polygon.datatype=}")
                cell.remove(polygon)

        for path in cell.paths:
            if (path.layers[0], path.datatypes[0]) not in layers_i_care_about:
                # print(f"Removing {path.layers=} {path.datatypes=}")
                cell.remove(path)

def filter_filters(library):

    top = library.top_level()
    assert len(top) == 1
    cell = top[0]
    for ref in cell.references:

        # print(f"{ref.cell.name=}")
        # Filters
        if 'decap' in ref.cell.name:
            # print(f" kill")
            ref.cell.remove(*ref.cell.polygons)
        if 'tapvpwr' in ref.cell.name:
            # print(f" kill")
            ref.cell.remove(*ref.cell.polygons)

        # Some power vias
        if '320_320' in ref.cell.name:
            # print(f" kill")
            ref.cell.remove(*ref.cell.polygons)
        if '400_400' in ref.cell.name:
            # print(f" kill")
            ref.cell.remove(*ref.cell.polygons)

        # Adding these guys takes us from 2 mins to 42 seconds
        if '1600_1600' in ref.cell.name:
            # print(f" kill")
            ref.cell.remove(*ref.cell.polygons)
        if 'INTERNAL' in ref.cell.name:
            # print(f" kill")
            ref.cell.remove(*ref.cell.polygons)
        if 'PR' in ref.cell.name:
            # print(f" kill")
            ref.cell.remove(*ref.cell.polygons)

def filter_pads(library):
    """
    Here we want to take all possible ports (On layer li, or 67,20)
    and Remove any that aren't IO ports
    """
    for cell in library.cells:

        name = cell.name

        collected_labels = []
        for label in cell.labels:
            if label.layer == 67 and label.text in labels_i_care_about:
                collected_labels.append(label)
            else:
                cell.remove(label)

        direct_pads = []
        for polygon in cell.polygons:
            if (polygon.layer, polygon.datatype) != (67, 20): continue

            keep = False
            for label in collected_labels:
                origin = label.origin
                if polygon.contain(label.origin):
                    # We're collecting the port name for later
                    name = cell.name.replace('sky130_fd_sc_hd__','')
                    polygon.set_property("port_name", f"{name}:{label.text}")
                    direct_pads.append((polygon, label.text))

        # Here we check for overlapping pads, because only one of them may have
        # a label over them, but they are connected/the same
        for polygon in cell.polygons:
            if (polygon.layer, polygon.datatype) != (67, 20): continue

            keep = False
            for poly, text in direct_pads:
                if polygon == poly:
                    keep = True
                    break
                elif overlaps(polygon, poly):
                    print(f"FOUND OVERLAPPPPPP on '{poly.get_property('port_name')}'")
                    name = cell.name.replace('sky130_fd_sc_hd__','')
                    polygon.set_property("port_name", f"{name}:{text}")
                    keep = True
                    break

            if not keep:
                cell.remove(polygon)


def custom_flatten(library):
    """
    This copies the 'flatten' logic from the original library,
    but allows me to preserve the type of cell the polys
    came from, and which port it is
    """

    count = {}

    top = library.top_level()
    assert len(top) == 1
    cell = top[0]
    for i, ref in enumerate(cell.references):

        name = ref.cell.name
        name = name.replace('sky130_fd_sc_hd__','')
        count[name] = count.get(name, 0) + 1

        # Paths apparently don't need to be moved?
        # Also TODO: Should actually convert to polys
        # to allow easy overlay checking
        paths = ref.cell.get_paths()
        for path in paths:
            path.translate(*ref.origin)

        polys = ref.cell.get_polygons()
        for poly in polys:
            port_name = poly.get_property("port_name")
            if port_name:

                port_name = port_name[0].decode('utf-8')
                _, _port = port_name.split(':')

                x, y = ref.origin
                port_id = f"x:{x:.3f}:y:{y:.3f}:{name}:{count[name]}:{_port}"
                # print(f"{port_name=} {port_id=}")
                # Now every circuit element port identifies itself
                poly.set_property("port_id", port_id)

            # Transorm to the position of the reference
            poly.transform(ref.magnification, ref.x_reflection, ref.rotation, ref.origin)

        # # TODO: Move labels to be in the right place
        # # Although to be honest I don't really need them anymore
        # for l in ref.cell.get_labels():
        #     # TODO: Fix label locations - Something about the translation + magnification is not working.
        #     # Instead, I should copy the 'transform' function similar to the polys
        #     new_origin = l.origin[0] + ref.origin[0], l.origin[1] + ref.origin[1]
        #     labels.append(
        #         gdstk.Label(
        #             l.text,
        #             ref.origin, #new_origin,
        #             anchor=l.anchor,
        #             # rotation=l.rotation,
        #             magnification=l.magnification,
        #             # x_reflection=l.x_reflection,
        #             layer=l.layer,
        #             texttype=0
        #         )
        #    )

        cell.add(*polys, *paths)
    # cell.remove(*cell.references)

    for ref in cell.references:
        # cell.remove(ref) # For some reason this library hates having references removed?
        ref.cell.remove(*ref.cell.polygons)
        ref.cell.remove(*ref.cell.paths)


def overlaps(a, b):
    """
    Just do bounding box. It's not idea but it'll have to do
    """
    (a_xmin, a_ymin), (a_xmax, a_ymax) = a.bounding_box()
    (b_xmin, b_ymin), (b_xmax, b_ymax) = b.bounding_box()

    ret = True
    if a_xmax < b_xmin: return False
    if a_xmin > b_xmax: return False
    if a_ymax < b_ymin: return False
    if a_ymin > b_ymax: return False

    # We'll see if this fixes the issue of mux A0 and A1 overlapping
    if a.contain_any(*b.points): return True
    if b.contain_any(*a.points): return True

    # I can't remember if this helps or not
    if gdstk.boolean(a, b, 'and'): return True


    # print(f"{a.bounding_box()} {b.bounding_box()} {ret=}")
    return False

# # This doesn't work, it is over-agressive and very slow
# def overlaps(a, b):
#     if a.contain_all(*b.points): return True
#     if b.contain_all(*a.points): return True
#
#     return False


def singly_connected(el, mid, lower, upper):
    for poly in lower:
        if overlaps(poly, el): return True
    for poly in upper:
        if overlaps(poly, el): return True
    for poly in mid:
        if poly == el:
            continue
        if overlaps(poly, el): return True
    return False

def doubly_connected(el, lower, upper):
    maybe = False
    for poly in lower:
        if overlaps(poly, el):
            maybe = True
            break

    if not maybe: return False

    for poly in upper:
        if overlaps(poly, el): return True
    return False


def connected_components(cell):

    print("Connected components")

    layer_elements = {
        key: [] for key in name_to_layer.keys()
    }
    wires = 0

    # Map from layer, datatype -> layer_name
    for poly in cell.polygons:
        layer_name = layer_to_name[poly.layer, poly.datatype]
        layer_elements[layer_name].append(poly)

    for poly in cell.polygons:
        layer_name = layer_to_name[poly.layer, poly.datatype]
        # Do vias and mcon first as they have the stricted requirements to be
        # connected top and bottom
        if layer_name not in {"mcon", "via", "via2", "via3"}: continue

        layer_name = layer_to_name[poly.layer, poly.datatype]

        layer_offset = layer_ordering.index(layer_name)
        lower = layer_offset-1
        upper = layer_offset+1

        if lower < 0:
            lower_layers = []
            upper_layers = layer_elements[layer_ordering[upper]]
        elif upper >= len(layer_ordering):
            lower_layers = layer_elements[layer_ordering[lower]]
            upper_layers = []
        else:
            upper_layers = layer_elements[layer_ordering[upper]]
            lower_layers = layer_elements[layer_ordering[lower]]

        connected = doubly_connected(poly, lower_layers, upper_layers)

        if not connected:
            cell.remove(poly)
        else:
            wires += 1
            if not poly.get_property("port_id"):
                poly.set_property("wire_seg_id", f"wire:{wires}")

    for poly in cell.polygons:
        layer_name = layer_to_name[poly.layer, poly.datatype]
        if layer_name in {"mcon", "via", "via2", "via3"}: continue
        layer_name = layer_to_name[poly.layer, poly.datatype]

        layer_offset = layer_ordering.index(layer_name)
        lower = layer_offset-1
        upper = layer_offset+1

        mid = layer_elements[layer_ordering[layer_offset]]
        if lower < 0:
            lower_layers = []
            upper_layers = layer_elements[layer_ordering[upper]]
        elif upper >= len(layer_ordering):
            lower_layers = layer_elements[layer_ordering[lower]]
            upper_layers = []
        else:
            upper_layers = layer_elements[layer_ordering[upper]]
            lower_layers = layer_elements[layer_ordering[lower]]

        connected = singly_connected(poly, mid, lower_layers, upper_layers)

        if not connected:
            cell.remove(poly)
        else:
            wires += 1
            if not poly.get_property("port_id"):
                poly.set_property("wire_seg_id", f"wire:{wires}")

    # TODO: Improve via filtering? Vias must connect above and below
    # TODO: Would there be any abutted elements? like a poly to a line on the same layer?

    # WORKING UP TO HERE WITH DIRECTIONAL ARTIFACTS

def convert_paths(library):
    for cell in library.cells:
        for path in cell.paths:
            cell.add(*path.to_polygons())
            cell.remove(path)


def cell_graph(cell):

    layer_elements = {
        key: [] for key in name_to_layer.keys()
    }

    ret = []

    for poly in cell.polygons:
        layer_name = layer_to_name[poly.layer, poly.datatype]
        layer_elements[layer_name].append(poly)

    for poly in cell.polygons:
        layer_name = layer_to_name[poly.layer, poly.datatype]
        if layer_name == 'li1': continue

        layer_offset = layer_ordering.index(layer_name)
        lower = layer_offset-1
        upper = layer_offset+1

        if lower < 0:
            lower_layers = []
        elif upper >= len(layer_ordering):
            lower_layers = layer_elements[layer_ordering[lower]]
        else:
            lower_layers = layer_elements[layer_ordering[lower]]

        mid = layer_elements[layer_ordering[layer_offset]]

        wire_seg_id = poly.get_property("wire_seg_id")[0].decode('utf-8')

        for el in lower_layers:
            if overlaps(poly, el):
                if layer_name == 'mcon':
                    port_id = el.get_property("port_id")[0].decode('utf-8')
                    ret.append((str(port_id), str(wire_seg_id)))
                else:
                    wire2_id = el.get_property("wire_seg_id")[0].decode('utf-8')
                    ret.append((str(wire2_id), str(wire_seg_id)))

        for el in mid:
            if poly == el:
                continue
            if overlaps(poly, el):
                if layer_name == 'mcon':
                    port_id = el.get_property("port_id")[0].decode('utf-8')
                    ret.append((str(port_id), str(wire_seg_id)))
                else:
                    wire2_id = el.get_property("wire_seg_id")[0].decode('utf-8')
                    ret.append((str(wire2_id), str(wire_seg_id)))

    return ret

def counts(library, top):

    cnts = {}
    for poly in library[top].polygons:
        if port_name := poly.get_property("port_name"):
            port_name = port_name[0].decode('utf-8')
            name, port = port_name.split(":")
            cnts[name] = cnts.get(name, {})
            cnts[name][port] = cnts[name].get(port, 0) + 1

    return cnts


def compare_counts(a,b):
    print("NAME, PORT, COUNT")
    assert a.keys() == b.keys(), f"{a.keys()=} {b.keys()=}"
    for name in a:
        assert a[name].keys() == b[name].keys(), f"{a[name].keys()=} {b[name].keys()=}"
        for port in a[name]:
            assert a[name][port] == b[name][port], f"a[{name}]{port}]={a[name][port]} b[{name}][{port}]={b[name][port]}"
            print(name, port, a[name][port])

def network(filename, top, output):
    library = gdstk.read_gds(filename)
    with measure_time("converting_paths"):
        convert_paths(library)
    with measure_time("filter_layers"):
        filter_layers(library)
    with measure_time("filter_filters"):
        filter_filters(library)
    with measure_time("filter_pads"):
        filter_pads(library) # <- Keep pads that overlap with labels
    with measure_time("custom_flatten"):
        custom_flatten(library) # Why doesn't this work? It's like the library doesn't like references being removed?
    with measure_time("connected_components"):
        before = counts(library, top)
        connected_components(library[top])
        after = counts(library, top)
        # compare_counts(before, after)
    with measure_time("call_graph"):
        els = cell_graph(library[top])
    with open(f"outputs/{output}.txt", "w") as fp:
        for x,y in els:
            print(f"{x} -> {y}", file=fp)

    write_files(library, library[top], "outputs/network")


if __name__ == '__main__':
    if sys.argv[1] == 'warmup':
        network("warmup/04_final.gds", 'adder_demo', sys.argv[1])
    elif sys.argv[1] == 'puzzle':
        network("puzzle.gds", 'puzzle', sys.argv[1])
    else:
        raise ValueError(f"{sys.argv[1]=} not valid target")
