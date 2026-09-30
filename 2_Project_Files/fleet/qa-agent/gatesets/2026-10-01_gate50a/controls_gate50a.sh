#!/bin/bash
# controls_gate50a.sh — every guard in the gate50a kit driven on the REAL subject (#1363, ITEM A) and on PLANTED defects, each with the rc it must
# give and a WHY pattern its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a control
# that makes it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g50a_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate50a.json, kit.json and the filled prompt are sha256-checked unchanged at the end (PNZ, KJZ, PRZ). The launcher runs with --check
# (headless) except L9, the real launch path with stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run
# that must refuse at step 0, routing) and R8 (a real run with a routed temp file that must stop at G50A_STOP_AFTER_3B) — both stop long before the
# usage gate / cockpit. Mode plants RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>): core.filemode is false.
# Each by-name keyword has its own launcher refusal (LK*): the keyword is broken into `<KW>-X`, which the launcher's TOKEN match must NOT accept.
# GL0/GL1 run the seat's gatelines46.py (READ-ONLY, python3 on SCRATCH logs only) to prove the drafter's reading of its VERDICT states.
# A NEW COPY of gate49a's controls (shape, harness, ssh-retry), re-keyed and re-planted for this kit's 4 locks; gate49a's file is not edited.
# Usage: controls_gate50a.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g50a_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g50a_sp/clone"; L="$GS/launch_qa_secuura_batch1363.sh"; PROMPT="$GS/2026-10-01_secuura-batch1363.prompt.txt"; CAP="$GS/mail_gate50a_ready.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate50a.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"; H="$(PJ pr_pins.head)"
SHA() { shasum -a 256 "$1" | cut -c1-64; }
PINSHA="$(SHA "$GS/pins_gate50a.json")"; KITSHA="$(SHA "$GS/kit.json")"; PRSHA="$(SHA "$PROMPT")"
KYC='Blockchain/Dev/services/kyc/package-lock.json'; ROOTL='Blockchain/Dev/package-lock.json'; ADM='Blockchain/Dev/frontend/admin/package-lock.json'
VER='Blockchain/Dev/frontend/verifier/package-lock.json'; DFK='Blockchain/Dev/services/kyc/Dockerfile'; KYCM='Blockchain/Dev/services/kyc/package.json'
MOB='Blockchain/Dev/mobile/secuura-app/package-lock.json'
GL='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-01_seatB-51st/raise/gatelines46.py'
H53="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["census"]["1253"]["head"])' "$GS/gh_read_1.json")"
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
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|LOCKDELTA|REACH|OVERLAPS|MODE|VERDICT' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
IDN=0
commitw() { # commitw <tree> <parent> <msg>
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate50a.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate50a.invalid GIT_AUTHOR_DATE=2026-10-01T00:00:00Z GIT_COMMITTER_DATE=2026-10-01T00:00:00Z \
    git -C "$CL" commit-tree "$1" -p "$2" -m "$3"
}
mkdev() { # mkdev <path> <transform> — a develop MOVE plant: a child of develop (for --develop simulations)
  local p="$1" tf="$2" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.dev.$IDN"
  git -C "$CL" show "$DEV:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || return 1
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$DEV"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$DEV" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$DEV" "gate50a control plant: develop move on $p"
}
restack() { # restack <subject head> <path> <transform> — the subject's own tree with ONE more path edited, parent = the subject's parent
  local h="$1" p="$2" tf="$3" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.rs.$IDN"
  git -C "$CL" show "$h:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || { echo "PLANT TRANSFORM FAILED for $p" >&2; return 1; }
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$h" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate50a control plant: $p over $h"
}
remode() { # remode <subject head> <path> <mode> — the subject's own tree with ONE path's RECORDED mode changed
  local h="$1" p="$2" mo="$3" idx tree; IDN=$((IDN + 1)); idx="$W/idx.rm.$IDN"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"; GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mo,$(git -C "$CL" rev-parse "$h:$p"),$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate50a control plant: $p recorded $mo"
}
mut() { # mut <src> <dst> <old> <new> — a literal replacement (python, no shell quoting), refusing when <old> is absent
  python3 -c 'import sys; s=open(sys.argv[1]).read(); assert sys.argv[3] in s, "mut: anchor absent: " + sys.argv[3]; open(sys.argv[2], "w").write(s.replace(sys.argv[3], sys.argv[4]))' "$@"
}
echo "=== controls_gate50a $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1363 $H | END_TREE $END | plants $W"

echo "--- pin_gate50a.py (head, shape, locks only, the move, alone, the squash, RECORDED modes + control, the hook files, the unchanged pins) — simulations write pins_gate50a.SIM-<name>.json only"
PN="$GS/pin_gate50a.py"
ctl PN0  0 'PASS: FAIL=0 -> pins_gate50a.SIM-real.json .* 4 paths \+19/-19' -- python3 "$PN" "$SP" --simulate real "1363=$H"
ctl PN0e 0 "END_TREE $END \| git diff --shortstat develop END: 4 files changed, 19 insertions\(\+\), 19 deletions\(-\)" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 5 path\(s\) pinned \(4 PR, 1 control\), 5 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0k 0 'mobile/secuura-app/package-lock.json: develop 2f5f8c1f4edf .*BYTE-EQUAL in every tree' -- cat "$W/PN0.out"
ctl PN0s 0 'frontend/issuer/src/utils/sanitize.ts: develop dd80cb817e26 .*BYTE-EQUAL in every tree' -- cat "$W/PN0.out"
ctl PN1  1 'REFUSING: --develop is a controls-only override' -- python3 "$PN" "$SP" --develop "$OLDDEV"
PDF="$(restack "$H" "$DFK" "s = s + '# gate50a control plant: the Dockerfile edited\n'")"
ctl PN2  1 '\(K\) Blockchain/Dev/services/kyc/Dockerfile is not byte-equal' -- python3 "$PN" "$SP" --simulate df "1363=$PDF"
DCF="$(mkdev "$KYC" "s = s + '\n'")"
ctl PN3  1 '\(C\) #1363: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate cfl "1363=$H" --develop "$DCF"
M755="$(remode "$H" "$KYC" 100755)"
ctl PN4  1 'Blockchain/Dev/services/kyc/package-lock.json: want 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1363=$M755"
DMV="$(mkdev "Blockchain/Dev/BACKLOG.md" "s = s + '\n<!-- gate50a control plant: an unrelated develop move -->\n'")"
ctl PN5  0 '#1363 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 1 path\(s\) \| reaches its own paths: NONE' -- python3 "$PN" "$SP" --simulate mv "1363=$H" --develop "$DMV"
PMF="$(restack "$H" "$KYCM" "s = s + ' '")"
ctl PN6  1 "\(B\) non-lock paths .*package.json paths \['Blockchain/Dev/services/kyc/package.json'\]" -- python3 "$PN" "$SP" --simulate pj "1363=$PMF"
PMO="$(restack "$H" "$MOB" "s = s + '\n'")"
ctl PN7  1 '\(K\) Blockchain/Dev/mobile/secuura-app/package-lock.json is not byte-equal' -- python3 "$PN" "$SP" --simulate mob "1363=$PMO"

echo "--- lockdelta_gate50a.py (LOCK-DELTA-4 / OWN-DEPENDENCIES / DEPENDENT-RANGES / REGISTRY-TRUE / ADVISORY-RANGES / RESIDUE prediction)"
LDP="$GS/lockdelta_gate50a.py"
OTHER="import re; m = [x for x in re.finditer(r'\"(node_modules/[^\"]+)\": \{\n\s+\"version\": \"([^\"]+)\"', s) if x.group(1) not in ('node_modules/axios', 'node_modules/dompurify')][0]; s = s[:m.start(2)] + m.group(2) + '-g50a' + s[m.end(2):]"
AXK='"node_modules/axios": {\n      "version": "1.20.0"'
ctl LD0  0 'LOCKDELTA PASS: 0 FAIL of 50 checks .* 4 locks, 5 moves \(5 PROD\), 9 dependant range\(s\) \| numstat \+19/-19' -- python3 "$LDP" "$SP"
ctl LD0x 0 "L2x Blockchain/Dev/services/kyc node_modules/axios: .*form-data '\^4\.0\.5' -> '\^4\.0\.6'.* -> ALLOWED" -- cat "$W/LD0.out"
ctl LD0d 0 'PASS L4dc: CONTROL: <major\+1>\.0\.0 of each of 17 resolved own dependenc' -- cat "$W/LD0.out"
ctl LD0g 0 'PASS L5d axios@1\.20\.0: .*: True' -- cat "$W/LD0.out"
ctl LD0r 0 'PASS L5c dompurify@3\.4\.16: CONTROLS: .*reads False; .*reads False' -- cat "$W/LD0.out"
ctl LD0a 0 "PASS L6 GHSA-p98j-92pf-mc4p: dompurify .*to-versions \['3\.4\.16'\] OUTSIDE every range: True \| from-versions inside \(control\): \['3\.4\.13'\]" -- cat "$W/LD0.out"
ctl LD0w 0 'PASS L6 GHSA-542g-h47m-68v8: axios high published 2026-09-30T15:01:07Z' -- cat "$W/LD0.out"
ctl LD0s 0 "L7 RESIDUE: 1 entr\(y/ies\) in 1 lock\(s\) of 45 at the head: \['Blockchain/Dev/mobile/secuura-app/package-lock.json'\]" -- cat "$W/LD0.out"
ctl LD0n 0 'numstat sum \+19/-19 \| the seat claimed \+19/-19: CLAIM MATCH' -- cat "$W/LD0.out"
P1="$(restack "$H" "$KYC" "$OTHER")";                                                                          ctl LD1 1 'FAIL L2 Blockchain/Dev/services/kyc node_modules/' -- python3 "$LDP" "$SP" --head "$P1" --offline
ctl LD1m 0 'FAIL L3: moves measured 6 \(claimed 5\)' -- cat "$W/LD1.out"
ctl LD1o 0 'NOT MEASURED L5 / L6 / L7: --offline' -- cat "$W/LD1.out"
P2="$(restack "$H" "$ROOTL" "a = 'sha512-sqo+pNp3qRhCIpbgR'; assert s.count(a) == 1; s = s.replace(a, 'sha512-sqo+pNp3qRhCIpbgS')")"; ctl LD2 1 'FAIL L5 dompurify@3\.4\.16' -- python3 "$LDP" "$SP" --head "$P2"
P3="$(restack "$H" "$ADM" "a = '\"form-data\": \"^4.0.6\"'; assert s.count(a) == 1; s = s.replace(a, '\"form-data\": \"^4.0.7\"')")"; ctl LD3 1 "L2x Blockchain/Dev/frontend/admin node_modules/axios: .*'\^4\.0\.7'.* -> NOT ALLOWED" -- python3 "$LDP" "$SP" --head "$P3" --offline
ctl LD3d 0 'FAIL L4d Blockchain/Dev/frontend/admin node_modules/axios' -- cat "$W/LD3.out"
P4="$(restack "$H" "$ROOTL" "a = '$AXK,'; assert s.count(a) == 1, s.count(a); s = s.replace(a, a + '\n      \"dev\": true,')")"; ctl LD4 1 "FAIL L2 Blockchain/Dev node_modules/axios: 1\.18\.1 -> 1\.20\.0 \| flags PROD -> dev" -- python3 "$LDP" "$SP" --head "$P4" --offline
P5="$(restack "$H" "$VER" "a = '\"version\": \"1.20.0\"'; assert s.count(a) == 1; s = s.replace(a, '\"version\": \"2.0.0\"')")";    ctl LD5 1 'FAIL L4 Blockchain/Dev/frontend/verifier node_modules/axios: 1\.18\.1 -> 2\.0\.0 .*head False' -- python3 "$LDP" "$SP" --head "$P5" --offline
REV="s = s.replace('\"version\": \"1.20.0\"', '\"version\": \"1.18.1\"').replace('axios-1.20.0.tgz', 'axios-1.18.1.tgz').replace('sha512-r8aOh8j9cGKpgQAqpzrUHnSIc6a59Y3Xf/cv8sy1DrHCkZHzQGEuoq1tARk6qSyDdtQGSDgpb9kFlruzPvrgwg==', 'sha512-3nTvFlvpn9Zu/RkHUqtc7/+al4UpRW5az71ap5zccp6e8RAYEzhMTecX8Dz1wWDYrPpUoB1HAQEGEAEvUr7S9g==').replace('\"form-data\": \"^4.0.6\"', '\"form-data\": \"^4.0.5\"')"
P6="$(restack "$H" "$ADM" "$REV")";                                                                              ctl LD6 1 "FAIL L0: changed paths 3 .*missing \['Blockchain/Dev/frontend/admin/package-lock.json'\]" -- python3 "$LDP" "$SP" --head "$P6" --offline
ctl LD7  1 'FAIL L0: changed paths 0 ' -- python3 "$LDP" "$SP" --head "$DEV" --offline
ctl LD8  0 'PASS L4s: the semver evaluator holds on 18 fixed cases' -- cat "$W/LD7.out"

echo "--- reach_gate50a.py (RUNTIME-REACH / ROOT-LOCK-CONSUMERS read; controls inside)"
RCP="$GS/reach_gate50a.py"
ctl RE0  0 'REACH READ: tree 9e84e1fabafe \| 3 image Dockerfile\(s\) copy a moved lock \| root-lock copies 0 .*controls hold' -- python3 "$RCP" "$SP"
ctl RE0c 0 "R1 CONTROL: the matcher finds services/kyc/Dockerfile's own .*COPY: True" -- cat "$W/RE0.out"
ctl RE0p 0 "Blockchain/Dev/services/kyc/Dockerfile +Blockchain/Dev/services/kyc/package-lock.json +PROD \['axios 1\.18\.1->1\.20\.0'\] \| dev none" -- cat "$W/RE0.out"
ctl RE1  0 'REACH READ: tree 4f18c59a89db \| 0 image Dockerfile\(s\) copy a moved lock' -- python3 "$RCP" "$SP" --tree "$DEV"

echo "--- overlaps_gate50a.py (carries its own two-way control)"
ctl OV0  0 'OVERLAPS READ: 11 PR\(s\) \| conflict today 1 \| conflict after ITEM A 1 .*touching the moved packages 0' -- env G50A_OVJSON="$W/overlaps.json" python3 "$GS/overlaps_gate50a.py" "$SP"
ctl OV0c 0 'CT-CLEAN an unrelated plant over the squash: clean \| CT-CONFLICT .*CONFLICT .*-> OK' -- cat "$W/OV0.out"
ctl OV0p 0 '#1360 +PeterObeden .*after ITEM A clean .*touches the moved packages: no' -- cat "$W/OV0.out"

echo "--- keyscan_gate50a.py (subject, body, live surfaces)"
KS="$GS/keyscan_gate50a.py"; S6="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1363"]["title"])' "$GS/gh_read_1.json")"
ctl KS0  0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1  1 'FAIL #1363 S2' -- python3 "$KS" "$SP" --subject "$S6 (#1363)"
ctl KS2  1 'FAIL #1363 S1' -- python3 "$KS" "$SP" --subject "KS-1378: in-range lock refresh (KS-1395)"
ctl KS3  1 'FAIL #1363 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --subject "${S6}0123456789"
printf '' > "$W/b_empty.txt";                                    ctl KS4 1 'FAIL #1363 B1 KS-1378' -- python3 "$KS" "$SP" --body-file "$W/b_empty.txt"
printf 'Refs KS-1378\nCloses KS-1378\n' > "$W/b_close.txt";      ctl KS5 1 'FAIL #1363 B2' -- python3 "$KS" "$SP" --body-file "$W/b_close.txt"
printf 'Refs KS-1378\nsee KS-1395\n' > "$W/b_for.txt";           ctl KS6 1 "FAIL #1363 B3: .*foreign \['KS-1395'\]" -- python3 "$KS" "$SP" --body-file "$W/b_for.txt"
printf 'Refs KS-1378\nnone is one of the two KS-1395 names outside any fence\n' > "$W/pb.txt"; ctl KS7 0 "OUTSIDE any fence: \['KS-1395'\]" -- python3 "$KS" "$SP" --prbody-file "$W/pb.txt"
ctl KS8  0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL' -- python3 "$KS" "$SP" --subject "KS-1378: lodash 5 in every lock and a baseline row"

echo "--- gatelines46.py (the seat's, READ-ONLY: python3 on SCRATCH logs) — which VERDICT state is the clean one"
printf '=== scripts/__tests__/pre_push_hook_base.test.sh ===\n28 passed, 0 failed\n=== scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh ===\n6 passed, 0 failed\n=== scripts/__tests__/run_shell_suites.test.sh ===\n49 passed, 0 failed\nshell suites: 67 passed, 0 failed, 0 skipped (of 67)\n' > "$W/gl_clean.log"
sed 's/^28 passed, 0 failed$/28 passed, 1 failed/' "$W/gl_clean.log" > "$W/gl_bad.log"
ctl GLS  0 '' -- test "$(SHA "$GL")" = 74d3a65881b8001ffd6994bab2d901a34efb157b9282310a005ae5eb20f75416
ctl GL0  0 'VERDICT: MATCHES the declared fleet STOP condition' -- python3 "$GL" "$W/gl_clean.log"
ctl GL1  0 'VERDICT: MISMATCH — STOP' -- python3 "$GL" "$W/gl_bad.log"
ctl GL1b 0 'pre_push_hook_base.test.sh +\(28, 1\) +MISMATCH' -- cat "$W/GL1.out"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L1  6 '#1363 — .* is not at .* AND refs/pull/1363/head' -- env G50A_HEAD_1363="$DEV" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G50A_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1363 — the compare is not the pinned' -- env G50A_PATHS_1363="$KYC" "$L" --check
mut "$PROMPT" "$W/p_go.txt" 'GO (Seat B 51st): merge 1363 on gate50a' 'GO (Seat B 51st): merge 1364 on gate50a';   ctl L4 26 'merge authority / the GO string' -- env G50A_PROMPT="$W/p_go.txt" "$L" --check
mut "$PROMPT" "$W/p_seat.txt" 'The merge seat is Seat B 51st' 'The merge seat is Seat B 49th';                   ctl L4b 26 'merge authority / the GO string' -- env G50A_PROMPT="$W/p_seat.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                        ctl L5 8 'unfilled double-brace' -- env G50A_PROMPT="$W/p_tok.txt" "$L" --check
{ cat "$PROMPT"; echo 'merge #<PR>'; } > "$W/p_ph.txt";                                                         ctl L5b 8 'unpinned PR placeholder' -- env G50A_PROMPT="$W/p_ph.txt" "$L" --check
i=0
for kw in LOCK-DELTA-4 OWN-DEPENDENCIES DEPENDENT-RANGES REGISTRY-TRUE REPRODUCE-REFRESH PRISTINE-CONTROL AUDIT-LEGS-BASE-HEAD THIRTEEN-IDS-ABSENT GATE-STILL-REFUSES NO-BASELINE-ROW ADVISORY-MAP RUNTIME-REACH ROOT-LOCK-CONSUMERS SUITES NPM-CI-HEAD MOBILE-UNTOUCHED CLEAN-MERGE END-TREE MODES COLLISION-CENSUS SUBJECT-KEY-SCAN SUBJECT-LANDS-AT SUBJECT-TRUE-OF-DIFF REFS-OWN-KEY NO-CLOSING-KEYWORD PR-BODY-CLAIMS NEW-TICKET-TEXT GATELINES-VERDICT FUSE-COUNT TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  i=$((i + 1)); sed "s/$kw/$kw-X/g" "$PROMPT" > "$W/p_kw$i.txt"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G50A_PROMPT="$W/p_kw$i.txt" "$L" --check
done
sed "s/$H/${H:0:39}x/g" "$CAP" > "$W/cap_noh.md";                                                               ctl L7 20 "do not both name #1363's head" -- env G50A_BRIEF="$W/cap_noh.md" "$L" --check
mut "$PROMPT" "$W/p_h1.txt" 'NO ticket filed' 'NO tickets filed';                                                    ctl L8 39 'the HOLDS' -- env G50A_PROMPT="$W/p_h1.txt" "$L" --check
mut "$PROMPT" "$W/p_h2.txt" 'You NEVER reply to Peter' 'You may reply to Peter';                                     ctl L8b 39 'the HOLDS' -- env G50A_PROMPT="$W/p_h2.txt" "$L" --check
mut "$PROMPT" "$W/p_h3.txt" 'Never read or write a real `.env`' 'Never write a real `.env`';                         ctl L8c 39 'the HOLDS' -- env G50A_PROMPT="$W/p_h3.txt" "$L" --check
mut "$PROMPT" "$W/p_h4.txt" 'Docker runs are `--rm --network none` with the source mounted READ-ONLY' 'Docker runs are `--rm`'; ctl L8d 39 'the HOLDS' -- env G50A_PROMPT="$W/p_h4.txt" "$L" --check
mut "$PROMPT" "$W/p_h5.txt" 'No `az` command of any kind' 'No `az login`';                                          ctl L8e 39 'the HOLDS' -- env G50A_PROMPT="$W/p_h5.txt" "$L" --check
mut "$PROMPT" "$W/p_h6.txt" 'NO checklist tick' 'NO early checklist tick';                                           ctl L8f 39 'the HOLDS' -- env G50A_PROMPT="$W/p_h6.txt" "$L" --check
mut "$PROMPT" "$W/p_h7.txt" 'THE NAMED EXCEPTIONS to those holds — these and NO others' 'THE NAMED EXCEPTIONS to those holds'; ctl L8g 39 'the HOLDS' -- env G50A_PROMPT="$W/p_h7.txt" "$L" --check
mut "$PROMPT" "$W/p_h8.txt" 'NEVER `up`, `down`' '`up`, `down`';                                                     ctl L8h 39 'the HOLDS' -- env G50A_PROMPT="$W/p_h8.txt" "$L" --check
mut "$PROMPT" "$W/p_h9.txt" '"no lock regenerated" means no REAL lock' '"no lock regenerated" means little';        ctl L8i 39 'the HOLDS' -- env G50A_PROMPT="$W/p_h9.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                            ctl L10 31 'launch develop / the END_TREE' -- env G50A_PROMPT="$W/p_dev.txt" "$L" --check
mut "$PROMPT" "$W/p_tier.txt" '#1363 T1 —' '#1363 T2 —';                                                              ctl L11 7 'the tier line' -- env G50A_PROMPT="$W/p_tier.txt" "$L" --check
mut "$PROMPT" "$W/p_round.txt" 'a round-1 NO GO goes back to the author for round 2' 'a round-1 NO GO ships nothing';  ctl L11b 7 'the tiering rule' -- env G50A_PROMPT="$W/p_round.txt" "$L" --check
mut "$PROMPT" "$W/p_tkt.txt" 'PR #1363 is KS-1378' 'PR #1363 is KS-1379';                                             ctl L12 32 "state 'PR #1363 is KS-1378'" -- env G50A_PROMPT="$W/p_tkt.txt" "$L" --check
mut "$PROMPT" "$W/p_a1.txt" 'MG-1 4 over 4 paths' 'MG-1 over the paths';                                              ctl L13 25 'the MERGE ADDENDUM rules' -- env G50A_PROMPT="$W/p_a1.txt" "$L" --check
mut "$PROMPT" "$W/p_a2.txt" 'NOTHING to report.md after you send the verdict mail' 'little to report.md after you send the verdict mail'; ctl L13b 25 'REPORT-HASH-LAST' -- env G50A_PROMPT="$W/p_a2.txt" "$L" --check
mut "$PROMPT" "$W/p_a3.txt" 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' 'EVERY SUBJECT YOU PROPOSE SHOULD FIT THE DIFF'; ctl L13c 25 'the MERGE ADDENDUM rules' -- env G50A_PROMPT="$W/p_a3.txt" "$L" --check
mut "$PROMPT" "$W/p_a4.txt" 'FUSE 2026-10-09 rows at END' 'FUSE rows';                                               ctl L13d 25 'the MERGE ADDENDUM rules' -- env G50A_PROMPT="$W/p_a4.txt" "$L" --check
mut "$PROMPT" "$W/p_a5.txt" 'BASELINE audit-baseline.json == develop blob' 'BASELINE unchanged';                      ctl L13e 25 'the MERGE ADDENDUM rules' -- env G50A_PROMPT="$W/p_a5.txt" "$L" --check
mut "$PROMPT" "$W/p_a6.txt" 'NEW TICKET <POST AS-IS' 'NEW TICKET <ruled';                                             ctl L13f 25 'the MERGE ADDENDUM rules' -- env G50A_PROMPT="$W/p_a6.txt" "$L" --check
mut "$PROMPT" "$W/p_subj.txt" 'GATE50A #1363' 'GATE50A #1364';                                                        ctl L14 23 'the verdict subject' -- env G50A_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                         ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
mut "$PROMPT" "$W/p_k1.txt" "$GS/overlaps_1.out" "$GS/overlaps_elsewhere.out";                                         ctl L16 8 'overlaps_1.out is missing, empty, or not named' -- env G50A_PROMPT="$W/p_k1.txt" "$L" --check
mut "$PROMPT" "$W/p_k2.txt" "$GS/READY_1363_mail.md" "$GS/READY_elsewhere.md";                                         ctl L17 8 'READY_1363_mail.md is missing, empty, or not named' -- env G50A_PROMPT="$W/p_k2.txt" "$L" --check
mut "$PROMPT" "$W/p_k3.txt" '2026-09-30-batch1356-g49a/report.md' '2026-09-30-batch1357-g49b/report.md';              ctl L18 8 'the previous round report' -- env G50A_PROMPT="$W/p_k3.txt" "$L" --check
mut "$PROMPT" "$W/p_k4.txt" "$GS/gh_body_1363.md" "$GS/gh_body_elsewhere.md";                                          ctl L19 8 'gh_body_1363.md is missing, empty, or not named' -- env G50A_PROMPT="$W/p_k4.txt" "$L" --check
mut "$PROMPT" "$W/p_k5.txt" "$GS/end_tree_crosscheck_1.out" "$GS/end_tree_elsewhere.out";                              ctl L19b 8 'end_tree_crosscheck_1.out is missing, empty, or not named' -- env G50A_PROMPT="$W/p_k5.txt" "$L" --check
mut "$PROMPT" "$W/p_x1.txt" 'A NOT MEASURED runtime reach on a T1 PR is not a GO' 'A NOT MEASURED runtime reach is noted';  ctl L20 34 'the RUNTIME-FIRST rule' -- env G50A_PROMPT="$W/p_x1.txt" "$L" --check
mut "$PROMPT" "$W/p_x2.txt" 'ROUTE (b) IS REFUSED.' 'ROUTE (b) IS OPEN.';                                              ctl L21 36 'the authority line' -- env G50A_PROMPT="$W/p_x2.txt" "$L" --check
mut "$PROMPT" "$W/p_x3.txt" 'IT IS CLIENT-VISIBLE: Peter reads the board.' 'It is internal.';                          ctl L22 37 'the NEW-TICKET ruling' -- env G50A_PROMPT="$W/p_x3.txt" "$L" --check
mut "$PROMPT" "$W/p_x4.txt" 'is at 76%' 'is fine';                                                                    ctl L23 38 'the proportionality line' -- env G50A_PROMPT="$W/p_x4.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate50a.sh"
ctl R0  0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key outside reported_overlaps \| 11 expected overlap\(s\) reported \| 0 sequenced by Wednesday .*1 client-human PR\(s\) reported \| 4 kit path\(s\), 1 kit key\(s\)' -- cat "$W/R0.out"
ctl R0e 0 'EXPECTED OVERLAP \(reported_overlaps; reported, never sequenced by a gate\) #1360 PeterObeden' -- cat "$W/R0.out"
ctl R0h 0 'CLIENT-HUMAN \(reported, never sequenced by a gate\) #1362 by PeterObeden' -- cat "$W/R0.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pin, 1 of 1' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                                ctl R1 1 'is not registered in inbox_routing.conf' -- env G50A_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
echo '{}' > "$W/reported_empty.json";                                        ctl R2 15 "OVERLAP #1360 .*paths \['Blockchain/Dev/package-lock.json', 'Blockchain/Dev/services/kyc/package-lock.json'\]" -- env G50A_REPORTED="$W/reported_empty.json" "$R" "$L" "$SP" --dry-run
ctl R3  15 "OVERLAP #1253 .*title keys \['KS-1297'\]" -- env G50A_TITLE_KEY="KS-1297" "$R" "$L" "$SP" --dry-run
printf '{"1253": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H53" > "$W/seq_ok.json"
printf '{"1253": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$H" > "$W/seq_bad.json"
ctl R3s 0 'SEQUENCED OUT-OF-KIT #1253 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- env G50A_TITLE_KEY="KS-1297" G50A_SEQUENCED="$W/seq_ok.json" "$R" "$L" "$SP" --dry-run
ctl R3c 0 'DRY RUN COMPLETE' -- cat "$W/R3s.out"
ctl R3w 15 'OVERLAP #1253 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G50A_TITLE_KEY="KS-1297" G50A_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #1253 ' -- env G50A_WIDEN_RX="-l5-1$" "$R" "$L" "$SP" --dry-run
sed "s/|$H|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh";                      ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1363|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G50A_ROUTING="$W/routing_ok.conf" G50A_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins, kit.json and the filled prompt are untouched by every control above"
ctl PNZ 0 '' -- test "$(SHA "$GS/pins_gate50a.json")" = "$PINSHA"
ctl KJZ 0 '' -- test "$(SHA "$GS/kit.json")" = "$KITSHA"
ctl PRZ 0 '' -- test "$(SHA "$PROMPT")" = "$PRSHA"
echo "SUMMARY gate50a: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
