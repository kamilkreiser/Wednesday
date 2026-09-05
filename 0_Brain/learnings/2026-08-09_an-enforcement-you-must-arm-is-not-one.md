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
