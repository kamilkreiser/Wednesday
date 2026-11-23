#!/bin/bash
# QA-R3 F-D: N in "Registered 0 hooks from N plugins" per committed debug.excerpt.log. usage: fd_count.sh <clone> <rev>
C=$1; R=$2; S=spikes/U-B1-hook-allow-silent
for f in $(git -C "$C" ls-tree -r --name-only "$R" -- $S/raw | grep '/debug.excerpt.log$'); do
  run=$(basename "$(dirname "$f")")
  ns=$(git -C "$C" show "$R:$f" | grep -o 'Registered [0-9]* hooks from [0-9]* plugins' | sed -E 's/.* from ([0-9]+) plugins/\1/' | sort -u | tr '\n' ',' | sed 's/,$//')
  k=$(git -C "$C" show "$R:$f" | grep -c 'Registered [0-9]* hooks from [0-9]* plugins')
  echo "$run N=$ns lines=$k"
done
