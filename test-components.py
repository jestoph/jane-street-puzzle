import subprocess as sp
import sys
import glob

import random
comp1 = glob.glob("component/*.v")
random.shuffle(comp1)

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

if len(comp1) != len(components):
    print(f"WARNING: We have components without tests! {set(comp1)^set(components)}")

components = [x.replace("component/","").replace(".v","") for x in components]

def run_and_log(cmd, log):
    print(log, end="")
    ret = sp.run(cmd, capture_output=True, text=True)
    if ret.returncode or ret.stderr or 'warning' in ret.stderr:
        print()
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.returncode or 'FAILED' in ret.stdout or 'warning' in ret.stderr:
            print(ret.stderr)
        sys.exit(ret.returncode)
    else:
        print("ok")

def standalone(component):
    cmd = ["iverilog", "-g2012", "-o", "test.vpp", component]
    run_and_log(cmd, f"Compiling {component} as standalone...")


def compile(component):
    sim, comp, tb = f"simulation/{component}_sim.vvp", f"component/{component}.v", f"testbench/{component}_tb.v"
    cmd = ["iverilog", "-Wfloating-nets", "-g2012", "-y", "./component", "-o", sim, comp, tb]
    run_and_log(cmd, f"Compiling simulation for {component}...")

def run_sim(component):
    sim = f"simulation/{component}_sim.vvp"
    cmd = ["vvp", sim]
    run_and_log(cmd, f"Running {component} simulation ...")

def verilate(component):
    if 'diode' in component: return
    cmd = ["verilator", "--lint-only", "-Wall", component]
    run_and_log(cmd, f"verilating {component}...")


if __name__ == '__main__':
    for component in comp1:
        verilate(component)
        standalone(component)
    for component in components:
        compile(component)
        run_sim(component)
