#!/bin/bash
# bash_patch2_arms.sh — arms for the multi-file BASH tier (tasks/bash_patch2/) and its lint gate (2026-10-07, rung 3).
#
# A synthetic bash repo is built in a SCRATCH dir (never under !CODING), shaped like KS-1274: scripts/job.sh reads a
# tool's report and says clean|failed (the defect: a report with no `Results` reads clean); scripts/summary.sh maps a
# result to a word (the defect: `failed` is UNKNOWN). Suites in scripts/__tests__: job_loud (MODIFIED, RED: a new 🔴
# cell + a `bare` stub mode + its clean stub), job_stub (MODIFIED, SUPPORT: its clean stub `{}` -> `{"Results":[]}`),
# summary_new (NEW, RED), an undeclared sibling naming job.sh (exit code 1 on an empty report), a reference suite.
# Every arm goes END TO END: a brief is written for the variant, tasks/bash_patch2/build_bash_input2.sh builds the input
# from it (through the unchanged bash_patch builder), and tasks/bash_patch2/checker.sh judges the variant's diff in a
# fresh clone. Expected vs actual is printed for every arm.
#   P1  PASS     the 2-product / 3-test golden (2 RED incl. one NEW, 1 SUPPORT)            -> rc 0, RESULT: PASS, B6 ran
#   F1  FAIL     golden + an UNDECLARED scripts/other.sh section                          -> rc 1, B3 … UNDECLARED
#   F2  FAIL     golden minus the SUPPORT suite's section (declared, UNTOUCHED)           -> rc 1, B3 … UNTOUCHED
#   F3  FAIL     the RED suite's new cell is GREEN before the fix                         -> rc 1, B4 … declared RED but NOT red
#   F4  FAIL     the SUPPORT suite's edit is RED with the test edits alone                -> rc 1, B4 … declared SUPPORT but NOT green
#   F5  FAIL     product 2's fix is wrong: summary_new still red after                    -> rc 1, B5 GREEN-AFTER: still red
#   F6  FAIL     the fix changes the exit code an UNDECLARED sibling pins                 -> rc 1, B6 NEW failure
#   F7  FAIL     one byte of a SUPPORT '+' line differs from the brief (A3c cannot see it) -> rc 1, B3x BYTE IDENTITY
#   F8  FAIL     the output drops a product '+' line the brief adds                       -> rc 1, B3b INCOMPLETE (A3c)
#   F9  FAIL     the output removes a line the brief's `## Where` says STAYS              -> rc 1, B3c … STAYS
#   R1-R5 REFUSE builder: a test line with neither RED nor SUPPORT · a NEW SUPPORT suite · a test hunk under `## The exact
#                change` · a declared file the brief carries no lines for · a declared NEW suite that exists   -> rc 2
#   L1  ACCEPT   brief_lint: the real KS-1274 brief (tier bash_patch2)                    -> rc 0 (the control for L2/L3)
#   L2  REFUSE   brief_lint: the same brief pinned tier=bash_patch (3 tests > 1)          -> rc 2, CONTRACT
#   L3  REFUSE   brief_lint: the same brief with its ref= pin removed                     -> rc 2, PINS
#   T1  task.md  tasks/bash_patch2/make_task.py derives rc 0, and REFUSES rc 2 on a task.md missing an anchor
set -uo pipefail
SPARK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; LM="$(dirname "$SPARK")"
B2="$LM/tasks/bash_patch2"; BUILD="$B2/build_bash_input2.sh"; CHK="$B2/checker.sh"
T="${SPARK_TEST_TMP:-$(mktemp -d "${TMPDIR:-/tmp}/bp2_arms.XXXXXX")}"; mkdir -p "$T"
P=0; F=0
ok()  { echo "ARM PASS $*"; P=$((P+1)); }
bad() { echo "ARM FAIL $*"; F=$((F+1)); }
echo "bash_patch2_arms: fixtures in $T"

# ---------------------------------------------------------------- the synthetic repo + variants (python writes them all)
SYN="$T/syn"; mkdir -p "$SYN"
python3 - "$SYN" "$T" <<'PY' || { echo "bash_patch2_arms: the fixture generator failed — no arm can be judged"; exit 2; }
import os, sys
syn, T = sys.argv[1:3]
os.makedirs(f"{syn}/scripts/__tests__", exist_ok=True)
HEAD = ['#!/bin/bash', 'set -uo pipefail', 'HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; JOB="$HERE/../job.sh"',
        'W="$(mktemp -d "${TMPDIR:-/tmp}/bp2syn.XXXXXX")"; trap \'rm -rf "$W"\' EXIT', 'pass=0; fail=0',
        "ok()  { printf '  ok   %s\\n' \"$1\"; pass=$((pass + 1)); }", "bad() { printf '  FAIL %s\\n' \"$1\"; fail=$((fail + 1)); }"]
TAIL = ["printf '\\n  %d passed, %d failed\\n' \"$pass\" \"$fail\"", '[ "$fail" -eq 0 ] || exit 1', 'exit 0']
tip = {
 "scripts/job.sh": ['#!/bin/bash', '# job: run the tool and say whether its report is clean', 'out="$("${TOOL:-tool}" 2>/dev/null)"',
                    'if [ -z "$out" ]; then echo "failed"; exit 1; fi', 'echo "clean"'],
 "scripts/summary.sh": ['#!/bin/bash', '# summary: one word per job result', 'case "$1" in', '  clean) echo "OK" ;;', '  *) echo "UNKNOWN" ;;', 'esac'],
 "scripts/other.sh": ['#!/bin/bash', 'echo other'],
 "scripts/__tests__/job_loud.test.sh": ['#!/bin/bash', '# job_loud: the job\'s verdict per tool report'] + HEAD[1:] + [
     "CLEAN='{}'",
     'stub() {',
     "  { echo '#!/bin/bash'",
     "    echo 'case \"${MODE:-}\" in'",
     "    echo '  empty) exit 1 ;;'",
     "    echo 'esac'",
     "    echo \"echo '$CLEAN'\"",
     '  } > "$W/tool"; chmod +x "$W/tool"',
     '}',
     'stub',
     'got="$(TOOL="$W/tool" bash "$JOB")"',
     'if [ "$got" = clean ]; then ok "CONTROL a clean report is clean"; else bad "CONTROL a clean report is clean (got $got)"; fi',
     'got="$(MODE=empty TOOL="$W/tool" bash "$JOB")"',
     'if [ "$got" = failed ]; then ok "CONTROL an empty report is failed"; else bad "CONTROL an empty report is failed (got $got)"; fi'] + TAIL,
 "scripts/__tests__/job_stub.test.sh": ['#!/bin/bash', '# job_stub: a clean report exits 0'] + HEAD[1:] + [
     "CLEAN='{}'",
     "printf '#!/bin/bash\\necho %s\\n' \"'$CLEAN'\" > \"$W/tool\"; chmod +x \"$W/tool\"",
     'got="$(TOOL="$W/tool" bash "$JOB")"; rc=$?',
     'if [ "$got $rc" = "clean 0" ]; then ok "CONTROL a clean report exits 0"; else bad "CONTROL a clean report exits 0 (got $got $rc)"; fi'] + TAIL,
 "scripts/__tests__/sibling.test.sh": ['#!/bin/bash', '# sibling: job.sh exits 1 on an empty report'] + HEAD[1:] + [
     "printf '#!/bin/bash\\nexit 1\\n' > \"$W/tool\"; chmod +x \"$W/tool\"",
     'TOOL="$W/tool" bash "$JOB" > /dev/null; rc=$?',
     'if [ "$rc" = 1 ]; then ok "CONTROL an empty report exits 1"; else bad "CONTROL an empty report exits 1 (rc $rc)"; fi'] + TAIL,
 "scripts/__tests__/ref.test.sh": ['#!/bin/bash', '# ref: a reference suite'] + HEAD[1:] + ['ok "CONTROL ref"'] + TAIL,
}
for p, L in tip.items():
    open(f"{syn}/{p}", "w").write("\n".join(L) + "\n")
NEWT = ['#!/bin/bash', '# summary_new: summary names a failed job', 'set -uo pipefail',
        'HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; S="$HERE/../summary.sh"', 'pass=0; fail=0',
        "ok()  { printf '  ok   %s\\n' \"$1\"; pass=$((pass + 1)); }", "bad() { printf '  FAIL %s\\n' \"$1\"; fail=$((fail + 1)); }",
        'if [ "$(bash "$S" failed)" = FAILED ]; then ok "🔴 failed is FAILED"; else bad "🔴 failed is FAILED"; fi',
        'if [ "$(bash "$S" clean)" = OK ]; then ok "CONTROL clean is OK"; else bad "CONTROL clean is OK"; fi'] + TAIL

def hunk(path, start, body):
    L = tip[path]; old = [t for k, t in body if k in " -"]; new = [t for k, t in body if k in " +"]
    for i, t in enumerate(old): assert L[start - 1 + i] == t, (path, start + i, L[start - 1 + i], t)
    return f"@@ -{start},{len(old)} +{start},{len(new)} @@\n" + "".join(k + t + "\n" for k, t in body)
def sec(path, *hunks): return f"--- a/{path}\n+++ b/{path}\n" + "".join(hunks)
def job(guard='if [ -z "$out" ] || ! printf \'%s\' "$out" | grep -q Results; then echo "failed"; exit 1; fi', comment=True, keep_stays=True):
    b = [(" ", '# job: run the tool and say whether its report is clean')]
    b += [(" ", 'out="$("${TOOL:-tool}" 2>/dev/null)"')] if keep_stays else [("-", 'out="$("${TOOL:-tool}" 2>/dev/null)"'), ("+", 'out="$("${TOOL:-tool}")"')]
    b += [("-", 'if [ -z "$out" ]; then echo "failed"; exit 1; fi')]
    b += [("+", '# a report with no Results is not a scan')] if comment else []
    b += [("+", guard), (" ", 'echo "clean"')]
    return sec("scripts/job.sh", hunk("scripts/job.sh", 2, b))
def summary(word="FAILED"):
    return sec("scripts/summary.sh", hunk("scripts/summary.sh", 3, [(" ", 'case "$1" in'), (" ", '  clean) echo "OK" ;;'),
               ("+", f'  failed) echo "{word}" ;;'), (" ", '  *) echo "UNKNOWN" ;;'), (" ", 'esac')]))
LT = tip["scripts/__tests__/job_loud.test.sh"]
def loud(red_ok_word="failed"):
    i = LT.index("CLEAN='{}'") + 1
    h1 = hunk("scripts/__tests__/job_loud.test.sh", i, [("-", "CLEAN='{}'"), ("+", "CLEAN='{\"Results\":[]}'"), (" ", 'stub() {'),
              (" ", "  { echo '#!/bin/bash'"), (" ", "    echo 'case \"${MODE:-}\" in'"), (" ", "    echo '  empty) exit 1 ;;'"),
              ("+", "    echo '  bare) echo \"{}\"; exit 0 ;;'"), (" ", "    echo 'esac'")])
    j = LT.index('got="$(MODE=empty TOOL="$W/tool" bash "$JOB")"') + 1
    h2 = hunk("scripts/__tests__/job_loud.test.sh", j, [(" ", LT[j - 1]), (" ", LT[j]),
              ("+", 'got="$(MODE=bare TOOL="$W/tool" bash "$JOB")"'),
              ("+", f'if [ "$got" = {red_ok_word} ]; then ok "🔴 a bare {{}} report is failed"; else bad "🔴 a bare {{}} report is failed (got $got)"; fi'),
              (" ", TAIL[0])])
    # the second hunk's new-side start moves by the first hunk's +1 line
    h2 = h2.replace(f"+{j},", f"+{j + 1},", 1)
    return sec("scripts/__tests__/job_loud.test.sh", h1, h2)
ST = tip["scripts/__tests__/job_stub.test.sh"]
def stub(clean="CLEAN='{\"Results\":[]}'"):
    i = ST.index("CLEAN='{}'") + 1
    return sec("scripts/__tests__/job_stub.test.sh", hunk("scripts/__tests__/job_stub.test.sh", i - 1,
               [(" ", ST[i - 2]), ("-", "CLEAN='{}'"), ("+", clean), (" ", ST[i])]))
def newt():
    return "--- /dev/null\n+++ b/scripts/__tests__/summary_new.test.sh\n" + f"@@ -0,0 +1,{len(NEWT)} @@\n" + "".join("+" + l + "\n" for l in NEWT)
other = sec("scripts/other.sh", hunk("scripts/other.sh", 2, [("-", "echo other"), ("+", "echo other2")]))
G = dict(job=job(), summary=summary(), loud=loud(), stub=stub(), new=newt())
V = {  # variant: (brief parts, output parts)
 "golden": (G, G),
 "undeclared": (G, dict(G, other=other)),
 "untouched": (G, {k: v for k, v in G.items() if k != "stub"}),
 "greenbefore": (dict(G, loud=loud("clean")), dict(G, loud=loud("clean"))),
 "supportred": (dict(G, stub=stub("CLEAN=''")), dict(G, stub=stub("CLEAN=''"))),
 "stillred": (dict(G, summary=summary("FAIL")), dict(G, summary=summary("FAIL"))),
 "sibbreak": (dict(G, job=job(guard='if [ -z "$out" ] || ! printf \'%s\' "$out" | grep -q Results; then echo "failed"; exit 2; fi')),) * 2,
 "bytemut": (G, dict(G, stub=stub("CLEAN='{\"Results\": []}'"))),
 "dropadd": (G, dict(G, job=job(comment=False))),
 "staysgone": (G, dict(G, job=job(keep_stays=False))),
}
ORDER = ["job", "summary", "loud", "stub", "new", "other"]
HDR = ("File: `scripts/job.sh`\nFile: `scripts/summary.sh`\n"
       "Test file: `scripts/__tests__/job_loud.test.sh`  (MODIFIED, RED)\n"
       "Test stub: `scripts/__tests__/job_stub.test.sh`  (MODIFIED, SUPPORT)\n"
       "Test file: `scripts/__tests__/summary_new.test.sh`  (NEW, RED)\n")
def brief(parts, hdr=HDR, test_in_change=False, drop_new_block=False):
    prod = "".join(parts[k] for k in ("job", "summary"))
    tst = "".join(parts[k] for k in ("loud", "stub"))
    if test_in_change: prod += tst; tst = ""
    newblk = "" if drop_new_block else ("File: `scripts/__tests__/summary_new.test.sh`\n\n```bash\n" + "\n".join(NEWT) + "\n```\n\n")
    return ("# KS-9 synthetic — bash_patch2 arm\n\n" + hdr + "Tip: `@TIP@`\nRunner: `bash`\nTier: `bash_patch2`\n\n"
            "## The mode\n\nFive files.\n\n## What is wrong\n\nA report with no Results reads clean; summary says UNKNOWN for failed.\n\n"
            "## Where\n\n- `:3` — (correct) the read of the tool's report stays.\n- `:4` — **the guard**\n\n"
            "## The exact change\n\n```diff\n" + prod + "```\n\n## The test\n\n" + ("```diff\n" + tst + "```\n\n" if tst else "") + newblk +
            "## UNMEASURED\n\nnone (synthetic)\n\n## Scope\n\nsynthetic\n\n## Output\n\nOne diff.\n")
for name, (bp, op) in V.items():
    os.makedirs(f"{T}/{name}", exist_ok=True)
    open(f"{T}/{name}/brief.md", "w").write(brief(bp))
    open(f"{T}/{name}/out.md", "w").write("```diff\n" + "".join(op[k] for k in ORDER if k in op) + "```\n")
# builder refusals
R = {
 "R1-no-role": brief(G, hdr=HDR.replace("(MODIFIED, SUPPORT)", "(MODIFIED)")),
 "R2-new-support": brief(G, hdr=HDR.replace("(NEW, RED)", "(NEW, SUPPORT)")),
 "R3-test-in-change": brief(G, test_in_change=True),
 "R4-no-lines": brief(G, drop_new_block=True),
 "R5-new-exists": brief(G, hdr=HDR.replace("job_loud.test.sh`  (MODIFIED, RED)", "job_loud.test.sh`  (NEW, RED)")),
}
for name, b in R.items():
    os.makedirs(f"{T}/{name}", exist_ok=True); open(f"{T}/{name}/brief.md", "w").write(b)
print("fixtures written:", len(V), "variants,", len(R), "refusal briefs")
PY
git -C "$SYN" init -q -b develop && git -C "$SYN" add -A && git -C "$SYN" -c user.name=arms -c user.email=arms@local commit -q -m "synthetic tip" \
  && git -C "$SYN" remote add origin "$SYN" || { echo "bash_patch2_arms: could not build the synthetic repo"; exit 2; }
TIP="$(git -C "$SYN" rev-parse HEAD)"
for b in "$T"/*/brief.md; do sed -i '' "s/@TIP@/$TIP/" "$b"; done
REF="scripts/__tests__/ref.test.sh"

build() { # build <dir> -> rc of the builder; input at <dir>/input.json
  NIGHT_SOURCE_CHECKOUT="$SYN" bash "$BUILD" KS-9 "$1/input.json" "$1/brief.md" "ref=$REF" > "$1/build.out" 2>&1
}
arm() { # arm <name> <variant> <want rc> <substring>
  local name="$1" v="$2" want="$3" sub="$4" W="$T/$2"
  build "$W"; local brc=$?
  if [ "$brc" -ne 0 ]; then bad "$name builder rc=$brc (want 0): $(tail -2 "$W/build.out" | tr '\n' ' ')"; return; fi
  git clone -q "$SYN" "$W/clone" && git -C "$W/clone" checkout -q --detach "$TIP"
  bash "$CHK" "$W/input.json" "$W/out.md" "$W/clone" > "$W/checker.out" 2>&1; local rc=$?
  local res; res="$(grep -m1 '^RESULT:' "$W/checker.out")"
  local why; why="$(grep -E '^FAIL ' "$W/checker.out" | head -1 | cut -c1-220)"
  if [ "$rc" -eq "$want" ] && grep -qF -- "$sub" "$W/checker.out"; then ok "$name :: expected rc=$want '$sub' :: actual rc=$rc :: $res${why:+ :: $why}"
  else bad "$name :: expected rc=$want '$sub' :: actual rc=$rc :: $res :: $why (full: $W/checker.out)"; fi
}
arm P1-golden-pass golden 0 "RESULT: PASS ("
grep -E '^(PASS|FAIL|INFO) B|^RESULT' "$T/golden/checker.out" | cut -c1-200 | sed 's/^/    P1: /'
grep -qF 'PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (2 suite(s): ref.test.sh 1p/0f->1p/0f; sibling.test.sh 1p/0f->1p/0f;)' "$T/golden/checker.out" \
  && ok "P1b B6 RAN on the 2 undeclared suites naming the stem 'job' (sibling + ref; a B6 that never runs could not fail F6)" || bad "P1b B6 did not run as expected: $(grep -m1 'B6' "$T/golden/checker.out")"
arm F1-undeclared undeclared 1 "touched but UNDECLARED: ['scripts/other.sh']"
arm F2-untouched untouched 1 "declared but UNTOUCHED: ['scripts/__tests__/job_stub.test.sh']"
arm F3-red-green-before greenbefore 1 "job_loud.test.sh: declared RED but NOT red before the product sections"
arm F4-support-red-alone supportred 1 "job_stub.test.sh: declared SUPPORT but NOT green with the test edits alone"
arm F5-still-red-after stillred 1 "FAIL B5 GREEN-AFTER: still red (or empty) after the product sections: summary_new.test.sh"
arm F6-sibling-new-red sibbreak 1 "FAIL B6 NEW failure(s) in undeclared sibling suite(s) after the patch: scripts/__tests__/sibling.test.sh(before=0 after=1)"
arm F7-byte-identity bytemut 1 "FAIL B3x BYTE IDENTITY — DIFF scripts/__tests__/job_stub.test.sh"
arm F8-dropped-addition dropadd 1 "FAIL B3b INCOMPLETE (A3c): 1 of 3 brief '+' line(s) ABSENT"
arm F9-stays-removed staysgone 1 "FAIL B3c a line the brief says STAYS was removed from job.sh"

# ---------------------------------------------------------------- builder refusals
for r in R1-no-role:"exactly one of RED / SUPPORT" R2-new-support:"is NEW but SUPPORT" R3-test-in-change:"which is not a declared product" \
         R4-no-lines:"carries no lines for the declared file scripts/__tests__/summary_new.test.sh" R5-new-exists:"is declared NEW but is present at the tip"; do
  n="${r%%:*}"; s="${r#*:}"; build "$T/$n"; rc=$?
  if [ "$rc" -eq 2 ] && grep -qF -- "$s" "$T/$n/build.out"; then ok "$n :: expected rc=2 '$s' :: actual rc=$rc :: $(grep -m1 REFUSED "$T/$n/build.out" | cut -c1-170)"
  else bad "$n :: expected rc=2 '$s' :: actual rc=$rc :: $(tail -2 "$T/$n/build.out" | tr '\n' ' ')"; fi
done
# the refusals' control: the golden brief BUILT (P1 above) — and its input carries the declared roles
python3 - "$T/golden/input.json" <<'PY' && ok "R0 control: the golden brief builds rc 0 with task_type bash_patch2, 2 products, roles red/support/red" || bad "R0 the golden input is not the declared set"
import json, sys
d = json.load(open(sys.argv[1]))
assert d["task_type"] == "bash_patch2"
assert d["product_files"] == ["scripts/job.sh", "scripts/summary.sh"]
assert [(t["path"].rsplit("/", 1)[-1], t["status"], t["role"]) for t in d["test_files"]] == [("job_loud.test.sh", "modified", "red"), ("job_stub.test.sh", "modified", "support"), ("summary_new.test.sh", "new", "red")]
assert "scripts/summary.sh" in d["files"] and "scripts/__tests__/job_stub.test.sh" in d["files"]
assert d["ticket"]["description"].startswith("# KS-9 synthetic")
PY

# ---------------------------------------------------------------- lint arms (the real KS-1274 brief)
BR="$LM/night/briefs/KS-1274-trivy-bare-object"
o="$(python3 "$SPARK/brief_lint.py" "$BR" 2>&1)"; r=$?
[ "$r" -eq 0 ] && echo "$o" | grep -q "^B_TIER=bash_patch2" && ok "L1 control :: expected rc=0 B_TIER=bash_patch2 :: actual rc=$r" || bad "L1 :: actual rc=$r $o"
o="$(python3 "$SPARK/brief_lint.py" "$BR" tier=bash_patch 2>&1)"; r=$?
[ "$r" -eq 2 ] && echo "$o" | grep -q 'CONTRACT' && ok "L2 :: expected rc=2 CONTRACT :: actual rc=$r :: $(echo "$o" | grep -m1 CONTRACT | cut -c1-150)" || bad "L2 :: actual rc=$r $o"
mkdir -p "$T/L3"; cp "$BR/KS-1274.md" "$T/L3/"
o="$(python3 "$SPARK/brief_lint.py" "$T/L3" 2>&1)"; r=$?
[ "$r" -eq 2 ] && echo "$o" | grep -q 'PINS' && ok "L3 :: expected rc=2 PINS :: actual rc=$r :: $(echo "$o" | grep -m1 PINS | cut -c1-120)" || bad "L3 :: actual rc=$r $o"

# ---------------------------------------------------------------- make_task.py derivation + its refusal
o="$(python3 "$B2/make_task.py" "$T/task.md" 2>&1)"; r=$?
[ "$r" -eq 0 ] && grep -q '^3. BASH_PATCH2 (multi-file)' "$T/task.md" && ! grep -q 'touches EXACTLY two files' "$T/task.md" \
  && ok "T1 make_task.py :: expected rc=0, rule 3 replaced :: actual rc=$r" || bad "T1 make_task.py rc=$r $o"
mkdir -p "$T/mt/bash_patch2" "$T/mt/bash_patch"; cp "$B2/make_task.py" "$T/mt/bash_patch2/"
sed 's/touches EXACTLY two files/touches EXACTLY 2 files/' "$LM/tasks/bash_patch/task.md" > "$T/mt/bash_patch/task.md"
o="$(python3 "$T/mt/bash_patch2/make_task.py" "$T/mt/task.md" 2>&1)"; r=$?
[ "$r" -eq 2 ] && echo "$o" | grep -q 'REFUSED' && ok "T2 make_task.py on a task.md with a moved anchor :: expected rc=2 :: actual rc=$r" || bad "T2 rc=$r $o"

echo "bash_patch2_arms: $P pass, $F fail (fixtures $T)"
[ "$F" -eq 0 ]
