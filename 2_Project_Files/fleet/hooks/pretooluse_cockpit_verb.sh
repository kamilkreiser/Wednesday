#!/bin/bash
# pretooluse_cockpit_verb.sh — REFUSE a Bash call that (1) runs cockpit.sh with a verb it does not have,
# (2) runs cockpit.sh with NO verb (or a --flag in the verb slot), or (3) runs any fleet tool
# (2_Project_Files/fleet/... or 2_Project_Files/tools/... *.sh) with BOTH stdout and stderr sent to /dev/null.
# WHY (1) (ledger 2026-11-10 11:00 + 2026-11-12 18:5x + 19:1x, the same costume three times, twice in one session
# minutes after the row was written): a filler `cockpit.sh <invented verb> 2>/dev/null` rode inside pane-close /
# wake-ack calls. cockpit.sh is a WRITE tool (it types into agent panes); an invented verb only dies today, but
# the habit is "run a write tool as filler", and the next invented word may be a real verb.
# WHY (2) and (3) (ledger 2026-11-19 22:11, REGRESSION w>=5 across 11-17..11-19): a bare cockpit.sh call with both
# streams discarded, and then `cockpit.sh --help`, slipped past (1), which refused only INVENTED verbs, not ABSENT
# ones; the 11-17 07:20 stray wake_ack.sh call was a fleet WRITE tool with its output discarded. A fleet tool
# appears in a call only as the act it exists for, with its output kept; to learn what a tool does, read its
# header (sed -n), never run it.
# Valid verbs are read from cockpit.sh's own usage line at run time (never a copied list), so a new verb needs no edit here.
# Quoted heredoc bodies (<<'X' ... X) are stripped before matching: prose about these commands is not a command
# (2026-11-19 23:5x: the previous version refused a heredoc that WROTE this file).
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
OUT=$(printf '%s\n' "$CMD" | python3 "$SELF_DIR/pretooluse_cockpit_verb_check.py" "$VERBS")
RC=$?
if [ $RC -ne 0 ]; then
  echo "pretooluse_cockpit_verb: checker failed rc $RC (not blocking): $OUT" >&2
  exit 0
fi
if [ -n "$OUT" ]; then
  cat >&2 <<MSG
REFUSED by pretooluse_cockpit_verb.sh:
$OUT
(cockpit.sh valid verbs: $VERBS). A fleet tool appears in a call only as the act it exists for, with its output
kept (ledger 2026-11-10, 2026-11-12 x2, 2026-11-17 x3, 2026-11-19 22:11 REGRESSION). To learn what a tool does,
READ its header or dispatch (sed -n), never run it. Remove it and re-issue the call with only the commands it is for.
MSG
  exit 2
fi
exit 0
