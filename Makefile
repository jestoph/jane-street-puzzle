
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
	iverilog -g2012 -y ./component -o test.vpp outputs/adder.v
	iverilog -g2012 -y ./component -o test.vpp outputs/comparitor.v
	iverilog -g2012 -y ./component -o test.vpp outputs/sr1.v
	iverilog -g2012 -y ./component -o test.vpp outputs/sr2.v

test-testbench:
	iverilog -g2012 -y ./component -o test.vpp outputs/comparitor.v testbench/comparitor_tb.v
	iverilog -g2012 -y ./component -o test.vpp outputs/adder.v testbench/adder_tb.v
	iverilog -g2012 -y ./component -o test.vpp outputs/sr1.v testbench/sr1_tb.v
	iverilog -g2012 -y ./component -o test.vpp outputs/sr2.v testbench/sr2_tb.v
