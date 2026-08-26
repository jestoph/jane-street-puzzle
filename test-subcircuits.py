import subprocess as sp
import sys

components = """\
output_section
puzzle
""".split() # TODO: add 'all.v'

# adder
# comparitor
# sr1
# sr2
# all


VERBOSE = True

def compile(component):
    print(f"Compiling {component}...", end="")
    sim, comp, tb = f"simulation/{component}_sim.vvp", f"outputs/{component}.v", f"testbench/{component}_tb.v"
    cmd = ["iverilog", "-g2012", "-y", "./component", "-o", sim, comp, tb]
    ret = sp.run(cmd, capture_output=True, text=True)
    if ret.returncode or VERBOSE:
        print()
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.stderr:
            print(ret.stderr)
        if ret.returncode:
            sys.exit(ret.returncode)
    else:
        print("hello")

def run_sim(component):
    print(f"Running {component} simulation ...", end="")
    sim = f"simulation/{component}_sim.vvp"
    cmd = ["vvp", sim]
    ret = sp.run(cmd, capture_output=True, text=True)
    if ret.returncode or 'FAILED' in ret.stdout or VERBOSE:
        print()
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.stderr:
            print(ret.stderr)
        if ret.returncode:
            sys.exit(ret.returncode)
    else:
        print("ok")


if __name__ == '__main__':
    for component in components:
        compile(component)
        run_sim(component)
