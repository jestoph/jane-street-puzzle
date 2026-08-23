
PYTHON:=./venv/bin/python3

.PHONY: check logo cells stats network test simplify test-components

check:
	${PYTHON} -m mypy *.py

logo:
	${PYTHON} logo.py

cells:
	${PYTHON} cells.py

stats:
	${PYTHON} stats.py

network:
	${PYTHON} network.py

simplify:
	${PYTHON} simplify.py

#
# Build and test all components
#
test-components:
	python3 test-components.py

test-compiles:
	iverilog -g2012 -y ./component -o outputs/adder.vpp outputs/adder.v
	iverilog -g2012 -y ./component -o outputs/comparitor.vpp outputs/comparitor.v
	iverilog -g2012 -y ./component -o outputs/sr1.vpp outputs/sr1.v
	iverilog -g2012 -y ./component -o outputs/sr2.vpp outputs/sr2.v
	iverilog -g2012 -y ./component -o outputs/all.vpp outputs/all.v

test-testbench-compiles:
	iverilog -g2012 -y ./component -o simulation/comparitor_sim.vpp outputs/comparitor.v testbench/comparitor_tb.v
	iverilog -g2012 -y ./component -o simulation/adder_sim.vpp outputs/adder.v testbench/adder_tb.v
	iverilog -g2012 -y ./component -o simulation/sr1_sim.vpp outputs/sr1.v testbench/sr1_tb.v
	iverilog -g2012 -y ./component -o simulation/sr2_sim.vpp outputs/sr2.v testbench/sr2_tb.v
	iverilog -g2012 -y ./component -o simulation/all_sim.vpp outputs/all.v testbench/all_tb.v
