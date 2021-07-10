DOC=peupfudge
AUXFILES=${DOC}.aux ${DOC}.log texput.log

all: ${DOC}.pdf

${DOC}.pdf: ${DOC}.tex core.tex examples.tex probability_reference.tex ndf_plot.pdf ndf_table.tex reference_sheet.pdf reference_sheet.tex
	pdflatex ${DOC}.tex

ndf_plot.pdf: python/make_ndf_data.py
	python3 python/make_ndf_data.py

ndf_table.tex: python/make_ndf_data.py
	python3 python/make_ndf_data.py

reference_sheet.pdf: reference_sheet.svg
	inkscape reference_sheet.svg --export-pdf=$@

.PHONY: clean cleanaux

clean:
	rm -rf ${AUXFILES} ${DOC}.pdf ndf_plot.pdf ndf_table.tex reference_sheet.pdf

cleanaux:
	rm -rf ${AUXFILES}
