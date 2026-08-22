DOC := peup
DISPLAY_VERSION_FILE := .build/display-version.txt
FILENAME_VERSION_FILE := .build/filename-version.txt
PYTHON_ENV := pyproject.toml uv.lock .python-version
TYPST_SOURCES := $(wildcard *.typ)
SVG_ASSETS := assets/svg/PEUP_logo.svg \
	assets/svg/char_sheet_example.svg \
	assets/svg/framework_diagram.svg
ILLUSTRATIONS := assets/illustrations/bridge.png \
	assets/illustrations/strong_metal.png \
	assets/illustrations/shooting_gremlins.png \
	assets/illustrations/yussra_race_example.jpeg \
	assets/illustrations/arm_wrestle.png
FONTS := fonts/kalam/Kalam-Regular.ttf \
	fonts/libertinus/LibertinusSerif-Regular.otf \
	fonts/libertinus/LibertinusSerif-Bold.otf

.PHONY: all clean

all: $(TYPST_SOURCES) ndf_table.json ndf_plot.pdf $(SVG_ASSETS) $(ILLUSTRATIONS) $(FONTS) python/make_version.py $(PYTHON_ENV)
	uv run --locked python python/make_version.py $(DISPLAY_VERSION_FILE) $(FILENAME_VERSION_FILE)
	typst compile --ignore-system-fonts --font-path fonts --input "version-file=$(DISPLAY_VERSION_FILE)" $(DOC).typ "Peup-$$(cat $(FILENAME_VERSION_FILE)).pdf"

ndf_table.json: python/make_ndf_data.py $(PYTHON_ENV)
	uv run --locked python python/make_ndf_data.py --table $@

ndf_plot.pdf: python/make_ndf_data.py $(PYTHON_ENV)
	uv run --locked python python/make_ndf_data.py --plot $@

clean:
	rm -f Peup.pdf Peup-*.pdf ndf_table.json ndf_plot.pdf $(DISPLAY_VERSION_FILE) $(FILENAME_VERSION_FILE)
