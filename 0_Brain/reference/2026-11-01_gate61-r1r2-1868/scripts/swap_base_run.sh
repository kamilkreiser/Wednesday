#!/bin/bash
# Gate 61: swap the three product files to a given commit, run the given jest jobs, restore head, verify sha256.
# usage: swap_base_run.sh <commit> <tag> <job>...   job = "<integ|unit>:<pattern>:<logname>"
set -u
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate61-r1r2-1868
R=$G/repo
HEAD_SHA=a46c251e1419d48bb8a50519e7ee0e306ad2fbe1
O=Blockchain/Dev/services/originate/src
FILES=("$O/routes/documents.ts" "$O/repositories/documentRepo.ts" "$O/services/reanchorInFlight.ts")
COMMIT="$1"; TAG="$2"; shift 2
[ "$(git -C "$R" rev-parse --show-toplevel)" = "$R" ] || { echo "REFUSE toplevel"; exit 9; }
: > "$G/evidence/head_product.sha256"
for f in "${FILES[@]}"; do shasum -a 256 "$R/$f" >> "$G/evidence/head_product.sha256"; done
for f in "${FILES[@]}"; do git -C "$R" show "$COMMIT:$f" > "$R/$f"; done
for job in "$@"; do
  KIND="${job%%:*}"; rest="${job#*:}"; PAT="${rest%%:*}"; NAME="${rest#*:}"
  bash "$G/scripts/jest_run.sh" "$KIND" app "$G/evidence/$NAME" "$PAT"; RC=$?
  echo "[$TAG] $NAME rc=$RC"
  grep -E "\[g61\]|Tests:|✕" "$G/evidence/$NAME"
done
for f in "${FILES[@]}"; do git -C "$R" show "$HEAD_SHA:$f" > "$R/$f"; done
shasum -a 256 -c "$G/evidence/head_product.sha256"; RC=$?
echo "restore-check rc=$RC"
git -C "$R" status --short -- Blockchain/Dev/services/originate/src/routes Blockchain/Dev/services/originate/src/repositories Blockchain/Dev/services/originate/src/services
