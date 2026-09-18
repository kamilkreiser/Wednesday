#!/bin/bash
# test_only_arms.sh — red-proof for the test_only tier (tasks/test_only/: build_test_only_input.sh, checker.sh, task.md;
# 2026-09-18, commissioned by Wednesday). Every checker arm runs the REAL checker end to end in ONE scratch clone at
# develop 8b9c3f022 (the tip Secuura PR #1042 / KS-1254 was raised against) and reads its PASS/FAIL/RESULT lines and rc.
# Nothing is re-implemented; each fixture is built from the REAL #1042 diff (`git diff 8b9c3f022 2ad066ae2 -- <test>`,
# a read verb on the source checkout) or the golden input, with ONE named edit asserted to have landed.
#
#   ARM1  GOLDEN PASS — the real #1042 test diff, golden input (night/briefs/KS-1254.md) → RESULT: PASS (8/8), M2 reds
#         exactly {variantUpperA, liveness}, M6 exactly {credit, liveness}; AND the planted bytes hash to the r2 gate's
#         landed blobs (git hash-object: 31973b68c for M2, dc88518e7 for M6) — the tamper is the gate's, byte for byte
#   ARM2  declared-set strictness — the input claims M2 reds only {variantUpperA} (liveness omitted) → FAIL T6[M2]
#         naming `red but NOT declared` + the liveness cell; stopped at T6
#   ARM3  a cell that does not reach — the diff with the `credit` row (and its comment) removed, input built from a brief
#         without those two '+' lines and M6 declared {liveness} → M2 still PASS, FAIL T6[M6] (measured: M6 reds NOTHING —
#         liveness included — the gate report's "develop 0 red under M6"); stopped at T6
#   ARM3c the same diff with an input that still declares `credit` red under M6 → FAIL T5 (a declared cell not in the run)
#   ARM3b the same credit-less diff against the GOLDEN input → FAIL T4 naming the missing credit line (no test run)
#   ARM4  a product-file touch — the golden diff plus a comment line added to contract.mjs → FAIL T2, stopped at T2
#   ARM5  restore guard — TO_TEST_SKIP_RESTORE=M2 (the arms-only hook) → FAIL T8[M2] RESTORE FAILED, stopped at T8, and
#         the clone's contract.mjs really is still tampered (sha != tip) — then ARM5b: the golden again on that SAME
#         dirty clone → the checker's reset restores it and PASS (8/8)
#   ARM6  NEW behaviour — variantUpperA's expectation flipped true → false in the diff AND the input's '+' line → FAIL T5
#         (red at the untouched tip), stopped at T5, no tamper planted
#   ARM7  JEST PASS — a NEW originate test file (jest/ts-jest) pinning DOCUMENT_WRITE_ROLES with tampers J1/J2
#         (tests/fixtures/test_only/jest_brief.md) → RESULT: PASS (8/8), runner jest
#   ARM7b JEST subset strictness — J1 declared to red one cell MORE than it does (`leaves OWNER out`) → FAIL T6[J1]
#         naming `declared but GREEN`
#   ARM8  every red is an ASSERTION — a tamper M2 whose To is a syntax error (the guard cannot load) → FAIL T6[M2]
#         naming NON-ASSERTION red(s)
#   ARM9  the builder refuses what the checker could not grade: (a) a tamper From that is not the tip's line, (b) a blank
#         line in a modify-in-place fence, (c) a tamper with an empty Reds, (d) a control also declared red → rc 2 each;
#         and the golden brief → rc 0
#
# Usage: TO_CLONE=<clone at 8b9c3f022, prepared by tasks/test_only/prepare_clone.sh for packages/shared AND
#        services/originate> bash test_only_arms.sh
#        With TO_CLONE unset, the arms make one under TO_SCRATCH (default a mktemp -d): `git clone --shared --no-checkout
#        <source> <clone>` + `checkout --detach 8b9c3f022` + prepare_clone.sh twice — every write verb in the scratch clone.
# rc 0 only when every arm holds. Every rc is read on its own line, never through a pipe. No rm. bash 3.2.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
TD=$LM/tasks/test_only
CK="${TO_CHECKER:-$TD/checker.sh}"
BLD=$TD/build_test_only_input.sh
FX=$LM/tests/fixtures/test_only
SRC="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
TIP=8b9c3f022bee76b79a47f1b8c5de8ad3ddb4a0ae
HEAD1042=2ad066ae213631e05a6f0d67d5d57b73cdb23dac
TF=Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts
CM=Blockchain/Dev/scripts/spec-examples/check/contract.mjs
SP="${TO_SCRATCH:-$(mktemp -d "${TMPDIR:-/tmp}/to_arms.XXXXXX")}"
mkdir -p "$SP"
RUNS="$SP/arms_$(date +%Y%m%d-%H%M%S)"; mkdir -p "$RUNS"
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }
bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
for f in "$CK" "$BLD" "$LM/night/briefs/KS-1254.md" "$FX/jest_brief.md" "$FX/jest_golden.diff"; do [ -f "$f" ] || { echo "FATAL: missing $f"; exit 2; }; done
echo "test_only arms $(date '+%F %H:%M:%S') · checker $CK ($(shasum -a 256 "$CK" | cut -c1-12)) · builder ($(shasum -a 256 "$BLD" | cut -c1-12)) · runs $RUNS"

# ---- the clone
CLONE="${TO_CLONE:-}"
if [ -z "$CLONE" ]; then
  CLONE="$SP/clone_to_arms"
  if [ ! -d "$CLONE/.git" ]; then
    git clone --shared --no-checkout "$SRC" "$CLONE" > "$RUNS/clone.out" 2>&1
    git -C "$CLONE" checkout --detach "$TIP" >> "$RUNS/clone.out" 2>&1
  fi
fi
[ "$(git -C "$CLONE" rev-parse HEAD 2>/dev/null)" = "$TIP" ] || { echo "FATAL: $CLONE is not a clone at $TIP"; exit 2; }

# ---- inputs (the builder, on the golden brief and the jest fixture brief)
bash "$BLD" KS-1254 "$RUNS/in_golden.json" "$LM/night/briefs/KS-1254.md" ctx=65536 > "$RUNS/build_golden.out" 2>&1
rc=$?
[ "$rc" -eq 0 ] || { echo "FATAL: the golden brief did not build (rc $rc): $(cat "$RUNS/build_golden.out")"; exit 2; }
bash "$BLD" TO-ARMS-JEST "$RUNS/in_jest.json" "$FX/jest_brief.md" > "$RUNS/build_jest.out" 2>&1
rc=$?
[ "$rc" -eq 0 ] || { echo "FATAL: the jest fixture brief did not build (rc $rc): $(cat "$RUNS/build_jest.out")"; exit 2; }
bash "$TD/prepare_clone.sh" "$RUNS/in_golden.json" "$CLONE" > "$RUNS/prepare_shared.out" 2>&1
rc=$?
[ "$rc" -eq 0 ] || { echo "FATAL: prepare_clone (packages/shared) rc $rc"; exit 2; }
bash "$TD/prepare_clone.sh" "$RUNS/in_jest.json" "$CLONE" > "$RUNS/prepare_originate.out" 2>&1
rc=$?
[ "$rc" -eq 0 ] || { echo "FATAL: prepare_clone (services/originate) rc $rc"; exit 2; }

# ---- fixtures: the REAL #1042 diff, and one-edit variants (each edit asserted to land exactly once)
git -C "$SRC" diff "$TIP" "$HEAD1042" -- "$TF" > "$RUNS/golden.diff"
python3 - "$RUNS" "$FX" "$SRC" "$TIP" <<'PYFX'
import json, subprocess, sys
runs, fx, src, tip = sys.argv[1:5]
g = open(f"{runs}/golden.diff", encoding="utf-8").read()
assert g.count("\n+    ['credit', `credit_${V4}`, false],\n") == 1 and g.count("\n+    ['variantUpperA',") == 1, "not the #1042 diff"
def out(name, diff): open(f"{runs}/{name}.md", "w", encoding="utf-8").write("```diff\n" + diff + ("" if diff.endswith("\n") else "\n") + "```\n")
def one(t, a, b, what):
    assert t.count(a) == 1, (what, t.count(a)); return t.replace(a, b)
out("out_golden", g)
# ARM3: credit row + its comment removed; header recounted (+506,17 -> +506,15)
c1 = "+    // KS-1254: `cred` is refused as an exact prefix only (denycred below), so credit_ stays benign.\n"
c2 = "+    ['credit', `credit_${V4}`, false],\n"
nc = one(one(one(g, c1, "", "arm3 c1"), c2, "", "arm3 c2"), "@@ -506,12 +506,17 @@", "@@ -506,12 +506,15 @@", "arm3 hdr")
out("out_nocredit", nc)
# ARM4: + a product section (a comment line above contract.mjs:246, context copied from the tip)
cm = subprocess.run(["git", "-C", src, "show", f"{tip}:Blockchain/Dev/scripts/spec-examples/check/contract.mjs"], capture_output=True, text=True).stdout.split("\n")
sec = ("--- a/Blockchain/Dev/scripts/spec-examples/check/contract.mjs\n+++ b/Blockchain/Dev/scripts/spec-examples/check/contract.mjs\n"
       f"@@ -244,3 +244,4 @@\n {cm[243]}\n {cm[244]}\n+// arms: a product-file touch\n {cm[245]}\n")
out("out_product", g + sec)
# ARM6: variantUpperA asserted NOT to fire (new behaviour; red at the tip)
up_old = "+    ['variantUpperA', 'anchor_3f2b1c9e-7d4a-4b6c-Ae1f-2a3b4c5d6e7f', true],"
up_new = "+    ['variantUpperA', 'anchor_3f2b1c9e-7d4a-4b6c-Ae1f-2a3b4c5d6e7f', false],"
out("out_newbehaviour", one(g, up_old, up_new, "arm6"))
d = json.load(open(f"{runs}/in_golden.json", encoding="utf-8"))
def jw(name, x): json.dump(x, open(f"{runs}/{name}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
# ARM2: M2 declared {variantUpperA} only
x = json.loads(json.dumps(d)); t = [t for t in x["tampers"] if t["id"] == "M2"][0]; assert len(t["reds"]) == 2
t["reds"] = ["variantUpperA"]; jw("in_arm2", x)
# ARM3: the input a brief without the credit '+' lines builds
x = json.loads(json.dumps(d)); n0 = len(x["expected_plus"])
x["expected_plus"] = [e for e in x["expected_plus"] if "credit" not in e]; assert len(x["expected_plus"]) == n0 - 2
jw("in_arm3c", x)   # ARM3c: the brief still declares `credit` red under M6 -> T5 (a declared cell missing from the run)
t = [t for t in x["tampers"] if t["id"] == "M6"][0]; t["reds"] = [r for r in t["reds"] if r != "credit"]; assert len(t["reds"]) == 1
jw("in_arm3", x)    # ARM3: the brief a credit-less author writes: M6 declared {liveness} -> the tamper gate measures
# ARM6: the '+' line flipped in the input too (so T4 passes and T5 is what measures)
x = json.loads(json.dumps(d)); i = [k for k, e in enumerate(x["expected_plus"]) if "variantUpperA" in e]; assert len(i) == 1
x["expected_plus"][i[0]] = up_new[1:]; jw("in_arm6", x)
# ARM8: M2's To is a syntax error
x = json.loads(json.dumps(d)); t = [t for t in x["tampers"] if t["id"] == "M2"][0]
t["to"] = "  /^(?![a-z]*(?:token|secret;"; x["tampers"] = [t]; jw("in_arm8", x)
# ARM7/7b: jest
j = json.load(open(f"{runs}/in_jest.json", encoding="utf-8"))
out("out_jest", open(f"{fx}/jest_golden.diff", encoding="utf-8").read())
x = json.loads(json.dumps(j)); t = [t for t in x["tampers"] if t["id"] == "J1"][0]; t["reds"] = t["reds"] + ["leaves OWNER out"]; jw("in_arm7b", x)
print("fixtures ok")
PYFX
rc=$?
[ "$rc" -eq 0 ] || { echo "FATAL: fixture build rc $rc"; exit 2; }

run_ck() {
  # run_ck <name> <input> <out.md> [env assignment] — the real checker; rc into $CRC, output in $RUNS/<name>.checker.out
  local name="$1" inp="$2" om="$3"; mkdir -p "$RUNS/$name"; cp "$om" "$RUNS/$name/out.md"
  if [ -n "${4:-}" ]; then env "$4" bash "$CK" "$inp" "$RUNS/$name/out.md" "$CLONE" > "$RUNS/$name.checker.out" 2>&1
  else bash "$CK" "$inp" "$RUNS/$name/out.md" "$CLONE" > "$RUNS/$name.checker.out" 2>&1; fi
  CRC=$?
}
has(){ /usr/bin/grep -q -F -- "$2" "$RUNS/$1.checker.out"; }
res(){ /usr/bin/grep -m1 '^RESULT:' "$RUNS/$1.checker.out"; }

echo "--- ARM1 GOLDEN PASS"
run_ck arm1 "$RUNS/in_golden.json" "$RUNS/out_golden.md"
if [ "$CRC" -eq 0 ] && has arm1 "RESULT: PASS (8/8)" && has arm1 "PASS T6[M2] red set == declared exactly: {the boundary run is live: one E7 per firing row, on exactly , variantUpperA}" && has arm1 "PASS T6[M6] red set == declared exactly: {credit, the boundary run is live: one E7 per firing row, on exactly }" && has arm1 "83/83 cells"; then ok "ARM1 rc 0, $(res arm1), M2 {variantUpperA, liveness}, M6 {credit, liveness}, 83 cells"
else bad "ARM1" "rc $CRC $(res arm1)"; fi
BLOBS="$(python3 - "$RUNS/in_golden.json" "$CLONE" <<'PYB'
import json, subprocess, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); out = []
for t in d["tampers"]:
    raw = subprocess.run(["git", "-C", sys.argv[2], "show", f"{d['tip']}:{t['file']}"], capture_output=True).stdout
    L = raw.split(b"\n"); assert L[t["line"] - 1] == t["from"].encode(); L[t["line"] - 1] = t["to"].encode()
    h = subprocess.run(["git", "hash-object", "--stdin"], input=b"\n".join(L), capture_output=True).stdout.decode().strip()
    out.append(f"{t['id']}={h[:9]}")
print(" ".join(out))
PYB
)"
if [ "$BLOBS" = "M2=31973b68c M6=dc88518e7" ]; then ok "ARM1 planted bytes hash to the r2 gate's landed blobs: $BLOBS"
else bad "ARM1 blobs" "got '$BLOBS', want 'M2=31973b68c M6=dc88518e7'"; fi

echo "--- ARM2 declared-set strictness (M2 declared {variantUpperA} only)"
run_ck arm2 "$RUNS/in_arm2.json" "$RUNS/out_golden.md"
if [ "$CRC" -ne 0 ] && has arm2 "FAIL T6[M2] red set != declared: red but NOT declared ['the boundary run is live: one E7 per fi" && has arm2 "stopped at T6"; then ok "ARM2 rc $CRC: $(/usr/bin/grep -m1 '^FAIL T6' "$RUNS/arm2.checker.out" | cut -c1-160)"
else bad "ARM2" "rc $CRC $(res arm2)"; fi

echo "--- ARM3 a cell that does not reach (credit row removed)"
run_ck arm3 "$RUNS/in_arm3.json" "$RUNS/out_nocredit.md"
if [ "$CRC" -ne 0 ] && has arm3 "PASS T6[M2]" && /usr/bin/grep -q '^FAIL T6\[M6\] reds NOTHING' "$RUNS/arm3.checker.out" && has arm3 "stopped at T6"; then ok "ARM3 rc $CRC: $(/usr/bin/grep -m1 '^FAIL T6\[M6\]' "$RUNS/arm3.checker.out" | cut -c1-200)"
else bad "ARM3" "rc $CRC $(res arm3)"; fi
run_ck arm3c "$RUNS/in_arm3c.json" "$RUNS/out_nocredit.md"
if [ "$CRC" -ne 0 ] && has arm3c "DECLARED CELL NOT IN THE RUN: credit" && has arm3c "stopped at T5"; then ok "ARM3c rc $CRC: the brief still declaring credit -> FAIL T5 (declared cell not in the run), no tamper planted"
else bad "ARM3c" "rc $CRC $(res arm3c)"; fi
run_ck arm3b "$RUNS/in_golden.json" "$RUNS/out_nocredit.md"
if [ "$CRC" -ne 0 ] && has arm3b "FAIL T4 BRIEF LINES" && has arm3b "MISSING '+' \"['credit', \`credit_\${V4}\`, false],\"" && has arm3b "stopped at T4"; then ok "ARM3b rc $CRC: FAIL T4 names the missing credit row"
else bad "ARM3b" "rc $CRC $(res arm3b) $(/usr/bin/grep -m1 '^FAIL' "$RUNS/arm3b.checker.out" | cut -c1-200)"; fi

echo "--- ARM4 a product-file touch"
run_ck arm4 "$RUNS/in_golden.json" "$RUNS/out_product.md"
if [ "$CRC" -ne 0 ] && has arm4 "FAIL T2 touched-file set must be exactly" && has arm4 "$CM" && has arm4 "stopped at T2"; then ok "ARM4 rc $CRC: FAIL T2 names $CM"
else bad "ARM4" "rc $CRC $(res arm4)"; fi

echo "--- ARM5 restore guard (TO_TEST_SKIP_RESTORE=M2)"
TIPSHA="$(git -C "$CLONE" show "$TIP:$CM" | shasum -a 256 | cut -c1-64)"
run_ck arm5 "$RUNS/in_golden.json" "$RUNS/out_golden.md" TO_TEST_SKIP_RESTORE=M2
NOWSHA="$(shasum -a 256 "$CLONE/$CM" | cut -c1-64)"
if [ "$CRC" -ne 0 ] && has arm5 "FAIL T8[M2] RESTORE FAILED" && has arm5 "stopped at T8 (an unrestored tamper; hard fail)" && ! has arm5 "T6[M6]" && [ "$NOWSHA" != "$TIPSHA" ]; then ok "ARM5 rc $CRC: FAIL T8[M2] RESTORE FAILED, run stopped before M6; the clone's contract.mjs really is tampered (${NOWSHA:0:12} != tip ${TIPSHA:0:12})"
else bad "ARM5" "rc $CRC $(res arm5) now=${NOWSHA:0:12} tip=${TIPSHA:0:12}"; fi
run_ck arm5b "$RUNS/in_golden.json" "$RUNS/out_golden.md"
NOWSHA="$(shasum -a 256 "$CLONE/$CM" | cut -c1-64)"
if [ "$CRC" -eq 0 ] && has arm5b "RESULT: PASS (8/8)" && [ "$NOWSHA" = "$TIPSHA" ]; then ok "ARM5b rc 0: the next run's reset restored the tampered clone and the golden PASSES; contract.mjs == tip"
else bad "ARM5b" "rc $CRC $(res arm5b) now=${NOWSHA:0:12}"; fi

echo "--- ARM6 NEW behaviour (red at the untouched tip)"
run_ck arm6 "$RUNS/in_arm6.json" "$RUNS/out_newbehaviour.md"
if [ "$CRC" -ne 0 ] && has arm6 "PASS T4" && has arm6 "FAIL T5 GREEN AT THE TIP" && has arm6 "RED AT THE TIP: variantUpperA" && has arm6 "stopped at T5" && ! has arm6 "tamper M2:"; then ok "ARM6 rc $CRC: FAIL T5 (variantUpperA red at the tip), no tamper planted"
else bad "ARM6" "rc $CRC $(res arm6)"; fi

echo "--- ARM7 JEST PASS (originate, new file)"
run_ck arm7 "$RUNS/in_jest.json" "$RUNS/out_jest.md"
if [ "$CRC" -eq 0 ] && has arm7 "runner jest" && has arm7 "RESULT: PASS (8/8)" && has arm7 "PASS T6[J1] red set == declared exactly: {has exactly four roles, lists ISSUER_ADMIN}"; then ok "ARM7 rc 0: jest $(res arm7)"
else bad "ARM7" "rc $CRC $(res arm7)"; fi
run_ck arm7b "$RUNS/in_arm7b.json" "$RUNS/out_jest.md"
if [ "$CRC" -ne 0 ] && has arm7b "FAIL T6[J1] red set != declared: declared but GREEN ['leaves OWNER out']" && has arm7b "PASS T6[J2]"; then ok "ARM7b rc $CRC: FAIL T6[J1] declared but GREEN ['leaves OWNER out'] (a declared SUPERSET fails too)"
else bad "ARM7b" "rc $CRC $(res arm7b)"; fi

echo "--- ARM8 every red is an assertion (M2 = a syntax error)"
run_ck arm8 "$RUNS/in_arm8.json" "$RUNS/out_golden.md"
if [ "$CRC" -ne 0 ] && /usr/bin/grep -q '^FAIL T6\[M2\].*NON-ASSERTION red' "$RUNS/arm8.checker.out" && has arm8 "PASS T8[M2]"; then ok "ARM8 rc $CRC: $(/usr/bin/grep -m1 '^FAIL T6' "$RUNS/arm8.checker.out" | cut -c1-200)"
else bad "ARM8" "rc $CRC $(res arm8) $(/usr/bin/grep -m1 '^FAIL' "$RUNS/arm8.checker.out" | cut -c1-200)"; fi

echo "--- ARM9 builder refusals"
python3 - "$LM/night/briefs/KS-1254.md" "$RUNS" <<'PYR'
import sys
b = open(sys.argv[1], encoding="utf-8").read(); r = sys.argv[2]
def one(t, a, z, what):
    assert t.count(a) >= 1, what; return t.replace(a, z, 1)
open(f"{r}/brief_a.md", "w").write(one(b, "Line: 246", "Line: 245", "a"))
open(f"{r}/brief_b.md", "w").write(one(b, "+    ['variantUpperA',", "+\n+    ['variantUpperA',", "b"))
open(f"{r}/brief_c.md", "w").write(one(b, "Reds: `credit`, `liveness`", "Reds: ", "c"))
open(f"{r}/brief_d.md", "w").write(one(b, "- `denycred`", "- `denycred`\n- `credit`", "d"))
PYR
for x in a b c d; do
  bash "$BLD" KS-1254 "$RUNS/in_refuse_$x.json" "$RUNS/brief_$x.md" > "$RUNS/build_refuse_$x.out" 2>&1
  brc=$?
  if [ "$brc" -eq 2 ] && /usr/bin/grep -q 'REFUSED' "$RUNS/build_refuse_$x.out"; then ok "ARM9$x builder rc 2: $(cut -c1-150 "$RUNS/build_refuse_$x.out" | head -1)"
  else bad "ARM9$x" "builder rc $brc: $(head -2 "$RUNS/build_refuse_$x.out")"; fi
done
bash "$BLD" KS-1254 "$RUNS/in_golden_again.json" "$LM/night/briefs/KS-1254.md" > "$RUNS/build_again.out" 2>&1
brc=$?
[ "$brc" -eq 0 ] && ok "ARM9 control: the golden brief builds (rc 0)" || bad "ARM9 control" "rc $brc"

echo "arms: $pass ok, $fail failed (runs in $RUNS)"
[ "$fail" -eq 0 ] && exit 0
exit 1
