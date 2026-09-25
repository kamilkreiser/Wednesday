#!/bin/bash
# controls_gate21T1d.sh — every guard of the kit, run BOTH WAYS. Each control has a DOCTORED arm (one planted defect; the guard must refuse with its
# own exit code) and a PRISTINE twin through the SAME mechanism (same override / same copied file, defect not planted; must pass) — so a refusal is
# attributable to the defect, not to the harness. `--invert` flips every expectation: every control must then report MISMATCH (proves the harness can
# fail). Launches nothing: launcher controls use `--check` (headless) or stop at the non-TTY guard; repin controls use `--dry-run`, a bad argv, or a
# routing-file override that stops at step 0; predict controls run in a MOVED COPY of the kit. Writes only under <scratchpad>/g21T1d_controls_*.
# The doctored arms and their twins run with develop PINNED to the launcher's own pin (pchk: QAB1239_CUR_DEV), so a develop move DURING a controls run
# cannot mask a doctored arm as exit 17 (the tier-2d drafter's fix: #1234 landed mid-run and 73 arms read 17). P, D/twin, M/twin, N2 and the repin arms
# read the LIVE develop.
# Usage: controls_gate21T1d.sh <scratchpad dir> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
SP="${1:-}"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no scratchpad $SP"; exit 9; } ;; *) echo "usage: controls_gate21T1d.sh <scratchpad> [--invert]"; exit 9;; esac
L="$GS/launch_qa_secuura_batch1239-t1r2.sh"; PR="$GS/2026-09-25_secuura-batch1239-t1r2.prompt.txt"; CAP="$GS/mail_gate21T1d_ready.md"
REPIN="$GS/repin_and_launch_gate21T1d.sh"
CW="$SP/g21T1d_controls_$(date -u +%H%M%S)"; mkdir -p "$CW"
PDEV="$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$L")"
PHEAD='c8e1875c21e994a746e36c8b8efec8de1d9dbc98'
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
# doctor <src> <dst> <old> <new>: copy with ONE planted defect (every occurrence); refuses (rc 99) if <old> is absent, so a control never passes vacuously
doctor() { python3 - "$1" "$2" "$3" "$4" <<'PY'
import re, sys
s, d, o, n = sys.argv[1:5]
t = open(s, encoding='utf-8').read()
# whitespace-tolerant: the prompt is hard-wrapped, and the launcher's `has` checks read it whitespace-joined
rx = re.compile(r'\s+'.join(re.escape(w) for w in o.split(' ')))
t2, k = rx.subn(lambda m: n, t)
if k == 0: print('DOCTOR: anchor absent: %r' % o[:80]); sys.exit(99)
open(d, 'w', encoding='utf-8').write(t2)
PY
}
chk() { "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
pchk() { QAB1239_CUR_DEV="${QAB1239_CUR_DEV:-$PDEV}" "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
# a prompt control: doctored arm + pristine twin through QAB1239_PROMPT, develop pinned
pctl() { # id want old new label
  local id="$1" want="$2"; doctor "$PR" "$CW/$id.prompt" "$3" "$4" || { judge "$id" "$want" 99 "DOCTOR FAILED: $5"; return; }
  cp "$PR" "$CW/$id.pristine.prompt"
  judge "$id" "$want" "$(QAB1239_PROMPT="$CW/$id.prompt" pchk "$id")" "$5"
  judge "$id/twin" 0 "$(QAB1239_PROMPT="$CW/$id.pristine.prompt" pchk "$id.twin")" "$5 — pristine copy through the same override"
}
say "controls_gate21T1d.sh $(date -u +%FT%TZ)$([ "$INV" = 1 ] && echo ' --invert') | kit $GS | work $CW | pinned develop for doctored arms $PDEV"
say "--- launcher (--check unless stated)"
judge P 0 "$(chk P)" "positive: the kit as filled, LIVE develop"
judge C 6 "$(QAB1239_HEAD=0000000000000000000000000000000000000000 pchk C)" "stale #1239 head"
judge C2 6 "$(QAB1239_HEAD=42c20e998a1a69887b8378968a8ff4f19106c24b pchk C2)" "the ROUND-1 head 42c20e998 (a real sha, no longer the PR head)"
judge C/twin 0 "$(QAB1239_HEAD="$PHEAD" pchk C.twin)" "the real #1239 head through the same override"
judge D 17 "$(QAB1239_CUR_DEV=c41e268eb9355fe06eed7590455aa2fbbd90c59b chk D)" "develop moved (the previous develop c41e268eb)"
judge D/twin 0 "$(QAB1239_CUR_DEV="$PDEV" chk D.twin)" "the pinned develop through the same override"
PATHS_OK="$(sed -n 's/^  "1239|[^|]*|[^|]*|[0-9a-f]\{40\}|[0-9]*|[0-9]*|\([^"]*\)"$/\1/p' "$L")"
judge V 10 "$(QAB1239_PATHS="$(printf '%s' "$PATHS_OK" | sed 's/shareRepo\.ts/shareRepo.TS/')" pchk V)" "base-invariant compare: a same-count WRONG path name"
judge V/twin 0 "$(QAB1239_PATHS="$PATHS_OK" pchk V.twin)" "the right paths through the same override"
doctor "$CAP" "$CW/O.cap" 'Expected: 0, Received: 1' 'Expected: 0, Received: 2' && cp "$CAP" "$CW/O.pristine.cap"
judge O 30 "$(QAB1239_BRIEF="$CW/O.cap" pchk O)" "capture missing a seat item ('Expected: 0, Received: 1')"
judge O/twin 0 "$(QAB1239_BRIEF="$CW/O.pristine.cap" pchk O.twin)" "pristine capture through the same override"
pctl G 8 $'ultrathink\n' $'think\n' "no thinking directive"
pctl U 8 'PR #1239 is KS-1263.' 'PR #1239 is {{KS_1263}}.' "an unfilled fill token"
pctl H20 20 "$PHEAD" 'c8e1875c21e994a746e36c8b8efec8de1d9dbc9X' "the prompt names a wrong head"
pctl T 32 'PR #1239 is KS-1263.' 'PR #1239 is KS-1264.' "the ticket statement"
pctl I 7 '#1239 T1' '#1239 T2' "the tier line"
pctl I2 7 'THE CAP: a NO GO now SHIPS NOTHING' 'a NO GO goes to a round 3' "the round-2-of-2 cap"
pctl K 33 'T-TRAP' 'T-TRAQ' "a by-name keyword (T-TRAP)"
pctl K2 33 "THE SEAT'S PLATFORM DB" "THE SEAT'S DB" "a by-name keyword (lead b)"
pctl B 34 'NONE lies inside the two handlers the cells reach' 'SOME lie inside the two handlers' "the region rule"
pctl B2 34 'a move touching the handlers, db.ts, shareRepo.ts or packages/shared/src/db = STOP' 'a move touching the handlers = note it' "the region STOP on a develop move"
pctl S 35 'the FIRST N in 55450..55459' 'the FIRST N in 55432..55459' "disposable DB: the port range"
pctl S2 35 'REPORTED and NEVER touched' 'REPORTED and may be touched' "disposable DB: foreign containers"
pctl S3 35 'NO SECUURA STACK SLOT IS USED' 'A SECUURA STACK SLOT MAY BE USED' "disposable DB: never a slot"
pctl S4 35 'PROOF OF GONE' 'CLEANUP' "disposable DB: the proof of gone"
pctl R 36 'PROVE IT IN MODE T' 'PROVE IT IN EITHER MODE' "Wednesday's ruling (b): MODE T"
pctl R2 36 'NEVER PASS MISLABELLED' 'MAY PASS' "MODE F must fail loud"
pctl R3 36 'RED-ATTRIBUTION: the red names ROWS' 'RED-ATTRIBUTION: any red counts' "the BASE red must name rows"
pctl R4 36 'THIS IS THE SECOND INSTRUMENT' 'THIS IS OPTIONAL' "the W2 statement-log witness"
pctl R5 36 'getTenantManager() is null' 'the manager is missing' "T-TRAP names the refusal"
pctl F 37 'F1 ROLLBACK-CELLS-SCHEMA (Major)' 'F1 ROLLBACK-CELLS-SCHEMA (Minor)' "round-1 dispositions: F1's class"
pctl F2 37 'F6 POOL-IDENTITY (Minor): TICKETED as KS-1304' 'F6 POOL-IDENTITY (Minor): open' "round-1 dispositions: F6 ticketed"
pctl Y 38 'pre-existing (KS-562), not caused by this change"' 'pre-existing, not caused by this change"' "the anchoring wording"
pctl Y2 38 'an ASSERTION failure is REAL' 'an ASSERTION failure is noise' "the load rule"
pctl Hh 39 'NEVER WRITE THE SHARED CHECKOUT' 'WRITE THE SHARED CHECKOUT IF NEEDED' "holds: the shared checkout"
pctl Z 43 'never by name, never pid 1' 'by name if needed' "login_stub reaper rule"
pctl A 26 '`GO: merge #1239 batch`' '`GO: merge #1239`' "the GO string"
pctl E 25 'Exactly ONE equality target PER PR FILE (6 over 6 paths)' 'Exactly ONE equality target PER PR FILE' "addendum counts"
pctl E2 25 'the squash body drops KS-1155 and KS-1228' 'the squash body may keep KS-1155 and KS-1228' "MG-3: own key only"
pctl J 23 '[QA -> Wednesday] TIER-1 GATE #1239 KS-1263 round 2 of 2 (Seat B 27th)' '[QA -> Wednesday] TIER-1 GATE #1239 round 2' "the verdict subject"
ET="$(sed -n "s/^END_TREE='\(.*\)'$/\1/p" "$L")"
for W in "W:$ET:the END_TREE" "W2:42c20e998a1a69887b8378968a8ff4f19106c24b:the round-1 head R1"; do
  id="${W%%:*}"; rest="${W#*:}"; sha="${rest%%:*}"; lab="${rest#*:}"
  python3 - "$PR" "$CW/$id.prompt" "$sha" <<'PY'
import sys
s, d, sha = sys.argv[1:4]; t = open(s, encoding='utf-8').read(); assert sha in t
open(d, 'w', encoding='utf-8').write(t.replace(sha, sha[:-1] + ('0' if sha[-1] != '0' else '1')))
PY
  cp "$PR" "$CW/$id.pristine.prompt"
  judge "$id" 31 "$(QAB1239_PROMPT="$CW/$id.prompt" pchk "$id")" "$lab not in full in the prompt"
  judge "$id/twin" 0 "$(QAB1239_PROMPT="$CW/$id.pristine.prompt" pchk "$id.twin")" "pristine prompt through the same override"
done
"$L" < /dev/null > "$CW/N.out" 2>&1; judge N 21 "$?" "LAUNCH path (no --check) with stdin not a TTY — refuses before exec"
QAB1239_PROMPT="$PR" "$L" --check > "$CW/N2.out" 2>&1; judge N2 0 "$?" "an override set is allowed under --check (the launch path refuses it, exit 16, after the TTY guard)"
mkdir -p "$CW/moved"; cp -p "$L" "$CW/moved/"; "$CW/moved/$(basename "$L")" --check > "$CW/M.out" 2>&1; judge M 2 "$?" "the launcher copied out of its filled home (a MOVED KIT)"
"$L" --check > "$CW/M.twin.out" 2>&1; judge M/twin 0 "$?" "the same launcher at home"
say "--- repin_and_launch (dry runs / refusals only)"
bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R1.out" 2>&1; judge R1 0 "$?" "dry run, the kit as filled"
doctor "$L" "$CW/R2.launch.sh" "$PHEAD|6|2|" 'c8e1875c21e994a746e36c8b8efec8de1d9dbc99|6|2|' && chmod 755 "$CW/R2.launch.sh"
bash "$REPIN" "$CW/R2.launch.sh" "$SP" --dry-run > "$CW/R2.out" 2>&1; judge R2 11 "$?" "a stale #1239 head pin"
cp -p "$L" "$CW/R2.twin.launch.sh"; bash "$REPIN" "$CW/R2.twin.launch.sh" "$SP" --dry-run > "$CW/R2.twin.out" 2>&1; judge R2/twin 0 "$?" "the same copied-launcher mechanism, pins intact"
doctor "$L" "$CW/R3.launch.sh" "DEVELOP_SHA='$PDEV'" "DEVELOP_SHA='c41e268eb9355fe06eed7590455aa2fbbd90c59b'" && chmod 755 "$CW/R3.launch.sh"
bash "$REPIN" "$CW/R3.launch.sh" "$SP" --dry-run > "$CW/R3.out" 2>&1; judge R3 10 "$?" "the pinned develop is stale (the dry run reports the re-pin and stops)"
: > "$CW/empty_routing.conf"
G21T1D_ROUTING="$CW/empty_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4.out" 2>&1; judge R4 1 "$?" "a REAL run with the routing line absent stops at step 0 (routing file override: deterministic)"
printf 'QA/Secuura-batch1239|coagent@agentmail.to|yes\n' > "$CW/good_routing.conf"
G21T1D_ROUTING="$CW/good_routing.conf" bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R4.twin.out" 2>&1; judge R4/twin 0 "$?" "the routing line present (override file), dry run"
bash "$REPIN" "$L" /tmp > "$CW/R5.out" 2>&1; judge R5 9 "$?" "a scratchpad outside /private/tmp/claude-501/"
say "--- the moved kit and predict (in a COPY of the kit, never the home)"
MK="$CW/movedkit"; mkdir -p "$MK"; /usr/bin/rsync -a --exclude '_meas' --exclude 'launch_*.out' --exclude 'controls_*.out' "$GS/" "$MK/"
bash "$MK/repin_and_launch_gate21T1d.sh" "$MK/launch_qa_secuura_batch1239-t1r2.sh" "$SP" --dry-run > "$CW/R6.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -i 'MOVED KIT' "$CW/R6.out" && rc=98
judge R6 0 "$rc" "moved-kit dry run: rc 0 AND reports MOVED KIT"
python3 "$MK/predict_gate21T1d.py" "$SP" --develop 379c6eb1d45905f398fae67ee7dd2f46ad40432f > "$CW/P1.out" 2>&1; judge P1 1 "$?" "predict over an OLDER develop (379c6eb1d: the two overlaps absent) — the overlap guard refuses"
python3 "$MK/predict_gate21T1d.py" "$SP" --develop "$PDEV" > "$CW/P1.twin.out" 2>&1; judge P1/twin 0 "$?" "predict over the PINNED develop through the same override"
python3 "$MK/predict_gate21T1d.py" "$SP" --develop "$PDEV" --pretend-hunk 2200 > "$CW/P2.out" 2>&1; judge P2 1 "$?" "region guard: a synthetic move hunk at BASE line 2200 (inside /:id/share) refuses"
python3 "$MK/predict_gate21T1d.py" "$SP" --develop "$PDEV" --pretend-hunk 1700 > "$CW/P3.out" 2>&1; judge P3 1 "$?" "region guard: a synthetic move hunk at BASE line 1700 (inside /:id/transfer-custody) refuses"
python3 "$MK/predict_gate21T1d.py" "$SP" --develop "$PDEV" --pretend-hunk 2400 > "$CW/P2.twin.out" 2>&1; judge P2/twin 0 "$?" "region guard: the same mechanism at BASE line 2400 (inside /:id/revoke) passes"
python3 "$MK/predict_gate21T1d.py" "$SP" > "$CW/F0.out" 2>&1; rc0=$?
python3 "$MK/fill_gate21T1d.py" > "$CW/F1.out" 2>&1; rc=$?
"$MK/launch_qa_secuura_batch1239-t1r2.sh" --check > "$CW/F1.check.out" 2>&1; rc2=$?
[ "$rc0" = 0 ] && [ "$rc" = 0 ] && [ "$rc2" = 0 ] && /usr/bin/grep -q -F "GS='$MK'" "$MK/launch_qa_secuura_batch1239-t1r2.sh" && rc=0 || rc=97
judge F1 0 "$rc" "the moved copy re-measured + re-filled at its new home: predict rc 0, fill rc 0, --check rc 0, its launcher names the new home"
say "RESULT $([ "$INV" = 1 ] && echo '(inverted) ')$OK OK / $BAD MISMATCH of $N  $(date -u +%FT%TZ)"
[ "$BAD" = 0 ]
