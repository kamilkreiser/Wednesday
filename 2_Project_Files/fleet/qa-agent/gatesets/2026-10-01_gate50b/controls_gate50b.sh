#!/bin/bash
# controls_gate50b.sh — every guard in the gate50b kit driven on the REAL subject (#1364) and on PLANTED defects, each with the rc it must give and
# a WHY pattern its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a control that makes
# it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g50b_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate50b.json, kit.json and the filled prompt are sha256-checked unchanged at the end (PNZ, KJZ, PRZ). The launcher runs with --check
# (headless) except L9, the real launch path with stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run
# that must refuse at step 0, routing) and R8 (a real run with a routed temp file that must stop at G50B_STOP_AFTER_3B) — both stop long before the
# usage gate / cockpit. Mode plants RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>): core.filemode is false.
# Each by-name keyword has its own launcher refusal (LK*): the keyword is broken into `<KW>-X`, which the launcher's TOKEN match must NOT accept.
# A NEW COPY of gate50a's controls (shape, harness, ssh-retry), re-planted for this kit's baseline PR, proportionately smaller; gate50a's file is not edited.
# Usage: controls_gate50b.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g50b_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g50b_sp/clone"; L="$GS/launch_qa_secuura_batch1364.sh"; PROMPT="$GS/2026-10-01_secuura-batch1364.prompt.txt"; CAP="$GS/READY_1364_mail.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate50b.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"; H="$(PJ pr_pins.head)"
SHA() { shasum -a 256 "$1" | cut -c1-64; }
PINSHA="$(SHA "$GS/pins_gate50b.json")"; KITSHA="$(SHA "$GS/kit.json")"; PRSHA="$(SHA "$PROMPT")"
BASE='Blockchain/Dev/scripts/audit/audit-baseline.json'; CON='Blockchain/Dev/scripts/audit/baseline-contract.mjs'; TST='Blockchain/Dev/scripts/audit/baseline-contract.test.mjs'
RF='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-30_seatB-49th/cleanup/r53p-reason-corrected.txt'
H60="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["census"]["1360"]["head"])' "$GS/gh_read_1.json")"
TOT=0; OK=0; MM=0; RETRIES=0
ctl() { # ctl <id> <expected rc> <why regex or ''> -- <command...>
  local id="$1" exp="$2" why="$3"; shift 4
  local out rc good try=0; out="$("$@" 2>&1)"; rc=$?
  # GitHub intermittently DENIES the Secuura deploy key's SSH auth under a burst of ls-remote / fetch (gate47, measured). The GUARDS fail closed
  # on it, which is right; the HARNESS retries such a run up to 3 times, 20 s apart, and counts every retry.
  while [ "$try" -lt 3 ] && printf '%s' "$out" | grep -qE 'Permission denied \(publickey\)|Could not read from remote repository'; do
    try=$((try + 1)); RETRIES=$((RETRIES + 1)); sleep 20; out="$("$@" 2>&1)"; rc=$?
  done
  printf '%s\n' "$out" > "$W/$id.out"
  good=0; [ "$rc" = "$exp" ] && { [ -z "$why" ] || printf '%s' "$out" | grep -qE -- "$why"; } && good=1
  [ "$INV" = 1 ] && good=$((1 - good))
  TOT=$((TOT + 1)); if [ "$good" = 1 ]; then OK=$((OK + 1)); v=OK; else MM=$((MM + 1)); v=MISMATCH; fi
  local shown=''; if [ -n "$why" ]; then shown="$(printf '%s' "$out" | grep -E -- "$why" | tail -1)"; fi
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|READ|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|BASELINE|SOURCES|MODE' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
IDN=0
commitw() { # commitw <tree> <parent> <msg>
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate50b.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate50b.invalid GIT_AUTHOR_DATE=2026-10-01T00:00:00Z GIT_COMMITTER_DATE=2026-10-01T00:00:00Z \
    git -C "$CL" commit-tree "$1" -p "$2" -m "$3"
}
mkdev() { # mkdev <path> <transform> — a develop MOVE plant: a child of develop (for --develop simulations)
  local p="$1" tf="$2" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.dev.$IDN"
  git -C "$CL" show "$DEV:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || return 1
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$DEV"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$DEV" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$DEV" "gate50b control plant: develop move on $p"
}
restack() { # restack <subject head> <path> <transform> — the subject's own tree with ONE more path edited, parent = the subject's parent
  local h="$1" p="$2" tf="$3" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.rs.$IDN"
  git -C "$CL" show "$h:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || { echo "PLANT TRANSFORM FAILED for $p" >&2; return 1; }
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$h" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate50b control plant: $p over $h"
}
remode() { # remode <subject head> <path> <mode> — the subject's own tree with ONE path's RECORDED mode changed
  local h="$1" p="$2" mo="$3" idx tree; IDN=$((IDN + 1)); idx="$W/idx.rm.$IDN"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"; GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mo,$(git -C "$CL" rev-parse "$h:$p"),$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate50b control plant: $p recorded $mo"
}
mut() { # mut <src> <dst> <old> <new> — a literal replacement (python, no shell quoting), refusing when <old> is absent
  python3 -c 'import sys; s=open(sys.argv[1]).read(); assert sys.argv[3] in s, "mut: anchor absent: " + sys.argv[3]; open(sys.argv[2], "w").write(s.replace(sys.argv[3], sys.argv[4]))' "$@"
}
echo "=== controls_gate50b $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1364 $H | END_TREE $END | plants $W"

echo "--- pin_gate50b.py (head, shape, audit-only, the move, alone, the squash, RECORDED modes + control, the hook files, the unchanged pins) — simulations write pins_gate50b.SIM-<name>.json only"
PN="$GS/pin_gate50b.py"
ctl PN0  0 'PASS: FAIL=0 -> pins_gate50b.SIM-real.json .* 2 paths \+2/-9' -- python3 "$PN" "$SP" --simulate real "1364=$H"
ctl PN0e 0 "END_TREE $END \| git diff --shortstat develop END: 2 files changed, 2 insertions\(\+\), 9 deletions\(-\)" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 3 path\(s\) pinned \(2 PR, 1 control\), 3 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0k 0 'baseline-contract.test.mjs: develop 2379c0aeee6e .*BYTE-EQUAL in every tree' -- cat "$W/PN0.out"
ctl PN1  1 'REFUSING: --develop is a controls-only override' -- python3 "$PN" "$SP" --develop "$OLDDEV"
PFL="$(restack "$H" "$TST" "a = 'length > 20,'; assert s.count(a) == 1; s = s.replace(a, 'length > 19,')")"
ctl PN2  1 '\(K\) Blockchain/Dev/scripts/audit/baseline-contract.test.mjs is not byte-equal' -- python3 "$PN" "$SP" --simulate floor "1364=$PFL"
DCF="$(mkdev "$BASE" "s = s + '\n'")"
ctl PN3  1 '\(C\) #1364: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate cfl "1364=$H" --develop "$DCF"
M755="$(remode "$H" "$BASE" 100755)"
ctl PN4  1 'Blockchain/Dev/scripts/audit/audit-baseline.json: want 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1364=$M755"
DMV="$(mkdev "Blockchain/Dev/BACKLOG.md" "s = s + '\n<!-- gate50b control plant: an unrelated develop move -->\n'")"
ctl PN5  0 '#1364 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 1 path\(s\) \| reaches its own paths: NONE' -- python3 "$PN" "$SP" --simulate mv "1364=$H" --develop "$DMV"
P3F="$(restack "$H" "Blockchain/Dev/BACKLOG.md" "s = s + ' '")"
ctl PN6  1 "\(B\) paths outside scripts/audit/ \['Blockchain/Dev/BACKLOG.md'\]" -- python3 "$PN" "$SP" --simulate third "1364=$P3F"

echo "--- baseline_gate50b.py (requirement 1 + 3 prediction; controls inside)"
BL="$GS/baseline_gate50b.py"
ctl BL0  0 'BASELINE PASS: 0 FAIL of 14 checks .* rows 26 -> 25 \| removed \[.GHSA-mwp4-54f8-5fhr.\] \| fuse 4 -> 3' -- python3 "$BL" "$SP"
ctl BL0c 0 'PASS B5: .*CHARACTER-EXACT: True .*CONTROL base reason == file: False' -- cat "$W/BL0.out"
ctl BL0f 0 'PASS B10: FILE baseline-contract.test.mjs .*CONTROL the same probe on baseline-contract.mjs \(the WRONG file\) reads False' -- cat "$W/BL0.out"
ctl BL0u 0 'PASS B11: FUSE at END [0-9a-f]{12}: 3 row\(s\) .*control at develop: 4' -- cat "$W/BL0.out"
B1P="$(restack "$H" "$BASE" "a = '\"reason\": \"Permanent acceptance (Kam ruling 2026-08-05, recorded on KS-559)'; assert s.count(a) >= 1, s.count(a); s = s.replace(a, '\"reason\": \"Permanent acceptance (Kam ruling 2026-08-05, recorded on KS-559) g50b', 1)")"
ctl BL1  1 "FAIL B3: surviving rows that differ \['GHSA-8xcm-r25x-g524', 'GHSA-r53p-7pc4-xj5r'\]" -- python3 "$BL" "$SP" --head "$B1P"
B2P="$(restack "$H" "$BASE" "import re; m = re.search(r'\"GHSA-frvp-7c67-39w9\": \{.*?\"expires\": \"2026-10-09\"', s, re.S); assert m; s = s[:m.end()-11] + '2026-10-10\"' + s[m.end():]")"
ctl BL2  1 "FAIL B7: rows whose expires changed \['GHSA-frvp-7c67-39w9'\]" -- python3 "$BL" "$SP" --head "$B2P"
ctl BL2b 0 'FAIL B6: 2026-10-09 cohort base 4 .* -> head 2' -- cat "$W/BL2.out"
B3P="$(restack "$H" "$CON" "a = \"  'GHSA-w5hq-g745-h8pq', // uuid          KS-470\n\"; assert s.count(a) == 1; s = s.replace(a, '')")"
ctl BL3  1 'FAIL B8: GRANDFATHERED_NO_EXPIRY block byte-equal: False \| ids 17' -- python3 "$BL" "$SP" --head "$B3P"
ctl BL3b 0 'FAIL B9: baseline-contract.mjs differing line' -- cat "$W/BL3.out"
B4P="$(restack "$H" "$BASE" "a = 'At acceptance the pin was undici 5.29.0'; assert s.count(a) == 1; s = s.replace(a, 'At acceptance the pin was undici 5.29.1')")"
ctl BL4  1 'FAIL B5: head reason == r53p-reason-corrected.txt CHARACTER-EXACT: False' -- python3 "$BL" "$SP" --head "$B4P"
{ cat "$RF"; printf '\n'; } > "$W/reason_nl.txt"
ctl BL5  1 'FAIL B5: .*CHARACTER-EXACT: False \| file 1949 B .*ends in newline: True' -- python3 "$BL" "$SP" --reason-file "$W/reason_nl.txt"
ctl BL6  1 'FAIL B0: changed paths 0 ' -- python3 "$BL" "$SP" --head "$DEV"
ctl BL6b 0 'FAIL B1: rows base 26 \(want 26\) head 26 \(want 25\)' -- cat "$W/BL6.out"

echo "--- sources_gate50b.py (ITEM 4 / ITEM 5 source reads; controls inside)"
SO="$GS/sources_gate50b.py"
ctl SO0  0 'SOURCES READ: 0 FAIL of 12 reads' -- python3 "$SO" "$SP"
ctl SO0n 0 'READ N2 nginx-production.conf: server_tokens off \(control\) 1 \| proxy_hide_header Server 0' -- cat "$W/SO0.out"
ctl SO0d 0 'READ N2 nginx-demo.conf: server_tokens off \(control\) 1 \| proxy_hide_header Server 0' -- cat "$W/SO0.out"
ctl SO0g 0 'READ N2 nginx.conf: server_tokens off \(control\) 1 \| proxy_hide_header Server 1' -- cat "$W/SO0.out"
ctl SO0v 0 "READ I5b: KS-1397 draft internal-vocabulary hits \{'Wednesday': 1, 'gate': 1, 'DRAFT': 1\}" -- cat "$W/SO0.out"
ctl SO0t 0 'READ I4: probe_rls.out \(before\): charge_events rls=false force=false policies=0 rows=8 .*rows 8 rls false force false policies 0' -- cat "$W/SO0.out"
cp "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-01_seatB-51st/item4/TICKET-TITLE.txt" "$W/title.txt"; printf 'x' >> "$W/title.txt"
ctl SO1  1 'FAIL I0: title 122 B' -- python3 "$SO" "$SP" --title-file "$W/title.txt"
tail -n +2 "$GS/KS-1397_acceptance_DRAFT.md" > "$W/draft_noheader.md"
ctl SO2  0 'READ I5b: KS-1397 draft internal-vocabulary hits NONE' -- python3 "$SO" "$SP" --draft "$W/draft_noheader.md"
ctl SO3  1 "FAIL N1: nginx.conf :24 .* \| :142 " -- python3 "$SO" "$SP" --tree "$(restack "$DEV" 'Blockchain/Dev/docker/nginx-gateway/nginx.conf' "a = '    proxy_hide_header Server;'; assert s.count(a) == 1; s = s.replace(a, '    # removed by a g50b plant')")"

echo "--- keyscan_gate50b.py (subject, body, live surfaces)"
KS="$GS/keyscan_gate50b.py"; S6="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1364"]["title"])' "$GS/gh_read_1.json")"
ctl KS0  0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1  1 'FAIL #1364 S2' -- python3 "$KS" "$SP" --subject "$S6 (#1364)"
ctl KS2  1 'FAIL #1364 S1' -- python3 "$KS" "$SP" --subject "KS-729: remove the dead mwp4 row (KS-530)"
ctl KS3  1 'FAIL #1364 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --subject "${S6}0123456"
printf '' > "$W/b_empty.txt";                                    ctl KS4 1 'FAIL #1364 B1 KS-729' -- python3 "$KS" "$SP" --body-file "$W/b_empty.txt"
printf 'Refs KS-729\nCloses KS-729\n' > "$W/b_close.txt";        ctl KS5 1 'FAIL #1364 B2' -- python3 "$KS" "$SP" --body-file "$W/b_close.txt"
printf 'Refs KS-729\nsee KS-530\n' > "$W/b_for.txt";             ctl KS6 1 "FAIL #1364 B3: .*foreign \['KS-530'\]" -- python3 "$KS" "$SP" --body-file "$W/b_for.txt"
printf 'Refs KS-729\nthe fuse rows sit on KS-528 outside any fence\n' > "$W/pb.txt"; ctl KS7 0 "OUTSIDE any fence: \['KS-528'\]" -- python3 "$KS" "$SP" --prbody-file "$W/pb.txt"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L1  6 '#1364 — .* is not at .* AND refs/pull/1364/head' -- env G50B_HEAD_1364="$DEV" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G50B_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1364 — the compare is not the pinned' -- env G50B_PATHS_1364="$BASE" "$L" --check
mut "$PROMPT" "$W/p_go.txt" 'GO (Seat B 51st): merge 1364 on gate50b' 'GO (Seat B 51st): merge 1363 on gate50b';   ctl L4 26 'merge authority / the GO string' -- env G50B_PROMPT="$W/p_go.txt" "$L" --check
mut "$PROMPT" "$W/p_seat.txt" 'The merge seat is Seat B 51st' 'The merge seat is Seat B 49th';                   ctl L4b 26 'merge authority / the GO string' -- env G50B_PROMPT="$W/p_seat.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                        ctl L5 8 'unfilled double-brace' -- env G50B_PROMPT="$W/p_tok.txt" "$L" --check
{ cat "$PROMPT"; echo 'merge #<PR>'; } > "$W/p_ph.txt";                                                         ctl L5b 8 'unpinned PR placeholder' -- env G50B_PROMPT="$W/p_ph.txt" "$L" --check
i=0
for kw in DIFF-REDERIVED TWO-FILES-ONLY ROWS-26-25 REASON-CMP NOTHING-REDATED GRANDFATHERED-BYTE-EQUAL CONTRACT-ONE-LINE FLOOR-NOT-LOWERED MWP4-DEAD-BOTH-LEGS LEG7-PROBE LEGS-RC-HEAD GATE-STILL-REFUSES FUSE-COHORT ITEM4-TICKET-TEXT KS1397-COMMENT SUBJECT-KEY-SCAN SUBJECT-LANDS-AT SUBJECT-TRUE-OF-DIFF REFS-OWN-KEY NO-CLOSING-KEYWORD DEHYPHENATED-KEYS PR-BODY-CLAIMS CLEAN-MERGE END-TREE MODES COLLISION-CENSUS TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  i=$((i + 1)); sed "s/$kw/$kw-X/g" "$PROMPT" > "$W/p_kw$i.txt"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G50B_PROMPT="$W/p_kw$i.txt" "$L" --check
done
mut "$PROMPT" "$W/p_fn.txt" 'ASSERT THE FILENAME TOO' 'assert the content';                                         ctl L6 33 'the filename rule' -- env G50B_PROMPT="$W/p_fn.txt" "$L" --check
sed "s/$H/${H:0:39}x/g" "$CAP" > "$W/cap_noh.md";                                                               ctl L7 20 "do not both name #1364's head" -- env G50B_BRIEF="$W/cap_noh.md" "$L" --check
mut "$PROMPT" "$W/p_h1.txt" 'NO ticket filed' 'NO tickets filed';                                                    ctl L8 39 'the HOLDS' -- env G50B_PROMPT="$W/p_h1.txt" "$L" --check
mut "$PROMPT" "$W/p_h2.txt" 'You NEVER reply to Peter' 'You may reply to Peter';                                     ctl L8b 39 'the HOLDS' -- env G50B_PROMPT="$W/p_h2.txt" "$L" --check
mut "$PROMPT" "$W/p_h3.txt" 'Never read or write a real `.env`' 'Never write a real `.env`';                         ctl L8c 39 'the HOLDS' -- env G50B_PROMPT="$W/p_h3.txt" "$L" --check
mut "$PROMPT" "$W/p_h4.txt" 'no SSH to any host, no database read' 'no deploy of a database';                        ctl L8d 39 'the HOLDS' -- env G50B_PROMPT="$W/p_h4.txt" "$L" --check
mut "$PROMPT" "$W/p_h5.txt" 'No `az` command of any kind' 'No `az login`';                                          ctl L8e 39 'the HOLDS' -- env G50B_PROMPT="$W/p_h5.txt" "$L" --check
mut "$PROMPT" "$W/p_h7.txt" 'THE NAMED EXCEPTIONS to those holds — these and NO others' 'THE NAMED EXCEPTIONS to those holds'; ctl L8g 39 'the HOLDS' -- env G50B_PROMPT="$W/p_h7.txt" "$L" --check
mut "$PROMPT" "$W/p_h8.txt" 'No audit-baseline row edited in any tracked tree you keep' 'Audit-baseline rows may be edited'; ctl L8h 39 'the HOLDS' -- env G50B_PROMPT="$W/p_h8.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                            ctl L10 31 'launch develop / the END_TREE' -- env G50B_PROMPT="$W/p_dev.txt" "$L" --check
mut "$PROMPT" "$W/p_tier.txt" '#1364 T2 —' '#1364 T1 —';                                                              ctl L11 7 'the tier line' -- env G50B_PROMPT="$W/p_tier.txt" "$L" --check
mut "$PROMPT" "$W/p_round.txt" 'a round-1 NO GO goes back to the author for round 2' 'a round-1 NO GO ships nothing';  ctl L11b 7 'the tiering rule' -- env G50B_PROMPT="$W/p_round.txt" "$L" --check
mut "$PROMPT" "$W/p_tkt.txt" 'PR #1364 is KS-729' 'PR #1364 is KS-730';                                               ctl L12 32 "BOTH state the ticket" -- env G50B_PROMPT="$W/p_tkt.txt" "$L" --check
mut "$PROMPT" "$W/p_a1.txt" 'MG-1 2 over 2 paths' 'MG-1 over the paths';                                              ctl L13 25 'the MERGE ADDENDUM rules' -- env G50B_PROMPT="$W/p_a1.txt" "$L" --check
mut "$PROMPT" "$W/p_a2.txt" 'NOTHING to report.md after you send the verdict mail' 'little to report.md after you send the verdict mail'; ctl L13b 25 'REPORT-HASH-LAST' -- env G50B_PROMPT="$W/p_a2.txt" "$L" --check
mut "$PROMPT" "$W/p_a3.txt" 'ROWS 26 -> 25, removed {GHSA-mwp4-54f8-5fhr}' 'ROWS changed';                             ctl L13c 25 'the MERGE ADDENDUM rules' -- env G50B_PROMPT="$W/p_a3.txt" "$L" --check
mut "$PROMPT" "$W/p_a4.txt" 'KS-1397 <POST AS-IS' 'KS-1397 <ruled';                                                   ctl L13d 25 'the MERGE ADDENDUM rules' -- env G50B_PROMPT="$W/p_a4.txt" "$L" --check
mut "$PROMPT" "$W/p_subj.txt" 'GATE50B #1364' 'GATE50B #1363';                                                        ctl L14 23 'the verdict subject' -- env G50B_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                         ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
mut "$PROMPT" "$W/p_k1.txt" "$GS/baseline_1.out" "$GS/baseline_elsewhere.out";                                         ctl L16 8 'baseline_1.out is missing, empty, or not named' -- env G50B_PROMPT="$W/p_k1.txt" "$L" --check
mut "$PROMPT" "$W/p_k2.txt" "$GS/KS-1397_acceptance_DRAFT.md" "$GS/KS-1397_elsewhere.md";                              ctl L17 8 'KS-1397_acceptance_DRAFT.md is missing, empty, or not named' -- env G50B_PROMPT="$W/p_k2.txt" "$L" --check
mut "$PROMPT" "$W/p_k3.txt" '2026-10-01-batch1363-g50a/report.md' '2026-09-30-batch1356-g49a/report.md';              ctl L18 8 'the previous round report' -- env G50B_PROMPT="$W/p_k3.txt" "$L" --check
mut "$PROMPT" "$W/p_k4.txt" "$GS/ITEM4_ticket_text_mail.md" "$GS/ITEM4_elsewhere.md";                                  ctl L19 8 'ITEM4_ticket_text_mail.md is missing, empty, or not named' -- env G50B_PROMPT="$W/p_k4.txt" "$L" --check
mut "$PROMPT" "$W/p_x1.txt" 'NO DATABASE IS READ IN THIS GATE' 'A DATABASE MAY BE READ';                             ctl L20 34 'the NO-RUNTIME \+ NO-DATABASE rules' -- env G50B_PROMPT="$W/p_x1.txt" "$L" --check
mut "$PROMPT" "$W/p_x2.txt" 'never its CLEANUP block' 'or its CLEANUP block';                                          ctl L21 36 'the authority line' -- env G50B_PROMPT="$W/p_x2.txt" "$L" --check
mut "$PROMPT" "$W/p_x3.txt" 'NOTHING IS POSTED BY YOU' 'Post it if GO';                                               ctl L22 37 'the two TEXT rulings' -- env G50B_PROMPT="$W/p_x3.txt" "$L" --check
mut "$PROMPT" "$W/p_x3b.txt" 'NO `proxy_hide_header Server`' 'the same headers';                                      ctl L22b 37 'the two TEXT rulings' -- env G50B_PROMPT="$W/p_x3b.txt" "$L" --check
mut "$PROMPT" "$W/p_x4.txt" 'is at 82%' 'is fine';                                                                    ctl L23 38 'the proportionality line' -- env G50B_PROMPT="$W/p_x4.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate50b.sh"
ctl R0  0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key outside reported_overlaps \| 0 expected overlap\(s\) reported \| 0 sequenced by Wednesday .*2 client-human PR\(s\) reported \| 2 kit path\(s\), 1 kit key\(s\)' -- cat "$W/R0.out"
ctl R0h 0 'CLIENT-HUMAN \(reported, never sequenced by a gate\) #1360 by PeterObeden' -- cat "$W/R0.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pin, 1 of 1' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                                ctl R1 1 'is not registered in inbox_routing.conf' -- env G50B_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2  15 "OVERLAP #1360 .*paths \[.*'Blockchain/Dev/package-lock.json'" -- env G50B_OVERLAP_EXTRA="Blockchain/Dev/package-lock.json" "$R" "$L" "$SP" --dry-run
ctl R3  15 "OVERLAP #1360 .*title keys \['KS-1380'\]" -- env G50B_TITLE_KEY="KS-1380" "$R" "$L" "$SP" --dry-run
printf '{"1360": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H60" > "$W/seq_ok.json"
printf '{"1360": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$H" > "$W/seq_bad.json"
ctl R3s 0 'SEQUENCED OUT-OF-KIT #1360 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- env G50B_TITLE_KEY="KS-1380" G50B_SEQUENCED="$W/seq_ok.json" "$R" "$L" "$SP" --dry-run
ctl R3w 15 'OVERLAP #1360 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G50B_TITLE_KEY="KS-1380" G50B_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #1360 ' -- env G50B_WIDEN_RX="ks-1380-revert-pr-1358$" "$R" "$L" "$SP" --dry-run
sed "s/|$H|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh";                      ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1364|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G50B_ROUTING="$W/routing_ok.conf" G50B_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins, kit.json and the filled prompt are untouched by every control above"
ctl PNZ 0 '' -- test "$(SHA "$GS/pins_gate50b.json")" = "$PINSHA"
ctl KJZ 0 '' -- test "$(SHA "$GS/kit.json")" = "$KITSHA"
ctl PRZ 0 '' -- test "$(SHA "$PROMPT")" = "$PRSHA"
echo "SUMMARY gate50b: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
