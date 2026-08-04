# Peupfudge

This repository contains the source for the Peupfudge manual.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Make
- [Typst](https://typst.app/open-source/#download) 0.14.2 or newer

On the first build, uv installs Python 3.12 and synchronizes the locked Python dependencies.

## Build

Run all commands from the repository root. Build `peupfudge.pdf` with:

```sh
make
```

Builds show the current tag (or short commit hash), with `(draft)` for
uncommitted changes. Direct Typst builds show `Version unknown (draft)` unless
given `--input version-file=PATH`.

To install the locked Python environment explicitly, run:

```sh
uv sync --locked
```

Remove generated output with:

```sh
make clean
```

Update all locked Python dependencies within the declared requirements with:

```sh
uv lock --upgrade
```

## Figures and artwork

The reference sheet and XP allocation example are written in Typst. Shared figure components are defined in `figures.typ`.

The framework diagram and character-sheet example are the live-text SVGs in `artwork/`, embedded directly in the manual. Their printed text uses Libertinus Serif, and the handwritten entries use the bundled Kalam Regular font. The font license and provenance are recorded under `fonts/kalam/`.
