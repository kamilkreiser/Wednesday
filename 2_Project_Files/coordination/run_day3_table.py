"""Day-3c: many interacting formatting rules — first attempts should drop tests."""

from pathlib import Path

from harness import Task, run_search

HERE = Path(__file__).resolve().parent

SPEC = """Implement render_table(headers: list[str], rows: list[list]) -> str
producing an ASCII table:

- Column width = max(len(header), widest formatted cell in that column).
- Cells joined with ' | '; every output line is right-trimmed (no trailing
  whitespace anywhere).
- Line 1: headers, left-aligned/padded. Line 2: a divider of '-' whose length
  is sum(widths) + 3*(ncols-1). Then one line per row.
- Cell formatting and alignment: None -> '—' (em dash), left-aligned.
  Booleans -> 'yes'/'no', left-aligned. Floats -> two decimal places,
  right-aligned. Other ints -> str, right-aligned. Strings left-aligned.
- Empty rows list: just header line + divider.
- Widths are computed from the FORMATTED cell strings.
"""

task = Task(
    name="render_table_weak_seats",
    spec=SPEC,
    test_file=HERE / "day3" / "test_table.py",
)

if __name__ == "__main__":
    best = run_search(
        task,
        seat_names=["gpt-low", "haiku"],
        budget=14,
        out_dir=HERE / "day3" / "out_table",
    )
    print(f"\nBest attempt (by {best.seat}, "
          f"{best.verdict.passed}/{best.verdict.total} tests)")
