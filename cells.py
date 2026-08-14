import gdstk

def increase_view(svgfile):
    """
    My apologies for how stupid this is.
    """

    with open(svgfile) as fp:
        lines = fp.readlines()

    line = lines[1]

    assert '<svg xmlns' in line, f'{line=}'

    """
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="34.6" height="35.2" viewBox="-3.5 -31.2 34.6 35.2">

    to

    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="346" height="352" viewBox="-3.5 -31.2 34.6 35.2">
    """

    h = line.find("height=")
    s = line.find('"', h+1)
    e = line.find('"', s+1)

    print(f"{line[s+1:]=}")

    height = float(line[s+1:e])*10

    line = line[:s+1] + str(height) + line[e:]

    w = line.find("width=")
    s = line.find('"', w+1)
    e = line.find('"', s+1)

    width = float(line[s+1:e])*10

    line = line[:s+1] + str(width) + line[e:]

    lines = [lines[0], line] + lines[2:]

    with open(svgfile, "w") as fp:
        for line in lines:
            print(line, file=fp, end='')


def cells(filename):

    library = gdstk.read_gds(filename)

    for cell in library.cells:
        name = cell.name
        filename = f"outputs/{name}.svg"
        cell.write_svg(filename)
        # Turns out the svg includes labels by default but
        # I find the original size quite hard to see, so I'll
        # fudge it here
        increase_view(filename)
        lib = gdstk.Library(name)
        lib.add(cell)
        lib.write_gds(f"outputs/{name}.gds")


def cells_pads(filename):

    library = gdstk.read_gds(filename)

    for cell in library.cells:

        name = cell.name
        cell.filter([(67, 20)], remove=False, polygons=True, paths=True, labels=False)
        filename = f"outputs/{name}.li.svg"
        cell.write_svg(filename)
        # Turns out the svg includes labels by default but
        # I find the original size quite hard to see, so I'll
        # fudge it here
        increase_view(filename)
        lib = gdstk.Library(name)
        lib.add(cell)
        lib.write_gds(f"outputs/{name}.li.gds")

def cells_io(filename):

    labels_i_care_about = {"A", "A_N", "A1", "A2", "A2", "A3", "B", "B_N", "B1", "B1_N", "C", "CLK", "D", "RESET_B", "X", "Y", "S", "Q"}

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
                if polygon.contain(label.origin):
                    keep = True
            if not keep:
                cell.remove(polygon)

        # assert len(cell.paths) == 0, f"Cell {cell.name} has {len(cell.paths)=} on 67:20"
        # TODO: Do paths as well

        filename = f"outputs/{name}.li.io.svg"
        cell.write_svg(filename)
        # Turns out the svg includes labels by default but
        # I find the original size quite hard to see, so I'll
        # fudge it here
        increase_view(filename)
        lib = gdstk.Library(name)
        lib.add(cell)
        lib.write_gds(f"outputs/{name}.li.io.gds")

if __name__ == '__main__':
    cells("warmup/04_final.gds")
    cells_pads("warmup/04_final.gds")
    cells_io("warmup/04_final.gds")
