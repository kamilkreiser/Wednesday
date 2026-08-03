"""Verifiers: turn an attempt into a grounded score in [0, 1].

Per the two-schools law (Architecture/2026-08-03_two-schools-analysis.md):
the harness is only as good as its verifier. The test-suite verifier is the
gold standard; rubric/LLM-judge verifiers are deliberately NOT implemented yet.
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

TIMEOUT_S = 120


@dataclass
class Verdict:
    score: float          # fraction of tests passing, in [0, 1]
    passed: int
    total: int
    report: str           # failure detail, fed back into refinement prompts


def extract_python(text: str) -> str:
    """Pull the last ```python fenced block; fall back to the whole text."""
    blocks = re.findall(r"```(?:python)?\n(.*?)```", text, flags=re.DOTALL)
    return blocks[-1].strip() if blocks else text.strip()


def test_suite_verifier(code: str, test_file: Path) -> Verdict:
    """Run an unmodifiable test file against the candidate code.

    The candidate is written as `solution.py` in a temp dir alongside a copy of
    the tests; score = passed / total. Tests import from `solution`.
    """
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        (tmp / "solution.py").write_text(code)
        (tmp / "test_solution.py").write_text(test_file.read_text())
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "-v", "test_solution"],
            cwd=td, capture_output=True, text=True, timeout=TIMEOUT_S,
        )
    out = proc.stderr + proc.stdout
    # unittest -v prints "test_x ... ok" / "... FAIL" / "... ERROR" per test
    passed = len(re.findall(r"\.\.\. ok", out))
    failed = len(re.findall(r"\.\.\. (?:FAIL|ERROR)", out))
    total = passed + failed
    if total == 0:  # collection error, syntax error, crash before any test ran
        return Verdict(score=0.0, passed=0, total=0, report=out[-2000:])
    return Verdict(
        score=passed / total, passed=passed, total=total,
        report=out[-2000:] if failed else "all tests pass",
    )
