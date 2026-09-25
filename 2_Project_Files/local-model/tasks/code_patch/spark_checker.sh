#!/bin/bash
# spark_checker.sh <input.json> <out.md> <clone-dir> — the code_patch verdict for a SPARK run (2026-09-25).
#
# = tasks/code_patch/checker.sh, UNCHANGED and run first (its output is passed through byte for byte, so its
#   RESULT line and every A-line are what hold_ready.py reads), THEN kit clause 1's ANCHOR CHECK
#   (a2a_anchor.py — spark-kit 04 failure mode 9: `git apply` places a hunk by context search, so a header at a
#   line that does not exist still "applies strict"; checker.sh audits header COUNTS, never the START line).
#   The Ornith path never calls this file, so checker.sh's behaviour for Ornith is untouched.
#
# Prints, after checker.sh's own lines:
#   PASS A2a ANCHOR … | FAIL A2a ANCHOR … | INFO A2a skipped …   (full per-hunk lines in <out.md>.checker/a2a_anchor.out)
#   SPARK RESULT: PASS (checker 7/7 + A2a) | SPARK RESULT: FAIL (…)
# rc 0 only when checker.sh rc 0 AND A2a rc 0. The line prefix `SPARK RESULT:` is deliberately NOT `RESULT:`, so
# night_run.sh / hold_ready.py's `^RESULT:` readers see checker.sh's line only.
# bash 3.2; stderr never discarded; no cd; read verbs only outside the clone.
set -uo pipefail
INPUT="${1:-}"; OUT="${2:-}"; CLONE="${3:-}"
HERE="$(dirname "$0")"
if [ -z "$INPUT" ] || [ -z "$OUT" ] || [ -z "$CLONE" ]; then
  echo "usage: spark_checker.sh <input.json> <out.md> <clone-dir>" >&2; exit 1
fi
bash "$HERE/checker.sh" "$INPUT" "$OUT" "$CLONE"
CRC=$?
REP="$OUT.checker"
if [ -f "$REP/sections.json" ]; then
  python3 "$HERE/a2a_anchor.py" "$INPUT" "$CLONE" "$REP/sections.json" > "$REP/a2a_anchor.out" 2>&1
  ARC=$?
else
  echo "no sections.json — the checker stopped before splitting the diff (A1)" > "$REP/a2a_anchor.out"; ARC=5
fi
SUMLINE="$(/usr/bin/grep -m1 '^SUMMARY' "$REP/a2a_anchor.out" 2>/dev/null)"
if [ "$ARC" -eq 0 ]; then
  echo "PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip ($SUMLINE)"
elif [ "$ARC" -eq 1 ]; then
  echo "FAIL A2a ANCHOR: a hunk's header does NOT name the line its old side sits at — it applies only by git's context search: $(/usr/bin/grep -m2 '^BAD' "$REP/a2a_anchor.out" | tr '\n' ' ' | cut -c1-400) ($SUMLINE)"
elif [ "$ARC" -eq 5 ]; then
  echo "INFO A2a skipped — $(head -1 "$REP/a2a_anchor.out")"
else
  echo "FAIL A2a ANCHOR MEASURE ERROR (rc=$ARC): $(head -2 "$REP/a2a_anchor.out" | tr '\n' ' ')"
fi
if [ "$CRC" -eq 0 ] && [ "$ARC" -eq 0 ]; then
  echo "SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)"; exit 0
fi
echo "SPARK RESULT: FAIL (checker rc=$CRC; A2a rc=$ARC)"
exit 1
