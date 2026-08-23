
PYTHON:=./venv/bin/python3

.PHONY: check logo cells stats network test simplify

check:
	${PYTHON} -m mypy *.py $(find elements -name '*.py')

test:
	${PYTHON} -m pytest circuits.py

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

simulation/mux2.vvp: component/mux2.v testbench/mux2_tb.v
	iverilog -o simulation/mux2_sim.vvp component/mux2.v testbench/mux2_tb.v

waveform/mux2.vcd: simulation/mux2.vvp
	vvp simulation/mux2_sim.vvp

