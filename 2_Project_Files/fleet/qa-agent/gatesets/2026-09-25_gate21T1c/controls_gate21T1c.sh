#!/bin/bash
# controls_gate21T1c.sh — every guard of the kit, run BOTH WAYS. Each control has a DOCTORED arm (one planted defect; the guard must refuse with its
# own exit code) and a PRISTINE twin through the SAME mechanism (same override / same copied file, defect not planted; must pass) — so a refusal is
# attributable to the defect, not to the harness. `--invert` flips every expectation: every control must then report MISMATCH (proves the harness
# can fail). Launches nothing: launcher controls use `--check` (headless) or stop at the non-TTY guard; repin controls use `--dry-run`, a bad argv,
# or a routing file override that stops at step 0; predict controls run in a MOVED COPY of the kit. Writes only under <scratchpad>/g21c_controls_*.
# Usage: controls_gate21T1c.sh <scratchpad dir> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
SP="${1:-}"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no scratchpad $SP"; exit 9; } ;; *) echo "usage: controls_gate21T1c.sh <scratchpad> [--invert]"; exit 9;; esac
L="$GS/launch_qa_secuura_batch1234-t1.sh"; PR="$GS/2026-09-25_secuura-batch1234-t1.prompt.txt"; CAP="$GS/mail_gate21T1c_ready.md"
REPIN="$GS/repin_and_launch_gate21T1c.sh"
CW="$SP/g21c_controls_$(date -u +%H%M%S)"; mkdir -p "$CW"
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
# doctor <src> <dst> <old> <new>: copy with ONE planted defect; refuses (rc 99) if <old> is absent, so a control can never pass vacuously
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
# a prompt control: doctored arm + pristine twin through QAB1234_PROMPT
pctl() { # id want old new label
  local id="$1" want="$2"; doctor "$PR" "$CW/$id.prompt" "$3" "$4" || { judge "$id" "$want" 99 "DOCTOR FAILED: $5"; return; }
  cp "$PR" "$CW/$id.pristine.prompt"
  judge "$id" "$want" "$(QAB1234_PROMPT="$CW/$id.prompt" chk "$id")" "$5"
  judge "$id/twin" 0 "$(QAB1234_PROMPT="$CW/$id.pristine.prompt" chk "$id.twin")" "$5 — pristine copy through the same override"
}
say "controls_gate21T1c.sh $(date -u +%FT%TZ)$([ "$INV" = 1 ] && echo ' --invert') | kit $GS | work $CW"
say "--- launcher (--check unless stated)"
judge P 0 "$(chk P)" "positive: the kit as filled"
judge C 6 "$(QAB1234_HEAD_1239=0000000000000000000000000000000000000000 chk C)" "stale #1239 head"
judge C/twin 0 "$(QAB1234_HEAD_1239=42c20e998a1a69887b8378968a8ff4f19106c24b chk C.twin)" "the real #1239 head through the same override"
judge D 17 "$(QAB1234_CUR_DEV=aa600af94d69ad59db279d32cbbd7596931a739b chk D)" "develop moved (the previous develop aa600af94)"
judge D/twin 0 "$(QAB1234_CUR_DEV="$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$L")" chk D.twin)" "the pinned develop through the same override"
judge V 10 "$(QAB1234_PATHS_1234='Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh,Blockchain/Dev/scripts/run-shell-suites.SH' chk V)" "base-invariant compare: a same-count WRONG path for #1234"
judge V/twin 0 "$(QAB1234_PATHS_1234='Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh,Blockchain/Dev/scripts/run-shell-suites.sh' chk V.twin)" "the right paths through the same override"
doctor "$CAP" "$CW/O.cap" '41 passed, 8 failed' '41 passed, 8 FAILED' && cp "$CAP" "$CW/O.pristine.cap"
judge O 30 "$(QAB1234_BRIEF="$CW/O.cap" chk O)" "capture missing a seat item ('41 passed, 8 failed')"
judge O/twin 0 "$(QAB1234_BRIEF="$CW/O.pristine.cap" chk O.twin)" "pristine capture through the same override"
pctl G 8 $'ultrathink\n' $'think\n' "no thinking directive"
pctl U 8 'PR #1239 is KS-1263.' 'PR #1239 is {{KS_1263}}.' "an unfilled fill token"
pctl H20 20 '42c20e998a1a69887b8378968a8ff4f19106c24b' '42c20e998a1a69887b8378968a8ff4f19106c24X' "prompt names a wrong #1239 head"
pctl T 32 'PR #1239 is KS-1263.' 'PR #1239 is KS-1264.' "ticket statement for #1239"
pctl I 7 '#1239 T1' '#1239 T2' "tier line for #1239"
pctl K 33 'T-PRISMA' 'T-PRISM4' "a by-name keyword (T-PRISMA)"
pctl B 34 '#1239 DOES NOT satisfy (3)' '#1239 satisfies (3)' "the base-invariant rule loses #1239's overlap"
pctl S 35 'TEAR DOWN WHAT YOU START, NOTHING ELSE' 'TEAR DOWN WHAT YOU CAN' "stack rule: tear down what you start"
pctl S2 35 'NEVER connect to it, stop it, or remove it' 'you may stop it' "stack rule: the foreign container"
pctl R 36 'MODE T = MULTI_TENANCY_ENABLED=true AND PLATFORM_DATABASE_URL' 'MODE T = MULTI_TENANCY_ENABLED=true' "rollback rule: mode T without PLATFORM_DATABASE_URL"
pctl R2 36 'a MODE-F RUN MISLABELLED' 'a MODE-T RUN' "rollback rule: the platform-URL trap"
pctl R3 36 'POOL-BRANCH PROOF IS A KS-1263 RESIDUAL — NEVER implied from MODE F, never green' 'POOL-BRANCH PROOF MAY BE INFERRED FROM MODE F' "rollback rule: the residual rule"
pctl R4 36 'CONTROL (a completed callback COMMITS' 'CONTROL (optional' "rollback rule: the CONTROL must be green"
pctl Q 37 'G-alt-2 was REJECTED' 'G-alt-2 was fine' "req.db measurement rule"
pctl Y 38 'pre-existing (KS-562), not caused by this change"' 'pre-existing, not caused by this change"' "the anchoring wording"
pctl Y2 38 'an ASSERTION failure is REAL' 'an ASSERTION failure is noise' "the load rule"
pctl Hh 39 'NEVER WRITE THE SHARED CHECKOUT' 'WRITE THE SHARED CHECKOUT IF NEEDED' "holds: the shared checkout"
pctl X 40 'YOU DO NOT RUN IT EITHER' 'YOU MAY RUN IT' "#1234: no standalone runner run"
pctl X2 41 'GIT_CEILING_DIRECTORIES=/private/tmp' 'GIT_CEILING_DIRECTORIES=' "#1234: the safe harness"
pctl Z 43 'never by name, never pid 1' 'by name if needed' "login_stub reaper rule"
pctl A 26 '`GO: merge #1234, #1239 batch`' '`GO: merge #1234 batch`' "the GO string"
pctl E 25 'PER PR FILE (2 + 6 = 8 over 8 paths)' 'PER PR FILE' "addendum counts"
pctl J 23 '[QA -> Wednesday] TIER-1 BATCH GATE #1234 #1239 round 21' '[QA -> Wednesday] TIER-1 GATE #1234 #1239 round 21' "the verdict subject"
ET="$(sed -n "s/^END_TREE='\(.*\)'$/\1/p" "$L")"
python3 - "$PR" "$CW/W.prompt" "$ET" <<'PY'
import sys
s, d, et = sys.argv[1:4]; t = open(s, encoding='utf-8').read(); assert et in t
open(d, 'w', encoding='utf-8').write(t.replace(et, et[:-1] + ('0' if et[-1] != '0' else '1')))
PY
cp "$PR" "$CW/W.pristine.prompt"
judge W 31 "$(QAB1234_PROMPT="$CW/W.prompt" chk W)" "the END_TREE not in full in the prompt"
judge W/twin 0 "$(QAB1234_PROMPT="$CW/W.pristine.prompt" chk W.twin)" "pristine prompt through the same override"
"$L" < /dev/null > "$CW/N.out" 2>&1; judge N 21 "$?" "LAUNCH path (no --check) with stdin not a TTY — refuses before exec"
QAB1234_PROMPT="$PR" "$L" --check > "$CW/N2.out" 2>&1; judge N2 0 "$?" "an override set is allowed under --check (the launch path refuses it, exit 16, after the TTY guard)"
mkdir -p "$CW/moved"; cp -p "$L" "$CW/moved/"; "$CW/moved/$(basename "$L")" --check > "$CW/M.out" 2>&1; judge M 2 "$?" "the launcher copied out of its filled home (a MOVED KIT)"
"$L" --check > "$CW/M.twin.out" 2>&1; judge M/twin 0 "$?" "the same launcher at home"
say "--- repin_and_launch (dry runs / refusals only)"
bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R1.out" 2>&1; judge R1 0 "$?" "dry run, the kit as filled"
doctor "$L" "$CW/R2.launch.sh" '42c20e998a1a69887b8378968a8ff4f19106c24b|6|1|' '42c20e998a1a69887b8378968a8ff4f19106c24c|6|1|' && chmod 755 "$CW/R2.launch.sh"
bash "$REPIN" "$CW/R2.launch.sh" "$SP" --dry-run > "$CW/R2.out" 2>&1; judge R2 11 "$?" "a stale #1239 head pin"
cp -p "$L" "$CW/R2.twin.launch.sh"; bash "$REPIN" "$CW/R2.twin.launch.sh" "$SP" --dry-run > "$CW/R2.twin.out" 2>&1; judge R2/twin 0 "$?" "the same copied-launcher mechanism, pins intact"
doctor "$L" "$CW/R3.launch.sh" "DEVELOP_SHA='$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$L")'" "DEVELOP_SHA='aa600af94d69ad59db279d32cbbd7596931a739b'" && chmod 755 "$CW/R3.launch.sh"
bash "$REPIN" "$CW/R3.launch.sh" "$SP" --dry-run > "$CW/R3.out" 2>&1; judge R3 10 "$?" "the pinned develop is stale (the dry run reports the re-pin and stops)"
: > "$CW/empty_routing.conf"
G21C_ROUTING="$CW/empty_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4.out" 2>&1; judge R4 1 "$?" "a REAL run with the routing line absent stops at step 0 (routing file override: deterministic)"
printf 'QA/Secuura-batch1234|coagent@agentmail.to|yes\n' > "$CW/good_routing.conf"
G21C_ROUTING="$CW/good_routing.conf" bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R4.twin.out" 2>&1; judge R4/twin 0 "$?" "the routing line present (override file), dry run"
bash "$REPIN" "$L" /tmp > "$CW/R5.out" 2>&1; judge R5 9 "$?" "a scratchpad outside /private/tmp/claude-501/"
say "--- the moved kit and predict (in a COPY of the kit, never the home)"
MK="$CW/movedkit"; mkdir -p "$MK"; /usr/bin/rsync -a --exclude '_sp' --exclude '_meas' --exclude 'launch_*.out' "$GS/" "$MK/"
bash "$MK/repin_and_launch_gate21T1c.sh" "$MK/launch_qa_secuura_batch1234-t1.sh" "$SP" --dry-run > "$CW/R6.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -i 'MOVED KIT' "$CW/R6.out" && rc=98
judge R6 0 "$rc" "moved-kit dry run: rc 0 AND reports MOVED KIT"
python3 "$MK/predict_gate21T1c.py" "$SP" --develop 379c6eb1d45905f398fae67ee7dd2f46ad40432f > "$CW/P1.out" 2>&1; judge P1 1 "$?" "predict over an OLDER develop (379c6eb1d: #1239's two overlaps absent) — the overlap guard refuses"
python3 "$MK/predict_gate21T1c.py" "$SP" > "$CW/P1.twin.out" 2>&1; judge P1/twin 0 "$?" "predict over origin develop in the same copy"
python3 "$MK/fill_gate21T1c.py" > "$CW/F1.out" 2>&1; rc=$?
"$MK/launch_qa_secuura_batch1234-t1.sh" --check > "$CW/F1.check.out" 2>&1; rc2=$?
[ "$rc" = 0 ] && [ "$rc2" = 0 ] && /usr/bin/grep -q -F "GS='$MK'" "$MK/launch_qa_secuura_batch1234-t1.sh" && rc=0 || rc=97
judge F1 0 "$rc" "the moved copy re-filled at its new home: fill rc 0, --check rc 0, its launcher names the new home"
say "RESULT $([ "$INV" = 1 ] && echo '(inverted) ')$OK OK / $BAD MISMATCH of $N  $(date -u +%FT%TZ)"
[ "$BAD" = 0 ]
