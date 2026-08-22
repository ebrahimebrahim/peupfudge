"""Provide display and filename-safe versions derived from Git."""

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parent.parent
UNKNOWN_VERSION = "unknown (draft)"
MYSTERY_VERSION = "MysteryVersionFunForEating"


@dataclass(frozen=True)
class Version:
    """A version identifier and whether the working tree is a draft."""

    identifier: str | None
    draft: bool

    @property
    def label(self) -> str:
        """Return the version text displayed in the manual."""
        if self.identifier is None:
            return UNKNOWN_VERSION
        return f"{self.identifier} (draft)" if self.draft else self.identifier

    @property
    def filename_version(self) -> str:
        """Return a filename-safe version identifier."""
        if self.identifier is None:
            return MYSTERY_VERSION

        identifier = re.sub(r"[^A-Za-z0-9._-]+", "-", self.identifier)
        identifier = identifier.strip("._-")
        if not identifier:
            return MYSTERY_VERSION

        draft = "-draft" if self.draft else ""
        return f"{identifier}{draft}"


def git_output(*args: str) -> str | None:
    """Return stripped Git output, or ``None`` when the command fails."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=REPOSITORY,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def current_version() -> Version:
    """Return the version at ``HEAD`` and whether it is a draft."""
    tags = git_output("tag", "--points-at", "HEAD", "--sort=-version:refname")
    if tags is None:
        return Version(None, draft=True)

    tag = tags.splitlines()[0] if tags else None
    identifier = tag or git_output("rev-parse", "--short", "HEAD")
    status = git_output("status", "--porcelain", "--untracked-files=normal")
    if not identifier or status is None:
        return Version(None, draft=True)

    identifier = identifier.removeprefix("v")
    return Version(identifier or None, draft=bool(status))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "display_output",
        type=Path,
        metavar="DISPLAY_OUTPUT",
        help="output file for the version displayed in the document",
    )
    parser.add_argument(
        "filename_output",
        type=Path,
        metavar="FILENAME_OUTPUT",
        help="output file for the filename-safe version identifier",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    version = current_version()

    args.display_output.parent.mkdir(parents=True, exist_ok=True)
    args.display_output.write_text(f"{version.label}\n", encoding="utf-8")
    args.filename_output.parent.mkdir(parents=True, exist_ok=True)
    args.filename_output.write_text(
        f"{version.filename_version}\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
