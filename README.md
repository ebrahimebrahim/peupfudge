# Peupfudge

This repository contains the source for the Peupfudge manual.

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Make
- [Typst](https://typst.app/open-source/#download) 0.14.2 or newer

## Build

Run all commands from the repository root. Build `Peup.pdf` with:

```sh
make
```

Builds show the current tag (or short commit hash), with `(draft)` for
uncommitted changes. Direct Typst builds show `Version unknown (draft)` unless
given `--input version-file=PATH`.

Remove generated output with:

```sh
make clean
```

## Python environment

To install the locked Python environment explicitly, run:

```sh
uv sync --locked
```

Update all locked Python dependencies within the declared requirements with:

```sh
uv lock --upgrade
```

## Editing SVGs in Inkscape

Inkscakpe is not needed to build but it can be used to edit the SVGs.

To see the same fonts in Inkscape that are used in the manual build, open **Preferences → Tools → Text → Additional font directories**, add the absolute path to this repository's `fonts` directory, and restart Inkscape.
