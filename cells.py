import sys
import os
import gdstk

# Easiest way to view info
data = gdstk.gds_info("warmup/04_final.gds")
for k, v in data.items():
    print(k, v)


print()
all_layers = set([x for x, y in data["layers_and_datatypes"]])
print(all_layers)
print(len(all_layers))

# 
# print(library.layer_names)
# x = sorted(library.layers_and_datatypes())
# 
# for a in x: print(a)
# print()
# x = sorted(library.layers_and_texttypes())
# 
# for a in x: print(a)
# print()
# x = sorted(library.layer_names)
# 
# for a in x: print(a)
# 
# 
# 
# Get a list of all cells in the file
# library = gdstk.read_gds("puzzle.gds") # "warmup/04_final.gds")
library = gdstk.read_gds("warmup/04_final.gds")

# for cell in all_cells:
#     print()
#     print("name", cell.name)
#     print("labels", cell.get_labels())
#     print("paths", cell.get_paths())
#     print("polygons", cell.get_polygons())

# 
# help(all_cells[0])
# print(all_cells[0].area(by_spec=True))
# 
# # Find the top-level cells (cells not referenced by others)
# top_cells = library.top_level()
# for cell in top_cells:
#     print(f"Top-level cell name: {cell.name}")
# 
# # Inspect specific geometries inside a cell
# first_cell = all_cells[0]
# print(f"Polygons in '{first_cell.name}': {len(first_cell.polygons)}")
# 

def all_cells():
    cells = library.cells
    help(cells[0])
    print(f"Total cells found: {len(all_cells)}")

    total_polygons = 0
    labels = []
    for i, cell in enumerate(cells):
        # print(len(cell2.polygons), len(cell2.references), len(cell2.dependencies(True)))
        print(f"{i=} {cell.name=} {len(cell.references)=} {len(cell.polygons)=} {len(cell.dependencies(True))=}")
        total_polygons += len(cell.polygons)
        labels.extend(cell.get_labels())

        for label in cell.get_labels():
            label.magnification = 2

        print(f" > {set([label.text for label in cell.get_labels()])}")
        print(f" MAG {set([label.magnification for label in cell.get_labels()])}")
        print(f" LAYER {set([label.layer for label in cell.get_labels()])}")
        print()

    print()
    print(f"{total_polygons=}")

    all_text = set([label.text for label in labels])
    print(all_text)


    with open("output.csv", "w") as fp:
        print('cell_name,label_text', file=fp)
        for cell in all_cells:
            for label in cell.get_labels():
                print(cell.name, ",", label.text, file=fp)
            else:
                print(cell.name, ",", file=fp)


def removeTopReferences(top):
    for i, ref in enumerate(top.references):
        x,y = ref.origin # , cell.polygons.bounding_box()

        print(ref.cell.name, len(ref.cell.polygons))

        keep = True
        for j, polygon in enumerate(ref.cell.polygons):
            box = polygon.bounding_box()
            (min_x, min_y), (max_x, max_y) = box
            print(i, j, ref.cell.name, box)

            if min_x < 50 or min_y < 50:
                keep = False
                top.remove(ref)

    os.unlink("output.trimmed.gds")
    library.write_gds("output.trimmed.gds")

def remove_top_polygons(top):

    #top.flatten()
    for j, polygon in enumerate(top.polygons):
        box = polygon.bounding_box()
        (min_x, min_y), (max_x, max_y) = box
        print(j, top.name, box)

        keep = True
        if min_x < 50 or min_y < 50:
            keep = False
            top.remove(polygon)
        print(j, top.name, box, "->", keep)

    os.unlink("output.trimmed.gds")
    library.write_gds("output.trimmed.gds")

def remove_all_polygons(top):

    #top.flatten()
    for cell in library.cells:
        for j, polygon in enumerate(cell.polygons):
            box = polygon.bounding_box()
            (min_x, min_y), (max_x, max_y) = box
            print(j, cell.name, box)

            keep = True
            if min_x < 50 or min_y < 50:
                keep = False
                cell.remove(polygon)
            print(j, cell.name, box, "->", keep)

    os.unlink("output.trimmed.gds")
    library.write_gds("output.trimmed.gds")


def remove_all_polygons_and_paths(top):

    #top.flatten()
    for cell in library.cells:
        for j, polygon in enumerate(cell.polygons):
            box = polygon.bounding_box()
            (min_x, min_y), (max_x, max_y) = box
            print(j, cell.name, box)

            keep = True
            if min_x < 50 or min_y < 50:
                keep = False
                cell.remove(polygon)
            print(j, cell.name, box, "->", keep)

    for cell in library.cells:
        for j, path in enumerate(cell.paths):

            all_points = []
            for polygon in path.to_polygons():
                all_points.extend(polygon.points)

            ys = [y for _,y in all_points]
            xs = [x for x,_ in all_points]

            if max(ys) - min(ys) < 1:
                # Removes horizontal wires
                cell.remove(path)

            if max(xs) - min(xs) < 1:
                # Removes Vertical wires
                cell.remove(path)
            cell.remove(path)

    for cell in library.cells:
        if len(cell.polygons) > 0:
            print(f"Cell {cell.name} has polygons")
            for poly in cell.polygons:
                print(f" > {poly.layer}")
        if len(cell.paths) > 0:
            print(f"Cell {cell.name} has paths")
            for path in cell.paths:
                print(f" > {path.layers}")
                cell.remove(path)

    os.unlink("output.trimmed.gds")
    library.write_gds("output.trimmed.gds")





def pathBounds():
    pass

def remove_top_paths(top):

    for j, path in enumerate(top.paths):
        all_points = []
        for polygon in path.to_polygons():
            all_points.extend(polygon.points)

        ys = [y for _,y in all_points]
        xs = [x for x,_ in all_points]

        if max(ys) - min(ys) < 1:
            # Removes horizontal wires
            top.remove(path)

        if max(xs) - min(xs) < 1:
            # Removes Vertical wires
            top.remove(path)


    os.unlink("output.trimmed.gds")
    library.write_gds("output.trimmed.gds")

def remove_all_paths(top):
    for cell in library.cells:
        for j, path in enumerate(cell.paths):
            all_points = []
            for polygon in path.to_polygons():
                all_points.extend(polygon.points)

            ys = [y for _,y in all_points]
            xs = [x for x,_ in all_points]

            if max(ys) - min(ys) < 1:
                # Removes horizontal wires
                cell.remove(path)

            if max(xs) - min(xs) < 1:
                # Removes Vertical wires
                cell.remove(path)


    os.unlink("output.trimmed.gds")
    library.write_gds("output.trimmed.gds")

def delete_all_cells(top):

    top.flatten()
    for cell in library.cells:
        if cell != top:
            cell.remove(*cell.get_labels())
            cell.remove(*cell.get_paths())
            cell.remove(*cell.get_polygons())

    os.unlink("output.trimmed.gds")
    library.write_gds("output.trimmed.gds")


def logo():
    top = library.top_level()[0]
    print(top)
    print("BEFORE", top.name, len(top.polygons), len(top.references), len(top.dependencies(True)))

    to_pop = []
    MIN_X, MIN_Y = 8000, 70000

    # # It's on the top right, so I would guess x>8000 and y>70000 should roughly do it.
    new_top_references = []


    # TRIED:
    # * Removing top references -> Fail
    # * Removing top polygons -> Fail
    # * Removing all polygons -> removes everything but the wires?
    # * Removing top paths -> Was able to remove logo but not keep it? Also was using polygon by accident
    # * Removing all paths -> Was able to remove logo but not keep it? Also was using polygon by accident
    # remove_top_paths(top) -> Able to remove horizontal and verical wires

    remove_all_polygons_and_paths(top)

    # # top.flatten()
    # print("AFTER", len(top.polygons), len(top.references), len(top.dependencies(True)))

    # print("BOUNDING", top.polygons[100].bounding_box())
    # for i, polygon in enumerate(top.polygons):
    #     (min_x, min_y), (max_x, max_y) = polygon.bounding_box()
    #     result = min_x > MIN_X and min_y > MIN_Y
    #     print(f"{min_x}, {min_y}, {max_x}, {max_y} -> {result}")
    #     if not result:
    #         to_pop.append(i)
    # for pop in reversed(to_pop):
    #     top.polygons.pop(pop)

    # library.write_gds("output.flat.gds")


if __name__ == '__main__':
    logo()

