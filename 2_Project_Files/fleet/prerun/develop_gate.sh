#!/bin/bash
# LINEAGE (Seat X 7th, 2026-11-06): re-keyed from Seat V 24th's develop_gate.sh (sha256 56bc9f88...) by tools/rekey_push_x7.py; the planted-overlap control path token v24 -> x7 (count-asserted: 1). Gate logic unchanged.
# LINEAGE (Seat V 24th, 2026-11-06): re-keyed from Seat V 23rd's develop_gate.sh by COUNT-ASSERTED token pairs (tools/rekey_push_v24.py); gate logic unchanged; two path-value deviations declared in evidence/declared_changes_push.md.
# LINEAGE (Seat V 23rd, 2026-11-05): re-keyed from Seat V 22nd's develop_gate.sh by COUNT-ASSERTED token pairs (tools/rekey_push_v23.py). Logic unchanged.
# LINEAGE (Seat V 22nd, 2026-11-05): re-keyed from Seat V 21st's develop_gate.sh by COUNT-ASSERTED token pairs (tools/rekey_push_v22.py). Logic unchanged.
# LINEAGE (Seat V 21st, 2026-11-05): derived from Seat V 20th's develop_gate.sh; the planted-overlap control path token v20 -> v21 (count-asserted). Logic unchanged.
# LINEAGE (Seat V 20th, 2026-11-05): derived from Seat W 28th's develop_gate.sh by tools/rekey_push_v20.py (counted named replacements on non-LINEAGE lines; no logic line changed).
# LINEAGE (Seat W 28th, 2026-11-05): derived from Seat F 31st's develop_gate.sh by tools/rekey_push_w28.py (explicit counted pairs; no logic line changed; see evidence/declared_changes.md).
# LINEAGE (Seat F 31st, 2026-11-05): re-keyed copy of Seat F 29th's develop_gate.sh by named replacements (counts: {}); logic unchanged.
# LINEAGE (Seat F 29th, 2026-11-04): re-keyed from Seat R 81st's develop_gate.sh by NAMED edits (each replacement count-checked, listed in evidence/rekey_push.out); logic unchanged.
# LINEAGE (Seat R 81st, 2026-11-04): re-keyed from Seat R 80th's develop_gate.sh by NAMED edits read one by one (tools/rekey_named_r81.py, diff in evidence/rekey/develop_gate.diff): the planted-overlap control path token r80 -> r81 (the driver finds this file next to itself). Logic unchanged.
# LINEAGE (Seat R 80th, 2026-11-03): re-keyed from Seat R 79th's develop_gate.sh by NAMED edits read one by one (tools/rekey_named_r80.py, diff in evidence/rekey/develop_gate.diff): the planted-overlap control path token r79 -> r80 (the driver finds this file next to itself). Logic unchanged.
# LINEAGE (Seat R 79th, 2026-11-03): copy of Seat R 78th's develop_gate.sh with the r78 tokens on matching lines changed to r79 by rekey_r79.py (a named-file pass, the diff read line by line, no logic line changed). Earlier seats' LINEAGE lines are left exactly as they were written.
# LINEAGE (Seat R 78th, 2026-11-03): copy of Seat R 77th's develop_gate.sh with the r77 tokens on matching lines changed to r78 by rekey_r78.py (a named-file pass, the diff read line by line, no logic line changed). Earlier seats' LINEAGE lines are left exactly as they were written.
# LINEAGE (Seat R 77th, 2026-11-03): copy of Seat R 76th's develop_gate.sh with the r76 tokens on matching lines changed to r77 by rekey_r77.py (a named-file pass, the diff read line by line, no logic line changed). Earlier seats' LINEAGE lines are left exactly as they were written.
# LINEAGE (Seat R 76th, 2026-11-03): copy of Seat R 75th's develop_gate.sh (itself re-keyed from Seat W 17th's) with the r75 tokens on matching lines changed to r76 by rekey_r76.py (a named-file pass, the diff read line by line, no logic line changed). Older LINEAGE lines below were written by earlier seats and carry the new seat token only because of this pass.
# LINEAGE (Seat R 76th, 2026-11-03): re-keyed copy of Seat W 17th's develop_gate.sh by READING it: only the seat token, the env-var prefix W17_ -> R76_, tool names, paths and the planted-control path changed; every gate is unchanged. Remaining mentions of W 17th are historical comments, listed in evidence/rekey_batch3.out.
# Wednesday's rule for a develop move while a branch waits to push (as recorded in the fleet's memory 2026-10-28):
#   push on the base the branch was built on if `git diff --name-only <base> <new develop>` shares no file with the branch,
#   the two Projects Documents docs aside (a docs-only conflict is resolved at merge, not by re-queueing).
# Offline and pure: it reads objects already in the store. usage: develop_gate.sh WORKTREE BASE_DEVELOP EXPECT_HEAD ORIGIN_DEVELOP
# exit 0 = accept (prints one line saying why), exit 1 = refuse (prints the reason), exit 2 = a git step failed (the gate cannot say).
WT="$1"; BASED="$2"; EXPECT="$3"; DEV="$4"
DOC1='Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html'
DOC2='Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html'
g() { git -C "$WT" "$@"; }
for c in "$BASED" "$EXPECT" "$DEV"; do
  g cat-file -e "${c}^{commit}" 2>/dev/null || { echo "object $c is not in the object store"; exit 2; }
done
g merge-base --is-ancestor "$BASED" "$EXPECT" || { echo "BASE_DEVELOP $BASED is not an ancestor of $EXPECT"; exit 1; }
if [ "$DEV" = "$BASED" ]; then echo "develop has not moved ($DEV)"; exit 0; fi
# a develop that is not a descendant of the base was rewritten or is behind it: this rule says nothing about that, so refuse
g merge-base --is-ancestor "$BASED" "$DEV" || { echo "origin develop $DEV is not a descendant of the base $BASED (rewritten or behind): refusing"; exit 1; }
moved=$(g diff --name-only "$BASED" "$DEV") || { echo "git diff base..develop failed"; exit 2; }
mine=$(g diff --name-only "$BASED" "$EXPECT") || { echo "git diff base..head failed"; exit 2; }
[ -n "$mine" ] || { echo "the branch changes no file against its base: nothing to push"; exit 1; }
both=$(comm -12 <(printf '%s\n' "$moved" | sort -u) <(printf '%s\n' "$mine" | sort -u))
nondoc=$(printf '%s\n' "$both" | grep -v -F -x -e "$DOC1" -e "$DOC2" | grep -v '^$')
# Wednesday's condition (3), a planted-overlap control IN THE SAME RUN. A synthetic path planted into BOTH lists must raise the
# shared-outside-the-docs count by exactly 1, or the check is blind and says so (exit 2) instead of accepting.
PLANT='Blockchain/Dev/x8-planted-overlap-control.ts'
both_p=$(comm -12 <({ printf '%s\n' "$moved"; echo "$PLANT"; } | sort -u) <({ printf '%s\n' "$mine"; echo "$PLANT"; } | sort -u))
nondoc_p=$(printf '%s\n' "$both_p" | grep -v -F -x -e "$DOC1" -e "$DOC2" | grep -v '^$')
shared_n=$(printf '%s\n' "$nondoc" | grep -c .); control_n=$(printf '%s\n' "$nondoc_p" | grep -c .)
[ "$control_n" -eq $((shared_n + 1)) ] || { echo "the planted-overlap control did not fire (shared outside the docs=$shared_n, with the plant=$control_n): the check is blind"; exit 2; }
if [ -n "$nondoc" ]; then
  echo "origin develop $DEV moved $(printf '%s\n' "$moved" | grep -c .) file(s) past the base and $(printf '%s\n' "$nondoc" | grep -c .) of them are ALSO in this branch (not docs): $(printf '%s' "$nondoc" | head -5 | tr '\n' ';')"
  exit 1
fi
echo "DOCSRULE: move ${BASED:0:8}..${DEV:0:8} changed $(printf '%s\n' "$moved" | grep -c .) files, branch changes $(printf '%s\n' "$mine" | grep -c .), overlap $(printf '%s\n' "$both" | grep -c .) (all in the two shared docs), planted control $control_n = $shared_n + 1"
exit 0
