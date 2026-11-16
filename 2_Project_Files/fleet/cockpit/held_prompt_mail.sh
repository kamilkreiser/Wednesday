#!/bin/bash
# held_prompt_mail.sh — the one email of the held-prompt recovery (Kam ruled 2026-11-17 07:37,
# card wed-held-prompt-recovery-1117 = a: "save, email, clear, wake"). Called by the wake
# runner (arm_wake_watch.sh, wake_try_recover) once per held prompt.
#
# Same mail path as 2_Project_Files/tools/stale_card_escalate.sh: AGENTMAIL_API_KEY from
# 4_Credentials/.env, POST from wednesday-agent@agentmail.to to kreiser.org@me.com.
# The saved held text goes in the body, so anything that LOOKS like a key or token is
# masked in the mail (the saved file on disk keeps the exact text).
#
# Usage: held_prompt_mail.sh <subject> <body>
# Test hook: HELD_MAIL_DRY_SEND=1 prints the payload instead of sending.
# Exit: 0 sent · 1 send failed · 2 usage/env error.
set -uo pipefail
[ $# -eq 2 ] || { echo "usage: held_prompt_mail.sh <subject> <body>" >&2; exit 2; }
ROOT="$(cd -P "$(dirname "$0")/../../.." && pwd)"
if [ -z "${HELD_MAIL_DRY_SEND:-}" ]; then
  set -a; . "$ROOT/4_Credentials/.env"; set +a
  [ -n "${AGENTMAIL_API_KEY:-}" ] || { echo "held_prompt_mail: AGENTMAIL_API_KEY unset" >&2; exit 2; }
fi
SUBJ="$1" BODY="$2" python3 - <<'PY'
import json, os, re, sys, urllib.request
body = os.environ["BODY"]
# mask key/token shapes: sk-/ghp_/xox*/AKIA prefixes, JWT-ish, and any 32+ char run of key alphabet
pat = re.compile(r"(sk-[A-Za-z0-9_-]{8,}|gh[pousr]_[A-Za-z0-9]{8,}|xox[abpr]-[A-Za-z0-9-]{8,}|AKIA[A-Z0-9]{12,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_.-]+|[A-Za-z0-9+_=-]{32,})")
masked, n = pat.subn("[masked - see the saved file]", body)
if n:
    masked += f"\n\n({n} key-shaped string(s) masked in this mail; the saved file has the exact text.)"
payload = {"to": ["kreiser.org@me.com"], "subject": os.environ["SUBJ"], "text": masked}
if os.environ.get("HELD_MAIL_DRY_SEND"):
    print(json.dumps(payload, indent=1)); sys.exit(0)
req = urllib.request.Request("https://api.agentmail.to/v0/inboxes/wednesday-agent@agentmail.to/messages/send",
    data=json.dumps(payload).encode(),
    headers={"Authorization": "Bearer " + os.environ["AGENTMAIL_API_KEY"], "Content-Type": "application/json"})
try:
    code = urllib.request.urlopen(req, timeout=20).status
except Exception as e:
    print(f"held_prompt_mail: SEND FAILED: {e}", file=sys.stderr); sys.exit(1)
if code != 200:
    print(f"held_prompt_mail: SEND FAILED ({code})", file=sys.stderr); sys.exit(1)
print(f"held_prompt_mail: sent: {payload['subject']}")
PY
