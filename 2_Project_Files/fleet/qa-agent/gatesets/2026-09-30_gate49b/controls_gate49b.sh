#!/bin/bash
# controls_gate49b.sh — every guard in the gate49b kit driven on the REAL subjects (#1357, #1359; the #1358 post-merge audit) and on PLANTED defects, each with the rc it
# must give and a WHY pattern its output must carry (a refusal for the wrong reason is a MISMATCH; a check that prints nothing is paired with a
# control that makes it print).
#   normal:   every control must read OK                      -> rc 0
#   --invert: every expectation is flipped; every control must MISMATCH (a control that still reads OK could not fail) -> rc 1
# Plants: synthetic commits in the SCRATCH clone only (plumbing: read-tree / update-index / write-tree / commit-tree under a temp index — never a
# worktree, never the checkout) and files under <scratchpad>/g49b_sp/controls_<HHMMSS>/. The kit's own files are never edited; the real
# pins_gate49b.json, kit.json and the filled prompt are sha256-checked unchanged at the end (PNZ, KJZ, PRZ). The launcher runs with --check
# (headless) except L9, the real launch path with stdin NOT a TTY (must refuse rc 21 before exec). The repin runs --dry-run, except R1 (a real run
# that must refuse at step 0, routing) and R8 (a real run with a routed temp file that must stop at G49B_STOP_AFTER_3B) — both stop long before the
# usage gate / cockpit. Mode plants RECORD a mode in a synthetic commit (update-index --cacheinfo <mode>): core.filemode is false.
# Each by-name keyword has its own launcher refusal (LK*): the keyword is broken into `<KW>-X`, which the launcher's TOKEN match must NOT accept.
# Shape copied from gate49a's controls, three PRs, plus this kit's disjointness / order / goldens / claims instruments.
# Usage: controls_gate49b.sh <scratchpad> [--invert]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"; SP="$1"; INV=0; [ "${2:-}" = "--invert" ] && INV=1
W="$SP/g49b_sp/controls_$(date -u +%H%M%S)"; mkdir -p "$W"
CL="$SP/g49b_sp/clone"; L="$GS/launch_qa_secuura_batch1357.sh"; PROMPT="$GS/2026-09-30_secuura-batch1357.prompt.txt"; CAP="$GS/mail_gate49b_ready.md"
PJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]));
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/pins_gate49b.json" "$1"; }
DEV="$(PJ develop)"; OLDDEV="$(git -C "$CL" rev-parse "$DEV^")"; END="$(PJ end_tree)"
H57="$(PJ prs.1357.head)"; H59="$(PJ prs.1359.head)"; REAL="1357=$H57,1359=$H59"
KJ() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): d=d[k]
print(d)' "$GS/kit.json" "$1"; }
H58="$(KJ post_merge_audit.head)"; M58="$(KJ post_merge_audit.merge_commit)"; MP58="$(KJ post_merge_audit.merge_first_parent)"
SHA() { shasum -a 256 "$1" | cut -c1-64; }
PINSHA="$(SHA "$GS/pins_gate49b.json")"; KITSHA="$(SHA "$GS/kit.json")"; PRSHA="$(SHA "$PROMPT")"
DSH='Blockchain/Dev/deployment/azure/deploy.sh'; CSM='Blockchain/Dev/deployment/azure/check-startup-migrations.sh'; SHL='Blockchain/Dev/packages/shared/package-lock.json'
KYC='Blockchain/Dev/services/kyc/package-lock.json'; ANA='Blockchain/Dev/services/analytics/package-lock.json'; BIL='Blockchain/Dev/services/billing/package-lock.json'
MB="$(PJ prs.1359.merge_base)"; SUB_B="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["subsets"]["Seat B 49th"]["tree"])' "$GS/pins_gate49b.json")"; STEP59="$(python3 -c 'import json,sys; print([s["tree"] for s in json.load(open(sys.argv[1]))["chain"] if s["pr"]=="1359"][0])' "$GS/pins_gate49b.json")"
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
  [ -z "${shown:-}" ] && shown="$(printf '%s' "$out" | grep -E 'FAIL|REFUS|PASS|OVERLAP|DISJOINT|all guards|DRY RUN COMPLETE|STOPPED|KEYSCAN|LOCKDELTA|OVERLAPS|CLAIMS|MODE' | tail -1)"
  printf 'CONTROL %-6s expect rc %s%s | got rc %s -> %s%s | %s\n' "$id" "$exp" "${why:+ /why '$why'}" "$rc" "$v" "$([ "$try" -gt 0 ] && echo " (after $try ssh-denied retry)")" "$(printf '%s' "$shown" | cut -c1-190)"
}
IDN=0
commitw() { # commitw <tree> <parent> <msg>
  GIT_AUTHOR_NAME=ctl GIT_AUTHOR_EMAIL=ctl@gate49b.invalid GIT_COMMITTER_NAME=ctl GIT_COMMITTER_EMAIL=ctl@gate49b.invalid GIT_AUTHOR_DATE=2026-09-30T00:00:00Z GIT_COMMITTER_DATE=2026-09-30T00:00:00Z \
    git -C "$CL" commit-tree "$1" -p "$2" -m "$3"
}
mkdev() { # mkdev <path> <transform> — a develop MOVE plant: a child of develop (for --develop simulations)
  local p="$1" tf="$2" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.dev.$IDN"
  git -C "$CL" show "$DEV:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || return 1
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$DEV"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$DEV" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$DEV" "gate49b control plant: develop move on $p"
}
restack() { # restack <subject head> <path> <transform> — the subject's own tree with ONE more path edited, parent = the subject's parent
  local h="$1" p="$2" tf="$3" idx nb tree; IDN=$((IDN + 1)); idx="$W/idx.rs.$IDN"
  git -C "$CL" show "$h:$p" | python3 -c 'import sys; s=sys.stdin.read(); exec(sys.argv[1]); sys.stdout.write(s)' "$tf" > "$W/blob.tmp" || { echo "PLANT TRANSFORM FAILED for $p" >&2; return 1; }
  nb="$(git -C "$CL" hash-object -w "$W/blob.tmp")"; GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"
  GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$(git -C "$CL" ls-tree "$h" -- "$p" | awk '{print $1}'),$nb,$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate49b control plant: $p over $h"
}
remode() { # remode <subject head> <path> <mode> — the subject's own tree with ONE path's RECORDED mode changed
  local h="$1" p="$2" mo="$3" idx tree; IDN=$((IDN + 1)); idx="$W/idx.rm.$IDN"
  GIT_INDEX_FILE="$idx" git -C "$CL" read-tree "$h"; GIT_INDEX_FILE="$idx" git -C "$CL" update-index --cacheinfo "$mo,$(git -C "$CL" rev-parse "$h:$p"),$p"; tree="$(GIT_INDEX_FILE="$idx" git -C "$CL" write-tree)"
  commitw "$tree" "$(git -C "$CL" rev-parse "$h^")" "gate49b control plant: $p recorded $mo"
}
mut() { # mut <src> <dst> <old> <new> — a literal replacement (python, no shell quoting), refusing when <old> is absent
  python3 -c 'import sys; s=open(sys.argv[1]).read(); assert sys.argv[3] in s, "mut: anchor absent: " + sys.argv[3]; open(sys.argv[2], "w").write(s.replace(sys.argv[3], sys.argv[4]))' "$@"
}
echo "=== controls_gate49b $([ $INV = 1 ] && echo '(INVERTED)') $(date -u +%Y-%m-%dT%H:%M:%SZ) | develop $DEV | develop^ $OLDDEV | #1357 $H57 | #1359 $H59 | audit #1358 $H58 merged as $M58 | END_TREE $END | merge-base $MB | plants $W"

echo "--- pin_gate49b.py (heads, shape, the move, DISJOINT, alone, the chain, every order, the subsets, RECORDED modes + controls, hooks, unchanged pins, claimed blobs, goldens) — simulations write pins_gate49b.SIM-<name>.json only"
PN="$GS/pin_gate49b.py"
ctl PN0  0 "PASS: FAIL=0 -> pins_gate49b.SIM-real.json \| develop ${DEV:0:12} \| END_TREE $END \| 2 PRs, 6 distinct paths, 0 shared \| 2 permutations agree" -- python3 "$PN" "$SP" --simulate real "$REAL"
ctl PN0e 0 "END_TREE $END \| diff\(develop, END\): 6 path\(s\) == the union of the own paths \(6\): True" -- cat "$W/PN0.out"
ctl PN0d 0 'DISJOINT SUMMARY: 1 pair\(s\), 0 shared path\(s\) \| 6 paths in total, 6 distinct' -- cat "$W/PN0.out"
ctl PN0r 0 "REVERSE-order END $END \| == END_TREE: True" -- cat "$W/PN0.out"
ctl PN0s 0 "SUBSET Seat B 49th only \\(#1357 #1359\\) -> tree $SUB_B \\|"' diff\(develop, tree\) == its own 6 path\(s\): True' -- cat "$W/PN0.out"
ctl PN0m 0 'MODE SUMMARY: 8 path\(s\) pinned \(6 PR, 2 control\), 8 OK' -- cat "$W/PN0.out"
ctl PN0g 0 "#1359 golden KS-1054-N-1350-7b on develop ${DEV:0:12}:"' Blockchain/Dev/scripts/__tests__/ks1054_deploy_all_rc1_message.test.sh .*BYTE-EQUAL' -- cat "$W/PN0.out"
ctl PN0t 0 "ORDER step #1359 on [0-9a-f]{12}: clean \\| tree $STEP59" -- cat "$W/PN0.out"
ctl PN0l 0 '#1357 Blockchain/Dev/deployment/azure/check-startup-migrations.sh: head blob a46419eb4163 \| claimed a46419eb4163 \| MATCH' -- cat "$W/PN0.out"
ctl PN1  1 'REFUSING: --develop is a controls-only override' -- python3 "$PN" "$SP" --develop "$OLDDEV"
P2="$(restack "$H59" "$CSM" 's = s + "\n# control\n"')"
ctl PN2  1 '\(D\) #1357 and #1359 share \[.Blockchain/Dev/deployment/azure/check-startup-migrations.sh.\]' -- python3 "$PN" "$SP" --simulate shared "1357=$H57,1359=$P2"
P3="$(remode "$H59" "$DSH" 100644)"
ctl PN3  1 '#1359 Blockchain/Dev/deployment/azure/deploy.sh: want 100755 \(pin\) \| head 100644 .*MODE MISMATCH' -- python3 "$PN" "$SP" --simulate m644 "1357=$H57,1359=$P3"
P4="$(restack "$H59" "$DSH" 's = s.replace("could not be verified", "could not be verifed", 1)')"
ctl PN4  1 '\(M\) #1359 Blockchain/Dev/deployment/azure/deploy.sh: golden \(golden base\) blob [0-9a-f]{12} != head blob' -- python3 "$PN" "$SP" --simulate gold "1357=$H57,1359=$P4"
P5="$(restack "$H59" "$SHL" 's = s.replace("\"lockfileVersion\": 3", "\"lockfileVersion\": 3 ", 1)')"
ctl PN5  1 '\(K\) Blockchain/Dev/packages/shared/package-lock.json is not byte-equal in every tree' -- python3 "$PN" "$SP" --simulate shlock "1357=$H57,1359=$P5"
P6="$(restack "$H57" "$CSM" 's = s + "\n# control\n"')"
ctl PN6  1 '\(L\) #1357 Blockchain/Dev/deployment/azure/check-startup-migrations.sh blob [0-9a-f]{12} != claimed a46419eb4163' -- python3 "$PN" "$SP" --simulate blob "1357=$P6,1359=$H59"
D7="$(mkdev "$DSH" 's = s + "\n# develop control move\n"')"
ctl PN7  1 '\(C\) #1359: the develop move touches its own path\(s\) \[.Blockchain/Dev/deployment/azure/deploy.sh.\]' -- python3 "$PN" "$SP" --simulate devmove "$REAL" --develop "$D7"
D8="$(mkdev 'Blockchain/Dev/BACKLOG.md' 's = s + "\n<!-- control -->\n"')"
ctl PN8  0 "#1359 move ${MB:0:12}\\.\\.[0-9a-f]{12}: [0-9]+ path\\(s\\) \\| reaches its own paths: NONE" -- python3 "$PN" "$SP" --simulate devunrel "$REAL" --develop "$D8"
ctl PN8p 0 'PASS: FAIL=0 -> pins_gate49b.SIM-devunrel.json' -- cat "$W/PN8.out"

echo "--- lockdelta_gate49b.py (the #1358 POST-MERGE AUDIT: head = the merge commit, base = its first parent; plants restack the merge commit)"
LD="$GS/lockdelta_gate49b.py"
ctl LD0  0 'LOCKDELTA PASS: 0 FAIL of 28 checks \| 27 moves \(1 PROD\), 15 locks, base 15 / head 0 disagreeing' -- python3 "$LD" "$SP"
ctl LD0p 0 'PRODUCTION moves .*: 1 \[.package-lock.json node_modules/@types/pg 8.20.0->8.23.1.\]' -- cat "$W/LD0.out"
ctl LD0a 0 'INFO L2 entries whose resolved / integrity were ABSENT at base and PRESENT at head: 2' -- cat "$W/LD0.out"
ctl LD0l 0 'PASS L8: every one of the 15 landed blobs at the merge [0-9a-f]{12} == #1358.s PR head [0-9a-f]{12} blob: yes \| CONTROL the base blob differs from the head for 15 of 15' -- cat "$W/LD0.out"
ctl LD0r 0 'L7 ROOT-lock copies .*: 0 .*CONTROL analytics Dockerfile COPY found: True' -- cat "$W/LD0.out"
P11="$(restack "$M58" "$KYC" 'import re; s = re.sub(r"(\"node_modules/@types/express\": \{\n\s+\"version\": \")[^\"]+", r"\g<1>4.17.99", s, count=1)')"
ctl LD1  1 'FAIL L2: 28 changed entr.*NO: .*services/kyc/package-lock.json.*node_modules/@types/express' -- python3 "$LD" "$SP" --head "$P11" --offline
ctl LD1b 0 'FAIL L8: every one of the 15 landed blobs .*NO: \[.Blockchain/Dev/services/kyc/package-lock.json.\]' -- cat "$W/LD1.out"
P12="$(restack "$M58" "$KYC" 's = s.replace("\"node_modules/@types/pg\": {\n      \"version\": \"8.23.1\"", "\"node_modules/@types/pg\": {\n      \"version\": \"8.20.0\"", 1)')"
ctl LD2  1 'FAIL L6: base: 15 of 27 disagree .* \| head: 1 of 27' -- python3 "$LD" "$SP" --head "$P12" --offline
ctl LD2t 0 'FAIL L3: 27 moves .*every to-version == packages/shared.s: False' -- cat "$W/LD2.out"
P13="$(restack "$M58" "$ANA" 's = s.replace("\"node_modules/@types/pg\": {\n      \"version\": \"8.23.1\",", "\"node_modules/@types/pg\": {\n      \"version\": \"8.23.1\",\n      \"optional\": true,", 1)')"
ctl LD3  1 'FAIL L2: 27 changed entr.*NO: .*services/analytics/package-lock.json' -- python3 "$LD" "$SP" --head "$P13" --offline
P14="$(restack "$M58" "$BIL" 'import re; s = re.sub(r"(\"node_modules/@types/pg\": \{\n\s+\"version\": \"8.23.1\",\n\s+\"resolved\": \"[^\"]+\",\n\s+\"integrity\": \"sha512-)(.)", lambda m: m.group(1) + ("A" if m.group(2) != "A" else "B"), s, count=1)')"
ctl LD4  1 'FAIL L5 @types/pg@8.23.1: 13 head entr' -- python3 "$LD" "$SP" --head "$P14"
ctl LD5  1 'FAIL L0: changed paths [0-9]+ == the kit.s 15 locks: False' -- python3 "$LD" "$SP" --head "$MP58" --offline

echo "--- overlaps_gate49b.py (carries its own three controls: CT-CLEAN / CT-CONFLICT / CT-AGREE)"
ctl OV0  0 'OVERLAPS READ: [0-9]+ PR\(s\) \(0 on the kit paths, [0-9]+ on the #1358 audit locks\) \| conflict today 1' -- env G49B_OVJSON="$W/ov.json" python3 "$GS/overlaps_gate49b.py" "$SP"
ctl OV0c 0 'CT-CLEAN .*: clean \| CT-CONFLICT .*: CONFLICT .*CT-AGREE .*: 1 disagreeing .*-> OK' -- cat "$W/OV0.out"
ctl OV0r 0 'AUDIT-ROW #1360 +PeterObeden' -- cat "$W/OV0.out"
ctl OV0p 0 '#649 .*today CONFLICT .*touches @types esc/pg: \[.package-lock.json:@types/pg.\]' -- cat "$W/OV0.out"

echo "--- keyscan_gate49b.py (subject, body, live surfaces, per PR)"
KS="$GS/keyscan_gate49b.py"
ctl KS0 0 'KEYSCAN PASS: 12 checks over 2 PR\(s\), 0 FAIL' -- python3 "$KS" "$SP"
ctl KS1 1 'FAIL #1357 S2' -- python3 "$KS" "$SP" --pr 1357 --subject 'KS-1054: a present but broken python3 fails closed on the startup check (#1357)'
ctl KS2 1 'FAIL #1357 S1: subject keys \[.KS-1054., .KS-1380.\]' -- python3 "$KS" "$SP" --pr 1357 --subject 'KS-1054: a broken python3 fails closed (KS-1380 unchanged)'
ctl KS3 1 'FAIL #1359 S3: declared 85, lands at 93' -- python3 "$KS" "$SP" --pr 1359 --subject 'KS-1054: rc 1 from the startup check reads as failed or unverified, not as failed, ok'
ctl KS4 1 'FAIL #1357 S1: subject keys \[.KS-10540.\]' -- python3 "$KS" "$SP" --pr 1357 --subject 'KS-10540: a present but broken python3 fails closed on the startup check'
printf 'Short body.\n' > "$W/body_norefs.txt";                        ctl KS5 1 'FAIL #1359 B1 KS-1054: `Refs KS-1054` lines: 0' -- python3 "$KS" "$SP" --pr 1359 --body-file "$W/body_norefs.txt"
printf 'Closes KS-1054\nRefs KS-1054\n' > "$W/body_close.txt";      ctl KS6 1 'FAIL #1359 B2: closing keyword' -- python3 "$KS" "$SP" --pr 1359 --body-file "$W/body_close.txt"
printf 'Refs KS-1054\nsee KS-1380\n' > "$W/body_foreign.txt";       ctl KS7 1 'FAIL #1357 B3: body key set \[.KS-1054., .KS-1380.\] \| foreign \[.KS-1380.\]' -- python3 "$KS" "$SP" --pr 1357 --body-file "$W/body_foreign.txt"
ctl KS8 0 'KEYSCAN PASS: 6 checks over 1 PR\(s\)' -- python3 "$KS" "$SP" --pr 1357 --subject 'KS-1054: deletes every migration and deploys to production'

echo "--- claims_gate49b.py (the ruling verbatim, the drafts, the anchors)"
ctl CL0 0 'CLAIMS READ: C1 ruling verbatim True \| 56 draft sentence\(s\)' -- env G49B_DRAFTS_OUT="$W/drafts_CL0.md" python3 "$GS/claims_gate49b.py" "$SP"
ctl CL0a 0 'C3 deploy.sh:857 .*develop: log_error .*FAILED — see above" \| PR head: # rc 1 is a failed count' -- cat "$W/CL0.out"
python3 -c 'import json,sys; b=json.load(open(sys.argv[1]))["prs"]["1357"]["body"]; assert "is not stopped" in b; open(sys.argv[2],"w").write(b.replace("is not stopped", "is not restarted"))' "$GS/gh_read_1.json" "$W/body1357_mut.md"
ctl CL1 1 'PROBLEM: C1: the ruling \(a\) is not verbatim' -- env G49B_DRAFTS_OUT="$W/drafts_CL1.md" python3 "$GS/claims_gate49b.py" "$SP" --prbody-1357 "$W/body1357_mut.md"

echo "--- the launcher (--check; L9 the real launch path, non-TTY)"
ctl L0  0 'all guards pass' -- "$L" --check
ctl L0n 0 '#1357 T1 236f9dce3898 compare ok \(behind [0-9]+\) \| #1359 T1 acac1f5e28ea compare ok \(behind [0-9]+\)' -- cat "$W/L0.out"
ctl L1  6 '#1359 — .* is not at .* AND refs/pull/1359/head' -- env G49B_HEAD_1359="$DEV" "$L" --check
ctl L2  17 'origin develop .* != the pinned develop' -- env G49B_CUR_DEV="$OLDDEV" "$L" --check
ctl L3  10 '#1359 — the compare is not the pinned' -- env G49B_PATHS_1359="$KYC" "$L" --check
mut "$PROMPT" "$W/p_go.txt" 'GO (Seat D 1st): merge 1357 1359 on gate49b' 'GO (Seat D 1st): merge 1357 on gate49b';   ctl L4 26 'merge authority / the GO string' -- env G49B_PROMPT="$W/p_go.txt" "$L" --check
mut "$PROMPT" "$W/p_ord.txt" 'in the order #1357 -> #1359, on the ONE GO' 'in any order, on the ONE GO';            ctl L4b 26 'the merge seat / the order' -- env G49B_PROMPT="$W/p_ord.txt" "$L" --check
mut "$PROMPT" "$W/p_seat.txt" 'The merge seat for both PRs is Seat D 1st' 'The merge seat for both PRs is Seat B 49th';  ctl L4c 26 'merge authority / the GO string / the merge seat' -- env G49B_PROMPT="$W/p_seat.txt" "$L" --check
{ cat "$PROMPT"; echo '{{UNFILLED}}'; } > "$W/p_tok.txt";                                                        ctl L5 8 'unfilled double-brace' -- env G49B_PROMPT="$W/p_tok.txt" "$L" --check
{ cat "$PROMPT"; echo 'merge #<PR>'; } > "$W/p_ph.txt";                                                         ctl L5b 8 'unpinned PR placeholder' -- env G49B_PROMPT="$W/p_ph.txt" "$L" --check
i=0
for kw in POST-MERGE-AUDIT MERGED-BEFORE-GATE CLEAN-MERGE DISJOINT END-TREE ORDER-INDEPENDENT MODES EXEC-BITS COLLISION-CENSUS BEHAVIOUR-1357 RED-FIRST-1357 PREDICATE-CONTRACT CALLERS-READ RULING-VERBATIM BEHAVIOUR-1359 GOLDENS-BYTE-EQUAL RED-FIRST-1359 NO-COUNTER-CHANGE MESSAGE-TRUE IMAGE-BUILDS LOCK-DELTA-15 LANDED-EQUALS-HEAD DEPENDENT-RANGES REGISTRY-TRUE LOCK-AGREEMENT AUDIT-LEGS-DEVELOP TSC-NOT-A-RED-PROOF SUITES SHELL-RUNNER SHARED-BUILT-FIRST SUBJECT-KEY-SCAN SUBJECT-LANDS-AT SUBJECT-TRUE-OF-DIFF REFS-OWN-KEY NO-CLOSING-KEYWORD PR-BODY-CLAIMS DRAFTED-COMMENTS NO-REPEAT-49AFF833 FOLLOW-ONS FUSE-COUNT OUT-OF-SCOPE TIERING DISK-ENOSPC REPORT-HASH-LAST; do
  i=$((i + 1)); python3 -c 'import re,sys; s=open(sys.argv[1]).read(); open(sys.argv[2],"w").write(re.sub(r"(?<![A-Za-z0-9-])%s(?![A-Za-z0-9-])" % re.escape(sys.argv[3]), sys.argv[3] + "-X", s))' "$PROMPT" "$W/p_kw$i.txt" "$kw"
  ctl "LK$i" 33 "by-name keyword '$kw'" -- env G49B_PROMPT="$W/p_kw$i.txt" "$L" --check
done
sed "s/$H59/${H59:0:39}x/g" "$CAP" > "$W/cap_noh.md";                                                           ctl L7 20 "do not both name #1359's head" -- env G49B_BRIEF="$W/cap_noh.md" "$L" --check
mut "$PROMPT" "$W/p_h1.txt" 'NO ticket filed' 'NO tickets filed';                                                    ctl L8 39 'the HOLDS' -- env G49B_PROMPT="$W/p_h1.txt" "$L" --check
mut "$PROMPT" "$W/p_h2.txt" 'You NEVER reply to Peter' 'You may reply to Peter';                                     ctl L8b 39 'the HOLDS' -- env G49B_PROMPT="$W/p_h2.txt" "$L" --check
mut "$PROMPT" "$W/p_h3.txt" 'Never read or write a real `.env`' 'Never write a real `.env`';                         ctl L8c 39 'the HOLDS' -- env G49B_PROMPT="$W/p_h3.txt" "$L" --check
mut "$PROMPT" "$W/p_h4.txt" 'Docker runs are `--rm --network none` with the source mounted READ-ONLY' 'Docker runs are `--rm`'; ctl L8d 39 'the HOLDS' -- env G49B_PROMPT="$W/p_h4.txt" "$L" --check
mut "$PROMPT" "$W/p_h5.txt" 'No `az` command of any kind' 'No `az login`';                                          ctl L8e 39 'the HOLDS' -- env G49B_PROMPT="$W/p_h5.txt" "$L" --check
mut "$PROMPT" "$W/p_h6.txt" '`deploy.sh` / `deploy-all.sh` are NEVER run whole' '`deploy.sh` / `deploy-all.sh` are run whole';  ctl L8f 39 'the HOLDS' -- env G49B_PROMPT="$W/p_h6.txt" "$L" --check
mut "$PROMPT" "$W/p_h7.txt" 'THE NAMED EXCEPTIONS to those holds — these and NO others' 'THE NAMED EXCEPTIONS to those holds'; ctl L8g 39 'the HOLDS' -- env G49B_PROMPT="$W/p_h7.txt" "$L" --check
mut "$PROMPT" "$W/p_h8.txt" 'NEVER `up`, `down`' '`up`, `down`';                                                     ctl L8h 39 'the HOLDS' -- env G49B_PROMPT="$W/p_h8.txt" "$L" --check
mut "$PROMPT" "$W/p_h9.txt" '"no lock regenerated" means no REAL lock' '"no lock regenerated" means little';        ctl L8i 39 'the HOLDS' -- env G49B_PROMPT="$W/p_h9.txt" "$L" --check
if [ -t 0 ]; then echo "CONTROL L9     SKIPPED — stdin is a TTY here, the real launch path would exec -> MISMATCH"; TOT=$((TOT + 1)); MM=$((MM + 1)); else
ctl L9 21 'stdin is not a TTY' -- "$L" < /dev/null; fi
sed "s/$DEV/${DEV:0:39}x/g" "$PROMPT" > "$W/p_dev.txt";                                                            ctl L10 31 'launch develop / the END_TREE' -- env G49B_PROMPT="$W/p_dev.txt" "$L" --check
mut "$PROMPT" "$W/p_tier.txt" '#1359 T1 —' '#1359 T2 —';                                                              ctl L11 7 'the tier lines' -- env G49B_PROMPT="$W/p_tier.txt" "$L" --check
mut "$PROMPT" "$W/p_round.txt" 'a round-1 NO GO goes back to the author for round 2' 'a round-1 NO GO ships nothing';  ctl L11b 7 'the tiering rule' -- env G49B_PROMPT="$W/p_round.txt" "$L" --check
mut "$PROMPT" "$W/p_frz.txt" 'The gate is FROZEN at TWO PRs' 'The gate is open to more PRs';                       ctl L11c 7 'FROZEN at TWO' -- env G49B_PROMPT="$W/p_frz.txt" "$L" --check
mut "$PROMPT" "$W/p_tkt.txt" 'PR #1359 is KS-1054' 'PR #1359 is KS-1055';                                             ctl L12 32 "state 'PR #1359 is KS-1054'" -- env G49B_PROMPT="$W/p_tkt.txt" "$L" --check
sed 's/#1358 is KS-1380/#1358 is KS-1381/' "$CAP" > "$W/cap_tkt.md";                                               ctl L12b 32 "state 'PR #1358 is KS-1380'" -- env G49B_BRIEF="$W/cap_tkt.md" "$L" --check
mut "$PROMPT" "$W/p_a1.txt" 'MG-1 2 over 2 then 4 over 4 paths' 'MG-1 over the paths';                                             ctl L13 25 'the MERGE ADDENDUM rules' -- env G49B_PROMPT="$W/p_a1.txt" "$L" --check
mut "$PROMPT" "$W/p_a2.txt" 'NOTHING to report.md after you send the verdict mail' 'little to report.md after you send the verdict mail'; ctl L13b 25 'REPORT-HASH-LAST' -- env G49B_PROMPT="$W/p_a2.txt" "$L" --check
mut "$PROMPT" "$W/p_a3.txt" 'EVERY SUBJECT YOU PROPOSE MUST BE TRUE OF THE DIFF' 'EVERY SUBJECT YOU PROPOSE SHOULD FIT THE DIFF'; ctl L13c 25 'the MERGE ADDENDUM rules' -- env G49B_PROMPT="$W/p_a3.txt" "$L" --check
mut "$PROMPT" "$W/p_a4.txt" 'ONE LINE, naming EACH PR' 'ONE LINE PER SEAT';                                                          ctl L13d 25 'the MERGE ADDENDUM rules' -- env G49B_PROMPT="$W/p_a4.txt" "$L" --check
mut "$PROMPT" "$W/p_a5.txt" 'tree <per-step tree>' 'tree <END>';                                 ctl L13e 25 'the MERGE ADDENDUM rules' -- env G49B_PROMPT="$W/p_a5.txt" "$L" --check
mut "$PROMPT" "$W/p_subj.txt" 'GATE49B #1357 #1359 (' 'GATE49B #1357 (';                                        ctl L14 23 'the verdict subject' -- env G49B_PROMPT="$W/p_subj.txt" "$L" --check
cp "$L" "$W/launch_moved.sh"; chmod +x "$W/launch_moved.sh";                                                         ctl L15 2 'a MOVED KIT' -- "$W/launch_moved.sh" --check
mut "$PROMPT" "$W/p_k1.txt" "$GS/claims_1.out" "$GS/claims_elsewhere.out";                                             ctl L16 8 'claims_1.out is missing, empty, or not named' -- env G49B_PROMPT="$W/p_k1.txt" "$L" --check
mut "$PROMPT" "$W/p_k2.txt" "$GS/drafts_gate49b.md" "$GS/drafts_elsewhere.md";                                         ctl L17 8 'drafts_gate49b.md is missing, empty, or not named' -- env G49B_PROMPT="$W/p_k2.txt" "$L" --check
mut "$PROMPT" "$W/p_k3.txt" '2026-09-30-batch1356-g49a/report.md' '2026-09-30-batch1355-g48b/report.md.x';            ctl L18 8 'the previous round report' -- env G49B_PROMPT="$W/p_k3.txt" "$L" --check
mut "$PROMPT" "$W/p_k4.txt" "$GS/gh_body_1359.md" "$GS/gh_body_elsewhere.md";                                          ctl L19 8 'gh_body_1359.md is missing, empty, or not named' -- env G49B_PROMPT="$W/p_k4.txt" "$L" --check
mut "$PROMPT" "$W/p_x1.txt" 'A NOT MEASURED behaviour line on a T1 PR is not a GO' 'A NOT MEASURED behaviour line is noted';  ctl L20 34 'the BEHAVIOUR-FIRST rule' -- env G49B_PROMPT="$W/p_x1.txt" "$L" --check
mut "$PROMPT" "$W/p_x2.txt" 'The 09-09 baseline grant is NOT used.' 'The 09-09 baseline grant is used.';               ctl L21 36 'the authority line' -- env G49B_PROMPT="$W/p_x2.txt" "$L" --check
mut "$PROMPT" "$W/p_x3.txt" 'THE LEG-14 TRAP (SHARED-BUILT-FIRST)' 'THE LEG-14 NOTE (SHARED-BUILT-FIRST)';              ctl L22 37 'the LEG-14 trap' -- env G49B_PROMPT="$W/p_x3.txt" "$L" --check
mut "$PROMPT" "$W/p_x4.txt" 'with no judgement words' 'plainly';                                                      ctl L24 40 'the POST-MERGE AUDIT section' -- env G49B_PROMPT="$W/p_x4.txt" "$L" --check
mut "$PROMPT" "$W/p_x7.txt" 'as a merge commit, before any gate.' 'as a merge commit.';                             ctl L24b 40 'its verbatim statement' -- env G49B_PROMPT="$W/p_x7.txt" "$L" --check
mut "$PROMPT" "$W/p_x8.txt" 'The #1358 audit writes NO GO' 'The #1358 audit may write a GO';                    ctl L24c 40 'the POST-MERGE AUDIT section' -- env G49B_PROMPT="$W/p_x8.txt" "$L" --check
mut "$PROMPT" "$W/p_x5.txt" 'Nothing is posted by you.' 'Post what is true.';                                          ctl L23 38 'the client-comment rule' -- env G49B_PROMPT="$W/p_x5.txt" "$L" --check
mut "$PROMPT" "$W/p_x6.txt" 'every sentence carries its instrument or "unmeasured"' 'most sentences carry an instrument'; ctl L23b 38 'the client-comment rule' -- env G49B_PROMPT="$W/p_x6.txt" "$L" --check

echo "--- the launch action (repin: --dry-run; R1 and R8 real runs that stop before the usage gate)"
R="$GS/repin_and_launch_gate49b.sh"
ctl R0  0 'DRY RUN COMPLETE' -- "$R" "$L" "$SP" --dry-run
ctl R0c 0 'CENSUS [0-9]+ other open PR\(s\) read \| 0 touch a kit path or carry a kit key outside reported_overlaps \| 0 expected overlap\(s\) reported \| 0 sequenced by Wednesday .*[0-9]+ client-human PR\(s\) reported \| 6 kit path\(s\), 1 kit key\(s\)' -- cat "$W/R0.out"
ctl R0e 0 '0 expected overlap\(s\) reported' -- cat "$W/R0.out"
ctl R0b 0 'BOTH INSTRUMENTS AGREE with the pin, 2 of 2' -- cat "$W/R0.out"
: > "$W/routing_empty.conf";                                                ctl R1 1 'is not registered in inbox_routing.conf' -- env G49B_ROUTING="$W/routing_empty.conf" "$R" "$L" "$SP"
ctl R2 15 'OVERLAP #649 .*paths \[.Blockchain/Dev/package-lock.json.\]' -- env G49B_OVERLAP_EXTRA='Blockchain/Dev/package-lock.json' "$R" "$L" "$SP" --dry-run
ctl R3  15 'OVERLAP #1360 .*title keys \[.KS-1380.\]' -- env G49B_TITLE_KEY="KS-1380" "$R" "$L" "$SP" --dry-run
H60="$(python3 -c '
import json, urllib.request
t = [l.split("=",1)[1].strip().strip(chr(34)).strip(chr(39)) for l in open("/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env") if l.startswith("GH_TOKEN=")][0]
print(json.load(urllib.request.urlopen(urllib.request.Request("https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/1360", headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))["head"]["sha"])')"   # RE-READ here: Peter pushes to #1360 (it moved mid-run in the superseded run 2)
echo "  #1360 head re-read immediately before R3s: $H60"
printf '{"1360": {"head": "%s", "ruling": "CONTROL stand-in, not a ruling"}}\n' "$H60" > "$W/seq_ok.json"
printf '{"1360": {"head": "%s", "ruling": "CONTROL stand-in at a WRONG head"}}\n' "$H57" > "$W/seq_bad.json"
ctl R3s 0 'SEQUENCED OUT-OF-KIT #1360 .*head [0-9a-f]{12} == the head Wednesday sequenced' -- env G49B_TITLE_KEY="KS-1380" G49B_SEQUENCED="$W/seq_ok.json" "$R" "$L" "$SP" --dry-run
ctl R3c 0 'DRY RUN COMPLETE' -- cat "$W/R3s.out"
ctl R3w 15 'OVERLAP #1360 .*SEQUENCED at head [0-9a-f]{12} but now [0-9a-f]{12} — refused' -- env G49B_TITLE_KEY="KS-1380" G49B_SEQUENCED="$W/seq_bad.json" "$R" "$L" "$SP" --dry-run
ctl R4  0 'DISJOINT OUT-OF-KIT #125[03] ' -- env G49B_WIDEN_RX="-l5-1$" "$R" "$L" "$SP" --dry-run
sed "s/|$H59|/|$DEV|/" "$L" > "$W/launcher_wronghead.sh"; chmod +x "$W/launcher_wronghead.sh";                    ctl R5 11 'a head moved' -- "$R" "$W/launcher_wronghead.sh" "$SP" --dry-run
sed "s/^DEVELOP_SHA='$DEV'$/DEVELOP_SHA='$OLDDEV'/" "$L" > "$W/launcher_olddev.sh"; chmod +x "$W/launcher_olddev.sh"; ctl R6 10 'develop MOVED since the fill' -- "$R" "$W/launcher_olddev.sh" "$SP" --dry-run
ctl R7  9 'must be a Claude session scratchpad' -- "$R" "$L" /tmp/not-a-scratchpad --dry-run
echo "QA/Secuura-batch1357|coagent@agentmail.to|yes" > "$W/routing_ok.conf"; ctl R8 0 'STOPPED AFTER 3b' -- env G49B_ROUTING="$W/routing_ok.conf" G49B_STOP_AFTER_3B=1 "$R" "$L" "$SP"
ctl R8r 0 'line present: 1 \(grep rc=0' -- cat "$W/R8.out"
n_rout="$(ls "$GS"/launch_[0-9]*.routing.out 2>/dev/null | wc -l | tr -d ' ')"; echo "  (R1 / R8 real runs wrote their step outputs as $GS/launch_<HHMMSS>.* — $n_rout routing file(s) now; kept, never deleted)"

echo "--- the real pins, kit.json and the filled prompt are untouched by every control above"
ctl PNZ 0 '' -- test "$(SHA "$GS/pins_gate49b.json")" = "$PINSHA"
ctl KJZ 0 '' -- test "$(SHA "$GS/kit.json")" = "$KITSHA"
ctl PRZ 0 '' -- test "$(SHA "$PROMPT")" = "$PRSHA"
echo "SUMMARY gate49b: $TOT controls, OK $OK, MISMATCH $MM | ssh-denied retries $RETRIES$([ $INV = 1 ] && echo ' (inverted: every control must MISMATCH; an OK here is a control that could not fail)')"
if [ "$INV" = 1 ]; then [ "$OK" = 0 ] && exit 1 || exit 2; else [ "$MM" = 0 ] && exit 0 || exit 1; fi
