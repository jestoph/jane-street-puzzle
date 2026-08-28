import subprocess as sp
import sys
import glob


components = """\
blob
output_section
puzzle
""".split() + list([x.split("/")[1].replace("_tb.v","") for x in glob.glob("testbench/part*.v")])

# # This is to allow me to only do a few.
# components = """\
# part9b
# """.split() # TODO: add 'all.v'


# adder
# comparitor
# sr1
# sr2
# all


VERBOSE = True

def run_and_log(cmd, log):
    print(log, end="", flush=True)
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
    sim, tb = f"simulation/{component}_sim.vvp", f"testbench/{component}_tb.v"
    cmd = ["iverilog", "-Wfloating-nets", "-g2012", "-y", "./component", "-y", "./outputs", "-o", sim, tb]
    run_and_log(cmd, f"Compiling {component}...")

def run_sim(component):
    sim = f"simulation/{component}_sim.vvp"
    cmd = ["vvp", sim]
    run_and_log(cmd, f"Running {component} simulation ...")

def verilate(component):
    comp, tb = f"outputs/{component}.v", f"testbench/{component}_tb.v"

    cmd = ["verilator", "--lint-only", "-Wall",
           "-Wno-TIMESCALEMOD", "-Wno-UNUSEDSIGNAL", "-Wno-EOFNEWLINE", # These are just time wasters
           "-y", "./component", "-y", "./outputs", tb]
    run_and_log(cmd, f"verilating {component}...")

if __name__ == '__main__':
    for component in components:
        verilate(component)
    for component in components:
        compile(component)
    for component in components:
        run_sim(component)

