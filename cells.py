import gdstk
import sys
from common import labels_i_care_about, increase_view

def write_files(cell, name):
    filename = f"{name}.svg"
    cell.write_svg(filename)
    # Turns out the svg includes labels by default but
    # I find the original size quite hard to see, so I'll
    # fudge it here
    increase_view(filename)
    lib = gdstk.Library(name)
    lib.add(cell)
    lib.write_gds(f"{name}.gds")

def cells(filename):

    library = gdstk.read_gds(filename)

    for cell in library.cells:
        name = cell.name
        write_files(cell, f"outputs/{name}")


def cells_pads(filename):

    library = gdstk.read_gds(filename)

    for cell in library.cells:

        name = cell.name
        cell.filter([(67, 20)], remove=False, polygons=True, paths=True, labels=False)
        write_files(cell, f"outputs/{name}.li")

def cells_io(filename):

    library = gdstk.read_gds(filename)

    for cell in library.cells:

        name = cell.name
        cell.filter([(67, 20)], remove=False, polygons=True, paths=True, labels=False)

        collected_labels = []
        for label in cell.labels:
            if label.text not in labels_i_care_about:
                cell.remove(label)
            else:
                collected_labels.append(label)

        for polygon in cell.polygons:
            keep = False
            for label in collected_labels:
                origin = label.origin
                print(f"ORIGIN {origin=}")
                # TODO: May need to apply some offset to account for the width of the text relative to wherever the origin is
                # (I'd like it to be in the dead center)
                # TODO: THERE IS A SLIGHT BUG HERE! OVERLAPPING POLYS ON THIS LAYER ARE THE SAME PAD
                # This fails for one of the dfrtp cells on pad D as it is two overlapping polys but
                # only one has the label over it
                if polygon.contain(label.origin):
                    keep = True
            if not keep:
                cell.remove(polygon)

        # assert len(cell.paths) == 0, f"Cell {cell.name} has {len(cell.paths)=} on 67:20"
        # TODO: Do paths as well

        write_files(cell, f"outputs/{name}.li.io")

if __name__ == '__main__':
    if sys.argv[1] == 'warmup':
        cells("warmup/04_final.gds")
        cells_pads("warmup/04_final.gds")
        cells_io("warmup/04_final.gds")
    elif sys.argv[1] == 'puzzle':
        cells("puzzle.gds")
        cells_pads("puzzle.gds")
        cells_io("puzzle.gds")
