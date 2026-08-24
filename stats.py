import gdstk
import sys
from common import read_layers, mdtable


def stats(filename, top):

    data = gdstk.gds_info(filename)
    for k in ["num_polygons", "num_paths", "num_references", "num_labels", "unit", "precision"]:
        print(k, data[k])

    layers = read_layers()
    layer_map = {}
    for layer in layers:
        layer_map[( layer['layer'], layer['datatype'] )] = layer

    print("layers and datatypes:")
    md = []
    for (layer, datatype) in sorted(data["layers_and_datatypes"]):
        default = {"layer_name": "unknown", "purpose": "unknown", "layer": str(layer), "datatype": str(datatype), "description": 'unknown'}
        md.append(layer_map.get((str(layer), str(datatype)), default))

    mdtable(md)

    print()
    library = gdstk.read_gds(filename)

    print(f"{len(library.top_level())=}")
    print(f"{len(library.cells)=}")
    print(f"{len(library.top_level()[0].references)=}")
    print()

    ref_counts_by_name = {}
    for ref in library.top_level()[0].references:
        ref_counts_by_name[ref.cell.name] = ref_counts_by_name.get(ref.cell.name, 0) + 1

    cell = library[top]
    cell.flatten()

    md = []
    for cell in sorted(library.cells, key=lambda x: x.name.lower()):
        md.append({
            "cell_name": cell.name,
            "cell_count(refs)": ref_counts_by_name.get(cell.name),
            "cell_labels": len(cell.labels),
            "cell_paths": len(cell.paths),
            "cell_polygons": len(cell.polygons),
            "cell_properties": len(cell.properties),
            "cell_references": len(cell.references),
            "cell_area": f"{cell.area():.2f}",
            "cell_bounding_box": cell.bounding_box(),
        })

    mdtable(md)

    layer_polys(library, top)

def layer_polys(library, top):

    cell = library[top]
    cell.flatten()

    layer_poly_count = {}
    layer_map = {v:k for k,v in {
        "li1" :(67,20),
        "mcon":(67,44),
        "met1":(68,20),
        "via" :(68,44),
        "met2":(69,20),
        "via2":(69,44),
        "met3":(70,20),
    }.items()}

    for cell in library.cells:
        for poly in cell.polygons:
            l = poly.layer, poly.datatype
            layer_poly_count[l] = layer_poly_count.get(l, 0) + 1



    print()
    for layer, name in layer_map.items():
        print(f"{name}:{layer}: {layer_poly_count[layer]}")


if __name__ == '__main__':
    if sys.argv[1] == 'warmup':
        stats("warmup/04_final.gds", top="adder_demo")
    elif sys.argv[1] == 'puzzle':
        stats("puzzle.gds", top="puzzle")
    else:
        raise ValueError(f"{sys.argv[1]=} not valid target")

