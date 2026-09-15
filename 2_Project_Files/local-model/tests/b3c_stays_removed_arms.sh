#!/bin/bash
# b3c_stays_removed_arms.sh — red-proof for bash_patch checker B3c (2026-09-16): a "(correct) … stays" site
# appearing as a '-' line in the product section is REFUSED. Arms run the checker's OWN B3c predicate
# (extracted from checker.sh by its marker, never re-implemented) on REAL run artefacts.
#   ARM1 KS-1093 r1 (the real false green: :321 removed by the insert-after dialect) → REMOVED (non-empty)
#   ARM2 KS-1047 r1 (a one-line replacement; every (correct) site untouched)          → empty
#   ARM3 KS-1127 r1 (a multi-edit rewrite)                                            → empty
#   ARM4 the OLD checker (.pre-0916-b3c) carries no B3c marker                         → control: the predicate is new
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CK=$LM/tasks/bash_patch/checker.sh
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }; bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
PRED="$(awk 'index($0,"REMOVED_STAYS=\"$(python3 - ")==1{f=1;next} f && $0=="PY"{exit} f' "$CK")"
[ -n "$PRED" ] || { echo "FATAL: could not extract the B3c predicate from $CK"; exit 2; }
run_pred(){ python3 -c "$PRED" "$1" "$2"; }
arm(){ # name run-dir expect(empty|nonempty)
  local in="$LM/runs/$2/input.json" sec="$LM/runs/$2/out.md.checker/section_1.diff"
  [ -f "$in" ] && [ -f "$sec" ] || { bad "$1" "artefact missing: $in / $sec"; return; }
  local out; out="$(run_pred "$in" "$sec")"
  case "$3" in
    nonempty) [ -n "$out" ] && ok "$1 → REMOVED: $(printf '%s' "$out" | head -1 | cut -c1-70)" || bad "$1" "predicate printed nothing";;
    empty)    [ -z "$out" ] && ok "$1 → nothing removed" || bad "$1" "predicate printed: $out";;
  esac
}
arm "ARM1 KS-1093 r1 real output" 2026-09-16_ks1093-ornith35b-night nonempty
arm "ARM2 KS-1047 r1 real output" 2026-09-16_ks1047-ornith35b-night empty
arm "ARM3 KS-1127 r1 real output" 2026-09-16_ks1127-ornith35b-night empty
if ! grep -q 'REMOVED_STAYS' "$CK.pre-0916-b3c" && grep -q 'REMOVED_STAYS' "$CK"; then ok "ARM4 the OLD checker has no B3c; the new one does"; else bad "ARM4" "marker presence unexpected"; fi
echo "b3c arms: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
