#!/bin/bash
# fleet_ack.sh — clear a fleet activity item once it has been ANSWERED.
#
# WHY THIS EXISTS (Kam, panel 2026-09-08 10:19, verbatim):
#   "and clear fleet activity items once answered"
# The dashboard's mail tile flags a message with `attn`, which the collector
# recomputes every run as `"QUESTION" in subject.upper()`. That is a pure
# function of the SUBJECT, so answering a mail could never clear its flag —
# the item stayed lit forever and the tile stopped meaning anything.
#
# This writes the ack that generate.py now honours, keyed `mail:<message ts>`.
# The `mail:` prefix is deliberate: the chat sidebar joins ack_state on a BARE
# ts, so a prefixed key cannot be picked up there BY CONSTRUCTION.
#
# HONESTY RULE (WED-73), unchanged: "answered" is written ONLY by Wednesday's
# own session, and only after the ANSWER has been verified at the destination.
# The dashboard itself may still write nothing but "action_requested".
# The row is never removed — only the call-to-action clears, so the record of
# the question survives (never-delete).
#
# Usage:
#   fleet_ack.sh list                          show items still flagged
#   fleet_ack.sh answered "<subj substring>" "<label>"   ack every match
#   fleet_ack.sh unack    "<subj substring>"   remove the ack (re-flag it)
# Exit: 0 ok · 2 usage · 3 no match (refuses rather than silently acking nothing)
set -u
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
DATA="$PROJECT_DIR/0_Brain/dashboard/data"

CMD="${1:-}"; [ -n "$CMD" ] || { echo "usage: fleet_ack.sh list|answered|unack ..." >&2; exit 2; }

DATA="$DATA" CMD="$CMD" NEEDLE="${2:-}" LABEL="${3:-}" python3 - <<'PY'
import json, os, sys, datetime
DATA=os.environ["DATA"]; CMD=os.environ["CMD"]
NEEDLE=os.environ.get("NEEDLE",""); LABEL=os.environ.get("LABEL","")
am=os.path.join(DATA,"agentmail.json"); ap=os.path.join(DATA,"ack_state.json")
try:
    msgs=json.load(open(am))["data"]["messages"]
except Exception as e:
    print(f"fleet_ack: cannot read the mail feed: {e}", file=sys.stderr); sys.exit(2)
ack=json.load(open(ap)) if os.path.exists(ap) else {}
if not isinstance(ack,dict): ack={}
def answered(m):
    a=ack.get("mail:"+m["ts"])
    return isinstance(a,dict) and a.get("state") in ("answered","done")

if CMD=="list":
    flagged=[m for m in msgs if m.get("attn") and not answered(m)]
    done=[m for m in msgs if m.get("attn") and answered(m)]
    print(f"FLAGGED, still needing an answer: {len(flagged)}")
    for m in flagged: print(f"  ! {m['ts'][:16]}  {m['subject'][:110]}")
    print(f"ANSWERED (flag cleared, row kept): {len(done)}")
    for m in done:
        a=ack.get("mail:"+m["ts"]); print(f"  . {m['ts'][:16]}  {m['subject'][:80]}  <- {a.get('label','')}")
    sys.exit(0)

if not NEEDLE:
    print("usage: fleet_ack.sh answered|unack \"<subject substring>\" [label]", file=sys.stderr); sys.exit(2)
hits=[m for m in msgs if NEEDLE.lower() in (m.get("subject") or "").lower()]
if not hits:
    print(f"fleet_ack: REFUSED — no message subject contains {NEEDLE!r}. "
          f"Acking nothing is worse than failing loudly.", file=sys.stderr); sys.exit(3)
now=datetime.datetime.now().astimezone().isoformat()
for m in hits:
    k="mail:"+m["ts"]
    if CMD=="answered":
        ack[k]={"state":"answered","ts":now,"label":LABEL or "answered by Wednesday"}
        print(f"ACKED  {m['ts'][:16]}  {m['subject'][:90]}")
    elif CMD=="unack":
        ack.pop(k,None); print(f"UNACKED {m['ts'][:16]}  {m['subject'][:90]}")
    else:
        print(f"fleet_ack: unknown command {CMD!r}", file=sys.stderr); sys.exit(2)
json.dump(ack, open(ap,"w"), indent=1, ensure_ascii=False)
print(f"({len(hits)} written to {ap})")
PY
