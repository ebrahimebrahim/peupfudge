#!/bin/bash
set -e

python/gen_numbers.py
python/gen_trees.py

inkscape -D -z --file=svg/bp1.svg --export-pdf=bp1.pdf --export-latex
inkscape -D -z --file=svg/bp2.svg --export-pdf=bp2.pdf --export-latex
inkscape -D -z --file=svg/bp3.svg --export-pdf=bp3.pdf --export-latex
inkscape -D -z --file=svg/tb.svg  --export-pdf=tb.pdf  --export-latex

pdflatex peupfudge.tex
makeindex peupfudge.idx
pdflatex peupfudge.tex
