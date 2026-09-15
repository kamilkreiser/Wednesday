#!/bin/bash
# d6_arms.sh — red-proof for tasks/doc_patch/d6_ranges.py (2026-09-15, IMPROVEMENTS row 92). Synthetic before/after so the
# arms do not depend on a run dir: a 12-line file with two `## ` sections; sections given 0-based half-open.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; PY="$HERE/../tasks/doc_patch/d6_ranges.py"
S="$(mktemp -d /private/tmp/claude-501/d6_arms.XXXXXX)"
printf '%s\n' "# Title" "intro" "## A" "a1" "a2" "a3" "## B" "b1" "b2" "b3" "b4" > "$S/before.md"
printf '%s\n' "# Title" "intro" "## A" "a1" "a2 CHANGED" "a3" "## B" "b1" "b2" "b3" "b4 CHANGED" > "$S/after_in.md"        # both edits inside A (2-6) and B (6-11); B's last line = EOF
printf '%s\n' "# Title" "intro CHANGED" "## A" "a1" "a2" "a3" "## B" "b1" "b2" "b3" "b4" > "$S/after_out.md"                # the edit is in the preamble
printf '%s\n' "# Title" "intro" "## A" "a1" "a2" "a3" "## B" "b1" "b2" "b3" "b4" "b5 INSERTED" > "$S/after_append.md"       # an insertion at EOF, inside B
pass=0; fail=0
run() { local name="$1" after="$2" want="$3"; python3 "$PY" "$S/before.md" "$after" "2-6,6-11" > "$S/out" 2>&1; rc=$?; if [ "$rc" -eq "$want" ]; then echo "PASS $name (rc=$rc)"; pass=$((pass+1)); else echo "FAIL $name (rc=$rc, wanted $want): $(cat "$S/out" | tr '\n' ' ')"; fail=$((fail+1)); fi; }
run "arm1 edits inside both sections incl. the LAST line of the last section" "$S/after_in.md" 0
run "arm2 an edit in the preamble is OUTSIDE" "$S/after_out.md" 1
run "arm3 an insertion at EOF inside the last section" "$S/after_append.md" 0
echo "d6_arms: $pass passed, $fail failed"; [ "$fail" -eq 0 ]
