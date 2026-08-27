import subprocess as sp
import sys

components = """\
blob
part9a
part9e
puzzle
part9c
part9e
part9d
part4
part3
part2
part1
output_section

""".split() # TODO: add 'all.v'

"""

blob
output_section
part1
part2
part3
part4
part9a
part9c
part9d
part9e
part9e
puzzle


"""
# adder
# comparitor
# sr1
# sr2
# all


VERBOSE = True

def compile(component):
    print(f"Compiling {component}...", end="")
    sim, comp, tb = f"simulation/{component}_sim.vvp", f"outputs/{component}.v", f"testbench/{component}_tb.v"
    cmd = ["iverilog", "-Wfloating-nets", "-g2012", "-y", "./component", "-o", sim, comp, tb]
    ret = sp.run(cmd, capture_output=True, text=True)
    if ret.returncode or 'warning' in ret.stderr or VERBOSE:
        print()
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.stderr:
            print(ret.stderr)
        if ret.returncode or 'FAILED' in ret.stdout or 'warning' in ret.stderr:
            sys.exit(ret.returncode)
    else:
        print("hello")

def run_sim(component):
    print(f"Running {component} simulation ...", end="")
    sim = f"simulation/{component}_sim.vvp"
    cmd = ["vvp", sim]
    ret = sp.run(cmd, capture_output=True, text=True)
    if ret.returncode or 'FAILED' in ret.stdout or 'warning' in ret.stdout or VERBOSE:
        print()
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.stderr:
            print(ret.stderr)
        if ret.returncode or 'FAILED' in ret.stdout or 'warning' in ret.stderr:
            sys.exit(ret.returncode)
    else:
        print("ok")


if __name__ == '__main__':
    for component in components:
        compile(component)
    for component in components:
        run_sim(component)
