# Peupfudge

This repository contains the source for the Peupfudge manual.

## Requirements

Install these host tools before building:

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Make
- Inkscape
- A LaTeX distribution that provides `pdflatex`

Installation steps vary by platform. Ensure `make`, `inkscape`, and `pdflatex` are available on your `PATH`.

On the first build, uv installs Python 3.12 and synchronizes the locked Python dependencies.

## Build

Run all commands from the repository root. Build the manual with:

```sh
make
```

The resulting manual is written to `peupfudge.pdf` in the repository root.

To install the locked Python environment explicitly before building, run:

```sh
uv sync --locked
```

## Maintenance

Remove all generated build output with:

```sh
make clean
```

Remove only LaTeX auxiliary files with:

```sh
make cleanaux
```

To update all locked Python dependencies within the declared requirements, run:

```sh
uv lock --upgrade
```
