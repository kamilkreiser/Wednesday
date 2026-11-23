#!/bin/bash
# own scan: added lines of base...head (and clarifications file) vs classes; prefixes derived from the session logs
W=/private/tmp/claude-501/qsf/clone; B=3164374a8a20d73296558997438b97a41a7837ad; H=663c93eccd4f758379973f8f2b6c26b1fc7bab59
REF=/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude
CL="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/1_Project_Definition/CLARIFICATIONS.md"
ADDED=$(git -C $W diff $B...$H | grep -E '^\+[^+]')
# id prefixes: every >=32-hex run in the sources -> first 8 chars; plus 8-hex after mailbox/session/channel words
IDS=$(cat $REF/windows/2026-11-23_WO-7_part2_results.md $REF/windows/2026-11-23_WO-14_*.md $REF/windows/2026-11-23_WO-1[012]_results.md $REF/c1_session_2026-11-23/*.log $REF/c1_session_2026-11-23/*.json $REF/c2_session_2026-11-23/*.log "/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/5_Project_History/STATUS_C2_REHEARSAL.md" \
 | grep -o -E '[0-9a-f]{32,64}' | cut -c1-8 | sort -u)
IDS2=$(cat $REF/windows/*.md $REF/c?_session_2026-11-23/*.log | grep -o -i -E '(mailbox|session|channel|joined session|key id) [0-9a-f]{8}' | grep -o -E '[0-9a-f]{8}$' | sort -u)
ALLIDS=$(printf '%s\n%s\n' "$IDS" "$IDS2" | sort -u | grep -E '^[0-9a-f]{8}$' | tr '\n' '|' | sed 's/|$//')
echo "id prefixes collected: $(echo "$ALLIDS" | tr '|' '\n' | wc -l)"

pat() { case "$1" in
 person_client) echo 'kam|kamil|kreis|datasec|secuura|philip|anupam|cuffy|baidya|anthropic|noreply';;
 seat_names) echo 'friday|wednesday|tuesday|thursday|windows agent|agentmail';;
 paths) echo '/volumes|/users/|/home/|/private/|/tmp/|laptop-dev|~/|c2reh|c2c-c2|tmux';;
 pc_folders) echo 'c:\\|\\c2c|\\wdc|wdc[0-9]|\\t7|\\t11|\\wo1|e:\\|drive e';;
 addresses) echo '192\.168|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|en0|wss://[0-9a-z]';;
 mail) echo '@[a-z0-9]|\.com|\.au|\.org';;
 sheetwords) echo '\bstick\b|\busb\b|\bt9\b|hostname';;
 ids) echo "$ALLIDS";;
esac; }
for k in person_client seat_names paths pc_folders addresses mail sheetwords ids; do
  P=$(pat $k)
  n=$(printf '%s\n' "$ADDED" | grep -i -c -E "$P")
  echo "CLASS $k: added-lines hits = $n"
  [ "$n" != 0 ] && printf '%s\n' "$ADDED" | grep -i -n -E "$P" | cut -c1-220
  if [ -f "$CL" ]; then c=$(grep -i -c -E "$P" "$CL"); echo "   clarifications hits = $c"; [ "$c" != 0 ] && grep -i -n -E "$P" "$CL" | cut -c1-160; fi
done
echo "--- positive controls (each must print >=1)"
for pair in 'person_client|Kam asked' 'seat_names|Friday said' 'paths|/Volumes/x' 'paths|/private/tmp' 'pc_folders|C:\c2c\t11' 'pc_folders|E:\line' 'addresses|192.168.4.23' 'addresses|10.1.2.3' 'mail|user@host.com' 'sheetwords|the stick'; do
  k=${pair%%|*}; s=${pair#*|}; printf '  %-12s %-22s -> %s\n' "$k" "$s" "$(printf '%s\n' "$s" | grep -i -c -E "$(pat $k)")"
done
first=$(echo "$ALLIDS" | cut -d'|' -f1); echo "  ids (a collected prefix) -> $(printf 'x %s y\n' "$first" | grep -i -c -E "$(pat ids)")"
