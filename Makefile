
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
