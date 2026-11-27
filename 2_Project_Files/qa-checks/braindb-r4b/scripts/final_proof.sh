#!/bin/bash
# final_proof.sh: manifest again, compare with the one taken at 19:52; processes by executable with -D; my socket directories; git status.
Q=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/qa-checks/braindb-r4b
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/063b86e1-bf25-4ab6-9e57-b16c1f229efa/scratchpad/r4b
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db
date '+%Y-%m-%d %H:%M:%S %Z'
/bin/bash "$Q/scripts/manifest.sh" "$Q/raw/manifest_after.txt"
echo "manifest before: $(wc -l < "$Q/raw/manifest_before.txt" | tr -d ' ') lines, sha256 $(shasum -a 256 < "$Q/raw/manifest_before.txt" | cut -c1-16) ; after: $(wc -l < "$Q/raw/manifest_after.txt" | tr -d ' ') lines, sha256 $(shasum -a 256 < "$Q/raw/manifest_after.txt" | cut -c1-16)"
if cmp -s "$Q/raw/manifest_before.txt" "$Q/raw/manifest_after.txt"; then echo "IDENTICAL"; else echo "DIFFERENT; the differing lines (diff before after):"; diff "$Q/raw/manifest_before.txt" "$Q/raw/manifest_after.txt" | sed 's/^/   /' | cut -c1-260 | head -40; fi
echo "sections: $(/usr/bin/grep -c '^-- ' "$Q/raw/manifest_after.txt") (lane files, pgdata+quarantine+lock stat, first checker, second checker, brain learnings)"
echo "lane: postmaster.pid in pgdata-wednesday: $([ -e "$L/pgdata-wednesday/postmaster.pid" ] && echo PRESENT || echo absent) ; lane socket directory /tmp/wed-braindb-501-wednesday holds $(ls -A /tmp/wed-braindb-501-wednesday 2>&1 | wc -l | tr -d ' ') entries"
echo "-- every process whose EXECUTABLE is postgres and that carries -D (a postmaster), with its -D:"
snap="$(ps -axww -o pid=,comm=)"; n=0; mine=0; lane=0
while read -r pid comm; do
  case "${comm##*/}" in postgres)
    cmd="$(ps -ww -p "$pid" -o command=)"
    case "$cmd" in *" -D "*) n=$((n+1)); d="$(printf '%s' "$cmd" | sed -E 's/.* -D ([^ ]+).*/\1/')"; echo "   pid $pid -D $d"
      case "$d" in "$S"/*|"$Q"/*) mine=$((mine+1));; "$L"/*) lane=$((lane+1));; esac;; esac;;
  esac
done <<< "$snap"
echo "postmasters on this Mac: $n ; with -D under my scratch or my folder: $mine ; with -D in the lane: $lane (control: bash processes seen by the same snapshot: $(printf '%s\n' "$snap" | awk '{print $2}' | /usr/bin/grep -c -E '(^|/)bash$'))"
echo "postmaster.pid files under my scratch (outside base/): $(find "$S" -name postmaster.pid -not -path '*/base/*' 2>/dev/null | wc -l | tr -d ' ')"
echo "my socket directories under /tmp (q4*): $(ls -d /tmp/q4* 2>/dev/null | wc -l | tr -d ' ') ; entries inside them: $(ls -A /tmp/q4*/ 2>/dev/null | /usr/bin/grep -c -v -E '^(/tmp/q4.*:)?$')"
echo "-- git status of the tree (short), lines that are not the seat's earlier ones:"
git -C /Volumes/DevMASTER/WEDNESDAY status --short 2>&1 | cut -c1-150
