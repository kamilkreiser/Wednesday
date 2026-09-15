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
OLD=$LM/tasks/code_patch/reanchor.py.pre-0916-minuschain
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
cp "$RUN/out.md.checker/section_1.diff" "$W/real.diff"

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

echo "reanchor_minuschain_arms: $PASS passed, $FAIL failed (work dir kept: $W)"
[ "$FAIL" -eq 0 ] || exit 1
exit 0
