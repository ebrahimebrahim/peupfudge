"""Generate the probability data and plot used by the Peupfudge manual."""

import argparse
import json
from functools import cache
from pathlib import Path


@cache
def outcome_count(dice: int, total: int) -> int:
    """Return the number of ways to roll ``total`` on ``dice`` fudge dice."""
    if abs(total) > dice:
        return 0
    if dice == 0:
        return int(total == 0)
    return sum(outcome_count(dice - 1, total - face) for face in (-1, 0, 1))


def probability(dice: int, total: int) -> float:
    """Return the probability of rolling exactly ``total`` on fudge dice."""
    return outcome_count(dice, total) / (3**dice)


def cumulative_probability(dice: int, threshold: int) -> float:
    """Return the probability that a fudge-dice roll meets ``threshold``."""
    successful_outcomes = sum(
        outcome_count(dice, total)
        for total in range(max(-dice, threshold), dice + 1)
    )
    return successful_outcomes / (3**dice)


def write_table(output: Path) -> None:
    thresholds = list(range(-5, 6))
    rows = [
        {
            "dice": dice,
            "label": f"{dice}dF",
            "probabilities": [
                f"{cumulative_probability(dice, threshold):.2f}"
                for threshold in thresholds
            ],
        }
        for dice in range(1, 10)
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps({"thresholds": thresholds, "rows": rows}, indent=2) + "\n",
        encoding="utf-8",
    )


def write_plot(output: Path) -> None:
    import matplotlib.pyplot as plt

    totals = list(range(-9, 10))
    figure, axes = plt.subplots()
    for dice in (2, 4, 6, 9):
        axes.plot(
            totals,
            [probability(dice, total) for total in totals],
            label=f"{dice}dF",
        )
    axes.set_xticks(totals, labels=totals)
    axes.legend()
    axes.set_title("Probabilities when rolling NdF")
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output)
    plt.close(figure)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--table", type=Path, metavar="OUTPUT", help="write table data as JSON"
    )
    parser.add_argument(
        "--plot", type=Path, metavar="OUTPUT", help="write the probability plot as PDF"
    )
    args = parser.parse_args()
    if args.table is None and args.plot is None:
        parser.error("at least one of --table or --plot is required")
    return args


def main() -> None:
    args = parse_args()
    if args.table is not None:
        write_table(args.table)
    if args.plot is not None:
        write_plot(args.plot)


if __name__ == "__main__":
    main()
