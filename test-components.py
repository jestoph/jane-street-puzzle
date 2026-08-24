import subprocess as sp
import sys
import glob

comp1 = glob.glob("component/*.v")

components = """\
component/and4bb.v
component/a31o.v
component/a21o.v
component/a21bo.v
component/xor2.v
component/xnor2.v
component/nand2.v
component/and2.v
component/mux2.v
component/o21bai.v
component/dfrtp.v
component/and3.v
component/nor2.v
component/or2.v
component/a21boi.v
""".split()

assert len(comp1) == len(components), "We have components without tests! {set(comp1)^set(components)}"

components = [x.replace("component/","").replace(".v","") for x in components]

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
