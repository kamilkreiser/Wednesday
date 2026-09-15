#!/bin/bash
# a2b_arms.sh — red-proof for tasks/code_patch/a2b_placeholder.sh (2026-09-16 00:3x, KS-887 r1+retry: a modify-in-place
# test hunk with NO new cell was refused as a placeholder twice — the rule read every test section as a new file).
# Arms on REAL artefacts (09-08 rule 12):
#   1 KS-887 r1's real section: `--- a/` existing file, 0 cells added, 0 removed       → QUIET rc 0 (the false FAIL)
#   2 KS-1120 night3's real section: `--- /dev/null`, 4 lines, 0 cells (a true stub)    → FIRES rc 1
#   3 KS-1130 night's real section: `--- /dev/null`, 0 cells (a true stub)               → FIRES rc 1
#   4 KS-1172 night9's real pinned test section: existing file, +1 cell, 0 removed       → QUIET rc 0
#   5 synthetic from arm 1: the same existing-file section with one `-    it(` line added → FIRES rc 1 (cells removed)
#   6 the OLD predicate (0 `+it(` in the section ⇒ stub) on arm 1's section              → fires — the control: the old rule refused the correct hunk
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
P=${P:-$LM/tasks/code_patch/a2b_placeholder.sh}
S1=$LM/runs/2026-09-16_ks887-ornith35b-night/out.md.checker/section_1.diff
S2=$LM/runs/2026-09-15_ks1120-ornith35b-night3/out.md.checker/section_1.diff
S3=$LM/runs/2026-09-15_ks1130-ornith35b-night/out.md.checker/section_1.diff
S4=$(python3 -c "import json; [print(o['file']) for o in json.load(open('$LM/runs/2026-09-15_ks1172-ornith35b-night9/out.md.checker/sections.json')) if 'lifecycleEventRepo.test' in o['path']]" | tail -1)
fail=0
out=$(bash "$P" "$S1"); rc=$?; [ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ARM1 PASS (rc=0 quiet — existing file, assertions rewritten, no cell removed)" || { echo "ARM1 FAIL (rc=$rc: $out)"; fail=1; }
out=$(bash "$P" "$S2"); rc=$?; [ "$rc" -eq 1 ] && echo "ARM2 PASS (rc=1: $out)" || { echo "ARM2 FAIL (rc=$rc: $out)"; fail=1; }
out=$(bash "$P" "$S3"); rc=$?; [ "$rc" -eq 1 ] && echo "ARM3 PASS (rc=1: $out)" || { echo "ARM3 FAIL (rc=$rc: $out)"; fail=1; }
out=$(bash "$P" "$S4"); rc=$?; [ "$rc" -eq 0 ] && [ -z "$out" ] && echo "ARM4 PASS (rc=0 quiet — existing file, one cell added)" || { echo "ARM4 FAIL (rc=$rc: $out)"; fail=1; }
TMP=$(mktemp); { cat "$S1"; printf '%s\n' "-    it('a cell the model deleted', () => {"; } > "$TMP"
out=$(bash "$P" "$TMP"); rc=$?; [ "$rc" -eq 1 ] && echo "ARM5 PASS (rc=1: $out)" || { echo "ARM5 FAIL (rc=$rc: $out)"; fail=1; }
old_n=$(/usr/bin/grep -c -E '^\+\s*(it|test)\(' "$S1"); [ "$old_n" -eq 0 ] && echo "ARM6 PASS (the OLD rule counts 0 '+it(' on arm 1's section and would refuse it — the control)" || { echo "ARM6 FAIL (old rule counts $old_n)"; fail=1; }
exit $fail
