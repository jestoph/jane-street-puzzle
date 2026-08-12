import gdstk

def cells(filename):

    library = gdstk.read_gds(filename)

    for cell in library.cells:
        name = cell.name
        cell.write_svg(f"outputs/{name}.svg")
        lib = gdstk.Library(name)
        lib.add(cell)
        lib.write_gds(f"outputs/{name}.gds")

def cells_with_visible_labels(filename):

    # TODO
    pass

if __name__ == '__main__':
    cells("warmup/04_final.gds")
    cells_with_visible_lables("warmup/04_final.gds")

