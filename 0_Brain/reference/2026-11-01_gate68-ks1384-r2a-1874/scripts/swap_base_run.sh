#!/bin/bash
# Gate 68 (adapted from gate 65): swap the delta's originate product files to a given commit, run the given jest jobs,
# restore the head, verify sha256. usage: swap_base_run.sh <commit> <tag> <job>...   job = "<integ|unit>:<pattern>:<logname>"
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate68-ks1384-r2a-1874
R=$G/repo
HEAD_SHA=31d1466788bea96f6175b595c8fb3078229668be
O=Blockchain/Dev/services/originate/src
FILES=("$O/routes/documents.ts" "$O/repositories/documentRepo.ts" "$O/services/reanchorInFlight.ts")
COMMIT="$1"; TAG="$2"; shift 2
[ "$(git -C "$R" rev-parse --show-toplevel)" = "$R" ] || { echo "REFUSE toplevel"; exit 9; }
: > "$G/evidence/head_product.sha256"
for f in "${FILES[@]}"; do git -C "$R" show "$HEAD_SHA:$f" | shasum -a 256 | sed "s#-#$R/$f#" >> "$G/evidence/head_product.sha256"; done
shasum -a 256 -c "$G/evidence/head_product.sha256" || { echo "REFUSE not at head before swap"; exit 8; }
for f in "${FILES[@]}"; do git -C "$R" show "$COMMIT:$f" > "$R/$f"; done
for f in "${FILES[@]}"; do echo "swapped $f -> $(git -C "$R" show "$COMMIT:$f" | shasum -a 256 | cut -c1-12) on disk $(shasum -a 256 "$R/$f" | cut -c1-12)"; done
for job in "$@"; do
  KIND="${job%%:*}"; rest="${job#*:}"; PAT="${rest%%:*}"; NAME="${rest#*:}"
  bash "$G/scripts/jest_run.sh" "$KIND" app "$G/evidence/$NAME" "$PAT"; RC=$?
  echo "[$TAG] $NAME rc=$RC"
  grep -E "\[g6[58]\]|Tests:|✕" "$G/evidence/$NAME"
done
for f in "${FILES[@]}"; do git -C "$R" show "$HEAD_SHA:$f" > "$R/$f"; done
shasum -a 256 -c "$G/evidence/head_product.sha256"; RC=$?
echo "restore-check rc=$RC"
git -C "$R" status --short -- Blockchain/Dev/services/originate/src/routes Blockchain/Dev/services/originate/src/repositories Blockchain/Dev/services/originate/src/services
