#!/bin/bash
# usage_gate_arms.sh — red-proof for usage_gate.sh: five arms, each with its expected rc.
# Arms live in a FILE (the 2026-09-14 no-rm lesson: a gate is red-proofed from a file, never
# from a command carrying the forbidden strings). Run: bash usage_gate_arms.sh → FAILS=<n>.
set -u
SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
GATE="$SELF_DIR/../usage_gate.sh"
T=$(mktemp -d "${TMPDIR:-/tmp}/usage_gate_arms.XXXXXX")
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
OLD=$(date -u -v-45M +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '45 minutes ago' +%Y-%m-%dT%H:%M:%SZ)
fails=0
arm() { # name file expected_rc [env...]
  local name="$1" file="$2" want="$3"; shift 3
  env "$@" USAGE_GATE_FILE="$file" bash "$GATE" > "$T/$name.out" 2>&1; local rc=$?
  if [ "$rc" -eq "$want" ]; then echo "PASS $name rc=$rc"; else echo "FAIL $name rc=$rc want=$want — $(tail -1 "$T/$name.out")"; fails=$((fails+1)); fi
}
printf '{"agent":"wednesday","pct":89,"resets_in":"5d","ts":"%s"}\n' "$NOW" > "$T/under.json"
printf '{"agent":"wednesday","pct":90,"resets_in":"5d","ts":"%s"}\n' "$NOW" > "$T/at.json"
printf '{"agent":"wednesday","pct":94,"resets_in":"5d","ts":"%s"}\n' "$NOW" > "$T/over.json"
printf '{"agent":"wednesday","pct":50,"resets_in":"5d","ts":"%s"}\n' "$OLD" > "$T/stale.json"
printf 'not json\n' > "$T/broken.json"
arm under  "$T/under.json"  0
arm at     "$T/at.json"     3
arm over   "$T/over.json"   3
arm stale  "$T/stale.json"  4
arm stale-allowed "$T/stale.json" 0 USAGE_GATE_ALLOW_STALE=1
arm broken "$T/broken.json" 4
arm missing "$T/absent.json" 4
arm custom-cut "$T/under.json" 3 WED_USAGE_STOP=85
echo "FAILS=$fails"
exit $fails
