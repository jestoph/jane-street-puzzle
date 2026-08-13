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

if __name__ == '__main__':
    cells("warmup/04_final.gds")
