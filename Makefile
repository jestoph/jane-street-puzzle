
PYTHON:=./venv/bin/python3

check:
	${PYTHON} -m mypy circuits.py $(find elements -name '*.py')

test:
	${PYTHON} -m pytest circuits.py

logo:
	${PYTHON} logo.py

cells:
	mkdir -p cells
	${PYTHON} cells.py warmup/04_final.gds

stats:
	${PYTHON} stats.py warmup/04_final.gds
	${PYTHON} stats.py puzzle.gds
