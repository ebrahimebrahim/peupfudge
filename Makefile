DOC := peupfudge
VERSION_FILE := .build/version.txt
PYTHON_ENV := pyproject.toml uv.lock .python-version
TYPST_SOURCES := $(wildcard *.typ)
SVG_ASSETS := assets/svg/char_sheet_example.svg assets/svg/framework_diagram.svg
FONTS := fonts/kalam/Kalam-Regular.ttf \
	fonts/libertinus/LibertinusSerif-Regular.otf \
	fonts/libertinus/LibertinusSerif-Bold.otf

.PHONY: all clean FORCE

all: $(DOC).pdf

$(DOC).pdf: $(TYPST_SOURCES) ndf_table.json ndf_plot.pdf $(SVG_ASSETS) $(FONTS) python/make_version.py $(PYTHON_ENV) FORCE
	uv run --locked python python/make_version.py $(VERSION_FILE)
	typst compile --ignore-system-fonts --font-path fonts --input "version-file=$(VERSION_FILE)" $(DOC).typ $@

FORCE:

ndf_table.json: python/make_ndf_data.py $(PYTHON_ENV)
	uv run --locked python python/make_ndf_data.py --table $@

ndf_plot.pdf: python/make_ndf_data.py $(PYTHON_ENV)
	uv run --locked python python/make_ndf_data.py --plot $@

clean:
	rm -f $(DOC).pdf ndf_table.json ndf_plot.pdf $(VERSION_FILE)
