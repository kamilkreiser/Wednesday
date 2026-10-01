#!/bin/bash
# controls_gate51a.sh — drives every guard in the gate51a kit, on the REAL subject (#1365) and on PLANTED defects. Each control names the rc it
# must give and a WHY pattern its output must carry. A refusal for the wrong reason is a MISMATCH. A check that prints nothing is paired with
# a control that makes it print.
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped, so every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants are synthetic commits in the SCRATCH clone only. They use plumbing (read-tree / update-index / write-tree / commit-tree under a temp
# index), never a worktree and never the checkout, plus files under <scratchpad>/g51a_sp/controls_<HHMMSS>/. The kit's own files are never
# edited. The real pins_gate51a.json, kit.json and the filled prompt are sha256-checked unchanged at the end (PNZ, KJZ, PRZ).
# The launcher runs with --check (headless), except L9: the real launch path with stdin NOT a TTY, which must refuse rc 21 before exec.
# The repin runs --dry-run, except R1 (a real run that must refuse at step 0, routing) and R8 (a real run with a routed temp file that must stop
# at G51A_STOP_AFTER_3B). Both stop long before the usage gate / cockpit.
# Mode plants RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>), because core.filemode is false.
# Each by-name keyword has its own launcher refusal (LK*): the keyword is broken into `<KW>-X`, which the launcher's TOKEN match must NOT accept.
# This is a NEW COPY of gate50b's controls (shape, harness, ssh-retry), re-planted for this kit's spec-annotation PR. gate50b's file is not edited.
# Usage: controls_gate51a.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g51a_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g51a_sp/clone"; L="$GS/launch_qa_secuura_batch1365.sh"; PROMPT="$GS/2026-10-01_secuura-batch1365.prompt.txt"; CAP="$GS/READY_1365_mail.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate51a.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"; H="$(PJ pr_pins.head)"
SHA() { shasum -a 256 "$1" | cut -c1-64; }
PINSHA="$(SHA "$GS/pins_gate51a.json")"; KITSHA="$(SHA "$GS/kit.json")"; PRSHA="$(SHA "$PROMPT")"
Y='Blockchain/Dev/docs/openapi/secuura-api.yaml'; AN='Blockchain/Dev/services/analytics/src/analytics.openapi.ts'
NR='Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts'; TP='Blockchain/Dev/services/tenant-provisioning/src/index.ts'
GD="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["goldens_dir"])' "$GS/kit.json")"
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
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|SPECDIFF|HANDLERS|MODE' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
IDN=0
commitw() { # commitw <tree> <parent> <msg>
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate51a.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate51a.invalid GIT_AUTHOR_DATE=2026-10-01T00:00:00Z GIT_COMMITTER_DATE=2026-10-01T00:00:00Z \
    git -C "$CL" commit-tree "$1" -p "$2" -m "$3"
}
mkdev() { # mkdev <path> <transform> — a develop MOVE plant: a child of develop (for --develop simulations)
  local p="$1" tf="$2" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.dev.$IDN"
  git -C "$CL" show "$DEV:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || return 1
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$DEV"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$DEV" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$DEV" "gate51a control plant: develop move on $p"
}
restack() { # restack <subject head> <path> <transform> — the subject's own tree with ONE more path edited, parent = the subject's parent
  local h="$1" p="$2" tf="$3" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.rs.$IDN"
  git -C "$CL" show "$h:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || { echo "PLANT TRANSFORM FAILED for $p" >&2; return 1; }
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$h" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate51a control plant: $p over $h"
}
remode() { # remode <subject head> <path> <mode> — the subject's own tree with ONE path's RECORDED mode changed
  local h="$1" p="$2" mo="$3" idx tree; IDN=$((IDN + 1)); idx="$W/idx.rm.$IDN"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"; GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mo,$(git -C "$CL" rev-parse "$h:$p"),$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate51a control plant: $p recorded $mo"
}
mut() { # mut <src> <dst> <old> <new> — a literal replacement (python, no shell quoting), refusing when <old> is absent
  python3 -c 'import sys; s=open(sys.argv[1]).read(); assert sys.argv[3] in s, "mut: anchor absent: " + sys.argv[3]; open(sys.argv[2], "w").write(s.replace(sys.argv[3], sys.argv[4]))' "$@"
}
echo "=== controls_gate51a $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1365 $H | END_TREE $END | plants $W"

echo "--- pin_gate51a.py (head, shape, allowed prefixes, the move, alone, the squash, RECORDED modes + control, hook files, the unchanged HANDLER pins) — simulations write pins_gate51a.SIM-<name>.json only"
PN="$GS/pin_gate51a.py"
ctl PN0  0 'PASS: FAIL=0 -> pins_gate51a.SIM-real.json .* 11 paths \+316/-6' -- python3 "$PN" "$SP" --simulate real "1365=$H"
ctl PN0e 0 "END_TREE $END \| git diff --shortstat develop END: 11 files changed, 316 insertions\(\+\), 6 deletions\(-\)" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 12 path\(s\) pinned \(11 PR, 1 control\), 12 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0k 0 'nft.routes.ts: develop 6df435dcb5df .*BYTE-EQUAL in every tree' -- cat "$W/PN0.out"
ctl PN1  1 'REFUSING: --develop is a controls-only override' -- python3 "$PN" "$SP" --develop "$OLDDEV"
PRT="$(restack "$H" "$NR" "s = s + '\n// gate51a control plant: a runtime handler file edited\n'")"
ctl PN2  1 '\(K\) Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts is not byte-equal' -- python3 "$PN" "$SP" --simulate rt "1365=$PRT"
DCF="$(mkdev "$Y" "s = s + '\n'")"
ctl PN3  1 '\(C\) #1365: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate cfl "1365=$H" --develop "$DCF"
M755="$(remode "$H" "$Y" 100755)"
ctl PN4  1 'Blockchain/Dev/docs/openapi/secuura-api.yaml: want 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1365=$M755"
DMV="$(mkdev "Blockchain/Dev/BACKLOG.md" "s = s + '\n<!-- gate51a control plant: an unrelated develop move -->\n'")"
ctl PN5  0 '#1365 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 1 path\(s\) \| reaches its own paths: NONE' -- python3 "$PN" "$SP" --simulate mv "1365=$H" --develop "$DMV"
P3F="$(restack "$H" "Blockchain/Dev/BACKLOG.md" "s = s + ' '")"
ctl PN6  1 "\(B\) paths outside the allowed prefixes \['Blockchain/Dev/BACKLOG.md'\]" -- python3 "$PN" "$SP" --simulate third "1365=$P3F"

echo "--- specdiff_gate51a.py (requirement 1 prediction; the yaml control inside)"
SD="$GS/specdiff_gate51a.py"
ctl SD0  0 'SPECDIFF PASS: 0 FAIL of 7 checks' -- python3 "$SD" "$SP"
ctl SD0r 0 'PASS S2 .*11 `required: true` added \(6 replacements, 5 insertions' -- cat "$W/SD0.out"
ctl SD0g 0 'PASS S4 goldens byte-equal: 10 of 10 non-yaml paths .*yaml control differs: True' -- cat "$W/SD0.out"
ctl SD0y 0 "yaml lines == '        required: true': develop 60, head 71 \(delta 11\)" -- cat "$W/SD0.out"
S1P="$(restack "$H" "$AN" "a = \"summary: 'Generate an analytics report',\"; assert s.count(a) == 1; s = s.replace(a, \"summary: 'Generate an analytics report!',\")")"
ctl SD1  1 "FAIL S2 only .*files where another key moved: \['Blockchain/Dev/services/analytics/src/analytics.openapi.ts'\]" -- python3 "$SD" "$SP" --head "$S1P"
S2P="$(restack "$H" "$Y" "a = 'summary: Estimate mint cost for a chain + tier + metadata size\n      requestBody:\n        required: true'; assert s.count(a) == 1; s = s.replace(a, a[:-4] + 'false')")"
ctl SD2  1 'FAIL S3 yaml' -- python3 "$SD" "$SP" --head "$S2P"
mkdir -p "$W/goldens"; for g in $(python3 -c 'import json,sys; print(" ".join(json.load(open(sys.argv[1]))["goldens"]))' "$GS/kit.json"); do mkdir -p "$W/goldens/$g/out.md.checker"; cp "$GD/$g/out.md.checker/patch.diff" "$W/goldens/$g/out.md.checker/patch.diff"; done
mut "$W/goldens/spark_secuura_2026-10-01_KS-1364-billing/out.md.checker/patch.diff" "$W/goldens/spark_secuura_2026-10-01_KS-1364-billing/out.md.checker/patch.diff" 'no Stripe.' 'no Stripe!'
ctl SD3  1 'FAIL S4 goldens byte-equal: 9 of 10 non-yaml paths' -- python3 "$SD" "$SP" --goldens-dir "$W/goldens"
ctl SD4  1 "FAIL S6 no runtime path: .*\['Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts'\]" -- python3 "$SD" "$SP" --head "$PRT"
ctl SD5  1 'FAIL S1 file set: 0 paths' -- python3 "$SD" "$SP" --head "$DEV"

echo "--- handlers_gate51a.py (requirement 3 prediction; the TENANT-CTL control inside)"
HD="$GS/handlers_gate51a.py"
ctl HD0  0 'HANDLERS PASS: 11 of 11 operations REJECTS-EMPTY at [0-9a-f]{12} \| control TENANT-CTL OK' -- python3 "$HD" "$SP"
ctl HD0c 0 'OK   TENANT-CTL .*required NONE \| ACCEPTS-EMPTY \(want ACCEPTS-EMPTY\)' -- cat "$W/HD0.out"
ctl HD0m 0 'RUNTIME root lock at [0-9a-f]{12}: express 4\.[0-9.]+ \| body-parser 1\.[0-9.]+' -- cat "$W/HD0.out"
H1P="$(restack "$H" "$NR" "a = \"  storageTier: z.nativeEnum(StorageTier),\n  chain: z.enum(['cardano', 'ethereum', 'polygon']),\n\"; assert s.count(a) == 1; s = s.replace(a, \"  storageTier: z.nativeEnum(StorageTier).optional(),\n  chain: z.enum(['cardano', 'ethereum', 'polygon']).optional(),\n\")")"
ctl HD1  1 'FAIL NR2 POST /api/nft/estimate .*required NONE \| ACCEPTS-EMPTY \(want REJECTS-EMPTY\)' -- python3 "$HD" "$SP" --tree "$H1P"
H2P="$(restack "$H" "$NR" "a = 'const validationResult = RecordMintSchema.safeParse(req.body);'; assert s.count(a) == 1; s = s.replace(a, 'const validationResult = { success: true, data: req.body } as any;')")"
ctl HD2  1 'FAIL NR1 POST /api/nft/record: validator .* not within 12 lines' -- python3 "$HD" "$SP" --tree "$H2P"
H3P="$(restack "$H" "$TP" "a = '  name: z.string().trim().min(1).max(255).optional(),'; assert s.count(a) == 1; s = s.replace(a, '  name: z.string().trim().min(1).max(255),')")"
ctl HD3  1 'FAIL TENANT-CTL .*REJECTS-EMPTY \(want ACCEPTS-EMPTY\)' -- python3 "$HD" "$SP" --tree "$H3P"

echo "--- keyscan_gate51a.py (subject, body, live surfaces)"
KS="$GS/keyscan_gate51a.py"; S6="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1365"]["title"])' "$GS/gh_read_1.json")"
ctl KS0  0 'KEYSCAN PASS: 6 checks over 1 PR, 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1  1 'FAIL #1365 S2' -- python3 "$KS" "$SP" --subject "$S6 (#1365)"
ctl KS2  1 'FAIL #1365 S1' -- python3 "$KS" "$SP" --subject "KS-1364: mark eleven bodies required (KS-1015)"
ctl KS3  1 'FAIL #1365 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --subject "${S6}0123"
printf '' > "$W/b_empty.txt";                                    ctl KS4 1 'FAIL #1365 B1 KS-1364' -- python3 "$KS" "$SP" --body-file "$W/b_empty.txt"
printf 'Refs KS-1364\nCloses KS-1364\n' > "$W/b_close.txt";      ctl KS5 1 'FAIL #1365 B2' -- python3 "$KS" "$SP" --body-file "$W/b_close.txt"
printf 'Refs KS-1364\nsee KS-1015\n' > "$W/b_for.txt";           ctl KS6 1 "FAIL #1365 B3: .*foreign \['KS-1015'\]" -- python3 "$KS" "$SP" --body-file "$W/b_for.txt"
printf 'Refs KS-1364\nthe referral lane is KS-1015 outside any fence\n' > "$W/pb.txt"; ctl KS7 0 "OUTSIDE any fence: \['KS-1015'\]" -- python3 "$KS" "$SP" --prbody-file "$W/pb.txt"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L1  6 '#1365 — .* is not at .* AND refs/pull/1365/head' -- env G51A_HEAD_1365="$DEV" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G51A_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1365 — the compare is not the pinned' -- env G51A_PATHS_1365="$Y" "$L" --check
mut "$PROMPT" "$W/p_go.txt" 'GO (Seat B 52nd): merge 1365 on gate51a' 'GO (Seat B 52nd): merge 1364 on gate51a';   ctl L4 26 'merge authority / the GO string' -- env G51A_PROMPT="$W/p_go.txt" "$L" --check
mut "$PROMPT" "$W/p_seat.txt" 'The merge seat is Seat B 52nd' 'The merge seat is Seat B 51st';                   ctl L4b 26 'merge authority / the GO string' -- env G51A_PROMPT="$W/p_seat.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                        ctl L5 8 'unfilled double-brace' -- env G51A_PROMPT="$W/p_tok.txt" "$L" --check
{ cat "$PROMPT"; echo 'merge #<PR>'; } > "$W/p_ph.txt";                                                         ctl L5b 8 'unpinned PR placeholder' -- env G51A_PROMPT="$W/p_ph.txt" "$L" --check
i=0
for kw in PATHS-ELEVEN REQUIRED-ONLY YAML-ELEVEN GOLDENS-BYTE-EQUAL GENERATOR-REPRODUCES CHECK-OPENAPI-RC HANDLER-REJECTS-ABSENT NO-RUNTIME-CHANGE RED-FIRST CONTROLS-GREEN SUITES-BASE-HEAD TSC-NO-REGRESSION SUBJECT-KEY-SCAN SUBJECT-LANDS-AT SUBJECT-TRUE-OF-DIFF REFS-OWN-KEY NO-CLOSING-KEYWORD DEHYPHENATED-KEYS SIX-REMAINING-NAMED NOT-COVERED-HONEST PR-BODY-CLAIMS CLEAN-MERGE END-TREE MODES COLLISION-CENSUS TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  i=$((i + 1)); sed "s/$kw/$kw-X/g" "$PROMPT" > "$W/p_kw$i.txt"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G51A_PROMPT="$W/p_kw$i.txt" "$L" --check
done
mut "$PROMPT" "$W/p_fn.txt" 'ASSERT THE FILENAME TOO' 'assert the content';                                         ctl L6 33 'the filename rule' -- env G51A_PROMPT="$W/p_fn.txt" "$L" --check
sed "s/$H/${H:0:39}x/g" "$CAP" > "$W/cap_noh.md";                                                               ctl L7 20 "do not both name #1365's head" -- env G51A_BRIEF="$W/cap_noh.md" "$L" --check
mut "$PROMPT" "$W/p_h1.txt" 'NO ticket filed' 'NO tickets filed';                                                    ctl L8 39 'the HOLDS' -- env G51A_PROMPT="$W/p_h1.txt" "$L" --check
mut "$PROMPT" "$W/p_h2.txt" 'You NEVER reply to Peter' 'You may reply to Peter';                                     ctl L8b 39 'the HOLDS' -- env G51A_PROMPT="$W/p_h2.txt" "$L" --check
mut "$PROMPT" "$W/p_h3.txt" 'Never read or write a real `.env`' 'Never write a real `.env`';                         ctl L8c 39 'the HOLDS' -- env G51A_PROMPT="$W/p_h3.txt" "$L" --check
mut "$PROMPT" "$W/p_h4.txt" 'Reverts and plants live only in a SCRATCH worktree you created' 'Reverts may live anywhere';  ctl L8d 39 'the HOLDS' -- env G51A_PROMPT="$W/p_h4.txt" "$L" --check
mut "$PROMPT" "$W/p_h7.txt" 'THE NAMED EXCEPTIONS to those holds — these and NO others' 'THE NAMED EXCEPTIONS to those holds'; ctl L8g 39 'the HOLDS' -- env G51A_PROMPT="$W/p_h7.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                            ctl L10 31 'launch develop / the END_TREE' -- env G51A_PROMPT="$W/p_dev.txt" "$L" --check
mut "$PROMPT" "$W/p_tier.txt" '#1365 T2 —' '#1365 T1 —';                                                              ctl L11 7 'the tier line' -- env G51A_PROMPT="$W/p_tier.txt" "$L" --check
mut "$PROMPT" "$W/p_round.txt" 'a round-1 NO GO goes back to the author for round 2' 'a round-1 NO GO ships nothing';  ctl L11b 7 'the tiering rule' -- env G51A_PROMPT="$W/p_round.txt" "$L" --check
mut "$PROMPT" "$W/p_tkt.txt" 'PR #1365 is KS-1364' 'PR #1365 is KS-1365';                                             ctl L12 32 "BOTH state the ticket" -- env G51A_PROMPT="$W/p_tkt.txt" "$L" --check
mut "$PROMPT" "$W/p_a1.txt" 'MG-1 11 over 11 paths' 'MG-1 over the paths';                                            ctl L13 25 'the MERGE ADDENDUM rules' -- env G51A_PROMPT="$W/p_a1.txt" "$L" --check
mut "$PROMPT" "$W/p_a2.txt" 'NOTHING to report.md after you send the verdict mail' 'little to report.md after you send the verdict mail'; ctl L13b 25 'REPORT-HASH-LAST' -- env G51A_PROMPT="$W/p_a2.txt" "$L" --check
mut "$PROMPT" "$W/p_a3.txt" 'HANDLERS 11 of 11 reject an absent body' 'HANDLERS checked';                             ctl L13c 25 'the MERGE ADDENDUM rules' -- env G51A_PROMPT="$W/p_a3.txt" "$L" --check
mut "$PROMPT" "$W/p_subj.txt" 'GATE51A #1365' 'GATE51A #1364';                                                        ctl L14 23 'the verdict subject' -- env G51A_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                         ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
mut "$PROMPT" "$W/p_k1.txt" "$GS/handlers_1.out" "$GS/handlers_elsewhere.out";                                         ctl L16 8 'handlers_1.out is missing, empty, or not named' -- env G51A_PROMPT="$W/p_k1.txt" "$L" --check
mut "$PROMPT" "$W/p_k2.txt" "$GS/READY_1365_CORRECTION_mail.md" "$GS/READY_elsewhere.md";                              ctl L17 8 'READY_1365_CORRECTION_mail.md is missing, empty, or not named' -- env G51A_PROMPT="$W/p_k2.txt" "$L" --check
mut "$PROMPT" "$W/p_k3.txt" '2026-10-01-batch1364-g50b/report.md' '2026-10-01-batch1363-g50a/report.md';              ctl L18 8 'the previous round report' -- env G51A_PROMPT="$W/p_k3.txt" "$L" --check
mut "$PROMPT" "$W/p_x1.txt" 'No live server is started, no Schemathesis is run, and no image is built in this gate' 'A live server may be started'; ctl L20 34 'the NO-RUNTIME rule' -- env G51A_PROMPT="$W/p_x1.txt" "$L" --check
mut "$PROMPT" "$W/p_x2.txt" 'A HANDLER THAT ACCEPTS AN ABSENT BODY IS A MAJOR' 'A HANDLER THAT ACCEPTS AN ABSENT BODY IS A NOTE';  ctl L21 36 'the RUNTIME-TRUTH rule' -- env G51A_PROMPT="$W/p_x2.txt" "$L" --check
mut "$PROMPT" "$W/p_x2b.txt" 'never from memory' 'from memory if need be';                                          ctl L21b 36 'the RUNTIME-TRUTH rule' -- env G51A_PROMPT="$W/p_x2b.txt" "$L" --check
mut "$PROMPT" "$W/p_x3.txt" 'You change no ticket state' 'You may move KS-1364 back';                               ctl L22 37 "the NOT-THE-GATE'S items" -- env G51A_PROMPT="$W/p_x3.txt" "$L" --check
mut "$PROMPT" "$W/p_x4.txt" 'is at 87%' 'is fine';                                                                    ctl L23 38 'the proportionality line' -- env G51A_PROMPT="$W/p_x4.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate51a.sh"
ctl R0  0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key outside reported_overlaps \| 0 expected overlap\(s\) reported \| 0 sequenced by Wednesday .*2 client-human PR\(s\) reported \| 11 kit path\(s\), 1 kit key\(s\)' -- cat "$W/R0.out"
ctl R0h 0 'CLIENT-HUMAN \(reported, never sequenced by a gate\) #1360 by PeterObeden' -- cat "$W/R0.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pin, 1 of 1' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                                ctl R1 1 'is not registered in inbox_routing.conf' -- env G51A_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2  15 "OVERLAP #1360 .*paths \[.*'Blockchain/Dev/package-lock.json'" -- env G51A_OVERLAP_EXTRA="Blockchain/Dev/package-lock.json" "$R" "$L" "$SP" --dry-run
ctl R3  15 "OVERLAP #1360 .*title keys \['KS-1380'\]" -- env G51A_TITLE_KEY="KS-1380" "$R" "$L" "$SP" --dry-run
printf '{"1360": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H60" > "$W/seq_ok.json"
printf '{"1360": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$H" > "$W/seq_bad.json"
ctl R3s 0 'SEQUENCED OUT-OF-KIT #1360 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- env G51A_TITLE_KEY="KS-1380" G51A_SEQUENCED="$W/seq_ok.json" "$R" "$L" "$SP" --dry-run
ctl R3w 15 'OVERLAP #1360 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G51A_TITLE_KEY="KS-1380" G51A_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #1360 ' -- env G51A_WIDEN_RX="ks-1380-revert-pr-1358$" "$R" "$L" "$SP" --dry-run
sed "s/|$H|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh";                      ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1365|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G51A_ROUTING="$W/routing_ok.conf" G51A_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins, kit.json and the filled prompt are untouched by every control above"
ctl PNZ 0 '' -- test "$(SHA "$GS/pins_gate51a.json")" = "$PINSHA"
ctl KJZ 0 '' -- test "$(SHA "$GS/kit.json")" = "$KITSHA"
ctl PRZ 0 '' -- test "$(SHA "$PROMPT")" = "$PRSHA"
echo "SUMMARY gate51a: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
