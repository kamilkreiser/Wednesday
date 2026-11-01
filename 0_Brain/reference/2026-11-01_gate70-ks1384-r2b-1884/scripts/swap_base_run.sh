#!/bin/bash
# Gate 70 (adapted from gate 68's): swap EVERY originate product file the delta modifies to a given commit, run the given
# probe jobs (each placed for its run only, by probe_run.sh), restore the head, verify sha256.
# The delta's three NEW originate files (anchorRead.ts, anchorResolution.ts, ownCreateClient.ts) stay on disk: at the base
# nothing imports them (checked by grep below, logged).
# usage: swap_base_run.sh <commit> <tag> <job>...   job = "<probe-src-path>|<logname>"
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate70-ks1384-r2b-1884
R=$G/repo
HEAD_SHA=ecfe4f07fdcec78b8d45d897bd4dccd4be829be7
O=Blockchain/Dev/services/originate/src
FILES=("$O/routes/documents.ts" "$O/repositories/documentRepo.ts" "$O/services/reanchorInFlight.ts" "$O/services/anchorStateSync.ts"
       "$O/routes/verification.ts" "$O/routes/verificationV2.ts" "$O/originate.openapi.ts")
COMMIT="$1"; TAG="$2"; shift 2
[ "$(git -C "$R" rev-parse --show-toplevel)" = "$R" ] || { echo "REFUSE toplevel"; exit 9; }
SUMS="$G/evidence/head_product_$TAG.sha256"
: > "$SUMS"
for f in "${FILES[@]}"; do git -C "$R" show "$HEAD_SHA:$f" | shasum -a 256 | sed "s#-#$R/$f#" >> "$SUMS"; done
shasum -a 256 -c "$SUMS" || { echo "REFUSE not at head before swap"; exit 8; }
for f in "${FILES[@]}"; do git -C "$R" show "$COMMIT:$f" > "$R/$f"; done
for f in "${FILES[@]}"; do echo "swapped $f -> $(git -C "$R" show "$COMMIT:$f" | shasum -a 256 | cut -c1-12) on disk $(shasum -a 256 "$R/$f" | cut -c1-12)"; done
echo "importers of the new files at the swapped base (expect none outside the new files and tests):"
grep -rln "anchorResolution\|ownCreateClient\|services/anchorRead\|'./anchorRead'" "$R/$O" --include='*.ts' | grep -v __tests__ || echo "  none"
for job in "$@"; do
  SRC="${job%%|*}"; NAME="${job#*|}"
  bash "$G/scripts/probe_run.sh" "$SRC" "$NAME"; RC=$?
  echo "[$TAG] $NAME rc=$RC"
done
for f in "${FILES[@]}"; do git -C "$R" show "$HEAD_SHA:$f" > "$R/$f"; done
shasum -a 256 -c "$SUMS"; RC=$?
echo "restore-check rc=$RC"
git -C "$R" status --short
