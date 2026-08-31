import sys

if __name__ == '__main__':

    el = ""
    replacements = {}
    cache = {}
    with open(sys.argv[1]) as fp:

        for line in fp:
            split = line.strip().split()

            if len(split) == 1 and split[0] == ");" and el:

                with open(f"component/{el}.v") as fp1:
                    printer = ""
                    for _line in fp1:
                        if 'assign' in _line:

                            printer = _line.replace("(", " ( ").replace(")", " ) ").replace("~", " ~ ").replace("|", " | ").replace("&", " & ").replace(";", " ; ")
                            new_printer = [replacements.get(x, x) for x in printer.split()]
                            print(" ".join(new_printer), end="")
                    if not printer:
                        print(f"ERROR: COULD NOT FIND ASSIGN IN component/{el}.v")



                # print(el, replacements)
                el = ""
                replacements = {}
                continue

            if len(split) == 3 and split[2] == "(" and 'df' not in split[1]:
                el = split[0]
                continue

            if not el:
                print(line, end = "")
            else:

                if split[0].startswith("."):
                    pin, wire = split[0].replace(".","").replace(",","").replace(")"," ").replace(",","").split("(")
                    replacements[pin] = wire
