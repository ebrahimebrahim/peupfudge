DOC=peupfudge
AUXFILES=${DOC}.aux ${DOC}.log texput.log

all: ${DOC}.pdf

${DOC}.pdf: ${DOC}.tex core.tex examples.tex
	pdflatex ${DOC}.tex

.PHONY: clean cleanaux

clean:
	rm -rf ${AUXFILES} ${DOC}.pdf

cleanaux:
	rm -rf ${AUXFILES}
