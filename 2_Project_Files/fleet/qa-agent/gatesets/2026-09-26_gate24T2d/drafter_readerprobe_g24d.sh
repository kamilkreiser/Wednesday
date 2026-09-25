#!/bin/bash
# drafter_readerprobe_g24d.sh — the DRAFTER's own run of #1253 ROUND 2's REAL fixture guard (91e066264004) under THE READER RULE — a PREDICTION
# instrument for the kit (the gate re-measures in its own clone). The tree is `git archive` of the head's Blockchain/Dev/scripts + .githooks from the
# kit's scratch clone into <kit>/_sp/readerprobe/<stamp>/tree (never the checkout). Each shape is written into a COPY of the subject at the c2 call site
# (:247 — deliberately NOT c0 or c1, which cells 10 and 11 use as their own tamper anchors), the tamper is ASSERTED APPLIED (the copy differs from the
# subject and the anchor line is gone or a `(` line appears), and the REAL guard runs with SUBJ_SH=<copy>. Recorded per shape: the guard's own
# `N passed, M failed`, cell 9's line (ok/FAIL and its detail), and which other cells failed. stdout and stderr are captured SEPARATELY.
# Deletes nothing; the guard's own WORK dir is its own mktemp (it removes it on EXIT by its own trap). Usage: drafter_readerprobe_g24d.sh <kit dir>
set -u
K="${1:?kit dir}"; CL="$K/_sp/g24d_sp/clone.git"; P="$K/_sp/readerprobe/$(date -u +%H%M%S)"; T="$P/tree"; mkdir -p "$T"
git --git-dir "$CL" archive 91e066264004fdb22c67efb0c25fc44375ec6eac Blockchain/Dev/scripts .githooks | tar -x -C "$T"
G="$T/Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh"; S="$T/Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh"
A='build_fixture "$WORK/c2" with-develop'
shape() { # $1 name -> writes $P/subj.<name>.test.sh
  local f="$P/subj.$1.test.sh"
  case "$1" in
    pristine)      cp "$S" "$f" ;;
    trailing-pipe) awk -v a="$A" '$0==a{print a " | cat"; next}{print}' "$S" > "$f" ;;
    brace-pipe)    awk -v a="$A" '$0==a{print "{ " a "; } | cat"; next}{print}' "$S" > "$f" ;;
    backticks)     awk -v a="$A" '$0==a{print "x=`" a "`"; next}{print}' "$S" > "$f" ;;
    paren-line)    awk -v a="$A" '$0==a{print "("; print a; print ")"; next}{print}' "$S" > "$f" ;;
    background)    awk -v a="$A" '$0==a{print a " &"; print "wait"; next}{print}' "$S" > "$f" ;;
    or-true)       awk -v a="$A" '$0==a{print a " || true"; next}{print}' "$S" > "$f" ;;
    false-or)      awk -v a="$A" '$0==a{print "false || " a; next}{print}' "$S" > "$f" ;;
    if-then)       awk -v a="$A" '$0==a{print "if " a "; then :; fi"; next}{print}' "$S" > "$f" ;;
    cmdsub-multiline) awk -v a="$A" '$0==a{print "x=$("; print a; print ")"; next}{print}' "$S" > "$f" ;;
    paren-2-above) awk -v a="$A" '$0==a{print "("; print "  : noop"; print a; print ")"; next}{print}' "$S" > "$f" ;;
    paren-inline-above) awk -v a="$A" '$0==a{print "( : noop"; print a; print ")"; next}{print}' "$S" > "$f" ;;
  esac
  printf '%s' "$f"
}
echo "drafter_readerprobe_g24d.sh $(date -u +%FT%TZ) | /bin/bash $(/bin/bash -c 'echo $BASH_VERSION') | guard blob $(git --git-dir "$CL" rev-parse 91e066264004:Blockchain/Dev/scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh) | load $(uptime | sed 's/.*averages*: //')"
for s in pristine trailing-pipe brace-pipe backticks paren-line background or-true false-or if-then cmdsub-multiline paren-2-above paren-inline-above; do
  f="$(shape "$s")"
  applied=YES; cmp -s "$f" "$S" && applied=no; [ "$s" = pristine ] && applied=n/a
  SUBJ_SH="$f" /bin/bash "$G" > "$P/$s.out" 2> "$P/$s.err"; rc=$?
  c9="$(grep -A1 -E '^  (ok|FAIL) +NB-1218-c: ' "$P/$s.out" | tr '\n' ' ' | sed 's/  */ /g' | cut -c1-230)"
  printf '%-19s applied=%-3s rc=%s %s | failed cells: %s | cell9: %s\n' "$s" "$applied" "$rc" "$(grep -E '^ +[0-9]+ passed, [0-9]+ failed' "$P/$s.out" | tr -s ' ')" \
    "$(grep -E '^  FAIL ' "$P/$s.out" | sed 's/^  FAIL //' | cut -c1-40 | tr '\n' ';')" "$c9"
done
echo "done $(date -u +%FT%TZ)"
