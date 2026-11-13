#!/bin/bash
# pretooluse_inbox_scope.sh — PreToolUse hook (matcher: Bash), Tuesday seat only: REFUSE any command that reads
# another seat's AgentMail inbox.
#
# WHY (ledger _ledger_laptop_datasec.md 2026-11-13, cross-client print family w=9): re-checking a digest, s274 typed a
# loop over two inboxes, tuesday-agent@ AND wednesday-agent@, and about 90 of another client's mail subjects printed
# into this Datasec seat. The rule ("never read wednesday-agent@: not this seat's inbox") lived in the pickup file and
# lost to a convenient loop. This puts it in the path.
#
# REFUSES (exit 2): a Bash command whose text holds an AgentMail inbox PATH for any inbox other than this seat's own
# (tuesday-agent@) and the shared fleet bus (coagent@), i.e. `inboxes/<name>@agentmail.to` with another <name>, or an
# `inboxes/$VAR` path (an inbox chosen at run time from a loop can not be checked, so it is refused; write each URL out).
# ALLOWS: inboxes/tuesday-agent@..., inboxes/coagent@..., and any command that only NAMES another address elsewhere
# (for example the "to" field of a mail this seat sends from its own inbox: coordination mail to the other seat).
# FAIL-OPEN, stated: unparseable hook input -> pass, with a line on stderr saying the check did not run.
HOOK_INPUT="$(cat)"; export HOOK_INPUT
python3 -I - <<'PY'
import json, os, re, sys
try:
    cmd = json.loads(os.environ.get("HOOK_INPUT", "")).get("tool_input", {}).get("command", "") or ""
except Exception:
    print("pretooluse_inbox_scope: input not parseable; check NOT run", file=sys.stderr); sys.exit(0)
ALLOWED = {"tuesday-agent", "coagent"}
bad = []
for m in re.finditer(r"agentmail\.to/v[0-9]+/inboxes/([^/\s\"'?]+)", cmd):  # the API path only: prose that mentions an inbox is not a read (2026-11-13 false positive on a note)
    who = m.group(1)
    if who.startswith("$") or who.startswith("${"):
        bad.append(who + " (an inbox chosen at run time)")
        continue
    name = who.split("@", 1)[0].lower()
    if name not in ALLOWED:
        bad.append(who)
if bad:
    print("REFUSED by pretooluse_inbox_scope.sh: this seat reads only its own inbox (tuesday-agent@) and the fleet bus "
          "(coagent@). Path(s) naming another inbox: " + ", ".join(sorted(set(bad))) + ". Another seat's inbox holds another "
          "client's mail (ledger 2026-11-13, w=9 of the cross-client print family). Write each inbox URL out; never loop "
          "over inboxes.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
PY
