---
date: 2026-08-09
type: correction
source: "Overnight 2026-08-08/09: TWO Vision QUESTION mails (plan confirmation 02:15Z, CI-observation 02:22Z) went unanswered for the whole session and were never answered at all; NexusAI sat idle ~17h after its plan confirmation was answered and wrapped as 'boot-only session, execution handed to next session'. wake_watch.sh — the enforcement built on 2026-08-05 for exactly this failure — was NOT RUNNING (verified: no process; its log last written 2026-08-06)."
status: live
supersedes: ""
tier: M
---

# An enforcement you have to remember to arm is not an enforcement

**The failure.** I briefed two agents, answered one plan confirmation, and then
spent the session on an unrelated research task. Vision asked me two questions.
Neither was ever answered. They waited the protocol window, proceeded correctly
under the 15-minute fallback, and delivered — but the second question was the
one that mattered: *nobody could observe the CI runs*, and only I or Kam could
unblock it. NexusAI, meanwhile, did nothing at all for seventeen hours and I
never noticed, because nothing told me and I never looked.

**Why the existing rules did not fire.** My standing behaviour is explicit:
*"re-check the inbox PERIODICALLY during long sessions — at natural checkpoints
(a long task finishes, before proposing next steps), not just at boot."* I
finished three long research tasks and checked at none of them. So the rule was
written, correct, unambiguous, and it did nothing — which is the same story as
every w≥3 row in the ledger.

**The part that is genuinely new, and worse.** The enforcement for this already
exists. `fleet/cockpit/wake_watch.sh` was built on 2026-08-05 as the w=3
response to precisely this failure class: it samples every 60s and wakes me on
new mail within about a minute. It would have caught both questions.

**It was not running.** Nothing starts it. Nothing checks that it is running.
Arming it depends on me remembering to arm it — which means the mechanism I
built to compensate for my unreliable attention is itself gated on my unreliable
attention.

That is [[2026-08-07_a-promise-is-not-a-mechanism]] pointed at my own tooling.
There I learned that unsupervised *work* needs a trigger rather than an
intention. This is the same error one level up: **a safeguard that must be
manually switched on is an intention wearing a mechanism's clothes.** It
produces the worst of both worlds — the reassurance of having built something,
with none of the protection.

**The distinction worth keeping.** The enforcements in this brain that have
actually held are the ones that cannot be skipped, because they sit in the path
of the thing they govern: the pre-commit hook fires because committing runs it;
`send_brief.sh` refuses because it *is* the send path; `doctor.sh` runs at boot.
The ones that have failed are the ones running *beside* the work rather than
*in* it. Ask of any new safeguard: **what would have to happen for this to be
off, and would I notice?** If the answer is "I forget, and no", it is not built
yet.

**How to apply:**
1. **A safeguard that runs beside the work must have something that arms it and
   something that checks it is armed.** Launcher start plus a `doctor.sh` check
   is the minimum. An unarmed watcher should read as a preflight failure, not as
   silence.
2. **Prefer in-path enforcement over parallel monitoring** every time the choice
   exists. A gate in the path beats a watcher alongside it.
3. **Treat "no mail from an agent" as a question, never as an answer.** Silence
   from a briefed agent is equally consistent with working, finished, stalled,
   and dead. Seventeen hours of silence read as "busy" and meant "idle".
4. **Checkpoint discipline is mine even when a watcher exists** — the watcher is
   the backstop, not the plan. Finishing any long task is a checkpoint: check
   the inbox before starting the next thing, not when I happen to think of it.

**The honest credit.** None of this was self-caught. The Vision agent surfaced
it by naming it plainly in their wrap — *"you did not answer my QUESTION within
the protocol window, so per the 15-minute rule I proceeded"* — and by refusing
to claim the two DoD items nobody had actually verified, quoting this fleet's own
doctrine back at me: *a check nobody watched is a check that cannot fail.* They
were owed answers and did the right thing without them.

**Related:** [[2026-08-07_a-promise-is-not-a-mechanism]] (family parent),
[[2026-08-04_delegation-v2-observability]], [[2026-08-05_wed-work-threshold-delegation]],
[[2026-08-04_never-blanket-markseen-mid-monitoring]] (the 08-04 swallowed
question — same family, different cause), [[2026-08-07_a-check-that-cannot-fail]],
[[_ledger]]

## EXTENSION 2026-09-07 — the strongest evidence yet, and it is that a guard caught the COORDINATOR, not the builder

**The case.** Wednesday's `split` brief told the Secuura seat to revert a file to its state **on
develop** and prove byte-identity. **Base still carried Kam's real address AND his real name** — the
redaction had happened in round 1 of that same PR — so *"restore it to develop"* meant *"undo the
redaction"*. **The instruction written to make things safer would have re-published his identity.**

**What caught it was a drift guard the BUILDER had written four hours earlier, in that same round**,
which enumerates seed sites **from the tree** rather than from a hand-written list. It fired on
Wednesday's instruction and told the seat the address was back in that file. The seat had already
caught, re-targeted and pushed **before Wednesday's own STOP arrived** — the messages crossed, and
the fix was the guard's and the seat's, not the warning's.

**The agent's formulation, adopted verbatim because it is better than the file's own:** *"Guards in
the path beat rules in briefs. Rules live in whoever remembers them. That guard did not need anyone
to remember anything."*

**The two things this adds to the file:**

1. **A guard's blast radius exceeds its author's intent, and that is the point.** It was written to
   stop a builder's drift and it caught a coordinator's instruction — **the one class of error no
   review layer above it was going to catch, because the coordinator IS the review layer.** A
   hand-written list would have contained the two files someone remembered, one of which was the file
   Wednesday's instruction changed. **Enumerate from the source; never list from memory.**
2. **The discoverability corollary, learned the same day:** an enforcement nobody can find is an
   enforcement that gets routed around in good faith. See
   [[2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id]] — a QA launch guard sat in a
   gitignored directory and was ~25 minutes from being bypassed by the coordinator who was trying to
   honour it. **Arm it, check it is armed, and make sure the next person can find it.**

**Also from the same day, the seat's own second keeper:** *"three wrong-path zeroes, each caught only
because the control returned zero too. A zero from a wrong path is the check-that-cannot-fail wearing
a shell's clothes."* ([[2026-08-07_a-check-that-cannot-fail]].)

## EXTENSION 2026-09-10 — the sibling clause: an enforcement you must CHOOSE TO CALL is not one either. **An optional mechanism is a rule with a script attached.**

**This file has said "an enforcement you must ARM is not one" since 2026-08-09 and it is the
brain's largest family (149 ledger rows). Today it failed in its own blind spot: the tool was
built, armed, executable, documented — and simply not called.**

**The case, and the timing is what makes it evidence.** At 09:00 a Kam panel message carrying
`view="tuesday"` was read as this seat's. **At 09:33 `2_Project_Files/tools/kam_msgs.sh` was BUILT
to prevent exactly that**, reading `view` and filtering by seat; its own header records the 09:00
failure as its reason. **At 17:00–18:02 it was bypassed** for an ad-hoc `json.load(...)` one-liner
filtering on `role` alone. Result: **4 of Kam's 12 `view="tuesday"` messages that day read as this
seat's**, two needlessly forwarded to the other coordinator, and **Kam told that his TABS were at
fault — a false claim, which then went into WED-147.** He had addressed all 58 correctly.

**Why the existing rule did not cover it:** "arm it" was satisfied. The tool existed and ran. The
gap is that **invoking it remained a decision**, and a decision under time pressure loses to a
reflex — the same way "never `cd`" lost to a reflex five times before it became a hook.

## The discriminator, measured on one day

On 2026-09-10 this seat was stopped **ten times** by enforcement, and **every single one was
IN-PATH and unavoidable**: the `cd` PreToolUse hook (3), `send_brief.sh`'s provenance/scope gates
(4), `decision_queue.sh`'s prior-rulings gate (3). **Zero of those required remembering anything.**
The one mechanism that had to be *chosen* — `kam_msgs.sh` — was the one that failed, on the day it
was built.

> **Ask of any new mechanism: can I complete the action WITHOUT it?**
> If yes, it is a rule. Rules lose to reflexes. Move it into the path — a hook, a gate, a refusal —
> or accept that it will work only while attention is cheap.

**Fixed the same hour, in the path:** `hooks/pretooluse_seat_scoped_chat.sh` REFUSES any Bash call
touching `chat_log.json` / `chat_kam.json` that never mentions `view`, and names the tool to use.
Red-proofed on six arms before arming — **and the first version's allow-test was itself a selector
bug** (`['\"]view['\"]` missed `d.get(\"view\")`, because the escaped quotes put a backslash
between the quote and the word), **caught by exercising it rather than reading it**. The allow test
is now deliberately generous: **a gate with false positives gets routed around**, which is how this
family began.

Related: [[2026-09-10_surprising-measurements-are-selector-errors]] ·
[[2026-09-10_a-panel-message-is-a-record-not-a-string]] ·
[[2026-08-06_exercise-mechanisms-before-arming]]
