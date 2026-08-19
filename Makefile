
PYTHON:=./venv/bin/python3

.PHONY: check logo cells stats network test simplify

check:
	${PYTHON} -m mypy *.py $(find elements -name '*.py')

# test:
# 	${PYTHON} -m pytest circuits.py

logo:
	${PYTHON} logo.py

cells:
	${PYTHON} cells.py

stats:
	${PYTHON} stats.py

network:
	${PYTHON} network.py
#	dot -Tsvg outputs/graph.dot -o outputs/graph.svg
#
test:
	${PYTHON} test.py

simplify:
	${PYTHON} simplify.py > output.txt

