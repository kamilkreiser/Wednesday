# Expiring grants — anything Kam time-scoped, with the date it DIES

**Why this file exists:** a time-scoped instruction with no mechanism to expire it becomes a
permanent change nobody decided to make. Every seat reads this at boot; an entry past its date is
**dead** and must be re-asked, not assumed.

| grant | given | EXPIRES | scope, exactly |
|---|---|---|---|
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

**Lapsed at midnight 13→14 Sep 2026 AEST (moved here at the first Monday boot, 2026-09-14 06:52, per rule 3 above).** The v1.3 baseline returns: demo-affecting changes pause for Kam (demo = UAT, Peter's nod); no deploys without Kam's word; production is his signature class again (the 09-07 week grants — merge-for-the-week, deploy, production-ban-lifted — lapsed the same midnight per their `doctor.sh` expiry checks). The open-ended TESTED grant above still stands.

| grant | given | EXPIRED | scope, exactly |
|---|---|---|---|
| **Deploy freely to kintsugi AND demo** | Kam, email 2026-09-10 15:24 — *"Please deploy everything possible to kintsugi. Also deploy everything possible to demo. This rule stands until the end of the week."* | **END OF SUNDAY 2026-09-13 AEST** | Deploy MERGED work to both boxes. **"Everything possible" = what has merged to develop** — it does NOT authorise merging the 66 unapproved PRs, bypassing a gate, or `--no-verify`. Kintsugi first (his 13:22 rule). Production is untouched and does not exist. |
| **Both boxes end the week at PARITY** | Kam, panel 2026-09-10 17:10 — *"make sure that everything that we do this week is replicated and fixed on both servers."* | **END OF SUNDAY 2026-09-13 AEST** (same week as the deploy grant above) | Anything deployed/fixed on kintsugi this week lands on demo too, and vice versa. **This is a PARITY duty, not a new permission** — it does not widen what may be deployed ("everything possible" still = what has MERGED). If something lands on one box and cannot land on the other, that is a REPORT to Wednesday, never a silent asymmetry. |
