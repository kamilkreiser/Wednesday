#!/bin/bash
# test_only_bash_arms.sh — red-proof for the test_only tier's BASH runner (tasks/test_only/: checker.sh, builder,
# prepare_clone.sh; 2026-09-18 18:xx, commissioned by Wednesday). Sibling of test_only_arms.sh (the 18 vitest/jest arms,
# which must keep passing). Every checker arm runs the REAL checker end to end in ONE scratch clone at Secuura develop
# 921d201e3 — the parent of #875 (c342a62e9, KS-936), a MERGED test-only change to orchestrate_jobs.test.sh that adds
# CELL 13 pinning EXISTING orchestrate.sh behaviour. Nothing is re-implemented; each fixture is the golden with ONE
# named edit asserted to land exactly once.
#
#   B1   GOLDEN PASS — the builder's input from tests/fixtures/test_only/bash_brief_ks936.md, answer = the brief's own
#        fence (bash_golden_ks936.diff) → RESULT: PASS (8/8), runner bash, 13/13 cells, P1 reds exactly {cell13},
#        S1 reds exactly {cell4, cell11} — the red sets #875's commit message measured ("ONLY CELL 13 red";
#        "reds CELLS 4 and 11 and leaves CELL 13 green")
#   B1r  the REAL #875 diff byte for byte (em-dashes and blank lines included) against the same input with its
#        expected_plus set to the real '+' lines → PASS (8/8), same red sets
#   B2   declared-set strictness — S1 declared {cell4} only → FAIL T6[S1] `red but NOT declared`
#   B2b  superset — P1 declared {cell13, cell4} → FAIL T6[P1] `declared but GREEN`
#   B3   a tamper no cell reaches (SC_PROFILE at orchestrate.sh:142, declared {cell13}) → FAIL T6 `reds NOTHING`
#   B4a  NON-ASSERTION — CELL 13's red branch calls `badd` (undefined): under P1 the suite prints no FAIL for it and
#        bash says `badd: command not found` → FAIL T6[P1] (a bash diagnostic; the cell did not run)
#   B4b  NON-ASSERTION — CELL 13's red branch runs `tailx` inside its message: the FAIL line prints AND bash says
#        `tailx: command not found` → FAIL T6[P1] `NON-ASSERTION red(s)`
#   B5   a product-file touch (a comment added to orchestrate.sh) → FAIL T2, stopped at T2
#   B6   NEW behaviour — CELL 13's `!= 0` flipped to `= 0` (answer and brief) → FAIL T5 (red at the tip), no tamper
#   B7   restore guard — TO_TEST_SKIP_RESTORE=P1 → FAIL T8[P1]; then B7b the golden on that dirty clone → PASS
#   B8   an ambiguous cell name (a control `an UNREADABLE` prefixes three cells) → FAIL T5 `AMBIGUOUS`
#   B9   the suite prints FAIL but exits 0 (a `fail=0` before the totals) → FAIL T6[P1] `EXITED 0`
#   B10  builder refusals (rc 2 each): a — a bash-4 idiom (mapfile); b — a cell name not in the suite's text;
#        c — a tamper that breaks parsing; d — a cell name carrying `$`; e — a tamper on a test file; f — a fence
#        that does not parse; g — a NEW suite with no ok/FAIL cell printer; and the golden brief → rc 0
#
# Usage: TOB_CHECKER=<checker> TOB_BUILDER=<builder> TOB_PREPARE=<prepare_clone> TOB_SCRATCH=<dir> bash test_only_bash_arms.sh
#        (defaults: the live tasks/test_only files, a mktemp -d). Every write verb runs in the scratch clone. No rm.
# rc 0 only when every arm holds. Every rc read on its own line, never through a pipe. bash 3.2.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
TD=$LM/tasks/test_only
CK="${TOB_CHECKER:-$TD/checker.sh}"
BLD="${TOB_BUILDER:-$TD/build_test_only_input.sh}"
PREP="${TOB_PREPARE:-$TD/prepare_clone.sh}"
FX=$LM/tests/fixtures/test_only
SRC="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
TIP=921d201e358f572d6d19e84a5403a176b35e1f77
TF=Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh
OR=Blockchain/Testing/ci/orchestrate.sh
SP="${TOB_SCRATCH:-$(mktemp -d "${TMPDIR:-/tmp}/tob_arms.XXXXXX")}"
mkdir -p "$SP"
RUNS="$SP/bash_arms_$(date +%Y%m%d-%H%M%S)"; mkdir -p "$RUNS"
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }
bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
for f in "$CK" "$BLD" "$PREP" "$FX/bash_brief_ks936.md" "$FX/bash_golden_ks936.diff" "$FX/bash_golden_real_875.diff"; do [ -f "$f" ] || { echo "FATAL: missing $f"; exit 2; }; done
echo "test_only BASH arms $(date '+%F %H:%M:%S') · checker $CK ($(shasum -a 256 "$CK" | cut -c1-12)) · builder $BLD ($(shasum -a 256 "$BLD" | cut -c1-12)) · /bin/bash $(/bin/bash -c 'echo $BASH_VERSION') · runs $RUNS"

CLONE="$SP/clone_bash_arms"
if [ ! -d "$CLONE/.git" ]; then
  git clone --shared --no-checkout "$SRC" "$CLONE" > "$RUNS/clone.out" 2>&1
  git -C "$CLONE" checkout --detach "$TIP" >> "$RUNS/clone.out" 2>&1
fi
[ "$(git -C "$CLONE" rev-parse HEAD 2>/dev/null)" = "$TIP" ] || { echo "FATAL: $CLONE is not a clone at $TIP"; exit 2; }

bash "$BLD" KS-936-GOLDEN "$RUNS/in_golden.json" "$FX/bash_brief_ks936.md" > "$RUNS/build_golden.out" 2>&1
rc=$?
[ "$rc" -eq 0 ] || { echo "FATAL: the golden bash brief did not build (rc $rc): $(cat "$RUNS/build_golden.out")"; exit 2; }
bash "$PREP" "$RUNS/in_golden.json" "$CLONE" > "$RUNS/prepare.out" 2>&1
rc=$?
[ "$rc" -eq 0 ] || { echo "FATAL: prepare_clone rc $rc: $(cat "$RUNS/prepare.out")"; exit 2; }
/usr/bin/grep -q 'runner bash — no node farm' "$RUNS/prepare.out" || { echo "FATAL: prepare_clone did not take the bash path: $(cat "$RUNS/prepare.out")"; exit 2; }

python3 - "$RUNS" "$FX" "$SRC" "$TIP" <<'PYFX'
import json, subprocess, sys
runs, fx, src, tip = sys.argv[1:5]
g = open(f"{fx}/bash_golden_ks936.diff", encoding="utf-8").read()
real = open(f"{fx}/bash_golden_real_875.diff", encoding="utf-8").read()
assert real.count("\n+build_fixture \"$WORK/postapiunread\" post-api-unreadable\n") == 1, "not the #875 diff"
def out(name, diff): open(f"{runs}/{name}.md", "w", encoding="utf-8").write("```diff\n" + diff + ("" if diff.endswith("\n") else "\n") + "```\n")
def one(t, a, b, what):
    assert t.count(a) == 1, (what, t.count(a)); return t.replace(a, b)
d = json.load(open(f"{runs}/in_golden.json", encoding="utf-8"))
def jw(name, x): json.dump(x, open(f"{runs}/{name}.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
cp = lambda: json.loads(json.dumps(d))
def ep_one(x, a, b, what):
    i = [k for k, e in enumerate(x["expected_plus"]) if e == a]; assert len(i) == 1, (what, len(i)); x["expected_plus"][i[0]] = b
out("out_golden", g); out("out_real", real)
# B1r: the real '+' lines
x = cp(); x["expected_plus"] = [l[1:] for l in real.split("\n") if l.startswith("+") and not l.startswith("+++")]; jw("in_real", x)
# B2 / B2b
x = cp(); t = [t for t in x["tampers"] if t["id"] == "S1"][0]; assert len(t["reds"]) == 2; t["reds"] = t["reds"][:1]; jw("in_b2", x)
x = cp(); t = [t for t in x["tampers"] if t["id"] == "P1"][0]; t["reds"] = t["reds"] + [d["tampers"][1]["reds"][0]]; jw("in_b2b", x)
# B3: a tamper no cell reaches
orl = subprocess.run(["git", "-C", src, "show", f"{tip}:Blockchain/Testing/ci/orchestrate.sh"], capture_output=True, text=True).stdout.split("\n")
frm = 'SC_PROFILE=$([ "$TIER" = "pr" ] && echo "readonly" || echo "all")'; assert orl[141] == frm, orl[141]
x = cp(); x["tampers"] = [{"id": "Z", "file": "Blockchain/Testing/ci/orchestrate.sh", "line": 142, "from": frm,
                           "to": frm.replace('"readonly"', '"all"'), "reds": list(d["tampers"][0]["reds"]), "reds_as_written": ["cell13"]}]; jw("in_b3", x)
# B4a: `badd` in CELL 13's red branch (answer and brief)
a = '  bad "an UNREADABLE post-API job makes the GATE NOT PASS, REFUSES by name, and claims nothing about having run" \\'
a = "  " + a
out("out_b4a", one(g, "\n+" + a + "\n", "\n+" + a.replace("bad \"", "badd \"", 1) + "\n", "b4a"))
x = cp(); ep_one(x, a, a.replace("bad \"", "badd \"", 1), "b4a ep"); jw("in_b4a", x)
# B4b: `tailx` in its message
m = '        "rc=$rc_pa (rc=0 here is the pre-fix GATE PASS this cell exists to catch), output: $(tail -5 "$WORK/postapiunread/out.txt" | tr \'\\n\' \' \')"'
out("out_b4b", one(g, "\n+" + m + "\n", "\n+" + m.replace("$(tail -5", "$(tailx -5") + "\n", "b4b"))
x = cp(); ep_one(x, m, m.replace("$(tail -5", "$(tailx -5"), "b4b ep"); jw("in_b4b", x)
# B5: + a product section
sec = (f"--- a/Blockchain/Testing/ci/orchestrate.sh\n+++ b/Blockchain/Testing/ci/orchestrate.sh\n"
       f"@@ -45,2 +45,3 @@\n {orl[44]}\n+# arms: a product-file touch\n {orl[45]}\n")
out("out_b5", g + sec)
# B6: CELL 13 asserts the opposite (red at the untouched tip)
c6 = '  if [ "$rc_pa" != 0 ] \\'
out("out_b6", one(g, "\n+" + c6 + "\n", "\n+" + c6.replace("!= 0", "= 0") + "\n", "b6"))
x = cp(); ep_one(x, c6, c6.replace("!= 0", "= 0"), "b6 ep"); jw("in_b6", x)
# B8: an ambiguous control
x = cp(); x["controls"] = x["controls"] + ["an UNREADABLE"]; jw("in_b8", x)
# B9: `fail=0` before the totals — FAIL lines printed, rc 0
lastp = 'chmod 644 "$PA_UNREAD_JOB" 2>/dev/null'
b9 = one(g, "\n+" + lastp + "\n", "\n+" + lastp + "\n+fail=0\n", "b9")
b9 = one(b9, "@@ -351,1 +357,42 @@", "@@ -351,1 +357,43 @@", "b9 hdr")
out("out_b9", b9)
x = cp(); x["expected_plus"] = x["expected_plus"] + ["fail=0"]; jw("in_b9", x)
# B10 builder refusal briefs
b = open(f"{fx}/bash_brief_ks936.md", encoding="utf-8").read()
w = lambda n, t: open(f"{runs}/brief_{n}.md", "w", encoding="utf-8").write(t)
w("a", one(b, '+  rc_pa="$(run_orchestrator "$WORK/postapiunread")"', '+  mapfile -t _x < /dev/null; rc_pa="$(run_orchestrator "$WORK/postapiunread")"', "a"))
w("b", one(b, "`cell13` = `an UNREADABLE post-API job makes the GATE NOT PASS`", "`cell13` = `an UNREADABLE post-API job makes the GATE FAIL`", "b"))
w("c", one(b, 'To:\n```\n  if true; then\n```\nReds: `cell13`', 'To:\n```\n  if require_job "$job"; the\n```\nReds: `cell13`', "c"))
w("d", one(b, "- `SELF and RUN_DIR are BOUND in a child process`", "- `SELF and RUN_DIR are BOUND in a child process`\n- `a missing job makes the run REFUSE loudly, BY NAME, and exit non-zero (rc=$rc_miss)`", "d"))
w("e", one(b, "File: `Blockchain/Testing/ci/orchestrate.sh`\nLine: 105\nFrom:\n```\n  if require_job \"$job\"; then\n```\nTo:\n```\n  if true; then\n```",
             "File: `Blockchain/Dev/scripts/__tests__/stack_env.test.sh`\nLine: 1\nFrom:\n```\n#!/usr/bin/env bash\n```\nTo:\n```\n#!/bin/sh\n```", "e"))
w("f", one(b, '+    elif [ "$mode" = post-api-unreadable ] && [ "$j" = 06-tenant-isolation ]; then', '+    elif [ "$mode" = post-api-unreadable ] && [ "$j" = 06-tenant-isolation ]; the', "f"))
g_new = ("# arms: a NEW suite with no cell printer\n\nFile: `Blockchain/Dev/scripts/__tests__/arms_noprinter.test.sh`\nTip: `" + tip + "`\n\n## The exact change\n\n```diff\n"
         "@@ -0,0 +1,3 @@\n+#!/usr/bin/env bash\n+echo \"all good\"\n+exit 0\n```\n\n## Tampers\n\n### P1 x\nFile: `Blockchain/Testing/ci/orchestrate.sh`\nLine: 129\nFrom:\n```\n  if require_job \"$job\"; then\n```\nTo:\n```\n  if true; then\n```\nReds: `all good`\n\n## Controls\n\n- `exit 0`\n")
w("g", g_new)
print("fixtures ok")
PYFX
rc=$?
[ "$rc" -eq 0 ] || { echo "FATAL: fixture build rc $rc"; exit 2; }

run_ck() {
  local name="$1" inp="$2" om="$3"; mkdir -p "$RUNS/$name"; cp "$om" "$RUNS/$name/out.md"
  if [ -n "${4:-}" ]; then env "$4" bash "$CK" "$inp" "$RUNS/$name/out.md" "$CLONE" > "$RUNS/$name.checker.out" 2>&1
  else bash "$CK" "$inp" "$RUNS/$name/out.md" "$CLONE" > "$RUNS/$name.checker.out" 2>&1; fi
  CRC=$?
}
has(){ /usr/bin/grep -q -F -- "$2" "$RUNS/$1.checker.out"; }
res(){ /usr/bin/grep -m1 '^RESULT:' "$RUNS/$1.checker.out"; }
firstfail(){ /usr/bin/grep -m1 '^FAIL' "$RUNS/$1.checker.out" | cut -c1-220; }
C13="an UNREADABLE post-API job makes the GATE NOT PASS"
C4="a missing job makes the run REFUSE loudly, BY NAME, and exit non-zero"
C11="an UNREADABLE Stage-1 job REFUSES by name and exits non-zero"

echo "--- B1 GOLDEN PASS (brief fence as the answer)"
run_ck b1 "$RUNS/in_golden.json" "$RUNS/out_golden.md"
if [ "$CRC" -eq 0 ] && has b1 "RESULT: PASS (8/8)" && has b1 "runner=bash cells=13" && has b1 "PASS T6[P1] red set == declared exactly: {$C13}" && has b1 "PASS T6[S1] red set == declared exactly: {a missing job makes the run REFUSE loudly, BY NAME, and exit, $C11}" && has b1 "13/13 cells"; then ok "B1 rc 0, $(res b1), P1 {cell13}, S1 {cell4, cell11}, 13 cells"
else bad "B1" "rc $CRC $(res b1) $(firstfail b1)"; fi

echo "--- B1r the REAL #875 diff, byte for byte"
run_ck b1r "$RUNS/in_real.json" "$RUNS/out_real.md"
if [ "$CRC" -eq 0 ] && has b1r "RESULT: PASS (8/8)" && has b1r "PASS T6[P1] red set == declared exactly: {$C13}" && has b1r "PASS T6[S1] red set == declared exactly"; then ok "B1r rc 0: the merged #875 change itself grades PASS (8/8) with the same red sets"
else bad "B1r" "rc $CRC $(res b1r) $(firstfail b1r)"; fi

echo "--- B2 / B2b declared-set strictness"
run_ck b2 "$RUNS/in_b2.json" "$RUNS/out_golden.md"
if [ "$CRC" -ne 0 ] && has b2 "FAIL T6[S1] red set != declared: red but NOT declared ['an UNREADABLE Stage-1 job REFUSES" && has b2 "PASS T6[P1]"; then ok "B2 rc $CRC: $(/usr/bin/grep -m1 '^FAIL T6' "$RUNS/b2.checker.out" | cut -c1-150)"
else bad "B2" "rc $CRC $(res b2) $(firstfail b2)"; fi
run_ck b2b "$RUNS/in_b2b.json" "$RUNS/out_golden.md"
if [ "$CRC" -ne 0 ] && has b2b "FAIL T6[P1] red set != declared: declared but GREEN ['a missing job makes the run REFUSE"; then ok "B2b rc $CRC: FAIL T6[P1] declared but GREEN (a superset fails too)"
else bad "B2b" "rc $CRC $(res b2b) $(firstfail b2b)"; fi

echo "--- B3 a tamper no cell reaches"
run_ck b3 "$RUNS/in_b3.json" "$RUNS/out_golden.md"
if [ "$CRC" -ne 0 ] && /usr/bin/grep -q '^FAIL T6\[Z\] reds NOTHING' "$RUNS/b3.checker.out" && has b3 "PASS T8[Z]"; then ok "B3 rc $CRC: $(/usr/bin/grep -m1 '^FAIL T6' "$RUNS/b3.checker.out" | cut -c1-150)"
else bad "B3" "rc $CRC $(res b3) $(firstfail b3)"; fi

echo "--- B4a / B4b non-assertion reds"
run_ck b4a "$RUNS/in_b4a.json" "$RUNS/out_b4a.md"
if [ "$CRC" -ne 0 ] && has b4a "PASS T5" && /usr/bin/grep -q '^FAIL T6\[P1\].*bash diagnostic.*badd: command not found' "$RUNS/b4a.checker.out"; then ok "B4a rc $CRC: $(/usr/bin/grep -m1 '^FAIL T6' "$RUNS/b4a.checker.out" | cut -c1-230)"
else bad "B4a" "rc $CRC $(res b4a) $(firstfail b4a)"; fi
run_ck b4b "$RUNS/in_b4b.json" "$RUNS/out_b4b.md"
if [ "$CRC" -ne 0 ] && has b4b "PASS T5" && /usr/bin/grep -q '^FAIL T6\[P1\] NON-ASSERTION red(s).*tailx: command not found' "$RUNS/b4b.checker.out"; then ok "B4b rc $CRC: $(/usr/bin/grep -m1 '^FAIL T6' "$RUNS/b4b.checker.out" | cut -c1-230)"
else bad "B4b" "rc $CRC $(res b4b) $(firstfail b4b)"; fi

echo "--- B5 a product-file touch"
run_ck b5 "$RUNS/in_golden.json" "$RUNS/out_b5.md"
if [ "$CRC" -ne 0 ] && has b5 "FAIL T2 touched-file set must be exactly" && has b5 "$OR" && has b5 "stopped at T2"; then ok "B5 rc $CRC: FAIL T2 names $OR"
else bad "B5" "rc $CRC $(res b5) $(firstfail b5)"; fi

echo "--- B6 NEW behaviour (red at the untouched tip)"
run_ck b6 "$RUNS/in_b6.json" "$RUNS/out_b6.md"
if [ "$CRC" -ne 0 ] && has b6 "PASS T4" && has b6 "FAIL T5 GREEN AT THE TIP" && has b6 "RED AT THE TIP: $C13" && has b6 "stopped at T5" && ! has b6 "tamper P1:"; then ok "B6 rc $CRC: FAIL T5 (cell13 red at the tip), no tamper planted"
else bad "B6" "rc $CRC $(res b6) $(firstfail b6)"; fi

echo "--- B7 restore guard"
TIPSHA="$(git -C "$CLONE" show "$TIP:$OR" | shasum -a 256 | cut -c1-64)"
run_ck b7 "$RUNS/in_golden.json" "$RUNS/out_golden.md" TO_TEST_SKIP_RESTORE=P1
NOWSHA="$(shasum -a 256 "$CLONE/$OR" | cut -c1-64)"
if [ "$CRC" -ne 0 ] && has b7 "FAIL T8[P1] RESTORE FAILED" && has b7 "stopped at T8" && ! has b7 "T6[S1]" && [ "$NOWSHA" != "$TIPSHA" ]; then ok "B7 rc $CRC: FAIL T8[P1], stopped before S1; orchestrate.sh really is tampered (${NOWSHA:0:12} != ${TIPSHA:0:12})"
else bad "B7" "rc $CRC $(res b7) now=${NOWSHA:0:12} tip=${TIPSHA:0:12}"; fi
run_ck b7b "$RUNS/in_golden.json" "$RUNS/out_golden.md"
NOWSHA="$(shasum -a 256 "$CLONE/$OR" | cut -c1-64)"
if [ "$CRC" -eq 0 ] && has b7b "RESULT: PASS (8/8)" && [ "$NOWSHA" = "$TIPSHA" ]; then ok "B7b rc 0: the next run's reset restored the clone and the golden PASSES"
else bad "B7b" "rc $CRC $(res b7b) now=${NOWSHA:0:12}"; fi

echo "--- B8 an ambiguous cell name"
run_ck b8 "$RUNS/in_b8.json" "$RUNS/out_golden.md"
if [ "$CRC" -ne 0 ] && has b8 "AMBIGUOUS CELL NAME: the declared name 'an UNREADABLE' matches" && has b8 "stopped at T5"; then ok "B8 rc $CRC: FAIL T5 $(/usr/bin/grep -m1 'AMBIGUOUS' "$RUNS/b8.checker.out" | cut -c1-110)"
else bad "B8" "rc $CRC $(res b8) $(firstfail b8)"; fi

echo "--- B9 FAIL lines with rc 0"
run_ck b9 "$RUNS/in_b9.json" "$RUNS/out_b9.md"
if [ "$CRC" -ne 0 ] && has b9 "PASS T5" && /usr/bin/grep -q '^FAIL T6\[P1\].*EXITED 0' "$RUNS/b9.checker.out"; then ok "B9 rc $CRC: FAIL T6[P1] the suite printed FAIL but EXITED 0"
else bad "B9" "rc $CRC $(res b9) $(firstfail b9)"; fi

echo "--- B10 builder refusals"
for x in a b c d e f g; do
  bash "$BLD" KS-936-ARM "$RUNS/in_refuse_$x.json" "$RUNS/brief_$x.md" > "$RUNS/build_refuse_$x.out" 2>&1
  brc=$?
  if [ "$brc" -eq 2 ] && /usr/bin/grep -q 'REFUSED' "$RUNS/build_refuse_$x.out"; then ok "B10$x builder rc 2: $(head -1 "$RUNS/build_refuse_$x.out" | cut -c1-170)"
  else bad "B10$x" "builder rc $brc: $(head -2 "$RUNS/build_refuse_$x.out")"; fi
done
bash "$BLD" KS-936-GOLDEN "$RUNS/in_golden_again.json" "$FX/bash_brief_ks936.md" > "$RUNS/build_again.out" 2>&1
brc=$?
[ "$brc" -eq 0 ] && ok "B10 control: the golden bash brief builds (rc 0)" || bad "B10 control" "rc $brc"

echo "bash arms: $pass ok, $fail failed (runs in $RUNS)"
[ "$fail" -eq 0 ] && exit 0
exit 1
