#!/bin/bash
# controls_gate24T2c.sh — every guard of the gate24T2c kit, run BOTH WAYS. Each control has a DOCTORED arm (one planted defect; the guard must refuse
# with its own exit code) and, where the mechanism is an override or a copied file, a PRISTINE twin through the SAME mechanism (defect not planted;
# must pass) — so a refusal is attributable to the defect, not to the harness. `--invert` flips every expectation: every control must then report
# MISMATCH (proves each control can fail and the harness can report it). Launches nothing: launcher controls use `--check` (headless) or stop at the
# non-TTY guard; repin controls use `--dry-run`, a bad argv, or a routing-file override that stops at step 0; predict / fill controls run in a MOVED
# COPY of the kit, never the home. Each doctored prompt phrase is chosen OUTSIDE the by-name ladder and the seat items, so the control reaches the rule
# it names (the ladder, exit 33, runs first). Doctored arms are PINNED to the launcher's own develop (pchk) so a develop move mid-run cannot mask them as
# exit 17 — but a develop move mid-run still invalidates the predict / fill arms: if origin develop moves during a run, QUARANTINE that run's output and
# re-run (gate24T2b's first run was lost that way). The sibling batch is controlled POSITIVELY: gate24T2b's seven squashed onto develop must re-pin
# cleanly and move the fleet STOP read to 55 / 10 (P-T2Bm). Writes only under <scratchpad>/g24c_controls_*. Derived from gate24T2b's controls.
# Usage: controls_gate24T2c.sh <scratchpad dir> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
SP="${1:-}"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no scratchpad $SP"; exit 9; } ;; *) echo "usage: controls_gate24T2c.sh <scratchpad> [--invert]"; exit 9;; esac
L="$GS/launch_qa_secuura_batch1245r2-t2.sh"; PR="$GS/2026-09-26_secuura-batch1245r2-t2.prompt.txt"; CAP="$GS/mail_gate24T2c_ready.md"
REPIN="$GS/repin_and_launch_gate24T2c.sh"; CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
CW="$SP/g24c_controls_$(date -u +%H%M%S)$([ "$INV" = 1 ] && echo _inv)"; mkdir -p "$CW"
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
pchk() { QAB24C_CUR_DEV="${QAB24C_CUR_DEV:-$PDEV}" "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
pctl() { # id want old new label
  local id="$1" want="$2"; doctor "$PR" "$CW/$id.prompt" "$3" "$4" || { judge "$id" "$want" 99 "DOCTOR FAILED: $5"; return; }
  cp "$PR" "$CW/$id.pristine.prompt"
  judge "$id" "$want" "$(QAB24C_PROMPT="$CW/$id.prompt" pchk "$id")" "$5"
  judge "$id/twin" 0 "$(QAB24C_PROMPT="$CW/$id.pristine.prompt" pchk "$id.twin")" "$5 — pristine copy through the same override"
}
hd() { sed -n "s/^  \"$1|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|.*$/\1/p" "$L"; }
H45="$(hd 1245)"; H56="$(hd 1256)"; H59="$(hd 1259)"; H61="$(hd 1261)"; PDEV="$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$L")"
[ -n "$H45" ] && [ -n "$H56" ] && [ -n "$H59" ] && [ -n "$H61" ] && [ -n "$PDEV" ] || { echo "REFUSING: could not read the #1245 / #1256 / #1259 / #1261 rows / DEVELOP_SHA from $L"; exit 9; }
DEV0="$(git -C "$CHECKOUT" ls-remote origin refs/heads/develop | cut -f1)"
P58="Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh,Blockchain/Dev/scripts/run-migrations.sh"
P45="systemTest/performance/tests/unit/support/capturedChildOutput.ts,systemTest/performance/tests/unit/utils/unitSuiteSlotIndependence.test.ts"
say "controls_gate24T2c.sh $(date -u +%FT%TZ)$([ "$INV" = 1 ] && echo ' --invert') | kit $GS | work $CW | origin develop at start $DEV0 (pinned $PDEV)"
say "--- launcher (--check unless stated)"
judge P 0 "$(chk P)" "positive: the kit as filled"
judge C 6 "$(QAB24C_HEAD_1245=0000000000000000000000000000000000000000 pchk C)" "stale #1245 head"
judge C2 6 "$(QAB24C_HEAD_1245=1700b5ae7dd56ad3e30602a40b20ae6469c35350 pchk C2)" "#1245's ROUND-1 head pinned (1700b5ae — the round gate24T2a graded)"
judge C4 6 "$(QAB24C_HEAD_1261="$H56" pchk C4)" "#1256's head pinned as #1261's"
judge C/twin 0 "$(QAB24C_HEAD_1245="$H45" QAB24C_HEAD_1261="$H61" pchk C.twin)" "the real #1245 / #1261 heads through the same overrides"
judge D 17 "$(QAB24C_CUR_DEV=6e2a00bfed577528de1ee02b41cb5a0e99172b35 chk D)" "develop moved (BASE 6e2a00bfe as the current develop)"
judge D/twin 0 "$(QAB24C_CUR_DEV="$PDEV" chk D.twin)" "the pinned develop through the same override"
judge V 10 "$(QAB24C_PATHS_1258="${P58/run-migrations.sh/run_migrations.sh}" pchk V)" "base-invariant compare: #1258 with a same-count WRONG path name"
judge V2 10 "$(QAB24C_PATHS_1245="${P45//systemTest\/performance/systemTest/akto}" pchk V2)" "base-invariant compare: #1245 with WRONG paths (another package)"
judge V/twin 0 "$(QAB24C_PATHS_1258="$P58" QAB24C_PATHS_1245="$P45" pchk V.twin)" "the right paths through the same override"
doctor "$CAP" "$CW/O.cap" '#1257 ran 0 of 15 legs, by design' '#1257 ran some legs' && cp "$CAP" "$CW/O.pristine.cap"
judge O 30 "$(QAB24C_BRIEF="$CW/O.cap" pchk O)" "capture missing a seat item (#1257's 0 of 15 legs)"
judge O/twin 0 "$(QAB24C_BRIEF="$CW/O.pristine.cap" pchk O.twin)" "pristine capture through the same override"
pctl G 8 $'ultrathink\n' $'think\n' "no thinking directive"
pctl U 8 'PR #1256 is KS-1159.' 'PR #1256 is {{KS_1159}}.' "an unfilled fill token"
pctl H20 20 "$H61" "${H61%?}$([ "${H61: -1}" = 0 ] && echo 1 || echo 0)" "the prompt names a wrong #1261 head"
pctl T 32 'PR #1256 is KS-1159.' 'PR #1256 is KS-1160.' "ticket statement for #1256"
pctl I 7 '#1258 T2' '#1258 T3' "tier line for #1258"
pctl I2 7 'The batch is FROZEN at seven' 'The batch is FROZEN at six' "the batch frozen at seven"
pctl K 33 'REVERT-SKIPS' 'REVERT-SKIP' "a by-name keyword (REVERT-SKIPS, every occurrence)"
pctl B 34 'a sibling batch merging is not a difference' 'a sibling batch merging is a difference' "base-invariant rule"
pctl B2 34 'THERE IS NO DECLARED OVERLAP in this batch' 'THERE IS NO DECLARED OVERLAP in that batch' "no declared overlap in this batch"
pctl B3 34 'declare any overlap you find with its merged-blob target' 'ignore any overlap you find' "pairwise: declare any overlap"
pctl S 35 'NO Docker action of any kind' 'a Docker action if useful' "no Docker"
pctl S2 35 'NEVER connect to it' 'connect as needed' "never the native :5432"
pctl X 36 'restore by bytes' 'restore somehow' "red-proof rule: restore by bytes"
pctl X2 36 'in YOUR OWN clone' 'in the shared checkout' "red proof in the tester's own clone"
pctl X3 36 '(4) an INERT TAMPER' '(4) one INERT TAMPER' "an inert tamper is a FAIL of the arm"
pctl F 37 'THE FLEET STOP after this merge is READ FROM THE DEVELOP IT LANDS ON' 'THE FLEET STOP after this merge is 6/0 and 49/0' "fleet STOP: read from the develop the merge lands on"
pctl F2 37 'was OVERWRITTEN by the seat' 'was kept by the seat' "fleet STOP: #1256's record overwritten"
pctl F3 37 'NO STANDALONE RUN of' 'A STANDALONE RUN of' "fleet STOP: no standalone run beyond the changed suites"
pctl Y 38 'pre-existing (KS-562), not caused by this change"' 'pre-existing, not caused by this change"' "the anchoring wording"
pctl Y2 38 'an ASSERTION failure is REAL' 'an ASSERTION failure is noise' "the load rule"
pctl Hh 39 'NEVER WRITE THE SHARED CHECKOUT' 'WRITE THE SHARED CHECKOUT IF NEEDED' "holds: the shared checkout"
pctl H2 39 'NO ticket filed' 'tickets may be filed' "holds: no ticket filed"
pctl Q 40 'A WRONG READING ON ANY REAL SHAPE = NO GO for #1245 (blocking)' 'A wrong reading is a note for #1245' "THE RULE (#1245): a wrong reading on a real shape is NO GO"
pctl Q2 40 'AT THE CAP A NO GO SHIPS NOTHING and the residue is ticketed by Wednesday' 'AT THE CAP A NO GO ships a partial fix' "THE RULE: at the cap a NO GO ships nothing"
pctl Q3 40 'with the two streams SEPARATE' 'with the streams joined' "THE RULE: the real code path, streams SEPARATE"
pctl Q4 40 'do not soften the rule yourself' 'soften it if you like' "THE RULE: not softened by the gate"
pctl RR 41 'A WRONG READING ON ANY REAL SHAPE = NO GO for that PR (blocking)' 'A wrong reading on a real shape is a note for that PR' "THE READER RULE: wrong reading on a real shape is NO GO"
pctl RR2 41 'NAMES it as a shape the check catches' 'mentions it' "THE READER RULE: a shape the PR's own text names counts as real"
pctl MC 42 'T-CALL (iii) MUST NOW RED' 'T-CALL (iii) may stay green' "the must-change list: T-CALL (iii) must now red"
pctl MC2 42 'the {3,2} row present' 'the {3,2} row optional' "the must-change list: the {3,2} row"
pctl Z 43 'never by name, never pid 1' 'by name if needed' "login_stub reaper rule"
pctl SC 44 'DECLARED SCOPE (grade as disclosed scope, never as a defect of the PR)' 'DECLARED SCOPE (grade as you see fit)' "declared scope"
pctl L8 45 'Legs 3/4/8 are NOT RUN in this gate and OWED BY NONE' 'Legs 3/4/8 are owed' "legs 3/4/8 NOT run, owed by none"
pctl AZ 46 'NEVER EXECUTE sync-secrets.sh AND NEVER RUN `az`' 'EXECUTE sync-secrets.sh IF USEFUL' "#1260: never executed, never az"
pctl AZ2 46 'the log MUST stay EMPTY' 'the log may fill' "#1260: the az shim log must stay empty"
pctl EG 47 'READ /etc/hosts' 'SKIP /etc/hosts' "#1261: NODNS-EGRESS measured before the cells run"
pctl A 26 '`GO: merge #1245, #1256, #1257, #1258, #1259, #1260, #1261 batch`' '`GO: merge #1245 batch`' "the GO string"
pctl E 25 'PER PR FILE (2 over 2 paths) for #1245 and #1258, (1 over 1 path) for #1256, #1257, #1259, #1260 and #1261' 'PER PR FILE' "addendum count"
pctl E2 25 'subject <= 92 chars' 'subject any length' "addendum: subject <= 92"
pctl J 23 '[QA -> Wednesday] TIER-2 GATE batch #1245r2 #1256 #1257 #1258 #1259 #1260 #1261 (Seats L6 L5 B28, round 24)' '[QA -> Wednesday] TIER-2 GATE batch #1245r2' "the verdict subject"
for tok in END_TREE END_TREE_NO1245; do
  ET="$(sed -n "s/^$tok='\(.*\)'$/\1/p" "$L")"
  python3 - "$PR" "$CW/W$tok.prompt" "$ET" <<'PY'
import sys
s, d, et = sys.argv[1:4]; t = open(s, encoding='utf-8').read(); assert len(et) == 40 and et in t
open(d, 'w', encoding='utf-8').write(t.replace(et, et[:-1] + ('0' if et[-1] != '0' else '1')))
PY
  cp "$PR" "$CW/W$tok.pristine.prompt"
  judge "W:$tok" 31 "$(QAB24C_PROMPT="$CW/W$tok.prompt" pchk "W$tok")" "the $tok not in full in the prompt"
  judge "W:$tok/twin" 0 "$(QAB24C_PROMPT="$CW/W$tok.pristine.prompt" pchk "W$tok.twin")" "pristine prompt through the same override"
done
QAB24C_CUR_DEV="$PDEV" "$L" < /dev/null > "$CW/N.out" 2>&1; judge N 21 "$?" "LAUNCH path (no --check) with stdin not a TTY — refuses before exec"
QAB24C_CUR_DEV="$PDEV" QAB24C_PROMPT="$PR" "$L" --check > "$CW/N2.out" 2>&1; rc=$?; [ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'TEST OVERRIDE is set' "$CW/N2.out" && rc=94
judge N2 0 "$rc" "an override set is allowed under --check AND reported (the launch path refuses it, exit 16, after the TTY guard)"
mkdir -p "$CW/moved"; cp -p "$L" "$CW/moved/"; QAB24C_CUR_DEV="$PDEV" "$CW/moved/$(basename "$L")" --check > "$CW/M.out" 2>&1; judge M 2 "$?" "the launcher copied out of its filled home (a MOVED KIT)"
QAB24C_CUR_DEV="$PDEV" "$L" --check > "$CW/M.twin.out" 2>&1; judge M/twin 0 "$?" "the same launcher at home"
say "--- repin_and_launch (dry runs / refusals only)"
bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R1.out" 2>&1; judge R1 0 "$?" "dry run, the kit as filled"
doctor "$L" "$CW/R2.launch.sh" "$H59|1|" "${H59%?}$([ "${H59: -1}" = 0 ] && echo 1 || echo 0)|1|" && chmod 755 "$CW/R2.launch.sh"
bash "$REPIN" "$CW/R2.launch.sh" "$SP" --dry-run > "$CW/R2.out" 2>&1; judge R2 11 "$?" "a stale #1259 head pin"
cp -p "$L" "$CW/R2.twin.launch.sh"; bash "$REPIN" "$CW/R2.twin.launch.sh" "$SP" --dry-run > "$CW/R2.twin.out" 2>&1; judge R2/twin 0 "$?" "the same copied-launcher mechanism, pins intact"
doctor "$L" "$CW/R3.launch.sh" "DEVELOP_SHA='$PDEV'" "DEVELOP_SHA='6e2a00bfed577528de1ee02b41cb5a0e99172b35'" && chmod 755 "$CW/R3.launch.sh"
bash "$REPIN" "$CW/R3.launch.sh" "$SP" --dry-run > "$CW/R3.out" 2>&1; judge R3 10 "$?" "the pinned develop is stale (the dry run reports the re-pin and stops)"
: > "$CW/empty_routing.conf"
G24C_ROUTING="$CW/empty_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4.out" 2>&1; judge R4 1 "$?" "a REAL run with the routing line absent stops at step 0 (routing-file override: deterministic)"
printf 'QA/Secuura-batch1245r2|coagent@agentmail.to|yes\n' > "$CW/good_routing.conf"
G24C_ROUTING="$CW/good_routing.conf" bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R4.twin.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'line present: 1 (grep rc=0' "$CW/R4.twin.out" && rc=95
judge R4/twin 0 "$rc" "the routing line present (override file), dry run — AND step 0 reads it as present"
printf 'QA/Secuura-batch1249|coagent@agentmail.to|yes\nQA/Secuura-batch1245|coagent@agentmail.to|yes\n' > "$CW/other_routing.conf"
G24C_ROUTING="$CW/other_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4b.out" 2>&1; judge R4b 1 "$?" "only gate24T2b's pane and a round-1-shaped pane (…batch1245 without r2) routed — this pane is NOT, a real run stops at step 0"
bash "$REPIN" "$L" /tmp > "$CW/R5.out" 2>&1; judge R5 9 "$?" "a scratchpad outside /private/tmp/claude-501/"
say "--- the moved kit, predict and fill (in a COPY of the kit, never the home)"
MK="$CW/movedkit"; mkdir -p "$MK"; /usr/bin/rsync -a --exclude '_sp' --exclude 'launch_*.out' --exclude 'g24c_controls_*' "$GS/" "$MK/"
bash "$MK/repin_and_launch_gate24T2c.sh" "$MK/launch_qa_secuura_batch1245r2-t2.sh" "$SP" --dry-run > "$CW/R6.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'MOVED KIT' "$CW/R6.out" && rc=98
judge R6 0 "$rc" "moved-kit dry run: rc 0 AND reports MOVED KIT"
for s in 1245 1256 1257 1258 1259 1260 1261; do
  python3 "$MK/predict_gate24T2c.py" "$SP" --simulate "foreign$s" > "$CW/P$s.out" 2>&1; judge "P$s" 1 "$?" "predict over develop + a FOREIGN edit of #$s's own file — the base-invariant check (3) refuses"
done
python3 "$MK/predict_gate24T2c.py" "$SP" --simulate mergedT2b > "$CW/PT2Bm.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'run_shell_suites 55, fixture_guard 10' "$CW/PT2Bm.out" && rc=93
judge P-T2Bm 0 "$rc" "predict over develop + squashes of gate24T2b's seven (the expected mover): re-pins cleanly AND reads the fleet STOP moving to 55 / 10"
python3 "$MK/predict_gate24T2c.py" "$SP" > "$CW/P.twin.out" 2>&1; judge P/twin 0 "$?" "predict over origin develop in the same copy (no simulation)"
cp "$MK/pins_gate24T2c.json" "$CW/pins.real.json"; cp "$MK/pins_gate24T2c.SIM-mergedT2b.json" "$MK/pins_gate24T2c.json" 2>> "$CW/F2.cp.err"
if [ -s "$MK/pins_gate24T2c.SIM-mergedT2b.json" ] && ! cmp -s "$CW/pins.real.json" "$MK/pins_gate24T2c.json"; then python3 "$MK/fill_gate24T2c.py" > "$CW/F2.out" 2>&1; rc=$?; else echo "the SIM pins file was not written — the control cannot run" > "$CW/F2.out"; rc=96; fi
judge F2 1 "$rc" "fill refuses a SIMULATED pins file (the mergedT2b SIM pins — a PASSING simulation — asserted present and swapped in first)"
cp "$CW/pins.real.json" "$MK/pins_gate24T2c.json"
python3 "$MK/fill_gate24T2c.py" > "$CW/F1.out" 2>&1; rc=$?
"$MK/launch_qa_secuura_batch1245r2-t2.sh" --check > "$CW/F1.check.out" 2>&1; rc2=$?
[ "$rc" = 0 ] && [ "$rc2" = 0 ] && /usr/bin/grep -q -F "GS='$MK'" "$MK/launch_qa_secuura_batch1245r2-t2.sh" && rc=0 || rc=97
judge F1 0 "$rc" "the moved copy re-filled at its new home: fill rc 0, --check rc 0, its launcher names the new home"
DEV1="$(git -C "$CHECKOUT" ls-remote origin refs/heads/develop | cut -f1)"
[ "$DEV1" = "$DEV0" ] && say "  origin develop UNMOVED during this run ($DEV1)" || say "  ORIGIN DEVELOP MOVED DURING THIS RUN ($DEV0 -> $DEV1): QUARANTINE this run's output and re-run"
say "RESULT $([ "$INV" = 1 ] && echo '(inverted) ')$OK OK / $BAD MISMATCH of $N  $(date -u +%FT%TZ)"
[ "$BAD" = 0 ]
