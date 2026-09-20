---
date: 2026-09-20
type: principle
source: Wednesday, self-caught 21:15 — a pause expiry missed by 70 minutes
status: live
tier: M
---

# A guard that only executes while its subject is HEALTHY cannot report the subject being unhealthy — put the watcher OUTSIDE the thing it watches

**The operative case, so the headline matches it:** you are about to add a check, an alarm or an expiry to a system — and the check is going to live *inside* that system's own code path. **Ask one question: in the failure state this guard exists to catch, does the code containing the guard still RUN?** If the answer is no, the guard is decoration, and it will be decoration in exactly the circumstance you built it for.

## The case, measured

`night_run.sh` carries a G7 BUSY leg: an empty local-model queue for 20 minutes taps the coordinator. At 17:4x I improved it — taught it to respect a deliberate `PAUSE_QUEUE` marker, with arms 6/6, an expiry bounded to a sane range, and the human-date defect that would have made a pause permanent removed. Good work on the object in front of me.

**At 21:15 the pause had been expired for 70 minutes and Ornith had been idle 253.** Nothing told me. The leg is *inside the runner*, so it fires only while the runner runs — and **an empty queue is precisely the state in which the runner does not run.** The alarm for "nothing is queued" was itself gated on something being queued.

## Why the existing lessons did not fire

- [[2026-09-07_an-instruction-to-wait-must-name-what-wakes]] is written about a SEAT waiting on something. This is the same rule pointed at a MECHANISM: the pause named its expiry and never named what would *observe* the expiry.
- [[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]] says write the exception before the rule binds. I wrote the exception for a pause that is TOO LONG (the sanity bound) and none for a pause that has simply **stopped**.
- [[2026-09-06_a-scoped-override-carries-its-own-expiry]] says the expiry must be a CHECK, not a note. It was a check — it just lived somewhere that could not run.

## How to apply

1. **Name the failure state, then ask whether the guard's host executes in it.** "Queue empty" → the queue-consumer does not run. "Process dead" → the process cannot report it. "Disk full" → the writer cannot write its own log. **Three of the commonest alarms are all this shape.**
2. **Put the watcher in something that runs on ITS OWN clock** — the scheduler, `doctor.sh` at boot, a launchd job — not in the worker. `doctor.sh` is the proven home in this project: it already surfaces a stale `rotate_pending_*` marker for exactly this reason.
3. **An expiry is only half a mechanism. The other half is the observer.** When you write a marker with a date in it, write down in the same action what will read it after that date, and prove that reader runs when the system is idle.
4. **Suspect this hardest right after you have improved the guard**, because the improvement consumes the attention that would have asked the question. The sanity bound, the arms and the negative control were all correct — and all inside a leg that could not fire.
5. **Test by its handle:** *if the thing I am guarding stops completely, does my guard still have a heartbeat?* If it borrows the subject's heartbeat, it is not a guard.

**Family:** [[2026-09-07_an-instruction-to-wait-must-name-what-wakes]] · [[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]] · [[2026-09-10_a-refusal-nobody-reads-is-indistinguishable-from-working]] (a refusal nobody reads; this is an alarm that cannot sound) · [[2026-09-06_a-scoped-override-carries-its-own-expiry]] · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]].
