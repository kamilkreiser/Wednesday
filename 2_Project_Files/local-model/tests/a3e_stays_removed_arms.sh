#!/bin/bash
# a3e_stays_removed_arms.sh — red-proof for code_patch checker A3e (2026-09-16): a "(correct) … stays" site removed
# by the product hunk ('-' with no matching '+') is REFUSED; a rewrite that removes AND re-adds it is not. The arms
# run the checker's OWN A3e predicate (extracted by its PY3E marker, never re-implemented) on REAL run artefacts.
#   ARM1 KS-1121 r2 retry (a whole-function rewrite; :235 stays untouched)                     → empty
#   ARM2 KS-975 item 2 (one replacement; :225/:227/:232/:234/:86 stays kept as context)          → empty
#   ARM3 a SYNTHETIC section removing KS-1121's :235 `const credential = await getById(id);`     → REMOVED
#   ARM4 the same line removed AND re-added (a rewrite)                                          → empty
#   ARM5 the OLD checker (.pre-0916-a3e) carries no A3e marker                                    → control
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CK=$LM/tasks/code_patch/checker.sh
SP="${A3E_SCRATCH:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/5bad346c-a054-4ac3-af91-9a46b788ea63/scratchpad/a3e}"
mkdir -p "$SP"
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }; bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
PRED="$(awk 'index($0,"A3E_REMOVED=\"$(python3 - ")>0{f=1;next} f && $0=="PY3E"{exit} f' "$CK")"
[ -n "$PRED" ] || { echo "FATAL: could not extract the A3e predicate from $CK"; exit 2; }
run_pred(){ python3 -c "$PRED" "$1" "$2"; }
sec_of(){ # run-dir → the product section file (reanchored if present)
  local d="$1/out.md.checker"; [ -f "$d/section_1.reanchored.diff" ] && echo "$d/section_1.reanchored.diff" || echo "$d/section_1.diff"; }
R1121=$LM/runs/2026-09-16_ks1121-ornith35b-night2/retry
R975=$LM/runs/2026-09-16_ks975-ornith35b-night2
out="$(run_pred "$R1121/../input.json" "$(sec_of "$R1121")")"; [ -z "$out" ] && ok "ARM1 KS-1121 r2 retry → nothing removed" || bad "ARM1" "$out"
out="$(run_pred "$R975/input.json" "$(sec_of "$R975")")"; [ -z "$out" ] && ok "ARM2 KS-975 item 2 → nothing removed" || bad "ARM2" "$out"
printf -- '--- a/x.ts\n+++ b/x.ts\n@@ -234,3 +234,2 @@\n   reason?: string,\n-  const credential = await getById(id);\n   if (!credential) return undefined;\n' > "$SP/synthetic_removed.diff"
out="$(run_pred "$R1121/../input.json" "$SP/synthetic_removed.diff")"; [ -n "$out" ] && ok "ARM3 synthetic removal of :235 → REMOVED: $(printf '%s' "$out" | cut -c1-60)" || bad "ARM3" "predicate printed nothing"
printf -- '--- a/x.ts\n+++ b/x.ts\n@@ -234,3 +234,3 @@\n   reason?: string,\n-  const credential = await getById(id);\n+  const credential = await getById(id);\n   if (!credential) return undefined;\n' > "$SP/synthetic_rewrite.diff"
out="$(run_pred "$R1121/../input.json" "$SP/synthetic_rewrite.diff")"; [ -z "$out" ] && ok "ARM4 removed AND re-added → nothing removed" || bad "ARM4" "$out"
if ! grep -q 'A3E_REMOVED' "$CK.pre-0916-a3e" && grep -q 'A3E_REMOVED' "$CK"; then ok "ARM5 the OLD checker has no A3e; the new one does"; else bad "ARM5" "marker presence unexpected"; fi
echo "a3e arms: $pass passed, $fail failed"
[ "$fail" -eq 0 ]
