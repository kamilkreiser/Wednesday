#!/bin/bash
# code_patch_a4_assertion_arms.sh [NEW_CHECKER] [OLD_CHECKER] — code_patch A4: a red is an ASSERTION only by the
# test_only tier's predicate (2026-09-18, A4-ASSERT)
#
# The defect (found by the test_only tier's builder, ARM8, 2026-09-18): code_patch A4 classed a failure as an assertion
# when its message contained the substring "expected" (any case). `SyntaxError: Unexpected end of JSON input` and every
# `Unexpected token …` load error contain it, so a 🔴 cell that never reached its assertion passed A4 as red-first; and
# the non-assertion list only caught messages naming Reference/Type/Syntax/RangeError, so "Error: Cannot find module …"
# slipped through too. The fix reuses tasks/test_only/checker.sh's predicate verbatim:
#   ("AssertionError" in msgs) or bool(re.search(r"\bexpect\(", msgs))
#
# HOW IT TESTS (same method as a4_allreds_arms.sh — no vitest, no clone, no seam): the A4 DECISION is cut out of the
# checker file itself (summ(), getn(), `red_total=` .. the A5 banner, which contains the PY4 classifier) and run against
# a stored red_first.json + input.json. OLD = the backup, for the negative controls.
#
#   ARM0  drift guard: the predicate text in NEW code_patch == the one in tasks/test_only/checker.sh (byte for byte)
#   ARM1  REAL vitest assertion red (KS-1258 run, AssertionError: expected …)          NEW -> PASS A4 (ASSERTION)
#   ARM2  REAL jest assertion red (KS-1229 night6, expect(received).toEqual(expected))   NEW -> PASS A4 (ASSERTION)
#   ARM3a the KS-1258 🔴 cell failing `SyntaxError: Unexpected end of JSON input`         NEW -> FAIL A4 ; OLD -> PASS (control)
#   ARM3b the same with `SyntaxError: Unexpected token 'export'` (an import/parse error) NEW -> FAIL A4 ; OLD -> PASS (control)
#   ARM3c the same with `SyntaxError: Unexpected token '<', "<html>" is not valid JSON`  NEW -> FAIL A4 ; OLD -> PASS (control)
#   ARM3d the jest DECLARED red cell (no 🔴) failing `Unexpected end of JSON input`       NEW -> FAIL A4 ; OLD -> PASS (control)
#   ARM4a 🔴 cell failing `TypeError: Cannot read properties of undefined`                NEW -> FAIL A4 (not an assertion)
#   ARM4b 🔴 cell failing `Error: Cannot find module './no-such-module-ks'`               NEW -> FAIL A4 (OLD also FAILs here,
#         only because the brief DECLARES that cell and the declared-green read had no "expected" to match)
#   ARM4e the same with the brief's red_cells removed (an undeclared 🔴 red)             NEW -> FAIL A4 ; OLD -> PASS (control:
#         OLD's non-assertion list only knew Reference/Type/Syntax/RangeError)
#   ARM4c REAL jest TS6133 "Test suite failed to run" (0 tests run)                       NEW -> FAIL A4 (did not run)
#   ARM4d the vitest assertion file + a second file that failed to LOAD (no cells)        NEW -> FAIL A4 naming "(file)"
#   ARM5  mix: the real 🔴 assertion red + a second 🔴 cell failing Unexpected end of JSON NEW -> FAIL A4 ; OLD -> PASS (control)
#   ARM6  census over every runs/**/red_first.json with an input.json: OLD vs NEW A4 verdict; holds when every flip is
#         OLD PASS -> NEW FAIL and an INDEPENDENT read finds a failed cell (or load-failed file) that is not an assertion
# Each arm prints `ARMx rc=<0|1>` on its own line (0 = the arm holds). rc 0 only when every arm holds.
set -uo pipefail
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
NEW="${1:-$LM/tasks/code_patch/checker.sh}"
OLD="${2:-$(ls -t "$LM"/tasks/code_patch/checker.sh.pre-*-a4assert 2>/dev/null | head -1)}"
TO="$LM/tasks/test_only/checker.sh"
FX="$LM/tests/fixtures/a4_assertion"
SP="${A4A_SCRATCH:-/private/tmp/claude-501/night/a4assert/arms_$(date +%H%M%S)_$$}"
mkdir -p "$SP"
[ -f "$NEW" ] && [ -n "$OLD" ] && [ -f "$OLD" ] || { echo "FATAL: checker missing: NEW=$NEW OLD=$OLD"; exit 2; }
echo "NEW $NEW sha256 $(shasum -a 256 "$NEW" | cut -c1-12)"
echo "OLD $OLD sha256 $(shasum -a 256 "$OLD" | cut -c1-12)"
echo "scratch $SP"
OKN=0; BADN=0
arm() { # arm <name> <0|1> <text>
  echo "$1 rc=$2"
  if [ "$2" -eq 0 ]; then echo "  ok   $3"; OKN=$((OKN+1)); else echo "  BAD  $3"; BADN=$((BADN+1)); fi
}

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
         'rc_red="$(python3 -c \'import json,sys; j=json.load(open(sys.argv[1])); print(1 if (j.get("numFailedTests") or j.get("numFailedTestSuites")) else 0)\' "$REP/red_first.json")"']
body += L[b0:b1]
body += ['echo "CUT-END FAILS=$FAILS"']
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(body) + "\n")
print(f"cut {sys.argv[1]}: summ {s0+1}-{s1+1}, getn {g+1}, A4 decision {b0+1}-{b1}")
PYCUT
}
cut_a4 "$NEW" "$SP/a4_new.sh" || { echo "FATAL: cannot cut NEW"; exit 2; }
cut_a4 "$OLD" "$SP/a4_old.sh" || { echo "FATAL: cannot cut OLD"; exit 2; }

# run_a4 <new|old> <label> <red_first.json> <input.json> -> OUT, V ("PASS A4"/"FAIL A4"/"")
run_a4() {
  local which="$1" label="$2" rf="$3" inp="$4" mode
  mode="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print("test_only" if ((d.get("defect_line") or {}).get("tamper")) else "code_patch")' "$inp" 2>/dev/null || echo code_patch)"
  local d="$SP/$label.$which"; mkdir -p "$d"
  cp "$rf" "$d/red_first.json"; : > "$d/red_first.out"
  bash "$SP/a4_$which.sh" "$d" "$inp" "$mode" > "$d/decision.out" 2>&1
  OUT="$d/decision.out"; V="$(/usr/bin/grep -o -E '^(PASS|FAIL) A4' "$OUT" | head -1)"
  echo "  [$which $label mode=$mode] $(/usr/bin/grep -E '^(PASS|FAIL) A4' "$OUT" | head -1 | cut -c1-300)"
}
has() { /usr/bin/grep -q -F -- "$2" "$1"; }

# ---------------------------------------------------------------- ARM0 drift guard
P_TO="$(/usr/bin/grep -c -F 'is_assert = ("AssertionError" in msgs) or bool(re.search(r"\bexpect\(", msgs))' "$TO")"
P_NEW="$(/usr/bin/grep -c -F 'assertion = lambda msgs: ("AssertionError" in msgs) or bool(re.search(r"\bexpect\(", msgs))' "$NEW")"
P_NEW_OLDSUB="$(/usr/bin/grep -c -i -F '"expected" in msgs.lower()' "$NEW")"
P_OLD_OLDSUB="$(/usr/bin/grep -c -i -F '"expected" in msgs.lower()' "$OLD")"   # positive control: the old text is findable
echo "=== ARM0 predicate: test_only=$P_TO new=$P_NEW ; substring test in NEW=$P_NEW_OLDSUB (OLD=$P_OLD_OLDSUB, positive control)"
[ "$P_TO" -eq 1 ] && [ "$P_NEW" -eq 1 ] && [ "$P_NEW_OLDSUB" -eq 0 ] && [ "$P_OLD_OLDSUB" -ge 1 ]; arm ARM0 $? "the test_only predicate is the code_patch predicate; no '\"expected\" in msgs.lower()' left in NEW"

# ---------------------------------------------------------------- synthetic fixtures from the REAL runs
python3 - "$FX" "$SP" <<'PYSYN'
import json, sys, copy
fx, sp = sys.argv[1], sys.argv[2]
v = json.load(open(f"{fx}/vitest_ks1258/red_first.json"))
jst = json.load(open(f"{fx}/jest_ks1229n6/red_first.json"))
tsl = json.load(open(f"{fx}/jest_ts_load_ks1074n3/red_first.json"))
cells = lambda j: [a for t in j["testResults"] for a in t["assertionResults"]]
red = next(a for a in cells(v) if a["status"] == "failed")
frame = [l for l in red["failureMessages"][0].split("\n") if l.strip().startswith("at ")][0]   # the real vitest frame
# REAL node v24.7.0 output (PROVENANCE.txt), first two stack lines, + the real vitest frame
MSG = {
  "eoj":  "SyntaxError: Unexpected end of JSON input\n    at JSON.parse (<anonymous>)\n" + frame,
  "tok":  "SyntaxError: Unexpected token 'export'\n    at new Function (<anonymous>)\n" + frame,
  "html": "SyntaxError: Unexpected token '<', \"<html>\" is not valid JSON\n    at JSON.parse (<anonymous>)\n" + frame,
  "type": "TypeError: Cannot read properties of undefined (reading 'isOptional')\n" + frame,
  "mod":  "Error: Cannot find module './no-such-module-ks'\nRequire stack:\n" + frame,
}
def recount(j):
    c = cells(j); j["numTotalTests"] = len(c)
    j["numFailedTests"] = sum(a["status"] == "failed" for a in c); j["numPassedTests"] = sum(a["status"] == "passed" for a in c)
for k, m in MSG.items():
    a = copy.deepcopy(v); r = next(x for x in cells(a) if x["status"] == "failed"); r["failureMessages"] = [m]
    json.dump(a, open(f"{sp}/v_{k}.json", "w"), ensure_ascii=False)
# ARM3d: jest declared red cell (title "RED KS-1229 VT1 …", no 🔴) fails with Unexpected end of JSON input
a = copy.deepcopy(jst); r = next(x for x in cells(a) if x["status"] == "failed")
jframe = [l for l in r["failureMessages"][0].split("\n") if l.strip().startswith("at ")][0]
r["failureMessages"] = ["SyntaxError: Unexpected end of JSON input\n    at JSON.parse (<anonymous>)\n" + jframe]
json.dump(a, open(f"{sp}/j_eoj.json", "w"), ensure_ascii=False)
# ARM4d: the vitest assertion file + a second testResult that failed to load (the real jest TS6133 file entry)
a = copy.deepcopy(v); le = copy.deepcopy(tsl["testResults"][0]); le["assertionResults"] = []
a["testResults"].append(le); a["numFailedTestSuites"] = 1
json.dump(a, open(f"{sp}/v_plus_loadfile.json", "w"), ensure_ascii=False)
# ARM5: the real 🔴 assertion red stays; a second 🔴 cell (a copy of it) fails with Unexpected end of JSON input
a = copy.deepcopy(v); tr = a["testResults"][0]["assertionResults"]; r = next(x for x in tr if x["status"] == "failed")
twin = copy.deepcopy(r); twin["title"] = "🔴 the advice JSON parses (a second red)"; twin["fullName"] = twin["title"]
twin["failureMessages"] = [MSG["eoj"]]; tr.insert(tr.index(r) + 1, twin); recount(a)
json.dump(a, open(f"{sp}/v_mix.json", "w"), ensure_ascii=False)
i = json.load(open(f"{fx}/vitest_ks1258/input.json")); i["defect_line"].pop("red_cells", None)
json.dump(i, open(f"{sp}/v_input_undeclared.json", "w"), ensure_ascii=False)
print("synthetic fixtures written:", ", ".join(sorted(["v_" + k for k in MSG] + ["j_eoj", "v_plus_loadfile", "v_mix"])))
PYSYN
[ -f "$SP/v_mix.json" ] || { echo "FATAL: synthetic fixtures not written"; exit 2; }
VI="$FX/vitest_ks1258/input.json"; JI="$FX/jest_ks1229n6/input.json"

echo "=== ARM1 REAL vitest assertion red -> ASSERTION, NEW PASS A4"
run_a4 new arm1 "$FX/vitest_ks1258/red_first.json" "$VI"
[ "$V" = "PASS A4" ] && has "$OUT" "assertion reds"; arm ARM1 $? "vitest AssertionError red classed ASSERTION (PASS A4)"

echo "=== ARM2 REAL jest assertion red -> ASSERTION, NEW PASS A4"
run_a4 new arm2 "$FX/jest_ks1229n6/red_first.json" "$JI"
[ "$V" = "PASS A4" ] && has "$OUT" "(1 failed / 87 run;"; arm ARM2 $? "jest expect(received).toEqual(expected) red classed ASSERTION (PASS A4, 1/87)"

three() { # three <arm> <fixture> <input> <needle-in-NEW-FAIL> <what>
  local n="$1" f="$2" i="$3" needle="$4" what="$5" vn vo
  run_a4 new "$n" "$f" "$i"; vn="$V"; local on="$OUT"
  run_a4 old "$n" "$f" "$i"; vo="$V"
  [ "$vn" = "FAIL A4" ] && has "$on" "non-assertion failure(s)" && has "$on" "$needle" && [ "$vo" = "PASS A4" ]
  arm "$n" $? "$what: NEW FAIL (non-assertion, names '$needle'); OLD PASS (the negative control reproduces the defect)"
}
echo "=== ARM3a Unexpected end of JSON input"
three ARM3a "$SP/v_eoj.json" "$VI" "SyntaxError: Unexpected end of JSON input" "🔴 cell, Unexpected end of JSON input"
echo "=== ARM3b Unexpected token 'export'"
three ARM3b "$SP/v_tok.json" "$VI" "SyntaxError: Unexpected token 'export'" "🔴 cell, Unexpected token (import/parse)"
echo "=== ARM3c Unexpected token '<' (not valid JSON)"
three ARM3c "$SP/v_html.json" "$VI" "SyntaxError: Unexpected token '<'" "🔴 cell, Unexpected token '<'"
echo "=== ARM3d jest declared cell, Unexpected end of JSON input"
run_a4 new ARM3d "$SP/j_eoj.json" "$JI"; vn="$V"; on="$OUT"
run_a4 old ARM3d "$SP/j_eoj.json" "$JI"; vo="$V"
[ "$vn" = "FAIL A4" ] && has "$on" "SyntaxError: Unexpected end of JSON input" && [ "$vo" = "PASS A4" ]
arm ARM3d $? "jest declared red cell (no 🔴) failing Unexpected end of JSON: NEW FAIL; OLD PASS (control)"

echo "=== ARM4a TypeError"
run_a4 new ARM4a "$SP/v_type.json" "$VI"
[ "$V" = "FAIL A4" ] && has "$OUT" "TypeError: Cannot read properties of undefined"; arm ARM4a $? "TypeError load/type failure: NEW FAIL (not an assertion)"
echo "=== ARM4b Cannot find module (declared cell)"
run_a4 new ARM4b "$SP/v_mod.json" "$VI"
[ "$V" = "FAIL A4" ] && has "$OUT" "non-assertion failure(s)" && has "$OUT" "Error: Cannot find module './no-such-module-ks'"; arm ARM4b $? "module-not-found: NEW FAIL, named as a non-assertion failure"
echo "=== ARM4e Cannot find module, brief declares no red_cells"
three ARM4e "$SP/v_mod.json" "$SP/v_input_undeclared.json" "Error: Cannot find module './no-such-module-ks'" "undeclared 🔴 cell, module-not-found"
echo "=== ARM4c REAL jest TS6133 load failure (0 tests run)"
run_a4 new ARM4c "$FX/jest_ts_load_ks1074n3/red_first.json" "$FX/jest_ts_load_ks1074n3/input.json"
[ "$V" = "FAIL A4" ] && ! has "$OUT" "PASS A4"; arm ARM4c $? "TS type error, suite failed to run: NEW FAIL A4 ($(/usr/bin/grep -o -E 'did not run any test|non-assertion' "$OUT" | head -1))"
echo "=== ARM4d assertion file + a load-failed file"
run_a4 new ARM4d "$SP/v_plus_loadfile.json" "$VI"
[ "$V" = "FAIL A4" ] && has "$OUT" "(file) "; arm ARM4d $? "a file that failed to load beside an assertion red: NEW FAIL naming the (file)"

echo "=== ARM5 mix: one assertion red + one Unexpected end of JSON red"
three ARM5 "$SP/v_mix.json" "$VI" "🔴 the advice JSON parses (a second red) -> SyntaxError: Unexpected end of JSON input" "mixed file"

# ---------------------------------------------------------------- ARM6 census
echo "=== ARM6 census: OLD vs NEW A4 on every stored red_first.json with an input.json"
python3 - "$LM/runs" "$SP/census.tsv" <<'PYC'
import json, glob, os, sys
rows = []
for rf in sorted(glob.glob(sys.argv[1] + "/**/out.md.checker/red_first.json", recursive=True)):
    inp = os.path.join(os.path.dirname(os.path.dirname(rf)), "input.json")
    if not os.path.exists(inp): continue
    try: json.load(open(rf)); json.load(open(inp))
    except Exception: continue
    rows.append((rf, inp))
open(sys.argv[2], "w").write("".join(f"{a}\t{b}\n" for a, b in rows))
print(f"census inputs: {len(rows)}")
PYC
N=0; FLIPS=0; FLIP_BAD=0; : > "$SP/census_flips.tsv"
while IFS="$(printf '\t')" read -r rf inp; do
  [ -z "$rf" ] && continue
  N=$((N+1))
  run_a4 old "c$N" "$rf" "$inp" > /dev/null; vo="$V"
  run_a4 new "c$N" "$rf" "$inp" > /dev/null; vn="$V"; on="$OUT"
  run="${rf#$LM/runs/}"; run="${run%/out.md.checker/red_first.json}"
  if [ "$vo" != "$vn" ]; then
    FLIPS=$((FLIPS+1))
    chk="$(python3 - "$rf" <<'PYI'
import json, re, sys
j = json.load(open(sys.argv[1])); bad = []
for t in j.get("testResults", []):
    if t.get("status") == "failed" and not t.get("assertionResults"): bad.append("(file) " + (t.get("message") or "")[:60])
    for a in t.get("assertionResults", []):
        m = " ".join(a.get("failureMessages") or [])
        if a.get("status") == "failed" and "AssertionError" not in m and not re.search(r"\bexpect\(", m): bad.append(m.strip().split("\n")[0][:70])
print(("CONSISTENT " + " | ".join(bad)) if bad else "INCONSISTENT no non-assertion failure found")
PYI
)"
    echo "  FLIP [$vo -> $vn] $run :: $chk"
    printf '%s\t%s\t%s\t%s\n' "$run" "$vo" "$vn" "$chk" >> "$SP/census_flips.tsv"
    case "$chk" in CONSISTENT*) ;; *) FLIP_BAD=$((FLIP_BAD+1));; esac
    { [ "$vo" = "PASS A4" ] && [ "$vn" = "FAIL A4" ]; } || FLIP_BAD=$((FLIP_BAD+1))
  fi
done < "$SP/census.tsv"
echo "  census: $N runs, $FLIPS flip(s) (list: $SP/census_flips.tsv)"
[ "$N" -ge 1 ] && [ "$FLIP_BAD" -eq 0 ]; arm ARM6 $? "census $N runs, $FLIPS flip(s), every flip OLD PASS -> NEW FAIL on a real non-assertion red"

echo "RESULT: $OKN ok, $BADN bad"
[ "$BADN" -eq 0 ]
