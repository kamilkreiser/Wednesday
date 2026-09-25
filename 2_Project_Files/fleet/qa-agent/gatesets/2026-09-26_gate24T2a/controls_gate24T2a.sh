#!/bin/bash
# controls_gate24T2a.sh — every guard of the gate24T2a kit, run BOTH WAYS. Each control has a DOCTORED arm (one planted defect; the guard must refuse
# with its own exit code) and, where the mechanism is an override or a copied file, a PRISTINE twin through the SAME mechanism (defect not planted;
# must pass) — so a refusal is attributable to the defect, not to the harness. `--invert` flips every expectation: every control must then report
# MISMATCH (proves each control can fail and the harness can report it). Launches nothing: launcher controls use `--check` (headless) or stop at the
# non-TTY guard; repin controls use `--dry-run`, a bad argv, or a routing-file override that stops at step 0; predict / fill controls run in a MOVED
# COPY of the kit, never the home. Each doctored prompt phrase is chosen OUTSIDE the by-name ladder and the seat items, so the control reaches the rule
# it names (the ladder, exit 33, runs first). Doctored arms are PINNED to the launcher's own develop (pchk) so a develop move mid-run cannot mask them as
# exit 17. Writes only under <scratchpad>/g24a_controls_*. Derived from gate21T2d/e's controls, re-keyed to FOUR rows.
# Usage: controls_gate24T2a.sh <scratchpad dir> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
SP="${1:-}"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no scratchpad $SP"; exit 9; } ;; *) echo "usage: controls_gate24T2a.sh <scratchpad> [--invert]"; exit 9;; esac
L="$GS/launch_qa_secuura_batch1243-t2.sh"; PR="$GS/2026-09-26_secuura-batch1243-t2.prompt.txt"; CAP="$GS/mail_gate24T2a_ready.md"
REPIN="$GS/repin_and_launch_gate24T2a.sh"
CW="$SP/g24a_controls_$(date -u +%H%M%S)$([ "$INV" = 1 ] && echo _inv)"; mkdir -p "$CW"
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
pchk() { QAB24A_CUR_DEV="${QAB24A_CUR_DEV:-$PDEV}" "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
pctl() { # id want old new label
  local id="$1" want="$2"; doctor "$PR" "$CW/$id.prompt" "$3" "$4" || { judge "$id" "$want" 99 "DOCTOR FAILED: $5"; return; }
  cp "$PR" "$CW/$id.pristine.prompt"
  judge "$id" "$want" "$(QAB24A_PROMPT="$CW/$id.prompt" pchk "$id")" "$5"
  judge "$id/twin" 0 "$(QAB24A_PROMPT="$CW/$id.pristine.prompt" pchk "$id.twin")" "$5 — pristine copy through the same override"
}
hd() { sed -n "s/^  \"$1|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|.*$/\1/p" "$L"; }
H45="$(hd 1245)"; H48="$(hd 1248)"; PDEV="$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$L")"
[ -n "$H45" ] && [ -n "$H48" ] && [ -n "$PDEV" ] || { echo "REFUSING: could not read the #1245 / #1248 rows / DEVELOP_SHA from $L"; exit 9; }
P44="systemTest/performance/runner/k6_docker.ts,systemTest/performance/tests/unit/runner/k6DockerRedaction.test.ts"
P48="Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts"
say "controls_gate24T2a.sh $(date -u +%FT%TZ)$([ "$INV" = 1 ] && echo ' --invert') | kit $GS | work $CW"
say "--- launcher (--check unless stated)"
judge P 0 "$(chk P)" "positive: the kit as filled"
judge C 6 "$(QAB24A_HEAD_1243=0000000000000000000000000000000000000000 pchk C)" "stale #1243 head"
judge C2 6 "$(QAB24A_HEAD_1245=b4427d416592b40eb5ddb8727b2d6c31f3c7d067 pchk C2)" "#1241's head pinned as #1245's (the older attempt on the same file)"
judge C3 6 "$(QAB24A_HEAD_1248=a40cb9eea049f57348ef0a2c68326b56a577f7db pchk C3)" "L3's unpushed a40cb9eea049 pinned as #1248's head"
judge C/twin 0 "$(QAB24A_HEAD_1245="$H45" QAB24A_HEAD_1248="$H48" pchk C.twin)" "the real #1245 and #1248 heads through the same override"
judge D 17 "$(QAB24A_CUR_DEV=6e2a00bfed577528de1ee02b41cb5a0e99172b35 chk D)" "develop moved (BASE 6e2a00bfe as the current develop)"
judge D/twin 0 "$(QAB24A_CUR_DEV="$PDEV" chk D.twin)" "the pinned develop through the same override"
judge V 10 "$(QAB24A_PATHS_1244="${P44/k6_docker.ts/k6_Docker.ts}" pchk V)" "base-invariant compare: #1244 with a same-count WRONG path name"
judge V2 10 "$(QAB24A_PATHS_1248="${P48/packages\/shared/packages\/common}" pchk V2)" "base-invariant compare: #1248 with a WRONG path (another package)"
judge V/twin 0 "$(QAB24A_PATHS_1244="$P44" QAB24A_PATHS_1248="$P48" pchk V.twin)" "the right paths through the same override"
doctor "$CAP" "$CW/O.cap" 'A3 reds three cells here, not two.' 'A3 reds two cells here.' && cp "$CAP" "$CW/O.pristine.cap"
judge O 30 "$(QAB24A_BRIEF="$CW/O.cap" pchk O)" "capture missing a seat item ('A3 reds three cells here, not two.')"
judge O/twin 0 "$(QAB24A_BRIEF="$CW/O.pristine.cap" pchk O.twin)" "pristine capture through the same override"
pctl G 8 $'ultrathink\n' $'think\n' "no thinking directive"
pctl U 8 'PR #1244 is KS-1111.' 'PR #1244 is {{KS_1111}}.' "an unfilled fill token"
pctl H20 20 '1700b5ae7dd56ad3e30602a40b20ae6469c35350' '1700b5ae7dd56ad3e30602a40b20ae6469c3535X' "the prompt names a wrong #1245 head"
pctl T 32 'PR #1244 is KS-1111.' 'PR #1244 is KS-1112.' "ticket statement for #1244"
pctl T2 32 'PR #1243 is KS-1117 + KS-1300.' 'PR #1243 is KS-1117.' "ticket statement for #1243 (the two-key row)"
pctl I 7 '#1248 T2' '#1248 T3' "tier line for #1248"
pctl I2 7 'is FROZEN at four' 'is FROZEN at three' "the batch frozen at four"
pctl K 33 'CONT-DEFERRED' 'CONT-LATER' "a by-name keyword (CONT-DEFERRED)"
pctl B 34 'a sibling batch merging is not a difference' 'a sibling batch merging is a difference' "base-invariant rule"
pctl B2 34 'there is no declared exception here' 'an overlap is fine here' "no declared overlap: a move on an own path STOPS"
pctl B3 34 'declare any overlap you find with its merged-blob target' 'ignore any overlap you find' "pairwise: declare any overlap with its merged-blob target"
pctl S 35 'NO Docker action of any kind' 'a Docker action if useful' "no Docker"
pctl S2 35 'NEVER connect to it' 'connect as needed' "never the native :5432"
pctl X 36 'restore by bytes' 'restore somehow' "red-proof rule: restore by bytes"
pctl X2 36 'in YOUR OWN clone' 'in the shared checkout' "red proof in the tester's own clone"
pctl F 37 'there is NO 28/0 to claim for #1243, #1244 or #1245' 'there is a 28/0 to claim for #1243, #1244 or #1245' "fleet STOP: the systemTest pushes ran no Blockchain/Dev leg"
pctl F3 37 'NO STANDALONE RUN of' 'A STANDALONE RUN of' "fleet STOP: no standalone run"
pctl Y 38 'pre-existing (KS-562), not caused by this change"' 'pre-existing, not caused by this change"' "the anchoring wording"
pctl Y2 38 'an ASSERTION failure is REAL' 'an ASSERTION failure is noise' "the load rule"
pctl Hh 39 'NEVER WRITE THE SHARED CHECKOUT' 'WRITE THE SHARED CHECKOUT IF NEEDED' "holds: the shared checkout"
pctl H2 39 'NO ticket filed' 'tickets may be filed' "holds: no ticket filed"
pctl Q 40 'NULL, a throw, or wrong counts on ANY real shape is NO GO for #1245 (blocking)' 'NULL on a real shape is a note for #1245' "#1245 LIVE-SHAPE: NULL/wrong on a real shape is NO GO"
pctl Q2 40 'stdout AND stderr PIPED' 'stdout on a TTY' "#1245 LIVE-SHAPE: piped, not a TTY (as spawnSync)"
pctl Q3 40 'THROUGH THE REAL CODE PATH — never a lifted regex, never a re-implementation, never a Python port' 'through whatever path is easiest' "#1245 LIVE-SHAPE: the real function, never a lift"
pctl Q4 40 'The LOOKALIKE shapes S16-S18 and E5 are REAL vitest output and fall under THE RULE as written' 'The LOOKALIKE shapes S16-S18 and E5 are graded as notes only' "#1245 LIVE-SHAPE: the lookalike shapes fall under THE RULE"
pctl R 41 'At least one KS-1313 cell must red on a :210-only change' 'No KS-1313 cell need red on a :210-only change' "#1245 T-103: a :210-only change must red a cell"
pctl R2 41 'T-CALL — the call site' 'T-CALL — optional' "#1245 T-CALL: the call site is graded"
pctl N42 42 '#1245 is judged against develop' '#1245 is judged against #1241' "#1245 judged against develop, #1241 not graded"
pctl Z 43 'never by name, never pid 1' 'by name if needed' "login_stub reaper rule"
pctl SC 44 'grade its absence as disclosed scope' 'grade its absence as a defect' "KS-1300 item 1 is disclosed scope"
pctl SC2 44 'NO WIDENING of the masked name set' 'a welcome widening of the masked name set' "KS-1111: no widening of the name set"
pctl SC3 44 'it stays OUT of scope as Wednesday ruled' 'grade it as a defect' "#1248's named-continuation limit stays out of scope"
pctl W8 45 'IF W8 DOES NOT GO RED, THE FIXTURE DID NOT SURVIVE AND THE MATRIX IS UNREAD -> NO GO for #1248 (blocking)' 'IF W8 DOES NOT GO RED, note it' "#1248 T-2: W8 not red = NO GO"
pctl W8b 45 'T-2 FIRST' 'T-2 LAST' "#1248 T-2 runs FIRST"
pctl A 26 '`GO: merge #1243, #1244, #1245, #1248 batch`' '`GO: merge #1243 batch`' "the GO string"
pctl E 25 'PER PR FILE (5 over 5 paths) for #1243' 'PER PR FILE for #1243' "addendum count"
pctl J 23 '[QA -> Wednesday] TIER-2 GATE batch #1243 #1244 #1245 #1248 (Seat L6, round 24)' '[QA -> Wednesday] TIER-2 GATE batch #1243 #1244 #1245 #1248' "the verdict subject"
ET="$(sed -n "s/^END_TREE='\(.*\)'$/\1/p" "$L")"
python3 - "$PR" "$CW/W.prompt" "$ET" <<'PY'
import sys
s, d, et = sys.argv[1:4]; t = open(s, encoding='utf-8').read(); assert et in t
open(d, 'w', encoding='utf-8').write(t.replace(et, et[:-1] + ('0' if et[-1] != '0' else '1')))
PY
cp "$PR" "$CW/W.pristine.prompt"
judge W 31 "$(QAB24A_PROMPT="$CW/W.prompt" pchk W)" "the END_TREE not in full in the prompt"
judge W/twin 0 "$(QAB24A_PROMPT="$CW/W.pristine.prompt" pchk W.twin)" "pristine prompt through the same override"
"$L" < /dev/null > "$CW/N.out" 2>&1; judge N 21 "$?" "LAUNCH path (no --check) with stdin not a TTY — refuses before exec"
QAB24A_PROMPT="$PR" "$L" --check > "$CW/N2.out" 2>&1; rc=$?; [ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'TEST OVERRIDE is set' "$CW/N2.out" && rc=94
judge N2 0 "$rc" "an override set is allowed under --check AND reported (the launch path refuses it, exit 16, after the TTY guard)"
mkdir -p "$CW/moved"; cp -p "$L" "$CW/moved/"; "$CW/moved/$(basename "$L")" --check > "$CW/M.out" 2>&1; judge M 2 "$?" "the launcher copied out of its filled home (a MOVED KIT)"
"$L" --check > "$CW/M.twin.out" 2>&1; judge M/twin 0 "$?" "the same launcher at home"
say "--- repin_and_launch (dry runs / refusals only)"
bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R1.out" 2>&1; judge R1 0 "$?" "dry run, the kit as filled"
doctor "$L" "$CW/R2.launch.sh" "$H45|1|1|" "${H45%?}$([ "${H45: -1}" = 0 ] && echo 1 || echo 0)|1|1|" && chmod 755 "$CW/R2.launch.sh"
bash "$REPIN" "$CW/R2.launch.sh" "$SP" --dry-run > "$CW/R2.out" 2>&1; judge R2 11 "$?" "a stale #1245 head pin"
cp -p "$L" "$CW/R2.twin.launch.sh"; bash "$REPIN" "$CW/R2.twin.launch.sh" "$SP" --dry-run > "$CW/R2.twin.out" 2>&1; judge R2/twin 0 "$?" "the same copied-launcher mechanism, pins intact"
doctor "$L" "$CW/R3.launch.sh" "DEVELOP_SHA='$PDEV'" "DEVELOP_SHA='6e2a00bfed577528de1ee02b41cb5a0e99172b35'" && chmod 755 "$CW/R3.launch.sh"
bash "$REPIN" "$CW/R3.launch.sh" "$SP" --dry-run > "$CW/R3.out" 2>&1; judge R3 10 "$?" "the pinned develop is stale (the dry run reports the re-pin and stops)"
: > "$CW/empty_routing.conf"
G24A_ROUTING="$CW/empty_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4.out" 2>&1; judge R4 1 "$?" "a REAL run with the routing line absent stops at step 0 (routing-file override: deterministic)"
printf 'QA/Secuura-batch1243|coagent@agentmail.to|yes\n' > "$CW/good_routing.conf"
G24A_ROUTING="$CW/good_routing.conf" bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R4.twin.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'line present: 1 (grep rc=0' "$CW/R4.twin.out" && rc=95
judge R4/twin 0 "$rc" "the routing line present (override file), dry run — AND step 0 reads it as present"
printf 'QA/Secuura-batch1241r2|coagent@agentmail.to|yes\n' > "$CW/other_routing.conf"
G24A_ROUTING="$CW/other_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4b.out" 2>&1; judge R4b 1 "$?" "only another gate's pane line present — this pane is NOT routed, a real run stops at step 0"
bash "$REPIN" "$L" /tmp > "$CW/R5.out" 2>&1; judge R5 9 "$?" "a scratchpad outside /private/tmp/claude-501/"
say "--- the moved kit, predict and fill (in a COPY of the kit, never the home)"
MK="$CW/movedkit"; mkdir -p "$MK"; /usr/bin/rsync -a --exclude '_sp' --exclude 'launch_*.out' --exclude 'g24a_controls_*' "$GS/" "$MK/"
bash "$MK/repin_and_launch_gate24T2a.sh" "$MK/launch_qa_secuura_batch1243-t2.sh" "$SP" --dry-run > "$CW/R6.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'MOVED KIT' "$CW/R6.out" && rc=98
judge R6 0 "$rc" "moved-kit dry run: rc 0 AND reports MOVED KIT"
for s in 1243 1244 1245 1248; do
  python3 "$MK/predict_gate24T2a.py" "$SP" --simulate "foreign$s" > "$CW/P$s.out" 2>&1; judge "P$s" 1 "$?" "predict over develop + a FOREIGN edit of #$s's own file — the base-invariant check (3) refuses"
done
python3 "$MK/predict_gate24T2a.py" "$SP" > "$CW/P.twin.out" 2>&1; judge P/twin 0 "$?" "predict over origin develop in the same copy (no simulation)"
cp "$MK/pins_gate24T2a.json" "$CW/pins.real.json"; cp "$MK/pins_gate24T2a.SIM-foreign1245.json" "$MK/pins_gate24T2a.json" 2>> "$CW/F2.cp.err"
if [ -s "$MK/pins_gate24T2a.SIM-foreign1245.json" ] && ! cmp -s "$CW/pins.real.json" "$MK/pins_gate24T2a.json"; then python3 "$MK/fill_gate24T2a.py" > "$CW/F2.out" 2>&1; rc=$?; else echo "the SIM pins file was not written — the control cannot run" > "$CW/F2.out"; rc=96; fi
judge F2 1 "$rc" "fill refuses a SIMULATED pins file (the SIM pins asserted present and swapped in first)"
cp "$CW/pins.real.json" "$MK/pins_gate24T2a.json"
python3 "$MK/fill_gate24T2a.py" > "$CW/F1.out" 2>&1; rc=$?
"$MK/launch_qa_secuura_batch1243-t2.sh" --check > "$CW/F1.check.out" 2>&1; rc2=$?
[ "$rc" = 0 ] && [ "$rc2" = 0 ] && /usr/bin/grep -q -F "GS='$MK'" "$MK/launch_qa_secuura_batch1243-t2.sh" && rc=0 || rc=97
judge F1 0 "$rc" "the moved copy re-filled at its new home: fill rc 0, --check rc 0, its launcher names the new home"
say "RESULT $([ "$INV" = 1 ] && echo '(inverted) ')$OK OK / $BAD MISMATCH of $N  $(date -u +%FT%TZ)"
[ "$BAD" = 0 ]
