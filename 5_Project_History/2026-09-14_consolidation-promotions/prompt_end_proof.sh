#!/bin/bash
# WED-141-style proof: extract the INITIAL_PROMPT="..." block from a launcher, source it with
# dummy vars under set -u, and print where the variable ENDS. bash -n cannot see a moving
# string boundary; this can.
set -u
L="$1"
START=$(/usr/bin/grep -n '^INITIAL_PROMPT="ultrathink$' "$L" | cut -d: -f1)
END=$(awk -v s="$START" 'NR>s && /"$/ && !/\\"$/ {print NR; exit}' "$L")
BLOCK=$(sed -n "${START},${END}p" "$L")
( set -u
  AGENT_UPPER=X PROJECT_DIR=/p DEVMASTER_STATE=s AGENT_SCOPE=sc BRAIN_DIR=/b DASH_URL=u DASH_STATE=d SEAT_LEDGER=l SELF_INBOX=i DEVMASTER=/d DEVMASTER_VAULT=/v OTHER_LEDGER=o
  eval "$BLOCK"
  echo "block lines ${START}-${END}; INITIAL_PROMPT chars=${#INITIAL_PROMPT} lines=$(printf '%s\n' "$INITIAL_PROMPT" | wc -l | tr -d ' ')"
  echo "LAST LINE: $(printf '%s\n' "$INITIAL_PROMPT" | tail -1)"
  echo "note_entry line present: $(printf '%s\n' "$INITIAL_PROMPT" | /usr/bin/grep -c 'note_entry.sh')"
)
