#!/bin/bash
# bash_selftest_arms.sh — red-proof for the bash_patch SELF-TESTING mode (2026-09-26; KS-766 is the first case):
# tasks/bash_patch/build_bash_input.sh (a `## Self-testing … test hunks: N (trailing words)` brief -> input.self_testing)
# and tasks/bash_patch/checker.sh S0-S5 (a ONE-file bash script whose suite runs via `<script> --self-test`).
#
# The patch UNDER TEST is KS-766's golden (night/briefs/KS-766/golden.diff) fed as if it were the model's output, and
# variants of it by one substitution each. Product Blockchain/Dev/scripts/base-image-watch.sh at develop d7cdecf1.
#   B1 the builder on the REAL brief -> rc 0, test_hunks [2], red 12 / green 0, 2 red cells, golden named, and its
#      "prompt source" line names the brief
#   A1 golden                                  -> RESULT: PASS; tip 20 PASS; test hunk alone rc 12; full rc 0, 22 PASS
#   A2 golden with the TEST hunk REMOVED       -> a) real input: FAIL   b) gates relaxed: FAIL at S4 RED-FIRST (no red)
#   A3 a FIX hunk corrupted (the ticket's clamp tamper in E1) so the full apply still exits 12
#                                              -> a) real input: FAIL   b) gates relaxed: FAIL at S5 GREEN-AFTER (rc 12)
#   A4 golden + a second (new) file            -> FAIL at S3 touched set
#   A5 a) E3's header RELOCATED (-628 -> -600) b) an IMPOSSIBLE header (-9628, past EOF) -> FAIL at S2 or S2a
#   N1 NEGATIVE CONTROL: the OLD checker (.pre-0926-*-bashselftest) on the golden + new input does NOT pass
# "gates relaxed" = the input with golden, expected_plus, red_cells and the arm's own must_change site removed, so the
# arm reaches the red/green gate it is about instead of stopping at an earlier (also correct) gate.
# The source checkout is only READ (cat-file / archive / show). Scratch trees are kept, never deleted.
# Usage: bash bash_selftest_arms.sh [checker under test] [old checker]     rc 0 only when every arm holds.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CHK="${1:-$LM/tasks/bash_patch/checker.sh}"
OLD="${2:-$(ls "$LM"/tasks/bash_patch/checker.sh.pre-0926-*-bashselftest 2>&1 | head -1)}"
BUILD=$LM/tasks/bash_patch/build_bash_input.sh
SRC="${NIGHT_SOURCE_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
BRIEF=$LM/night/briefs/KS-766/KS-766.md; GOLD=$LM/night/briefs/KS-766/golden.diff
W="$(mktemp -d "${BASH_SELFTEST_SCRATCH:-${TMPDIR:-/tmp}}/bash_selftest_arms.XXXXXX")"
export BASH_SELFTEST_SCRATCH="$W/scratch"; mkdir -p "$BASH_SELFTEST_SCRATCH"
n=0; ok=0
arm() { n=$((n+1)); if [ "$2" = 1 ]; then ok=$((ok+1)); echo "ARM $1 PASS — $3"; else echo "ARM $1 FAIL — $3"; fi; }
# ---- B1 the builder
IN="$W/input.json"
ALLOW_CONTEXT_AS_ADDITION=1 bash "$BUILD" KS-766 "$IN" "$BRIEF" > "$W/build.out" 2>&1; brc=$?
BCHK="$(python3 - "$IN" "$BRIEF" "$W/build.out" <<'PY'
import json, sys
try: d = json.load(open(sys.argv[1]))
except Exception as e: print(f"no input: {e}"); sys.exit(0)
s = d.get("self_testing") or {}
out = open(sys.argv[3]).read()
ok = (s.get("test_hunks") == [2] and s.get("red_rc") == 12 and s.get("green_rc") == 0 and len(d["defect_line"].get("red_cells", [])) == 2
      and (s.get("golden_diff") or "").endswith("KS-766/golden.diff") and f"prompt source: WEDNESDAY BRIEF {sys.argv[2]}" in out
      and d["product_file"] == "Blockchain/Dev/scripts/base-image-watch.sh" and d["tip"].startswith("d7cdecf1"))
print("OK" if ok else f"BAD {s} / {out[:200]}")
PY
)"
[ "$brc" = 0 ] && [ "$BCHK" = OK ] && arm B1 1 "builder rc 0 on the real brief (heading with trailing words): $(/usr/bin/grep -m1 'prompt source' "$W/build.out" | cut -c1-120)" || arm B1 0 "builder rc=$brc $BCHK $(tail -1 "$W/build.out")"
# relaxed input for arm <name> (see header): expected_plus keeps only the brief lines the arm's own diff adds
relax() {  # <arm name> -> $W/input_relaxed_<arm>.json
  python3 - "$IN" "$W/input_relaxed_$1.json" "$W/$1.md" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
arm_plus = {l[1:].strip() for l in open(sys.argv[3], encoding="utf-8").read().split("\n") if l.startswith("+") and not l.startswith("+++")}
d["self_testing"]["golden_diff"] = None; d["self_testing"]["golden_sha256"] = None
d["defect_line"]["expected_plus"] = [e for e in d["defect_line"]["expected_plus"] if e.strip() in arm_plus]
d["defect_line"]["red_cells"] = []
d["defect_line"]["sites"] = [s for s in d["defect_line"]["sites"] if s["line"] != 631]
json.dump(d, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
PY
}
# ---- outputs
python3 - "$GOLD" "$W" <<'PY'
import os, re, sys
g = open(sys.argv[1], encoding="utf-8").read(); W = sys.argv[2]
hdr_end = g.index("@@ ")
hunks = [h for h in re.split(r"(?m)^(?=@@ )", g[hdr_end:]) if h]; head = g[:hdr_end]
assert len(hunks) == 3, len(hunks)
def put(name, body): open(f"{W}/{name}.md", "w", encoding="utf-8").write("```diff\n" + body + "```\n")
put("A1", g)
put("A2", head + hunks[0] + hunks[2])
e1 = hunks[0]; assert e1.count('+        print("future")\n') == 1
put("A3", head + e1.replace('+        print("future")\n', '+        print(f"{max(age, 0.0):.2f}")\n') + hunks[1] + hunks[2])
put("A4", g + "--- /dev/null\n+++ b/Blockchain/Dev/scripts/zz-selftest-extra.sh\n@@ -0,0 +1,2 @@\n+#!/usr/bin/env bash\n+echo extra\n")
assert g.count("@@ -628,7 +668,24 @@") == 1
put("A5a", g.replace("@@ -628,7 +668,24 @@", "@@ -600,7 +640,24 @@"))
put("A5b", g.replace("@@ -628,7 +668,24 @@", "@@ -9628,7 +9668,24 @@"))
PY
run() { bash "$CHK" "$2" "$W/$1.md" "$SRC" > "$W/$1.$3.out" 2>&1; echo $?; }
res() { /usr/bin/grep -E '^(RESULT|FAIL )' "$W/$1" | head -2 | cut -c1-170 | tr '\n' '·'; }
# A1
rc=$(run A1 "$IN" real)
/usr/bin/grep -q '^RESULT: PASS' "$W/A1.real.out" && /usr/bin/grep -q 'SUMMARY .*tip=rc0/20P/0F red=rc12/.*green=rc0/22P/0F' "$W/A1.real.out" \
  && /usr/bin/grep -q '^PASS S2 every section applies at the tip (strict' "$W/A1.real.out" && /usr/bin/grep -q '^PASS S3g GOLDEN' "$W/A1.real.out" \
  && arm A1 1 "golden PASS (rc=$rc): $(/usr/bin/grep '^SUMMARY' "$W/A1.real.out" | cut -c1-150)" || arm A1 0 "rc=$rc $(res A1.real.out) $(/usr/bin/grep '^SUMMARY' "$W/A1.real.out")"
# A2
relax A2; rc=$(run A2 "$IN" real); rc2=$(run A2 "$W/input_relaxed_A2.json" relaxed)
[ "$rc" = 1 ] && /usr/bin/grep -q '^RESULT: FAIL' "$W/A2.real.out" && arm A2a 1 "test hunk removed, real input -> FAIL (rc=$rc): $(res A2.real.out)" || arm A2a 0 "rc=$rc $(res A2.real.out)"
[ "$rc2" = 1 ] && /usr/bin/grep -q '^FAIL S4 RED-FIRST: the test hunk(s) alone are NOT red' "$W/A2.relaxed.out" && arm A2b 1 "test hunk removed, gates relaxed -> FAIL at S4 (rc=$rc2): $(res A2.relaxed.out)" || arm A2b 0 "rc=$rc2 $(res A2.relaxed.out)"
# A3
relax A3; rc=$(run A3 "$IN" real); rc2=$(run A3 "$W/input_relaxed_A3.json" relaxed)
[ "$rc" = 1 ] && /usr/bin/grep -q '^RESULT: FAIL' "$W/A3.real.out" && arm A3a 1 "clamp tamper in the fix, real input -> FAIL (rc=$rc): $(res A3.real.out)" || arm A3a 0 "rc=$rc $(res A3.real.out)"
[ "$rc2" = 1 ] && /usr/bin/grep -q '^PASS S4 RED-FIRST' "$W/A3.relaxed.out" && /usr/bin/grep -q '^FAIL S5 GREEN-AFTER: rc=12' "$W/A3.relaxed.out" && arm A3b 1 "clamp tamper, gates relaxed -> red ok, FAIL at S5 (rc=$rc2): $(res A3.relaxed.out)" || arm A3b 0 "rc=$rc2 $(res A3.relaxed.out)"
# A4
rc=$(run A4 "$IN" real)
[ "$rc" = 1 ] && /usr/bin/grep -q '^FAIL S3 touched-file set' "$W/A4.real.out" && arm A4 1 "second file -> FAIL at S3 (rc=$rc): $(res A4.real.out)" || arm A4 0 "rc=$rc $(res A4.real.out)"
# A5
for a in A5a A5b; do rc=$(run $a "$IN" real)
  [ "$rc" = 1 ] && /usr/bin/grep -q -E '^FAIL S2a? ' "$W/$a.real.out" && arm $a 1 "bad header -> FAIL at S2/S2a (rc=$rc): $(res $a.real.out)" || arm $a 0 "rc=$rc $(res $a.real.out)"; done
# N1 negative control: the OLD checker cannot judge a self-testing input
# (run against an EMPTY scratch repo, never the source checkout: the old checker's default path quarantines/resets its clone)
if [ -f "$OLD" ]; then mkdir -p "$W/emptyclone"; git -C "$W/emptyclone" init -q > "$W/emptyclone.init.out" 2>&1
  bash "$OLD" "$IN" "$W/A1.md" "$W/emptyclone" > "$W/N1.out" 2>&1; rc=$?
  [ "$rc" != 0 ] && ! /usr/bin/grep -q '^RESULT: PASS' "$W/N1.out" && arm N1 1 "OLD checker on the golden does not pass (rc=$rc): $(res N1.out)" || arm N1 0 "OLD checker passed?! rc=$rc"
else arm N1 0 "old checker not found: $OLD"; fi
echo "ARMS $ok/$n (work dir kept, never deleted: $W)"
[ "$ok" -eq "$n" ]
