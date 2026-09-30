#!/bin/bash
# controls_gate49a.sh — every guard in the gate49a kit driven on the REAL subject (#1356, ITEM A) and on PLANTED defects, each with the rc it must
# give and a WHY pattern its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a control
# that makes it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g49a_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate49a.json, kit.json and the filled prompt are sha256-checked unchanged at the end (PNZ, KJZ, PRZ). The launcher runs with --check
# (headless) except L9, the real launch path with stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run
# that must refuse at step 0, routing) and R8 (a real run with a routed temp file that must stop at G49A_STOP_AFTER_3B) — both stop long before the
# usage gate / cockpit. Mode plants RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>): core.filemode is false.
# Each by-name keyword has its own launcher refusal (LK*): the keyword is broken into `<KW>-X`, which the launcher's TOKEN match must NOT accept.
# Shape copied from gate48b's controls, one PR, plus this kit's lockdelta / reach / overlaps / keyscan / pinpr instruments.
# Usage: controls_gate49a.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g49a_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g49a_sp/clone"; L="$GS/launch_qa_secuura_batch1356.sh"; PROMPT="$GS/2026-09-30_secuura-batch1356.prompt.txt"; CAP="$GS/mail_gate49a_ready.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate49a.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"; H="$(PJ pr_pins.head)"
SHA() { shasum -a 256 "$1" | cut -c1-64; }
PINSHA="$(SHA "$GS/pins_gate49a.json")"; KITSHA="$(SHA "$GS/kit.json")"; PRSHA="$(SHA "$PROMPT")"
MCP='Blockchain/Dev/services/mcp-server/package-lock.json'; ROOTL='Blockchain/Dev/package-lock.json'; ADM='Blockchain/Dev/frontend/admin/package-lock.json'
SHL='Blockchain/Dev/services/shared/package-lock.json'; DFM='Blockchain/Dev/services/mcp-server/Dockerfile'; MCPM='Blockchain/Dev/services/mcp-server/package.json'
H51="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["census"]["1351"]["head"])' "$GS/gh_read_1.json")"
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
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|LOCKDELTA|REACH|OVERLAPS|MODE|PINPR' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
IDN=0
commitw() { # commitw <tree> <parent> <msg>
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate49a.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate49a.invalid GIT_AUTHOR_DATE=2026-09-30T00:00:00Z GIT_COMMITTER_DATE=2026-09-30T00:00:00Z \
    git -C "$CL" commit-tree "$1" -p "$2" -m "$3"
}
mkdev() { # mkdev <path> <transform> — a develop MOVE plant: a child of develop (for --develop simulations)
  local p="$1" tf="$2" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.dev.$IDN"
  git -C "$CL" show "$DEV:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || return 1
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$DEV"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$DEV" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$DEV" "gate49a control plant: develop move on $p"
}
restack() { # restack <subject head> <path> <transform> — the subject's own tree with ONE more path edited, parent = the subject's parent
  local h="$1" p="$2" tf="$3" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.rs.$IDN"
  git -C "$CL" show "$h:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || { echo "PLANT TRANSFORM FAILED for $p" >&2; return 1; }
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$h" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate49a control plant: $p over $h"
}
remode() { # remode <subject head> <path> <mode> — the subject's own tree with ONE path's RECORDED mode changed
  local h="$1" p="$2" mo="$3" idx tree; IDN=$((IDN + 1)); idx="$W/idx.rm.$IDN"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"; GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mo,$(git -C "$CL" rev-parse "$h:$p"),$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate49a control plant: $p recorded $mo"
}
mut() { # mut <src> <dst> <old> <new> — a literal replacement (python, no shell quoting), refusing when <old> is absent
  python3 -c 'import sys; s=open(sys.argv[1]).read(); assert sys.argv[3] in s, "mut: anchor absent: " + sys.argv[3]; open(sys.argv[2], "w").write(s.replace(sys.argv[3], sys.argv[4]))' "$@"
}
echo "=== controls_gate49a $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1356 $H | END_TREE $END | plants $W"

echo "--- pin_gate49a.py (head, shape, locks only, the move, alone, the squash, RECORDED modes + control, the hook files, the unchanged pins) — simulations write pins_gate49a.SIM-<name>.json only"
PN="$GS/pin_gate49a.py"
ctl PN0  0 'PASS: FAIL=0 -> pins_gate49a.SIM-real.json .* 18 paths \+90/-90' -- python3 "$PN" "$SP" --simulate real "1356=$H"
ctl PN0e 0 "END_TREE $END \| git diff --shortstat develop END: 18 files changed, 90 insertions\(\+\), 90 deletions\(-\)" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 19 path\(s\) pinned \(18 PR, 1 control\), 19 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0k 0 'mobile/secuura-app/package-lock.json: develop 2f5f8c1f4edf .*BYTE-EQUAL in every tree' -- cat "$W/PN0.out"
ctl PN0h 0 '\.githooks/pre-push: .*IDENTICAL in every tree' -- cat "$W/PN0.out"
ctl PN1  1 'REFUSING: --develop is a controls-only override' -- python3 "$PN" "$SP" --develop "$OLDDEV"
PDF="$(restack "$H" "$DFM" "s = s + '# gate49a control plant: the Dockerfile edited\n'")"
ctl PN2  1 '\(K\) Blockchain/Dev/services/mcp-server/Dockerfile is not byte-equal' -- python3 "$PN" "$SP" --simulate df "1356=$PDF"
DCF="$(mkdev "$SHL" "a = '\"node_modules/brace-expansion\": {\n      \"version\": \"5.0.9\"'; assert s.count(a) == 1; s = s.replace(a, a[:-6] + '5.0.10\"')")"
ctl PN3  1 '\(C\) #1356: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate cfl "1356=$H" --develop "$DCF"
M755="$(remode "$H" "$MCP" 100755)"
ctl PN4  1 'Blockchain/Dev/services/mcp-server/package-lock.json: want 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1356=$M755"
DMV="$(mkdev "Blockchain/Dev/BACKLOG.md" "s = s + '\n<!-- gate49a control plant: an unrelated develop move -->\n'")"
ctl PN5  0 '#1356 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 1 path\(s\) \| reaches its own paths: NONE' -- python3 "$PN" "$SP" --simulate mv "1356=$H" --develop "$DMV"
PMF="$(restack "$H" "$MCPM" "s = s.replace('\"version\"', '\"version\"', 1) + ' '")"
ctl PN6  1 "\(B\) non-lock paths .*package.json paths \['Blockchain/Dev/services/mcp-server/package.json'\]" -- python3 "$PN" "$SP" --simulate pj "1356=$PMF"

echo "--- lockdelta_gate49a.py (LOCK-DELTA-18 / DEPENDENT-RANGES / REGISTRY-TRUE / ADVISORY-RANGES / RESIDUE / STUB prediction)"
LDP="$GS/lockdelta_gate49a.py"
OTHER="import re; m = [x for x in re.finditer(r'\"(node_modules/[^\"]+)\": \{\n\s+\"version\": \"([^\"]+)\"', s) if x.group(1) not in ('node_modules/brace-expansion', 'node_modules/fast-uri', 'node_modules/ip-address')][0]; s = s[:m.start(2)] + m.group(2) + '-g49a' + s[m.end(2):]"
ctl LD0  0 'LOCKDELTA PASS: 0 FAIL of 118 checks .* 18 locks, 30 moves \(7 PROD\), 36 dependant range\(s\) \| numstat \+90/-90' -- python3 "$LDP" "$SP"
ctl LD0p 0 'PASS L3: moves measured 30 \(claimed 30\).*EQUAL' -- cat "$W/LD0.out"
ctl LD0c 0 'PASS L4c: CONTROL: <major\+1>\.0\.0 judged against all 36 dependant range\(s\) reads NOT satisfied every time' -- cat "$W/LD0.out"
ctl LD0r 0 'PASS L5c ip-address@10\.7\.2: CONTROLS: .*reads False; .*reads False' -- cat "$W/LD0.out"
ctl LD0a 0 'PASS L6 GHSA-h3mg-xc3c-68pw: ip-address .*to-versions \[.10\.7\.2.\] OUTSIDE every range: True \| from-versions inside \(control\): \[.10\.7\.0.\]' -- cat "$W/LD0.out"
ctl LD0s 0 "L7 RESIDUE: 5 entr\(y/ies\) in 1 lock\(s\) of 45 at the head: \['Blockchain/Dev/mobile/secuura-app/package-lock.json'\]" -- cat "$W/LD0.out"
ctl LD0f 0 'L8 STUB FIXTURE GHSA-redp-roof-0001 .*: 7 fast-uri entr\(y/ies\) at the head inside it.*stays LIVE' -- cat "$W/LD0.out"
ctl LD0n 0 'numstat sum \+90/-90 \| the seat claimed \+102/-102: CLAIM DIFFERS' -- cat "$W/LD0.out"
P1="$(restack "$H" "$MCP" "$OTHER")";                                                                        ctl LD1 1 'FAIL L2 Blockchain/Dev/services/mcp-server node_modules/' -- python3 "$LDP" "$SP" --head "$P1" --offline
ctl LD1m 0 'FAIL L3: moves measured 31 \(claimed 30\)' -- cat "$W/LD1.out"
ctl LD1o 0 'NOT MEASURED L5 / L6 / L7: --offline' -- cat "$W/LD1.out"
P2="$(restack "$H" "$MCP" "a = 'sha512-GZMtZUTNRpOVIECoX'; assert s.count(a) == 1; s = s.replace(a, 'sha512-GZMtZUTNRpOVIECoY')")"; ctl LD2 1 'FAIL L5 fast-uri@3\.1\.8' -- python3 "$LDP" "$SP" --head "$P2"
P3="$(restack "$H" "$ROOTL" "a = '\"node_modules/brace-expansion\": {\n      \"version\": \"5.0.12\",'; assert s.count(a) == 1; s = s.replace(a, a + '\n      \"dev\": true,')")"; ctl LD3 1 "FAIL L2 Blockchain/Dev node_modules/brace-expansion: 5\.0\.9 -> 5\.0\.12 \| flags PROD -> dev" -- python3 "$LDP" "$SP" --head "$P3" --offline
P4="$(restack "$H" "$MCP" "a = '\"version\": \"10.7.2\"'; assert s.count(a) == 1; s = s.replace(a, '\"version\": \"11.0.0\"')")";    ctl LD4 1 'FAIL L4 Blockchain/Dev/services/mcp-server node_modules/ip-address: 10\.7\.0 -> 11\.0\.0 .*head False' -- python3 "$LDP" "$SP" --head "$P4" --offline
REV="s = s.replace('\"version\": \"5.0.12\"', '\"version\": \"5.0.9\"').replace('brace-expansion-5.0.12.tgz', 'brace-expansion-5.0.9.tgz').replace('sha512-YovQ3rzhaLMIrDjNDMkNS01tea93qhEhG5xy8f6+R0l+dw3Ki+5sCoIoI942iuLZTHWogWktgwVDhU09iNEimQ==', 'sha512-ScQ4IuvIEF1TMlP7Zt+vjJ//9zlPb2SDcxWxM3bk8s6t6GGdJ7KO1dCcTidOPJKePW30LE/2cT7wCyPho9/Wxg==')"
P5="$(restack "$H" "$ADM" "$REV")";                                                                           ctl LD5 1 "FAIL L0: changed paths 17 .*missing \['Blockchain/Dev/frontend/admin/package-lock.json'\]" -- python3 "$LDP" "$SP" --head "$P5" --offline
ctl LD6  1 'FAIL L0: changed paths 0 ' -- python3 "$LDP" "$SP" --head "$DEV" --offline
ctl LD7  0 'PASS L4s: the semver evaluator holds on 18 fixed cases' -- cat "$W/LD6.out"

echo "--- reach_gate49a.py (RUNTIME-REACH / ROOT-LOCK-CONSUMERS / SHARED-GUARD-TESTS read; controls inside)"
RCP="$GS/reach_gate49a.py"
ctl RE0  0 'REACH READ: tree 52dadb07f70d \| 11 image Dockerfile\(s\) copy a moved lock \| root-lock copies 0 .*controls hold' -- python3 "$RCP" "$SP"
ctl RE0c 0 "R1 CONTROL: the matcher finds services/mcp-server/Dockerfile's own .*COPY: True" -- cat "$W/RE0.out"
ctl RE0p 0 "Blockchain/Dev/services/mcp-server/Dockerfile +Blockchain/Dev/services/mcp-server/package-lock.json PROD \['brace-expansion 5\.0\.9->5\.0\.12', 'fast-uri 3\.1\.7->3\.1\.8', 'ip-address 10\.7\.0->10\.7\.2'\] \| dev none" -- cat "$W/RE0.out"
ctl RE0t 0 'R3 CONTROLS: .*gate-exit-codes.test.mjs: True \| a nonsense path found in 0 file' -- cat "$W/RE0.out"
ctl RE1  0 'REACH READ: tree 3e3a68260d0e \| 0 image Dockerfile\(s\) copy a moved lock' -- python3 "$RCP" "$SP" --tree "$DEV"

echo "--- overlaps_gate49a.py (carries its own two-way control)"
ctl OV0  0 'OVERLAPS READ: 10 PR\(s\) \| conflict today 1 \| conflict after ITEM A 1' -- env G49A_OVJSON="$W/overlaps.json" python3 "$GS/overlaps_gate49a.py" "$SP"
ctl OV0c 0 'CT-CLEAN an unrelated plant over the squash: clean \| CT-CONFLICT .*CONFLICT .*-> OK' -- cat "$W/OV0.out"

echo "--- keyscan_gate49a.py (subject, body, live surfaces)"
KS="$GS/keyscan_gate49a.py"; S6="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1356"]["title"])' "$GS/gh_read_1.json")"
ctl KS0  0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1  1 'FAIL #1356 S2' -- python3 "$KS" "$SP" --subject "$S6 (#1356)"
ctl KS2  1 'FAIL #1356 S1' -- python3 "$KS" "$SP" --subject "KS-1378: in-range lock refresh (KS-729)"
ctl KS3  1 'FAIL #1356 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --subject "${S6}0123456789abc"
ctl KS3b 1 "FAIL #1356 S1: subject keys \['KS-13780'\]" -- python3 "$KS" "$SP" --subject "KS-13780: in-range lock refresh"
printf '' > "$W/b_empty.txt";                                    ctl KS4 1 'FAIL #1356 B1 KS-1378' -- python3 "$KS" "$SP" --body-file "$W/b_empty.txt"
printf 'Refs KS-1378\nCloses KS-1378\n' > "$W/b_close.txt";      ctl KS5 1 'FAIL #1356 B2' -- python3 "$KS" "$SP" --body-file "$W/b_close.txt"
printf 'Refs KS-1378\nsee KS-729\n' > "$W/b_for.txt";            ctl KS6 1 "FAIL #1356 B3: .*foreign \['KS-729'\]" -- python3 "$KS" "$SP" --body-file "$W/b_for.txt"
printf 'Refs KS-1378\nthe ip-address pair continues KS-729 outside any fence\n' > "$W/pb.txt"; ctl KS7 0 "OUTSIDE any fence: \['KS-729'\]" -- python3 "$KS" "$SP" --prbody-file "$W/pb.txt"
ctl KS8  0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL' -- python3 "$KS" "$SP" --subject "KS-1378: undici 8 in every lock and a baseline row"

echo "--- pinpr_gate49a.py (the pin step itself)"
ctl PP1  1 'REFUSING: kit.json is already pinned' -- python3 "$GS/pinpr_gate49a.py" 1356 "$H" --check
ctl PP2  0 'usage: pinpr_gate49a.py' -- sh -c "python3 '$GS/pinpr_gate49a.py' 1356 notasha; exit 0"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L1  6 '#1356 — .* is not at .* AND refs/pull/1356/head' -- env G49A_HEAD_1356="$DEV" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G49A_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1356 — the compare is not the pinned' -- env G49A_PATHS_1356="$MCP" "$L" --check
mut "$PROMPT" "$W/p_go.txt" 'GO (Seat B 49th): merge 1356 on gate49a' 'GO (Seat B 49th): merge 1357 on gate49a';   ctl L4 26 'merge authority / the GO string' -- env G49A_PROMPT="$W/p_go.txt" "$L" --check
mut "$PROMPT" "$W/p_seat.txt" 'The merge seat is Seat B 49th' 'The merge seat is Seat B 48th';                   ctl L4b 26 'merge authority / the GO string' -- env G49A_PROMPT="$W/p_seat.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                        ctl L5 8 'unfilled double-brace' -- env G49A_PROMPT="$W/p_tok.txt" "$L" --check
{ cat "$PROMPT"; echo 'merge #<PR>'; } > "$W/p_ph.txt";                                                         ctl L5b 8 'unpinned PR placeholder' -- env G49A_PROMPT="$W/p_ph.txt" "$L" --check
i=0
for kw in LOCK-DELTA-18 DEPENDENT-RANGES REGISTRY-TRUE REPRODUCE-REFRESH PRISTINE-CONTROL AUDIT-LEGS-BASE-HEAD SIX-IDS-ABSENT GATE-STILL-REFUSES NO-BASELINE-ROW RUNTIME-REACH ROOT-LOCK-CONSUMERS SUITES SHARED-GUARD-TESTS NPM-CI-HEAD CLEAN-MERGE END-TREE MODES COLLISION-CENSUS SUBJECT-KEY-SCAN SUBJECT-LANDS-AT SUBJECT-TRUE-OF-DIFF REFS-OWN-KEY NO-CLOSING-KEYWORD PR-BODY-CLAIMS FOLLOW-ONS FUSE-COUNT TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  i=$((i + 1)); sed "s/$kw/$kw-X/g" "$PROMPT" > "$W/p_kw$i.txt"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G49A_PROMPT="$W/p_kw$i.txt" "$L" --check
done
sed "s/$H/${H:0:39}x/g" "$CAP" > "$W/cap_noh.md";                                                               ctl L7 20 "do not both name #1356's head" -- env G49A_BRIEF="$W/cap_noh.md" "$L" --check
mut "$PROMPT" "$W/p_h1.txt" 'NO ticket filed' 'NO tickets filed';                                                    ctl L8 39 'the HOLDS' -- env G49A_PROMPT="$W/p_h1.txt" "$L" --check
mut "$PROMPT" "$W/p_h2.txt" 'You NEVER reply to Peter' 'You may reply to Peter';                                     ctl L8b 39 'the HOLDS' -- env G49A_PROMPT="$W/p_h2.txt" "$L" --check
mut "$PROMPT" "$W/p_h3.txt" 'Never read or write a real `.env`' 'Never write a real `.env`';                         ctl L8c 39 'the HOLDS' -- env G49A_PROMPT="$W/p_h3.txt" "$L" --check
mut "$PROMPT" "$W/p_h4.txt" 'Docker runs are `--rm --network none` with the source mounted READ-ONLY' 'Docker runs are `--rm`'; ctl L8d 39 'the HOLDS' -- env G49A_PROMPT="$W/p_h4.txt" "$L" --check
mut "$PROMPT" "$W/p_h5.txt" 'No `az` command of any kind' 'No `az login`';                                          ctl L8e 39 'the HOLDS' -- env G49A_PROMPT="$W/p_h5.txt" "$L" --check
mut "$PROMPT" "$W/p_h6.txt" 'NO checklist tick' 'NO early checklist tick';                                           ctl L8f 39 'the HOLDS' -- env G49A_PROMPT="$W/p_h6.txt" "$L" --check
mut "$PROMPT" "$W/p_h7.txt" 'THE NAMED EXCEPTIONS to those holds — these and NO others' 'THE NAMED EXCEPTIONS to those holds'; ctl L8g 39 'the HOLDS' -- env G49A_PROMPT="$W/p_h7.txt" "$L" --check
mut "$PROMPT" "$W/p_h8.txt" 'NEVER `up`, `down`' '`up`, `down`';                                                     ctl L8h 39 'the HOLDS' -- env G49A_PROMPT="$W/p_h8.txt" "$L" --check
mut "$PROMPT" "$W/p_h9.txt" '"no lock regenerated" means no REAL lock' '"no lock regenerated" means little';        ctl L8i 39 'the HOLDS' -- env G49A_PROMPT="$W/p_h9.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                            ctl L10 31 'launch develop / the END_TREE' -- env G49A_PROMPT="$W/p_dev.txt" "$L" --check
mut "$PROMPT" "$W/p_tier.txt" '#1356 T1 —' '#1356 T2 —';                                                              ctl L11 7 'the tier line' -- env G49A_PROMPT="$W/p_tier.txt" "$L" --check
mut "$PROMPT" "$W/p_round.txt" 'a round-1 NO GO goes back to the author for round 2' 'a round-1 NO GO ships nothing';  ctl L11b 7 'the tiering rule' -- env G49A_PROMPT="$W/p_round.txt" "$L" --check
mut "$PROMPT" "$W/p_tkt.txt" 'PR #1356 is KS-1378' 'PR #1356 is KS-1379';                                             ctl L12 32 "state 'PR #1356 is KS-1378'" -- env G49A_PROMPT="$W/p_tkt.txt" "$L" --check
mut "$PROMPT" "$W/p_a1.txt" 'MG-1 18 over 18 paths' 'MG-1 over the paths';                                            ctl L13 25 'the MERGE ADDENDUM rules' -- env G49A_PROMPT="$W/p_a1.txt" "$L" --check
mut "$PROMPT" "$W/p_a2.txt" 'NOTHING to report.md after you send the verdict mail' 'little to report.md after you send the verdict mail'; ctl L13b 25 'REPORT-HASH-LAST' -- env G49A_PROMPT="$W/p_a2.txt" "$L" --check
mut "$PROMPT" "$W/p_a3.txt" 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' 'EVERY SUBJECT YOU PROPOSE SHOULD FIT THE DIFF'; ctl L13c 25 'the MERGE ADDENDUM rules' -- env G49A_PROMPT="$W/p_a3.txt" "$L" --check
mut "$PROMPT" "$W/p_a4.txt" 'FUSE 2026-10-09 rows at END' 'FUSE rows';                                               ctl L13d 25 'the MERGE ADDENDUM rules' -- env G49A_PROMPT="$W/p_a4.txt" "$L" --check
mut "$PROMPT" "$W/p_a5.txt" 'BASELINE audit-baseline.json == develop blob' 'BASELINE unchanged';                      ctl L13e 25 'the MERGE ADDENDUM rules' -- env G49A_PROMPT="$W/p_a5.txt" "$L" --check
mut "$PROMPT" "$W/p_subj.txt" 'GATE49A #1356' 'GATE49A #1357';                                                        ctl L14 23 'the verdict subject' -- env G49A_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                         ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
mut "$PROMPT" "$W/p_k1.txt" "$GS/overlaps_1.out" "$GS/overlaps_elsewhere.out";                                         ctl L16 8 'overlaps_1.out is missing, empty, or not named' -- env G49A_PROMPT="$W/p_k1.txt" "$L" --check
mut "$PROMPT" "$W/p_k2.txt" "$GS/reach_1.out" "$GS/reach_elsewhere.out";                                               ctl L17 8 'reach_1.out is missing, empty, or not named' -- env G49A_PROMPT="$W/p_k2.txt" "$L" --check
mut "$PROMPT" "$W/p_k3.txt" '2026-09-30-batch1355-g48b/report.md' '2026-09-30-batch1354-g48a/report.md';              ctl L18 8 'the previous round report' -- env G49A_PROMPT="$W/p_k3.txt" "$L" --check
mut "$PROMPT" "$W/p_k4.txt" "$GS/gh_body_1356.md" "$GS/gh_body_elsewhere.md";                                          ctl L19 8 'gh_body_1356.md is missing, empty, or not named' -- env G49A_PROMPT="$W/p_k4.txt" "$L" --check
mut "$PROMPT" "$W/p_x1.txt" 'A NOT MEASURED runtime reach on a T1 PR is not a GO' 'A NOT MEASURED runtime reach is noted';  ctl L20 34 'the RUNTIME-FIRST rule' -- env G49A_PROMPT="$W/p_x1.txt" "$L" --check
mut "$PROMPT" "$W/p_x2.txt" 'The 09-09 baseline grant is NOT used.' 'The 09-09 baseline grant is used.';               ctl L21 36 'the authority line' -- env G49A_PROMPT="$W/p_x2.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate49a.sh"
ctl R0  0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key outside reported_overlaps \| 10 expected overlap\(s\) reported \| 0 sequenced by Wednesday .*3 client-human PR\(s\) reported \| 18 kit path\(s\), 1 kit key\(s\)' -- cat "$W/R0.out"
ctl R0e 0 'EXPECTED OVERLAP \(reported_overlaps; reported, never sequenced by a gate\) #949 dependabot' -- cat "$W/R0.out"
ctl R0h 0 'CLIENT-HUMAN \(reported, never sequenced by a gate\) #1351 by PeterObeden' -- cat "$W/R0.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pin, 1 of 1' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                                ctl R1 1 'is not registered in inbox_routing.conf' -- env G49A_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
echo '{}' > "$W/reported_empty.json";                                        ctl R2 15 'OVERLAP #949 .*paths \[.Blockchain/Dev/package-lock.json.\]' -- env G49A_REPORTED="$W/reported_empty.json" "$R" "$L" "$SP" --dry-run
ctl R3  15 'OVERLAP #1351 .*title keys \[.KS-1386.\]' -- env G49A_TITLE_KEY="KS-1386" "$R" "$L" "$SP" --dry-run
printf '{"1351": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H51" > "$W/seq_ok.json"
printf '{"1351": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$H" > "$W/seq_bad.json"
ctl R3s 0 'SEQUENCED OUT-OF-KIT #1351 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- env G49A_TITLE_KEY="KS-1386" G49A_SEQUENCED="$W/seq_ok.json" "$R" "$L" "$SP" --dry-run
ctl R3c 0 'DRY RUN COMPLETE' -- cat "$W/R3s.out"
ctl R3w 15 'OVERLAP #1351 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G49A_TITLE_KEY="KS-1386" G49A_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #125[03] ' -- env G49A_WIDEN_RX="-l5-1$" "$R" "$L" "$SP" --dry-run
sed "s/|$H|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh";                      ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1356|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G49A_ROUTING="$W/routing_ok.conf" G49A_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins, kit.json and the filled prompt are untouched by every control above"
ctl PNZ 0 '' -- test "$(SHA "$GS/pins_gate49a.json")" = "$PINSHA"
ctl KJZ 0 '' -- test "$(SHA "$GS/kit.json")" = "$KITSHA"
ctl PRZ 0 '' -- test "$(SHA "$PROMPT")" = "$PRSHA"
echo "SUMMARY gate49a: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
