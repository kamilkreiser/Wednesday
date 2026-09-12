#!/bin/bash
# Tuesday s11 exiting watcher (from s10's, multi-pid). Exits on the FIRST of:
#   - a tuesday-agent@ message newer than MARK that is not this seat's own outbound
#     (Kam's panel relays ARE from tuesday-agent@ and are kept by subject)
#   - any watched pid exiting
#   - the deadline (HH:MM local)
# CHANGE vs s10's copy: a non-JSON listing (network blip / rate limit) is logged to
# stderr and RETRIED; three in a row exits as "WAKE listing-broken" so a dead API
# still surfaces, but one blip no longer reads as mail (false wake 14:29, s11).
# Usage: watch_s11b.sh <MARK iso-utc> <deadline HH:MM> <pid> [pid...]
MARK="$1"; DEADLINE="$2"; shift 2
set -a; source /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env; set +a
fails=0
while true; do
  now=$(date +%H:%M)
  if [[ "$now" > "$DEADLINE" || "$now" == "$DEADLINE" ]]; then echo "WAKE deadline $DEADLINE reached ($now)"; exit 0; fi
  for p in "$@"; do
    if ! kill -0 "$p" 2>/dev/null; then echo "WAKE pid $p exited at $now"; exit 0; fi
  done
  out=$(curl -sS -H "Authorization: Bearer $AGENTMAIL_API_KEY" "https://api.agentmail.to/v0/inboxes/tuesday-agent@agentmail.to/messages?limit=15" 2>&1)
  hit=$(printf '%s' "$out" | MARK="$MARK" python3 -c '
import json,os,sys
try: d=json.load(sys.stdin)
except Exception as e: print("PARSE-ERROR "+str(e)); sys.exit()
mark=os.environ["MARK"]
for x in d.get("messages",[]):
  ts=x.get("timestamp",""); s=x.get("subject",""); f=x.get("from","") or ""
  if ts<=mark: continue
  if "tuesday-agent@" in f and not s.startswith("[Kam -> Tuesday]") and "GATE VERDICT" not in s: continue
  print(ts[:19]+" | "+f[:40]+" | "+s[:140])
')
  case "$hit" in
    PARSE-ERROR*)
      fails=$((fails+1))
      echo "$now $hit :: body head: $(printf '%s' "$out" | head -c 200)" >&2
      if [ "$fails" -ge 3 ]; then echo "WAKE listing-broken ($fails consecutive parse errors) at $now"; exit 0; fi ;;
    "") fails=0 ;;
    *) echo "WAKE mail at $now:"; echo "$hit"; exit 0 ;;
  esac
  sleep 60
done
