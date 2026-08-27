import subprocess as sp
import sys

components = """\
part1
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

def run_and_log(cmd, log):
    print(log, end="")
    ret = sp.run(cmd, capture_output=True, text=True)
    if VERBOSE or ret.returncode or ret.stderr or 'warning' in ret.stderr:
        print()
        print(cmd)
        if ret.stdout:
            print(ret.stdout)
        if ret.returncode or 'FAILED' in ret.stdout or 'warning' in ret.stderr:
            print(ret.stderr)
            sys.exit(ret.returncode)
    else:
        print("ok")

def compile(component):
    print(f"Compiling {component}...", end="")
    sim, comp, tb = f"simulation/{component}_sim.vvp", f"outputs/{component}.v", f"testbench/{component}_tb.v"
    cmd = ["iverilog", "-Wfloating-nets", "-g2012", "-y", "./component", "-o", sim, comp, tb]
    run_and_log(cmd, f"Compiling {component}...")

def run_sim(component):
    print(f"Running {component} simulation ...", end="")
    sim = f"simulation/{component}_sim.vvp"
    cmd = ["vvp", sim]
    run_and_log(cmd, f"Running {component} simulation ...")

def compile_run_part123():
    component = "part123"
    sim, tb = f"simulation/{component}_sim.vvp", f"testbench/{component}_tb.v"
    comps = "outputs/part1.v", "outputs/part2.v", "outputs/part3.v"
    cmd = ["iverilog", "-Wfloating-nets", "-g2012", "-y", "./component", "-o", sim, *comps, tb]
    run_and_log(cmd, f"Compiling {component} ...")
    cmd = ["vvp", sim]
    run_and_log(cmd, f"Running {component} simulation ...")

if __name__ == '__main__':
    compile_run_part123()
    for component in components:
        compile(component)
    for component in components:
        run_sim(component)


