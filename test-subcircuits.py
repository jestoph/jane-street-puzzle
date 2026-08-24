import subprocess as sp
import sys

components = """\
adder
comparitor
sr1
sr2
all
""".split() # TODO: add 'all.v'

def compile(component):
    print(f"Compiling {component}...", end="")
    sim, comp, tb = f"simulation/{component}_sim.vvp", f"outputs/{component}.v", f"testbench/{component}_tb.v"
    cmd = ["iverilog", "-g2012", "-y", "./component", "-o", sim, comp, tb]
    ret = sp.run(cmd, capture_output=True, text=True)
    if ret.returncode:
        print()
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.stderr:
            print(ret.stderr)
        sys.exit(ret.returncode)
    else:
        print("ok")

def run_sim(component):
    print(f"Running {component} simulation ...", end="")
    sim = f"simulation/{component}_sim.vvp"
    cmd = ["vvp", sim]
    ret = sp.run(cmd, capture_output=True, text=True)
    if ret.returncode or 'FAILED' in ret.stdout:
        print()
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.stderr:
            print(ret.stderr)
        sys.exit(ret.returncode)
    else:
        print("ok")


if __name__ == '__main__':
    for component in components:
        compile(component)
        run_sim(component)
