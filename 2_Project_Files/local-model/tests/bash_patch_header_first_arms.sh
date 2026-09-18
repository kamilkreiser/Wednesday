#!/bin/bash
# bash_patch_header_first_arms.sh — red-proof for the bash_patch B2 HEADER-FIRST measure (2026-09-18 19:0x; the test_only
# T3 fix of 18:37 carried to B2; IMPROVEMENTS 18:50 OWED row). The planted shape is KS-1153's: `@@ -N,0 +M,k @@` over k '+'
# lines plus ONE trailing context line. Strict `git apply --check` accepts it, drops the context line, and anchors the hunk
# at END OF FILE. Built from the real KS-1261 run (its '+' lines, its test section) with only the script hunk's header and
# leading context rewritten.
#   U1-U4 hdr_mis (cut from the checker under test, not re-implemented): the planted hunk is named; a consistent hunk, a
#         consistent hunk with a trailing EMPTY line (the KS-1163 r2 blank context), and a new-file hunk are silent
#   N1    NEGATIVE CONTROL — the OLD checker (checker.sh, or $OLD) passes B2 "(strict)" and the '+' lines land at EOF
#   P1    the NEW checker takes the named `--recount (MISCOUNTED header` path at B2
#   P2    ... and the applied script has the 3 '+' lines immediately AFTER `fail=0` and BEFORE `env_fail=0` (placement)
#   P3    ... and the run PASSES 7/7 (the brief's fix, correctly placed, is green)
#   R1-R2 the real KS-1261 and KS-1136 item-1 outputs still PASS 7/7 with B2 "(strict)" (consistent headers: no change)
# Usage: bash bash_patch_header_first_arms.sh <scratch clone at 8b9c3f022bee…> [checker under test] [old checker]
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CLONE="${1:?scratch clone at 8b9c3f022bee76b79a47f1b8c5de8ad3ddb4a0ae}"
NEW="${2:-$LM/tasks/bash_patch/checker.sh}"; OLD="${3:-}"
R61=$LM/runs/2026-09-18_ks1261-ornith35b-night; R36=$LM/runs/2026-09-18_ks1136-ornith35b-night2
PROD=Blockchain/Dev/scripts/preflight/preflight.sh
W=$(mktemp -d "${TMPDIR:-/tmp}/bp_hdrfirst.XXXXXX"); fail=0; n=0; ok=0
arm() { n=$((n+1)); if [ "$2" = 1 ]; then ok=$((ok+1)); echo "ARM $1 PASS — $3"; else fail=1; echo "ARM $1 FAIL — $3"; fi; }
# ---- the planted output (only the script hunk changes; '+' lines and the test section are the real run's)
python3 - "$R61/out.md" "$W/planted.md" <<'PY'
import sys
t = open(sys.argv[1], encoding="utf-8").read()
i = t.index('@@ -94,3 +94,6 @@'); j = t.index("\n--- ", i)
plus = [l for l in t[i:j].split("\n") if l.startswith("+")]
assert len(plus) == 3, plus
t = t[:i] + "@@ -94,0 +95,3 @@\n" + "\n".join(plus) + "\n env_fail=0   # KS-991: leg 1 could not RUN (no workspace install) vs a real finding" + t[j:]
open(sys.argv[2], "w", encoding="utf-8").write(t)
PY
# placement measure: 0 when the three '+' lines sit exactly between `fail=0` and `env_fail=0 …`, else prints where they are
placed() { python3 - "$1" "$R61/out.md.checker/section_1.diff" <<'PY'
import sys
res = open(sys.argv[1], encoding="utf-8").read().split("\n")
plus = [l[1:] for l in open(sys.argv[2], encoding="utf-8").read().split("\n") if l.startswith("+") and not l.startswith("+++")]
pos = [i for i in range(len(res) - len(plus) + 1) if res[i:i + len(plus)] == plus]
if len(pos) == 1 and res[pos[0] - 1] == "fail=0" and res[pos[0] + len(plus)].startswith("env_fail=0   # KS-991"):
    print(f"placed :{pos[0]+1}-{pos[0]+len(plus)} after fail=0, before env_fail=0"); sys.exit(0)
print(f"MISPLACED: '+' block at {[p+1 for p in pos]} of {len(res)-1} lines; above={res[pos[0]-1][:40]!r}" if pos else "MISPLACED: block absent"); sys.exit(1)
PY
}
# ---- U: hdr_mis, cut from the checker under test
sed -n '/^hdr_mis() {/,/^}/p' "$NEW" > "$W/hdr_mis.sh"
if [ ! -s "$W/hdr_mis.sh" ]; then arm U0 0 "hdr_mis not found in $NEW"; else
  . "$W/hdr_mis.sh"
  printf -- '--- a/x\n+++ b/x\n@@ -94,0 +95,3 @@\n+a\n+b\n+c\n ctx\n' > "$W/u1.diff"
  printf -- '--- a/x\n+++ b/x\n@@ -1,3 +1,4 @@\n c1\n+a\n c2\n c3\n' > "$W/u2.diff"
  printf -- '--- a/x\n+++ b/x\n@@ -1,3 +1,4 @@\n c1\n+a\n c2\n\n' > "$W/u3.diff"
  printf -- '--- /dev/null\n+++ b/y\n@@ -0,0 +1,2 @@\n+a\n+b\n' > "$W/u4.diff"
  u1="$(hdr_mis "$W/u1.diff")"; arm U1 "$([ -n "$u1" ] && echo 1 || echo 0)" "planted -N,0 + trailing context is NAMED: ${u1:-<silent>}"
  arm U2 "$([ -z "$(hdr_mis "$W/u2.diff")" ] && echo 1 || echo 0)" "a consistent hunk is silent"
  arm U3 "$([ -z "$(hdr_mis "$W/u3.diff")" ] && echo 1 || echo 0)" "a consistent hunk whose last context line is written EMPTY (KS-1163 r2) is silent"
  arm U4 "$([ -z "$(hdr_mis "$W/u4.diff")" ] && echo 1 || echo 0)" "a consistent new-file hunk is silent"
fi
# ---- N1 negative control: the old checker
if [ -n "$OLD" ]; then
  cp "$W/planted.md" "$W/old.md"; bash "$OLD" "$R61/input.json" "$W/old.md" "$CLONE" > "$W/old.out" 2>&1
  pm="$(placed "$W/old.md.checker/after.sh")"; prc=$?
  arm N1 "$( /usr/bin/grep -q '^PASS B2 every section applies at the tip (strict)$' "$W/old.out" && [ "$prc" -ne 0 ] && echo 1 || echo 0)" "OLD checker: $(/usr/bin/grep -m1 -E '^(PASS|FAIL) B2' "$W/old.out" | cut -c1-70) · $pm"
fi
# ---- P: the checker under test on the planted shape
cp "$W/planted.md" "$W/new.md"; bash "$NEW" "$R61/input.json" "$W/new.md" "$CLONE" > "$W/new.out" 2>&1
arm P1 "$( /usr/bin/grep -q '^PASS B2 .*--recount (MISCOUNTED header' "$W/new.out" && echo 1 || echo 0)" "B2: $(/usr/bin/grep -m1 -E '^(PASS|FAIL) B2' "$W/new.out" | cut -c1-150)"
pm="$(placed "$W/new.md.checker/after.sh" 2>&1)"; prc=$?
arm P2 "$([ "$prc" -eq 0 ] && echo 1 || echo 0)" "placement after B5's apply: $pm"
arm P3 "$( /usr/bin/grep -q '^RESULT: PASS (7/7)' "$W/new.out" && echo 1 || echo 0)" "verdict: $(/usr/bin/grep -m1 '^RESULT' "$W/new.out")"
# ---- R: the real held outputs are unchanged (consistent headers stay strict)
for pair in "R1:$R61" "R2:$R36"; do
  a="${pair%%:*}"; r="${pair#*:}"; cp "$r/out.md" "$W/$a.md"
  bash "$NEW" "$r/input.json" "$W/$a.md" "$CLONE" > "$W/$a.out" 2>&1
  arm "$a" "$( /usr/bin/grep -q '^PASS B2 every section applies at the tip (strict)$' "$W/$a.out" && /usr/bin/grep -q '^RESULT: PASS (7/7)' "$W/$a.out" && echo 1 || echo 0)" "$(basename "$r"): $(/usr/bin/grep -m1 -E '^(PASS|FAIL) B2' "$W/$a.out" | cut -c1-70) · $(/usr/bin/grep -m1 '^RESULT' "$W/$a.out")"
done
echo "ARMS $ok/$n (work dir kept, never deleted: $W)"
exit $fail
