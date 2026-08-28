
PYTHON:=./venv/bin/python3

.PHONY: check cells stats network simplify

check:
	# ${PYTHON} -m mypy *.py
	${PYTHON} check-io.py
	${PYTHON} check-unnamed-wires.py
	${PYTHON} test-components.py
	${PYTHON} check-subcircuit-elements.py
	${PYTHON} test-subcircuits.py

cells:
	${PYTHON} cells.py puzzle

stats:
	${PYTHON} stats.py puzzle

network:
	${PYTHON} network.py puzzle

simplify:
	${PYTHON} simplify.py puzzle

clean:
	rm -f outputs/*
	rm -f waveform/*

