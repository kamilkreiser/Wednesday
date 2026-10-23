#!/bin/bash
# stale_card_escalate.sh — Kam's rule 6 (live board, 2026-10-23 14:31:46, verbatim):
#   "if there is an unanswered item for more than 48 hours, escalate by emailing me"
#
# Lists OPEN decision cards older than 48 h in THIS seat's scope and, with --send,
# emails Kam ONE digest naming them. A card already escalated is re-mailed only
# after another 24 h (a reminder, not a flood). Datasec cards (Tuesday's) and
# Friday's cards are out of scope: each seat escalates its own.
#
# Usage:
#   stale_card_escalate.sh --check   # print what WOULD be escalated; sends nothing
#   stale_card_escalate.sh --send    # email the digest to Kam, record what was sent
# Test hooks: STALE_NOW=<ISO8601> pins the clock; STALE_DECISIONS=<path> another store;
#   STALE_STATE=<path> another state file; STALE_DRY_SEND=1 prints the payload instead of sending.
# Exit: 0 ok (nothing stale, or sent) · 1 send failed · 2 usage/env error.
set -uo pipefail
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SELF_DIR/../.." && pwd)"
MODE="${1:-}"
case "$MODE" in --check|--send) ;; *) echo "usage: stale_card_escalate.sh --check|--send" >&2; exit 2 ;; esac
DEC="${STALE_DECISIONS:-$ROOT/0_Brain/dashboard/data/decisions.json}"
STATE="${STALE_STATE:-$ROOT/2_Project_Files/fleet/state/stale_card_escalations.json}"
[ -f "$DEC" ] || { echo "stale_card_escalate: no decision store at $DEC" >&2; exit 2; }
if [ "$MODE" = "--send" ] && [ -z "${STALE_DRY_SEND:-}" ]; then
  set -a; . "$ROOT/4_Credentials/.env"; set +a
  [ -n "${AGENTMAIL_API_KEY:-}" ] || { echo "stale_card_escalate: AGENTMAIL_API_KEY unset" >&2; exit 2; }
fi
MODE="$MODE" DEC="$DEC" STATE="$STATE" python3 - <<'PY'
import json, os, sys, datetime, urllib.request
now = datetime.datetime.fromisoformat(os.environ["STALE_NOW"]) if os.environ.get("STALE_NOW") \
      else datetime.datetime.now(datetime.timezone.utc).astimezone()
cards = json.load(open(os.environ["DEC"]))
try:
    state = json.load(open(os.environ["STATE"]))
except FileNotFoundError:
    state = {}
stale = []
for c in cards:
    if c.get("status") != "open" or c.get("seat") == "friday":
        continue
    if str(c.get("client_project", "")).startswith("Datasec"):
        continue
    ts = datetime.datetime.fromisoformat(c["ts"])
    age_h = (now - ts).total_seconds() / 3600
    if age_h < 48:
        continue
    last = state.get(c["id"])
    if last and (now - datetime.datetime.fromisoformat(last)).total_seconds() < 24 * 3600:
        continue
    stale.append((c, age_h))
print(f"stale_card_escalate: {len(stale)} open card(s) over 48 h in scope (clock {now.isoformat(timespec='minutes')})")
for c, h in stale:
    print(f"  {c['id']}  {c.get('client_project')}  open {h/24:.1f} days  — {c.get('title','')[:90]}")
if os.environ["MODE"] == "--check" or not stale:
    sys.exit(0)
lines = ["Kam, these are waiting on you for more than 48 hours. Each is a card on the live board's fleet activity, with a default that fires if you don't tap it.", ""]
for c, h in stale:
    lines.append(f"- {c.get('client_project')}: {c.get('title','')} (open {h/24:.1f} days). Default: {c.get('default_action','')}")
lines += ["", "Rule them by tapping the card. This mail repeats once a day while any stays open (your rule of 23 Oct 14:31).", "", "Wednesday"]
payload = {"to": ["kreiser.org@me.com"],
           "subject": f"[Wednesday -> Kam] {len(stale)} item(s) waiting on you for over 48 hours",
           "text": "\n".join(lines)}
if os.environ.get("STALE_DRY_SEND"):
    print(json.dumps(payload, indent=1)); sys.exit(0)
req = urllib.request.Request("https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages/send",
    data=json.dumps(payload).encode(),
    headers={"Authorization": "Bearer " + os.environ["AGENTMAIL_API_KEY"], "Content-Type": "application/json"})
try:
    code = urllib.request.urlopen(req, timeout=20).status
except Exception as e:
    print(f"stale_card_escalate: SEND FAILED: {e}", file=sys.stderr); sys.exit(1)
if code != 200:
    print(f"stale_card_escalate: SEND FAILED ({code})", file=sys.stderr); sys.exit(1)
for c, _ in stale:
    state[c["id"]] = now.isoformat()
tmp = os.environ["STATE"] + ".tmp"
os.makedirs(os.path.dirname(os.environ["STATE"]), exist_ok=True)
json.dump(state, open(tmp, "w"), indent=1); os.replace(tmp, os.environ["STATE"])
print(f"stale_card_escalate: sent: {payload['subject']}")
PY
