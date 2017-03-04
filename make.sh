#!/bin/bash
set -e

python/gen_xptable.py
python/gen_trees.py
pdflatex peupfudge.tex
makeindex peupfudge.idx
pdflatex peupfudge.tex
