import gdstk

def logo():
    library = gdstk.read_gds("warmup/04_final.gds")

    for cell in library.cells:
        for poly in cell.polygons:
            (min_x, min_y), _ = poly.bounding_box()
            if min_x < 50 or min_y < 50:
                cell.remove(poly)

    for cell in library.cells:
        for path in cell.paths:
            cell.remove(path)

    library.write_gds("logo.gds")



if __name__ == '__main__':
    logo()
