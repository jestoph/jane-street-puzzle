
PYTHON:=./venv/bin/python3

.PHONY: check logo cells stats network test simplify test-components

check:
	${PYTHON} -m mypy *.py

cells:
	${PYTHON} cells.py warmup

stats:
	${PYTHON} stats.py warmup

network:
	${PYTHON} network.py warmup

simplify:
	${PYTHON} simplify.py warmup

#
# Build and test all components
#
test-components:
	python3 test-components.py

test-subcircuits:
	python3 test-subcircuits.py

clean:
	rm -f outputs/*
