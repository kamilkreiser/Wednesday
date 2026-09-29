#!/bin/bash
# controls_gate47.sh — every guard in the gate47 kit driven on the REAL subject and on PLANTED defects, each with the rc it must give and a WHY pattern
# its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a control that makes it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g47_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate47.json is sha256-checked unchanged at the end (PNZ). The launcher runs with --check (headless) except L9, the real launch path with
# stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run that must refuse at step 0, routing) and R8
# (a real run with a routed temp file that must stop at G47_STOP_AFTER_3B) — both stop long before the usage gate / cockpit.
# Mode plants (PN6 / PN7 / PN7b) RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>): core.filemode is false, a disk chmod proves nothing.
# Each by-name keyword the commission added (HOOK-SKIPPED-LEGS-1349 … TIERING) has its own launcher refusal (LK*): the keyword is broken into
# `<KW>-X`, which the launcher's TOKEN match must NOT accept (so `MODES` is not satisfied by `MODES-X`).
# R0 is the kit's LIVE state: #1351 (out of kit) touches a kit path, so the real census refuses rc 15; R0s-R8 run under a controls-only stand-in
# for Wednesday's sequencing (G47_SEQUENCED at #1351's head as fetched into the scratch clone), so every later step is still reached and controlled.
# Shape copied from the gate46 controls (and gate44 / gate45 for the two-PR parts), re-keyed for gate47 (#1349 then #1350).
# Usage: controls_gate47.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g47_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g47_sp/clone"; L="$GS/launch_qa_secuura_batch1349.sh"; PROMPT="$GS/2026-09-30_secuura-batch1349.prompt.txt"; CAP="$GS/mail_gate47_ready.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate47.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"
H49="$(PJ prs.1349.head)"; H50="$(PJ prs.1350.head)"; MB49="$(PJ prs.1349.merge_base)"
PINSHA="$(shasum -a 256 "$GS/pins_gate47.json" | cut -c1-64)"
AZ='Blockchain/Dev/deployment/azure'; DEPLOY="$AZ/deploy.sh"; PRED="$AZ/check-startup-migrations.sh"
TESTSH='Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh'; AKTO='systemTest/akto/src/setup/aktoRateLimit.ts'
TOT=0; OK=0; MM=0; RETRIES=0
ctl() { # ctl <id> <expected rc> <why regex or ''> -- <command...>
  local id="$1" exp="$2" why="$3"; shift 4
  local out rc good try=0; out="$("$@" 2>&1)"; rc=$?
  # GitHub intermittently DENIES the Secuura deploy key's SSH auth under a burst of ls-remote / fetch (measured 2026-09-29T14:51-14:52Z: 3 of 5
  # denied; 6 of 6 OK at 5 s spacing at 15:05Z). The GUARDS fail closed on it (rc 2 / REFUSING), which is right; the HARNESS retries such a run
  # up to 3 times, 20 s apart, and counts every retry in the SUMMARY — a control is never judged on an SSH denial.
  while [ "$try" -lt 3 ] && printf '%s' "$out" | grep -qE 'Permission denied \(publickey\)|Could not read from remote repository'; do
    try=$((try + 1)); RETRIES=$((RETRIES + 1)); sleep 20; out="$("$@" 2>&1)"; rc=$?
  done
  printf '%s\n' "$out" > "$W/$id.out"
  good=0; [ "$rc" = "$exp" ] && { [ -z "$why" ] || printf '%s' "$out" | grep -qE -- "$why"; } && good=1
  [ "$INV" = 1 ] && good=$((1 - good))
  TOT=$((TOT + 1)); if [ "$good" = 1 ]; then OK=$((OK + 1)); v=OK; else MM=$((MM + 1)); v=MISMATCH; fi
  local shown=''; if [ -n "$why" ]; then shown="$(printf '%s' "$out" | grep -E -- "$why" | tail -1)"; fi
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|TESTREFS|MODE' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
mkcommit() { # mkcommit <parent> <path> <python transform of s (the blob text)> [<recorded mode override>] -> prints the new commit sha (scratch clone only)
  local par="$1" p="$2" tf="$3" mo="${4:-}" idx="$W/idx.$(date +%s).$RANDOM" nb tree mode
  git -C "$CL" show "$par:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp"
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"
  mode="${mo:-$(git -C "$CL" ls-tree "$par" -- "$p" | awk '{print $1}')}"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$par"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mode,$nb,$p"
  tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"   # the temp index stays in $W (never deleted)
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate47.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate47.invalid GIT_AUTHOR_DATE=2026-09-30T00:00:00Z GIT_COMMITTER_DATE=2026-09-30T00:00:00Z \
    git -C "$CL" commit-tree "$tree" -p "$par" -m "gate47 control plant: $p${mo:+ recorded $mo}"
}
echo "=== controls_gate47 $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1349 head $H49 (merge-base $MB49) | #1350 head $H50 | plants $W"

echo "--- pin_gate47.py (heads, shape, the move, overlap, each alone, the chain + reverse, END, RECORDED modes, the hook) — simulations write pins_gate47.SIM-<name>.json only"
PN="$GS/pin_gate47.py"
ctl PN0  0 'PASS: FAIL=0 -> pins_gate47.SIM-real.json' -- python3 "$PN" "$SP" --simulate real ""
ctl PN0e 0 "END_TREE $END" -- cat "$W/PN0.out"
ctl PN0v 0 "REVERSE-order END $END \| == END_TREE: True" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 6 path\(s\) pinned, 6 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0c 0 '#1349 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 2 path\(s\) .* reaches its own paths: NONE' -- cat "$W/PN0.out"
ctl PN0d 0 'OVERLAP SUMMARY: 1 pair\(s\) checked, 0 overlapping \| 6 path\(s\) in total, 6 distinct' -- cat "$W/PN0.out"
ctl PN0h 0 '\.githooks/pre-push: .*IDENTICAL in every tree' -- cat "$W/PN0.out"
ctl PN0j 0 '#1349: 0 of 2 path\(s\) under Blockchain/Dev/ .*FAST-SKIPS' -- cat "$W/PN0.out"
ctl PN0k 0 '#1350: 4 of 4 path\(s\) under Blockchain/Dev/ .*TRIGGERS' -- cat "$W/PN0.out"
ctl PN1  1 '\(A\) #1349 head .* != the expected \(pinned\) head' -- python3 "$PN" "$SP" --expect-head "1349=$DEV"
ctl PN1b 1 '\(A\) #1350 head .* != the expected \(pinned\) head' -- python3 "$PN" "$SP" --expect-head "1350=$H49"
# PN3: a #1349 stand-in (on its real base 8c810023f9c9) that ALSO edits deploy.sh on the line #1348's squash inserted after — a CONFLICT over develop.
CFL="$(mkcommit "$H49" "$DEPLOY" "a = 'log_error \"Post-deploy verification found \$ERRORS issue(s) — see above\"'; ls = s.split('\n'); ix = [i for i, l in enumerate(ls) if a in l]; assert len(ix) == 1, ix; ls[ix[0]] = ls[ix[0]] + '  # gate47 control plant: the line #1348 inserted after'; ls.insert(ix[0] + 1, '        : # gate47 control plant'); s = '\n'.join(ls)")"
ctl PN3  1 '\(E\) #1349 does not merge ALONE cleanly onto develop' -- python3 "$PN" "$SP" --simulate cfl "1349=$CFL"
ctl PN3b 0 'step #1349 NOT clean' -- cat "$W/PN3.out"
ctl PN4  0 '\(C\) #1349: the develop move touches its own path' -- cat "$W/PN3.out"
# PN5: a #1349 stand-in that ALSO edits the predicate #1350 edits — the OVERLAP line must print, and the chain must refuse.
OVL="$(mkcommit "$H49" "$PRED" "s = s + '# gate47 control plant: #1349 also touches the predicate\n'")"
ctl PN5  1 'OVERLAP #1349 x #1350: \[.Blockchain/Dev/deployment/azure/check-startup-migrations.sh.\]' -- python3 "$PN" "$SP" --simulate ovl "1349=$OVL"
M644="$(mkcommit "$H50" "$DEPLOY" "pass" 100644)"
ctl PN6  1 '#1350 Blockchain/Dev/deployment/azure/deploy.sh: want 100755 \| head 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m644 "1350=$M644"
M755="$(mkcommit "$H50" "$TESTSH" "pass" 100755)"
ctl PN7  1 '#1350 Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh: want 100644 \| head 100755 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1350=$M755"
A755="$(mkcommit "$H49" "$AKTO" "pass" 100755)"
ctl PN7b 1 '#1349 systemTest/akto/src/setup/aktoRateLimit.ts: want 100644 \| head 100755 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate a755 "1349=$A755"

echo "--- testrefs_gate47.py (the census; CT-POS x2 / CT-NEG / CT-TREE inside)"
TR="$GS/testrefs_gate47.py"
ctl TR0  0 'TESTREFS PASS: 0 control problem' -- python3 "$TR" "$SP"
ctl TR0n 0 "CENSUS UNION \(PATH \+ BASENAME, at ${END:0:12}\): 7 test file" -- cat "$W/TR0.out"
# TR1: the census at DEVELOP — #1349's test does not exist there yet, so its CT-POS must FAIL (the tree argument is honoured), #1350's must hold,
# and CT-TREE is not run at a tree other than END.
ctl TR1  1 'CT-POS: #1349 its own test .* is not found' -- python3 "$TR" "$SP" --tree "$DEV"
ctl TR1b 0 'CT-POS #1350 its own test found by the census: True OK' -- cat "$W/TR1.out"
ctl TR1t 1 '' -- grep -q 'CT-TREE' "$W/TR1.out"
ctl TR2  1 'CT-POS: #1349 its own test .* is not found' -- env G47_TR_GLOB=':(glob)Blockchain/**/*.gate47-nomatch' python3 "$TR" "$SP"
ctl TR2b 0 'CT-POS: #1350 its own test .* is not found' -- cat "$W/TR2.out"
ctl TR4  0 'BASENAME .*\)deploy\\\\\.sh.\]: 1 file' -- cat "$W/TR0.out"
ctl TR4p 0 "PATH +\['Blockchain/Dev/deployment/azure/deploy.sh'[^]]*\]: 0 file" -- cat "$W/TR0.out"
ctl TR5  0 'CT-TREE #1349 test blob at END [0-9a-f]{12} == head [0-9a-f]{12}: True \| at develop ABSENT \| #1350 ks1054 test blob at END [0-9a-f]{12} == head [0-9a-f]{12}: True \| != develop [0-9a-f]{12}: True OK' -- cat "$W/TR0.out"

echo "--- keyscan_gate47.py (subjects, bodies, live-surface FLAGs)"
KS="$GS/keyscan_gate47.py"
S49="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1349"]["subject"])' "$GS/kit.json")"
S50="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1350"]["subject"])' "$GS/kit.json")"
ctl KS0  0 'KEYSCAN PASS: 12 checks over 2 PRs, 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1  1 'FAIL #1349 S2' -- python3 "$KS" "$SP" --pr 1349 --subject "$S49 (#1349)"
ctl KS2  1 'FAIL #1350 S1' -- python3 "$KS" "$SP" --pr 1350 --subject "KS-1054: a skipped check stops reading as a pass (KS-1374)"
ctl KS2b 1 'FAIL #1349 S1' -- python3 "$KS" "$SP" --pr 1349 --subject "KS-1054: pace the Akto scan by the target it attacks"
ctl KS3  1 'FAIL #1350 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --pr 1350 --subject "${S50}0123456789012"
printf '' > "$W/b_empty.txt";                                   ctl KS4 1 'FAIL #1349 B1 KS-1374' -- python3 "$KS" "$SP" --pr 1349 --body-file "$W/b_empty.txt"
printf 'Refs KS-1054\nCloses KS-1054\n' > "$W/b_close.txt";      ctl KS5 1 'FAIL #1350 B2' -- python3 "$KS" "$SP" --pr 1350 --body-file "$W/b_close.txt"
printf 'Refs KS-1374\nthe KS-1054 predicate\n' > "$W/b_for.txt"; ctl KS6 1 'FAIL #1349 B3: .*foreign \[.KS-1054.\]' -- python3 "$KS" "$SP" --pr 1349 --body-file "$W/b_for.txt"
printf 'KS-1054 continues the KS-1332 predicate\n' > "$W/pb.txt"; ctl KS7 0 'FLAG #1350 PR body: .*FOREIGN \[.KS-1332.\]' -- python3 "$KS" "$SP" --pr 1350 --prbody-file "$W/pb.txt"
# KS8: a subject that is FALSE of the diff (#1350 ALSO makes python3-absent FAIL a deploy — "changes no exit status" is false) still PASSES the
# key scan — the scan cannot judge TRUTH; SUBJECT-TRUE-OF-DIFF is the gate's, not this tool's.
ctl KS8  0 'KEYSCAN PASS: 6 checks over 1350, 0 FAIL' -- python3 "$KS" "$SP" --pr 1350 --subject "KS-1054: a skipped migration check reads as a skip; no exit status changes"
ctl KS9  0 'INFO #1349 PR title == declared subject: True' -- cat "$W/KS0.out"
ctl KS9b 0 'INFO #1350 PR title == declared subject: True' -- cat "$W/KS0.out"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L1  6 '#1349 — .* is not at .* AND refs/pull/1349/head' -- env G47_HEAD_1349="$DEV" "$L" --check
ctl L1b 6 '#1350 — .* is not at .* AND refs/pull/1350/head' -- env G47_HEAD_1350="$H49" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G47_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1350 — the compare is not the pinned' -- env G47_PATHS_1350="Blockchain/Dev/package.json" "$L" --check
sed "s/GO (Seat B 46th): merge 1349 1350 on gate47/GO (Seat B 45th): merge 1349 1350 on gate47/g" "$PROMPT" > "$W/p_go.txt";   ctl L4 26 'merge authority / the GO string' -- env G47_PROMPT="$W/p_go.txt" "$L" --check
sed "s/The merge seat is Seat B 46th/The merge seat is Seat B 47th/g" "$PROMPT" > "$W/p_seat.txt";                               ctl L4b 26 'merge authority / the GO string' -- env G47_PROMPT="$W/p_seat.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                                        ctl L5 8 'unfilled double-brace' -- env G47_PROMPT="$W/p_tok.txt" "$L" --check
i=0
for kw in HOOK-SKIPPED-LEGS-1349 SUITE-1349 SUITE-1350-MACOS SUITE-1350-GNU CALLER-CELLS-1350 N-1348-6-BOTH-WAYS R8-EXECUTES PYTHON3-ABSENT-FAILS-CLOSED TAMPER-ARMS-1350 MODES DRAFTED-COMMENTS-CHECKED CLEAN-MERGE SUBJECT-TRUE-OF-DIFF REPORT-HASH-LAST TIERING; do
  i=$((i + 1)); sed "s/$kw/$kw-X/g" "$PROMPT" > "$W/p_kw$i.txt"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G47_PROMPT="$W/p_kw$i.txt" "$L" --check
done
sed "s/$H49/${H49:0:39}x/g" "$CAP" > "$W/cap_no49.md";                                                                             ctl L7 20 "do not both name #1349's head" -- env G47_BRIEF="$W/cap_no49.md" "$L" --check
sed "s/$H50/${H50:0:39}x/g" "$CAP" > "$W/cap_no50.md";                                                                             ctl L7b 20 "do not both name #1350's head" -- env G47_BRIEF="$W/cap_no50.md" "$L" --check
sed "s/NO ticket filed/NO tickets filed/g" "$PROMPT" > "$W/p_hold.txt";                                                          ctl L8 39 'the HOLDS' -- env G47_PROMPT="$W/p_hold.txt" "$L" --check
sed "s/You NEVER reply to Peter/You may reply to Peter/g" "$PROMPT" > "$W/p_hold2.txt";                                          ctl L8b 39 'the HOLDS' -- env G47_PROMPT="$W/p_hold2.txt" "$L" --check
sed 's/Never read or write a real `.env`/Never write a real `.env`/g' "$PROMPT" > "$W/p_hold3.txt";                                ctl L8c 39 'the HOLDS' -- env G47_PROMPT="$W/p_hold3.txt" "$L" --check
sed 's/Docker runs are `--rm --network none` with the source mounted READ-ONLY/Docker runs are `--rm`/g' "$PROMPT" > "$W/p_hold4.txt"; ctl L8d 39 'the HOLDS' -- env G47_PROMPT="$W/p_hold4.txt" "$L" --check
sed 's/No `az` command of any kind/No `az login`/g' "$PROMPT" > "$W/p_hold5.txt";                                                  ctl L8e 39 'the HOLDS' -- env G47_PROMPT="$W/p_hold5.txt" "$L" --check
sed 's/NO checklist tick/NO early checklist tick/g' "$PROMPT" > "$W/p_hold6.txt";                                                  ctl L8f 39 'the HOLDS' -- env G47_PROMPT="$W/p_hold6.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                                          ctl L10 31 'launch develop / the END_TREE' -- env G47_PROMPT="$W/p_dev.txt" "$L" --check
sed "s/#1350 T1 —/#1350 T2 —/" "$PROMPT" > "$W/p_tier.txt";                                                                        ctl L11 7 'the tier lines' -- env G47_PROMPT="$W/p_tier.txt" "$L" --check
sed "s/a round-1 NO GO goes back to the author for round 2/a round-1 NO GO ships nothing/" "$PROMPT" > "$W/p_round.txt";           ctl L11b 7 'the tiering rule' -- env G47_PROMPT="$W/p_round.txt" "$L" --check
sed "s/PR #1349 is KS-1374/PR #1349 is KS-1373/" "$PROMPT" > "$W/p_tkt.txt";                                                       ctl L12 32 "BOTH state 'PR #1349 is KS-1374'" -- env G47_PROMPT="$W/p_tkt.txt" "$L" --check
sed "s/MG-1 6 over 6 paths/MG-1 over the paths/g" "$PROMPT" > "$W/p_add.txt";                                                      ctl L13 25 'the MERGE ADDENDUM rules' -- env G47_PROMPT="$W/p_add.txt" "$L" --check
sed "s/NOTHING to report.md after you send the verdict mail/little to report.md after you send the verdict mail/g" "$PROMPT" > "$W/p_hash.txt"; ctl L13b 25 'REPORT-HASH-LAST' -- env G47_PROMPT="$W/p_hash.txt" "$L" --check
sed "s/EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF/EVERY SUBJECT YOU PROPOSE SHOULD FIT THE DIFF/g" "$PROMPT" > "$W/p_true.txt"; ctl L13c 25 'the MERGE ADDENDUM rules' -- env G47_PROMPT="$W/p_true.txt" "$L" --check
sed "s/drafted texts: KS-1374/drafted texts: none/g" "$PROMPT" > "$W/p_dt.txt";                                                    ctl L13d 25 'the MERGE ADDENDUM rules' -- env G47_PROMPT="$W/p_dt.txt" "$L" --check
sed "s/GATE47 #1349 #1350/GATE46 #1349 #1350/g" "$PROMPT" > "$W/p_subj.txt";                                                        ctl L14 23 'the verdict subject' -- env G47_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                                     ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
sed "s#$GS/linear_gate47.md#$GS/linear_elsewhere.md#g" "$PROMPT" > "$W/p_lin.txt";                                                ctl L16 8 'the Linear read' -- env G47_PROMPT="$W/p_lin.txt" "$L" --check
sed "s#$GS/drafted_texts_gate47.md#$GS/drafted_elsewhere.md#g" "$PROMPT" > "$W/p_dr.txt";                                         ctl L17 8 'the drafted texts' -- env G47_PROMPT="$W/p_dr.txt" "$L" --check
sed "s#2026-09-29-batch1348r2-g46/report.md#2026-09-29-batch1348-g45/report.md#g" "$PROMPT" > "$W/p_prev.txt";                     ctl L18 8 'the previous round report' -- env G47_PROMPT="$W/p_prev.txt" "$L" --check
sed "s#$GS/overlap_probe_1.out#$GS/overlap_probe_elsewhere.out#g" "$PROMPT" > "$W/p_ovp.txt";                                        ctl L19 8 'the out-of-kit overlap probe' -- env G47_PROMPT="$W/p_ovp.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate47.sh"
# R0: the REAL census, kit.json sequenced_out_of_kit EMPTY — #1351 (KS-1386, opened 14:37:24Z while these controls were first run) touches
# aktoRateLimit.ts, so the launch action REFUSES rc 15. This is the kit's live state at drafting, not a plant.
ctl R0  15 'OVERLAP #1351 .*paths \[.systemTest/akto/src/setup/aktoRateLimit.ts.\]' -- "$R" "$L" "$SP" --dry-run
# A stand-in for Wednesday's sequencing (G47_SEQUENCED, controls-only): #1351 at its CURRENT head is reported, not refused; at a wrong head it refuses.
H51="$(git -C "$CL" rev-parse refs/remotes/pr/1351)"
printf '{"1351": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H51" > "$W/seq_ok.json"
printf '{"1351": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$H49" > "$W/seq_bad.json"
export G47_SEQUENCED="$W/seq_ok.json"
ctl R0s 0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0q 0 'SEQUENCED OUT-OF-KIT #1351 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- cat "$W/R0s.out"
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key \| 1 sequenced by Wednesday' -- cat "$W/R0s.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pins, 2 of 2' -- cat "$W/R0s.out"
ctl R0w 15 'OVERLAP #1351 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G47_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
: > "$W/routing_empty.conf";                                               ctl R1 1 'is not registered in inbox_routing.conf' -- env G47_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2  15 'OVERLAP #[0-9]+ .*paths \[.Blockchain/Dev/package-lock.json.\]' -- env G47_OVERLAP_EXTRA="Blockchain/Dev/package-lock.json" "$R" "$L" "$SP" --dry-run
ctl R3  15 'OVERLAP #1253 .*title keys \[.KS-1297.\]' -- env G47_TITLE_KEY="KS-1297" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #9[0-9]+ dependabot' -- env G47_WIDEN_RX="^dependabot/" "$R" "$L" "$SP" --dry-run
sed "s/|$H49|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh"; ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/|$H50|/|$H49|/" "$L" > "$W/launcher_wronghead50.sh"; chmod +x "$W/launcher_wronghead50.sh"; ctl R5b 11 'a head moved' -- "$R" "$W/launcher_wronghead50.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1349|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G47_ROUTING="$W/routing_ok.conf" G47_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
unset G47_SEQUENCED
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step-0 outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins are untouched by every control above"
ctl PNZ 0 '' -- test "$(shasum -a 256 "$GS/pins_gate47.json" | cut -c1-64)" = "$PINSHA"
echo "SUMMARY gate47: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
