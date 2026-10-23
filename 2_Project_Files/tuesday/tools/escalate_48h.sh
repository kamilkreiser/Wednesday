#!/bin/bash
# escalate_48h.sh — email Kam ONE mail listing OPEN Datasec cards unanswered > 48 h and not yet escalated.
# Age = now - card "ts" (the store's created/added stamp). Datasec = client_project field startswith "Datasec/".
# Sends only when ESCALATE_SEND=1 and --dry-run not given; otherwise prints the mail and writes NO state.
# State (gitignored): $ESCALATE_STATE, default 2_Project_Files/fleet/state/escalated_48h.json
#   {card_id: {"msg_id": ..., "sent": ts}} — written only after HTTP success.
# Overrides for arms: DQ_FILE (store), ESCALATE_STATE, ESCALATE_ENV (env file), ESCALATE_THRESHOLD_H (default 48).
# Usage: escalate_48h.sh [--dry-run]
set -u
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export DQ_FILE="${DQ_FILE:-$DIR/../../../0_Brain/dashboard/data/decisions.json}"
export ESCALATE_STATE="${ESCALATE_STATE:-$DIR/../../fleet/state/escalated_48h.json}"
export ESCALATE_ENV="${ESCALATE_ENV:-$DIR/../../../4_Credentials/.env}"
export ESCALATE_THRESHOLD_H="${ESCALATE_THRESHOLD_H:-48}"
SEND=0
[ "${ESCALATE_SEND:-0}" = "1" ] && SEND=1
for a in "$@"; do case "$a" in --dry-run) SEND=0 ;; *) echo "escalate_48h: unknown arg '$a' (only --dry-run)" >&2; exit 2 ;; esac; done
export SEND
python3 - <<'PYEOF'
import datetime, json, os, sys, urllib.request
TO = "kamil.kreiser@datasec.com.au"
FROM_INBOX = "tuesday-agent@agentmail.to"
store, state_f, thr = os.environ["DQ_FILE"], os.environ["ESCALATE_STATE"], float(os.environ["ESCALATE_THRESHOLD_H"])
try: data = json.load(open(store))
except Exception as e: print(f"escalate_48h: cannot read {store}: {e}", file=sys.stderr); sys.exit(2)
state = {}
if os.path.exists(state_f):
    try: state = json.load(open(state_f))
    except Exception as e: print(f"escalate_48h: state file unreadable ({e}) - refusing to send blind", file=sys.stderr); sys.exit(2)
now = datetime.datetime.now().astimezone()
due = []
for c in data:
    if not str(c.get("client_project", "")).startswith("Datasec/") or c.get("status") != "open": continue
    if c["id"] in state: continue
    try: age = (now - datetime.datetime.fromisoformat(c["ts"])).total_seconds() / 3600.0
    except Exception: print(f"escalate_48h: WARNING card {c.get('id')} has no parseable ts, skipped", file=sys.stderr); continue
    if age > thr: due.append((age, c))
if not due:
    print("escalate_48h: nothing to escalate"); sys.exit(0)
due.sort(key=lambda x: -x[0])
n = len(due)
subject = f"[Tuesday -> Kam] 48h unanswered: {n} Datasec card(s)"
lines = [f"BLUF: {n} Datasec decision card(s) have waited more than {int(thr)} hours for your answer. The live board is where to answer; reply there, not by email.", ""]
for age, c in due:
    lines += [f"- {c['id']}", f"    project: {c['client_project'].split('/',1)[1]}", f"    title: {c.get('title','')}",
              f"    age: {age:.0f} h", f"    default action if you don't answer: {c.get('default_action','')}"]
lines += ["", "Each card is escalated once; you will not get this mail again for the same card.", "-- Tuesday"]
body = "\n".join(lines)
if os.environ["SEND"] != "1":
    print("DRY RUN (nothing sent, no state written)"); print("to:", TO); print("from:", FROM_INBOX); print("subject:", subject); print(); print(body); sys.exit(0)
key = None
try:
    for ln in open(os.environ["ESCALATE_ENV"]):
        ln = ln.strip()
        if ln.startswith("AGENTMAIL_API_KEY="): key = ln.split("=", 1)[1].strip().strip('"').strip("'")
except Exception as e: print(f"escalate_48h: cannot read env file: {e}", file=sys.stderr); sys.exit(2)
if not key: print("escalate_48h: AGENTMAIL_API_KEY not found", file=sys.stderr); sys.exit(2)
req = urllib.request.Request(f"https://api.agentmail.to/v0/inboxes/{FROM_INBOX}/messages/send",
    data=json.dumps({"to": [TO], "subject": subject, "text": body}).encode(),
    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
try:
    r = urllib.request.urlopen(req, timeout=20); code = r.status; resp = json.loads(r.read().decode() or "{}")
except Exception as e:
    print(f"escalate_48h: SEND FAILED: {type(e).__name__}", file=sys.stderr); sys.exit(2)
if code != 200: print(f"escalate_48h: SEND FAILED HTTP {code}", file=sys.stderr); sys.exit(2)
mid = resp.get("message_id") or resp.get("id") or "unknown"
ts = now.isoformat()
for _, c in due: state[c["id"]] = {"msg_id": mid, "sent": ts}
tmp = state_f + ".tmp"
os.makedirs(os.path.dirname(state_f), exist_ok=True)
json.dump(state, open(tmp, "w"), indent=1); os.replace(tmp, state_f)
print(f"escalate_48h: sent {n} card(s), message id {mid}")
PYEOF
