DOC=peupfudge
AUXFILES=${DOC}.aux ${DOC}.log texput.log

all: ${DOC}.pdf

${DOC}.pdf: ${DOC}.tex core.tex examples.tex probability_reference.tex ndf_plot.pdf ndf_table.tex reference_sheet.pdf reference_sheet.tex char_sheet_example.pdf xp_allocation_example.pdf framework_diagram.pdf
	pdflatex ${DOC}.tex
	pdflatex ${DOC}.tex # run a second time to pick up references

ndf_plot.pdf: python/make_ndf_data.py
	python3 python/make_ndf_data.py

ndf_table.tex: python/make_ndf_data.py
	python3 python/make_ndf_data.py

reference_sheet.pdf: reference_sheet.svg
	inkscape reference_sheet.svg --export-pdf=$@

char_sheet_example.pdf: char_sheet_example.svg
	inkscape char_sheet_example.svg --export-pdf=$@

xp_allocation_example.pdf: xp_allocation_example.svg
	inkscape xp_allocation_example.svg --export-pdf=$@

framework_diagram.pdf: framework_diagram.svg
	inkscape framework_diagram.svg --export-pdf=$@

.PHONY: clean cleanaux

clean:
	rm -rf ${AUXFILES} ${DOC}.pdf ndf_plot.pdf ndf_table.tex reference_sheet.pdf char_sheet_example.pdf xp_allocation_example.pdf framework_diagram.pdf

cleanaux:
	rm -rf ${AUXFILES}
