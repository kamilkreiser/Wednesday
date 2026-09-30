#!/bin/bash
# controls_gate48b.sh — every guard in the gate48b kit driven on the REAL subjects (#1354 then #1355) and on PLANTED defects, each with the rc it
# must give and a WHY pattern its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a
# control that makes it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g48b_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate48b.json and lockcensus_gate48b.json are sha256-checked unchanged at the end (PNZ, LCZ). The launcher runs with --check (headless)
# except L9, the real launch path with stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run that must
# refuse at step 0, routing) and R8 (a real run with a routed temp file that must stop at G48B_STOP_AFTER_3B) — both stop long before the usage
# gate / cockpit. Mode plants RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>): core.filemode is false, a disk chmod proves nothing.
# Each by-name keyword has its own launcher refusal (LK*): the keyword is broken into `<KW>-X`, which the launcher's TOKEN match must NOT accept.
# A REAL old commit is used as a control subject where one exists: #1354's gate48a head 4370be410bbf (the row WITH expires, no contract line).
# Shape copied from gate48a's controls, two PRs, plus this kit's lock-delta / baseline / census / overlaps / image instruments.
# Usage: controls_gate48b.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g48b_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g48b_sp/clone"; L="$GS/launch_qa_secuura_batch1355.sh"; PROMPT="$GS/2026-09-30_secuura-batch1355.prompt.txt"; CAP="$GS/mail_gate48b_ready.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate48b.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"; H4="$(PJ prs.1354.head)"; H5="$(PJ prs.1355.head)"
OLD4='4370be410bbf37b839b1030f3e28f95d11c454fe'
PINSHA="$(shasum -a 256 "$GS/pins_gate48b.json" | cut -c1-64)"; LCSHA="$(shasum -a 256 "$GS/lockcensus_gate48b.json" | cut -c1-64)"
PERF='systemTest/performance/package-lock.json'; BL='Blockchain/Dev/scripts/audit/audit-baseline.json'; CT='Blockchain/Dev/scripts/audit/baseline-contract.mjs'
ISSL='Blockchain/Dev/frontend/issuer/package-lock.json'; ROOTL='Blockchain/Dev/package-lock.json'; ROOTM='Blockchain/Dev/package.json'; DF='Blockchain/Dev/frontend/issuer/Dockerfile'
H51="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["census"]["1351"]["head"])' "$GS/gh_read_1.json")"
TOT=0; OK=0; MM=0; RETRIES=0
ctl() { # ctl <id> <expected rc> <why regex or ''> -- <command...>
  local id="$1" exp="$2" why="$3"; shift 4
  local out rc good try=0; out="$("$@" 2>&1)"; rc=$?
  # GitHub intermittently DENIES the Secuura deploy key's SSH auth under a burst of ls-remote / fetch (gate47, measured). The GUARDS fail closed
  # on it (rc 2 / REFUSING), which is right; the HARNESS retries such a run up to 3 times, 20 s apart, and counts every retry.
  while [ "$try" -lt 3 ] && printf '%s' "$out" | grep -qE 'Permission denied \(publickey\)|Could not read from remote repository'; do
    try=$((try + 1)); RETRIES=$((RETRIES + 1)); sleep 20; out="$("$@" 2>&1)"; rc=$?
  done
  printf '%s\n' "$out" > "$W/$id.out"
  good=0; [ "$rc" = "$exp" ] && { [ -z "$why" ] || printf '%s' "$out" | grep -qE -- "$why"; } && good=1
  [ "$INV" = 1 ] && good=$((1 - good))
  TOT=$((TOT + 1)); if [ "$good" = 1 ]; then OK=$((OK + 1)); v=OK; else MM=$((MM + 1)); v=MISMATCH; fi
  local shown=''; if [ -n "$why" ]; then shown="$(printf '%s' "$out" | grep -E -- "$why" | tail -1)"; fi
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|LOCKDELTA|BASELINE|CENSUS|OVERLAPS|IMAGE READ|MODE' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
mkdev() { # mkdev <path> <transform> — a develop MOVE plant: a child of develop (for --develop simulations)
  local p="$1" tf="$2" idx="$W/idx.dev.$RANDOM" nb tree
  git -C "$CL" show "$DEV:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || return 1
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$DEV"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$DEV" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate48b.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate48b.invalid GIT_AUTHOR_DATE=2026-09-30T00:00:00Z GIT_COMMITTER_DATE=2026-09-30T00:00:00Z \
    git -C "$CL" commit-tree "$tree" -p "$DEV" -m "gate48b control plant: develop move on $p"
}
restack() { # restack <subject head> <path> <transform> — the subject's own tree with ONE more path edited, parent = the subject's parent
  local h="$1" p="$2" tf="$3" idx="$W/idx.rs.$RANDOM" nb tree
  git -C "$CL" show "$h:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || { echo "PLANT TRANSFORM FAILED for $p" >&2; return 1; }
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$h" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate48b.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate48b.invalid GIT_AUTHOR_DATE=2026-09-30T00:00:00Z GIT_COMMITTER_DATE=2026-09-30T00:00:00Z \
    git -C "$CL" commit-tree "$tree" -p "$(git -C "$CL" rev-parse "$h^")" -m "gate48b control plant: $p over $h"
}
remode() { # remode <subject head> <path> <mode> — the subject's own tree with ONE path's RECORDED mode changed
  local h="$1" p="$2" mo="$3" idx="$W/idx.rm.$RANDOM" tree
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"; GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mo,$(git -C "$CL" rev-parse "$h:$p"),$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate48b.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate48b.invalid GIT_AUTHOR_DATE=2026-09-30T00:00:00Z GIT_COMMITTER_DATE=2026-09-30T00:00:00Z \
    git -C "$CL" commit-tree "$tree" -p "$(git -C "$CL" rev-parse "$h^")" -m "gate48b control plant: $p recorded $mo"
}
mut() { # mut <src> <dst> <old> <new> — a literal replacement (python, no shell quoting), refusing when <old> is absent
  python3 -c 'import sys; s=open(sys.argv[1]).read(); assert sys.argv[3] in s, "mut: anchor absent: " + sys.argv[3]; open(sys.argv[2], "w").write(s.replace(sys.argv[3], sys.argv[4]))' "$@"
}
echo "=== controls_gate48b $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1354 $H4 | #1355 $H5 | END_TREE $END | plants $W"

echo "--- pin_gate48b.py (heads, shape, the move, alone, the CHAIN with its NO-OP, END both orders, RECORDED modes + control, the hook, the Dockerfile) — simulations write pins_gate48b.SIM-<name>.json only"
PN="$GS/pin_gate48b.py"
ctl PN0  0 'PASS: FAIL=0 -> pins_gate48b.SIM-real.json' -- python3 "$PN" "$SP" --simulate real ""
ctl PN0e 0 "END_TREE $END \| diff\(develop, END\): 7 path\(s\) == the union of the own paths \(7\): True" -- cat "$W/PN0.out"
ctl PN0n 0 "ORDER step #1355 on [0-9a-f]{12}: clean .*NO-OP \(already at the tip\): \['systemTest/performance/package-lock.json'\]" -- cat "$W/PN0.out"
ctl PN0r 0 "REVERSE-order END $END \| == END_TREE: True" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 9 path\(s\) pinned \(8 PR, 1 control\), 9 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0k 0 'frontend/issuer/Dockerfile: develop 67d5abc68560 .*BYTE-EQUAL in every tree' -- cat "$W/PN0.out"
ctl PN0h 0 '\.githooks/pre-push: .*IDENTICAL in every tree' -- cat "$W/PN0.out"
ctl PN1  1 '\(A\) #1355 head .* != the expected \(pinned\) head' -- python3 "$PN" "$SP" --expect-head "1355=$DEV"
ctl PN1d 1 'REFUSING: --develop is a controls-only override' -- python3 "$PN" "$SP" --develop "$OLDDEV"
PDF="$(restack "$H5" "$DF" "s = s + '# gate48b control plant: the Dockerfile edited\n'")"
ctl PN2  1 '\(K\) Blockchain/Dev/frontend/issuer/Dockerfile is not byte-equal' -- python3 "$PN" "$SP" --simulate df "1355=$PDF"
DCF="$(mkdev "$ROOTM" "a = '\"morgan\": \"^1.12.1\",'; assert s.count(a) == 1, s.count(a); s = s.replace(a, '\"morgan\": \"^1.12.2\",')")"
ctl PN3  1 '\(C\) #1355: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate cfl "1354=$H4,1355=$H5" --develop "$DCF"
M755="$(remode "$H5" "$ROOTM" 100755)"
ctl PN4  1 '#1355 Blockchain/Dev/package.json: want 100644 \| head 100755 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1355=$M755"
DMV="$(mkdev "Blockchain/Dev/BACKLOG.md" "s = s + '\n<!-- gate48b control plant: an unrelated develop move -->\n'")"
ctl PN5  0 '#1355 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 1 path\(s\) \| reaches its own paths: NONE' -- python3 "$PN" "$SP" --simulate mv "1354=$H4,1355=$H5" --develop "$DMV"
ctl PN6  0 "SUPERSEDED heads pinned: \[.1354.\]" -- python3 "$PN" "$SP" --simulate old1354 "1354=$OLD4"
ctl PN6s 0 "#1354 head $OLD4 is SUPERSEDED" -- cat "$W/PN6.out"
JY="i = s.index('/js-yaml/-/js-yaml-5.4.2.tgz'); j = s.rindex('\"version\": \"5.4.2\"', 0, i); s = s[:j] + '\"version\": \"5.4.1\"' + s[j + 18:]"
PJY="$(restack "$H4" "$PERF" "$JY")"
ctl PN7  1 "ORDER step #1355: merge-tree rc 1 — CONFLICT|\(F\) chain: step #1355 NOT clean" -- python3 "$PN" "$SP" --simulate jy "1354=$PJY"
ctl PN7n 0 "OVERLAP #1354 x #1355: systemTest/performance/package-lock.json .*SAME blob\+mode: False" -- cat "$W/PN7.out"

echo "--- lockdelta_gate48b.py (LOCK-DELTA-BOTH prediction)"
LDP="$GS/lockdelta_gate48b.py"; OTHER="import re; m = [x for x in re.finditer(r'\"(node_modules/[^\"]+)\": \{\n\s+\"version\": \"([^\"]+)\"', s) if x.group(1) not in ('node_modules/undici',)][0]; s = s[:m.start(2)] + m.group(2) + '-g48b' + s[m.end(2):]"
ctl LD0  0 'LOCKDELTA PASS: 0 FAIL' -- python3 "$LDP" "$SP"
ctl LD0d 0 'PASS D2: root: the same 3 undici entries \+ exactly 12 flag-only entries' -- cat "$W/LD0.out"
ctl LD0r 0 'issuer head +@connectrpc/connect-node .*declares \^5\.28\.3\) -> node_modules/undici 7\.30\.0' -- cat "$W/LD0.out"
P1="$(restack "$H5" "$ISSL" "$OTHER")";                                                                      ctl LD1 1 'FAIL D1: issuer' -- python3 "$LDP" "$SP" --head "$P1" --offline
P2="$(restack "$H5" "$ISSL" "a = 'sha512-dkrQXeHSaoam'; assert s.count(a) == 1; s = s.replace(a, 'sha512-DkrQXeHSaoam')")"; ctl LD2 1 'FAIL D4 issuer' -- python3 "$LDP" "$SP" --head "$P2"
ctl LD2c 0 'PASS D4c issuer: CONTROL' -- cat "$W/LD2.out"
P3="$(restack "$H5" "$ROOTM" "a = '\"undici\": \"^7.29.1\",\n    \"jsdom\"'; assert s.count(a) == 1; s = s.replace(a, '\"undici\": \"^7.29.1\",\n    \"zz-g48b\": \"1.0.0\",\n    \"jsdom\"')")"; ctl LD3 1 'FAIL M1 Dev' -- python3 "$LDP" "$SP" --head "$P3" --offline
P4="$(restack "$H5" "$ROOTL" "$OTHER")";                                                                      ctl LD4 1 'FAIL D2: root' -- python3 "$LDP" "$SP" --head "$P4" --offline
P5="$(restack "$H5" "$PERF" "$JY")"; ctl LD5 1 'FAIL D6: performance lock blob' -- python3 "$LDP" "$SP" --head "$P5" --offline
ctl LD6  0 'NOT MEASURED D4 / D5: --offline' -- cat "$W/LD5.out"

echo "--- baseline_gate48b.py (ROW-PERMANENT-FIELDS / CONTRACT-LINE-ONLY / NO-BASELINE-ROW / FUSE-COUNT / FOLLOW-ONS predictions)"
BLP="$GS/baseline_gate48b.py"
ctl BL0  0 'BASELINE PASS: 0 FAIL .*FUSE-COUNT 4 on 2026-10-09 at END' -- python3 "$BLP" "$SP"
ctl BL0c 0 'PASS R2: CONTRACT-LINE-ONLY: numstat 1 0 .*GHSA-p88m-4jfj-68fv < GHSA-r53p-7pc4-xj5r < GHSA-v2v4-37r5-5v8g: True' -- cat "$W/BL0.out"
ctl BL1  1 "FAIL R1: ROW-PERMANENT-FIELDS: .*expires '2026-10-09' PRESENT" -- python3 "$BLP" "$SP" --head1354 "$OLD4"
ctl BL1c 0 'FAIL R2: CONTRACT-LINE-ONLY: numstat empty' -- cat "$W/BL1.out"
PNA="$(restack "$H4" "$CT" "import re; l = [x for x in s.split('\n') if \"'GHSA-r53p-7pc4-xj5r'\" in x]; assert len(l) == 1; s = s.replace(l[0] + '\n', '', 1); a = \"  'GHSA-w5hq-g745-h8pq',\"; i = s.index(a); j = s.index('\n', i) + 1; s = s[:j] + l[0] + '\n' + s[j:]")"
ctl BL2  1 'FAIL R2: CONTRACT-LINE-ONLY: .*: False' -- python3 "$BLP" "$SP" --head1354 "$PNA"
PEX="$(restack "$H4" "$BL" "i = s.index('\"GHSA-r53p-7pc4-xj5r\"'); j = s.index('\"decidedAt\": \"2026-09-30\"', i); k = j + len('\"decidedAt\": \"2026-09-30\"'); s = s[:k] + ',\n      \"expires\": \"2026-10-09\"' + s[k:]")"
ctl BL3  1 "FAIL R1: .*expires '2026-10-09' PRESENT" -- python3 "$BLP" "$SP" --head1354 "$PEX"
ctl BL3e 0 'FAIL R3: the contract' -- cat "$W/BL3.out"
POR="$(restack "$H4" "$BL" "a = '\"decidedAt\": \"2026-07-19\"'; assert s.count(a) >= 1; s = s.replace(a, '\"decidedAt\": \"2026-07-20\"', 1)")"
ctl BL4  1 "FAIL R1: .*CHANGED|FAIL R1:" -- python3 "$BLP" "$SP" --head1354 "$POR"
ctl BL4c 0 "CHANGED \['GHSA-" -- cat "$W/BL4.out"

echo "--- lockcensus_gate48b.py (ROOT-LOCK-CONSUMERS / UNDICI-MAJOR-RUNTIME READ; controls CT-* inside)"
LCP="$GS/lockcensus_gate48b.py"
ctl LC0  0 'CENSUS DONE: 45 lock\(s\), 17 undici/js-yaml/connect-node entr\(y/ies\), 1 vulnerable \| root-lock copies 0' -- python3 "$LCP" "$SP"
ctl LC0c 0 'CONTROL: the matcher finds the issuer Dockerfile.s per-directory .frontend/issuer/package\*\.json. COPY: True' -- cat "$W/LC0.out"
ctl LC1  0 'CENSUS DONE: 45 lock\(s\), 19 undici/js-yaml/connect-node entr\(y/ies\), 4 vulnerable' -- python3 "$LCP" "$SP" --tree "$DEV" --offline
ctl LC1v 0 'VUL +undici +5\.29\.0 +dev=False Blockchain/Dev/frontend/issuer/package-lock.json' -- cat "$W/LC1.out"
ctl LC2  0 'ranges READ \(OFFLINE fallback, not read\)' -- cat "$W/LC1.out"

echo "--- overlaps_gate48b.py and image_read_gate48b.sh (each carries its own two-way control)"
ctl OV0  0 'OVERLAPS READ: 11 PR\(s\)' -- env G48B_OVJSON="$W/overlaps.json" python3 "$GS/overlaps_gate48b.py" "$SP"
ctl OV0c 0 'CT-CLEAN an unrelated plant over #1354 then #1355 squash: clean \| CT-CONFLICT .*CONFLICT' -- cat "$W/OV0.out"
ctl IR0  0 'IMAGE READ OK: 4 issuer probe images share one content' -- "$GS/image_read_gate48b.sh"
ctl IR0c 0 'CONTROL dev-vc-issuer layer list [0-9a-f]{16} differs: True' -- cat "$W/IR0.out"

echo "--- keyscan_gate48b.py (subjects, bodies, live-surface FLAGs)"
KS="$GS/keyscan_gate48b.py"; S5="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1355"]["subject"])' "$GS/kit.json")"
ctl KS0  0 'KEYSCAN PASS: 12 checks over 2 PR\(s\), 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1  1 'FAIL #1355 S2' -- python3 "$KS" "$SP" --pr 1355 --subject "$S5 (#1355)"
ctl KS2  1 'FAIL #1355 S1' -- python3 "$KS" "$SP" --pr 1355 --subject "KS-1378: undici 7.30.0 in both locks (KS-470)"
ctl KS3  1 'FAIL #1355 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --pr 1355 --subject "${S5}01234567"
ctl KS3b 1 "FAIL #1355 S1: subject keys \['KS-13780'\]" -- python3 "$KS" "$SP" --pr 1355 --subject "KS-13780: undici 7.30.0 in both locks"
printf '' > "$W/b_empty.txt";                                    ctl KS4 1 'FAIL #1355 B1 KS-1378' -- python3 "$KS" "$SP" --pr 1355 --body-file "$W/b_empty.txt"
printf 'Refs KS-1378\nCloses KS-1378\n' > "$W/b_close.txt";      ctl KS5 1 'FAIL #1355 B2' -- python3 "$KS" "$SP" --pr 1355 --body-file "$W/b_close.txt"
printf 'Refs KS-1378\nsee KS-470\n' > "$W/b_for.txt";            ctl KS6 1 "FAIL #1355 B3: .*foreign \['KS-470'\]" -- python3 "$KS" "$SP" --pr 1355 --body-file "$W/b_for.txt"
printf 'KS-1378 continues KS-559 outside any fence\n' > "$W/pb.txt"; ctl KS7 0 "OUTSIDE any fence: \['KS-559'\]" -- python3 "$KS" "$SP" --pr 1355 --prbody-file "$W/pb.txt"
ctl KS8  0 'KEYSCAN PASS: 6 checks over 1 PR\(s\), 0 FAIL' -- python3 "$KS" "$SP" --pr 1355 --subject "KS-1378: undici 7.30.0 in both locks and a baseline row added"
ctl KS9  1 'FAIL #1354 S1' -- python3 "$KS" "$SP" --pr 1354 --subject "KS-1378: js-yaml 5.4.2 and a permanent r53p row"
ctl KS9b 1 'FAIL #1354 B1 KS-470' -- python3 "$KS" "$SP" --pr 1354 --body-file "$W/b_empty.txt"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L1  6 '#1355 — .* is not at .* AND refs/pull/1355/head' -- env G48B_HEAD_1355="$DEV" "$L" --check
ctl L1b 6 '#1354 — .* is not at .* AND refs/pull/1354/head' -- env G48B_HEAD_1354="$DEV" "$L" --check
ctl L1s 35 'SUPERSEDED head 4370be410bbf' -- env G48B_HEAD_1354="$OLD4" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G48B_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1355 — the compare is not the pinned' -- env G48B_PATHS_1355="$ROOTM" "$L" --check
mut "$PROMPT" "$W/p_go.txt" 'GO (Seat B 48th): merge 1354 1355 on gate48b' 'GO (Seat B 48th): merge 1355 on gate48b';          ctl L4 26 'merge authority / the GO string' -- env G48B_PROMPT="$W/p_go.txt" "$L" --check
mut "$PROMPT" "$W/p_seat.txt" 'The merge seat is Seat B 48th' 'The merge seat is Seat B 47th';                     ctl L4b 26 'merge authority / the GO string' -- env G48B_PROMPT="$W/p_seat.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                          ctl L5 8 'unfilled double-brace' -- env G48B_PROMPT="$W/p_tok.txt" "$L" --check
i=0
for kw in ROW-PERMANENT-FIELDS CONTRACT-LINE-ONLY LOCK-DELTA-BOTH UPDATE-VERB-CORRECTION AUDIT-LEGS-HEAD-END NO-BASELINE-ROW ISSUER-IMAGE SUITES UNDICI-MAJOR-RUNTIME ROOT-LOCK-CONSUMERS PUSH-PREFLIGHT FOLLOW-ONS FUSE-COUNT CLEAN-MERGE END-TREE MODES OUT-OF-KIT-CENSUS SUBJECT-KEY-SCAN SUBJECT-LANDS-AT SUBJECT-TRUE-OF-DIFF REFS-OWN-KEY NO-CLOSING-KEYWORD PR-BODY-CLAIMS TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  i=$((i + 1)); sed "s/$kw/$kw-X/g" "$PROMPT" > "$W/p_kw$i.txt"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G48B_PROMPT="$W/p_kw$i.txt" "$L" --check
done
sed "s/$H5/${H5:0:39}x/g" "$CAP" > "$W/cap_noh.md";                                                                ctl L7 20 "do not both name #1355's head" -- env G48B_BRIEF="$W/cap_noh.md" "$L" --check
sed "s/$H4/${H4:0:39}x/g" "$CAP" > "$W/cap_noh4.md";                                                               ctl L7b 20 "do not both name #1354's head" -- env G48B_BRIEF="$W/cap_noh4.md" "$L" --check
mut "$PROMPT" "$W/p_h1.txt" 'NO ticket filed' 'NO tickets filed';                                                    ctl L8 39 'the HOLDS' -- env G48B_PROMPT="$W/p_h1.txt" "$L" --check
mut "$PROMPT" "$W/p_h2.txt" 'You NEVER reply to Peter' 'You may reply to Peter';                                     ctl L8b 39 'the HOLDS' -- env G48B_PROMPT="$W/p_h2.txt" "$L" --check
mut "$PROMPT" "$W/p_h3.txt" 'Never read or write a real `.env`' 'Never write a real `.env`';                         ctl L8c 39 'the HOLDS' -- env G48B_PROMPT="$W/p_h3.txt" "$L" --check
mut "$PROMPT" "$W/p_h4.txt" 'Docker runs are `--rm --network none` with the source mounted READ-ONLY' 'Docker runs are `--rm`'; ctl L8d 39 'the HOLDS' -- env G48B_PROMPT="$W/p_h4.txt" "$L" --check
mut "$PROMPT" "$W/p_h5.txt" 'No `az` command of any kind' 'No `az login`';                                          ctl L8e 39 'the HOLDS' -- env G48B_PROMPT="$W/p_h5.txt" "$L" --check
mut "$PROMPT" "$W/p_h6.txt" 'NO checklist tick' 'NO early checklist tick';                                           ctl L8f 39 'the HOLDS' -- env G48B_PROMPT="$W/p_h6.txt" "$L" --check
mut "$PROMPT" "$W/p_h7.txt" 'THE NAMED EXCEPTIONS to those holds — these and NO others' 'THE NAMED EXCEPTIONS to those holds'; ctl L8g 39 'the HOLDS' -- env G48B_PROMPT="$W/p_h7.txt" "$L" --check
mut "$PROMPT" "$W/p_h8.txt" 'NEVER `up`, `down`' '`up`, `down`';                                                     ctl L8h 39 'the HOLDS' -- env G48B_PROMPT="$W/p_h8.txt" "$L" --check
mut "$PROMPT" "$W/p_h9.txt" '"no lock regenerated" means no REAL lock' '"no lock regenerated" means little';        ctl L8i 39 'the HOLDS' -- env G48B_PROMPT="$W/p_h9.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                            ctl L10 31 'launch develop / the END_TREE' -- env G48B_PROMPT="$W/p_dev.txt" "$L" --check
mut "$PROMPT" "$W/p_tier.txt" '#1355 T1 —' '#1355 T2 —';                                                              ctl L11 7 'the tier lines' -- env G48B_PROMPT="$W/p_tier.txt" "$L" --check
mut "$PROMPT" "$W/p_round.txt" 'a round-1 NO GO goes back to the author for round 2' 'a round-1 NO GO ships nothing';  ctl L11b 7 'the tiering rule' -- env G48B_PROMPT="$W/p_round.txt" "$L" --check
mut "$PROMPT" "$W/p_tkt.txt" 'PR #1355 is KS-1378' 'PR #1355 is KS-1379';                                             ctl L12 32 "BOTH state 'PR #1354 is KS-470' and 'PR #1355 is KS-1378'" -- env G48B_PROMPT="$W/p_tkt.txt" "$L" --check
mut "$PROMPT" "$W/p_a1.txt" 'MG-1 3 over 3 then 5 over 5 paths' 'MG-1 over the paths';                               ctl L13 25 'the MERGE ADDENDUM rules' -- env G48B_PROMPT="$W/p_a1.txt" "$L" --check
mut "$PROMPT" "$W/p_a2.txt" 'NOTHING to report.md after you send the verdict mail' 'little to report.md after you send the verdict mail'; ctl L13b 25 'REPORT-HASH-LAST' -- env G48B_PROMPT="$W/p_a2.txt" "$L" --check
mut "$PROMPT" "$W/p_a3.txt" 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' 'EVERY SUBJECT YOU PROPOSE SHOULD FIT THE DIFF'; ctl L13c 25 'the MERGE ADDENDUM rules' -- env G48B_PROMPT="$W/p_a3.txt" "$L" --check
mut "$PROMPT" "$W/p_a4.txt" 'FUSE 2026-10-09 rows at END' 'FUSE rows';                                               ctl L13d 25 'the MERGE ADDENDUM rules' -- env G48B_PROMPT="$W/p_a4.txt" "$L" --check
mut "$PROMPT" "$W/p_a5.txt" 'BASELINE audit-baseline.json == #1354 head blob' 'BASELINE unchanged';                  ctl L13e 25 'the MERGE ADDENDUM rules' -- env G48B_PROMPT="$W/p_a5.txt" "$L" --check
mut "$PROMPT" "$W/p_subj.txt" 'GATE48B #1354 #1355' 'GATE48B #1355';                                                  ctl L14 23 'the verdict subject' -- env G48B_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                         ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
mut "$PROMPT" "$W/p_k1.txt" "$GS/overlaps_1.out" "$GS/overlaps_elsewhere.out";                                         ctl L16 8 'overlaps_1.out is missing, empty, or not named' -- env G48B_PROMPT="$W/p_k1.txt" "$L" --check
mut "$PROMPT" "$W/p_k2.txt" "$GS/row_reason_gate48b.md" "$GS/row_elsewhere.md";                                       ctl L17 8 'row_reason_gate48b.md is missing, empty, or not named' -- env G48B_PROMPT="$W/p_k2.txt" "$L" --check
mut "$PROMPT" "$W/p_k3.txt" '2026-09-30-batch1354-g48a/report.md' '2026-09-30-batch1349-g47/report.md';              ctl L18 8 'the previous round report' -- env G48B_PROMPT="$W/p_k3.txt" "$L" --check
mut "$PROMPT" "$W/p_k4.txt" "$GS/image_read_1.out" "$GS/image_elsewhere.out";                                           ctl L19 8 'image_read_1.out is missing, empty, or not named' -- env G48B_PROMPT="$W/p_k4.txt" "$L" --check
mut "$PROMPT" "$W/p_x1.txt" 'A NOT MEASURED runtime question on a T1 PR is not a GO' 'A NOT MEASURED runtime question is noted';  ctl L20 34 'the RUNTIME-FIRST rule' -- env G48B_PROMPT="$W/p_x1.txt" "$L" --check
mut "$PROMPT" "$W/p_x2.txt" "KAM'S RULING — not the advisory-baseline grant" "the advisory-baseline grant";                       ctl L21 36 "Kam's ruling as the authority" -- env G48B_PROMPT="$W/p_x2.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate48b.sh"
ctl R0  0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key outside reported_overlaps \| 11 expected overlap\(s\) reported \| 0 sequenced by Wednesday .*3 client-human PR\(s\) reported \| 7 kit path\(s\), 3 kit key\(s\)' -- cat "$W/R0.out"
ctl R0e 0 'EXPECTED OVERLAP \(reported_overlaps; reported, never sequenced by a gate\) #949 dependabot' -- cat "$W/R0.out"
ctl R0h 0 'CLIENT-HUMAN \(reported, never sequenced by a gate\) #1351 by PeterObeden' -- cat "$W/R0.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pins, 2 of 2' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                                ctl R1 1 'is not registered in inbox_routing.conf' -- env G48B_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
echo '{}' > "$W/reported_empty.json";                                        ctl R2 15 'OVERLAP #949 .*paths \[.Blockchain/Dev/package-lock.json.\]' -- env G48B_REPORTED="$W/reported_empty.json" "$R" "$L" "$SP" --dry-run
ctl R3  15 'OVERLAP #1351 .*title keys \[.KS-1386.\]' -- env G48B_TITLE_KEY="KS-1386" "$R" "$L" "$SP" --dry-run
printf '{"1351": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H51" > "$W/seq_ok.json"
printf '{"1351": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$H5" > "$W/seq_bad.json"
ctl R3s 0 'SEQUENCED OUT-OF-KIT #1351 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- env G48B_TITLE_KEY="KS-1386" G48B_SEQUENCED="$W/seq_ok.json" "$R" "$L" "$SP" --dry-run
ctl R3c 0 'DRY RUN COMPLETE' -- cat "$W/R3s.out"
ctl R3w 15 'OVERLAP #1351 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G48B_TITLE_KEY="KS-1386" G48B_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #125[03] ' -- env G48B_WIDEN_RX="-l5-1$" "$R" "$L" "$SP" --dry-run
sed "s/|$H5|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh";                     ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/|$H4|/|$OLD4|/" "$L" > "$W/launcher_superseded.sh"; chmod +x "$W/launcher_superseded.sh";                   ctl R5s 11 'the PINNED head is SUPERSEDED' -- "$R" "$W/launcher_superseded.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1355|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G48B_ROUTING="$W/routing_ok.conf" G48B_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins and the real census are untouched by every control above"
ctl PNZ 0 '' -- test "$(shasum -a 256 "$GS/pins_gate48b.json" | cut -c1-64)" = "$PINSHA"
ctl LCZ 0 '' -- test "$(shasum -a 256 "$GS/lockcensus_gate48b.json" | cut -c1-64)" = "$LCSHA"
echo "SUMMARY gate48b: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
