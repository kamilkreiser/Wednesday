---
date: 2026-09-01
type: correction
source: "w=2 (channel-of-record family, sender side): 2026-08-24 four resume taps to NexusAI s3 went pane-only during the 529 outage (agent flagged 'no mail for any of them'; status cell said 'practice adopted; watch for recurrence'); 2026-09-01 15:17 my first act as the rotation successor was a pane tap to Secuura s95 announcing the rotation with no mail behind it — its STATUS 05:18Z: 'NO such mail in my inbox… either your successor needs to mail me, or something is putting instructions in my pane.'"
status: live — ENFORCED 2026-09-02 (cockpit.sh say --mail)
supersedes: ""
tier: W
---

# A tap is a pointer, not a message — every coordination tap has a mail behind it, sent in the same action

**The operative case:** I am about to `cockpit.sh say` anything into an agent pane that
carries CONTENT — a ruling, a continuation, a "who I am", a queue change, an offer —
rather than a bare pointer ("ANSWER mailed, read it"). **Stop. Write the mail first,
send it through the gate, verify it at the destination, then tap a pointer at it.** The
tap wakes the agent; the mail is what it may act on. A tap with no mail behind it is,
from the agent's seat, indistinguishable from the generator's ghost text — and the
fleet rule I enforce on every agent says it must be treated exactly that way.

## Why it recurred (the w=2 diagnosis)

1. **The rule lived in a ledger STATUS cell** ("practice adopted; watch for recurrence",
   2026-08-24) — episodic memory. Nothing fires at the moment of typing a tap unless a
   lesson file's headline names that moment. This file does.
2. **The tap felt like coordination, not instruction.** "I'm the successor, carry on" reads
   as housekeeping. But from the receiving side it is a claim about WHO is speaking and
   WHAT authority stands — precisely the class the agent must refuse from a pane. The
   agent said so plainly and was right.
3. **Zero cost both times**, because the taps only restated mailed authority. Zero cost is
   the condition under which a pattern recurs unfiled (the mirror-reports-state lesson,
   same shape).

## How to apply

1. **Order, always:** mail via `send_brief.sh` (kind answer/addendum) → read back at the
   destination inbox → `cockpit.sh say` a POINTER naming the mail's subject. Never the
   reverse, never the tap alone.
2. **A bare pointer is the only content a tap may carry.** "ANSWER mailed — subject X" ·
   "read your inbox" · a continuation that cites a mail already there by subject/time.
   Anything a cold reader would need to trust — identity, ruling, queue, authority — is
   mail-only.
3. **Successor boots in particular:** the first contact with a live agent is a MAIL
   (subject `[Wednesday -> <Client>/<Project>] SUCCESSOR: …`) stating the rotation,
   the seat, and "your standing queue is unchanged unless this mail says otherwise";
   then the pointer tap. Rotations are exactly when an agent should be most suspicious
   of a new voice in its pane.
4. **Enforcement candidate (w=3 would promote it):** `cockpit.sh say` refuses a payload
   longer than a pointer unless `--mail <message-id or subject>` names a mail that the
   script verifies exists at the destination inbox. Until then this file is the rule.

**Related:** [[2026-08-06_ghost-suggestions-in-panes]] (the reader-side rule this is the
sender-side twin of), [[2026-08-07_authorship-is-checkable-dkim]] (why mail and not pane),
[[2026-08-26_mirror-reports-state-not-intent]] (zero-cost recurrences), [[2026-08-04_gitignore-artifacts-at-creation]]
(a candidate is not a destination), [[_ledger]]

## ENFORCED 2026-09-02 00:57 (w=3 — the order broke a third time, with the mail present)

Third instance (ledger 2026-09-02): the ANSWER was sent through the gate and the tap fired on the
send's exit code, seconds before a read-back CONFIRMED the mail at the destination (the delivery
race; the predecessor had re-read first at 00:25). Rule 4's candidate is now the mechanism:

- `cockpit.sh say <pane> <pointer> --mail '<subject substring>'` — reads the project's inbox
  (routing conf) up to 4× over ~24 s and REFUSES the tap (rc=5) unless a message with that subject
  is there. The read-back is in the path of the tap; it cannot be skipped or raced by hand.
- A tap longer than 200 chars without `--mail` is refused (rc=4): content goes by mail, always.
- Exercised before reliance: both refuse paths + the pass path on a scratch tmux session.
- For my hands: every pointer tap that follows a mail carries `--mail`. The bare form remains for
  taps with no mail behind them (a bell pointer, 'read your inbox').
