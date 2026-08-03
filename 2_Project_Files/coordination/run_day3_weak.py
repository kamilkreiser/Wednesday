"""Day-3b: the actual Sakana thesis test — WEAK seats + search on the same
semver task that GPT-5 one-shots. Question: does the tree climb to 23/23
through refinement and seat selection?"""

from pathlib import Path

from harness import Task, run_search
from run_day3 import SPEC

HERE = Path(__file__).resolve().parent

task = Task(
    name="semver_satisfies_weak_seats",
    spec=SPEC,
    test_file=HERE / "day3" / "test_semver.py",
)

if __name__ == "__main__":
    best = run_search(
        task,
        seat_names=["gpt-low", "haiku"],
        budget=14,
        out_dir=HERE / "day3" / "out_weak",
    )
    print(f"\nBest attempt (by {best.seat}, "
          f"{best.verdict.passed}/{best.verdict.total} tests)")
