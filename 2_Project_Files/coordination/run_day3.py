"""Day-3 proper run: semver range matcher — hard enough for partial scores."""

from pathlib import Path

from harness import Task, run_search

HERE = Path(__file__).resolve().parent

SPEC = """Implement satisfies(version: str, range_expr: str) -> bool for semver.

Version strings: MAJOR.MINOR.PATCH with optional -PRERELEASE and +BUILD parts
(e.g. '1.2.3', '1.0.0-alpha.1', '1.2.3+build.5').

Precedence (semver 2.0.0):
- Compare major, minor, patch numerically.
- A version WITH a prerelease has lower precedence than the same version
  without one (1.0.0-alpha < 1.0.0).
- Prerelease identifiers (dot-separated) compare left to right: purely numeric
  identifiers compare numerically; identifiers with letters compare ASCII-
  lexically; numeric identifiers always rank LOWER than alphanumeric ones.
  A larger set of identifiers ranks higher when all preceding ones are equal
  (alpha < alpha.1).
- Build metadata (+...) is IGNORED entirely for precedence.

Range syntax:
- Comparators: '1.2.3' or '=1.2.3' (exact), '>', '>=', '<', '<='.
- '^X.Y.Z': >=X.Y.Z and less than the next increment of the leftmost NON-ZERO
  component (^1.2.3 -> <2.0.0, ^0.2.3 -> <0.3.0, ^0.0.3 -> <0.0.4).
- '~X.Y.Z': >=X.Y.Z <X.(Y+1).0.
- Comparators separated by spaces are ANDed; ' || ' separates OR alternatives.

Prerelease gate (npm rule): a version that has a prerelease can only satisfy
an OR-alternative if at least one comparator in that alternative mentions a
prerelease on the SAME [major, minor, patch] tuple. Otherwise it does not
match, even if precedence alone would allow it.
"""

task = Task(
    name="semver_satisfies",
    spec=SPEC,
    test_file=HERE / "day3" / "test_semver.py",
)

if __name__ == "__main__":
    best = run_search(
        task,
        seat_names=["gpt", "claude"],
        budget=12,
        out_dir=HERE / "day3" / "out",
    )
    print(f"\nBest attempt (by {best.seat}, "
          f"{best.verdict.passed}/{best.verdict.total} tests)")
