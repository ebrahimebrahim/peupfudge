"""Write the Git-derived version label used by the Peupfudge manual."""

import argparse
import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parent.parent
UNKNOWN_VERSION = "unknown (draft)"


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


def version_label() -> str:
    """Return the version at ``HEAD``, marked as a draft when appropriate."""
    tags = git_output("tag", "--points-at", "HEAD", "--sort=-version:refname")
    if tags is None:
        return UNKNOWN_VERSION

    tag = tags.splitlines()[0] if tags else None
    identifier = tag or git_output("rev-parse", "--short", "HEAD")
    status = git_output("status", "--porcelain", "--untracked-files=normal")
    if not identifier or status is None:
        return UNKNOWN_VERSION

    identifier = identifier.removeprefix("v")
    return f"{identifier} (draft)" if status else identifier


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, metavar="OUTPUT")
    return parser.parse_args()


def main() -> None:
    output = parse_args().output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f"{version_label()}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
