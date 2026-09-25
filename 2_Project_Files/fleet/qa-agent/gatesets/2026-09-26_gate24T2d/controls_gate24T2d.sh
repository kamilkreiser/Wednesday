#!/bin/bash
# controls_gate24T2d.sh — every guard of the gate24T2d kit, run BOTH WAYS. Each control has a DOCTORED arm (one planted defect; the guard must refuse
# with its own exit code) and, where the mechanism is an override or a copied file, a PRISTINE twin through the SAME mechanism (defect not planted;
# must pass) — so a refusal is attributable to the defect, not to the harness. `--invert` flips every expectation: every control must then report
# MISMATCH (proves each control can fail and the harness can report it). Launches nothing: launcher controls use `--check` (headless) or stop at the
# non-TTY guard; repin controls use `--dry-run`, a bad argv, a routing-file override that stops at step 0, or a port override that stops at step 3c;
# predict / fill controls run in a MOVED COPY of the kit, never the home. Each doctored prompt phrase is chosen OUTSIDE the by-name ladder and the seat
# items, so the control reaches the rule it names (the ladder, exit 33, runs first). Doctored arms are PINNED to the launcher's own develop (pchk) so a
# develop move mid-run cannot mask them as exit 17. The ROUND-1 heads are controlled explicitly: a launcher or a pin still naming the NO-GO head
# (c78f4093fb53 / 6b88e4f03e82) must refuse (C3, C4, R2r). Starts no container and binds no port. Writes only under <scratchpad>/g24d_controls_*.
# Derived from gate24T2b's controls, re-keyed to SEVEN rows (the #1263-#1266 widens), no stack, plus the port step and the CAP / RULING (a) / DB / TIER-3 rules.
# Usage: controls_gate24T2d.sh <scratchpad dir> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
SP="${1:-}"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "no scratchpad $SP"; exit 9; } ;; *) echo "usage: controls_gate24T2d.sh <scratchpad> [--invert]"; exit 9;; esac
L="$GS/launch_qa_secuura_batch1250r2-t2.sh"; PR="$GS/2026-09-26_secuura-batch1250r2-t2.prompt.txt"; CAP="$GS/mail_gate24T2d_ready.md"
REPIN="$GS/repin_and_launch_gate24T2d.sh"
CW="$SP/g24d_controls_$(date -u +%H%M%S)$([ "$INV" = 1 ] && echo _inv)"; mkdir -p "$CW"
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
pchk() { QAB24D_CUR_DEV="${QAB24D_CUR_DEV:-$PDEV}" "$L" --check > "$CW/$1.out" 2>&1; echo $?; }
pctl() { # id want old new label
  local id="$1" want="$2"; doctor "$PR" "$CW/$id.prompt" "$3" "$4" || { judge "$id" "$want" 99 "DOCTOR FAILED: $5"; return; }
  cp "$PR" "$CW/$id.pristine.prompt"
  judge "$id" "$want" "$(QAB24D_PROMPT="$CW/$id.prompt" pchk "$id")" "$5"
  judge "$id/twin" 0 "$(QAB24D_PROMPT="$CW/$id.pristine.prompt" pchk "$id.twin")" "$5 — pristine copy through the same override"
}
hd() { sed -n "s/^  \"$1|[^|]*|[^|]*|\([0-9a-f]\{40\}\)|.*$/\1/p" "$L"; }
H50="$(hd 1250)"; H53="$(hd 1253)"; H62="$(hd 1262)"; H63="$(hd 1263)"; H64="$(hd 1264)"; H65="$(hd 1265)"; H66="$(hd 1266)"; PDEV="$(sed -n "s/^DEVELOP_SHA='\(.*\)'$/\1/p" "$L")"
R150='c78f4093fb531bceb94a8e9defb59350d8c60b73'; R153='6b88e4f03e82e3da0672efb1bb757ba5da912d6a'
[ -n "$H50" ] && [ -n "$H53" ] && [ -n "$H62" ] && [ -n "$H63" ] && [ -n "$H64" ] && [ -n "$H65" ] && [ -n "$H66" ] && [ -n "$PDEV" ] || { echo "REFUSING: could not read the #1250 / #1253 / #1262 / #1263 / #1264 rows / DEVELOP_SHA from $L"; exit 9; }
P50="Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh,Blockchain/Dev/scripts/run-shell-suites.sh"
P62="Blockchain/Dev/services/originate/src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts"
P63="Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts"
P64="Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts"
say "controls_gate24T2d.sh $(date -u +%FT%TZ)$([ "$INV" = 1 ] && echo ' --invert') | kit $GS | work $CW"
say "--- launcher (--check unless stated)"
judge P 0 "$(chk P)" "positive: the kit as filled"
judge C 6 "$(QAB24D_HEAD_1250=0000000000000000000000000000000000000000 pchk C)" "stale #1250 head"
judge C2 6 "$(QAB24D_HEAD_1250="$H53" pchk C2)" "#1253's head pinned as #1250's"
judge C3 6 "$(QAB24D_HEAD_1250="$R150" pchk C3)" "#1250 pinned at its ROUND-1 (NO GO) head c78f4093fb53 — the superseded head must refuse"
judge C4 6 "$(QAB24D_HEAD_1253="$R153" pchk C4)" "#1253 pinned at its ROUND-1 (NO GO) head 6b88e4f03e82"
judge C5 6 "$(QAB24D_HEAD_1263="$H62" pchk C5)" "#1262's head pinned as #1263's (the widen row)"
judge C7 6 "$(QAB24D_HEAD_1266="$H65" pchk C7)" "#1265's head pinned as #1266's"
judge C6 6 "$(QAB24D_HEAD_1264="$H63" pchk C6)" "#1263's head pinned as #1264's (the two widen rows swapped)"
judge C/twin 0 "$(QAB24D_HEAD_1250="$H50" QAB24D_HEAD_1253="$H53" QAB24D_HEAD_1262="$H62" QAB24D_HEAD_1263="$H63" QAB24D_HEAD_1264="$H64" QAB24D_HEAD_1265="$H65" QAB24D_HEAD_1266="$H66" pchk C.twin)" "the real seven heads through the same overrides"
judge D 17 "$(QAB24D_CUR_DEV=6e2a00bfed577528de1ee02b41cb5a0e99172b35 chk D)" "develop moved (BASE 6e2a00bfe as the current develop)"
judge D/twin 0 "$(QAB24D_CUR_DEV="$PDEV" chk D.twin)" "the pinned develop through the same override"
judge V 10 "$(QAB24D_PATHS_1250="${P50/run-shell-suites.sh/run_shell_suites.sh}" pchk V)" "base-invariant compare: #1250 with a same-count WRONG path name"
judge V2 10 "$(QAB24D_PATHS_1262="${P62//services\/originate/services\/kyc}" pchk V2)" "base-invariant compare: #1262 with a WRONG path (another service)"
judge V3 10 "$(QAB24D_PATHS_1263="${P63/ks879-no-raw/ks878-no-raw}" pchk V3)" "base-invariant compare: #1263 with a same-package WRONG file name"
judge V4 10 "$(QAB24D_PATHS_1264="${P64/vc-issuer/kyc}" pchk V4)" "base-invariant compare: #1264 with a WRONG service path"
judge V/twin 0 "$(QAB24D_PATHS_1250="$P50" QAB24D_PATHS_1262="$P62" QAB24D_PATHS_1263="$P63" QAB24D_PATHS_1264="$P64" pchk V.twin)" "the right paths through the same override"
doctor "$CAP" "$CW/O.cap" 'is MOCKED for this whole file' 'is mocked' && cp "$CAP" "$CW/O.pristine.cap"
judge O 30 "$(QAB24D_BRIEF="$CW/O.cap" pchk O)" "capture missing a seat item (#1262's mock sentence)"
judge O/twin 0 "$(QAB24D_BRIEF="$CW/O.pristine.cap" pchk O.twin)" "pristine capture through the same override"
doctor "$CAP" "$CW/O2.cap" 'INT-to-pid: nowhere, bash rule 2' 'INT-to-pid: see the matrix' && cp "$CAP" "$CW/O2.pristine.cap"
judge O2 30 "$(QAB24D_BRIEF="$CW/O2.cap" pchk O2)" "capture missing a seat item from Wednesday's RULING (a) (the pid-delivery premise)"
judge O2/twin 0 "$(QAB24D_BRIEF="$CW/O2.pristine.cap" pchk O2.twin)" "pristine capture through the same override"
doctor "$CAP" "$CW/O3.cap" 'All 31 changed lines in `git diff -U0` are comment lines' 'The changed lines are comments' && cp "$CAP" "$CW/O3.pristine.cap"
judge O3 30 "$(QAB24D_BRIEF="$CW/O3.cap" pchk O3)" "capture missing a #1263 seat item (the 31 comment lines claim)"
judge O3/twin 0 "$(QAB24D_BRIEF="$CW/O3.pristine.cap" pchk O3.twin)" "pristine capture through the same override"
pctl G 8 $'ultrathink\n' $'think\n' "no thinking directive"
pctl U 8 'PR #1253 is KS-1297.' 'PR #1253 is {{KS_1297}}.' "an unfilled fill token"
pctl H20 20 '3b319485d1e3a58f30e4190a7898d7562cb80c3b' '3b319485d1e3a58f30e4190a7898d7562cb80c3bX' "the prompt names a wrong #1262 head"
pctl T 32 'PR #1253 is KS-1297.' 'PR #1253 is KS-1298.' "ticket statement for #1253"
pctl T2 32 'PR #1250 is KS-1302 + KS-1303.' 'PR #1250 is KS-1302.' "ticket statement for #1250 (a two-key row)"
pctl T3 32 'PR #1262 is KS-1310 + KS-1311.' 'PR #1262 is KS-1310.' "ticket statement for #1262 (a two-key row)"
pctl T4 32 'PR #1263 is KS-1140.' 'PR #1263 is KS-1141.' "ticket statement for #1263 (the widen)"
pctl T5 32 'PR #1264 is KS-1281.' 'PR #1264 is KS-1282.' "ticket statement for #1264 (the second widen)"
pctl T6 32 'PR #1265 is KS-1315.' 'PR #1265 is KS-1316.' "ticket statement for #1265"
pctl T7 32 'PR #1266 is KS-1120.' 'PR #1266 is KS-1020.' "ticket statement for #1266"
pctl I 7 '#1253 T2' '#1253 T3' "tier line for #1253"
pctl I2 7 'The batch is FROZEN at seven' 'The batch is FROZEN at five' "the batch frozen at seven (five = the kit before the last two widens)"
pctl I6 7 '#1265 T2' '#1265 T3' "#1265's tier line is T2 (it carries a red proof)"
pctl I3 7 '#1263 T3' '#1263 T2' "#1263's tier line is T3 (comment-only)"
pctl I5 7 '#1264 T3' '#1264 T2' "#1264's tier line is T3 (comment-only)"
pctl I4 7 'TIER 3 (#1263 and #1264): THROUGH-CODE ONLY' 'TIER 3 (#1263 and #1264)' "the tier-3 definition"
pctl K 33 'SAFE-SHAPES-FLAGGED' 'SAFE-SHAPES' "a by-name keyword (SAFE-SHAPES-FLAGGED, every occurrence)"
pctl K2 33 'INT-PID-CONSTANT' 'INT-PID' "a by-name keyword (INT-PID-CONSTANT, every occurrence)"
pctl B 34 'a sibling batch merging is not a difference' 'a sibling batch merging is a difference' "base-invariant rule"
pctl B2 34 'There is NO declared overlap in this batch' 'An overlap is fine in this batch' "no declared overlap: a move on any own path STOPS"
pctl B3 34 'declare any overlap you find with its merged-blob target' 'ignore any overlap you find' "pairwise: declare any overlap with its merged-blob target"
pctl S 35 'Docker is permitted for #1262 ONLY' 'Docker is permitted' "Docker for #1262 only"
pctl S2 35 'binds on 127.0.0.1:55419 ONLY' 'binds on any free port in 55410-55419' "the gate's Postgres on :55419 only (55410-55418 are B 29th's)"
pctl S3 35 'PROVE THE PORT FREE against a control' 'check the port' "the port proof carries a control"
pctl S4 35 'TORN DOWN AND PROVEN GONE' 'stopped when done' "torn down and proven gone"
pctl S5 35 'NEVER connect to it' 'connect as needed' "never the native :5432"
pctl X 36 'restore by bytes' 'restore somehow' "red-proof rule: restore by bytes"
pctl X2 36 'in YOUR OWN clone' 'in the shared checkout' "red proof in the tester's own clone"
pctl F 37 '`fixture_guard` 12/0 if #1253 merges' '`fixture_guard` 10/0 if #1253 merges' "fleet STOP: the NEW fixture_guard count (12, not round 1's 10)"
pctl F2 37 '`run_shell_suites` 58/0 if #1250 merges' '`run_shell_suites` 55/0 if #1250 merges' "fleet STOP: the NEW run_shell_suites count (58, not round 1's 55)"
pctl F3 37 'NO STANDALONE RUN of' 'A STANDALONE RUN of' "fleet STOP: no standalone run beyond the two changed suites"
pctl Y 38 'pre-existing (KS-562), not caused by this change"' 'pre-existing, not caused by this change"' "the anchoring wording"
pctl Y2 38 'an ASSERTION failure is REAL' 'an ASSERTION failure is noise' "the load rule"
pctl Y3 38 'do not let it decide the cap' 'let it decide the cap' "N-1250-b TIMING-CELL: re-run once, never decides the cap (Wednesday's carried rule)"
pctl Hh 39 'NEVER WRITE THE SHARED CHECKOUT' 'WRITE THE SHARED CHECKOUT IF NEEDED' "holds: the shared checkout"
pctl H2 39 'NO ticket filed' 'tickets may be filed' "holds: no ticket filed"
pctl Q 40 'A WRONG READING ON ANY REAL SHAPE = NO GO for that PR (blocking)' 'A wrong reading is a note' "THE READER RULE: a wrong reading on a real shape is NO GO"
pctl Q2 40 '`false || bf` and `|| true` must NOT be flagged' '`false || bf` and `|| true` may be flagged' "THE READER RULE: the two safe || shapes must NOT be flagged (Wednesday's commission)"
pctl Q3 40 'THROUGH THE REAL CODE PATH — never a lifted regex, never a Python port' 'through whatever path is easiest' "THE READER RULE: the real code path, never a port"
pctl Q4 40 'NAMES it (as a shape the check catches OR as a shape it declares safe)' 'mentions it' "THE READER RULE: a shape the PR names SAFE counts as real too"
pctl R 41 'A signal arm that is vacuously green is a NO GO' 'A vacuous signal arm is a note' "RULING (a): a vacuously green signal arm is NO GO"
pctl R2 41 "SIGTERM sent to the RUNNER's own pid (by pid, never by name)" 'SIGTERM sent somehow' "#1250: signal the runner by pid"
pctl R3 41 'SIGTERM to the runner must end it non-zero, run no further suite, print no `shell suites:` verdict, and remove the named /tmp/rss dir' 'SIGTERM behaviour is informational' "#1250: the round-1 blocking property is still graded"
pctl R4 41 'on FOUR CONDITIONS' 'on some conditions' "RULING (a): the four conditions"
pctl N42 42 '-> 0/0 (the trigger was dropped' '-> any count (the trigger was dropped' "#1262: pg_trigger + pg_proc 0/0 after every run"
pctl N42b 42 'RED with "Expected: 0, Received: 1" at the custody count' 'RED at the custody count' "#1262: the red names its assertion text at the red base"
pctl N42c 42 'the describe REFUSES unless its connection is 127.0.0.1 on 55410-55419' 'the describe checks its connection' "#1262: the cell's own refusal (127.0.0.1, 55410-55419)"
pctl Z 43 'never by name, never pid 1' 'by name if needed' "login_stub reaper rule"
pctl SC 44 'A declared-scope item is still graded by THE READER RULE' 'A declared-scope item is never graded' "declared scope still under THE READER RULE"
pctl L8 45 'legs 3/4/8 NOT run (no stack; no spec surface)' 'legs 3/4/8 as convenient' "legs 3/4/8 NOT run"
pctl CAP 46 'AT THE CAP a NO GO ships nothing' 'AT THE CAP a NO GO ships anyway' "THE CAP: a NO GO ships nothing"
pctl CAP2 46 'the cap raises the cost of a NO GO, never the bar and never the leniency' 'the cap lowers the bar' "THE CAP: neither bar nor leniency moves"
pctl A 26 '`GO: merge #1250, #1253, #1262, #1263, #1264, #1265, #1266 batch`' '`GO: merge #1262 batch`' "the GO string"
pctl A4 26 "#1264's author Seat L8 is LIVE and squashes its own PR on the GO" '#1264 goes to the merge seat' "#1264's live author merges its own PR"
pctl A3 26 "#1263's author Seat L7 is LIVE and squashes its own PR on the GO" '#1263 goes to the merge seat' "#1263's live author merges its own PR"
pctl A2 26 'by a MERGE SEAT Wednesday names, never by an author' 'by the author' "a merge seat, never a wrapped author"
pctl E 25 'PER PR FILE (2 over 2 paths) for #1250, (1 over 1 path) for #1253, #1262, #1263, #1264, #1265 and #1266' 'PER PR FILE' "addendum count"
pctl E2 25 'FLEET STOP after this merge' 'counts after this merge' "addendum carries the fleet STOP after each merge"
pctl E3 25 'CAP NO GO (round 2 of 2)' 'NO GO (round 2)' "addendum's CAP form"
pctl J 23 '[QA -> Wednesday] TIER-2 GATE batch #1250r2 #1253r2 #1262 #1263 #1264 #1265 #1266 (Seats L5 B28 L7 L8, round 24 cap)' '[QA -> Wednesday] TIER-2 GATE batch #1250' "the verdict subject"
pctl TP 47 'A DIFFERENT emit, or a code line in the diff = NO GO for that PR (blocking)' 'A DIFFERENT emit is a note' "TIER-3: a DIFFERENT emit is NO GO"
pctl KP 47 '(P-3) T4 and T5 at develop (no cells) -> 129/129 green' '(P-3) skipped' "#1266's red proof: the classes were unpinned at develop"
pctl KP2 47 'RED PROOF (mandatory, YOUR worktree): (K-1) T-1 at head' 'RED PROOF (optional)' "#1265's red proof is mandatory"
pctl F4 37 '#1265 is a systemTest/ push: NOT APPLICABLE' '#1265 carries the usual counts' "fleet STOP: #1265's systemTest/ push has no preflight"
pctl TP2 47 'an instrument that cannot say DIFFERENT proves nothing' 'the emit alone suffices' "#1263 TIER-3: the emit instrument carries its DIFFERENT control"
for tok in END_TREE RED62; do
  ET="$(sed -n "s/^$tok='\(.*\)'$/\1/p" "$L")"
  python3 - "$PR" "$CW/W$tok.prompt" "$ET" <<'PY'
import sys
s, d, et = sys.argv[1:4]; t = open(s, encoding='utf-8').read(); assert len(et) == 40 and et in t
open(d, 'w', encoding='utf-8').write(t.replace(et, et[:-1] + ('0' if et[-1] != '0' else '1')))
PY
  cp "$PR" "$CW/W$tok.pristine.prompt"
  judge "W:$tok" 31 "$(QAB24D_PROMPT="$CW/W$tok.prompt" pchk "W$tok")" "the $tok not in full in the prompt"
  judge "W:$tok/twin" 0 "$(QAB24D_PROMPT="$CW/W$tok.pristine.prompt" pchk "W$tok.twin")" "pristine prompt through the same override"
done
QAB24D_CUR_DEV="$PDEV" "$L" < /dev/null > "$CW/N.out" 2>&1; judge N 21 "$?" "LAUNCH path (no --check) with stdin not a TTY — refuses before exec"
QAB24D_CUR_DEV="$PDEV" QAB24D_PROMPT="$PR" "$L" --check > "$CW/N2.out" 2>&1; rc=$?; [ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'TEST OVERRIDE is set' "$CW/N2.out" && rc=94
judge N2 0 "$rc" "an override set is allowed under --check AND reported (the launch path refuses it, exit 16, after the TTY guard)"
mkdir -p "$CW/moved"; cp -p "$L" "$CW/moved/"; QAB24D_CUR_DEV="$PDEV" "$CW/moved/$(basename "$L")" --check > "$CW/M.out" 2>&1; judge M 2 "$?" "the launcher copied out of its filled home (a MOVED KIT)"
QAB24D_CUR_DEV="$PDEV" "$L" --check > "$CW/M.twin.out" 2>&1; judge M/twin 0 "$?" "the same launcher at home"
say "--- repin_and_launch (dry runs / refusals only)"
bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R1.out" 2>&1; judge R1 0 "$?" "dry run, the kit as filled"
doctor "$L" "$CW/R2.launch.sh" "$H53|1|" "${H53%?}$([ "${H53: -1}" = 0 ] && echo 1 || echo 0)|1|" && chmod 755 "$CW/R2.launch.sh"
bash "$REPIN" "$CW/R2.launch.sh" "$SP" --dry-run > "$CW/R2.out" 2>&1; judge R2 11 "$?" "a stale #1253 head pin"
doctor "$L" "$CW/R2r.launch.sh" "$H50|2|" "$R150|2|" && chmod 755 "$CW/R2r.launch.sh"
bash "$REPIN" "$CW/R2r.launch.sh" "$SP" --dry-run > "$CW/R2r.out" 2>&1; judge R2r 11 "$?" "a launcher still pinned to #1250's ROUND-1 (NO GO) head"
doctor "$L" "$CW/R2w.launch.sh" "$H63|1|" "${H63%?}$([ "${H63: -1}" = 0 ] && echo 1 || echo 0)|1|" && chmod 755 "$CW/R2w.launch.sh"
bash "$REPIN" "$CW/R2w.launch.sh" "$SP" --dry-run > "$CW/R2w.out" 2>&1; judge R2w 11 "$?" "a stale #1263 head pin (the widen row)"
doctor "$L" "$CW/R2x.launch.sh" "$H64|1|" "${H64%?}$([ "${H64: -1}" = 0 ] && echo 1 || echo 0)|1|" && chmod 755 "$CW/R2x.launch.sh"
bash "$REPIN" "$CW/R2x.launch.sh" "$SP" --dry-run > "$CW/R2x.out" 2>&1; judge R2x 11 "$?" "a stale #1264 head pin (the second widen row)"
doctor "$L" "$CW/R2y.launch.sh" "$H66|1|" "${H66%?}$([ "${H66: -1}" = 0 ] && echo 1 || echo 0)|1|" && chmod 755 "$CW/R2y.launch.sh"
bash "$REPIN" "$CW/R2y.launch.sh" "$SP" --dry-run > "$CW/R2y.out" 2>&1; judge R2y 11 "$?" "a stale #1266 head pin (the last widen row)"
cp -p "$L" "$CW/R2.twin.launch.sh"; bash "$REPIN" "$CW/R2.twin.launch.sh" "$SP" --dry-run > "$CW/R2.twin.out" 2>&1; judge R2/twin 0 "$?" "the same copied-launcher mechanism, pins intact"
doctor "$L" "$CW/R3.launch.sh" "DEVELOP_SHA='$PDEV'" "DEVELOP_SHA='6e2a00bfed577528de1ee02b41cb5a0e99172b35'" && chmod 755 "$CW/R3.launch.sh"
bash "$REPIN" "$CW/R3.launch.sh" "$SP" --dry-run > "$CW/R3.out" 2>&1; judge R3 10 "$?" "the pinned develop is stale (the dry run reports the re-pin and stops)"
: > "$CW/empty_routing.conf"
G24D_ROUTING="$CW/empty_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4.out" 2>&1; judge R4 1 "$?" "a REAL run with the routing line absent stops at step 0 (routing-file override: deterministic)"
printf 'QA/Secuura-batch1250r2|coagent@agentmail.to|yes\n' > "$CW/good_routing.conf"
G24D_ROUTING="$CW/good_routing.conf" bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R4.twin.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'line present: 1 (grep rc=0' "$CW/R4.twin.out" && rc=95
judge R4/twin 0 "$rc" "the routing line present (override file), dry run — AND step 0 reads it as present"
printf 'QA/Secuura-batch1249|coagent@agentmail.to|yes\n' > "$CW/other_routing.conf"
G24D_ROUTING="$CW/other_routing.conf" bash "$REPIN" "$L" "$SP" > "$CW/R4b.out" 2>&1; judge R4b 1 "$?" "only gate24T2b's pane line present — this pane is NOT routed, a real run stops at step 0"
bash "$REPIN" "$L" /tmp > "$CW/R5.out" 2>&1; judge R5 9 "$?" "a scratchpad outside /private/tmp/claude-501/"
G24D_PORT=5432 bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R7.out" 2>&1; judge R7 15 "$?" "step 3c: the DB port BUSY (port override 5432, the native Postgres) refuses before any launch"
G24D_PORT=55419 bash "$REPIN" "$L" "$SP" --dry-run > "$CW/R7.twin.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -E 'listeners on :55419: 0$' "$CW/R7.twin.out" && rc=92
judge R7/twin 0 "$rc" "the same override naming :55419 (free) — dry run passes AND reads 0 listeners there"
say "--- the moved kit, predict and fill (in a COPY of the kit, never the home)"
MK="$CW/movedkit"; mkdir -p "$MK"; /usr/bin/rsync -a --exclude '_sp' --exclude 'launch_*.out' --exclude 'g24d_controls_*' "$GS/" "$MK/"
bash "$MK/repin_and_launch_gate24T2d.sh" "$MK/launch_qa_secuura_batch1250r2-t2.sh" "$SP" --dry-run > "$CW/R6.out" 2>&1; rc=$?
[ "$rc" = 0 ] && ! /usr/bin/grep -q -F 'MOVED KIT' "$CW/R6.out" && rc=98
judge R6 0 "$rc" "moved-kit dry run: rc 0 AND reports MOVED KIT"
for s in 1250 1253 1262 1263 1264 1265 1266; do
  python3 "$MK/predict_gate24T2d.py" "$SP" --simulate "foreign$s" > "$CW/P$s.out" 2>&1; judge "P$s" 1 "$?" "predict over develop + a FOREIGN edit of #$s's own file — the base-invariant check (3) refuses"
done
python3 "$MK/predict_gate24T2d.py" "$SP" > "$CW/P.twin.out" 2>&1; judge P/twin 0 "$?" "predict over origin develop in the same copy (no simulation)"
cp "$MK/pins_gate24T2d.json" "$CW/pins.real.json"
python3 - "$CW/pins.real.json" "$MK/pins_gate24T2d.json" <<'PY'
import json, sys
p = json.load(open(sys.argv[1])); p['simulation'] = 'foreign1250'; p['fail'] = 0
json.dump(p, open(sys.argv[2], 'w'), indent=1, sort_keys=True)
PY
python3 "$MK/fill_gate24T2d.py" > "$CW/F2.out" 2>&1; rc=$?; [ "$rc" = 1 ] && ! /usr/bin/grep -q -F 'is a SIMULATION' "$CW/F2.out" && rc=96
judge F2 1 "$rc" "fill refuses a SIMULATED pins file (fail=0, simulation named — refused FOR the simulation)"
python3 - "$CW/pins.real.json" "$MK/pins_gate24T2d.json" <<'PY'
import json, sys
p = json.load(open(sys.argv[1])); p['fail'] = 1
json.dump(p, open(sys.argv[2], 'w'), indent=1, sort_keys=True)
PY
python3 "$MK/fill_gate24T2d.py" > "$CW/F3.out" 2>&1; rc=$?; [ "$rc" = 1 ] && ! /usr/bin/grep -q -F 'carries fail=1' "$CW/F3.out" && rc=96
judge F3 1 "$rc" "fill refuses a pins file carrying a HARD FAIL"
cp "$CW/pins.real.json" "$MK/pins_gate24T2d.json"
python3 "$MK/fill_gate24T2d.py" > "$CW/F1.out" 2>&1; rc=$?
"$MK/launch_qa_secuura_batch1250r2-t2.sh" --check > "$CW/F1.check.out" 2>&1; rc2=$?
[ "$rc" = 0 ] && [ "$rc2" = 0 ] && /usr/bin/grep -q -F "GS='$MK'" "$MK/launch_qa_secuura_batch1250r2-t2.sh" && rc=0 || rc=97
judge F1 0 "$rc" "the moved copy re-filled at its new home: fill rc 0, --check rc 0, its launcher names the new home"
say "RESULT $([ "$INV" = 1 ] && echo '(inverted) ')$OK OK / $BAD MISMATCH of $N  $(date -u +%FT%TZ)"
[ "$BAD" = 0 ]
