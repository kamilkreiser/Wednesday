#!/bin/bash
# doc_d8d9_arms.sh — red-proof for the doc checker's D8 (every brief '+' line present EXACTLY) and D9 (an insert-only block
# follows its named "Insert AFTER line N" anchor), 2026-09-16 00:0x, row 99. All arms on REAL run artefacts:
#   1 KS-1049 A r1 (the false green: backticks dropped, bullet placed below the paragraph) → FAIL D8 + D9
#   2 KS-1035 D r1 (exact lines) under the CURRENT reanchor                                  → PASS 8/8 (D8 + D9 green)
#   3 the same KS-1035 output under the OLD reanchor (.pre-0915-blankoffset)                  → FAIL D9 (misplaced by a blank)
#   3c control for 3: the same scratch tree with the CURRENT reanchor                        → PASS 8/8 (so 3 is the reanchor)
# REWRITTEN 2026-09-17 (row "D9 vacuous on a blank anchor"): the 09-16 version could not run as written — it checked against
# the runs' night clones (gone) and built its inputs from the MOVING origin tip, and its ARM3 swapped the LIVE
# tasks/code_patch/reanchor.py in place. Now: the inputs are built by the real builder against a PINNED origin (a scratch bare
# repo whose develop = the runs' recorded tip 48e65c435, objects borrowed read-only from the source checkout); the checker
# runs on a scratch clone at that tip; ARM3 runs a scratch COPY of the doc_patch task tree with the old reanchor beside it.
# Nothing outside the work dir is written. Backup of the old script: doc_d8d9_arms.sh.pre-0917-d9blank.
# Env: ARMS_WORK (default mktemp -d) · ARMS_NEW (checker under test, default tasks/doc_patch/checker.sh) · ARMS_BUILDER
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
T=$LM/tasks/doc_patch; RC_=$LM/tasks/code_patch
CHK="${ARMS_NEW:-$T/checker.sh}"; BLD="${ARMS_BUILDER:-$T/build_doc_input.sh}"
W="${ARMS_WORK:-$(mktemp -d)}"; mkdir -p "$W"
SRC=/Volumes/DevMASTER/\!CODING/Secuura/Blockchain/2_Project_Files
R49=$LM/runs/2026-09-15_ks1049-ornith35b-night; R35=$LM/runs/2026-09-15_ks1035-ornith35b-night
B49=$LM/night/briefs/split_1049A/KS-1049.md; B35=$LM/night/briefs/split_1035D/KS-1035.md
for f in "$CHK" "$BLD" "$T/anchor_restore.py" "$T/d6_ranges.py" "$RC_/reanchor.py" "$RC_/reanchor.py.pre-0915-blankoffset" "$R49/out.md" "$R49/input.json" "$R35/out.md" "$R35/input.json" "$B49" "$B35"; do
  [ -f "$f" ] || { echo "ARM SETUP FAIL: missing $f"; exit 1; }
done
TIP="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["tip"])' "$R49/input.json")"
[ "$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["tip"])' "$R35/input.json")" = "$TIP" ] || { echo "ARM SETUP FAIL: the two runs are not at one tip"; exit 1; }
[ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" = "commit" ] || { echo "ARM SETUP FAIL: $TIP is not a local commit in $SRC"; exit 1; }
[ ! -e "$W/pin_origin.git" ] && [ ! -e "$W/pin_src" ] && [ ! -e "$W/clone" ] || { echo "ARM SETUP FAIL: $W is not fresh"; exit 1; }
{
  git init -q --bare "$W/pin_origin.git" && echo "$SRC/.git/objects" > "$W/pin_origin.git/objects/info/alternates" &&
  git -C "$W/pin_origin.git" update-ref refs/heads/develop "$TIP" &&
  git clone -q --shared --no-checkout "$SRC" "$W/pin_src" && git -C "$W/pin_src" remote set-url origin "$W/pin_origin.git" &&
  git clone -q --shared --no-checkout "$SRC" "$W/clone" && git -C "$W/clone" checkout -q --detach "$TIP"
} > "$W/setup.log" 2>&1 || { echo "ARM SETUP FAIL: pinned origin / clone (see $W/setup.log)"; exit 1; }
[ "$(git -C "$W/pin_src" ls-remote origin refs/heads/develop | awk '{print $1}')" = "$TIP" ] || { echo "ARM SETUP FAIL: pinned origin develop != $TIP"; exit 1; }
[ "$(git -C "$W/clone" rev-parse HEAD)" = "$TIP" ] || { echo "ARM SETUP FAIL: clone not at $TIP"; exit 1; }

NIGHT_SOURCE_CHECKOUT="$W/pin_src" bash "$BLD" KS-1049 "$W/in49.json" "$B49" product=Blockchain/Dev/CONTRIBUTING.md ctx=32768 > "$W/build49.out" 2>&1; rc=$?
[ "$rc" -eq 0 ] || { echo "ARM SETUP FAIL: build 1049 rc=$rc: $(head -1 "$W/build49.out")"; exit 1; }
NIGHT_SOURCE_CHECKOUT="$W/pin_src" bash "$BLD" KS-1035 "$W/in35.json" "$B35" product=Blockchain/Dev/docs/DEV-PROCESS.md ctx=32768 > "$W/build35.out" 2>&1; rc=$?
[ "$rc" -eq 0 ] || { echo "ARM SETUP FAIL: build 1035 rc=$rc: $(head -1 "$W/build35.out")"; exit 1; }
for n in 49 35; do [ "$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["tip"])' "$W/in$n.json")" = "$TIP" ] || { echo "ARM SETUP FAIL: in$n.json not at $TIP"; exit 1; }; done

# scratch task trees: the checker under test beside its helpers, with the OLD and the CURRENT reanchor
for v in old cur; do
  mkdir -p "$W/tree_$v/doc_patch" "$W/tree_$v/code_patch"
  cp "$CHK" "$W/tree_$v/doc_patch/checker.sh"; cp "$T/anchor_restore.py" "$T/d6_ranges.py" "$W/tree_$v/doc_patch/"
done
cp "$RC_/reanchor.py.pre-0915-blankoffset" "$W/tree_old/code_patch/reanchor.py"; cp "$RC_/reanchor.py" "$W/tree_cur/code_patch/reanchor.py"

fail=0; npass=0
chk() { # chk <checker> <input> <run dir> <arm> → CRC; report $W/<arm>/checker.out (out.md COPIED, run dirs never written)
  mkdir -p "$W/$4"; cp "$3/out.md" "$W/$4/out.md"
  bash "$1" "$2" "$W/$4/out.md" "$W/clone" > "$W/$4/checker.out" 2>&1; CRC=$?
  [ -z "$(git -C "$W/clone" status --porcelain --untracked-files=no)" ] || { echo "ARM SETUP FAIL: the checker left the clone modified after $4"; exit 1; }
}
v() { /usr/bin/grep -m1 '^RESULT:' "$W/$1/checker.out"; }
bad() { echo "ARM$1 FAIL — $2"; /usr/bin/grep -E '^(FAIL|RESULT)' "$W/$1/checker.out" 2>/dev/null | cut -c1-200 | sed 's/^/    /'; fail=1; }

chk "$CHK" "$W/in49.json" "$R49" 1
if [ "$CRC" -eq 1 ] && /usr/bin/grep -q '^FAIL D8' "$W/1/checker.out" && /usr/bin/grep -q '^FAIL D9' "$W/1/checker.out"; then echo "ARM1 PASS (1049 r1 → rc 1, FAIL D8 + D9; $(v 1))"; npass=$((npass+1)); else bad 1 "rc=$CRC"; fi
chk "$CHK" "$W/in35.json" "$R35" 2
if [ "$CRC" -eq 0 ] && [ "$(v 2)" = "RESULT: PASS (8/8)" ]; then echo "ARM2 PASS (1035 r1 → rc 0, PASS 8/8)"; npass=$((npass+1)); else bad 2 "rc=$CRC"; fi
chk "$W/tree_old/doc_patch/checker.sh" "$W/in35.json" "$R35" 3
if [ "$CRC" -eq 1 ] && /usr/bin/grep -q '^FAIL D9' "$W/3/checker.out"; then echo "ARM3 PASS (old reanchor, scratch tree → rc 1, FAIL D9; $(v 3))"; npass=$((npass+1)); else bad 3 "rc=$CRC"; fi
chk "$W/tree_cur/doc_patch/checker.sh" "$W/in35.json" "$R35" 3c
if [ "$CRC" -eq 0 ] && [ "$(v 3c)" = "RESULT: PASS (8/8)" ]; then echo "ARM3c PASS (control: current reanchor, same scratch tree → rc 0, PASS 8/8)"; npass=$((npass+1)); else bad 3c "rc=$CRC"; fi
echo "doc_d8d9_arms: $npass/4 arms passed (work dir $W)"
exit $fail
