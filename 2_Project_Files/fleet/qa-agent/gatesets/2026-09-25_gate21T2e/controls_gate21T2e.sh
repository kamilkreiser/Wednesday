#!/bin/bash
# controls_gate21T2e.sh — every guard of the gate21T2e kit, run BOTH WAYS. Each control has a DOCTORED arm (one planted defect; the guard must refuse
# with its own exit code) and, where the mechanism is an override or a copied file, a PRISTINE twin through the SAME mechanism (defect not planted;
# must pass) — so a refusal is attributable to the defect, not to the harness. `--invert` flips every expectation: every control must then report
# MISMATCH (proves each control can fail and the harness can report it). Launches nothing: launcher controls use `--check` (headless) or stop at the
# non-TTY guard; repin controls use `--dry-run`, a bad argv, or a routing-file override that stops at step 0; predict / fill controls run in a MOVED
# COPY of the kit, never the home. Each doctored prompt phrase is chosen OUTSIDE the by-name ladder, so the control reaches the rule it names (the
# ladder, exit 33, runs first). Doctored arms are PINNED to the launcher's own develop (pchk) so a develop move mid-run cannot mask them as exit 17.
# Writes only under <scratchpad>/g21e_controls_*. Derived from gate21T2d's controls_gate21T2d.sh, re-keyed to ONE row.
# Usage: controls_gate21T2e.sh <scratchpad dir> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
SP="${1:-}"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no scratchpad $SP"; exit 9; } ;; *) echo "usage: controls_gate21T2e.sh <scratchpad> [--invert]"; exit 9;; esac
L="$GS/launch_qa_secuura_1241-r2-t2.sh"; PR="$GS/2026-09-25_secuura-1241-r2-t2.prompt.txt"; CAP="$GS/mail_gate21T2e_ready.md"
REPIN="$GS/repin_and_launch_gate21T2e.sh"
CW="$SP/g21e_controls_$(date -u +%H%M%S)$([ "$INV" = 1 ] && echo _inv)"; mkdir -p "$CW"
OK=0; BAD=0; N=0
say() { printf '%s\n' "$*"; }
judge() { # $1 id, $2 want rc, $3 got rc, $4 label
  local want="$2"; N=$((N+1))
  if [ "$INV" = 1 ]; then
    if [ "$3" != "$want" ]; then OK=$((OK+1)); say "  OK       $1 (inverted: want != $want, got $3) — $4"; else BAD=$((BAD+1)); say "  MISMATCH $1 (inverted: want != $want, got $3) — $4"; fi
  else
    if [ "$3" = "$want" ]; then OK=$((OK+1)); say "  OK       $1 want $want got $3 — $4"; else BAD=$((BAD+1)); say "  MISMATCH $1 want $want got $3 — $4"; fi
  fi
}
# doctor <src> <dst> <old> <new>: a copy with ONE planted defect; refuses (rc 99) if <old> is absent, so a control can never pass vacuously
doctor() { python3 - "$1" "$2" "$3" "$4" <<'PY'
import re, sys
s, d, o, n = sys.argv[1:5]
t = open(s, encoding='utf-8').read()
rx = re.compile(r'\s+'.join(re.escape(w) for w in o.split(' ')))
t2, k = rx.subn(lambda m: n, t)
if k == 0: print('DOCTOR: anchor absent: %r' % o[:80]); sys.exit(99)
open(d, 'w', encoding='utf-8').write(t2)
PY
}
chk() { "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
pchk() { QAB1241R2_CUR_DEV="${QAB1241R2_CUR_DEV:-$PDEV}" "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
pctl() { # id want old new label
  local id="$1" want="$2"; doctor "$PR" "$CW/$id.prompt" "$3" "$4" || { judge "$id" "$want" 99 "DOCTOR FAILED: $5"; return; }
  cp "$PR" "$CW/$id.pristine.prompt"
  judge "$id" "$want" "$(QAB1241R2_PROMPT="$CW/$id.prompt" pchk "$id")" "$5"
  judge "$id/twin" 0 "$(QAB1241R2_PROMPT="$CW/$id.pristine.prompt" pchk "$id.twin")" "$5 — pristine copy through the same override"
}
H41="$(sed -n 's/^  "1241|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|.*$/\1/p' "$L")"; PDEV="$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$L")"
[ -n "$H41" ] && [ -n "$PDEV" ] || { echo "REFUSING: could not read the #1241 row / DEVELOP_SHA from $L"; exit 9; }
say "controls_gate21T2e.sh $(date -u +%FT%TZ)$([ "$INV" = 1 ] && echo ' --invert') | kit $GS | work $CW"
say "--- launcher (--check unless stated)"
judge P 0 "$(chk P)" "positive: the kit as filled"
judge C 6 "$(QAB1241R2_HEAD=0000000000000000000000000000000000000000 pchk C)" "stale #1241 head"
judge C2 6 "$(QAB1241R2_HEAD=e2d0518df40228f0a183bc4223c7a6840821253e pchk C2)" "the ROUND-1 head (e2d0518df) pinned instead of round 2's"
judge C/twin 0 "$(QAB1241R2_HEAD="$H41" pchk C.twin)" "the real head through the same override"
judge D 17 "$(QAB1241R2_CUR_DEV=e68e2f0e837df86da527d775a3a49c631b0f5b17 chk D)" "develop moved (round 1's develop e68e2f0e8)"
judge D/twin 0 "$(QAB1241R2_CUR_DEV="$PDEV" chk D.twin)" "the pinned develop through the same override"
judge V 10 "$(QAB1241R2_PATHS='systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.TS' pchk V)" "base-invariant compare: a same-count WRONG path name"
judge V/twin 0 "$(QAB1241R2_PATHS='systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts' pchk V.twin)" "the right path through the same override"
doctor "$CAP" "$CW/O.cap" 'There is no N-4' 'There is no N-5' && cp "$CAP" "$CW/O.pristine.cap"
judge O 30 "$(QAB1241R2_BRIEF="$CW/O.cap" pchk O)" "capture missing a seat item ('There is no N-4')"
judge O/twin 0 "$(QAB1241R2_BRIEF="$CW/O.pristine.cap" pchk O.twin)" "pristine capture through the same override"
pctl G 8 $'ultrathink\n' $'think\n' "no thinking directive"
pctl U 8 'PR #1241 is KS-1226.' 'PR #1241 is {{KS_1226}}.' "an unfilled fill token"
pctl H20 20 'b4427d416592b40eb5ddb8727b2d6c31f3c7d067' 'b4427d416592b40eb5ddb8727b2d6c31f3c7d06X' "the prompt names a wrong head"
pctl T 32 'PR #1241 is KS-1226.' 'PR #1241 is KS-1227.' "ticket statement for #1241"
pctl I 7 '#1241 T2' '#1241 T3' "tier line for #1241"
pctl I2 7 'ROUND 2 OF 2' 'ROUND 1 OF 2' "round 2 of 2 (the cap)"
pctl K 33 'SYMMETRIC-FIXTURE' 'SYMMETRIC-FORM' "a by-name keyword (SYMMETRIC-FIXTURE)"
pctl B 34 'a sibling batch merging is not a difference' 'a sibling batch merging is a difference' "base-invariant rule"
pctl B2 34 'there is no declared exception here' 'an overlap is fine here' "no declared overlap: a move on the own path STOPS"
pctl S 35 'NO Docker action of any kind' 'a Docker action if useful' "no Docker"
pctl S2 35 'NEVER connect to it' 'connect as needed' "never the native :5432"
pctl X 36 'restore by bytes' 'restore somehow' "red-proof rule: restore by bytes"
pctl X2 36 "RED on BOTH the round-1 reading and develop's reading" "RED on the round-1 reading or develop's reading" "red proof: red on BOTH round-1 and develop readings"
pctl F 37 'there is NO 28/0 to claim for #1241' 'there is a 28/0 to claim for #1241' "fleet STOP: #1241's push ran no Blockchain/Dev leg"
pctl F3 37 'NO STANDALONE RUN of' 'A STANDALONE RUN of' "fleet STOP: no standalone run"
pctl Y 38 'pre-existing (KS-562), not caused by this change"' 'pre-existing, not caused by this change"' "the anchoring wording"
pctl Y2 38 'an ASSERTION failure is REAL' 'an ASSERTION failure is noise' "the load rule"
pctl Y3 38 'KNOWN FALSE-RED class (ticket KS-1155; F4 for :127)' 'KNOWN FLAKE class (ticket KS-1155; F4 for :127)' "the load rule names F4"
pctl Hh 39 'NEVER WRITE THE SHARED CHECKOUT' 'WRITE THE SHARED CHECKOUT IF NEEDED' "holds: the shared checkout"
pctl H2 39 'NO ticket filed (the residue ticket is DESCRIBED, never filed)' 'the residue ticket may be filed' "holds: the residue ticket is described, never filed"
pctl Q 40 'NULL, a throw, or wrong counts on ANY real shape is NO GO for #1241 (blocking)' 'NULL on a real shape is a note for #1241' "LIVE-SHAPE: NULL on a real shape is NO GO"
pctl Q2 40 'stdout AND stderr PIPED' 'stdout on a TTY' "LIVE-SHAPE: piped, not a TTY (as spawnSync)"
pctl Q3 40 'THROUGH THE REAL CODE PATH — never a lifted regex, never a re-implementation, never a Python port' 'through whatever path is easiest' "LIVE-SHAPE: the real function, never a lift"
pctl R 41 'At least one KS-1226 cell must red on a :93-only change' 'No KS-1226 cell need red on a :93-only change' "T-103: a :93-only change must red a cell"
pctl R2 41 'the OTHER successor of round 1' 'another successor of round 1' "T-CALL: the call site is graded"
pctl CAP 42 'you describe the RESIDUE TICKET for Wednesday to file' 'you file the RESIDUE TICKET yourself' "round-2 cap: residue described for Wednesday"
pctl Z 43 'never by name, never pid 1' 'by name if needed' "login_stub reaper rule"
pctl IT1 44 'grade nothing about the budget' 'grade the budget too' "item 1 OUT of scope"
pctl A 26 '`GO: merge #1241 batch`' '`GO: merge #1241`' "the GO string"
pctl E 25 'PER PR FILE (1 over 1 path)' 'PER PR FILE' "addendum count"
pctl J 23 '[QA -> Wednesday] TIER-2 GATE #1241 round 2 of 2 (KS-1226 item 2, Seat B 27th)' '[QA -> Wednesday] TIER-2 GATE #1241 (KS-1226 item 2, Seat B 27th)' "the verdict subject"
ET="$(sed -n "s/^END_TREE='\(.*\)'$/\1/p" "$L")"
python3 - "$PR" "$CW/W.prompt" "$ET" <<'PY'
import sys
s, d, et = sys.argv[1:4]; t = open(s, encoding='utf-8').read(); assert et in t
open(d, 'w', encoding='utf-8').write(t.replace(et, et[:-1] + ('0' if et[-1] != '0' else '1')))
PY
cp "$PR" "$CW/W.pristine.prompt"
judge W 31 "$(QAB1241R2_PROMPT="$CW/W.prompt" pchk W)" "the END_TREE not in full in the prompt"
judge W/twin 0 "$(QAB1241R2_PROMPT="$CW/W.pristine.prompt" pchk W.twin)" "pristine prompt through the same override"
"$L" < /dev/null > "$CW/N.out" 2>&1; judge N 21 "$?" "LAUNCH path (no --check) with stdin not a TTY — refuses before exec"
QAB1241R2_PROMPT="$PR" "$L" --check > "$CW/N2.out" 2>&1; judge N2 0 "$?" "an override set is allowed under --check (the launch path refuses it, exit 16, after the TTY guard)"
mkdir -p "$CW/moved"; cp -p "$L" "$CW/moved/"; "$CW/moved/$(basename "$L")" --check > "$CW/M.out" 2>&1; judge M 2 "$?" "the launcher copied out of its filled home (a MOVED KIT)"
"$L" --check > "$CW/M.twin.out" 2>&1; judge M/twin 0 "$?" "the same launcher at home"
say "--- repin_and_launch (dry runs / refusals only)"
bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R1.out" 2>&1; judge R1 0 "$?" "dry run, the kit as filled"
doctor "$L" "$CW/R2.launch.sh" "$H41|1|2|" "${H41%?}$([ "${H41: -1}" = 0 ] && echo 1 || echo 0)|1|2|" && chmod 755 "$CW/R2.launch.sh"
bash "$REPIN" "$CW/R2.launch.sh" "$SP" --dry-run > "$CW/R2.out" 2>&1; judge R2 11 "$?" "a stale #1241 head pin"
cp -p "$L" "$CW/R2.twin.launch.sh"; bash "$REPIN" "$CW/R2.twin.launch.sh" "$SP" --dry-run > "$CW/R2.twin.out" 2>&1; judge R2/twin 0 "$?" "the same copied-launcher mechanism, pins intact"
doctor "$L" "$CW/R3.launch.sh" "DEVELOP_SHA='$PDEV'" "DEVELOP_SHA='e68e2f0e837df86da527d775a3a49c631b0f5b17'" && chmod 755 "$CW/R3.launch.sh"
bash "$REPIN" "$CW/R3.launch.sh" "$SP" --dry-run > "$CW/R3.out" 2>&1; judge R3 10 "$?" "the pinned develop is stale (the dry run reports the re-pin and stops)"
: > "$CW/empty_routing.conf"
G21E_ROUTING="$CW/empty_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4.out" 2>&1; judge R4 1 "$?" "a REAL run with the routing line absent stops at step 0 (routing-file override: deterministic)"
printf 'QA/Secuura-batch1241r2|coagent@agentmail.to|yes\n' > "$CW/good_routing.conf"
G21E_ROUTING="$CW/good_routing.conf" bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R4.twin.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'line present: 1 (grep rc=0' "$CW/R4.twin.out" && rc=95
judge R4/twin 0 "$rc" "the routing line present (override file), dry run — AND step 0 reads it as present"
printf 'QA/Secuura-batch1241|coagent@agentmail.to|yes\n' > "$CW/r1only_routing.conf"
G21E_ROUTING="$CW/r1only_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4b.out" 2>&1; judge R4b 1 "$?" "only round 1's pane line (QA/Secuura-batch1241) present — the r2 pane is NOT routed, a real run stops at step 0"
bash "$REPIN" "$L" /tmp > "$CW/R5.out" 2>&1; judge R5 9 "$?" "a scratchpad outside /private/tmp/claude-501/"
say "--- the moved kit, predict and fill (in a COPY of the kit, never the home)"
MK="$CW/movedkit"; mkdir -p "$MK"; /usr/bin/rsync -a --exclude '_sp' --exclude 'launch_*.out' "$GS/" "$MK/"
bash "$MK/repin_and_launch_gate21T2e.sh" "$MK/launch_qa_secuura_1241-r2-t2.sh" "$SP" --dry-run > "$CW/R6.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'MOVED KIT' "$CW/R6.out" && rc=98
judge R6 0 "$rc" "moved-kit dry run: rc 0 AND reports MOVED KIT"
python3 "$MK/predict_gate21T2e.py" "$SP" --simulate foreign1241 > "$CW/P1.out" 2>&1; judge P1 1 "$?" "predict over develop + a FOREIGN edit of #1241's own file — the base-invariant check (3) refuses"
python3 "$MK/predict_gate21T2e.py" "$SP" > "$CW/P1.twin.out" 2>&1; judge P1/twin 0 "$?" "predict over origin develop in the same copy (no simulation)"
cp "$MK/pins_gate21T2e.json" "$CW/pins.real.json"; cp "$MK/pins_gate21T2e.SIM-foreign1241.json" "$MK/pins_gate21T2e.json" 2>> "$CW/F2.cp.err"
if [ -s "$MK/pins_gate21T2e.SIM-foreign1241.json" ] && ! cmp -s "$CW/pins.real.json" "$MK/pins_gate21T2e.json"; then python3 "$MK/fill_gate21T2e.py" > "$CW/F2.out" 2>&1; rc=$?; else echo "the SIM pins file was not written — the control cannot run" > "$CW/F2.out"; rc=96; fi
judge F2 1 "$rc" "fill refuses a SIMULATED pins file (the SIM pins asserted present and swapped in first)"
cp "$CW/pins.real.json" "$MK/pins_gate21T2e.json"
python3 "$MK/fill_gate21T2e.py" > "$CW/F1.out" 2>&1; rc=$?
"$MK/launch_qa_secuura_1241-r2-t2.sh" --check > "$CW/F1.check.out" 2>&1; rc2=$?
[ "$rc" = 0 ] && [ "$rc2" = 0 ] && /usr/bin/grep -q -F "GS='$MK'" "$MK/launch_qa_secuura_1241-r2-t2.sh" && rc=0 || rc=97
judge F1 0 "$rc" "the moved copy re-filled at its new home: fill rc 0, --check rc 0, its launcher names the new home"
say "RESULT $([ "$INV" = 1 ] && echo '(inverted) ')$OK OK / $BAD MISMATCH of $N  $(date -u +%FT%TZ)"
[ "$BAD" = 0 ]
