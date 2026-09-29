#!/bin/bash
# controls_gate46.sh — every guard in the gate46 kit driven on the REAL subject and on PLANTED defects, each with the rc it must give and a WHY pattern
# its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a control that makes it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g46_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate46.json is sha256-checked unchanged at the end (PNZ). The launcher runs with --check (headless) except L9, the real launch path with
# stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run that must refuse at step 0, routing) and R8
# (a real run with a routed temp file that must stop at G46_STOP_AFTER_3B) — both stop long before the usage gate / cockpit.
# Mode plants (PN6 / PN7) RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>): core.filemode is false, a disk chmod proves nothing.
# Shape copied from the gate45 controls, re-keyed for gate46 (ONE PR, #1348 round 2, one commit behind develop).
# Usage: controls_gate46.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g46_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g46_sp/clone"; L="$GS/launch_qa_secuura_batch1348r2.sh"; PROMPT="$GS/2026-09-29_secuura-batch1348r2.prompt.txt"; CAP="$GS/mail_gate46_ready.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate46.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"
H="$(PJ prs.1348.head)"; MB="$(PJ prs.1348.merge_base)"
PINSHA="$(shasum -a 256 "$GS/pins_gate46.json" | cut -c1-64)"
DEPLOY='Blockchain/Dev/deployment/azure/deploy.sh'; TESTSH='Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh'
COMPOSE='Blockchain/Dev/docker-compose.yml'
TOT=0; OK=0; MM=0
ctl() { # ctl <id> <expected rc> <why regex or ''> -- <command...>
  local id="$1" exp="$2" why="$3"; shift 4
  local out rc good; out="$("$@" 2>&1)"; rc=$?
  printf '%s\n' "$out" > "$W/$id.out"
  good=0; [ "$rc" = "$exp" ] && { [ -z "$why" ] || printf '%s' "$out" | grep -qE -- "$why"; } && good=1
  [ "$INV" = 1 ] && good=$((1 - good))
  TOT=$((TOT + 1)); if [ "$good" = 1 ]; then OK=$((OK + 1)); v=OK; else MM=$((MM + 1)); v=MISMATCH; fi
  local shown=''; if [ -n "$why" ]; then shown="$(printf '%s' "$out" | grep -E -- "$why" | tail -1)"; fi
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|TESTREFS|MODE' | tail -1)"
  printf 'CONTROL %-5s expect rc %s%s | got rc %s -> %s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$(printf '%s' "$shown" | cut -c1-190)"
}
mkcommit() { # mkcommit <parent> <path> <python transform of s (the blob text)> [<recorded mode override>] -> prints the new commit sha (scratch clone only)
  local par="$1" p="$2" tf="$3" mo="${4:-}" idx="$W/idx.$(date +%s).$RANDOM" nb tree mode
  git -C "$CL" show "$par:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp"
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"
  mode="${mo:-$(git -C "$CL" ls-tree "$par" -- "$p" | awk '{print $1}')}"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$par"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mode,$nb,$p"
  tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"   # the temp index stays in $W (never deleted)
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate46.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate46.invalid GIT_AUTHOR_DATE=2026-09-29T00:00:00Z GIT_COMMITTER_DATE=2026-09-29T00:00:00Z \
    git -C "$CL" commit-tree "$tree" -p "$par" -m "gate46 control plant: $p${mo:+ recorded $mo}"
}
echo "=== controls_gate46 $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1348 head $H | merge-base $MB | plants $W"

echo "--- pin_gate46.py (the head, the shape, the round-2 delta, the move, the squash over develop, END, the RECORDED modes) — simulations write pins_gate46.SIM-<name>.json only"
PN="$GS/pin_gate46.py"
ctl PN0 0 'PASS: FAIL=0 -> pins_gate46.SIM-real.json' -- python3 "$PN" "$SP" --simulate real ""
ctl PN0e 0 "END_TREE $END" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 2 path\(s\) pinned, 2 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0c 0 'move [0-9a-f]{12}\.\.[0-9a-f]{12}: 6 path\(s\) .* reaches its own paths: NONE' -- cat "$W/PN0.out"
ctl PN0r 0 'deploy.sh round 1 .* BYTE-EQUAL \(blob\+mode\): True' -- cat "$W/PN0.out"
ctl PN1 1 '\(A\) #1348 head .* != the expected \(pinned\) head' -- python3 "$PN" "$SP" --expect-head "1348=$DEV"
PRD="$(mkcommit "$H" "$DEPLOY" "s = s + '# gate46 control: a round-2 stand-in that ALSO edits deploy.sh\n'")"
ctl PN2 1 '\(R\) the round-2 delta .* != the declared' -- python3 "$PN" "$SP" --simulate prod "1348=$PRD"
ctl PN2b 0 'deploy.sh changed between round 1 and the head' -- cat "$W/PN2.out"
CFL="$(mkcommit "$H" "$COMPOSE" "a = 'RATE_LIMIT_MAX_REQUESTS=\${RATE_LIMIT_MAX_REQUESTS:-2000}'; ls = s.split('\n'); ix = [i for i, l in enumerate(ls) if a in l]; assert len(ix) == 1, ix; ls[ix[0]] = ls[ix[0]] + '  # gate46 control plant: the SAME line #1347 rewrote'; s = '\n'.join(ls)")"
ctl PN3 1 '\(E\) #1348 NOT clean over develop' -- python3 "$PN" "$SP" --simulate cfl "1348=$CFL"
ctl PN4 0 '\(C\) #1348: the develop move touches its own path' -- cat "$W/PN3.out"
M644="$(mkcommit "$H" "$DEPLOY" "pass" 100644)"
ctl PN6 1 '#1348 Blockchain/Dev/deployment/azure/deploy.sh: want 100755 \| head 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m644 "1348=$M644"
M755="$(mkcommit "$H" "$TESTSH" "pass" 100755)"
ctl PN7 1 '#1348 Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh: want 100644 \| head 100755 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1348=$M755"

echo "--- testrefs_gate46.py (the census; CT-POS / CT-NEG / CT-TREE inside)"
TR="$GS/testrefs_gate46.py"
ctl TR0 0 'TESTREFS PASS: 0 control problem' -- python3 "$TR" "$SP"
ctl TR0n 0 "CENSUS UNION \(PATH \+ BASENAME, at ${END:0:12}\): 1 test file" -- cat "$W/TR0.out"
ctl TR1 0 'TESTREFS PASS' -- python3 "$TR" "$SP" --tree "$DEV"
ctl TR1t 1 '' -- grep -q 'CT-TREE' "$W/TR1.out"
ctl TR2 1 'CT-POS: its own test .* is not found' -- env G46_TR_GLOB=':(glob)Blockchain/**/*.gate46-nomatch' python3 "$TR" "$SP"
ctl TR4 0 'BASENAME .*deploy[^]]*\]: 1 file' -- cat "$W/TR0.out"
ctl TR4p 0 "PATH +\['Blockchain/Dev/deployment/azure/deploy.sh'[^]]*\]: 0 file" -- cat "$W/TR0.out"
ctl TR5 0 'CT-TREE the ks1054 test blob at END [0-9a-f]{12} == head [0-9a-f]{12}: True \| != develop [0-9a-f]{12}: True OK' -- cat "$W/TR0.out"

echo "--- keyscan_gate46.py (subject, body, live-surface FLAGs)"
KS="$GS/keyscan_gate46.py"
SUBJ="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1348"]["subject"])' "$GS/kit.json")"
ctl KS0 0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1 1 'FAIL #1348 S2' -- python3 "$KS" "$SP" --subject "$SUBJ (#1348)"
ctl KS2 1 'FAIL #1348 S1' -- python3 "$KS" "$SP" --subject "KS-1054: deploy.sh exits non-zero (KS-1332)"
ctl KS3 1 'FAIL #1348 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --subject "${SUBJ}01234567"
printf '' > "$W/b_empty.txt";                                   ctl KS4 1 'FAIL #1348 B1 KS-1054' -- python3 "$KS" "$SP" --body-file "$W/b_empty.txt"
printf 'Refs KS-1054\nCloses KS-1054\n' > "$W/b_close.txt";      ctl KS5 1 'FAIL #1348 B2' -- python3 "$KS" "$SP" --body-file "$W/b_close.txt"
printf 'Refs KS-1054\nthe KS-206 ceiling\n' > "$W/b_for.txt";    ctl KS6 1 'FAIL #1348 B3: .*foreign \[.KS-206.\]' -- python3 "$KS" "$SP" --body-file "$W/b_for.txt"
printf 'KS-1054 continues the KS-1332 predicate\n' > "$W/pb.txt"; ctl KS7 0 'FLAG #1348 PR body: .*FOREIGN \[.KS-1332.\]' -- python3 "$KS" "$SP" --prbody-file "$W/pb.txt"
# KS8: a subject that is FALSE of the diff (deploy.sh fails on ANY counted issue, N-1348-3, not migrations only) still PASSES the key scan —
# the scan cannot judge TRUTH; SUBJECT-TRUE-OF-DIFF is the gate's, not this tool's.
ctl KS8 0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL' -- python3 "$KS" "$SP" --subject "KS-1054: deploy.sh exits non-zero only when startup migrations have failed"
ctl KS9 0 'INFO #1348 PR title == declared subject: True' -- cat "$W/KS0.out"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0 0 'all guards pass' -- "$L" --check
ctl L1 6 '#1348 — .* is not at .* AND refs/pull/1348/head' -- env G46_HEAD_1348="$DEV" "$L" --check
ctl L2 17 'origin develop .* != the pinned develop' -- env G46_CUR_DEV="$OLDDEV" "$L" --check
ctl L3 10 '#1348 — the compare is not the pinned' -- env G46_PATHS_1348="Blockchain/Dev/package.json" "$L" --check
sed "s/GO (Seat B 46th): merge 1348 on gate46/GO (Seat B 45th): merge 1348 on gate46/g" "$PROMPT" > "$W/p_go.txt";            ctl L4 26 'merge authority / the GO string' -- env G46_PROMPT="$W/p_go.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                                  ctl L5 8 'unfilled double-brace' -- env G46_PROMPT="$W/p_tok.txt" "$L" --check
sed "s/TAMPER-RETURN-0-REDS-E1/TAMPER-RETURN-0/g" "$PROMPT" > "$W/p_kw.txt";                                               ctl L6 33 "by-name keyword 'TAMPER-RETURN-0-REDS-E1'" -- env G46_PROMPT="$W/p_kw.txt" "$L" --check
sed "s/SUITE-GNU-DEBIAN/SUITE-GNU/g" "$PROMPT" > "$W/p_gnu.txt";                                                            ctl L6b 33 "by-name keyword 'SUITE-GNU-DEBIAN'" -- env G46_PROMPT="$W/p_gnu.txt" "$L" --check
sed "s/TAMPER-UNCONDITIONAL-REDS-E2/TAMPER-UNCONDITIONAL/g" "$PROMPT" > "$W/p_unc.txt";                                     ctl L6c 33 "by-name keyword 'TAMPER-UNCONDITIONAL-REDS-E2'" -- env G46_PROMPT="$W/p_unc.txt" "$L" --check
sed "s/$H/${H:0:39}x/g" "$CAP" > "$W/cap_nohead.md";                                                                        ctl L7 20 "do not both name #1348's head" -- env G46_BRIEF="$W/cap_nohead.md" "$L" --check
sed "s/NO ticket filed/NO tickets filed/g" "$PROMPT" > "$W/p_hold.txt";                                                    ctl L8 39 'the HOLDS' -- env G46_PROMPT="$W/p_hold.txt" "$L" --check
sed "s/You NEVER reply to Peter/You may reply to Peter/g" "$PROMPT" > "$W/p_hold2.txt";                                    ctl L8b 39 'the HOLDS' -- env G46_PROMPT="$W/p_hold2.txt" "$L" --check
sed 's/Never read or write a real `.env`/Never write a real `.env`/g' "$PROMPT" > "$W/p_hold3.txt";                          ctl L8c 39 'the HOLDS' -- env G46_PROMPT="$W/p_hold3.txt" "$L" --check
sed 's/Docker runs are `--rm --network none` with the source mounted READ-ONLY/Docker runs are `--rm`/g' "$PROMPT" > "$W/p_hold4.txt"; ctl L8d 39 'the HOLDS' -- env G46_PROMPT="$W/p_hold4.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9    SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                                    ctl L10 31 'launch develop / the END_TREE' -- env G46_PROMPT="$W/p_dev.txt" "$L" --check
sed "s/#1348 T1 —/#1348 T2 —/" "$PROMPT" > "$W/p_tier.txt";                                                                 ctl L11 7 'the tier lines' -- env G46_PROMPT="$W/p_tier.txt" "$L" --check
sed "s/a NO GO on #1348 ships NOTHING of it/a NO GO on #1348 ships little of it/" "$PROMPT" > "$W/p_cap.txt";              ctl L11b 7 'the round-2-of-2 cap' -- env G46_PROMPT="$W/p_cap.txt" "$L" --check
sed "s/PR #1348 is KS-1054/PR #1348 is KS-1053/" "$PROMPT" > "$W/p_tkt.txt";                                                ctl L12 32 "BOTH state 'PR #1348 is KS-1054'" -- env G46_PROMPT="$W/p_tkt.txt" "$L" --check
sed "s/MG-1 2 over 2 paths/MG-1 over the paths/g" "$PROMPT" > "$W/p_add.txt";                                                ctl L13 25 'the MERGE ADDENDUM rules' -- env G46_PROMPT="$W/p_add.txt" "$L" --check
sed "s/NOTHING to report.md after you send the verdict mail/little to report.md after you send the verdict mail/g" "$PROMPT" > "$W/p_hash.txt"; ctl L13b 25 'REPORT-HASH-LAST' -- env G46_PROMPT="$W/p_hash.txt" "$L" --check
sed "s/EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF/EVERY SUBJECT YOU PROPOSE SHOULD FIT THE DIFF/g" "$PROMPT" > "$W/p_true.txt"; ctl L13c 25 'the MERGE ADDENDUM rules' -- env G46_PROMPT="$W/p_true.txt" "$L" --check
sed "s/GATE46 #1348 round 2 of 2/GATE45 #1348 round 2 of 2/g" "$PROMPT" > "$W/p_subj.txt";                                  ctl L14 23 'the verdict subject' -- env G46_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                               ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
sed "s#$GS/linear_gate46.md#$GS/linear_elsewhere.md#g" "$PROMPT" > "$W/p_lin.txt";                                          ctl L16 8 'the Linear read' -- env G46_PROMPT="$W/p_lin.txt" "$L" --check
sed "s#$GS/drafter_return_probe.out#$GS/drafter_probe_elsewhere.out#g" "$PROMPT" > "$W/p_probe.txt";                        ctl L17 8 'the drafter probe' -- env G46_PROMPT="$W/p_probe.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate46.sh"
ctl R0 0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                               ctl R1 1 'is not registered in inbox_routing.conf' -- env G46_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2 15 'OVERLAP #[0-9]+ .*paths \[.Blockchain/Dev/package-lock.json.\]' -- env G46_OVERLAP_EXTRA="Blockchain/Dev/package-lock.json" "$R" "$L" "$SP" --dry-run
ctl R3 15 'OVERLAP #1253 .*title keys \[.KS-1297.\]' -- env G46_TITLE_KEY="KS-1297" "$R" "$L" "$SP" --dry-run
ctl R4 0 'DISJOINT OUT-OF-KIT #9[0-9]+ dependabot' -- env G46_WIDEN_RX="^dependabot/" "$R" "$L" "$SP" --dry-run
sed "s/|$H|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh"; ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7 9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1348r2|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G46_ROUTING="$W/routing_ok.conf" G46_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step-0 outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins are untouched by every control above"
ctl PNZ 0 '' -- test "$(shasum -a 256 "$GS/pins_gate46.json" | cut -c1-64)" = "$PINSHA"
echo "SUMMARY gate46: $TOT controls, OK $OK, MISMATCH $MM$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
