#!/bin/bash
# controls_gate53.sh — drives every guard in the gate53 kit, on the REAL subject (#1369) and on PLANTED defects. Each control names the rc it
# must give and a WHY pattern its output must carry. A refusal for the wrong reason is a MISMATCH. A check that prints nothing is paired with
# a control that makes it print.
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped, so every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants are synthetic commits in the SCRATCH clone only. They use plumbing (read-tree / update-index / write-tree / commit-tree under a temp
# index), never a worktree and never the checkout, plus files under <scratchpad>/g53_sp/controls_<HHMMSS>/. The kit's own files are never
# edited. The real pins_gate53.json, kit.json and the filled prompt are sha256-checked unchanged at the end (PNZ, KJZ, PRZ).
# The launcher runs with --check (headless), except L9: the real launch path with stdin NOT a TTY, which must refuse rc 21 before exec.
# The repin runs --dry-run, except R1 (a real run that must refuse at step 0, routing) and R8 (a real run with a routed temp file that must stop
# at G53_STOP_AFTER_3B). Both stop long before the usage gate / cockpit.
# Mode plants RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>), because core.filemode is false.
# Each by-name keyword has its own launcher refusal (LK*): the keyword is broken into `<KW>-X`, which the launcher's TOKEN match must NOT accept.
# auditset controls read the kit's SAVED advisory reports (npm_audit_{base,head}_1.json) or planted copies of them — no live npm audit per plant;
# the registry controls (RG*) make live `npm view` reads (registry reads only).
# This is a NEW COPY of gate51a's / gate52's controls (shape, harness, ssh-retry), re-planted for this kit's lock + baseline PR. Theirs are not edited.
# Usage: controls_gate53.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g53_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g53_sp/clone"; L="$GS/launch_qa_secuura_batch1369.sh"; PROMPT="$GS/2026-10-02_secuura-batch1369.prompt.txt"; CAP="$GS/READY_1369_mail.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate53.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"; H="$(PJ pr_pins.1369.head)"
SHA() { shasum -a 256 "$1" | cut -c1-64; }
PINSHA="$(SHA "$GS/pins_gate53.json")"; KITSHA="$(SHA "$GS/kit.json")"; PRSHA="$(SHA "$PROMPT")"
LK='Blockchain/Dev/package-lock.json'; PJN='Blockchain/Dev/package.json'; BL='Blockchain/Dev/scripts/audit/audit-baseline.json'
BC='Blockchain/Dev/scripts/audit/baseline-contract.mjs'; ML='Blockchain/Dev/services/mcp-server/package-lock.json'
OD='Blockchain/Dev/services/originate/Dockerfile'; AD='Blockchain/Dev/services/auth/Dockerfile'
AB="$GS/npm_audit_base_1.json"; AH="$GS/npm_audit_head_1.json"
GHJ() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["census"][sys.argv[2]][sys.argv[3]])' "$GS/gh_read_1.json" "$1" "$2"; }
H60="$(GHJ 1360 head)"; H995="$(GHJ 995 head)"
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
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|LOCKDIFF|AUDITSET|REGISTRY|IMAGES|MODE|ENDTREE' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
IDN=0
commitw() { # commitw <tree> <parent> <msg>
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate53.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate53.invalid GIT_AUTHOR_DATE=2026-10-02T00:00:00Z GIT_COMMITTER_DATE=2026-10-02T00:00:00Z \
    git -C "$CL" commit-tree "$1" -p "$2" -m "$3"
}
mkdev() { # mkdev <path> <transform> — a develop MOVE plant: a child of develop (for --develop simulations)
  local p="$1" tf="$2" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.dev.$IDN"
  git -C "$CL" show "$DEV:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || return 1
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$DEV"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$DEV" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$DEV" "gate53 control plant: develop move on $p"
}
restack() { # restack <subject head> <path> <transform> — the subject's own tree with ONE more path edited, parent = the subject's parent
  local h="$1" p="$2" tf="$3" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.rs.$IDN"
  git -C "$CL" show "$h:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || { echo "PLANT TRANSFORM FAILED for $p" >&2; return 1; }
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$h" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate53 control plant: $p over $h"
}
remode() { # remode <subject head> <path> <mode> — the subject's own tree with ONE path's RECORDED mode changed
  local h="$1" p="$2" mo="$3" idx tree; IDN=$((IDN + 1)); idx="$W/idx.rm.$IDN"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"; GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mo,$(git -C "$CL" rev-parse "$h:$p"),$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate53 control plant: $p recorded $mo"
}
mut() { # mut <src> <dst> <old> <new> — a literal replacement (python, no shell quoting), refusing when <old> is absent
  python3 -c 'import sys; s=open(sys.argv[1]).read(); assert sys.argv[3] in s, "mut: anchor absent: " + sys.argv[3]; open(sys.argv[2], "w").write(s.replace(sys.argv[3], sys.argv[4]))' "$@"
}
echo "=== controls_gate53 $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1369 $H | END_TREE $END | plants $W"

echo "--- pin_gate53.py (head, shape, the 3 allowed paths + numstat, the move, alone, the squash == the prediction, RECORDED modes + control, hook files, the unchanged pins) — simulations write pins_gate53.SIM-<name>.json only"
PN="$GS/pin_gate53.py"
ctl PN0  0 'PASS: FAIL=0 -> pins_gate53.SIM-real.json .* 3 paths \+3/-18' -- python3 "$PN" "$SP" --simulate real "1369=$H"
ctl PN0e 0 "END_TREE $END \| git diff --shortstat develop END: 3 files changed, 3 insertions\(\+\), 18 deletions\(-\)" -- cat "$W/PN0.out"
ctl PN0p 0 "END_TREE == the seat's PREDICTED $END" -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 4 path\(s\) pinned \(3 PR, 1 control\), 4 OK .*100644.*100755' -- cat "$W/PN0.out"
ctl PN0k 0 'baseline-contract.mjs: develop ef82d7c5211d .*BYTE-EQUAL in every tree' -- cat "$W/PN0.out"
ctl PN1  1 'REFUSING: --develop is a controls-only override' -- python3 "$PN" "$SP" --develop "$OLDDEV"
PBC="$(restack "$H" "$BC" "s = s + '\n// gate53 control plant: the baseline contract edited\n'")"
ctl PN2  1 '\(K\) Blockchain/Dev/scripts/audit/baseline-contract.mjs is not byte-equal' -- python3 "$PN" "$SP" --simulate rt "1369=$PBC"
DCF="$(mkdev "$BL" "s = s + '\n'")"
ctl PN3  1 '\(C\) #1369: the develop move touches its own path' -- python3 "$PN" "$SP" --simulate cfl "1369=$H" --develop "$DCF"
M755="$(remode "$H" "$LK" 100755)"
ctl PN4  1 'Blockchain/Dev/package-lock.json: want 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m755 "1369=$M755"
DMV="$(mkdev "Blockchain/Dev/BACKLOG.md" "s = s + '\n<!-- gate53 control plant: an unrelated develop move -->\n'")"
ctl PN5  1 "\(F\) END_TREE [0-9a-f]{40} != the seat's PREDICTED $END" -- python3 "$PN" "$SP" --simulate mv "1369=$H" --develop "$DMV"
ctl PN5c 0 '#1369 move [0-9a-f]{12}\.\.[0-9a-f]{12}: 1 path\(s\) \| reaches its own paths: NONE' -- cat "$W/PN5.out"
P3F="$(restack "$H" "Blockchain/Dev/BACKLOG.md" "s = s + ' '")"
ctl PN6  1 "\(B\) paths outside the allowed paths \['Blockchain/Dev/BACKLOG.md'\]" -- python3 "$PN" "$SP" --simulate third "1369=$P3F"
PNS="$(restack "$H" "$PJN" "a = '  \"overrides\": {\n'; assert s.count(a) == 1; s = s.replace(a, a + '    \"gate53-plant\": \"1.0.0\",\n')")"
ctl PN7  1 '\(B\) numstat Blockchain/Dev/package.json \[4, 0\] != expected \[3, 0\]' -- python3 "$PN" "$SP" --simulate ns "1369=$PNS"

echo "--- lockdiff_gate53.py (requirements 1 + 5's row prediction; the substring-trap control inside)"
LD="$GS/lockdiff_gate53.py"
ctl LD0  0 'LOCKDIFF PASS: 0 FAIL of 11 checks' -- python3 "$LD" "$SP"
ctl LD0p 0 'PASS L2 @prisma/dev: value-equal True \| raw block byte-identical True' -- cat "$W/LD0.out"
ctl LD0s 0 'PASS B4 substring trap \(control\): at head the id occurs as a SUBSTRING on line\(s\) \[90, 97\]' -- cat "$W/LD0.out"
LV="$(restack "$H" "$LK" "a = '\"node_modules/hono\": {\n      \"version\": \"4.13.8\",'; assert s.count(a) == 1; s = s.replace(a, a.replace('4.13.8', '4.13.9'))")"
ctl LD1  1 "FAIL L1 key-by-key: .*added 0, changed 1, flips 0" -- python3 "$LD" "$SP" --head "$LV"
LF="$(restack "$H" "$LK" "a = '\"node_modules/@prisma/dev/node_modules/@prisma/debug\": {\n      \"version\": \"7.2.0\",\n      \"devOptional\": true,'; assert s.count(a) == 1; s = s.replace(a, a.replace('devOptional', 'dev'))")"
ctl LD2  1 "FAIL L1 key-by-key: .*changed 1, flips 1" -- python3 "$LD" "$SP" --head "$LF"
LPD="$(restack "$H" "$LK" "import re; i = s.index('\"node_modules/@prisma/dev\": {'); j = s.index('\"@hono/node-server\": \"1.19.11\"', i); s = s[:j] + '\"@hono/node-server\": \"^1.19.15\"' + s[j + len('\"@hono/node-server\": \"1.19.11\"'):]")"
ctl LD3  1 'FAIL L2 @prisma/dev' -- python3 "$LD" "$SP" --head "$LPD"
LWS="$(restack "$H" "$LK" "a = '\"node_modules/hono\": {\n'; assert s.count(a) == 1; s = s.replace(a, '\"node_modules/hono\": { \n')")"
ctl LD4  1 'FAIL L5 text diff' -- python3 "$LD" "$SP" --head "$LWS"
ctl LD4v 0 'PASS L1 key-by-key' -- cat "$W/LD4.out"
LOL="$(restack "$H" "$ML" "s = s + '\n'")"
ctl LD5  1 "FAIL L4 other locks: .*blobs that differ: \['Blockchain/Dev/package-lock.json', 'Blockchain/Dev/services/mcp-server/package-lock.json'\]" -- python3 "$LD" "$SP" --head "$LOL"
LTO="$(restack "$H" "$PJN" "a = '  \"overrides\": {\n'; assert s.count(a) == 1; s = s.replace(a, a + '    \"@hono/node-server\": \"^1.19.15\",\n')")"
ctl LD6  1 'FAIL M1 manifest: .*top-level "@hono/node-server" override PRESENT' -- python3 "$LD" "$SP" --head "$LTO"
LEX="$(restack "$H" "$BL" "i = s.index('\"GHSA-wrjc-x8rr-h8h6\"'); j = s.index('\"expires\": \"2026-10-09\"', i); s = s[:j] + '\"expires\": \"2026-10-31\"' + s[j + len('\"expires\": \"2026-10-09\"'):]")"
ctl LD7  1 "FAIL B3 fuses: expires changed on a surviving row: \['GHSA-wrjc-x8rr-h8h6'\]" -- python3 "$LD" "$SP" --head "$LEX"
LES="$(restack "$H" "$BL" "i = s.index('—', s.index('\"accepted\"')); s = s[:i] + '\\\\u2014' + s[i + 1:]")"
ctl LD8  1 'FAIL B2 bytes: .*changed by value 0, by raw bytes 1' -- python3 "$LD" "$SP" --head "$LES"
ctl LD8v 0 'PASS B1 key sets' -- cat "$W/LD8.out"
ctl LD9  1 "FAIL L1 key-by-key: removed \[\]" -- python3 "$LD" "$SP" --head "$DEV"

echo "--- auditset_gate53.py (requirement 5 prediction, on the SAVED advisory reports and planted copies)"
AS="$GS/auditset_gate53.py"
ctl AS0  0 'AUDITSET PASS: 0 FAIL of 4 checks .*reported 11 -> 9, baselined 25 -> 24, CLEANUP 14 -> 15' -- python3 "$AS" "$SP" --audit-base "$AB" --audit-head "$AH"
ctl AS0w 0 'WHY  no longer reported at head: GHSA-92pp-h63x-v22m @hono/node-server' -- cat "$W/AS0.out"
ctl AS0r 0 "RED  FAIL — new \['GHSA-frvp-7c67-39w9'\]" -- cat "$W/AS0.out"
ctl AS1  1 "HEAD FAIL — new \['GHSA-frvp-7c67-39w9'\]" -- python3 "$AS" "$SP" --audit-base "$AB" --audit-head "$AB"
python3 -c 'import json,sys; j=json.load(open(sys.argv[1])); j["vulnerabilities"]["zz-gate53-plant"]={"name":"zz-gate53-plant","severity":"high","via":[{"name":"zz-gate53-plant","severity":"high","url":"https://github.com/advisories/GHSA-zzzz-zzzz-zzzz","range":"<9"}],"nodes":["node_modules/zz-gate53-plant"]}; json.dump(j,open(sys.argv[2],"w"))' "$AH" "$W/audit_head_extra.json"
ctl AS2  1 "WHY  NEWLY reported at head: GHSA-zzzz-zzzz-zzzz" -- python3 "$AS" "$SP" --audit-base "$AB" --audit-head "$W/audit_head_extra.json"
ctl AS3  1 "HEAD FAIL — new \[\] \| lapsed \['GHSA-337j-9hxr-rhxg', 'GHSA-wrjc-x8rr-h8h6'\]" -- python3 "$AS" "$SP" --audit-base "$AB" --audit-head "$AH" --today 2026-10-09
A2R="$(restack "$H" "$BL" "import json; i = s.index('    \"GHSA-92pp-h63x-v22m\": {'); j = s.index('    },\n', i) + len('    },\n'); s = s[:i] + s[j:]")"
ctl AS4  1 'FAIL A2 HEAD: .*baselined 23 \(want 24\)' -- python3 "$AS" "$SP" --audit-base "$AB" --audit-head "$AH" --head "$A2R"

echo "--- registry_gate53.py (requirement 4 prediction; live npm view reads)"
RG="$GS/registry_gate53.py"
ctl RG0  0 'REGISTRY PASS: 0 FAIL of 4 checks' -- python3 "$RG" "$SP"
I11="$(npm view @hono/node-server@1.19.11 dist.integrity 2>"$W/npmview.err")"
ctl RG1  1 'FAIL R3 provenance' -- python3 "$RG" "$SP" --integrity "$I11"
ctl RG2  1 'FAIL R2 ranges: `>=1.19.15` -> max 2\.' -- python3 "$RG" "$SP" --range-caret '>=1.19.15'

echo "--- images_gate53.py (requirement 6 prediction; the control line inside)"
IM="$GS/images_gate53.py"
ctl IM0  0 'IMAGES PASS: 37 Dockerfiles, 0 image\(s\) copy the root lock, 0 unresolved, control FIRED' -- python3 "$IM" "$SP"
IR="$(restack "$H" "$OD" "a = 'COPY services/originate/package*.json ./'; assert s.count(a) == 1; s = s.replace(a, 'COPY package*.json ./')")"
ctl IM1  1 'HIT  Blockchain/Dev/services/originate/Dockerfile:28 .*context Blockchain/Dev' -- python3 "$IM" "$SP" --tree "$IR"
ctl IM1c 0 'control DID NOT FIRE' -- cat "$W/IM1.out"
IA="$(restack "$H" "$AD" "s = s + '\nCOPY package-lock.json /tmp/root-lock.json\n'")"
ctl IM2  1 'IMAGES FAIL: 37 Dockerfiles, 1 image\(s\) copy the root lock, 0 unresolved, control FIRED' -- python3 "$IM" "$SP" --tree "$IA"

echo "--- keyscan_gate53.py (subject, body, live surfaces, trailer, the method statement)"
KS="$GS/keyscan_gate53.py"; S6="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["prs"]["1369"]["title"])' "$GS/gh_read_1.json")"
ctl KS0  0 'KEYSCAN PASS: 10 checks over 1 PRs, 0 FAIL \(trailer control FIRED\)' -- python3 "$KS" "$SP"
ctl KS1  1 'FAIL #1369 S2' -- python3 "$KS" "$SP" --subject-1369 "$S6 (#1369)"
ctl KS2  1 'FAIL #1369 S1' -- python3 "$KS" "$SP" --subject-1369 "KS-530: scoped override (KS-528)"
ctl KS3  1 'FAIL #1369 S3: declared 86, lands at 94' -- python3 "$KS" "$SP" --subject-1369 "${S6}012"
printf '' > "$W/b_empty.txt";                                    ctl KS4 1 'FAIL #1369 B1 KS-530' -- python3 "$KS" "$SP" --body-file "$W/b_empty.txt"
printf 'Refs KS-530\nCloses KS-530\n' > "$W/b_close.txt";        ctl KS5 1 'FAIL #1369 B2' -- python3 "$KS" "$SP" --body-file "$W/b_close.txt"
python3 -c 'import sys; s=open(sys.argv[1]).read(); open(sys.argv[2],"w").write(s.replace("KS 528", "KS-528", 1))' "$GS/gh_body_1369.md" "$W/pb_for.txt"
ctl KS6  1 "FAIL #1369 L1 live surfaces: .*\['PR body'\]" -- python3 "$KS" "$SP" --prbody-file-1369 "$W/pb_for.txt"
printf 'KS-530: scoped override\n\nbody\n\nRefs KS-530\n\nCo-Authored-By: Someone <someone@example.invalid>\n' > "$W/cm.txt"; ctl KS7 1 'FAIL #1369 T1 no trailer' -- python3 "$KS" "$SP" --commit-msg-file-1369 "$W/cm.txt"
ctl KS8  1 'FAIL T1-CONTROL .*DID NOT FIRE|trailer control DID NOT FIRE' -- python3 "$KS" "$SP" --trailer-control "$H"
python3 -c 'import sys; s=open(sys.argv[1]).read(); assert "did not produce this edit unaided" in s; open(sys.argv[2],"w").write(s.replace("did not produce this edit unaided", "regenerated the lock"))' "$GS/gh_body_1369.md" "$W/pb_nometh.txt"
ctl KS9  1 "FAIL #1369 M1 method stated: .*missing \['did not produce this edit unaided'\]" -- python3 "$KS" "$SP" --prbody-file-1369 "$W/pb_nometh.txt"

echo "--- endtree_gate53.py"
ctl ET0  0 "ENDTREE AGREE: END_TREE $END read by 4 of 4 instruments \| == the seat's PREDICTED: True \| develop's tree differs: True" -- python3 "$GS/endtree_gate53.py" "$SP"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L1  6 '#1369 — .* is not at .* AND refs/pull/1369/head' -- env G53_HEAD_1369="$DEV" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G53_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1369 — the compare is not the pinned' -- env G53_PATHS_1369="$LK" "$L" --check
mut "$PROMPT" "$W/p_go.txt" 'GO (Seat B 54th): merge 1369 on gate53' 'GO (Seat B 54th): merge 1368 on gate53';      ctl L4 26 'merge authority / the GO string' -- env G53_PROMPT="$W/p_go.txt" "$L" --check
mut "$PROMPT" "$W/p_seat.txt" 'The merge seat is Seat B 54th' 'The merge seat is Seat B 53rd';                   ctl L4b 26 'merge authority / the GO string' -- env G53_PROMPT="$W/p_seat.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                        ctl L5 8 'unfilled double-brace' -- env G53_PROMPT="$W/p_tok.txt" "$L" --check
{ cat "$PROMPT"; echo 'merge #<PR>'; } > "$W/p_ph.txt";                                                         ctl L5b 8 'unpinned PR placeholder' -- env G53_PROMPT="$W/p_ph.txt" "$L" --check
i=0
for kw in NO-COLLATERAL PRISMA-DEV-BYTE-EQUAL OTHER-LOCKS-UNTOUCHED NPM-CI-HEAD LOCK-IDEMPOTENT INDEPENDENT-RESOLVE COUNTERFACTUAL EXTERNAL-NOT-BUNDLED RESOLVES-HOISTED PRISMA-RUNS CARET-NOT-GTE RED-FIRST AUDIT-LEGS REPORTED-11-TO-9 CLEANUP-VERBATIM ROW-KEYSET COHORT-TWO NO-IMAGE-READS-ROOT-LOCK SUITES-0-NEW-REDS TSC-NO-REGRESSION KEYSCAN-OWN-KEY NO-CLOSING-KEYWORD METHOD-STATED NO-TRAILER SUBJECT-LANDS-AT SUBJECT-TRUE-OF-DIFF PR-BODY-CLAIMS COLLISION-CENSUS NOT-TESTED-LIST CLEAN-MERGE END-TREE MODES TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  i=$((i + 1)); sed "s/$kw/$kw-X/g" "$PROMPT" > "$W/p_kw$i.txt"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G53_PROMPT="$W/p_kw$i.txt" "$L" --check
done
mut "$PROMPT" "$W/p_fn.txt" 'ASSERT THE FILENAME TOO' 'assert the content';                                         ctl L6 33 'the filename rule' -- env G53_PROMPT="$W/p_fn.txt" "$L" --check
sed "s/$H/${H:0:39}x/g" "$CAP" > "$W/cap_noh.md";                                                               ctl L7 20 "do not both name #1369's head" -- env G53_BRIEF="$W/cap_noh.md" "$L" --check
mut "$PROMPT" "$W/p_h1.txt" 'NO ticket filed' 'NO tickets filed';                                                    ctl L8 39 'the HOLDS' -- env G53_PROMPT="$W/p_h1.txt" "$L" --check
mut "$PROMPT" "$W/p_h2.txt" 'You NEVER reply to Peter' 'You may reply to Peter';                                     ctl L8b 39 'the HOLDS' -- env G53_PROMPT="$W/p_h2.txt" "$L" --check
mut "$PROMPT" "$W/p_h3.txt" 'Never read or write a real `.env`' 'Never write a real `.env`';                         ctl L8c 39 'the HOLDS' -- env G53_PROMPT="$W/p_h3.txt" "$L" --check
mut "$PROMPT" "$W/p_h4.txt" 'Reverts and plants live only in a SCRATCH worktree you created' 'Reverts may live anywhere';  ctl L8d 39 'the HOLDS' -- env G53_PROMPT="$W/p_h4.txt" "$L" --check
mut "$PROMPT" "$W/p_h7.txt" 'THE NAMED EXCEPTIONS to those holds — these and NO others' 'THE NAMED EXCEPTIONS to those holds'; ctl L8g 39 'the HOLDS' -- env G53_PROMPT="$W/p_h7.txt" "$L" --check
mut "$PROMPT" "$W/p_h8.txt" 'No image is built unless requirement 6 names one that copies the root lock.' 'Images may be built.'; ctl L8h 39 'the HOLDS' -- env G53_PROMPT="$W/p_h8.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                            ctl L10 31 'launch develop / the END_TREE' -- env G53_PROMPT="$W/p_dev.txt" "$L" --check
mut "$PROMPT" "$W/p_tier.txt" '#1369 T1 —' '#1369 T2 —';                                                              ctl L11 7 'the tier line' -- env G53_PROMPT="$W/p_tier.txt" "$L" --check
mut "$PROMPT" "$W/p_round.txt" 'a round-1 NO GO goes back to the author for round 2' 'a round-1 NO GO ships nothing';  ctl L11b 7 'the tiering rule' -- env G53_PROMPT="$W/p_round.txt" "$L" --check
mut "$PROMPT" "$W/p_tkt.txt" 'PR #1369 is KS-530' 'PR #1369 is KS-531';                                               ctl L12 32 "BOTH state the ticket" -- env G53_PROMPT="$W/p_tkt.txt" "$L" --check
mut "$PROMPT" "$W/p_a1.txt" 'MG-1 3 over 3 paths' 'MG-1 over the paths';                                              ctl L13 25 'the MERGE ADDENDUM rules' -- env G53_PROMPT="$W/p_a1.txt" "$L" --check
mut "$PROMPT" "$W/p_a2.txt" 'NOTHING to report.md after you send the verdict mail' 'little to report.md after you send the verdict mail'; ctl L13b 25 'REPORT-HASH-LAST' -- env G53_PROMPT="$W/p_a2.txt" "$L" --check
mut "$PROMPT" "$W/p_a3.txt" 'LOCK 1 removed 0 added 0 changed 0 flips' 'LOCK checked';                                ctl L13c 25 'the MERGE ADDENDUM rules' -- env G53_PROMPT="$W/p_a3.txt" "$L" --check
mut "$PROMPT" "$W/p_subj.txt" 'GATE53 #1369' 'GATE53 #1368';                                                          ctl L14 23 'the verdict subject' -- env G53_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                         ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
mut "$PROMPT" "$W/p_k1.txt" "$GS/lockdiff_1.out" "$GS/lockdiff_elsewhere.out";                                         ctl L16 8 'lockdiff_1.out is missing, empty, or not named' -- env G53_PROMPT="$W/p_k1.txt" "$L" --check
mut "$PROMPT" "$W/p_k2.txt" "briefs_staged/2026-10-02_answer_seatB54_method.md" "briefs_staged/2026-10-02_answer_elsewhere.md"; ctl L17 8 'the ruling / brief .*2026-10-02_answer_seatB54_method.md is missing, empty, or not named' -- env G53_PROMPT="$W/p_k2.txt" "$L" --check
mut "$PROMPT" "$W/p_k3.txt" '2026-10-01-batch1367-g52/report.md' '2026-10-01-batch1365-g51a/report.md';              ctl L18 8 'the previous round report' -- env G53_PROMPT="$W/p_k3.txt" "$L" --check
mut "$PROMPT" "$W/p_x1.txt" 'No live server is started, no Schemathesis is run, and no prisma dev server is started in this gate' 'A live server may be started'; ctl L20 34 'the NO-SERVER rule' -- env G53_PROMPT="$W/p_x1.txt" "$L" --check
mut "$PROMPT" "$W/p_x2.txt" 'AN OVERRIDE THAT MOVES THE LOCK BUT NOT THE EXECUTED CODE IS A FALSE FIX AND A BLOCKER' 'AN INERT OVERRIDE IS A NOTE';  ctl L21 36 'the REAL-FIX rule' -- env G53_PROMPT="$W/p_x2.txt" "$L" --check
mut "$PROMPT" "$W/p_x2b.txt" 'never from memory' 'from memory if need be';                                          ctl L21b 36 'the REAL-FIX rule' -- env G53_PROMPT="$W/p_x2b.txt" "$L" --check
mut "$PROMPT" "$W/p_x3.txt" 'You change no ticket state' 'You may move KS-530';                                      ctl L22 37 "the NOT-THE-GATE'S items" -- env G53_PROMPT="$W/p_x3.txt" "$L" --check
mut "$PROMPT" "$W/p_x4.txt" 'is at 95%' 'is fine';                                                                    ctl L23 38 'the proportionality line' -- env G53_PROMPT="$W/p_x4.txt" "$L" --check
mut "$PROMPT" "$W/p_x5.txt" 'EXPLAIN WHICH ADVISORIES STOPPED BEING REPORTED' 'EXPLAIN IF CONVENIENT';               ctl L24 35 'the 11 -> 9 rule' -- env G53_PROMPT="$W/p_x5.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate53.sh"
ctl R0  0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key outside reported_overlaps \| 12 expected overlap\(s\) reported \| 0 sequenced by Wednesday .*1 client-human PR\(s\) reported \| 3 kit path\(s\), 1 kit key\(s\)' -- cat "$W/R0.out"
ctl R0h 0 'CLIENT-HUMAN \(reported, never sequenced by a gate\) #1360 by PeterObeden' -- cat "$W/R0.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pins, 1 of 1' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                                ctl R1 1 'is not registered in inbox_routing.conf' -- env G53_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
echo '{}' > "$W/reported_empty.json"
ctl R2  15 "OVERLAP #1360 .*paths \[.*'Blockchain/Dev/package-lock.json'" -- env G53_REPORTED="$W/reported_empty.json" "$R" "$L" "$SP" --dry-run
ctl R3  15 "OVERLAP #995 .*title keys \['KS-741'\]" -- env G53_TITLE_KEY="KS-741" "$R" "$L" "$SP" --dry-run
printf '{"995": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H995" > "$W/seq_ok.json"
printf '{"995": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$H" > "$W/seq_bad.json"
ctl R3s 0 'SEQUENCED OUT-OF-KIT #995 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- env G53_TITLE_KEY="KS-741" G53_SEQUENCED="$W/seq_ok.json" "$R" "$L" "$SP" --dry-run
ctl R3w 15 'OVERLAP #995 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G53_TITLE_KEY="KS-741" G53_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
python3 -c 'import json,sys; r=json.load(open(sys.argv[1]))["reported_overlaps"]; r["1360"]=dict(r["1360"], head="0"*40); json.dump(r, open(sys.argv[2], "w"))' "$GS/kit.json" "$W/reported_moved.json"
ctl R3m 0 'EXPECTED OVERLAP .*#1360 PeterObeden \| head [0-9a-f]{12} \(HEAD MOVED since drafting: was 000000000000\)' -- env G53_REPORTED="$W/reported_moved.json" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #995 ' -- env G53_WIDEN_RX="ks-741-x-emitter" "$R" "$L" "$SP" --dry-run
sed "s/|$H|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh";                      ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1369|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G53_ROUTING="$W/routing_ok.conf" G53_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins, kit.json and the filled prompt are untouched by every control above"
ctl PNZ 0 '' -- test "$(SHA "$GS/pins_gate53.json")" = "$PINSHA"
ctl KJZ 0 '' -- test "$(SHA "$GS/kit.json")" = "$KITSHA"
ctl PRZ 0 '' -- test "$(SHA "$PROMPT")" = "$PRSHA"
echo "SUMMARY gate53: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
