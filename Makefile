
PYTHON:=./venv/bin/python3

.PHONY: check logo cells stats network test simplify test-components

check:
	#${PYTHON} -m mypy *.py
	${PYTHON} check-io.py
	${PYTHON} check-subcircuit-elements.py

cells:
	${PYTHON} cells.py puzzle

stats:
	${PYTHON} stats.py puzzle

network:
	${PYTHON} network.py puzzle

simplify:
	${PYTHON} simplify.py puzzle

#
# Build and test all components
#
test-components:
	python3 test-components.py

test-subcircuits:
	python3 test-subcircuits.py

clean:
	rm -f outputs/*

find-unfinished-components:
	grep -r "TODO: provide" component
