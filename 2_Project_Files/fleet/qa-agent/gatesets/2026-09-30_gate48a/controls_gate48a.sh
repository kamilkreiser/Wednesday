#!/bin/bash
# controls_gate48a.sh — every guard in the gate48a kit driven on the REAL subject and on PLANTED defects, each with the rc it must give and a WHY
# pattern its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a control that makes it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g48a_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate48a.json and lockcensus_gate48a.json are sha256-checked unchanged at the end (PNZ, LCZ). The launcher runs with --check (headless)
# except L9, the real launch path with stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run that must
# refuse at step 0, routing) and R8 (a real run with a routed temp file that must stop at G48A_STOP_AFTER_3B) — both stop long before the usage
# gate / cockpit. Mode plants RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>): core.filemode is false, a disk chmod proves nothing.
# Each by-name keyword has its own launcher refusal (LK*): the keyword is broken into `<KW>-X`, which the launcher's TOKEN match must NOT accept.
# Shape copied from the gate47 controls, cut to ONE PR, plus the lock / baseline / census instruments of this kit.
# Usage: controls_gate48a.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g48a_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g48a_sp/clone"; L="$GS/launch_qa_secuura_batch1354.sh"; PROMPT="$GS/2026-09-30_secuura-batch1354.prompt.txt"; CAP="$GS/mail_gate48a_ready.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate48a.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"; H="$(PJ prs.1354.head)"
PINSHA="$(shasum -a 256 "$GS/pins_gate48a.json" | cut -c1-64)"; LCSHA="$(shasum -a 256 "$GS/lockcensus_gate48a.json" | cut -c1-64)"
LOCK='systemTest/performance/package-lock.json'; BL='Blockchain/Dev/scripts/audit/audit-baseline.json'; CT='Blockchain/Dev/scripts/audit/baseline-contract.mjs'
H51="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["census"]["1351"]["head"])' "$GS/gh_read_1.json")"
TOT=0; OK=0; MM=0; RETRIES=0
ctl() { # ctl <id> <expected rc> <why regex or ''> -- <command...>
  local id="$1" exp="$2" why="$3"; shift 4
  local out rc good try=0; out="$("$@" 2>&1)"; rc=$?
  # GitHub intermittently DENIES the Secuura deploy key's SSH auth under a burst of ls-remote / fetch (gate47, measured 2026-09-29T14:51Z). The
  # GUARDS fail closed on it (rc 2 / REFUSING), which is right; the HARNESS retries such a run up to 3 times, 20 s apart, and counts every retry.
  while [ "$try" -lt 3 ] && printf '%s' "$out" | grep -qE 'Permission denied \(publickey\)|Could not read from remote repository'; do
    try=$((try + 1)); RETRIES=$((RETRIES + 1)); sleep 20; out="$("$@" 2>&1)"; rc=$?
  done
  printf '%s\n' "$out" > "$W/$id.out"
  good=0; [ "$rc" = "$exp" ] && { [ -z "$why" ] || printf '%s' "$out" | grep -qE -- "$why"; } && good=1
  [ "$INV" = 1 ] && good=$((1 - good))
  TOT=$((TOT + 1)); if [ "$good" = 1 ]; then OK=$((OK + 1)); v=OK; else MM=$((MM + 1)); v=MISMATCH; fi
  local shown=''; if [ -n "$why" ]; then shown="$(printf '%s' "$out" | grep -E -- "$why" | tail -1)"; fi
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|LOCKDIFF|BASELINE|CENSUS|MODE' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
mkcommit() { # mkcommit <parent> <path> <python transform of s (the blob text)> [<recorded mode override>] -> prints the new commit sha (scratch clone only)
  local par="$1" p="$2" tf="$3" mo="${4:-}" idx="$W/idx.$(date +%s).$RANDOM" nb tree mode
  git -C "$CL" show "$par:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || { echo "PLANT TRANSFORM FAILED for $p" >&2; return 1; }
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"
  mode="${mo:-$(git -C "$CL" ls-tree "$par" -- "$p" | awk '{print $1}')}"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$par"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mode,$nb,$p"
  tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"   # the temp index stays in $W (never deleted)
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate48a.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate48a.invalid GIT_AUTHOR_DATE=2026-09-30T00:00:00Z GIT_COMMITTER_DATE=2026-09-30T00:00:00Z \
    git -C "$CL" commit-tree "$tree" -p "$par" -m "gate48a control plant: $p${mo:+ recorded $mo}"
}
mut() { # mut <src> <dst> <old> <new> — a literal replacement (python, no shell quoting), refusing when <old> is absent
  python3 -c 'import sys; s=open(sys.argv[1]).read(); assert sys.argv[3] in s, "mut: anchor absent: " + sys.argv[3]; open(sys.argv[2], "w").write(s.replace(sys.argv[3], sys.argv[4]))' "$@"
}
echo "=== controls_gate48a $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1354 head $H | END_TREE $END | plants $W"

echo "--- pin_gate48a.py (heads, shape, the move, alone, the squash, END, RECORDED modes + control, the hook, the contract) — simulations write pins_gate48a.SIM-<name>.json only"
PN="$GS/pin_gate48a.py"
ctl PN0  0 'PASS: FAIL=0 -> pins_gate48a.SIM-real.json' -- python3 "$PN" "$SP" --simulate real ""
ctl PN0e 0 "END_TREE $END \| diff\(develop, END\): 2 path\(s\) == the own paths \(2\): True" -- cat "$W/PN0.out"
ctl PN0t 0 "END_TREE == the head's own tree [0-9a-f]{12}: True" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 3 path\(s\) pinned \(2 PR, 1 control\), 3 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0k 0 'baseline-contract.mjs: develop 2504d9a28dc0 .*BYTE-EQUAL at develop, head and END' -- cat "$W/PN0.out"
ctl PN0h 0 '\.githooks/pre-push: .*IDENTICAL in every tree' -- cat "$W/PN0.out"
ctl PN1  1 '\(A\) #1354 head .* != the expected \(pinned\) head' -- python3 "$PN" "$SP" --expect-head "1354=$DEV"
ctl PN1d 1 'REFUSING: --develop is a controls-only override' -- python3 "$PN" "$SP" --develop "$OLDDEV"
PCT="$(mkcommit "$H" "$CT" "s = s + '// gate48a control plant: the contract edited\n'")"
ctl PN2  1 '\(K\) Blockchain/Dev/scripts/audit/baseline-contract.mjs is not byte-equal' -- python3 "$PN" "$SP" --simulate ct "1354=$PCT"
# PN3: develop moves ON the baseline row the head's insertion sits beside — the move reaches the PR's own path (and may conflict).
DCF="$(mkcommit "$DEV" "$BL" "a = '\"decidedAt\": \"2026-07-19\"\n    },\n    \"GHSA-v9p9-hfj2-hcw8\"'; assert s.count(a) == 1, s.count(a); s = s.replace(a, a.replace('2026-07-19', '2026-07-18'))")"
ctl PN3  1 '\(C\) #1354: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate cfl "1354=$H" --develop "$DCF"
M755="$(mkcommit "$H" "$BL" "pass" 100755)"
ctl PN4  1 '#1354 Blockchain/Dev/scripts/audit/audit-baseline.json: want 100644 \| head 100755 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1354=$M755"
# PN5: develop moves on an UNRELATED path — clean, and the END == head-tree line must now read False (the equality line can print False).
DMV="$(mkcommit "$DEV" "Blockchain/Dev/BACKLOG.md" "s = s + '\n<!-- gate48a control plant: an unrelated develop move -->\n'")"
ctl PN5  0 "END_TREE == the head's own tree [0-9a-f]{12}: False" -- python3 "$PN" "$SP" --simulate mv "1354=$H" --develop "$DMV"
ctl PN5c 0 '#1354 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 1 path\(s\) \| reaches its own paths: NONE' -- cat "$W/PN5.out"

echo "--- lockdiff_gate48a.py (LOCK-DIFF-ONE-ENTRY / JSYAML-OUT-OF-RANGE predictions)"
LDP="$GS/lockdiff_gate48a.py"
ctl LD0  0 'LOCKDIFF PASS: 0 FAIL' -- python3 "$LDP" "$SP"
ctl LD0m 0 'entries 274 -> 274 \| MOVED=1 .*ADDED=0 .*REMOVED=0 .*OTHER \(non-version field changes\)=0' -- cat "$W/LD0.out"
ctl LD0r 0 'PASS L6c: CONTROL: the base pin 5.2.3 IS inside' -- cat "$W/LD0.out"
P2M="$(mkcommit "$H" "$LOCK" "import re; m = [x for x in re.finditer(r'\n        \"(node_modules/[^\"]+)\": \{\n            \"version\": \"([^\"]+)\"', s) if x.group(1) != 'node_modules/js-yaml'][0]; s = s[:m.start(2)] + m.group(2) + '-g48a' + s[m.end(2):]")"
ctl LD1  1 'MOVED=2 .*FAIL L2|FAIL L2: exactly ONE entry' -- python3 "$LDP" "$SP" --head "$P2M" --offline
ctl LD1m 0 'MOVED=2' -- cat "$W/LD1.out"
PIN="$(mkcommit "$H" "$LOCK" "a = 'sha512-m+aqu+LwO1O6'; assert s.count(a) == 1; s = s.replace(a, 'sha512-M+aqu+LwO1O6')")"
ctl LD2  1 'FAIL L5: head resolved/integrity == registry' -- python3 "$LDP" "$SP" --head "$PIN"
PLK="$(mkcommit "$H" "$LOCK" "a = '\"resolved\": \"../../observability\"'; assert s.count(a) == 1; s = s.replace(a, '\"resolved\": \"../../observability-g48a\"')")"
ctl LD3  1 'FAIL L4: 1 link / secuura-observability entr' -- python3 "$LDP" "$SP" --head "$PLK" --offline
PLV="$(mkcommit "$H" "$LOCK" "a = '\"lockfileVersion\": 3'; assert s.count(a) == 1; s = s.replace(a, '\"lockfileVersion\": 2')")"
ctl LD4  1 'FAIL L1: lockfileVersion 3 -> 2' -- python3 "$LDP" "$SP" --head "$PLV" --offline
PRG="$(mkcommit "$H" "$LOCK" "a = '\"version\": \"5.4.2\",\n            \"resolved\": \"https://registry.npmjs.org/js-yaml/-/js-yaml-5.4.2.tgz\"'; assert s.count(a) == 1; s = s.replace(a, a.replace('5.4.2', '5.3.0'))")"
ctl LD5  1 'FAIL L6: the head pin 5.3.0 is OUTSIDE every vulnerable range' -- python3 "$LDP" "$SP" --head "$PRG"

echo "--- baseline_gate48a.py (BASELINE-ROW-FIELDS / CONTRACT / FUSE-COUNT predictions)"
BLP="$GS/baseline_gate48a.py"; NEWTAIL='"decidedAt": "2026-09-30",\n      "expires": "2026-10-09"'
ctl BL0  0 'BASELINE PASS: 0 FAIL \| FUSE-COUNT 5 row\(s\) expire 2026-10-09 at the head \(base 4\) \| GRANDFATHERED 17 == no-expiry 17' -- python3 "$BLP" "$SP"
ctl BL0b 0 'PASS B3: git diff --numstat 7 0 \| -U0: 7 `\+` line\(s\), 0 `-` line\(s\)' -- cat "$W/BL0.out"
PEX="$(mkcommit "$H" "$BL" "a = '$NEWTAIL'; assert s.count(a) == 1; s = s.replace(a, a.replace('2026-10-09', '2026-10-10'))")"
ctl BL1  1 "FAIL B4: .*expires '2026-10-10' \(want '2026-10-09'\)" -- python3 "$BLP" "$SP" --head "$PEX"
ctl BL1f 0 'FAIL B6: FUSE-COUNT at the head: 4 row' -- cat "$W/BL1.out"
POR="$(mkcommit "$H" "$BL" "a = '\"decidedAt\": \"2026-07-19\"'; assert s.count(a) >= 1; s = s.replace(a, '\"decidedAt\": \"2026-07-20\"', 1)")"
ctl BL2  1 'FAIL B2: exactly one row added' -- python3 "$BLP" "$SP" --head "$POR"
ctl BL2b 0 'FAIL B3: git diff --numstat 8 1' -- cat "$W/BL2.out"
PNE="$(mkcommit "$H" "$BL" "a = '$NEWTAIL'; assert s.count(a) == 1; s = s.replace(a, '\"decidedAt\": \"2026-09-30\"')")"
ctl BL3  1 'FAIL B5: .*GRANDFATHERED_NO_EXPIRY 17 ids == the 18 head rows with NO expires: False' -- python3 "$BLP" "$SP" --head "$PNE"
PTK="$(mkcommit "$H" "$BL" "a = '\"ticket\": \"KS-470\",\n      $NEWTAIL'; assert s.count(a) == 1; s = s.replace(a, a.replace('KS-470', 'KS-471'))")"
ctl BL4  1 "FAIL B4: .*ticket 'KS-471'" -- python3 "$BLP" "$SP" --head "$PTK"
ctl BLCT 1 'FAIL B5: contract blob base [0-9a-f]{12} == head [0-9a-f]{12}: False' -- python3 "$BLP" "$SP" --head "$PCT"

echo "--- lockcensus_gate48a.py (CLAUSE2 / EXCEPTION READ; controls CT-PARSE / CT-POS / CT-NEG inside)"
LCP="$GS/lockcensus_gate48a.py"
ctl LC0  0 'CENSUS DONE: 45 lock\(s\), 17 undici/js-yaml entr\(y/ies\), 3 vulnerable' -- python3 "$LCP" "$SP"
ctl LC0x 0 'VULNERABLE in a lock whose dir has an image / app class .*frontend/issuer/package-lock.json undici 5.29.0 \[DOCKERFILE-IN-DIR; COPIED-BY Blockchain/Dev/frontend/issuer/Dockerfile\]' -- cat "$W/LC0.out"
ctl LC1  0 'VUL js-yaml +5.2.3 +dev=False +systemTest/performance/package-lock.json' -- python3 "$LCP" "$SP" --tree "$DEV" --offline
ctl LC1n 0 'CENSUS DONE: 45 lock\(s\), 17 undici/js-yaml entr\(y/ies\), 4 vulnerable' -- cat "$W/LC1.out"
ctl LC2  0 'ranges READ \(OFFLINE fallback, not read\)' -- cat "$W/LC1.out"

echo "--- keyscan_gate48a.py (subject, body, live-surface FLAGs)"
KS="$GS/keyscan_gate48a.py"; S="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1354"]["subject"])' "$GS/kit.json")"
ctl KS0  0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL, 0 FLAG' -- python3 "$KS" "$SP"
ctl KS1  1 'FAIL #1354 S2' -- python3 "$KS" "$SP" --subject "$S (#1354)"
ctl KS2  1 'FAIL #1354 S1' -- python3 "$KS" "$SP" --subject "KS-470: js-yaml 5.4.2 in systemTest/performance (KS-1054)"
ctl KS3  1 'FAIL #1354 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --subject "${S}0123"
ctl KS3b 1 "FAIL #1354 S1: subject keys \['KS-4700'\]" -- python3 "$KS" "$SP" --subject "KS-4700: js-yaml 5.4.2 in systemTest/performance"
printf '' > "$W/b_empty.txt";                                  ctl KS4 1 'FAIL #1354 B1 KS-470' -- python3 "$KS" "$SP" --body-file "$W/b_empty.txt"
printf 'Refs KS-470\nCloses KS-470\n' > "$W/b_close.txt";       ctl KS5 1 'FAIL #1354 B2' -- python3 "$KS" "$SP" --body-file "$W/b_close.txt"
printf 'Refs KS-470\nsee the KS-1054 predicate\n' > "$W/b_for.txt"; ctl KS6 1 "FAIL #1354 B3: .*foreign \['KS-1054'\]" -- python3 "$KS" "$SP" --body-file "$W/b_for.txt"
printf 'KS-470 continues the KS-1378 class\n' > "$W/pb.txt";     ctl KS7 0 "FLAG #1354 PR body: .*FOREIGN \['KS-1378'\]" -- python3 "$KS" "$SP" --prbody-file "$W/pb.txt"
# KS8: a subject that is FALSE of the diff (#1354 DOES add a baseline row) still PASSES the key scan — truth is SUBJECT-TRUE-OF-DIFF, the gate's.
ctl KS8  0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL' -- python3 "$KS" "$SP" --subject "KS-470: js-yaml 5.4.2 in systemTest/performance, no baseline row added"
ctl KS9  0 'INFO #1354 PR title == declared subject: True .*commit subject == title: True' -- cat "$W/KS0.out"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L1  6 '#1354 — .* is not at .* AND refs/pull/1354/head' -- env G48A_HEAD_1354="$DEV" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G48A_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1354 — the compare is not the pinned' -- env G48A_PATHS_1354="Blockchain/Dev/scripts/audit/audit-baseline.json" "$L" --check
mut "$PROMPT" "$W/p_go.txt" 'GO (Seat B 47th): merge 1354 on gate48a' 'GO (Seat B 46th): merge 1354 on gate48a';       ctl L4 26 'merge authority / the GO string' -- env G48A_PROMPT="$W/p_go.txt" "$L" --check
mut "$PROMPT" "$W/p_seat.txt" 'The merge seat is Seat B 47th' 'The merge seat is Seat B 48th';                     ctl L4b 26 'merge authority / the GO string' -- env G48A_PROMPT="$W/p_seat.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                          ctl L5 8 'unfilled double-brace' -- env G48A_PROMPT="$W/p_tok.txt" "$L" --check
i=0
for kw in LOCK-DIFF-ONE-ENTRY JSYAML-OUT-OF-RANGE BASELINE-ROW-FIELDS CONTRACT-BYTE-EQUAL FUSE-COUNT AUDIT-GATES-HEAD-END CLAUSE2-REMEASURE EXCEPTION-CHECKED GRANT-CLAUSES REASON-TEXT-TRUE DRAFTED-TICKETS-CHECKED CLEAN-MERGE END-TREE MODES OUT-OF-KIT-CENSUS SUBJECT-KEY-SCAN SUBJECT-LANDS-AT SUBJECT-TRUE-OF-DIFF REFS-OWN-KEY NO-CLOSING-KEYWORD PR-BODY-CLAIMS TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  i=$((i + 1)); sed "s/$kw/$kw-X/g" "$PROMPT" > "$W/p_kw$i.txt"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G48A_PROMPT="$W/p_kw$i.txt" "$L" --check
done
sed "s/$H/${H:0:39}x/g" "$CAP" > "$W/cap_noh.md";                                                                   ctl L7 20 "do not both name #1354's head" -- env G48A_BRIEF="$W/cap_noh.md" "$L" --check
mut "$PROMPT" "$W/p_h1.txt" 'NO ticket filed' 'NO tickets filed';                                                    ctl L8 39 'the HOLDS' -- env G48A_PROMPT="$W/p_h1.txt" "$L" --check
mut "$PROMPT" "$W/p_h2.txt" 'You NEVER reply to Peter' 'You may reply to Peter';                                     ctl L8b 39 'the HOLDS' -- env G48A_PROMPT="$W/p_h2.txt" "$L" --check
mut "$PROMPT" "$W/p_h3.txt" 'Never read or write a real `.env`' 'Never write a real `.env`';                         ctl L8c 39 'the HOLDS' -- env G48A_PROMPT="$W/p_h3.txt" "$L" --check
mut "$PROMPT" "$W/p_h4.txt" 'Docker runs are `--rm --network none` with the source mounted READ-ONLY' 'Docker runs are `--rm`'; ctl L8d 39 'the HOLDS' -- env G48A_PROMPT="$W/p_h4.txt" "$L" --check
mut "$PROMPT" "$W/p_h5.txt" 'No `az` command of any kind' 'No `az login`';                                          ctl L8e 39 'the HOLDS' -- env G48A_PROMPT="$W/p_h5.txt" "$L" --check
mut "$PROMPT" "$W/p_h6.txt" 'NO checklist tick' 'NO early checklist tick';                                           ctl L8f 39 'the HOLDS' -- env G48A_PROMPT="$W/p_h6.txt" "$L" --check
mut "$PROMPT" "$W/p_h7.txt" 'THE NAMED EXCEPTIONS to those holds — these and NO others' 'THE NAMED EXCEPTIONS to those holds'; ctl L8g 39 'the HOLDS' -- env G48A_PROMPT="$W/p_h7.txt" "$L" --check
mut "$PROMPT" "$W/p_h8.txt" 'NEVER `up`, `down`' '`up`, `down`';                                                     ctl L8h 39 'the HOLDS' -- env G48A_PROMPT="$W/p_h8.txt" "$L" --check
mut "$PROMPT" "$W/p_h9.txt" '"no lock regenerated" means no REAL lock' '"no lock regenerated" means little';        ctl L8i 39 'the HOLDS' -- env G48A_PROMPT="$W/p_h9.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                            ctl L10 31 'launch develop / the END_TREE' -- env G48A_PROMPT="$W/p_dev.txt" "$L" --check
mut "$PROMPT" "$W/p_tier.txt" '#1354 T2 —' '#1354 T3 —';                                                              ctl L11 7 'the tier lines' -- env G48A_PROMPT="$W/p_tier.txt" "$L" --check
mut "$PROMPT" "$W/p_round.txt" 'a round-1 NO GO goes back to the author for round 2' 'a round-1 NO GO ships nothing';  ctl L11b 7 'the tiering rule' -- env G48A_PROMPT="$W/p_round.txt" "$L" --check
mut "$PROMPT" "$W/p_tkt.txt" 'PR #1354 is KS-470' 'PR #1354 is KS-471';                                               ctl L12 32 "BOTH state 'PR #1354 is KS-470'" -- env G48A_PROMPT="$W/p_tkt.txt" "$L" --check
mut "$PROMPT" "$W/p_a1.txt" 'MG-1 2 over 2 paths' 'MG-1 over the paths';                                              ctl L13 25 'the MERGE ADDENDUM rules' -- env G48A_PROMPT="$W/p_a1.txt" "$L" --check
mut "$PROMPT" "$W/p_a2.txt" 'NOTHING to report.md after you send the verdict mail' 'little to report.md after you send the verdict mail'; ctl L13b 25 'REPORT-HASH-LAST' -- env G48A_PROMPT="$W/p_a2.txt" "$L" --check
mut "$PROMPT" "$W/p_a3.txt" 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' 'EVERY SUBJECT YOU PROPOSE SHOULD FIT THE DIFF'; ctl L13c 25 'the MERGE ADDENDUM rules' -- env G48A_PROMPT="$W/p_a3.txt" "$L" --check
mut "$PROMPT" "$W/p_a4.txt" 'FUSE 2026-10-09 rows at END' 'FUSE rows';                                               ctl L13d 25 'the MERGE ADDENDUM rules' -- env G48A_PROMPT="$W/p_a4.txt" "$L" --check
mut "$PROMPT" "$W/p_a5.txt" 'CONTRACT baseline-contract.mjs == base blob' 'CONTRACT unchanged';                     ctl L13e 25 'the MERGE ADDENDUM rules' -- env G48A_PROMPT="$W/p_a5.txt" "$L" --check
mut "$PROMPT" "$W/p_subj.txt" 'GATE48A #1354' 'GATE48 #1354';                                                         ctl L14 23 'the verdict subject' -- env G48A_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                         ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
mut "$PROMPT" "$W/p_k1.txt" "$GS/drafted_texts_gate48a.md" "$GS/drafted_elsewhere.md";                                 ctl L16 8 'drafted_texts_gate48a.md is missing, empty, or not named' -- env G48A_PROMPT="$W/p_k1.txt" "$L" --check
mut "$PROMPT" "$W/p_k2.txt" "$GS/row_reason_gate48a.md" "$GS/row_elsewhere.md";                                       ctl L17 8 'row_reason_gate48a.md is missing, empty, or not named' -- env G48A_PROMPT="$W/p_k2.txt" "$L" --check
mut "$PROMPT" "$W/p_k3.txt" '2026-09-30-batch1349-g47/report.md' '2026-09-29-batch1348r2-g46/report.md';              ctl L18 8 'the previous round report' -- env G48A_PROMPT="$W/p_k3.txt" "$L" --check
mut "$PROMPT" "$W/p_k4.txt" "$GS/lockcensus_1.out" "$GS/lockcensus_elsewhere.out";                                     ctl L19 8 'lockcensus_1.out is missing, empty, or not named' -- env G48A_PROMPT="$W/p_k4.txt" "$L" --check
mut "$PROMPT" "$W/p_x1.txt" 'If the exception fires, the verdict is NO GO and you say so FIRST' 'If the exception fires, the verdict is NO GO';  ctl L20 34 'the EXCEPTION-FIRST rule' -- env G48A_PROMPT="$W/p_x1.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate48a.sh"
ctl R0  0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key \| 0 sequenced by Wednesday .*3 client-human PR\(s\) reported \| 2 kit path\(s\), 3 kit key\(s\)' -- cat "$W/R0.out"
ctl R0h 0 'CLIENT-HUMAN \(reported, never sequenced by a gate\) #1351 by PeterObeden' -- cat "$W/R0.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pins, 1 of 1' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                                ctl R1 1 'is not registered in inbox_routing.conf' -- env G48A_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2  15 'OVERLAP #[0-9]+ .*paths \[.Blockchain/Dev/package-lock.json.\]' -- env G48A_OVERLAP_EXTRA="Blockchain/Dev/package-lock.json" "$R" "$L" "$SP" --dry-run
ctl R3  15 'OVERLAP #1351 .*title keys \[.KS-1386.\]' -- env G48A_TITLE_KEY="KS-1386" "$R" "$L" "$SP" --dry-run
# R3s / R3w: a controls-only stand-in for Wednesday's sequencing of a CLIENT HUMAN's PR (#1351 at its current head): reported, not refused; a wrong head refuses.
printf '{"1351": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H51" > "$W/seq_ok.json"
printf '{"1351": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$H" > "$W/seq_bad.json"
ctl R3s 0 'SEQUENCED OUT-OF-KIT #1351 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- env G48A_TITLE_KEY="KS-1386" G48A_SEQUENCED="$W/seq_ok.json" "$R" "$L" "$SP" --dry-run
ctl R3c 0 'DRY RUN COMPLETE' -- cat "$W/R3s.out"
ctl R3w 15 'OVERLAP #1351 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G48A_TITLE_KEY="KS-1386" G48A_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #[0-9]+ dependabot' -- env G48A_WIDEN_RX="^dependabot/" "$R" "$L" "$SP" --dry-run
sed "s/|$H|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh";                      ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1354|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G48A_ROUTING="$W/routing_ok.conf" G48A_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins and the real census are untouched by every control above"
ctl PNZ 0 '' -- test "$(shasum -a 256 "$GS/pins_gate48a.json" | cut -c1-64)" = "$PINSHA"
ctl LCZ 0 '' -- test "$(shasum -a 256 "$GS/lockcensus_gate48a.json" | cut -c1-64)" = "$LCSHA"
echo "SUMMARY gate48a: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
