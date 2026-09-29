#!/bin/bash
# controls_gate43.sh — every guard in the gate43 kit driven on the REAL subject and on PLANTED defects, each with the rc it must give and a WHY pattern
# its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a control that makes it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g43_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate43.json is sha256-checked unchanged at the end (PNZ). The launcher runs with --check (headless) except L9, the real launch path with
# stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run that must refuse at step 0, routing) and R8
# (a real run with a routed temp file that must stop at G43_STOP_AFTER_3B) — both stop long before the usage gate / cockpit.
# Usage: controls_gate43.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g43_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g43_sp/clone"; L="$GS/launch_qa_secuura_batch1341.sh"; PROMPT="$GS/2026-09-29_secuura-batch1341.prompt.txt"; CAP="$GS/mail_gate43_ready.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate43.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"
H1341="$(PJ prs.1341.head)"; H1342="$(PJ prs.1342.head)"; H1343="$(PJ prs.1343.head)"; H1344="$(PJ prs.1344.head)"; H1345="$(PJ prs.1345.head)"
PINSHA="$(shasum -a 256 "$GS/pins_gate43.json" | cut -c1-64)"
PROXY='Blockchain/Dev/services/api-gateway/src/routes/proxy.ts'; BASEL='Blockchain/Dev/scripts/audit/audit-baseline.json'
TOT=0; OK=0; MM=0
ctl() { # ctl <id> <expected rc> <why regex or ''> -- <command...>
  local id="$1" exp="$2" why="$3"; shift 4
  local out rc good; out="$("$@" 2>&1)"; rc=$?
  printf '%s\n' "$out" > "$W/$id.out"
  good=0; [ "$rc" = "$exp" ] && { [ -z "$why" ] || printf '%s' "$out" | grep -qE -- "$why"; } && good=1
  [ "$INV" = 1 ] && good=$((1 - good))
  TOT=$((TOT + 1)); if [ "$good" = 1 ]; then OK=$((OK + 1)); v=OK; else MM=$((MM + 1)); v=MISMATCH; fi
  local shown; if [ -n "$why" ]; then shown="$(printf '%s' "$out" | grep -E -- "$why" | tail -1)"; fi
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|TESTREFS' | tail -1)"
  printf 'CONTROL %-5s expect rc %s%s | got rc %s -> %s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$(printf '%s' "$shown" | cut -c1-190)"
}
mkcommit() { # mkcommit <parent> <path> <python transform of s (the blob text)> -> prints the new commit sha (scratch clone only)
  local par="$1" p="$2" tf="$3" idx="$W/idx.$$" blob nb tree
  git -C "$CL" show "$par:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp"
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"
  mode="$(git -C "$CL" ls-tree "$par" -- "$p" | awk '{print $1}')"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$par"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mode,$nb,$p"
  tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"; mv "$idx" "$W/idx.used.$$" 2>/dev/null
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate43.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate43.invalid GIT_AUTHOR_DATE=2026-09-29T00:00:00Z GIT_COMMITTER_DATE=2026-09-29T00:00:00Z \
    git -C "$CL" commit-tree "$tree" -p "$par" -m "gate43 control plant: $p"
}
echo "=== controls_gate43 $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | old base $OLDDEV | plants $W"

echo "--- pin_gate43.py (the heads, the move, the OVERLAP matrix, the chain, END) — simulations write pins_gate43.SIM-<name>.json only"
PN="$GS/pin_gate43.py"
ctl PN0 0 'PASS: FAIL=0 -> pins_gate43.SIM-real.json .* 0 overlapping pair' -- python3 "$PN" "$SP" --simulate real ""
ctl PN0e 0 'END_TREE dd70cc631be4f2f9d8ac6c8744acf109931e4ee1' -- cat "$W/PN0.out"
ctl PN1 1 '\(A\) #1343 head .* != the expected \(pinned\) head' -- python3 "$PN" "$SP" --expect-head "1343=$DEV"
OVL="$(mkcommit "$H1344" "$PROXY" "s = s + '// gate43 control: an append-only edit of the proxy file\n'")"
ctl PN2 1 'OVERLAP #1342 x #1344: \[.*routes/proxy.ts' -- python3 "$PN" "$SP" --simulate ovl "1344=$OVL"
ctl PN2w 0 'step #1344 diff / blob mismatch' -- cat "$W/PN2.out"
CFL="$(mkcommit "$H1344" "$PROXY" "s = s.replace('    onProxyReq: (proxyReq, req) => {\n', '    onProxyReq: (proxyReq, req) => {\n      if (!proxyReq) return; // gate43 control: the SAME line #1342 edits\n', 1)")"
ctl PN3 1 'step #1344 NOT clean' -- python3 "$PN" "$SP" --simulate cfl "1344=$CFL"
MOV="$(mkcommit "$OLDDEV" "$BASEL" "s = s.replace('\"expires\"', '\"expires\"', 1) + ' '")"
ctl PN4 1 '\(C\) #1343: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate mov "1343=$MOV"
ctl PN5 0 'REVERSE-order END dd70cc631be4f2f9d8ac6c8744acf109931e4ee1 \| == END_TREE: True' -- cat "$W/PN0.out"

echo "--- testrefs_gate43.py (the census; CT-POS / CT-NEG / CT-TREE inside)"
TR="$GS/testrefs_gate43.py"
ctl TR0 0 'TESTREFS PASS: 0 control problem' -- python3 "$TR" "$SP"
ctl TR0n 0 'CENSUS UNION \(PATH \+ IMPORT, at dd70cc631be4\): 23 test file' -- cat "$W/TR0.out"
ctl TR1 0 'TESTREFS PASS' -- python3 "$TR" "$SP" --tree "$DEV"
ctl TR1n 1 '' -- grep -q 'ks1369-onproxyreq' "$W/TR1.out"
ctl TR2 1 'CT-POS .* its own test is not found' -- env G43_TR_GLOB=':(glob)Blockchain/**/*.gate43-nomatch' python3 "$TR" "$SP"
ctl TR3 0 'ks781-p3-3-body-parser-order.test.ts' -- cat "$W/TR0.out"

echo "--- keyscan_gate43.py (subjects, bodies, live-surface FLAGs)"
KS="$GS/keyscan_gate43.py"
SUBJ1342="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1342"]["subject"])' "$GS/kit.json")"
ctl KS0 0 'KEYSCAN PASS: 31 checks over 5 PRs, 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1 1 'FAIL #1342 S2' -- python3 "$KS" "$SP" --pr 1342 --subject "$SUBJ1342 (#1342)"
ctl KS2 1 'FAIL #1343 S1' -- python3 "$KS" "$SP" --pr 1343 --subject "KS-1371: unrevoke refuses a negative index (KS-662 kept)"
ctl KS3 1 'FAIL #1342 S3' -- python3 "$KS" "$SP" --pr 1342 --subject "$SUBJ1342 and a tail past ninety-two"
printf 'Refs KS-1375\n' > "$W/b_1341.txt";                                   ctl KS4 1 'FAIL #1341 B1 KS-1368' -- python3 "$KS" "$SP" --pr 1341 --body-file "$W/b_1341.txt"
printf 'Refs KS-1360\nCloses KS-1360\n' > "$W/b_1345.txt";                   ctl KS5 1 'FAIL #1345 B2' -- python3 "$KS" "$SP" --pr 1345 --body-file "$W/b_1345.txt"
printf 'Refs KS-1359\nthe KS-5 clamp kept\n' > "$W/b_1344.txt";              ctl KS6 1 'FAIL #1344 B3: .*foreign \[.KS-5.\]' -- python3 "$KS" "$SP" --pr 1344 --body-file "$W/b_1344.txt"
printf 'KS-1371 per the KS-662 ruling\n' > "$W/pb_1343.txt";                 ctl KS7 0 'FLAG #1343 PR body: .*FOREIGN \[.KS-662.\]' -- python3 "$KS" "$SP" --pr 1343 --prbody-file "$W/pb_1343.txt"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0 0 'all guards pass' -- "$L" --check
ctl L1 6 '#1343 — .* is not at .* AND refs/pull/1343/head' -- env G43_HEAD_1343="$DEV" "$L" --check
ctl L2 17 'origin develop .* != the pinned develop' -- env G43_CUR_DEV="$OLDDEV" "$L" --check
ctl L3 10 '#1344 — the compare is not the pinned' -- env G43_PATHS_1344="Blockchain/Dev/package.json" "$L" --check
sed "s/GO (Seat B 45th): merge 1341 1342 1343 1344 1345 on gate43/GO (Seat B 44th): merge 1341 1342 1343 1344 1345 on gate43/g" "$PROMPT" > "$W/p_go.txt"; ctl L4 26 'merge authority / the GO string' -- env G43_PROMPT="$W/p_go.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                                  ctl L5 8 'unfilled double-brace' -- env G43_PROMPT="$W/p_tok.txt" "$L" --check
sed "s/UPSTREAM-NOT-HUNG-1342/UPSTREAM-NOT-HUNG/g" "$PROMPT" > "$W/p_kw.txt";                                              ctl L6 33 "by-name keyword 'UPSTREAM-NOT-HUNG-1342'" -- env G43_PROMPT="$W/p_kw.txt" "$L" --check
sed "s/$H1345/${H1345:0:39}x/g" "$CAP" > "$W/cap_nohead.md";                                                                ctl L7 20 "do not both name #1345's head" -- env G43_BRIEF="$W/cap_nohead.md" "$L" --check
sed "s/NO ticket filed/NO tickets filed/g" "$PROMPT" > "$W/p_hold.txt";                                                    ctl L8 39 'the HOLDS' -- env G43_PROMPT="$W/p_hold.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9    SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                                    ctl L10 31 'launch develop / the END_TREE' -- env G43_PROMPT="$W/p_dev.txt" "$L" --check
sed "s/#1342 T1 —/#1342 T2 —/" "$PROMPT" > "$W/p_tier.txt";                                                                 ctl L11 7 'the tier lines' -- env G43_PROMPT="$W/p_tier.txt" "$L" --check
sed "s/PR #1344 is KS-1359/PR #1344 is KS-1358/" "$PROMPT" > "$W/p_tkt.txt";                                                ctl L12 32 "BOTH state 'PR #1344 is KS-1359'" -- env G43_PROMPT="$W/p_tkt.txt" "$L" --check
sed "s/MG-1 11 over 11 paths/MG-1 over the paths/g" "$PROMPT" > "$W/p_add.txt";                                              ctl L13 25 'the MERGE ADDENDUM rules' -- env G43_PROMPT="$W/p_add.txt" "$L" --check
sed "s/GATE43 batch #1341-#1345/GATE42 batch #1341-#1345/g" "$PROMPT" > "$W/p_subj.txt";                                    ctl L14 23 'the verdict subject' -- env G43_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                               ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate43.sh"
ctl R0 0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                               ctl R1 1 'is not registered in inbox_routing.conf' -- env G43_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2 15 'OVERLAP #[0-9]+ .*paths \[.Blockchain/Dev/package-lock.json.\]' -- env G43_OVERLAP_EXTRA="Blockchain/Dev/package-lock.json" "$R" "$L" "$SP" --dry-run
ctl R3 15 'OVERLAP #1253 .*title keys \[.KS-1297.\]' -- env G43_TITLE_KEY="KS-1297" "$R" "$L" "$SP" --dry-run
ctl R4 0 'DISJOINT OUT-OF-KIT #9[0-9]+ dependabot' -- env G43_WIDEN_RX="^dependabot/" "$R" "$L" "$SP" --dry-run
sed "s/|$H1345|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh"; ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7 9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1341|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G43_ROUTING="$W/routing_ok.conf" G43_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step-0 outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins are untouched by every control above"
ctl PNZ 0 '' -- test "$(shasum -a 256 "$GS/pins_gate43.json" | cut -c1-64)" = "$PINSHA"
echo "SUMMARY gate43: $TOT controls, OK $OK, MISMATCH $MM$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
