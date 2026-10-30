#!/bin/bash
# farm node_modules from the Secuura checkout INTO the clone; shared built in the clone. Read-only on source.
set -u
S="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev"
C=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator32/clone/Blockchain/Dev
farm(){ src="$1"; dst="$2"; shift 2; mkdir -p "$dst"; for n in $(ls -A "$src"); do skip=0; for s in "$@"; do [ "$n" = "$s" ] && skip=1; done; [ $skip = 1 ] && continue; [ -e "$dst/$n" ] || [ -L "$dst/$n" ] || ln -s "$src/$n" "$dst/$n"; done; }
farm "$S/node_modules" "$C/node_modules" .vite .package-lock.json @secuura
mkdir -p "$C/node_modules/.vite"
farm "$S/node_modules/@secuura" "$C/node_modules/@secuura" shared
ln -s ../../services/shared "$C/node_modules/@secuura/shared" 2>/dev/null
for ws in api-gateway shared; do farm "$S/services/$ws/node_modules" "$C/services/$ws/node_modules" .vite .package-lock.json; mkdir -p "$C/services/$ws/node_modules/.vite"; done
echo farmed
