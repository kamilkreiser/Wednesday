#!/bin/bash
# usage: hash_tree.sh <label>  -> raw/hashes_<label>.txt ; read-only over the protected paths
W=/Volumes/DevMASTER/WEDNESDAY; Q=$W/2_Project_Files/qa-checks/wake-r4
out="$Q/raw/hashes_$1.txt"
{
  date
  for d in "$W/2_Project_Files/wake" "$W/0_Brain/reference/2026-11-27_qa-wake" "$W/0_Brain/reference/2026-11-27_qa-wake-r3"; do
    find "$d" -type f -not -name '*.pyc' -print0 | sort -z | xargs -0 shasum -a 256
  done
  shasum -a 256 "$W/0_Brain/tasks/EXPIRING-GRANTS.md" "$W/Launch_Wednesday.command" "$W/CLAUDE.md" "$W/0_Brain/CLAUDE.md" "$W"/0_Brain/tasks/NEXT-PICKUP*.md
} > "$out"
wc -l "$out"
