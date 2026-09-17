#!/bin/bash
# a4_allreds_arms.sh [NEW_CHECKER] [OLD_CHECKER] — code_patch A4: EVERY declared red cell must red (2026-09-17)
#
# The defect (search 17l, night/briefs/NEXT_SEARCH_2026-09-17l.REPORT.md "Wednesday must read" item 2): A4 passed
# when ANY `## Red cells` entry failed. KS-1123 wrong_emptytwin (R1 fed '' instead of 0, so R1 GREEN under the tamper)
# got RESULT PASS (7/7) on 1 failed / 4 run.
#
# HOW IT TESTS (no vitest, no clone, no seam added to the checker): the A4 DECISION is cut out of the checker file
# itself — summ(), getn(), and every line from `red_total="$(getn "$RED" total)"` down to the A5 banner — and run in a
# bash subshell against a stored red_first.json + input (defect_line). The normal path is not touched: what runs here
# is the checker's own text, byte for byte. The same cut is taken from the OLD checker (the backup) for the controls.
#
# Arms:
#   ARM1  KS-1123 real run (R1+R2 red, 2 failed / 4)                      NEW -> PASS A4
#   ARM2  KS-1123 wrong_emptytwin (R1 green, 1 failed / 4), test_only     NEW -> FAIL naming R1 only, stopped at A4
#   ARM2b the same input, MODE=code_patch                                  NEW -> FAIL says "at the tip"
#   ARM3  the OLD checker on ARM2's input                                  OLD -> PASS A4 (negative control: the defect)
#   ARM3b the OLD checker on ARM1's input                                  OLD -> PASS A4 (the fixture is sane under OLD)
#   ARM4  KS-1205 real run (one declared red, 1 failed / 3)                NEW -> PASS A4
#   ARM5a R1's exact-title cell GREEN + a failed twin "<R1 title> (empty-string twin)"  NEW -> FAIL naming R1; OLD -> PASS
#   ARM5b declared short "KS-1123 R1"/"KS-1123 R2"; the only R1-ish failed cell is titled "KS-1123 R10 - …"
#         (prefix match only)                                              NEW -> FAIL naming "KS-1123 R1"; OLD -> PASS
#   ARM5d two cells carry R1's exact title, one red one green               NEW -> FAIL naming R1; OLD -> PASS
#   ARM5c declared short "KS-1123 R1"/"KS-1123 R2", titles as run (the documented title-substring form, KS-1172)
#                                                                          NEW -> PASS A4 (the substring form still works)
#   ARM6  census: every runs/**/red_first.json whose input declares red_cells — OLD vs NEW A4 verdict; flips listed;
#         holds when every flip is OLD PASS -> NEW FAIL and names a declared cell that is NOT an assertion red in that run
# rc 0 only when every arm holds. Fixtures: tests/fixtures/a4_allreds/ (PROVENANCE.txt). Scratch: $A4_SCRATCH.
set -uo pipefail
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
NEW="${1:-$LM/tasks/code_patch/checker.sh}"
OLD="${2:-$LM/tasks/code_patch/checker.sh.pre-0917-a4allreds}"
FX="$LM/tests/fixtures/a4_allreds"
SP="${A4_SCRATCH:-/private/tmp/claude-501/night/a4fix/arms_$(date +%H%M%S)_$$}"
mkdir -p "$SP"
[ -f "$NEW" ] && [ -f "$OLD" ] || { echo "FATAL: checker missing: NEW=$NEW OLD=$OLD"; exit 2; }
echo "NEW $NEW sha256 $(shasum -a 256 "$NEW" | cut -c1-12)"
echo "OLD $OLD sha256 $(shasum -a 256 "$OLD" | cut -c1-12)"
echo "scratch $SP"
OKN=0; BADN=0
ok()  { echo "  ok   $1"; OKN=$((OKN+1)); }
bad() { echo "  BAD  $1"; BADN=$((BADN+1)); }

# cut <checker> <out.sh> — the checker's own A4 decision text
cut_a4() {
  python3 - "$1" "$2" <<'PYCUT'
import sys
L = open(sys.argv[1], encoding="utf-8").read().split("\n")
def one(pred, what):
    idx = [i for i, l in enumerate(L) if pred(l)]
    if len(idx) != 1: sys.exit(f"CUT FAILED: {what} found {len(idx)} times")
    return idx[0]
s0 = one(lambda l: l.startswith("summ() {"), "summ() {")
s1 = next(i for i in range(s0, len(L)) if L[i] == "}")
g = one(lambda l: l.startswith("getn() {"), "getn() {")
b0 = one(lambda l: l.startswith('red_total="$(getn "$RED" total)"'), "red_total= line")
b1 = one(lambda l: l.startswith("# ----") and "A5 green-after" in l, "A5 banner")
body = ["#!/bin/bash", "set -uo pipefail", 'REP="$1"; INPUT="$2"; MODE="$3"; TEST_REL="src/__tests__/fixture.test.ts"',
        "FAILS=0", 'pass() { echo "PASS $1"; }', 'fail() { echo "FAIL $1"; FAILS=$((FAILS+1)); }']
body += L[s0:s1 + 1] + [L[g]]
body += ['RED="$(summ red_first)"',
         'rc_red="$(python3 -c \'import json,sys; j=json.load(open(sys.argv[1])); print(1 if (j["numFailedTests"] or j["numFailedTestSuites"]) else 0)\' "$REP/red_first.json")"']
body += L[b0:b1]
body += ['echo "CUT-END FAILS=$FAILS"']
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(body) + "\n")
print(f"cut {sys.argv[1]}: summ {s0+1}-{s1+1}, getn {g+1}, A4 decision {b0+1}-{b1}")
PYCUT
}
cut_a4 "$NEW" "$SP/a4_new.sh" || { echo "FATAL: cannot cut NEW"; exit 2; }
cut_a4 "$OLD" "$SP/a4_old.sh" || { echo "FATAL: cannot cut OLD"; exit 2; }

# run_a4 <new|old> <label> <red_first.json> <input.json> [mode] -> sets OUT (path) and RC
run_a4() {
  local which="$1" label="$2" rf="$3" inp="$4" mode="${5:-test_only}"
  local d="$SP/$label.$which"; mkdir -p "$d"
  cp "$rf" "$d/red_first.json"; : > "$d/red_first.out"
  bash "$SP/a4_$which.sh" "$d" "$inp" "$mode" > "$d/decision.out" 2>&1
  RC=$?; OUT="$d/decision.out"
  echo "  [$which $label mode=$mode rc=$RC] $(/usr/bin/grep -E '^(PASS|FAIL) A4|^RESULT' "$OUT" | tr '\n' ' ' | cut -c1-330)"
}
has()  { /usr/bin/grep -q -F -- "$2" "$1"; }

# ---------------------------------------------------------------- synthetic fixtures (derived from the REAL KS-1123 run)
python3 - "$FX" "$SP" <<'PYSYN'
import json, sys, copy
fx, sp = sys.argv[1], sys.argv[2]
real = json.load(open(f"{fx}/ks1123_real/red_first.json"))
inp = json.load(open(f"{fx}/ks1123_real/input.json"))
R1 = "KS-1123 R1 - a status of 0 with a real hash and height is off-chain-only"
def cells(j): return [a for t in j["testResults"] for a in t["assertionResults"]]
def recount(j):
    c = cells(j); j["numTotalTests"] = len(c)
    j["numFailedTests"] = sum(a["status"] == "failed" for a in c); j["numPassedTests"] = sum(a["status"] == "passed" for a in c)
# 5a: R1's exact-title cell passes; a failed twin carries R1's title plus a suffix
a = copy.deepcopy(real); tr = a["testResults"][0]["assertionResults"]
r1 = next(x for x in tr if x["title"] == R1); twin = copy.deepcopy(r1)
r1["status"] = "passed"; r1["failureMessages"] = []
twin["title"] = R1 + " (empty-string twin)"; twin["fullName"] = twin["fullName"] + " (empty-string twin)"
tr.insert(tr.index(r1) + 1, twin); recount(a)
json.dump(a, open(f"{sp}/syn5a_red_first.json", "w"), indent=1, ensure_ascii=False)
# 5b: declared short ids; the R1 cell is retitled R10 (so "KS-1123 R1" matches it only as a prefix)
b = copy.deepcopy(real)
for x in b["testResults"][0]["assertionResults"]:
    if x["title"] == R1:
        x["title"] = x["title"].replace("KS-1123 R1 ", "KS-1123 R10 "); x["fullName"] = x["fullName"].replace("KS-1123 R1 ", "KS-1123 R10 ")
json.dump(b, open(f"{sp}/syn5b_red_first.json", "w"), indent=1, ensure_ascii=False)
short = copy.deepcopy(inp); short["defect_line"]["red_cells"] = ["KS-1123 R1", "KS-1123 R2"]
json.dump(short, open(f"{sp}/syn_short_input.json", "w"), indent=1, ensure_ascii=False)
# 5d: two cells carry R1's exact title (a duplicated it(), or an it.each without a %s); one reds, one stays green
e = copy.deepcopy(real); tr = e["testResults"][0]["assertionResults"]
r1 = next(x for x in tr if x["title"] == R1); dup = copy.deepcopy(r1); dup["status"] = "passed"; dup["failureMessages"] = []
tr.insert(tr.index(r1) + 1, dup); recount(e)
json.dump(e, open(f"{sp}/syn5d_red_first.json", "w"), indent=1, ensure_ascii=False)
print("synthetic fixtures written: syn5a (R1 green + failed twin), syn5b (R1 -> R10), syn_short_input (declared KS-1123 R1 / R2)")
PYSYN
[ -f "$SP/syn5a_red_first.json" ] || { echo "FATAL: synthetic fixtures not written"; exit 2; }
R1="KS-1123 R1 - a status of 0 with a real hash and height is off-chain-only"
R2="KS-1123 R2 - a status of false with a real hash and height is off-chain-only"

echo "=== ARM1 KS-1123 real (R1+R2 red) -> NEW PASS"
run_a4 new arm1 "$FX/ks1123_real/red_first.json" "$FX/ks1123_real/input.json"
if has "$OUT" "PASS A4 RED-FIRST" && ! /usr/bin/grep -q '^FAIL' "$OUT" && [ ! -s "$SP/arm1.new/a4_declared_green.out" ] && [ -f "$SP/arm1.new/a4_declared_green.out" ]; then ok "ARM1 PASS A4, no FAIL, a4_declared_green.out empty"; else bad "ARM1"; fi

echo "=== ARM2 KS-1123 wrong_emptytwin (R1 green) -> NEW FAIL naming R1"
run_a4 new arm2 "$FX/ks1123_emptytwin/red_first.json" "$FX/ks1123_emptytwin/input.json"
if [ "$RC" -ne 0 ] && has "$OUT" "FAIL A4 RED-FIRST: declared red cell(s) did NOT fail by assertion under the tamper — $R1 (1 failed / 4 run)" \
   && ! /usr/bin/grep -q -F "$R2" "$OUT" && has "$OUT" "stopped at A4 (a declared red cell stayed green)" && ! has "$OUT" "PASS A4" \
   && [ "$(cat "$SP/arm2.new/a4_declared_green.out")" = "$R1" ]; then ok "ARM2 FAIL names R1, not R2; rc=$RC; stopped at A4"; else bad "ARM2"; fi

echo "=== ARM2b same input, MODE=code_patch -> NEW FAIL 'at the tip'"
run_a4 new arm2b "$FX/ks1123_emptytwin/red_first.json" "$FX/ks1123_emptytwin/input.json" code_patch
if [ "$RC" -ne 0 ] && has "$OUT" "did NOT fail by assertion at the tip — $R1"; then ok "ARM2b code_patch wording"; else bad "ARM2b"; fi

echo "=== ARM3 OLD checker on ARM2's input -> PASS (negative control)"
run_a4 old arm3 "$FX/ks1123_emptytwin/red_first.json" "$FX/ks1123_emptytwin/input.json"
if [ "$RC" -eq 0 ] && has "$OUT" "PASS A4 RED-FIRST" && ! /usr/bin/grep -q '^FAIL' "$OUT"; then ok "ARM3 OLD PASSes the emptytwin (the defect reproduced)"; else bad "ARM3 OLD did not PASS"; fi
echo "=== ARM3b OLD checker on ARM1's input -> PASS"
run_a4 old arm3b "$FX/ks1123_real/red_first.json" "$FX/ks1123_real/input.json"
if [ "$RC" -eq 0 ] && has "$OUT" "PASS A4 RED-FIRST"; then ok "ARM3b OLD PASS on the real run"; else bad "ARM3b"; fi

echo "=== ARM4 KS-1205 real (single declared red, 1 failed / 3) -> NEW PASS"
run_a4 new arm4 "$FX/ks1205_real/red_first.json" "$FX/ks1205_real/input.json"
if [ "$RC" -eq 0 ] && has "$OUT" "PASS A4 RED-FIRST" && has "$OUT" "(1 failed / 3 run;" && ! /usr/bin/grep -q '^FAIL' "$OUT"; then ok "ARM4 PASS 1/3"; else bad "ARM4"; fi

echo "=== ARM5a exact R1 green + failed superstring twin -> NEW FAIL naming R1; OLD PASS"
run_a4 new arm5a "$SP/syn5a_red_first.json" "$FX/ks1123_real/input.json"
if [ "$RC" -ne 0 ] && has "$OUT" "did NOT fail by assertion under the tamper — $R1 (2 failed / 5 run)" && [ "$(cat "$SP/arm5a.new/a4_declared_green.out")" = "$R1" ]; then ok "ARM5a NEW FAIL, the twin does not stand in for R1"; else bad "ARM5a NEW"; fi
run_a4 old arm5a "$SP/syn5a_red_first.json" "$FX/ks1123_real/input.json"
if [ "$RC" -eq 0 ] && has "$OUT" "PASS A4 RED-FIRST"; then ok "ARM5a OLD PASS (discriminates)"; else bad "ARM5a OLD"; fi

echo "=== ARM5b declared 'KS-1123 R1', only 'KS-1123 R10 - …' failed -> NEW FAIL naming 'KS-1123 R1'; OLD PASS"
run_a4 new arm5b "$SP/syn5b_red_first.json" "$SP/syn_short_input.json"
if [ "$RC" -ne 0 ] && [ "$(cat "$SP/arm5b.new/a4_declared_green.out")" = "KS-1123 R1" ] && has "$OUT" "under the tamper — KS-1123 R1 (2 failed / 4 run)"; then ok "ARM5b NEW FAIL, a prefix match does not count"; else bad "ARM5b NEW"; fi
run_a4 old arm5b "$SP/syn5b_red_first.json" "$SP/syn_short_input.json"
if [ "$RC" -eq 0 ] && has "$OUT" "PASS A4 RED-FIRST"; then ok "ARM5b OLD PASS (discriminates)"; else bad "ARM5b OLD"; fi

echo "=== ARM5d two cells titled exactly R1, one red one green -> NEW FAIL naming R1; OLD PASS"
run_a4 new arm5d "$SP/syn5d_red_first.json" "$FX/ks1123_real/input.json"
if [ "$RC" -ne 0 ] && [ "$(cat "$SP/arm5d.new/a4_declared_green.out")" = "$R1" ] && has "$OUT" "under the tamper — $R1 (2 failed / 5 run)"; then ok "ARM5d NEW FAIL, every cell carrying the declared title must red"; else bad "ARM5d NEW"; fi
run_a4 old arm5d "$SP/syn5d_red_first.json" "$FX/ks1123_real/input.json"
if [ "$RC" -eq 0 ] && has "$OUT" "PASS A4 RED-FIRST"; then ok "ARM5d OLD PASS (discriminates)"; else bad "ARM5d OLD"; fi

echo "=== ARM5c declared 'KS-1123 R1'/'KS-1123 R2', titles as run -> NEW PASS (documented substring form kept)"
run_a4 new arm5c "$FX/ks1123_real/red_first.json" "$SP/syn_short_input.json"
if [ "$RC" -eq 0 ] && has "$OUT" "PASS A4 RED-FIRST"; then ok "ARM5c substring declaration still PASSes"; else bad "ARM5c"; fi

echo "=== ARM6 census over runs/: OLD vs NEW A4 verdict on every stored red_first.json with declared red_cells"
python3 - "$LM/runs" "$SP/census.tsv" <<'PYC'
import json, glob, os, sys
rows = []
for rf in sorted(glob.glob(sys.argv[1] + "/**/red_first.json", recursive=True)):
    ck = os.path.dirname(rf); rd = os.path.dirname(ck)
    inp = os.path.join(rd, "input.json")
    if not os.path.exists(inp): continue
    try:
        d = json.load(open(inp)); rc = ((d.get("defect_line") or {}).get("red_cells")) if isinstance(d, dict) else None
        json.load(open(rf))
    except Exception: continue
    if not rc: continue
    mode = "test_only" if ((d.get("defect_line") or {}).get("tamper")) else "code_patch"
    rows.append((rf, inp, mode))
open(sys.argv[2], "w").write("".join(f"{a}\t{b}\t{c}\n" for a, b, c in rows))
print(f"census inputs: {len(rows)}")
PYC
N=0; FLIPS=0; FLIP_BAD=0
while IFS="$(printf '\t')" read -r rf inp mode; do
  [ -z "$rf" ] && continue
  N=$((N+1)); lab="c$N"
  bash "$SP/a4_old.sh" "$(mkdir -p "$SP/$lab.old" && cp "$rf" "$SP/$lab.old/red_first.json" && : > "$SP/$lab.old/red_first.out" && echo "$SP/$lab.old")" "$inp" "$mode" > "$SP/$lab.old/decision.out" 2>&1
  bash "$SP/a4_new.sh" "$(mkdir -p "$SP/$lab.new" && cp "$rf" "$SP/$lab.new/red_first.json" && : > "$SP/$lab.new/red_first.out" && echo "$SP/$lab.new")" "$inp" "$mode" > "$SP/$lab.new/decision.out" 2>&1
  vo="$(/usr/bin/grep -o -E '^(PASS|FAIL) A4' "$SP/$lab.old/decision.out" | head -1)"; vn="$(/usr/bin/grep -o -E '^(PASS|FAIL) A4' "$SP/$lab.new/decision.out" | head -1)"
  run="$(echo "$rf" | sed "s#^$LM/runs/##")"
  if [ "$vo" = "$vn" ]; then
    echo "  same  [$vo] $run"
  else
    FLIPS=$((FLIPS+1))
    # independent read: a named declared cell must be a cell that is NOT an assertion red in this run (or absent)
    chk="$(python3 - "$rf" "$SP/$lab.new/a4_declared_green.out" <<'PYI'
import json, sys
j = json.load(open(sys.argv[1])); names = [l for l in open(sys.argv[2]).read().split("\n") if l]
st = {}
for t in j["testResults"]:
    for a in t["assertionResults"]:
        m = " ".join(a.get("failureMessages") or [])
        st.setdefault(" ".join(a["title"].split()), []).append(a["status"] == "failed" and ("AssertionError" in m or "expected" in m.lower()))
bad = [n for n in names if n in st and all(st[n])]
print("CONSISTENT" if names and not bad else f"INCONSISTENT names={names} all-red={bad}")
PYI
)"
    echo "  FLIP  [$vo -> $vn] $run :: $(tr '\n' '|' < "$SP/$lab.new/a4_declared_green.out") :: $chk"
    if [ "$vo" != "PASS A4" ] || [ "$vn" != "FAIL A4" ] || [ "$chk" != "CONSISTENT" ]; then FLIP_BAD=$((FLIP_BAD+1)); fi
  fi
done < "$SP/census.tsv"
if [ "$N" -ge 1 ] && [ "$FLIP_BAD" -eq 0 ]; then ok "ARM6 census $N runs, $FLIPS flip(s), every flip OLD PASS -> NEW FAIL on a genuinely green declared cell"; else bad "ARM6 census N=$N flips=$FLIPS bad=$FLIP_BAD"; fi

echo "RESULT: $OKN ok, $BADN bad"
[ "$BADN" -eq 0 ]
