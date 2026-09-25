#!/bin/bash
# controls_gate24T2b.sh — every guard of the gate24T2b kit, run BOTH WAYS. Each control has a DOCTORED arm (one planted defect; the guard must refuse
# with its own exit code) and, where the mechanism is an override or a copied file, a PRISTINE twin through the SAME mechanism (defect not planted;
# must pass) — so a refusal is attributable to the defect, not to the harness. `--invert` flips every expectation: every control must then report
# MISMATCH (proves each control can fail and the harness can report it). Launches nothing: launcher controls use `--check` (headless) or stop at the
# non-TTY guard; repin controls use `--dry-run`, a bad argv, or a routing-file override that stops at step 0; predict / fill controls run in a MOVED
# COPY of the kit, never the home. Each doctored prompt phrase is chosen OUTSIDE the by-name ladder and the seat items, so the control reaches the rule
# it names (the ladder, exit 33, runs first). Doctored arms are PINNED to the launcher's own develop (pchk) so a develop move mid-run cannot mask them as
# exit 17 (N, N2, M and M/twin too: a develop move mid-run invalidated the first run, controls_0_aborted_devmove.out). The stack is controlled BOTH ways: a moved #1248 must refuse (C3, R2s, P1248), a SQUASHED #1248 must re-pin cleanly (P1248m, a POSITIVE
# simulation). Writes only under <scratchpad>/g24b_controls_*. Derived from gate24T2a's controls, re-keyed to SEVEN rows + the stack.
# Usage: controls_gate24T2b.sh <scratchpad dir> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
SP="${1:-}"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no scratchpad $SP"; exit 9; } ;; *) echo "usage: controls_gate24T2b.sh <scratchpad> [--invert]"; exit 9;; esac
L="$GS/launch_qa_secuura_batch1249-t2.sh"; PR="$GS/2026-09-26_secuura-batch1249-t2.prompt.txt"; CAP="$GS/mail_gate24T2b_ready.md"
REPIN="$GS/repin_and_launch_gate24T2b.sh"
CW="$SP/g24b_controls_$(date -u +%H%M%S)$([ "$INV" = 1 ] && echo _inv)"; mkdir -p "$CW"
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
pchk() { QAB24B_CUR_DEV="${QAB24B_CUR_DEV:-$PDEV}" "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
pctl() { # id want old new label
  local id="$1" want="$2"; doctor "$PR" "$CW/$id.prompt" "$3" "$4" || { judge "$id" "$want" 99 "DOCTOR FAILED: $5"; return; }
  cp "$PR" "$CW/$id.pristine.prompt"
  judge "$id" "$want" "$(QAB24B_PROMPT="$CW/$id.prompt" pchk "$id")" "$5"
  judge "$id/twin" 0 "$(QAB24B_PROMPT="$CW/$id.pristine.prompt" pchk "$id.twin")" "$5 — pristine copy through the same override"
}
hd() { sed -n "s/^  \"$1|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|.*$/\1/p" "$L"; }
H49="$(hd 1249)"; H53="$(hd 1253)"; H55="$(hd 1255)"; PDEV="$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$L")"; S48="$(sed -n "s/^STACK_1248='\(.*\)'$/\1/p" "$L")"
[ -n "$H49" ] && [ -n "$H53" ] && [ -n "$H55" ] && [ -n "$PDEV" ] && [ -n "$S48" ] || { echo "REFUSING: could not read the #1249 / #1253 / #1255 rows / DEVELOP_SHA / STACK_1248 from $L"; exit 9; }
P50="Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh,Blockchain/Dev/scripts/run-shell-suites.sh"
P54="Blockchain/Dev/packages/shared/src/__tests__/support/walkTimeouts.setup.ts,Blockchain/Dev/packages/shared/src/__tests__/walkTimeouts.test.ts,Blockchain/Dev/packages/shared/vitest.config.ts"
say "controls_gate24T2b.sh $(date -u +%FT%TZ)$([ "$INV" = 1 ] && echo ' --invert') | kit $GS | work $CW"
say "--- launcher (--check unless stated)"
judge P 0 "$(chk P)" "positive: the kit as filled"
judge C 6 "$(QAB24B_HEAD_1249=0000000000000000000000000000000000000000 pchk C)" "stale #1249 head"
judge C2 6 "$(QAB24B_HEAD_1249="$S48" pchk C2)" "#1248's head pinned as #1249's (the stack base, not the PR)"
judge C3 6 "$(QAB24B_STACK_1248="$H49" pchk C3)" "the STACK base moved: #1248's pin is not what refs/pull/1248/head reads"
judge C4 6 "$(QAB24B_HEAD_1255="$H53" pchk C4)" "#1253's head pinned as #1255's"
judge C/twin 0 "$(QAB24B_HEAD_1249="$H49" QAB24B_HEAD_1255="$H55" QAB24B_STACK_1248="$S48" pchk C.twin)" "the real #1249 / #1255 heads and the real stack pin through the same overrides"
judge D 17 "$(QAB24B_CUR_DEV=6e2a00bfed577528de1ee02b41cb5a0e99172b35 chk D)" "develop moved (BASE 6e2a00bfe as the current develop)"
judge D/twin 0 "$(QAB24B_CUR_DEV="$PDEV" chk D.twin)" "the pinned develop through the same override"
judge V 10 "$(QAB24B_PATHS_1250="${P50/run-shell-suites.sh/run_shell_suites.sh}" pchk V)" "base-invariant compare: #1250 with a same-count WRONG path name"
judge V2 10 "$(QAB24B_PATHS_1254="${P54//packages\/shared/packages\/common}" pchk V2)" "base-invariant compare: #1254 with WRONG paths (another package)"
judge V/twin 0 "$(QAB24B_PATHS_1250="$P50" QAB24B_PATHS_1254="$P54" pchk V.twin)" "the right paths through the same override"
doctor "$CAP" "$CW/O.cap" 'Arm B1 disables the walk. It reds the four new controls and does NOT red J2.' 'Arm B1 disables the walk.' && cp "$CAP" "$CW/O.pristine.cap"
judge O 30 "$(QAB24B_BRIEF="$CW/O.cap" pchk O)" "capture missing a seat item (#1249's arm B1 sentence)"
judge O/twin 0 "$(QAB24B_BRIEF="$CW/O.pristine.cap" pchk O.twin)" "pristine capture through the same override"
pctl G 8 $'ultrathink\n' $'think\n' "no thinking directive"
pctl U 8 'PR #1251 is KS-1147.' 'PR #1251 is {{KS_1147}}.' "an unfilled fill token"
pctl H20 20 '59245ff0b11c6b760ba5e2a9daedc5927e915e10' '59245ff0b11c6b760ba5e2a9daedc5927e915e1X' "the prompt names a wrong #1255 head"
pctl T 32 'PR #1251 is KS-1147.' 'PR #1251 is KS-1148.' "ticket statement for #1251"
pctl T2 32 'PR #1250 is KS-1302 + KS-1303.' 'PR #1250 is KS-1302.' "ticket statement for #1250 (a two-key row)"
pctl I 7 '#1253 T2' '#1253 T3' "tier line for #1253"
pctl I2 7 'The batch is FROZEN at seven' 'The batch is FROZEN at six' "the batch frozen at seven"
pctl K 33 'TRAILING-PIPE' 'TRAIL-PIPE' "a by-name keyword (TRAILING-PIPE, every occurrence)"
pctl B 34 'a sibling batch merging is not a difference' 'a sibling batch merging is a difference' "base-invariant rule"
pctl B2 34 'there is no declared exception here for any other path' 'an overlap is fine here' "only #1248 ∩ #1249 is declared: a move on any other own path STOPS"
pctl B3 34 'declare any overlap you find with its merged-blob target' 'ignore any overlap you find' "pairwise: declare any overlap with its merged-blob target"
pctl S 35 'NO Docker action of any kind' 'a Docker action if useful' "no Docker"
pctl S2 35 'NEVER connect to it' 'connect as needed' "never the native :5432"
pctl X 36 'restore by bytes' 'restore somehow' "red-proof rule: restore by bytes"
pctl X2 36 'in YOUR OWN clone' 'in the shared checkout' "red proof in the tester's own clone"
pctl F 37 '`fixture_guard` 10/0 (#1253), `run_shell_suites` 55/0 (#1250)' '`fixture_guard` 6/0, `run_shell_suites` 49/0' "fleet STOP: the NEW counts after #1250 and #1253"
pctl F2 37 'was OVERWRITTEN by the seat' 'was kept by the seat' "fleet STOP: #1255's record overwritten, read by the drafter before"
pctl F3 37 'NO STANDALONE RUN of' 'A STANDALONE RUN of' "fleet STOP: no standalone run beyond the two changed suites"
pctl Y 38 'pre-existing (KS-562), not caused by this change"' 'pre-existing, not caused by this change"' "the anchoring wording"
pctl Y2 38 'an ASSERTION failure is REAL' 'an ASSERTION failure is noise' "the load rule"
pctl Hh 39 'NEVER WRITE THE SHARED CHECKOUT' 'WRITE THE SHARED CHECKOUT IF NEEDED' "holds: the shared checkout"
pctl H2 39 'NO ticket filed' 'tickets may be filed' "holds: no ticket filed"
pctl Q 40 'A WRONG READING ON ANY REAL SHAPE = NO GO for that PR (blocking)' 'A wrong reading is a note' "THE READER RULE: a wrong reading on a real shape is NO GO"
pctl Q2 40 'NAMES it as a shape the check catches' 'mentions it' "THE READER RULE: a shape the PR's own text names counts as real"
pctl Q3 40 'THROUGH THE REAL CODE PATH — never a lifted regex, never a Python port' 'through whatever path is easiest' "THE READER RULE: the real code path, never a port"
pctl Q4 40 'do not soften the rule yourself' 'soften it if you like' "THE READER RULE: not softened by the gate"
pctl R 41 'exits 0 OR prints a green `shell suites:` verdict OR runs a further suite = NO GO for #1250 (blocking)' 'behaves oddly is a note' "#1250 TRAP: a killed runner reading green is NO GO"
pctl R2 41 "SIGTERM sent to the RUNNER's own pid (by pid, never by name)" 'SIGTERM sent somehow' "#1250 TRAP: signal the runner by pid"
pctl N42 42 '#1249 is graded over develop + #1248' '#1249 is graded over develop' "#1249 graded over develop + #1248"
pctl N42b 42 'its MERGE ADDENDUM line is the HOLD form ("HOLD: #1248 not GO")' 'its MERGE ADDENDUM line stands' "#1249 HOLDs when #1248 is not GO"
pctl Z 43 'never by name, never pid 1' 'by name if needed' "login_stub reaper rule"
pctl SC 44 'grade it NOT MEASURED, never as a defect of #1254' 'grade it as a defect of #1254' "KS-1155's load >= 30 bar is disclosed scope"
pctl L8 45 '#1252 is NO GO until they run' '#1252 may proceed anyway' "legs 3/4/8: a changed field makes them owed"
pctl L8b 45 'They are NOT RUN in this gate: NO Docker, NO database.' 'Run them.' "legs 3/4/8 are NOT run (no Docker, no DB)"
pctl A 26 '`GO: merge #1249, #1250, #1251, #1252, #1253, #1254, #1255 batch`' '`GO: merge #1249 batch`' "the GO string"
pctl A2 26 '#1249 ONLY AFTER #1248 is on develop' '#1249 in any order' "the GO carries #1249 after #1248"
pctl E 25 'PER PR FILE (1 over 1 path) for #1249, #1251, #1253 and #1255, (2 over 2 paths) for #1250, (3 over 3 paths) for #1252 and #1254' 'PER PR FILE' "addendum count"
pctl E2 25 'FLEET STOP after this merge' 'counts after this merge' "addendum carries the fleet STOP after each merge"
pctl J 23 '[QA -> Wednesday] TIER-2 GATE batch #1249 #1250 #1251 #1252 #1253 #1254 #1255 (Seats L6 L5 B28, round 24)' '[QA -> Wednesday] TIER-2 GATE batch #1249' "the verdict subject"
for tok in END_TREE END_TREE_NOSTACK; do
  ET="$(sed -n "s/^$tok='\(.*\)'$/\1/p" "$L")"
  python3 - "$PR" "$CW/W$tok.prompt" "$ET" <<'PY'
import sys
s, d, et = sys.argv[1:4]; t = open(s, encoding='utf-8').read(); assert len(et) == 40 and et in t
open(d, 'w', encoding='utf-8').write(t.replace(et, et[:-1] + ('0' if et[-1] != '0' else '1')))
PY
  cp "$PR" "$CW/W$tok.pristine.prompt"
  judge "W:$tok" 31 "$(QAB24B_PROMPT="$CW/W$tok.prompt" pchk "W$tok")" "the $tok not in full in the prompt"
  judge "W:$tok/twin" 0 "$(QAB24B_PROMPT="$CW/W$tok.pristine.prompt" pchk "W$tok.twin")" "pristine prompt through the same override"
done
QAB24B_CUR_DEV="$PDEV" "$L" < /dev/null > "$CW/N.out" 2>&1; judge N 21 "$?" "LAUNCH path (no --check) with stdin not a TTY — refuses before exec"
QAB24B_CUR_DEV="$PDEV" QAB24B_PROMPT="$PR" "$L" --check > "$CW/N2.out" 2>&1; rc=$?; [ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'TEST OVERRIDE is set' "$CW/N2.out" && rc=94
judge N2 0 "$rc" "an override set is allowed under --check AND reported (the launch path refuses it, exit 16, after the TTY guard)"
mkdir -p "$CW/moved"; cp -p "$L" "$CW/moved/"; QAB24B_CUR_DEV="$PDEV" "$CW/moved/$(basename "$L")" --check > "$CW/M.out" 2>&1; judge M 2 "$?" "the launcher copied out of its filled home (a MOVED KIT)"
QAB24B_CUR_DEV="$PDEV" "$L" --check > "$CW/M.twin.out" 2>&1; judge M/twin 0 "$?" "the same launcher at home"
say "--- repin_and_launch (dry runs / refusals only)"
bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R1.out" 2>&1; judge R1 0 "$?" "dry run, the kit as filled"
doctor "$L" "$CW/R2.launch.sh" "$H53|1|" "${H53%?}$([ "${H53: -1}" = 0 ] && echo 1 || echo 0)|1|" && chmod 755 "$CW/R2.launch.sh"
bash "$REPIN" "$CW/R2.launch.sh" "$SP" --dry-run > "$CW/R2.out" 2>&1; judge R2 11 "$?" "a stale #1253 head pin"
doctor "$L" "$CW/R2s.launch.sh" "STACK_1248='$S48'" "STACK_1248='${S48%?}$([ "${S48: -1}" = 0 ] && echo 1 || echo 0)'" && chmod 755 "$CW/R2s.launch.sh"
bash "$REPIN" "$CW/R2s.launch.sh" "$SP" --dry-run > "$CW/R2s.out" 2>&1; judge R2s 11 "$?" "a stale STACK pin (#1248 moved under #1249)"
cp -p "$L" "$CW/R2.twin.launch.sh"; bash "$REPIN" "$CW/R2.twin.launch.sh" "$SP" --dry-run > "$CW/R2.twin.out" 2>&1; judge R2/twin 0 "$?" "the same copied-launcher mechanism, pins intact"
doctor "$L" "$CW/R3.launch.sh" "DEVELOP_SHA='$PDEV'" "DEVELOP_SHA='6e2a00bfed577528de1ee02b41cb5a0e99172b35'" && chmod 755 "$CW/R3.launch.sh"
bash "$REPIN" "$CW/R3.launch.sh" "$SP" --dry-run > "$CW/R3.out" 2>&1; judge R3 10 "$?" "the pinned develop is stale (the dry run reports the re-pin and stops)"
: > "$CW/empty_routing.conf"
G24B_ROUTING="$CW/empty_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4.out" 2>&1; judge R4 1 "$?" "a REAL run with the routing line absent stops at step 0 (routing-file override: deterministic)"
printf 'QA/Secuura-batch1249|coagent@agentmail.to|yes\n' > "$CW/good_routing.conf"
G24B_ROUTING="$CW/good_routing.conf" bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R4.twin.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'line present: 1 (grep rc=0' "$CW/R4.twin.out" && rc=95
judge R4/twin 0 "$rc" "the routing line present (override file), dry run — AND step 0 reads it as present"
printf 'QA/Secuura-batch1243|coagent@agentmail.to|yes\n' > "$CW/other_routing.conf"
G24B_ROUTING="$CW/other_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4b.out" 2>&1; judge R4b 1 "$?" "only gate24T2a's pane line present — this pane is NOT routed, a real run stops at step 0"
bash "$REPIN" "$L" /tmp > "$CW/R5.out" 2>&1; judge R5 9 "$?" "a scratchpad outside /private/tmp/claude-501/"
say "--- the moved kit, predict and fill (in a COPY of the kit, never the home)"
MK="$CW/movedkit"; mkdir -p "$MK"; /usr/bin/rsync -a --exclude '_sp' --exclude 'launch_*.out' --exclude 'g24b_controls_*' "$GS/" "$MK/"
bash "$MK/repin_and_launch_gate24T2b.sh" "$MK/launch_qa_secuura_batch1249-t2.sh" "$SP" --dry-run > "$CW/R6.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'MOVED KIT' "$CW/R6.out" && rc=98
judge R6 0 "$rc" "moved-kit dry run: rc 0 AND reports MOVED KIT"
for s in 1249 1250 1251 1252 1253 1254 1255 1248; do
  python3 "$MK/predict_gate24T2b.py" "$SP" --simulate "foreign$s" > "$CW/P$s.out" 2>&1; judge "P$s" 1 "$?" "predict over develop + a FOREIGN edit of #$s's own file — the base-invariant check (3) refuses"
done
python3 "$MK/predict_gate24T2b.py" "$SP" --simulate merged1248 > "$CW/P1248m.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'STACK MODE: merged' "$CW/P1248m.out" && rc=93
judge P1248m 0 "$rc" "predict over develop + a SQUASH of #1248 (the expected next state): re-pins cleanly AND reads STACK MODE merged"
python3 "$MK/predict_gate24T2b.py" "$SP" > "$CW/P.twin.out" 2>&1; judge P/twin 0 "$?" "predict over origin develop in the same copy (no simulation)"
cp "$MK/pins_gate24T2b.json" "$CW/pins.real.json"; cp "$MK/pins_gate24T2b.SIM-merged1248.json" "$MK/pins_gate24T2b.json" 2>> "$CW/F2.cp.err"
if [ -s "$MK/pins_gate24T2b.SIM-merged1248.json" ] && ! cmp -s "$CW/pins.real.json" "$MK/pins_gate24T2b.json"; then python3 "$MK/fill_gate24T2b.py" > "$CW/F2.out" 2>&1; rc=$?; else echo "the SIM pins file was not written — the control cannot run" > "$CW/F2.out"; rc=96; fi
judge F2 1 "$rc" "fill refuses a SIMULATED pins file (the merged1248 SIM pins — a PASSING simulation — asserted present and swapped in first)"
cp "$CW/pins.real.json" "$MK/pins_gate24T2b.json"
python3 "$MK/fill_gate24T2b.py" > "$CW/F1.out" 2>&1; rc=$?
"$MK/launch_qa_secuura_batch1249-t2.sh" --check > "$CW/F1.check.out" 2>&1; rc2=$?
[ "$rc" = 0 ] && [ "$rc2" = 0 ] && /usr/bin/grep -q -F "GS='$MK'" "$MK/launch_qa_secuura_batch1249-t2.sh" && rc=0 || rc=97
judge F1 0 "$rc" "the moved copy re-filled at its new home: fill rc 0, --check rc 0, its launcher names the new home"
say "RESULT $([ "$INV" = 1 ] && echo '(inverted) ')$OK OK / $BAD MISMATCH of $N  $(date -u +%FT%TZ)"
[ "$BAD" = 0 ]
