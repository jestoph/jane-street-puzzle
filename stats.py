import gdstk

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

def stats(filename):

    data = gdstk.gds_info("warmup/04_final.gds")
    for k in ["num_polygons", "num_paths", "num_references", "num_labels", "unit", "precision"]:
        print(k, data[k])

    print("layers and datatypes:")
    for (layer, datatype) in sorted(data["layers_and_datatypes"]):
        print(f"   {layer=} {datatype=}")

    print()
    library = gdstk.read_gds(filename)

    print(f"{len(library.top_level())=}")
    print(f"{len(library.cells)=}")
    print()

    library['adder_demo'].flatten()

    data = []
    for cell in sorted(library.cells, key=lambda x: x.name.lower()):
        data.append({
            "cell_name": cell.name,
            "cell_labels": len(cell.labels),
            "cell_paths": len(cell.paths),
            "cell_polygons": len(cell.polygons),
            "cell_properties": len(cell.properties),
            "cell_references": len(cell.references),
            "cell_area": f"{cell.area():.2f}",
            "cell_bounding_box": cell.bounding_box(),
        })

    mdtable(data)



if __name__ == '__main__':
    stats("warmup/04_final.gds")

