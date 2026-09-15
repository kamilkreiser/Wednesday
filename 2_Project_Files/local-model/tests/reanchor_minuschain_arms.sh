#!/bin/bash
# reanchor_minuschain_arms.sh — red-proof for reanchor.py's rebuild_from_minus (2026-09-16 06:1x, KS-958 r1):
# a REPLACEMENT hunk whose '-' lines are byte-exact in the file but whose LEADING CONTEXT line is a truncated
# copy of a tip line — the whole-old-side anchor has no first line, so before this mode the hunk was
# "kept as written" and a correct product hunk was a false FAIL at B2.
# Arms (all on the tip guard at 48e65c435, git show read-only; the scratch dir is left in place):
#   1 REAL   — the KS-958 r1 section_1.diff → reanchors, `git apply --check` passes, the applied file is
#              BYTE-IDENTICAL to the hand-made golden (tolower on :338 and :342, nothing else)
#   2 OLD    — the .pre-0916-minuschain script on the same input → "kept as written" (the defect; the control
#              that proves arm 1 measures the change)
#   3 INSERT — the same mangled context with a '+' group that follows a CONTEXT line, not a '-' → refused
#              (an insert's placement is the context's, which is what cannot be trusted)
#   4 AMBIG  — a '-' line that occurs twice in the file with no second '-' to disambiguate → refused
#   5 ZERO   — a '-' line that occurs 0x → refused
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
REAN=${REAN:-$LM/tasks/code_patch/reanchor.py}
OLD=$LM/tasks/code_patch/reanchor.py.pre-0916-minuschain   # arms 2/8b use the script as it was BEFORE this morning (both defects present)
RUN=$LM/runs/2026-09-16_ks958-ornith35b-night
SRC="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
TIP=48e65c435
W=$(mktemp -d /tmp/reanchor_minuschain.XXXXXX)
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "ARM PASS $1"; }
bad() { FAIL=$((FAIL+1)); echo "ARM FAIL $1"; }

git -C "$SRC" show "$TIP:Blockchain/Dev/scripts/check-shared-relink.sh" > "$W/tip.sh"
# the golden: exactly the two tolower edits by sed on the tip
sed -e '338s/if (L ~ \/node_modules|npm|npx|yarn|pnpm\/)/if (tolower(L) ~ \/node_modules|npm|npx|yarn|pnpm\/)/' \
    -e '342s/else if (L ~ /else if (tolower(L) ~ /' "$W/tip.sh" > "$W/golden.sh"
[ "$(diff "$W/tip.sh" "$W/golden.sh" | grep -c '^[<>]')" = 4 ] || { echo "SETUP FAIL: golden is not a 2-line change"; exit 1; }
# the model's hunk comes from the IMMUTABLE out.md — the checker writes its REANCHORED result back over
# section_1.diff at every run (the .as-written copy sits beside it), so that file is a mutated artefact
awk '/^```diff/{f=1;next} /^```$/{f=0} f' "$RUN/out.md" | awk 'BEGIN{p=1} /^--- \/dev\/null/{p=0} p' > "$W/real.diff"
grep -q '^--- a/Blockchain/Dev/scripts/check-shared-relink.sh' "$W/real.diff" && grep -q "reproduced, in the round" "$W/real.diff" || { echo "SETUP FAIL: real.diff is not the model's product section from out.md"; exit 1; }

apply_check() { # $1 diff → prints the applied file at $2 (a fresh git repo in $W so `git apply` has a tree), rc of --check
  local d=$1 outf=$2 r; r=$(mktemp -d "$W/repo.XXXXXX")
  mkdir -p "$r/Blockchain/Dev/scripts"; cp "$W/tip.sh" "$r/Blockchain/Dev/scripts/check-shared-relink.sh"
  git -C "$r" init -q && git -C "$r" add -A && git -C "$r" -c user.email=a@b -c user.name=arm commit -qm tip
  if git -C "$r" apply --check "$d" 2>"$W/apply.err" && git -C "$r" apply "$d" 2>>"$W/apply.err"; then
    cp "$r/Blockchain/Dev/scripts/check-shared-relink.sh" "$outf"; return 0
  fi
  return 1
}

# ARM 1 — the real r1 hunk under the NEW script
python3 "$REAN" "$W/real.diff" "$W/tip.sh" "$W/real.rean.diff" > "$W/real.rean.out" 2>&1 || { bad "1 REAL: reanchor rc"; }
if grep -q "reanchored on the '-' LINES" "$W/real.rean.out" && apply_check "$W/real.rean.diff" "$W/real.applied.sh" && cmp -s "$W/real.applied.sh" "$W/golden.sh"; then
  ok "1 REAL: reanchored on the '-' lines, applies, applied == golden byte-for-byte"
else
  bad "1 REAL: $(cat "$W/real.rean.out" | tr '\n' ' ' | cut -c1-200) apply.err=$(cat "$W/apply.err" 2>/dev/null | head -2 | tr '\n' ' ')"
fi

# ARM 2 — the OLD script on the same input: kept as written (the control)
python3 "$OLD" "$W/real.diff" "$W/tip.sh" "$W/old.rean.diff" > "$W/old.rean.out" 2>&1
if grep -q "kept as written" "$W/old.rean.out" && ! apply_check "$W/old.rean.diff" "$W/old.applied.sh"; then
  ok "2 OLD: the pre-0916 script keeps the hunk as written and it does not apply (the defect reproduced)"
else
  bad "2 OLD: $(cat "$W/old.rean.out" | tr '\n' ' ' | cut -c1-200)"
fi

# ARM 3 — INSERT: the real two-run hunk (so the contiguous path has 0 hits and the old-side anchor fails on the
# mangled leading context) PLUS a '+' line right after the FIRST context line → reaches rebuild_from_minus and is refused
python3 - "$W/real.diff" "$W/insert.diff" <<'PY2'
import sys
L=open(sys.argv[1],encoding="utf-8").read().split("\n")
out=[]; done=False
for l in L:
    out.append(l)
    if not done and l.startswith("         # reproduced, in the round"):
        out.append("+        # an inserted comment with no '-' before it"); done=True
open(sys.argv[2],"w",encoding="utf-8").write("\n".join(out))
PY2
python3 "$REAN" "$W/insert.diff" "$W/tip.sh" "$W/insert.rean.diff" > "$W/insert.rean.out" 2>&1
if grep -q "kept as written" "$W/insert.rean.out" && ! grep -q "reanchored on the '-' LINES" "$W/insert.rean.out"; then ok "3 INSERT: a '+' after a context line is refused (kept as written)"; else bad "3 INSERT: $(cat "$W/insert.rean.out" | tr '\n' ' ' | cut -c1-200)"; fi

# ARM 4 — AMBIG: two '-' RUNS (nodeish[stage] = 1 … then the closing brace two lines on) that chain at :339→:341 AND
# :343→:345 — non-contiguous (0 contiguous hits), mangled leading context (old-side None), chain not unique → refused
python3 - "$W/ambig.diff" <<'PY2'
import sys
body="""--- a/Blockchain/Dev/scripts/check-shared-relink.sh
+++ b/Blockchain/Dev/scripts/check-shared-relink.sh
@@ -338,4 +338,4 @@
         # a leading context line that is NOT in the file
-          nodeish[stage] = 1
+          nodeish[stage] = 2
           if (nodeish_hit[stage] == "") nodeish_hit[stage] = L
-        }
+        };
"""
open(sys.argv[1],"w",encoding="utf-8").write(body)
PY2
python3 "$REAN" "$W/ambig.diff" "$W/tip.sh" "$W/ambig.rean.diff" > "$W/ambig.rean.out" 2>&1
if grep -q "not unique, kept as written" "$W/ambig.rean.out" && ! grep -q "reanchored on the '-' LINES" "$W/ambig.rean.out"; then ok "4 AMBIG: a '-' chain occurring twice is refused by name"; else bad "4 AMBIG: $(cat "$W/ambig.rean.out" | tr '\n' ' ' | cut -c1-200)"; fi

# ARM 5 — ZERO: a '-' line that is not in the file at all
python3 - "$W/zero.diff" <<'PY'
import sys
body="""--- a/Blockchain/Dev/scripts/check-shared-relink.sh
+++ b/Blockchain/Dev/scripts/check-shared-relink.sh
@@ -337,3 +337,3 @@
         # a leading context line that is NOT in the file
-        if (L ~ /this line is not in the guard at all/) {
+        if (tolower(L) ~ /this line is not in the guard at all/) {
         }
"""
open(sys.argv[1],"w",encoding="utf-8").write(body)
PY
python3 "$REAN" "$W/zero.diff" "$W/tip.sh" "$W/zero.rean.diff" > "$W/zero.rean.out" 2>&1
if grep -q "occur 0x in the file; kept as written" "$W/zero.rean.out"; then ok "5 ZERO: a '-' line absent from the file is refused"; else bad "5 ZERO: $(cat "$W/zero.rean.out" | tr '\n' ' ' | cut -c1-160)"; fi

# ARM 6 — INDENT-SHIFT (KS-884 r2, IMPROVEMENTS rows 110/111): the model indented every line of the hunk by +4 on
# `.githooks/pre-push`; the '-' lines chain with indent ignored at ONE constant delta → shifted, applies, and the
# applied hook's replaced lines carry the FILE's indent (4), never the model's (8)
R884=$LM/runs/2026-09-16_ks884-ornith35b-night2
git -C "$SRC" show "$TIP:.githooks/pre-push" > "$W/hook_tip.sh"
awk '/^```diff/{f=1;next} /^```$/{f=0} f' "$R884/out.md" | awk 'BEGIN{p=1} /^--- \/dev\/null/{p=0} p' > "$W/hook.real.diff"
python3 "$REAN" "$W/hook.real.diff" "$W/hook_tip.sh" "$W/hook.rean.diff" > "$W/hook.rean.out" 2>&1
hr=$(mktemp -d "$W/hookrepo.XXXXXX"); mkdir -p "$hr/.githooks"; cp "$W/hook_tip.sh" "$hr/.githooks/pre-push"
git -C "$hr" init -q && git -C "$hr" add -A && git -C "$hr" -c user.email=a@b -c user.name=arm commit -qm tip
if grep -q "INDENT SHIFT -4" "$W/hook.rean.out" && git -C "$hr" apply --check "$W/hook.rean.diff" 2>"$W/hook.apply.err" && git -C "$hr" apply "$W/hook.rean.diff" 2>>"$W/hook.apply.err" \
   && [ "$(grep -c "^        _refs='refs/heads/develop" "$hr/.githooks/pre-push")" = 0 ] && [ "$(grep -c "^    _refs='refs/heads/develop" "$hr/.githooks/pre-push")" = 1 ] \
   && [ "$(grep -c "^    _refs='develop origin/develop" "$hr/.githooks/pre-push")" = 0 ]; then
  ok "6 INDENT-SHIFT: KS-884 r2 shifted -4, applies, replaced lines at the file's indent (4 not 8)"
else
  bad "6 INDENT-SHIFT: $(cat "$W/hook.rean.out" | tr '\n' ' ' | cut -c1-200) apply.err=$(head -2 "$W/hook.apply.err" 2>/dev/null | tr '\n' ' ')"
fi

# ARM 7 — a NON-CONSTANT shift (one '-' line at +4, another at +8) → refused by name
python3 - "$W/nonconst.diff" <<'PY2'
import sys
body="""--- a/.githooks/pre-push
+++ b/.githooks/pre-push
@@ -159,4 +159,4 @@
        # a leading context line that is NOT in the file
-        _refs='develop origin/develop refs/remotes/origin/develop'
+        _refs='develop refs/heads/develop refs/remotes/origin/develop'
-            if git rev-parse --verify --quiet develop >/dev/null 2>&1 &&
+            if git rev-parse --verify --quiet refs/heads/develop >/dev/null 2>&1 &&
"""
open(sys.argv[1],"w",encoding="utf-8").write(body)
PY2
python3 "$REAN" "$W/nonconst.diff" "$W/hook_tip.sh" "$W/nonconst.rean.diff" > "$W/nonconst.rean.out" 2>&1
if grep -q "shift is not constant" "$W/nonconst.rean.out" && ! grep -q "INDENT SHIFT" "$W/nonconst.rean.out"; then ok "7 NONCONST: a non-constant indent shift is refused by name"; else bad "7 NONCONST: $(cat "$W/nonconst.rean.out" | tr '\n' ' ' | cut -c1-200)"; fi

# ARM 8 — SPLIT GROUPS (KS-1089 r1): a hunk whose two '+' lines sit INSIDE an if/else with context between them and
# whose one '-' sits after the `fi` — the applied file must carry each assignment in its OWN branch, and the old
# script's collapse (both after the `fi`) must be the negative
R1089=$LM/runs/2026-09-16_ks1089-ornith35b-night
git -C "$SRC" show "$TIP:Blockchain/Dev/scripts/run-shell-suites.sh" > "$W/runner_tip.sh"
awk '/^```diff/{f=1;next} /^```$/{f=0} f' "$R1089/out.md" | awk 'BEGIN{p=1} /^--- \/dev\/null/{p=0} p' > "$W/runner.real.diff"
order_ok() { # $1 file → the printed-nothing assignment comes right after its state line, the GIT_DIR one right after ITS state line
  python3 - "$1" <<'PY3'
import sys
L=[l.strip() for l in open(sys.argv[1]).read().split("\n")]
try:
    i=L.index('git_env_state="printed nothing"'); j=L.index('git_env_state="printed a list with $git_env_total usable name(s), GIT_DIR absent"')
except ValueError: sys.exit(1)
ok = L[i+1].startswith('git_env_headline="FAIL — could not ask') and L[j+1].startswith('git_env_headline="FAIL — git listed')
sys.exit(0 if ok else 1)
PY3
}
for which in NEW OLD; do
  [ $which = NEW ] && SCR=$REAN || SCR=$OLD
  python3 "$SCR" "$W/runner.real.diff" "$W/runner_tip.sh" "$W/runner.$which.diff" > "$W/runner.$which.out" 2>&1
  rr=$(mktemp -d "$W/runnerrepo.XXXXXX"); mkdir -p "$rr/Blockchain/Dev/scripts"; cp "$W/runner_tip.sh" "$rr/Blockchain/Dev/scripts/run-shell-suites.sh"
  git -C "$rr" init -q && git -C "$rr" add -A && git -C "$rr" -c user.email=a@b -c user.name=arm commit -qm tip
  git -C "$rr" apply "$W/runner.$which.diff" 2>"$W/runner.$which.err"; ap=$?
  if [ $which = NEW ]; then
    if [ $ap = 0 ] && order_ok "$rr/Blockchain/Dev/scripts/run-shell-suites.sh" && grep -q "split -/+ groups: positions kept" "$W/runner.NEW.out"; then ok "8 SPLIT-GROUPS: each headline assignment sits in its own branch (positions kept)"; else bad "8 SPLIT-GROUPS: apply=$ap $(cat "$W/runner.NEW.out" | tr '\n' ' ' | cut -c1-200)"; fi
  else
    if [ $ap = 0 ] && ! order_ok "$rr/Blockchain/Dev/scripts/run-shell-suites.sh"; then ok "8b OLD control: the pre-splitgroups script collapses both assignments after the fi (the defect reproduced)"; else bad "8b OLD control: apply=$ap order_ok=$(order_ok "$rr/Blockchain/Dev/scripts/run-shell-suites.sh" && echo yes || echo no)"; fi
  fi
done

echo "reanchor_minuschain_arms: $PASS passed, $FAIL failed (work dir kept: $W)"
[ "$FAIL" -eq 0 ] || exit 1
exit 0
