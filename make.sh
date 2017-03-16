#!/bin/bash
set -e

python/gen_numbers.py
python/gen_trees.py
pdflatex peupfudge.tex
makeindex peupfudge.idx
pdflatex peupfudge.tex
