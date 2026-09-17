#!/bin/bash
# doc_d9_blank_arms.sh — red-proof for "doc tier D9 vacuous on a BLANK anchor" (2026-09-17; proposal H1 in
# runs/2026-09-16_rebriefs-docs-evidence/ornith_rebriefs_REPORT.md). Two changes, backups `.pre-0917-d9blank`:
#   H1  tasks/doc_patch/build_doc_input.sh REFUSES (rc 2) an "Insert AFTER line N" whose tip line N is blank/whitespace-only,
#       naming the nearest non-blank neighbours.
#   D9  tasks/doc_patch/checker.sh: an input whose anchor is blank (built before H1) is held on the nearest NON-blank line
#       above + the same blank count + tip line N+1 below, with the '+' lines (blanks included) one contiguous run.
#       A non-blank anchor never enters that branch: its output must be byte-identical to the OLD checker's.
# Everything is SYNTHETIC (tests/fixtures/doc_d9_blank/, no client file): a throwaway git origin + checkout + clone is made
# in the work dir so the REAL builder runs unchanged (NIGHT_SOURCE_CHECKOUT, `ls-remote origin develop`).
#   ARM1  blank-anchor brief → NEW builder REFUSED naming :15/:17; control: OLD builder rc 0 on the same brief
#   ARM2a non-blank anchor (non-blank neighbours), correct placement → NEW builder rc 0; NEW PASS (8/8) == OLD byte-for-byte
#   ARM2b the same input, bullet one line low → FAIL D9, NEW == OLD byte-for-byte (non-blank path unchanged)
#   ARM2c the same input, '+' line altered → FAIL D8, NEW == OLD byte-for-byte
#   ARM3a legacy blank-anchor input (OLD builder), insert two paragraphs low → NEW FAIL D9 BLANK ANCHOR; OLD PASS (8/8)
#   ARM3b legacy input, KS-987 slide (two blanks above, none below)          → NEW FAIL D9 BLANK ANCHOR; OLD PASS (8/8)
#   ARM3c legacy input, an extra blank BELOW the insert                        → NEW FAIL D9 BLANK ANCHOR; OLD PASS (8/8)
#   ARM3d legacy input, CORRECT placement (the KS-866 shape)                   → NEW PASS (8/8) naming the held line; OLD PASS
#   ARM4  non-blank anchor whose neighbours are BLANK, leading blank '+'        → NEW builder rc 0; NEW PASS (8/8) == OLD
#   ARM5  tests/doc_anchor_restore_arms.sh with ARMS_NEW=<new checker>          → rc 0, 10/10
# Env: ARMS_WORK (default mktemp -d) · ARMS_NEW / ARMS_OLD (checkers) · ARMS_NEW_BUILDER / ARMS_OLD_BUILDER · ARMS_SKIP5=1
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
T=$LM/tasks/doc_patch; FX=$LM/tests/fixtures/doc_d9_blank; PROD=docs/GUIDE.md
NEW="${ARMS_NEW:-$T/checker.sh}"; OLD="${ARMS_OLD:-$T/checker.sh.pre-0917-d9blank}"
NEWB="${ARMS_NEW_BUILDER:-$T/build_doc_input.sh}"; OLDB="${ARMS_OLD_BUILDER:-$T/build_doc_input.sh.pre-0917-d9blank}"
W="${ARMS_WORK:-$(mktemp -d)}"; mkdir -p "$W"
for f in "$NEW" "$OLD" "$NEWB" "$OLDB" "$FX/GUIDE.md" "$FX/brief_blank_anchor.md" "$FX/brief_nonblank_anchor.md" "$FX/brief_blank_neighbour.md"; do
  [ -f "$f" ] || { echo "ARM SETUP FAIL: missing $f"; exit 1; }
done
cmp -s "$NEW" "$OLD" && { echo "ARM SETUP FAIL: NEW and OLD checker are the same file content"; exit 1; }

# synthetic origin (bare) + source checkout (the builder's NIGHT_SOURCE_CHECKOUT) + checker clone, all under $W
[ ! -e "$W/origin.git" ] && [ ! -e "$W/src" ] && [ ! -e "$W/clone" ] || { echo "ARM SETUP FAIL: $W is not fresh (use a new ARMS_WORK)"; exit 1; }
export GIT_AUTHOR_NAME=arms GIT_AUTHOR_EMAIL=arms@example.invalid GIT_COMMITTER_NAME=arms GIT_COMMITTER_EMAIL=arms@example.invalid
export GIT_AUTHOR_DATE="2026-09-17T00:00:00+0000" GIT_COMMITTER_DATE="2026-09-17T00:00:00+0000"
{
  git init -q --bare "$W/origin.git" && git init -q "$W/src" && mkdir -p "$W/src/docs" && cp "$FX/GUIDE.md" "$W/src/$PROD" &&
  git -C "$W/src" checkout -q -b develop && git -C "$W/src" add "$PROD" && git -C "$W/src" commit -q -m "synthetic guide" &&
  git -C "$W/src" remote add origin "$W/origin.git" && git -C "$W/src" push -q origin develop
} > "$W/setup.log" 2>&1 || { echo "ARM SETUP FAIL: synthetic repo (see $W/setup.log)"; exit 1; }
TIP="$(git -C "$W/src" rev-parse HEAD)"
[ "$(git -C "$W/src" ls-remote origin refs/heads/develop | awk '{print $1}')" = "$TIP" ] || { echo "ARM SETUP FAIL: origin develop != $TIP"; exit 1; }
git clone -q --shared --no-checkout "$W/src" "$W/clone" >> "$W/setup.log" 2>&1 && git -C "$W/clone" checkout -q --detach "$TIP" >> "$W/setup.log" 2>&1 || { echo "ARM SETUP FAIL: clone"; exit 1; }
cmp -s "$W/clone/$PROD" "$FX/GUIDE.md" || { echo "ARM SETUP FAIL: clone product differs from the fixture"; exit 1; }
export NIGHT_SOURCE_CHECKOUT="$W/src"

npass=0; fail=0; N=10
ok()  { echo "ARM $1 PASS — $2"; npass=$((npass+1)); }
bad() { echo "ARM $1 FAIL — $2"; fail=1; }
build() { # build <builder> <brief> <name> → rc in BRC, stderr+stdout in $W/<name>.build.out
  bash "$1" SYN-1 "$W/$3.json" "$FX/$2" product=$PROD > "$W/$3.build.out" 2>&1; BRC=$?
}
ia_of() { python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["defect_line"]["insert_after"])' "$1" 2>/dev/null; }
chk() { # chk <checker> <input name> <out fixture> <arm dir> → CRC; report at $W/<arm dir>/checker.out
  mkdir -p "$W/$4"; cp "$FX/$3" "$W/$4/out.md"
  bash "$1" "$W/$2.json" "$W/$4/out.md" "$W/clone" > "$W/$4/checker.out" 2>&1; CRC=$?
  [ -z "$(git -C "$W/clone" status --porcelain --untracked-files=no)" ] || { echo "ARM SETUP FAIL: the checker left the clone modified after $4"; exit 1; }
}
v() { /usr/bin/grep -m1 '^RESULT:' "$W/$1/checker.out"; }
d9() { /usr/bin/grep -m1 -E '^(PASS|FAIL|INFO) D9' "$W/$1/checker.out" | cut -c1-200; }

# ARM1 — H1 refusal, with the OLD builder as its control
build "$NEWB" brief_blank_anchor.md in_blank_new; RC_NEW=$BRC
build "$OLDB" brief_blank_anchor.md in_blank_old; RC_OLD=$BRC
if [ "$RC_NEW" -eq 2 ] && [ ! -f "$W/in_blank_new.json" ] \
   && /usr/bin/grep -q "REFUSED — 'Insert AFTER line 16' names a BLANK line" "$W/in_blank_new.build.out" \
   && /usr/bin/grep -q "above is line 15 ('- Rotate the logs weekly.')" "$W/in_blank_new.build.out" \
   && /usr/bin/grep -q "below is line 17 ('Check the health endpoint" "$W/in_blank_new.build.out" \
   && [ "$RC_OLD" -eq 0 ] && [ "$(ia_of "$W/in_blank_old.json")" = "16" ]; then
  ok 1 "blank anchor → NEW builder rc 2 REFUSED naming :15 above / :17 below, no input written; control OLD builder rc 0 (insert_after 16)"
else bad 1 "NEW rc=$RC_NEW ($(head -1 "$W/in_blank_new.build.out" | cut -c1-160)) / OLD rc=$RC_OLD ia=$(ia_of "$W/in_blank_old.json")"; fi

# ARM2 — non-blank anchor with non-blank neighbours: NEW builder builds; checker verdicts byte-identical to OLD
build "$NEWB" brief_nonblank_anchor.md in_nonblank; RC2=$BRC
if [ "$RC2" -ne 0 ] || [ "$(ia_of "$W/in_nonblank.json")" != "14" ]; then
  bad 2a "NEW builder rc=$RC2 on the non-blank brief: $(head -1 "$W/in_nonblank.build.out" | cut -c1-160)"; bad 2b "no input"; bad 2c "no input"
else
  chk "$NEW" in_nonblank out_nonblank_correct.md 2a_new; C_NEW=$CRC; chk "$OLD" in_nonblank out_nonblank_correct.md 2a_old; C_OLD=$CRC
  if [ "$C_NEW" -eq 0 ] && [ "$(v 2a_new)" = "RESULT: PASS (8/8)" ] && d9 2a_new | /usr/bin/grep -q '^PASS D9' && cmp -s "$W/2a_new/checker.out" "$W/2a_old/checker.out"; then
    ok 2a "non-blank anchor :14, correct → NEW builder rc 0; NEW rc 0 $(v 2a_new), byte-identical to OLD (rc $C_OLD)"
  else bad 2a "NEW rc=$C_NEW $(v 2a_new) [$(d9 2a_new)] / OLD rc=$C_OLD $(v 2a_old)"; fi
  chk "$NEW" in_nonblank out_nonblank_misplaced.md 2b_new; C_NEW=$CRC; chk "$OLD" in_nonblank out_nonblank_misplaced.md 2b_old; C_OLD=$CRC
  if [ "$C_NEW" -eq 1 ] && d9 2b_new | /usr/bin/grep -q '^FAIL D9 INSERT MISPLACED' && cmp -s "$W/2b_new/checker.out" "$W/2b_old/checker.out"; then
    ok 2b "non-blank anchor, one line low → NEW rc 1 FAIL D9, byte-identical to OLD (rc $C_OLD)"
  else bad 2b "NEW rc=$C_NEW [$(d9 2b_new)] / OLD rc=$C_OLD [$(d9 2b_old)]"; fi
  chk "$NEW" in_nonblank out_nonblank_altered.md 2c_new; C_NEW=$CRC; chk "$OLD" in_nonblank out_nonblank_altered.md 2c_old; C_OLD=$CRC
  if [ "$C_NEW" -eq 1 ] && /usr/bin/grep -q '^FAIL D8 ADDITION ALTERED' "$W/2c_new/checker.out" && cmp -s "$W/2c_new/checker.out" "$W/2c_old/checker.out"; then
    ok 2c "non-blank anchor, '+' line altered → NEW rc 1 FAIL D8, byte-identical to OLD (rc $C_OLD)"
  else bad 2c "NEW rc=$C_NEW $(v 2c_new) / OLD rc=$C_OLD $(v 2c_old)"; fi
fi

# ARM3 — the LEGACY blank-anchor input (OLD builder, as every input built before H1): misplaced inserts the OLD checker
# PASSES must FAIL D9 by name on the NEW checker; the correct placement must stay PASS on both
if [ "$RC_OLD" -ne 0 ]; then for a in 3a 3b 3c 3d; do bad $a "no legacy input (OLD builder rc=$RC_OLD)"; done
else
  arm3_red() { # arm3_red <arm> <fixture> <label>
    chk "$NEW" in_blank_old "$2" "$1_new"; local cn=$CRC; chk "$OLD" in_blank_old "$2" "$1_old"; local co=$CRC
    if [ "$cn" -eq 1 ] && [ "$(v "$1_new")" = "RESULT: FAIL (1 failed)" ] && d9 "$1_new" | /usr/bin/grep -q '^FAIL D9 INSERT MISPLACED — BLANK ANCHOR' \
       && [ "$co" -eq 0 ] && [ "$(v "$1_old")" = "RESULT: PASS (8/8)" ] && d9 "$1_old" | /usr/bin/grep -q "^PASS D9 .*tip line 16: ''"; then
      ok "$1" "$3 → NEW rc 1 $(v "$1_new") at D9 BLANK ANCHOR; OLD (negative control) rc 0 $(v "$1_old") on tip line 16: ''"
    else bad "$1" "$3: NEW rc=$cn $(v "$1_new") [$(d9 "$1_new")] / OLD rc=$co $(v "$1_old") [$(d9 "$1_old")]"; fi
  }
  arm3_red 3a out_blank_misplaced_far.md "insert two paragraphs low (after :18)"
  arm3_red 3b out_blank_double_above.md "KS-987 slide: two blanks above, none below"
  arm3_red 3c out_blank_double_below.md "an extra blank below the insert"
  chk "$NEW" in_blank_old out_blank_correct.md 3d_new; C_NEW=$CRC; chk "$OLD" in_blank_old out_blank_correct.md 3d_old; C_OLD=$CRC
  if [ "$C_NEW" -eq 0 ] && [ "$(v 3d_new)" = "RESULT: PASS (8/8)" ] && d9 3d_new | /usr/bin/grep -q "^PASS D9 .*BLANK ANCHOR held on a non-blank line (tip line 16 is blank; held on tip line 15: '- Rotate the logs weekly.' + 1 blank" \
     && [ "$C_OLD" -eq 0 ] && [ "$(v 3d_old)" = "RESULT: PASS (8/8)" ]; then
    ok 3d "legacy blank-anchor input, CORRECT placement → NEW rc 0 $(v 3d_new) held on :15 + 1 blank; OLD rc 0 $(v 3d_old)"
  else bad 3d "NEW rc=$C_NEW $(v 3d_new) [$(d9 3d_new)] / OLD rc=$C_OLD $(v 3d_old)"; fi
fi

# ARM4 — no over-fire: a non-blank anchor with BLANK neighbours and a leading blank '+' line
build "$NEWB" brief_blank_neighbour.md in_neighbour; RC4=$BRC
if [ "$RC4" -eq 0 ] && [ "$(ia_of "$W/in_neighbour.json")" = "11" ]; then
  chk "$NEW" in_neighbour out_neighbour_correct.md 4_new; C_NEW=$CRC; chk "$OLD" in_neighbour out_neighbour_correct.md 4_old; C_OLD=$CRC
  if [ "$C_NEW" -eq 0 ] && [ "$(v 4_new)" = "RESULT: PASS (8/8)" ] && d9 4_new | /usr/bin/grep -q '^PASS D9' && ! /usr/bin/grep -q 'BLANK ANCHOR' "$W/4_new/checker.out" && cmp -s "$W/4_new/checker.out" "$W/4_old/checker.out"; then
    ok 4 "anchor :11 with blank :10/:12, leading blank '+' → NEW builder rc 0; NEW rc 0 $(v 4_new), byte-identical to OLD (rc $C_OLD)"
  else bad 4 "NEW rc=$C_NEW $(v 4_new) [$(d9 4_new)] / OLD rc=$C_OLD $(v 4_old)"; fi
else bad 4 "NEW builder rc=$RC4 on a non-blank anchor with blank neighbours (H1 over-fire): $(head -1 "$W/in_neighbour.build.out" | cut -c1-200)"; fi

# ARM5 — the anchor-restore arms (real KS-890/1036/789 artefacts) on the NEW checker
if [ "${ARMS_SKIP5:-0}" = "1" ]; then echo "ARM 5 SKIPPED (ARMS_SKIP5=1)"; N=9
else
  mkdir -p "$W/arm5"
  ARMS_WORK="$W/arm5/work" ARMS_NEW="$NEW" bash "$LM/tests/doc_anchor_restore_arms.sh" > "$W/arm5/out" 2>&1; R5=$?
  if [ "$R5" -eq 0 ] && /usr/bin/grep -q '^doc_anchor_restore_arms: 10/10 arms passed' "$W/arm5/out"; then
    ok 5 "doc_anchor_restore_arms.sh on the NEW checker → rc 0, 10/10"
  else bad 5 "doc_anchor_restore_arms.sh rc=$R5: $(tail -3 "$W/arm5/out" | tr '\n' ' ' | cut -c1-240)"; fi
fi
echo "doc_d9_blank_arms: $npass/$N arms passed (work dir $W)"
exit $fail
