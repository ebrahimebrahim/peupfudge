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

## Artwork maintenance

Install Inkscape, Fontconfig, and these fonts:

- Roboto Regular and Bold
- Purisa Regular and Bold
- cmr10
- CMU Serif Roman
- DejaVu Sans

Edit the masters in `artwork/editable/*.inkscape.svg`. New masters should use ordinary SVG text. Then regenerate and validate the portable, text-to-path exports with:

```sh
make artwork
```

Commit the edited master and its regenerated portable SVG together.
