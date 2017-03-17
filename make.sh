#!/bin/bash
set -e

python/gen_numbers.py
python/gen_trees.py

cd svg
inkscape -D -z --file=bp1.svg --export-eps=bp1.eps
inkscape -D -z --file=bp2.svg --export-eps=bp2.eps
inkscape -D -z --file=bp3.svg --export-eps=bp3.eps
inkscape -D -z --file=bleeding.svg --export-eps=bleeding.eps
inkscape -D -z --file=healing.svg --export-eps=healing.eps
cd ..

pdflatex peupfudge.tex
makeindex peupfudge.idx
pdflatex peupfudge.tex
