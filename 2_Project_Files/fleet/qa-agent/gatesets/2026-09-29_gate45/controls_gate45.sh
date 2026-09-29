#!/bin/bash
# controls_gate45.sh — every guard in the gate45 kit driven on the REAL subject and on PLANTED defects, each with the rc it must give and a WHY pattern
# its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a control that makes it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g45_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate45.json is sha256-checked unchanged at the end (PNZ). The launcher runs with --check (headless) except L9, the real launch path with
# stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run that must refuse at step 0, routing) and R8
# (a real run with a routed temp file that must stop at G45_STOP_AFTER_3B) — both stop long before the usage gate / cockpit.
# Mode plants (PN6 / PN7) RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>): core.filemode is false, a disk chmod proves nothing.
# Shape copied from the gate44 controls, re-keyed for gate45 (#1348 T1 on develop, #1347 T2 round 2 one commit behind).
# Usage: controls_gate45.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g45_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g45_sp/clone"; L="$GS/launch_qa_secuura_batch1348.sh"; PROMPT="$GS/2026-09-29_secuura-batch1348.prompt.txt"; CAP="$GS/mail_gate45_ready.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate45.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"
H1348="$(PJ prs.1348.head)"; H1347="$(PJ prs.1347.head)"; MB1347="$(PJ prs.1347.merge_base)"
PINSHA="$(shasum -a 256 "$GS/pins_gate45.json" | cut -c1-64)"
DEPLOY='Blockchain/Dev/deployment/azure/deploy.sh'; TESTSH='Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh'
DEPLOYALL='Blockchain/Dev/deployment/azure/deploy-all.sh'
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
  local par="$1" p="$2" tf="$3" mo="${4:-}" idx="$W/idx.$$" nb tree mode
  git -C "$CL" show "$par:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp"
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"
  mode="${mo:-$(git -C "$CL" ls-tree "$par" -- "$p" | awk '{print $1}')}"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$par"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mode,$nb,$p"
  tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"; mv "$idx" "$W/idx.used.$$" 2>/dev/null
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate45.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate45.invalid GIT_AUTHOR_DATE=2026-09-29T00:00:00Z GIT_COMMITTER_DATE=2026-09-29T00:00:00Z \
    git -C "$CL" commit-tree "$tree" -p "$par" -m "gate45 control plant: $p${mo:+ recorded $mo}"
}
echo "=== controls_gate45 $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1347 merge-base $MB1347 | plants $W"

echo "--- pin_gate45.py (the heads, the move, the OVERLAP matrix, the chain, END, the RECORDED modes) — simulations write pins_gate45.SIM-<name>.json only"
PN="$GS/pin_gate45.py"
ctl PN0 0 'PASS: FAIL=0 -> pins_gate45.SIM-real.json .* 0 overlapping pair' -- python3 "$PN" "$SP" --simulate real ""
ctl PN0e 0 "END_TREE $END" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 2 path\(s\) pinned, 2 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0c 0 '#1347 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 4 path\(s\) .* reaches its own paths: NONE' -- cat "$W/PN0.out"
ctl PN1 1 '\(A\) #1347 head .* != the expected \(pinned\) head' -- python3 "$PN" "$SP" --expect-head "1347=$DEV"
OVL="$(mkcommit "$H1347" "$DEPLOY" "s = s + '# gate45 control: an append-only edit of deploy.sh\n'")"
ctl PN2 1 'OVERLAP #1348 x #1347: \[.*deployment/azure/deploy.sh' -- python3 "$PN" "$SP" --simulate ovl "1347=$OVL"
ctl PN2w 0 'step #1347 diff / blob mismatch' -- cat "$W/PN2.out"
CFL="$(mkcommit "$H1347" "$DEPLOY" "a = 'log_error \"Post-deploy verification found \$ERRORS issue(s) — see above\"\n'; assert s.count(a) == 1, s.count(a); s = s.replace(a, a + '        # gate45 control plant: the SAME insertion point #1348 uses\n', 1)")"
ctl PN3 1 'step #1347 NOT clean' -- python3 "$PN" "$SP" --simulate cfl "1347=$CFL"
MOV="$(mkcommit "$H1347" "$DEPLOYALL" "s = s + '# gate45 control: a #1347 stand-in touching a path the #1346 move touched\n'")"
ctl PN4 1 '\(C\) #1347: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate mov "1347=$MOV"
ctl PN5 0 "REVERSE-order END $END \| == END_TREE: True" -- cat "$W/PN0.out"
M644="$(mkcommit "$H1348" "$DEPLOY" "pass" 100644)"
ctl PN6 1 '#1348 Blockchain/Dev/deployment/azure/deploy.sh: want 100755 \| head 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m644 "1348=$M644"
M755="$(mkcommit "$H1348" "$TESTSH" "pass" 100755)"
ctl PN7 1 '#1348 Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh: want 100644 \| head 100755 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1348=$M755"

echo "--- testrefs_gate45.py (the census; CT-POS / CT-NEG / CT-TREE / CT-KNOWN inside)"
TR="$GS/testrefs_gate45.py"
ctl TR0 0 'TESTREFS PASS: 0 control problem' -- python3 "$TR" "$SP"
ctl TR0n 0 "CENSUS UNION \(PATH \+ BASENAME \+ IMPORT, at ${END:0:12}\): 41 test file" -- cat "$W/TR0.out"
ctl TR1 0 'TESTREFS PASS' -- python3 "$TR" "$SP" --tree "$DEV"
ctl TR1n 1 '' -- grep -q 'ks1374-platform-limit-from-env' "$W/TR1.out"
ctl TR2 1 'CT-POS .* its own test .* is not found' -- env G45_TR_GLOB=':(glob)Blockchain/**/*.gate45-nomatch' python3 "$TR" "$SP"
ctl TR3 0 'CT-KNOWN bootstrap_env_canonical_template.test.sh listed: True OK' -- cat "$W/TR0.out"
ctl TR4 0 'BASENAME .*deploy[^]]*\]: 1 file' -- cat "$W/TR0.out"
ctl TR4p 0 "PATH +\['Blockchain/Dev/deployment/azure/deploy.sh'[^]]*\]: 0 file" -- cat "$W/TR0.out"
ctl TR5 0 'CT-POS #1347 its own test\(s\) found by the census: 2 of 2 OK' -- cat "$W/TR0.out"

echo "--- keyscan_gate45.py (subjects, bodies, live-surface FLAGs)"
KS="$GS/keyscan_gate45.py"
SUBJ1347="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1347"]["subject"])' "$GS/kit.json")"
SUBJ1348="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1348"]["subject"])' "$GS/kit.json")"
TITLE1347="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1347"]["title"])' "$GS/kit.json")"
ctl KS0 0 'KEYSCAN PASS: 12 checks over 2 PRs, 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1 1 'FAIL #1348 S2' -- python3 "$KS" "$SP" --pr 1348 --subject "$SUBJ1348 (#1348)"
ctl KS2 1 'FAIL #1348 S1' -- python3 "$KS" "$SP" --pr 1348 --subject "KS-1054: deploy.sh exits non-zero (KS-1332)"
ctl KS3 1 'FAIL #1347 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --pr 1347 --subject "${SUBJ1347}xy"
printf '' > "$W/b_1348.txt";                                                   ctl KS4 1 'FAIL #1348 B1 KS-1054' -- python3 "$KS" "$SP" --pr 1348 --body-file "$W/b_1348.txt"
printf 'Refs KS-1374\nCloses KS-1374\n' > "$W/b_1347.txt";                     ctl KS5 1 'FAIL #1347 B2' -- python3 "$KS" "$SP" --pr 1347 --body-file "$W/b_1347.txt"
printf 'Refs KS-1374\nthe KS-206 ceiling\n' > "$W/b_1347f.txt";                ctl KS6 1 'FAIL #1347 B3: .*foreign \[.KS-206.\]' -- python3 "$KS" "$SP" --pr 1347 --body-file "$W/b_1347f.txt"
printf 'KS-1054 continues the KS-1332 predicate\n' > "$W/pb_1348.txt";         ctl KS7 0 'FLAG #1348 PR body: .*FOREIGN \[.KS-1332.\]' -- python3 "$KS" "$SP" --pr 1348 --prbody-file "$W/pb_1348.txt"
# KS8: the key scan PASSES #1347's stale live title — a key scan cannot judge TRUTH; SUBJECT-TRUE-OF-DIFF is the gate's, not this tool's.
ctl KS8 0 'PASS #1347 S3: declared 84, lands at 92' -- python3 "$KS" "$SP" --pr 1347 --subject "$TITLE1347"
ctl KS9 0 'INFO #1347 PR title == declared subject: False' -- cat "$W/KS0.out"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0 0 'all guards pass' -- "$L" --check
ctl L1 6 '#1347 — .* is not at .* AND refs/pull/1347/head' -- env G45_HEAD_1347="$DEV" "$L" --check
ctl L2 17 'origin develop .* != the pinned develop' -- env G45_CUR_DEV="$OLDDEV" "$L" --check
ctl L3 10 '#1348 — the compare is not the pinned' -- env G45_PATHS_1348="Blockchain/Dev/package.json" "$L" --check
sed "s/GO (Seat B 45th): merge 1348 1347 on gate45/GO (Seat B 44th): merge 1348 1347 on gate45/g" "$PROMPT" > "$W/p_go.txt"; ctl L4 26 'merge authority / the GO string' -- env G45_PROMPT="$W/p_go.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                                  ctl L5 8 'unfilled double-brace' -- env G45_PROMPT="$W/p_tok.txt" "$L" --check
sed "s/TAMPER-RETURN-0-1348/TAMPER-RETURN-1348/g" "$PROMPT" > "$W/p_kw.txt";                                               ctl L6 33 "by-name keyword 'TAMPER-RETURN-0-1348'" -- env G45_PROMPT="$W/p_kw.txt" "$L" --check
sed "s/$H1347/${H1347:0:39}x/g" "$CAP" > "$W/cap_nohead.md";                                                                ctl L7 20 "do not both name #1347's head" -- env G45_BRIEF="$W/cap_nohead.md" "$L" --check
sed "s/NO ticket filed/NO tickets filed/g" "$PROMPT" > "$W/p_hold.txt";                                                    ctl L8 39 'the HOLDS' -- env G45_PROMPT="$W/p_hold.txt" "$L" --check
sed "s/You NEVER reply to Peter/You may reply to Peter/g" "$PROMPT" > "$W/p_hold2.txt";                                    ctl L8b 39 'the HOLDS' -- env G45_PROMPT="$W/p_hold2.txt" "$L" --check
sed 's/Never read or write a real `.env`/Never write a real `.env`/g' "$PROMPT" > "$W/p_hold3.txt";                          ctl L8c 39 'the HOLDS' -- env G45_PROMPT="$W/p_hold3.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9    SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                                    ctl L10 31 'launch develop / the END_TREE' -- env G45_PROMPT="$W/p_dev.txt" "$L" --check
sed "s/#1348 T1 —/#1348 T2 —/" "$PROMPT" > "$W/p_tier.txt";                                                                 ctl L11 7 'the tier lines' -- env G45_PROMPT="$W/p_tier.txt" "$L" --check
sed "s/a NO GO on #1347 ships NOTHING/a NO GO on #1347 ships little/" "$PROMPT" > "$W/p_cap.txt";                          ctl L11b 7 'the round-2-of-2 cap' -- env G45_PROMPT="$W/p_cap.txt" "$L" --check
sed "s/PR #1347 is KS-1374/PR #1347 is KS-1373/" "$PROMPT" > "$W/p_tkt.txt";                                                ctl L12 32 "BOTH state 'PR #1347 is KS-1374'" -- env G45_PROMPT="$W/p_tkt.txt" "$L" --check
sed "s/MG-1 8 over 8 paths/MG-1 over the paths/g" "$PROMPT" > "$W/p_add.txt";                                                ctl L13 25 'the MERGE ADDENDUM rules' -- env G45_PROMPT="$W/p_add.txt" "$L" --check
sed "s/NOTHING to report.md after you send the verdict mail/little to report.md after you send the verdict mail/g" "$PROMPT" > "$W/p_hash.txt"; ctl L13b 25 'REPORT-HASH-LAST' -- env G45_PROMPT="$W/p_hash.txt" "$L" --check
sed "s/EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF/EVERY SUBJECT YOU PROPOSE SHOULD FIT THE DIFF/g" "$PROMPT" > "$W/p_true.txt"; ctl L13c 25 'the MERGE ADDENDUM rules' -- env G45_PROMPT="$W/p_true.txt" "$L" --check
sed "s/GATE45 batch #1348 #1347/GATE44 batch #1348 #1347/g" "$PROMPT" > "$W/p_subj.txt";                                    ctl L14 23 'the verdict subject' -- env G45_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                               ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
sed "s#$GS/linear_gate45.md#$GS/linear_elsewhere.md#g" "$PROMPT" > "$W/p_lin.txt";                                          ctl L16 8 'the Linear read' -- env G45_PROMPT="$W/p_lin.txt" "$L" --check
sed "s#$GS/drafter_return_probe.out#$GS/drafter_probe_elsewhere.out#g" "$PROMPT" > "$W/p_probe.txt";                        ctl L17 8 'the drafter probe' -- env G45_PROMPT="$W/p_probe.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate45.sh"
ctl R0 0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                               ctl R1 1 'is not registered in inbox_routing.conf' -- env G45_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2 15 'OVERLAP #[0-9]+ .*paths \[.Blockchain/Dev/package-lock.json.\]' -- env G45_OVERLAP_EXTRA="Blockchain/Dev/package-lock.json" "$R" "$L" "$SP" --dry-run
ctl R3 15 'OVERLAP #1253 .*title keys \[.KS-1297.\]' -- env G45_TITLE_KEY="KS-1297" "$R" "$L" "$SP" --dry-run
ctl R4 0 'DISJOINT OUT-OF-KIT #9[0-9]+ dependabot' -- env G45_WIDEN_RX="^dependabot/" "$R" "$L" "$SP" --dry-run
sed "s/|$H1347|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh"; ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7 9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1348|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G45_ROUTING="$W/routing_ok.conf" G45_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step-0 outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins are untouched by every control above"
ctl PNZ 0 '' -- test "$(shasum -a 256 "$GS/pins_gate45.json" | cut -c1-64)" = "$PINSHA"
echo "SUMMARY gate45: $TOT controls, OK $OK, MISMATCH $MM$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
