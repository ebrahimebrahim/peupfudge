#!/bin/bash
set -e

python/gen_xptable.py
pdflatex peupfudge.tex
