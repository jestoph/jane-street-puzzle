import subprocess as sp
import sys

components = """\
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

for component in components:
    sim, comp, tb = f"simulation/{component}_sim.vvp", f"component/{component}.v", f"testbench/{component}_tb.v"
    cmd = ["iverilog", "-g2012", "-o", sim, comp, tb]
    ret = sp.run(cmd, capture_output=True, text=True)
    if ret.returncode:
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.stderr:
            print(ret.stderr)
        sys.exit(ret.returncode)
    cmd = ["vvp", sim]
    ret = sp.run(cmd, capture_output=True, text=True)
    if ret.returncode or 'FAILED' in ret.stdout:
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.stderr:
            print(ret.stderr)
        sys.exit(ret.returncode)

