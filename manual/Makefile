DOC=peupfudge
AUXFILES=${DOC}.aux ${DOC}.log texput.log

all: ${DOC}.pdf

${DOC}.pdf: ${DOC}.tex core.tex examples.tex ndf_plot.pdf
	pdflatex ${DOC}.tex

ndf_plot.pdf: python/make_ndf_plot.py
	python3 python/make_ndf_plot.py

.PHONY: clean cleanaux

clean:
	rm -rf ${AUXFILES} ${DOC}.pdf ndf_plot.pdf

cleanaux:
	rm -rf ${AUXFILES}
