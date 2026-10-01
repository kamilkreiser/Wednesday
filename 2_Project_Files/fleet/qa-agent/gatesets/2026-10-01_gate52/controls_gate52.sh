#!/bin/bash
# controls_gate52.sh — drives every guard in the gate52 kit, on the REAL subjects (#1367, #1368) and on PLANTED defects. Each control names the rc it
# must give and a WHY pattern its output must carry. A refusal for the wrong reason is a MISMATCH. A check that prints nothing is paired with
# a control that makes it print.
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped, so every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants are synthetic commits in the SCRATCH clone only. They use plumbing (read-tree / update-index / write-tree / commit-tree under a temp
# index), never a worktree and never the checkout, plus files under <scratchpad>/g52_sp/controls_<HHMMSS>/. The kit's own files are never
# edited. The real pins_gate52.json, kit.json and the filled prompt are sha256-checked unchanged at the end (PNZ, KJZ, PRZ).
# The launcher runs with --check (headless), except L9: the real launch path with stdin NOT a TTY, which must refuse rc 21 before exec.
# The repin runs --dry-run, except R1 (a real run that must refuse at step 0, routing) and R8 (a real run with a routed temp file that must stop
# at G52_STOP_AFTER_3B). Both stop long before the usage gate / cockpit.
# Mode plants RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>), because core.filemode is false.
# Each by-name keyword has its own launcher refusal (LK*): the keyword is broken into `<KW>-X`, which the launcher's TOKEN match must NOT accept.
# This is a NEW COPY of gate51a's controls (shape, harness, ssh-retry), re-planted for this kit's two sibling PRs. gate51a's file is not edited.
# Usage: controls_gate52.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g52_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g52_sp/clone"; L="$GS/launch_qa_secuura_batch1367.sh"; PROMPT="$GS/2026-10-01_secuura-batch1367.prompt.txt"; CAP="$GS/READY_1367_1368_mail.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate52.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; EA="$(PJ end_tree_a)"; EB="$(PJ end_tree_b)"; HA="$(PJ pr_pins.1367.head)"; HB="$(PJ pr_pins.1368.head)"
DEVTREE="$(git -C "$CL" rev-parse "$DEV^{tree}")"
SHA() { shasum -a 256 "$1" | cut -c1-64; }
PINSHA="$(SHA "$GS/pins_gate52.json")"; KITSHA="$(SHA "$GS/kit.json")"; PRSHA="$(SHA "$PROMPT")"
Y='Blockchain/Dev/docs/openapi/secuura-api.yaml'; SV='Blockchain/Dev/services'
RO="$SV/referral/src/referral.openapi.ts"; RR="$SV/referral/src/routes/referrals.ts"; TO="$SV/tenant-provisioning/src/tenant-provisioning.openapi.ts"
TI="$SV/tenant-provisioning/src/index.ts"; VV="$SV/originate/src/routes/verificationV2.ts"
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
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|SPECDIFF|HANDLERS|MODE|ENDTREE' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
IDN=0
commitw() { # commitw <tree> <parent> <msg>
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate52.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate52.invalid GIT_AUTHOR_DATE=2026-10-01T00:00:00Z GIT_COMMITTER_DATE=2026-10-01T00:00:00Z \
    git -C "$CL" commit-tree "$1" -p "$2" -m "$3"
}
mkdev() { # mkdev <path> <transform> — a develop MOVE plant: a child of develop (for --develop simulations)
  local p="$1" tf="$2" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.dev.$IDN"
  git -C "$CL" show "$DEV:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || return 1
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$DEV"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$DEV" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$DEV" "gate52 control plant: develop move on $p"
}
restack() { # restack <subject head> <path> <transform> — the subject's own tree with ONE more path edited, parent = the subject's parent
  local h="$1" p="$2" tf="$3" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.rs.$IDN"
  git -C "$CL" show "$h:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || { echo "PLANT TRANSFORM FAILED for $p" >&2; return 1; }
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$h" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate52 control plant: $p over $h"
}
remode() { # remode <subject head> <path> <mode> — the subject's own tree with ONE path's RECORDED mode changed
  local h="$1" p="$2" mo="$3" idx tree; IDN=$((IDN + 1)); idx="$W/idx.rm.$IDN"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"; GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mo,$(git -C "$CL" rev-parse "$h:$p"),$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate52 control plant: $p recorded $mo"
}
mut() { # mut <src> <dst> <old> <new> — a literal replacement (python, no shell quoting), refusing when <old> is absent
  python3 -c 'import sys; s=open(sys.argv[1]).read(); assert sys.argv[3] in s, "mut: anchor absent: " + sys.argv[3]; open(sys.argv[2], "w").write(s.replace(sys.argv[3], sys.argv[4]))' "$@"
}
echo "=== controls_gate52 $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1367 $HA | #1368 $HB | END_TREE_A $EA | END_TREE_B $EB | plants $W"

echo "--- pin_gate52.py (heads, shape, siblings, the move, each alone, the chain, RECORDED modes + control, hook files, the unchanged pins) — simulations write pins_gate52.SIM-<name>.json only"
PN="$GS/pin_gate52.py"
ctl PN0  0 "PASS: FAIL=0 -> pins_gate52.SIM-real.json .*END_TREE_B $EB \| 3 \+ 5 paths" -- python3 "$PN" "$SP" --simulate real "1367=$HA,1368=$HB"
ctl PN0e 0 "END_TREE_B $EB \| git diff --shortstat develop END_B: 7 files changed, 225 insertions\(\+\), 2 deletions\(-\)" -- cat "$W/PN0.out"
ctl PN0s 0 'SECOND INSTRUMENT merge-tree --write-tree A B .* == END_TREE_B: True' -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 9 path-pin\(s\) \(8 PR, 1 control\), 9 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0k 0 'routes/referrals.ts: develop e97b7f0bc550 .*BYTE-EQUAL in every tree' -- cat "$W/PN0.out"
ctl PN1  1 'REFUSING: --develop is a controls-only override' -- python3 "$PN" "$SP" --develop "$OLDDEV"
PRT="$(restack "$HB" "$VV" "s = s + '\n// gate52 control plant: a runtime handler file edited\n'")"
ctl PN2  1 '\(K\) Blockchain/Dev/services/originate/src/routes/verificationV2.ts is not byte-equal' -- python3 "$PN" "$SP" --simulate rt "1367=$HA,1368=$PRT"
DCF="$(mkdev "$Y" "s = s + '\n'")"
ctl PN3  1 '\(C\) #1367: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate cfl "1367=$HA,1368=$HB" --develop "$DCF"
M755="$(remode "$HB" "$Y" 100755)"
ctl PN4  1 '#1368 Blockchain/Dev/docs/openapi/secuura-api.yaml: want 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1367=$HA,1368=$M755"
DMV="$(mkdev "Blockchain/Dev/BACKLOG.md" "s = s + '\n<!-- gate52 control plant: an unrelated develop move -->\n'")"
ctl PN5  1 "\(F\) END_TREE_B [0-9a-f]{40} != the seat's PREDICTED $EB" -- python3 "$PN" "$SP" --simulate mv "1367=$HA,1368=$HB" --develop "$DMV"
ctl PN5n 1 '#1368 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 1 path\(s\) \| reaches its own paths: NONE' -- python3 "$PN" "$SP" --simulate mv2 "1367=$HA,1368=$HB" --develop "$DMV"
P3F="$(restack "$HA" "Blockchain/Dev/BACKLOG.md" "s = s + ' '")"
ctl PN6  1 "\(B\) #1367 paths outside the allowed prefixes \['Blockchain/Dev/BACKLOG.md'\]" -- python3 "$PN" "$SP" --simulate third "1367=$P3F,1368=$HB"
TAB="$(git -C "$CL" merge-tree --write-tree "$HA" "$HB" | head -1)"; BONA="$(commitw "$TAB" "$HA" "gate52 control plant: B stacked ON A (not a sibling)")"
ctl PN7  1 '\(B2\) the two PRs are not siblings on one base' -- python3 "$PN" "$SP" --simulate stacked "1367=$HA,1368=$BONA"
CFB="$(restack "$HB" "$Y" "i = s.index('  /api/referrals/{code}:\n'); a = '\$ref: \"#/components/schemas/ReferralCode\"'; j = s.index(a, i); s = s[:j] + a[:-1] + 'Z\"' + s[j + len(a):]")"
ctl PN8  1 "\(F\) #1368 does NOT merge cleanly onto #1367's simulated squash" -- python3 "$PN" "$SP" --simulate conflict "1367=$HA,1368=$CFB"

echo "--- specdiff_gate52.py (requirement 4 prediction + the red-cell census; the yaml control inside)"
SD="$GS/specdiff_gate52.py"
ctl SD0  0 'SPECDIFF PASS: 0 FAIL of 17 checks' -- python3 "$SD" "$SP"
ctl SD0g 0 'PASS #1368 S4 goldens byte-equal: 4 of 4 non-yaml paths .*yaml control differs: True' -- cat "$W/SD0.out"
ctl SD0a 0 'PASS #1367 S2 only the GET 200 changed' -- cat "$W/SD0.out"
ctl SD0u 0 'PASS S8 union yaml at END_B: .*sha256 e761a0b3c1eac6a5' -- cat "$W/SD0.out"
S1P="$(restack "$HA" "$RO" "a = \"  summary: 'Look up a referral code',\"; assert s.count(a) == 1; s = s.replace(a, \"  summary: 'Look up a referral code!',\")")"
ctl SD1  1 'FAIL #1367 S2 only the GET 200 changed' -- python3 "$SD" "$SP" --head-1367 "$S1P"
S2P="$(restack "$HB" "$TO" "a = \"'application/json': { schema: TenantUpdateRequestSchema },\"; assert s.count(a) == 1; s = s.replace(a, \"'application/json': { schema: TenantUpdateRequestSchema.partial() },\")")"
ctl SD2  1 "FAIL #1368 S2 only .*files with another change: \['Blockchain/Dev/services/tenant-provisioning/src/tenant-provisioning.openapi.ts'\]" -- python3 "$SD" "$SP" --head-1368 "$S2P"
S3P="$(restack "$HB" "$Y" "a = '      summary: Update tenant fields\n'; assert s.count(a) == 1; s = s.replace(a, a + '      x-gate52-plant: true\n')")"
ctl SD3  1 'FAIL #1368 S3 yaml' -- python3 "$SD" "$SP" --head-1368 "$S3P"
mkdir -p "$W/goldens"; for g in spark_secuura_2026-09-30_KS-1015-envelope spark_secuura_2026-10-01_KS-1364-platform-tenants spark_secuura_2026-10-01_KS-1364-v2-verify; do mkdir -p "$W/goldens/$g/out.md.checker"; cp "$GD/$g/out.md.checker/patch.diff" "$W/goldens/$g/out.md.checker/patch.diff"; done
mut "$W/goldens/spark_secuura_2026-10-01_KS-1364-platform-tenants/out.md.checker/patch.diff" "$W/goldens/spark_secuura_2026-10-01_KS-1364-platform-tenants/out.md.checker/patch.diff" 'publishes a REQUIRED request body' 'publishes a REQUIRED request body!'
ctl SD4  1 'FAIL #1368 S4 goldens byte-equal: 3 of 4 non-yaml paths' -- python3 "$SD" "$SP" --goldens-dir "$W/goldens"
ctl SD5  1 'FAIL #1367 S1 file set: 0 paths' -- python3 "$SD" "$SP" --head-1367 "$DEV"
ctl SD6  1 'FAIL S8 union yaml at END_B' -- python3 "$SD" "$SP" --end-b "$DEVTREE"
PRA="$(restack "$HA" "$RR" "s = s + '\n// gate52 control plant: a runtime handler file edited\n'")"
ctl SD7  1 "FAIL #1367 S7 no runtime path: .*\['Blockchain/Dev/services/referral/src/routes/referrals.ts'\]" -- python3 "$SD" "$SP" --head-1367 "$PRA"

echo "--- handlers_gate52.py (requirements 1-3 prediction; the RG-CTL control inside)"
HD="$GS/handlers_gate52.py"
ctl HD0  0 'HANDLERS PASS: 8 checks, 0 FAIL' -- python3 "$HD" "$SP"
ctl HD0c 0 'OK   RG-CTL .*4xx branches after the validator NONE .*ACCEPTS-EMPTY \(want ACCEPTS-EMPTY\)' -- cat "$W/HD0.out"
ctl HD0m 0 'RUNTIME Blockchain/Dev/package-lock.json at [0-9a-f]{12}: express 4\.[0-9.]+ \| body-parser 1\.[0-9.]+' -- cat "$W/HD0.out"
ctl HD0e 0 'OK   RL1 200 data keys' -- cat "$W/HD0.out"
H1P="$(restack "$HB" "$TI" "a = 'if (sets.length === 0) {'; assert s.count(a) == 1; s = s.replace(a, 'if (false) {')")"
ctl HD1  1 'FAIL TP1 PATCH /api/platform/tenants/\{id\}: .*ACCEPTS-EMPTY \(want REJECTS-EMPTY\)' -- python3 "$HD" "$SP" --tree-1368 "$H1P"
H2P="$(restack "$HB" "$VV" "a = 'const hashToVerify = hash || providedHash || contentHash || documentHash;'; assert s.count(a) == 1; s = s.replace(a, 'const hashToVerify = hash || providedHash || contentHash;')")"
ctl HD2  1 'FAIL VV1 .*ALIASES MISSING' -- python3 "$HD" "$SP" --tree-1368 "$H2P"
H3P="$(restack "$HB" "$RR" "a = '  customCode: z.string().trim().min(4).max(16).optional(),'; assert s.count(a) == 1; s = s.replace(a, '  customCode: z.string().trim().min(4).max(16),')")"
ctl HD3  1 'FAIL RG-CTL .*REJECTS-EMPTY \(want ACCEPTS-EMPTY\)' -- python3 "$HD" "$SP" --tree-1368 "$H3P"
H3G="$(restack "$HB" "$RR" "a = '    const body = generateCodeSchema.parse(req.body);\n'; assert s.count(a) == 1; s = s.replace(a, a + '    if (!body.customCode) {\n      return res.status(400).json({ success: false });\n    }\n')")"
ctl HD3g 1 'FAIL RG-CTL .*4xx branches after the validator \[' -- python3 "$HD" "$SP" --tree-1368 "$H3G"
H4P="$(restack "$HA" "$RR" "a = \"        referrerReward: '50 SECURA',\n\"; assert s.count(a) == 1; s = s.replace(a, a + '        ownerId: referralCode.ownerId,\n')")"
ctl HD4  1 'FAIL RL1 200 data keys' -- python3 "$HD" "$SP" --tree-1367 "$H4P"
H5P="$(restack "$HA" "$RR" "i = s.index(\"router.get('/:code'\"); a = 'return res.status(404).json('; j = s.index(a, i); s = s[:j] + 'return res.status(409).json(' + s[j + len(a):]")"
ctl HD5  1 "FAIL RL1 statuses declared: .*undeclared in the spec: \['409'\]" -- python3 "$HD" "$SP" --tree-1367 "$H5P"
H6P="$(restack "$HA" "$RO" "a = '                customLabel: z.string().optional(),'; assert s.count(a) == 1; s = s.replace(a, '                customLabel: z.string(),')")"
ctl HD6  1 'FAIL RL1 yaml required' -- python3 "$HD" "$SP" --tree-1367 "$H6P"

echo "--- keyscan_gate52.py (subjects, bodies, live surfaces, NO TRAILER with its control)"
KS="$GS/keyscan_gate52.py"; SB="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1368"]["title"])' "$GS/gh_read_1.json")"
ctl KS0  0 'KEYSCAN PASS: 17 checks over 2 PRs, 0 FAIL \(trailer control FIRED\)' -- python3 "$KS" "$SP"
ctl KS1  1 'FAIL #1367 S2' -- python3 "$KS" "$SP" --subject-1367 "KS-1015: the referral lookup spec declares the envelope (#1367)"
ctl KS2  1 'FAIL #1368 S1' -- python3 "$KS" "$SP" --subject-1368 "KS-1364: mark two bodies required (KS-1015)"
ctl KS3  1 'FAIL #1368 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --subject-1368 "${SB}01"
printf '' > "$W/b_empty.txt";                                    ctl KS4 1 'FAIL #1367 B1 KS-1015' -- python3 "$KS" "$SP" --body-file "$W/b_empty.txt"
printf 'Refs KS-1015\nRefs KS-1364\nCloses KS-1364\n' > "$W/b_close.txt"; ctl KS5 1 'FAIL #1368 B2' -- python3 "$KS" "$SP" --body-file "$W/b_close.txt"
printf 'Refs KS-1015\nthe residue is KS-1364 outside any fence\n' > "$W/pb.txt"; ctl KS6 1 "FAIL #1367 L1 live surfaces: .*\['PR body'\]" -- python3 "$KS" "$SP" --prbody-file-1367 "$W/pb.txt"
printf 'KS-1364: mark two more request bodies required\n\nbody\n\nCo-Authored-By: Someone <someone@example.invalid>\n' > "$W/cm.txt"; ctl KS7 1 'FAIL #1368 T1 no trailer' -- python3 "$KS" "$SP" --commit-msg-file-1368 "$W/cm.txt"
ctl KS8  1 'FAIL T1-CONTROL .*DID NOT FIRE|trailer control DID NOT FIRE' -- python3 "$KS" "$SP" --trailer-control "$HA"

echo "--- endtree_gate52.py (three instruments per END_TREE)"
ctl ET0  0 "ENDTREE AGREE: END_TREE_A $EA read by 3 of 3 instruments \| END_TREE_B $EB read by 3 of 3" -- python3 "$GS/endtree_gate52.py" "$SP"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L1  6 '#1367 — .* is not at .* AND refs/pull/1367/head' -- env G52_HEAD_1367="$DEV" "$L" --check
ctl L1b 6 '#1368 — .* is not at .* AND refs/pull/1368/head' -- env G52_HEAD_1368="$HA" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G52_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1368 — the compare is not the pinned' -- env G52_PATHS_1368="$Y" "$L" --check
mut "$PROMPT" "$W/p_go.txt" 'GO (Seat B 53rd): merge 1367 1368 on gate52' 'GO (Seat B 53rd): merge 1368 1367 on gate52';   ctl L4 26 'merge authority / the GO string' -- env G52_PROMPT="$W/p_go.txt" "$L" --check
mut "$PROMPT" "$W/p_seat.txt" 'The merge seat is Seat B 53rd' 'The merge seat is Seat B 52nd';                   ctl L4b 26 'merge authority / the GO string' -- env G52_PROMPT="$W/p_seat.txt" "$L" --check
mut "$PROMPT" "$W/p_ord.txt" 'ONE AT A TIME, A FIRST' 'in either order';                                       ctl L4c 26 'merge authority / the GO string / the order' -- env G52_PROMPT="$W/p_ord.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                        ctl L5 8 'unfilled double-brace' -- env G52_PROMPT="$W/p_tok.txt" "$L" --check
{ cat "$PROMPT"; echo 'merge #<PR>'; } > "$W/p_ph.txt";                                                         ctl L5b 8 'unpinned PR placeholder' -- env G52_PROMPT="$W/p_ph.txt" "$L" --check
i=0
for kw in ENVELOPE-MATCHES-HANDLER ERROR-CODES-MATCH HANDLER-REJECTS-ABSENT BODY-PARSER-DEFAULT ALIASES-COVERED GENERATE-NOT-REQUIRED GOLDENS-BYTE-EQUAL GENERATOR-REPRODUCES CHECK-OPENAPI-RC YAML-SHAS RED-FIRST CONTROLS-GREEN SUITES-BASE-HEAD TSC-NO-REGRESSION SEQUENCE-A-THEN-B CLEAN-MERGE END-TREE BOTH-MERGEABLE MODES KEYSCAN-OWN-KEY NO-CLOSING-KEYWORD NO-TRAILER SUBJECT-LANDS-AT SUBJECT-TRUE-OF-DIFF PR-BODY-CLAIMS NO-RUNTIME-CHANGE COLLISION-CENSUS NOT-TESTED-LIST TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  i=$((i + 1)); sed "s/$kw/$kw-X/g" "$PROMPT" > "$W/p_kw$i.txt"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G52_PROMPT="$W/p_kw$i.txt" "$L" --check
done
mut "$PROMPT" "$W/p_fn.txt" 'ASSERT THE FILENAME TOO' 'assert the content';                                         ctl L6 33 'the filename rule' -- env G52_PROMPT="$W/p_fn.txt" "$L" --check
sed "s/$HB/${HB:0:39}x/g" "$CAP" > "$W/cap_noh.md";                                                             ctl L7 20 "do not both name #1368's head" -- env G52_BRIEF="$W/cap_noh.md" "$L" --check
mut "$PROMPT" "$W/p_h1.txt" 'NO ticket filed' 'NO tickets filed';                                                    ctl L8 39 'the HOLDS' -- env G52_PROMPT="$W/p_h1.txt" "$L" --check
mut "$PROMPT" "$W/p_h2.txt" 'You NEVER reply to Peter' 'You may reply to Peter';                                     ctl L8b 39 'the HOLDS' -- env G52_PROMPT="$W/p_h2.txt" "$L" --check
mut "$PROMPT" "$W/p_h3.txt" 'Never read or write a real `.env`' 'Never write a real `.env`';                         ctl L8c 39 'the HOLDS' -- env G52_PROMPT="$W/p_h3.txt" "$L" --check
mut "$PROMPT" "$W/p_h4.txt" 'Reverts and plants live only in a SCRATCH worktree you created' 'Reverts may live anywhere';  ctl L8d 39 'the HOLDS' -- env G52_PROMPT="$W/p_h4.txt" "$L" --check
mut "$PROMPT" "$W/p_h7.txt" 'THE NAMED EXCEPTIONS to those holds — these and NO others' 'THE NAMED EXCEPTIONS to those holds'; ctl L8g 39 'the HOLDS' -- env G52_PROMPT="$W/p_h7.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                            ctl L10 31 'launch develop / END_TREE_A / END_TREE_B' -- env G52_PROMPT="$W/p_dev.txt" "$L" --check
sed "s/$EA/${EA:0:39}x/g" "$PROMPT" > "$W/p_ea.txt";                                                               ctl L10b 31 'launch develop / END_TREE_A / END_TREE_B' -- env G52_PROMPT="$W/p_ea.txt" "$L" --check
mut "$PROMPT" "$W/p_tier.txt" '#1367 T2 —' '#1367 T1 —';                                                              ctl L11 7 'the tier lines' -- env G52_PROMPT="$W/p_tier.txt" "$L" --check
mut "$PROMPT" "$W/p_round.txt" 'a round-1 NO GO goes back to the author for round 2' 'a round-1 NO GO ships nothing';  ctl L11b 7 'the tiering rule' -- env G52_PROMPT="$W/p_round.txt" "$L" --check
mut "$PROMPT" "$W/p_sib.txt" 'B is NOT built on A' 'B is built on A';                                                ctl L11c 7 'the sibling order' -- env G52_PROMPT="$W/p_sib.txt" "$L" --check
mut "$PROMPT" "$W/p_tkt.txt" 'PR #1367 is KS-1015' 'PR #1367 is KS-1016';                                             ctl L12 32 "BOTH state each ticket" -- env G52_PROMPT="$W/p_tkt.txt" "$L" --check
mut "$PROMPT" "$W/p_a1.txt" 'MG-1 3 over 3 paths' 'MG-1 over the paths';                                              ctl L13 25 'the MERGE ADDENDUM rules' -- env G52_PROMPT="$W/p_a1.txt" "$L" --check
mut "$PROMPT" "$W/p_a2.txt" 'NOTHING to report.md after you send the verdict mail' 'little to report.md after you send the verdict mail'; ctl L13b 25 'REPORT-HASH-LAST' -- env G52_PROMPT="$W/p_a2.txt" "$L" --check
mut "$PROMPT" "$W/p_a3.txt" 'HANDLERS 2 of 2 reject an absent body' 'HANDLERS checked';                               ctl L13c 25 'the MERGE ADDENDUM rules' -- env G52_PROMPT="$W/p_a3.txt" "$L" --check
mut "$PROMPT" "$W/p_a4.txt" 'NO TRAILER' 'trailer as usual';                                                          ctl L13d 25 'the MERGE ADDENDUM rules' -- env G52_PROMPT="$W/p_a4.txt" "$L" --check
mut "$PROMPT" "$W/p_subj.txt" 'GATE52 #1367 #1368' 'GATE52 #1367';                                                    ctl L14 23 'the verdict subject' -- env G52_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                         ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
mut "$PROMPT" "$W/p_k1.txt" "$GS/handlers_1.out" "$GS/handlers_elsewhere.out";                                         ctl L16 8 'handlers_1.out is missing, empty, or not named' -- env G52_PROMPT="$W/p_k1.txt" "$L" --check
mut "$PROMPT" "$W/p_k2.txt" "$GS/gh_body_1368.md" "$GS/gh_body_elsewhere.md";                                          ctl L17 8 'gh_body_1368.md is missing, empty, or not named' -- env G52_PROMPT="$W/p_k2.txt" "$L" --check
mut "$PROMPT" "$W/p_k3.txt" '2026-10-01-batch1365-g51a/report.md' '2026-10-01-batch1364-g50b/report.md';              ctl L18 8 'the previous round report' -- env G52_PROMPT="$W/p_k3.txt" "$L" --check
mut "$PROMPT" "$W/p_x1.txt" 'No live server is started, no Schemathesis is run, and no image is built in this gate' 'A live server may be started'; ctl L20 34 'the NO-RUNTIME rule' -- env G52_PROMPT="$W/p_x1.txt" "$L" --check
mut "$PROMPT" "$W/p_x2.txt" 'A SPEC THAT DISAGREES WITH ITS HANDLER IS A MAJOR' 'A SPEC THAT DISAGREES WITH ITS HANDLER IS A NOTE';  ctl L21 36 'the SPEC-TRUTH rule' -- env G52_PROMPT="$W/p_x2.txt" "$L" --check
mut "$PROMPT" "$W/p_x2b.txt" 'never from memory' 'from memory if need be';                                          ctl L21b 36 'the SPEC-TRUTH rule' -- env G52_PROMPT="$W/p_x2b.txt" "$L" --check
mut "$PROMPT" "$W/p_x2c.txt" 'the same reading must say ACCEPTS here' 'the same reading may say anything here';      ctl L21c 36 'the SPEC-TRUTH rule' -- env G52_PROMPT="$W/p_x2c.txt" "$L" --check
mut "$PROMPT" "$W/p_x3.txt" 'You change no ticket state' 'You may move KS-1015 back';                               ctl L22 37 "the NOT-THE-GATE'S items" -- env G52_PROMPT="$W/p_x3.txt" "$L" --check
mut "$PROMPT" "$W/p_x4.txt" 'is at 92%' 'is fine';                                                                    ctl L23 38 'the proportionality line' -- env G52_PROMPT="$W/p_x4.txt" "$L" --check
mut "$PROMPT" "$W/p_x5.txt" "Kam's 17:40:22 grant" "a grant";                                                         ctl L23b 38 'the proportionality line' -- env G52_PROMPT="$W/p_x5.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate52.sh"
ctl R0  0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key outside reported_overlaps \| 0 expected overlap\(s\) reported \| 0 sequenced by Wednesday .*1 client-human PR\(s\) reported \| 7 kit path\(s\), 2 kit key\(s\)' -- cat "$W/R0.out"
ctl R0h 0 'CLIENT-HUMAN \(reported, never sequenced by a gate\) #1360 by PeterObeden' -- cat "$W/R0.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pins, 2 of 2' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                                ctl R1 1 'is not registered in inbox_routing.conf' -- env G52_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2  15 "OVERLAP #1360 .*paths \[.*'Blockchain/Dev/package-lock.json'" -- env G52_OVERLAP_EXTRA="Blockchain/Dev/package-lock.json" "$R" "$L" "$SP" --dry-run
ctl R3  15 "OVERLAP #1360 .*title keys \['KS-1380'\]" -- env G52_TITLE_KEY="KS-1380" "$R" "$L" "$SP" --dry-run
printf '{"1360": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H60" > "$W/seq_ok.json"
printf '{"1360": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$HA" > "$W/seq_bad.json"
ctl R3s 0 'SEQUENCED OUT-OF-KIT #1360 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- env G52_TITLE_KEY="KS-1380" G52_SEQUENCED="$W/seq_ok.json" "$R" "$L" "$SP" --dry-run
ctl R3w 15 'OVERLAP #1360 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G52_TITLE_KEY="KS-1380" G52_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #1360 ' -- env G52_WIDEN_RX="ks-1380-revert-pr-1358$" "$R" "$L" "$SP" --dry-run
sed "s/|$HB|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh";                      ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1367|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G52_ROUTING="$W/routing_ok.conf" G52_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins, kit.json and the filled prompt are untouched by every control above"
ctl PNZ 0 '' -- test "$(SHA "$GS/pins_gate52.json")" = "$PINSHA"
ctl KJZ 0 '' -- test "$(SHA "$GS/kit.json")" = "$KITSHA"
ctl PRZ 0 '' -- test "$(SHA "$PROMPT")" = "$PRSHA"
echo "SUMMARY gate52: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
