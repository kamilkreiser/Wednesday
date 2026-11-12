#!/bin/bash
# pretooluse_cockpit_verb.sh — REFUSE a Bash call that runs cockpit.sh with a verb it does not have.
# WHY (ledger 2026-11-10 11:00 + 2026-11-12 18:5x + 19:1x, the same costume three times, twice in one session
# minutes after the row was written): a filler `cockpit.sh <invented verb> 2>/dev/null` rode inside pane-close /
# wake-ack calls. cockpit.sh is a WRITE tool (it types into agent panes); an invented verb only dies today, but
# the habit is "run a write tool as filler", and the next invented word may be a real verb. A rule held as prose
# lost to the reflex twice; this puts it in the path.
# Valid verbs are read from cockpit.sh's own usage line at run time (never a copied list), so a new verb needs no edit here.
INPUT=$(cat)
CMD=$(printf '%s' "$INPUT" | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))
except Exception as e:
    print("pretooluse_cockpit_verb: could not parse hook input: %s" % e, file=sys.stderr)')
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
COCKPIT="$SELF_DIR/../cockpit/cockpit.sh"
VERBS=$(/usr/bin/grep -o 'usage: cockpit.sh [a-z]*|[a-z|]*' "$COCKPIT" | tail -1 | sed 's/usage: cockpit.sh //')
[ -n "$VERBS" ] || { echo "pretooluse_cockpit_verb: could not read verbs from $COCKPIT (not blocking)" >&2; exit 0; }
BAD=$(printf '%s\n' "$CMD" | python3 -c '
import re,sys
verbs=set(sys.argv[1].split("|"))
bad=[v for v in re.findall(r"cockpit\.sh[\"\x27]?\s+([A-Za-z_][A-Za-z0-9_-]*)", sys.stdin.read()) if v not in verbs]
print(" ".join(bad))' "$VERBS")
if [ -n "$BAD" ]; then
  cat >&2 <<MSG
REFUSED by pretooluse_cockpit_verb.sh: this call runs cockpit.sh with verb(s) it does not have: $BAD
(valid: $VERBS). cockpit.sh writes into agent panes; a filler or invented verb is a write command run for no
purpose (ledger 2026-11-10, 2026-11-12 x2). Remove it and re-issue the call with only the commands it is for.
MSG
  exit 2
fi
exit 0
