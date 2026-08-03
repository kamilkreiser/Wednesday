"""Smoke run: 2 seats (gpt, claude), small budget, real verifier."""

from pathlib import Path

from harness import Task, run_search

HERE = Path(__file__).resolve().parent

task = Task(
    name="parse_duration",
    spec=(
        "Implement parse_duration(s: str) -> int converting duration strings to "
        "total seconds. Units: d (days), h (hours), m (minutes), s (seconds). "
        "Components must appear in d,h,m,s order, each at most once, each a "
        "non-negative integer with a unit letter, no separators or whitespace. "
        "Examples: '2h' -> 7200, '1h30m' -> 5400, '1d2h3m4s' -> 93784, '0s' -> 0. "
        "Anything else (empty string, unknown units, bare numbers, wrong order, "
        "duplicates, whitespace, negatives) raises ValueError."
    ),
    test_file=HERE / "smoke" / "test_duration.py",
)

if __name__ == "__main__":
    best = run_search(
        task,
        seat_names=["gpt", "claude"],
        budget=6,
        out_dir=HERE / "smoke" / "out",
    )
    print(f"\nBest attempt (by {best.seat}, "
          f"{best.verdict.passed}/{best.verdict.total} tests):\n")
    print(best.code)
