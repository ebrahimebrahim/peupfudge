DOC := peupfudge
PYTHON_ENV := pyproject.toml uv.lock .python-version
TYPST_SOURCES := peupfudge.typ core.typ examples.typ probability_reference.typ reference_sheet.typ setup_checklist.typ
ARTWORK_STEMS := reference_sheet char_sheet_example xp_allocation_example framework_diagram
ARTWORK := $(addprefix artwork/,$(addsuffix .svg,$(ARTWORK_STEMS)))
EDITABLE_ARTWORK := $(addprefix artwork/editable/,$(addsuffix .inkscape.svg,$(ARTWORK_STEMS)))

.PHONY: all artwork clean

all: $(DOC).pdf

$(DOC).pdf: $(TYPST_SOURCES) ndf_table.json ndf_plot.pdf $(ARTWORK)
	typst compile --ignore-system-fonts $< $@

ndf_table.json: python/make_ndf_data.py $(PYTHON_ENV)
	uv run --locked python python/make_ndf_data.py --table $@

ndf_plot.pdf: python/make_ndf_data.py $(PYTHON_ENV)
	uv run --locked python python/make_ndf_data.py --plot $@

artwork: $(EDITABLE_ARTWORK)
	@command -v inkscape >/dev/null || { echo "make artwork: Inkscape is required" >&2; exit 1; }
	@command -v fc-match >/dev/null || { echo "make artwork: fc-match is required to verify fonts" >&2; exit 1; }
	@actual="$$(fc-match --format='%{family[0]}|%{style[0]}' 'Roboto:style=Regular')"; \
		test "$$actual" = 'Roboto|Regular' || { echo "make artwork: missing Roboto Regular (matched $$actual)" >&2; exit 1; }
	@actual="$$(fc-match --format='%{family[0]}|%{style[0]}' 'Roboto:style=Bold')"; \
		test "$$actual" = 'Roboto|Bold' || { echo "make artwork: missing Roboto Bold (matched $$actual)" >&2; exit 1; }
	@actual="$$(fc-match --format='%{family[0]}|%{style[0]}' 'Purisa:style=Bold')"; \
		test "$$actual" = 'Purisa|Bold' || { echo "make artwork: missing Purisa Bold (matched $$actual)" >&2; exit 1; }
	@actual="$$(fc-match --format='%{family[0]}|%{style[0]}' 'Purisa:style=Regular')"; \
		test "$$actual" = 'Purisa|Regular' || { echo "make artwork: missing Purisa Regular (matched $$actual)" >&2; exit 1; }
	@actual="$$(fc-match --format='%{family[0]}' 'cmr10')"; \
		test "$$actual" = 'cmr10' || { echo "make artwork: missing cmr10 (matched $$actual)" >&2; exit 1; }
	@actual="$$(fc-match --format='%{family[0]}|%{style[0]}' 'CMU Serif:style=Roman')"; \
		test "$$actual" = 'CMU Serif|Roman' || { echo "make artwork: missing CMU Serif Roman (matched $$actual)" >&2; exit 1; }
	@actual="$$(fc-match --format='%{family[0]}' 'DejaVu Sans')"; \
		test "$$actual" = 'DejaVu Sans' || { echo "make artwork: missing DejaVu Sans (matched $$actual)" >&2; exit 1; }
	@set -eu; \
		if grep -En '<([^[:space:]>]+:)?(flowRoot|flowPara|flowSpan)' $(EDITABLE_ARTWORK); then \
			echo "make artwork: editable SVG contains flowed text" >&2; \
			exit 1; \
		fi; \
		temporary="$$(mktemp -d)"; \
		trap 'rm -rf "$$temporary"' EXIT HUP INT TERM; \
		for stem in $(ARTWORK_STEMS); do \
			inkscape "artwork/editable/$$stem.inkscape.svg" \
				--export-plain-svg --export-text-to-path \
				--export-filename="$$temporary/$$stem.svg" >/dev/null; \
			test -s "$$temporary/$$stem.svg"; \
		done; \
		if grep -En '<([^[:space:]>]+:)?(flowRoot|flowPara|flowSpan|text)' "$$temporary"/*.svg; then \
			echo "make artwork: exported SVG contains flowed or live text" >&2; \
			exit 1; \
		fi; \
		mkdir -p artwork; \
		for stem in $(ARTWORK_STEMS); do \
			cp "$$temporary/$$stem.svg" "artwork/$$stem.svg"; \
		done

clean:
	rm -f $(DOC).pdf ndf_table.json ndf_plot.pdf
