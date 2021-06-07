DOC=peupfudge
AUXFILES=${DOC}.aux ${DOC}.log texput.log

all: ${DOC}.pdf

${DOC}.pdf: ${DOC}.tex core.tex examples.tex probability_reference.tex ndf_plot.pdf ndf_table.tex
	pdflatex ${DOC}.tex

ndf_plot.pdf: python/make_ndf_data.py
	python3 python/make_ndf_data.py

ndf_table.tex: python/make_ndf_data.py
	python3 python/make_ndf_data.py

.PHONY: clean cleanaux

clean:
	rm -rf ${AUXFILES} ${DOC}.pdf ndf_plot.pdf ndf_table.tex

cleanaux:
	rm -rf ${AUXFILES}
