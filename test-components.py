import subprocess as sp
import sys

components = """\
dfrtp
a21bo
a21boi
a21o
a31o
and2
and3
and4bb
mux2
nand2
nor2
o21bai
or2
xor2
xnor2
""".split()

def compile(component):
    print(f"Compiling {component}...", end="")
    sim, comp, tb = f"simulation/{component}_sim.vvp", f"component/{component}.v", f"testbench/{component}_tb.v"
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
