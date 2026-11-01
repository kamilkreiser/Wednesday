#!/bin/bash
# Gate 70: place a probe file in originate's src/__tests__ for ONE run, run it under the app role, then move it to the
# scratchpad quarantine (nothing is deleted). usage: probe_run.sh <probe-file> <log-name> [extra jest args]
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate70-ks1384-r2b-1884
R=$G/repo
T=$R/Blockchain/Dev/services/originate/src/__tests__
Q=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c6cc71e2-d540-45eb-85fa-5aca0154bf77/scratchpad/g70/_quarantine_2026-11-01
mkdir -p "$Q"
SRC="$1"; NAME="$2"; shift 2
B=$(basename "$SRC")
[ "$(git -C "$R" rev-parse --show-toplevel)" = "$R" ] || { echo "REFUSE toplevel"; exit 9; }
[ -e "$T/$B" ] && { echo "REFUSE: $T/$B already present"; exit 8; }
cp "$SRC" "$T/$B"
echo "probe $B sha256 $(shasum -a 256 "$T/$B" | cut -d' ' -f1)" | tee "$G/evidence/$NAME.sha"
bash "$G/scripts/jest_run.sh" integ app "$G/evidence/$NAME" "src/__tests__/$B" "$@"; RC=$?
mv "$T/$B" "$Q/$(date +%H%M%S)_$B"
echo "[$NAME] rc=$RC"
grep -E "Tests:" "$G/evidence/$NAME"
grep -E "✕" "$G/evidence/$NAME"
exit $RC
