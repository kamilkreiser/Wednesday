#!/usr/bin/env python3
"""build_launcher_diff.py — make the PROPOSED launcher diff from the two hunk files. Applies nothing.

Reads Launch_Wednesday.command (read-only) and proposed/launcher_hunk_A.sh / launcher_hunk_B.sh,
inserts A after the rules-card block and B after the INITIAL_PROMPT assignment, and prints a unified
diff (or writes it with --write to proposed/01_launcher_boot_prompt.diff). The diff has no removed
line by construction: both hunks are insertions. Standard library only.

Usage: build_launcher_diff.py [--launcher <path>] [--write] [--patched-out <path>]
"""
import argparse
import difflib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LAUNCHER = os.path.abspath(os.path.join(HERE, "..", "..", "..", "Launch_Wednesday.command"))
ANCHOR_A_PREV = "  rm -f /tmp/wednesday_rules_card.$$\n"   # the line before the rules-card block's closing fi
ANCHOR_B = "  session-end ritual in ./CLAUDE.md.\"\n"       # the last line of INITIAL_PROMPT


def patched_lines(src, hunk_a, hunk_b):
    ia = [i for i, l in enumerate(src) if l == ANCHOR_A_PREV]
    ib = [i for i, l in enumerate(src) if l == ANCHOR_B]
    if len(ia) != 1 or len(ib) != 1:
        raise SystemExit("anchor not found exactly once (A: %d, B: %d): the launcher changed; re-read it and re-anchor"
                         % (len(ia), len(ib)))
    a_at = ia[0] + 2  # after the 'fi' that closes the rules-card block
    if src[ia[0] + 1] != "fi\n":
        raise SystemExit("the line after anchor A is not 'fi': the rules-card block changed shape")
    b_at = ib[0] + 1
    if not a_at < b_at:
        raise SystemExit("anchor order is wrong")
    return src[:a_at] + hunk_a + src[a_at:b_at] + hunk_b + src[b_at:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--launcher", default=DEFAULT_LAUNCHER)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--patched-out")
    a = ap.parse_args()
    src = open(a.launcher, encoding="utf-8").read().splitlines(True)
    ha = open(os.path.join(HERE, "launcher_hunk_A.sh"), encoding="utf-8").read().splitlines(True)
    hb = open(os.path.join(HERE, "launcher_hunk_B.sh"), encoding="utf-8").read().splitlines(True)
    new = patched_lines(src, ha, hb)
    diff = "".join(difflib.unified_diff(src, new, "a/Launch_Wednesday.command", "b/Launch_Wednesday.command", n=3))
    removed = [l for l in diff.splitlines() if l.startswith("-") and not l.startswith("---")]
    if removed:
        raise SystemExit("the diff removes %d line(s); it must be additive only" % len(removed))
    if a.patched_out:
        with open(a.patched_out, "w", encoding="utf-8") as f:
            f.write("".join(new))
    if a.write:
        out = os.path.join(HERE, "01_launcher_boot_prompt.diff")
        with open(out, "w", encoding="utf-8") as f:
            f.write(diff)
        print("%s  +%d lines, -0 lines" % (out, sum(1 for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))))
    else:
        sys.stdout.write(diff)
    return 0


if __name__ == "__main__":
    sys.exit(main())
