#!/bin/bash
# usage: mkwt.sh <clone> <worktree-path> <sha>
set -euo pipefail
C="$1"; W="$2"; SHA="$3"
CO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev'
[ "$(git -C "$C" rev-parse --show-toplevel)" = "$C" ] || { echo "toplevel mismatch"; exit 9; }
git -C "$C" worktree add -q --detach "$W" "$SHA"
D="$W/Blockchain/Dev"
mkdir "$D/node_modules"
for e in "$CO/node_modules/"* "$CO/node_modules/".bin "$CO/node_modules/".package-lock.json; do
  n="$(basename "$e")"
  [ "$n" = "@secuura" ] && continue
  ln -s "$e" "$D/node_modules/$n"
done
mkdir "$D/node_modules/@secuura"
for e in "$CO/node_modules/@secuura/"*; do ln -s "$(readlink "$e")" "$D/node_modules/@secuura/$(basename "$e")"; done
ln -s "$CO/services/originate/node_modules" "$D/services/originate/node_modules"
ln -s "$CO/packages/shared/node_modules" "$D/packages/shared/node_modules"
( cd "$D/packages/shared" && npx tsc ) && echo "shared built rc 0"
ls "$D/packages/shared/dist" | wc -l
