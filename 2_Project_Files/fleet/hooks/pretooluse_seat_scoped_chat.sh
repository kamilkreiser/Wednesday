#!/bin/bash
# pretooluse_seat_scoped_chat.sh — PreToolUse hook (matcher: Bash): REFUSE any Bash call that
# reads the panel chat stores WITHOUT honouring the per-message `view` field.
#
# WHY (ledger, 2026-09-10, w=2 THE SAME DAY):
#   09:00  Kam's message carried view="tuesday"; it was read as Wednesday's.
#   09:33  `2_Project_Files/tools/kam_msgs.sh` was BUILT to fix exactly that, and its own header
#          says so. It reads `view` and filters by seat.
#   17:0x–18:0x  That tool was BYPASSED for an ad-hoc `json.load(...)` one-liner filtering on
#          `role` only. FOUR of Kam's `view="tuesday"` messages were read as this seat's; two
#          were needlessly forwarded to the other coordinator; and this seat then told Kam his
#          TABS were at fault and wrote that false claim into WED-147. He corrected it.
#   Measured after his correction: 58 Kam messages that day — 46 view=wednesday, 12 view=tuesday.
#   He had addressed every one of them correctly.
#
# THE POINT, and it is the whole reason this is a hook and not a note:
#   An OPTIONAL mechanism is a rule with a script attached. Every guard that actually stopped
#   this seat on 2026-09-10 — the `cd` hook, the brief provenance gates, the prior-rulings gate —
#   was IN THE PATH and unavoidable. `kam_msgs.sh` had to be remembered, and was not.
#
# Fail-open on the instrument (stated): a parse failure PASSES, so a hook bug cannot brick Bash.
INPUT=$(cat)
CMD=$(printf '%s' "$INPUT" | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin); print(d.get("tool_input",{}).get("command",""))
except Exception as e:
    print("", end=""); print("seat_scoped_chat: could not parse hook input: %s" % e, file=sys.stderr)')

# Only the panel chat STORES. chat_reply.sh (writing) and kam_rulings_today.sh / kam_msgs.sh
# (which already filter) are not the target — see the allow test below.
if printf '%s\n' "$CMD" | grep -qE 'chat_log\.json|chat_kam\.json'; then
  # ALLOWED: the sanctioned readers, or any command that demonstrably honours `view`.
  # ALLOW on the bare token `view` — NOT on a quoted/escaped shape. The first version matched
  # ['\"]view['\"] and get(.view.), and BOTH missed `d.get(\"view\")` because the escaped quotes
  # put a backslash between the quote and the word. That is a SELECTOR error, in the gate written
  # to catch a selector error, caught by red-proofing it before arming (2026-09-10). A gate with
  # false POSITIVES gets routed around, so the allow test is deliberately generous: mentioning
  # `view` at all is the evidence of awareness this gate asks for.
  if printf '%s\n' "$CMD" | grep -qE 'kam_msgs\.sh|kam_rulings_today\.sh|chat_streams|\bview\b'; then
    exit 0
  fi
  cat >&2 <<'MSG'
REFUSED by pretooluse_seat_scoped_chat.sh: this reads the panel chat store but never mentions
`view` — the field naming WHICH SEAT'S TAB the message was typed at.

On 2026-09-10 a reader that filtered on `role` alone surfaced 12 of Kam's `view="tuesday"`
messages to this seat; four were acted on as this seat's, two were forwarded to the other
coordinator as duplicates, and this seat told Kam his TABS were at fault. They were not — he
had addressed all 58 messages correctly.

USE THE TOOL THAT ALREADY EXISTS:
  bash "$CLAUDE_PROJECT_DIR/2_Project_Files/tools/kam_msgs.sh"          # this seat's messages
  bash "$CLAUDE_PROJECT_DIR/2_Project_Files/tools/kam_rulings_today.sh" # today's rulings

Or, if you genuinely need an ad-hoc read, make it seat-scoped and SAY SO in the code — filter
on `view` explicitly. Reading the other seat's messages is not forbidden; reading them WITHOUT
KNOWING they are the other seat's is.

This gate exists because the tool it points at was built for this exact failure at 09:33 the
same morning, and then bypassed at 17:00. An optional mechanism is a rule with a script
attached.
MSG
  exit 2
fi
exit 0
