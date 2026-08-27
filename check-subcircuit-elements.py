import glob

def check_subcircuits_dont_share_components():
    obj_to_file = {}
    for file in glob.glob("outputs/*.v"):
        if "puzzle.v" in file: continue
        with open(file) as fp:
            print(f"Checking {file} ...", end="")
            for lineno, line in enumerate(fp):
                args = line.strip().split()
                if len(args) < 3: continue
                if args[2] != "(": continue
                _, name, _ = args
                assert name not in obj_to_file, f"{name=} at {file}:{lineno} is already seen in {obj_to_file[name]}"
                obj_to_file[name] = f"{file}:{lineno}"
            print(f"ok")

if __name__ == '__main__':
    check_subcircuits_dont_share_components()
