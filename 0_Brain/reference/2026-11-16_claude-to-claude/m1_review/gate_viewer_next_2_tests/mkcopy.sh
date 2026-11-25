#!/bin/bash
# usage: mkcopy.sh <name> <sha>   -> $W/<name>/src (git archive of <sha>), $W/<name>/target (empty)
set -eu
W=/private/tmp/claude-501/qvx2; N="$1"; SHA="$2"
mkdir -p "$W/$N/src" "$W/$N/target"
git -C "$W/clone" archive "$SHA" | tar -x -C "$W/$N/src"
echo "$N $SHA $(date '+%F %T')" > "$W/$N/sha.txt"
