#!/bin/bash
# night_brief_subdir_arms.sh — red-proof for night/build_input.sh BRIEF RESOLUTION (2026-10-10, night-brief-subdirs).
# A Wednesday brief may be a flat night/briefs/<T>.md OR a subdirectory night/briefs/<dir>/<T>.md (Spark shape).
#
#   B1  flat briefs/<T>.md still resolves as before                      (fixture copy)
#   B2  brief_dir=KS-1410-transfer-process-expired-500 -> that subdir's brief (fixture AND the real briefs dir, read-only)
#   B3  KS-1410, no pin, two KS-1410-* subdirs -> REFUSED rc 2 naming both (fixture AND real dir with its four)
#   B4  OLD script (.pre-1010-briefsubdir) on B2's input -> bare ticket (proves the arm discriminates)
#   B5  ticket with no brief anywhere -> bare-ticket `prompt source` warning unchanged
#
# NO dry-run mode in build_input.sh (it always reads Linear + git ls-remote). So: the NEW resolver is exercised through
# BUILD_INPUT_RESOLVE_ONLY=1 (exits before any .env/network read), and the python `prompt source` block (5c) is extracted
# verbatim from the script under test and run in isolation against the resolver's NIGHT_BRIEFS_DIR. The full build is NOT run.
# Writes only under $FX (a fresh dir under the session scratchpad). No rm. bash 3.2.
#
# Usage: bash night_brief_subdir_arms.sh [new builder] [old builder]     rc 0 only when every arm holds.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
NEW="${1:-$LM/night/build_input.sh}"
OLD="${2:-$LM/night/build_input.sh.pre-1010-briefsubdir}"
REAL_BRIEFS="$LM/night/briefs"
SP="${BRIEFSUBDIR_SCRATCH:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ce91ac93-c45e-4849-a76b-deff4ef72ffc/scratchpad/briefsubdir}"
FX="$SP/fx_$(date +%H%M%S)_$$"
mkdir -p "$FX/briefs/KS-1410-aaa-first" "$FX/briefs/KS-1410-bbb-second" "$FX/briefs/KS-1410-transfer-process-expired-500" \
         "$FX/flatonly" "$FX/none" || { echo "cannot make fixture dir $FX" >&2; exit 1; }
printf '## The exact change\nfixture-aaa\n' > "$FX/briefs/KS-1410-aaa-first/KS-1410.md"
printf '## The exact change\nfixture-bbb\n' > "$FX/briefs/KS-1410-bbb-second/KS-1410.md"
printf '## The exact change\nfixture-transfer\n' > "$FX/briefs/KS-1410-transfer-process-expired-500/KS-1410.md"
printf '## The exact change\nfixture-flat\n' > "$FX/flatonly/KS-777.md"

FAILS=0
ok()  { echo "PASS $1"; }
bad() { echo "FAIL $1"; FAILS=$((FAILS + 1)); }

# resolve <script> <briefs root> <ticket> [pins...] -> sets RES_OUT, RES_RC. Never starts a build.
resolve() {
  local script="$1" root="$2" t="$3"; shift 3
  RES_OUT="$(NIGHT_BRIEFS_DIR="$root" BUILD_INPUT_RESOLVE_ONLY=1 bash "$script" "$t" "$FX/out.json" "$@" 2>&1)"; RES_RC=$?
}
# prompt_source <script> <NIGHT_BRIEFS_DIR> <ticket> : run the script's own 5c block (verbatim) in isolation.
prompt_source() {
  local script="$1" bdir="$2" t="$3" blk="$FX/blk_$$.py"
  { printf 'import os, sys\nticket=%s\ndesc="TICKET-DESC"\n' "'$t'"
    awk '/^brief_path = /{p=1} p{print} /prompt source: the ticket description/{if(p) exit}' "$script"; } > "$blk"
  NIGHT_BRIEFS_DIR="$bdir" python3 "$blk" 2>&1
}
nbd() { echo "$1" | sed -n 's/^NIGHT_BRIEFS_DIR=//p' | tail -1; }

# ---- B1 flat still resolves
resolve "$NEW" "$FX/flatonly" KS-777
D="$(nbd "$RES_OUT")"; PS="$(prompt_source "$NEW" "$D" KS-777)"
if [ "$RES_RC" -eq 0 ] && [ "$D" = "$FX/flatonly" ] && echo "$RES_OUT" | /usr/bin/grep -q '(flat file)' \
   && echo "$PS" | /usr/bin/grep -q "prompt source: WEDNESDAY BRIEF $FX/flatonly/KS-777.md"; then ok "B1 flat briefs/<T>.md resolves unchanged"
else bad "B1 flat (rc=$RES_RC dir=$D ps=$PS)"; fi
# B1b: real flat brief, read-only
RT="$(ls "$REAL_BRIEFS" | /usr/bin/grep -E '^KS-[0-9]+\.md$' | head -1)"; RT="${RT%.md}"
if [ -n "$RT" ]; then resolve "$NEW" "$REAL_BRIEFS" "$RT"
  if [ "$RES_RC" -eq 0 ] && [ "$(nbd "$RES_OUT")" = "$REAL_BRIEFS" ]; then ok "B1b real flat brief $RT resolves to the briefs root"; else bad "B1b real flat $RT (rc=$RES_RC)"; fi
fi

# ---- B2 brief_dir pin
resolve "$NEW" "$FX/briefs" KS-1410 brief_dir=KS-1410-transfer-process-expired-500
D="$(nbd "$RES_OUT")"; PS="$(prompt_source "$NEW" "$D" KS-1410)"
if [ "$RES_RC" -eq 0 ] && echo "$PS" | /usr/bin/grep -q "prompt source: WEDNESDAY BRIEF $FX/briefs/KS-1410-transfer-process-expired-500/KS-1410.md" \
   && echo "$RES_OUT" | /usr/bin/grep -q 'named by the brief_dir= pin'; then ok "B2 brief_dir pin -> that subdir's brief (fixture)"
else bad "B2 fixture (rc=$RES_RC out=$RES_OUT ps=$PS)"; fi
resolve "$NEW" "$REAL_BRIEFS" KS-1410 brief_dir=KS-1410-transfer-process-expired-500
if [ "$RES_RC" -eq 0 ] && [ "$(nbd "$RES_OUT")" = "$REAL_BRIEFS/KS-1410-transfer-process-expired-500" ]; then ok "B2b brief_dir pin on the REAL briefs dir (read-only)"
else bad "B2b real (rc=$RES_RC out=$RES_OUT)"; fi
resolve "$NEW" "$FX/briefs" KS-1410 brief_dir=no-such-dir
if [ "$RES_RC" -eq 2 ] && echo "$RES_OUT" | /usr/bin/grep -q 'REFUSED'; then ok "B2c a pin naming a dir without the brief is REFUSED rc 2"; else bad "B2c bad pin (rc=$RES_RC)"; fi

# ---- B3 ambiguity refused
resolve "$NEW" "$FX/briefs" KS-1410 ; FXRC=$RES_RC; FXOUT="$RES_OUT"
# fixture has THREE KS-1410-* dirs; make exactly TWO for the stated arm by using a two-dir root
mkdir -p "$FX/two/KS-1410-aaa-first" "$FX/two/KS-1410-bbb-second"
cp "$FX/briefs/KS-1410-aaa-first/KS-1410.md" "$FX/two/KS-1410-aaa-first/KS-1410.md"; cp "$FX/briefs/KS-1410-bbb-second/KS-1410.md" "$FX/two/KS-1410-bbb-second/KS-1410.md"
resolve "$NEW" "$FX/two" KS-1410
if [ "$RES_RC" -eq 2 ] && echo "$RES_OUT" | /usr/bin/grep -q 'KS-1410-aaa-first' && echo "$RES_OUT" | /usr/bin/grep -q 'KS-1410-bbb-second' \
   && ! echo "$RES_OUT" | /usr/bin/grep -q '^NIGHT_BRIEFS_DIR='; then ok "B3 two subdirs, no pin -> REFUSED rc 2, both named, none picked"
else bad "B3 (rc=$RES_RC out=$RES_OUT)"; fi
if [ "$FXRC" -eq 2 ] && echo "$FXOUT" | /usr/bin/grep -q '3 brief subdirectories'; then ok "B3b three subdirs -> REFUSED, count stated"; else bad "B3b (rc=$FXRC)"; fi
resolve "$NEW" "$REAL_BRIEFS" KS-1410
if [ "$RES_RC" -eq 2 ] && echo "$RES_OUT" | /usr/bin/grep -q 'KS-1410-transfer-process-expired-500' && echo "$RES_OUT" | /usr/bin/grep -q 'KS-1410-apigw-notifications-500'; then ok "B3c REAL dir (4 KS-1410 subdirs, no pin) -> REFUSED naming them"
else bad "B3c real (rc=$RES_RC out=$RES_OUT)"; fi
# single subdir, no pin -> used and SAID (spec item: exactly one)
mkdir -p "$FX/one/KS-2000-only-one"; printf 'x\n' > "$FX/one/KS-2000-only-one/KS-2000.md"
resolve "$NEW" "$FX/one" KS-2000
if [ "$RES_RC" -eq 0 ] && [ "$(nbd "$RES_OUT")" = "$FX/one/KS-2000-only-one" ] && echo "$RES_OUT" | /usr/bin/grep -q 'ONLY brief subdirectory'; then ok "B3d exactly one subdir -> used and SAID in the log"
else bad "B3d (rc=$RES_RC out=$RES_OUT)"; fi

# ---- B4 OLD script on B2's input -> bare ticket
D_OLD="$FX/briefs"   # old script has no resolver: NIGHT_BRIEFS_DIR stays the root; the pin is ignored
PS="$(prompt_source "$OLD" "$D_OLD" KS-1410)"
if echo "$PS" | /usr/bin/grep -q 'prompt source: the ticket description'; then ok "B4 OLD script + B2 input -> bare ticket (arm discriminates)"; else bad "B4 (ps=$PS)"; fi
# and the OLD script's python really did ignore a brief_dir pin (pins dict only; no consumer)
if ! /usr/bin/grep -q 'brief_dir' "$OLD"; then ok "B4b OLD script has no brief_dir consumer"; else bad "B4b OLD already mentions brief_dir"; fi

# ---- B5 no brief anywhere -> bare-ticket warning unchanged
resolve "$NEW" "$FX/none" KS-9999
D="$(nbd "$RES_OUT")"; PS="$(prompt_source "$NEW" "$D" KS-9999)"; PSO="$(prompt_source "$OLD" "$FX/none" KS-9999)"
if [ "$RES_RC" -eq 0 ] && [ "$PS" = "$PSO" ] && echo "$PS" | /usr/bin/grep -q 'prompt source: the ticket description (no night/briefs/<ticket>.md)'; then ok "B5 no brief -> bare-ticket warning, byte-identical to OLD"
else bad "B5 (rc=$RES_RC new=$PS old=$PSO)"; fi

echo "fixtures: $FX"
[ "$FAILS" -eq 0 ] && { echo "ALL ARMS PASS"; exit 0; } || { echo "$FAILS ARM(S) FAILED"; exit 1; }
