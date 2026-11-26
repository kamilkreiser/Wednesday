#!/bin/bash
# QA-POLICY-WORDS (h): card ids on added lines of a diff (stdin), each counted in the BASE BACKLOG.md
C=/private/tmp/claude-501/qpw/clone
grep -E '^\+' | grep -oE '[a-z]+-c2c-[a-z0-9-]+' | sort | uniq -c | while read n id; do
  b=$(git -C $C show 2004a04:BACKLOG.md | grep -c -F "$id")
  if [ "$b" -gt 0 ]; then echo "id $id added-occurrences=$n base-BACKLOG-lines=$b OLD"; else echo "id $id added-occurrences=$n base-BACKLOG-lines=0 NEW"; fi
done
