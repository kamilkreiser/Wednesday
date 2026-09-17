# Expiring grants — anything Kam time-scoped, with the date it DIES

**Why this file exists:** a time-scoped instruction with no mechanism to expire it becomes a
permanent change nobody decided to make. Every seat reads this at boot; an entry past its date is
**dead** and must be re-asked, not assumed.

| grant | given | EXPIRES | scope, exactly |
|---|---|---|---|
| **Ornith q4 ONLY; volume across the whole KS Backlog/Todo** — ⚠ **the "QA Sunday night, merge all at once" HALF IS SUPERSEDED by Kam 2026-09-18 09:15:10:** *"Okay, don't wait until Sunday. Merge, push, and deploy everything that's ready and archive all the items that have been done."* The q4-only and volume halves stand. | Kam, panel 2026-09-15 16:36:04 *"lets use the smaller model for the rest of the week. complete as many tickets as possible. work with the local LLM. we will do QA on these Sunday night and merge / commit all at once"* | **end of SUNDAY 2026-09-20** (derived: 2026-09-20 is a Sunday) | held diffs only until Sunday's QA; auth/MFA/OAuth product edits stay out until he names them (Wednesday's reading 16:37). Lesson: `learnings/2026-09-15_ornith-q4-only-volume-week-qa-sunday-merge-once.md` |
| **We approve and merge our own TESTED Platform K work** | Kam, panel 2026-09-11 16:56:00 *"For the time being, I / you will approve our own elements"* + 16:56:44 *"based on this.  FIx and merge all tickets after they are tested"* (on Stuart's forwarded proposal) | **OPEN-ENDED — "for the time being"; stands until Kam withdraws it** | Approval = Kam or Wednesday's GO after the QA gate at head + Test Evidence; squash, author merges; kintsugi gets merged work; **demo = UAT, waits for Peter's formal test and nod (narrows the week deploy grant's demo half — told to Kam)**; raise-to-1 stays unapplied. Platform K only. `learnings/2026-09-11_secuura-we-approve-and-merge-our-own-tested-work.md` |

⚠ **ASSUMPTION ON THE DATE, FLAGGED TO KAM 2026-09-10 15:2x AND NOT YET CORRECTED:** "end of the
week" read as **end of Sunday 13 September** (Sunday IS the 13th; 2026-09-14 is a Monday — this file said "Sunday 14 Sep" until 15:4x on 09-10, granting a day nobody gave). If he meant Friday 11th or 12th, this grant died earlier than
this file says. **Ask before relying on it on the 12th or 13th.**


## When a grant expires

1. **Stop.** The permission is gone; the previous rule returns — for demo that is *"demo-affecting
   changes always pause for Kam"*.
2. **Do not renew it by inference.** A grant that was given once is evidence about that week, not
   about this one.
3. **Delete the row or move it below a `## Expired` heading with the date it lapsed** — never leave
   a dead grant looking live.

## Expired

**LIFTED AFTER 2 h 39 min — Kam, panel 2026-09-18 09:16:16, verbatim:** *"The credits have reset, so please start up all agents and continue the work."* The 06:37 no-Claude-agents restriction is **DEAD**; it never reached its Sunday expiry. `usage_gate.sh` re-checked at 09:17: **OK — weekly usage 5% < 90%, gauge age 3 min** (the reset landed and the gauge is publishing again). The four parked launches (#1034 gate · #1037 KS-1101 drafter · seat A 9th successor · #1036 + Seat B) are UNPARKED.

**The lifted row, kept for the record:**

| grant | given | EXPIRES | scope, exactly |
|---|---|---|---|
| **RESTRICTION (not a grant): NO Claude agents at all — local LLM ONLY** | Kam, panel 2026-09-18 06:37:13 *"we are at 92% can you move to no more claude agents and only using the local LLM until sunday"* | **end of SUNDAY 2026-09-20** (derived: `date -j` says 2026-09-20 is a Sunday; today is Friday 2026-09-18 — the weekday and the date were checked against each other, not assumed) | **No seats, no QA gates, no drafters, no successors.** This SUPERSEDES the 90% usage cut (`2026-09-14_at-90pct-weekly-usage-no-new-agents…`) in the strict direction: under that rule the ~08:00 allowance renewal would have reopened launching; under THIS one it does not — the renewal unparks nothing. **CANCELLED by it:** the 02:18 renewal sequence (#1034 gate · #1037 KS-1101 drafter · seat A 9th successor · #1036 + Seat B) — all four are Claude launches and are parked until Sunday, NOT until 08:00. Wednesday + Ornith continue. **OPEN QUESTION put to Kam 06:38, unanswered:** whether in-session research sub-agents (the Agent tool, used to search the board and size Ornith's next ticket) are included. **Until he answers, treat them as INCLUDED** — the safest reading of "no more claude agents", and the cost is a thinner hand-picked Ornith queue, not a wrong action. Lesson: `learnings/2026-09-18_no-claude-agents-local-model-only-until-sunday.md`. **⚠ SCOPE UNRESOLVED, ASKED 06:5x, UNANSWERED:** a Tuesday commit SUBJECT at 06:52 — fifteen minutes AFTER this instruction — reads *"Kam released the pause, RD-521 dropped, S66 launched"*, i.e. a Claude seat started on DATASEC. Read as a subject only (Datasec is Tuesday's). So either this instruction is WEDNESDAY/SECUURA-scoped and Datasec runs to its own rules, or Kam has moved and Tuesday holds the newer version. **KEEP HOLDING until he answers** — guessing loose spends the allowance he is protecting; guessing tight costs an idle weekend, and only one of those is recoverable. Do NOT infer a release from another seat's commit subject. |


**Lapsed at midnight 13→14 Sep 2026 AEST (moved here at the first Monday boot, 2026-09-14 06:52, per rule 3 above).** The v1.3 baseline returns: demo-affecting changes pause for Kam (demo = UAT, Peter's nod); no deploys without Kam's word; production is his signature class again (the 09-07 week grants — merge-for-the-week, deploy, production-ban-lifted — lapsed the same midnight per their `doctor.sh` expiry checks). The open-ended TESTED grant above still stands.

| grant | given | EXPIRED | scope, exactly |
|---|---|---|---|
| **Deploy freely to kintsugi AND demo** | Kam, email 2026-09-10 15:24 — *"Please deploy everything possible to kintsugi. Also deploy everything possible to demo. This rule stands until the end of the week."* | **END OF SUNDAY 2026-09-13 AEST** | Deploy MERGED work to both boxes. **"Everything possible" = what has merged to develop** — it does NOT authorise merging the 66 unapproved PRs, bypassing a gate, or `--no-verify`. Kintsugi first (his 13:22 rule). Production is untouched and does not exist. |
| **Both boxes end the week at PARITY** | Kam, panel 2026-09-10 17:10 — *"make sure that everything that we do this week is replicated and fixed on both servers."* | **END OF SUNDAY 2026-09-13 AEST** (same week as the deploy grant above) | Anything deployed/fixed on kintsugi this week lands on demo too, and vice versa. **This is a PARITY duty, not a new permission** — it does not widen what may be deployed ("everything possible" still = what has MERGED). If something lands on one box and cannot land on the other, that is a REPORT to Wednesday, never a silent asymmetry. |
