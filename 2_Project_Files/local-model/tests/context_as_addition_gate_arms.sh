#!/bin/bash
# Arms for the CONTEXT-AS-ADDITION GATE in tasks/bash_patch/build_bash_input.sh (2026-09-16 15:4x).
#
# The defect: a '+' line is a CLAIM that the line is not in the file. When a brief's '+' set repeats a
# line it also removes, that line is CONTEXT — the model emits the honest minimal hunk and B3b/A3c
# refuse a CORRECT output as "a dropped addition". Three instances in one day (KS-1089, KS-1168 twice,
# KS-998), the last written by Wednesday minutes after filing the rule against it. w=3 -> enforcement.
#
# Both arms run the REAL builder on REAL briefs. The one mutation is reversed and proven by checksum.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(cd "$HERE/.." && pwd)"
BUILD="$LM/tasks/bash_patch/build_bash_input.sh"
BRIEF="$LM/night/briefs/KS-998.md"
BAD="$BRIEF.pre-1545-minimalhunk"     # the version whose '+' side repeated two removed lines
TMP="${TMPDIR:-/tmp}/ctx_add_arms.$$"; mkdir -p "$TMP"
PASS=0; FAIL=0
ok()  { PASS=$((PASS+1)); echo "  PASS  $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL  $1"; }
build() { bash "$BUILD" KS-998 "$TMP/in.json" "$BRIEF" \
            product=systemTest/scripts/check-package-format.sh \
            ref=systemTest/__tests__/manifest_path.test.sh \
            test_file=systemTest/__tests__/package_format_gate.test.sh ctx=49152 > "$TMP/out" 2>&1; RC=$?; }

[ -f "$BAD" ] || { echo "SKIP — the pre-fix brief backup is gone; this arms file needs it as its red case"; exit 2; }
SUM="$(shasum -a 256 "$BRIEF" | awk '{print $1}')"
cp "$BRIEF" "$TMP/restore"

echo "ARM 1 — the PRE-FIX brief (two '+' lines identical to '-' lines) must be REFUSED"
cp "$BAD" "$BRIEF"; build; cp "$TMP/restore" "$BRIEF"
if [ "$RC" -eq 2 ] && grep -q 'are CONTEXT, not additions' "$TMP/out"; then ok "refused rc=2, cause named"
else bad "expected rc 2 + the named cause, got rc=$RC: $(tail -2 "$TMP/out" | tr '\n' ' ')"; fi

echo "ARM 2 — the brief is restored byte-for-byte"
[ "$SUM" = "$(shasum -a 256 "$BRIEF" | awk '{print $1}')" ] && ok "checksum identical" || bad "NOT restored"

echo "ARM 3 — the MINIMAL-hunk brief (context kept as context) builds (rc 0)"
build
if [ "$RC" -eq 0 ]; then ok "rc=0 — no over-fire on a correctly written hunk"
else bad "OVER-FIRE: the minimal brief was refused (rc=$RC): $(tail -2 "$TMP/out" | tr '\n' ' ')"; fi

echo "ARM 4 — the override lets a read-and-understood case through"
cp "$BAD" "$BRIEF"; ALLOW_CONTEXT_AS_ADDITION=1 build; cp "$TMP/restore" "$BRIEF"
if [ "$RC" -eq 0 ]; then ok "rc=0 with the override"
else bad "override did not work (rc=$RC): $(tail -2 "$TMP/out" | tr '\n' ' ')"; fi

echo "ARM 5 — restored again after ARM 4"
[ "$SUM" = "$(shasum -a 256 "$BRIEF" | awk '{print $1}')" ] && ok "checksum identical" || bad "NOT restored"

echo
echo "arms: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
