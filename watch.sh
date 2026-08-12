#!/bin/bash

fswatch -o circuits.py elements/*.py |
while read -r
do
  clear
  ./venv/bin/python3 -m mypy circuits.py $(find elements -name '*.py')
  ./venv/bin/python3 -m pytest circuits.py
done
