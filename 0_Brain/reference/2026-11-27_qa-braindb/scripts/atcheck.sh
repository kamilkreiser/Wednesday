#!/bin/bash
S=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/qa-braindb
P="$(cat "$S/PROC_LAST")"; R=/Volumes/DevMASTER/WEDNESDAY; SOCK=/tmp/qa-bdb-501-b
[ -d "$SOCK" ] || mkdir -m 700 "$SOCK"
X() { BRAINDB_ROOT="$R" BRAINDB_PGDATA="$P/c3" BRAINDB_SOCKDIR="$SOCK" WED_AGENT=wednesday /bin/bash "$R/2_Project_Files/brain-db/braindb.sh" "$@"; }
X up 2>&1 | tail -1 | awk '{print substr($0,1,110)}'
TR="$(/opt/homebrew/opt/postgresql@15/bin/psql -X -At -h "$SOCK" -d braindb -c "select distinct t from brain.rules, unnest(triggers) t order by 1")"
echo "triggers in the index: $(printf '%s\n' "$TR" | wc -l | tr -d ' ')"
norm() { /usr/bin/grep -i -E '^• ' | sed -E 's/^• \[[^]]*\] //; s/^\[seat regression\] //' | sort; }
ti=0; tc=0; onlyi=0; onlyc=0; top5diff=0
for t in $TR; do
  X at "$t" > "$P/at-i-$t.txt" 2> "$P/at-i-$t.err"; python3 -B "$R/2_Project_Files/tools/rules_card.py" --seat wednesday --at "$t" > "$P/at-c-$t.txt" 2> "$P/at-c-$t.err"; rc=$?
  norm < "$P/at-i-$t.txt" > "$P/at-i-$t.n"; norm < "$P/at-c-$t.txt" > "$P/at-c-$t.n"
  a=$(wc -l < "$P/at-i-$t.n" | tr -d ' '); b=$(wc -l < "$P/at-c-$t.n" | tr -d ' ')
  oi=$(comm -23 "$P/at-i-$t.n" "$P/at-c-$t.n" | wc -l | tr -d ' '); oc=$(comm -13 "$P/at-i-$t.n" "$P/at-c-$t.n" | wc -l | tr -d ' ')
  ti=$((ti+a)); tc=$((tc+b)); onlyi=$((onlyi+oi)); onlyc=$((onlyc+oc))
  printf '%-10s index %3s  card %3s  only-index %s  only-card %s  (card rc %s; headers: %s | %s)\n' "$t" "$a" "$b" "$oi" "$oc" "$rc" "$(head -1 "$P/at-i-$t.txt" | cut -c1-24)" "$(head -1 "$P/at-c-$t.txt" | cut -c1-24)"
done
echo "TOTAL rule lines: index $ti, card $tc ; only in the index $onlyi ; only on the card $onlyc"
X stop | tail -1 | awk '{print substr($0,1,50)}'
snap="$(ps -axww -o pid=,command=)"; echo "mine left: $(printf '%s\n' "$snap" | /usr/bin/grep -i -F -c -- "-D $S")"
mv -n "$SOCK" "$S/_quarantine_/qa-bdb-501-b-2"
