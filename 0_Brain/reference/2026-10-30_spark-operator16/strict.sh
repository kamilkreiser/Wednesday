#!/bin/bash
# strict.sh <briefdir>: git apply --check -p1 golden against tip files (git show), strict, rc must be 0
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/52e2783b-09e1-49d1-9200-c6e9ede3ba54/scratchpad/op16
TIP=${TIP:-7152ac669d2d6af08be5b9dcd35132818377155d}
g=$1/golden.diff
td=$(mktemp -d $S/strict.XXXXXX)
for p in $(/usr/bin/grep -E '^--- a/' $g | sed 's#^--- a/##'); do mkdir -p $td/$(dirname $p); git -C $S/src show $TIP:$p > $td/$p; done
git -C $td init -q 2>/dev/null
( git -C $td apply --check -p1 $g ); echo "strict git apply --check rc=$?"
