# Expiring grants — anything Kam time-scoped, with the date it DIES

**Why this file exists:** a time-scoped instruction with no mechanism to expire it becomes a
permanent change nobody decided to make. Every seat reads this at boot; an entry past its date is
**dead** and must be re-asked, not assumed.

| grant | given | EXPIRES | scope, exactly |
|---|---|---|---|
| **Deploy freely to kintsugi AND demo** | Kam, email 2026-09-10 15:24 — *"Please deploy everything possible to kintsugi. Also deploy everything possible to demo. This rule stands until the end of the week."* | **END OF SUNDAY 2026-09-14 AEST** | Deploy MERGED work to both boxes. **"Everything possible" = what has merged to develop** — it does NOT authorise merging the 66 unapproved PRs, bypassing a gate, or `--no-verify`. Kintsugi first (his 13:22 rule). Production is untouched and does not exist. |

⚠ **ASSUMPTION ON THE DATE, FLAGGED TO KAM 2026-09-10 15:2x AND NOT YET CORRECTED:** "end of the
week" read as **end of Sunday 14 September**. If he meant Friday 12th, this grant died earlier than
this file says. **Ask before relying on it on the 13th or 14th.**

## When a grant expires

1. **Stop.** The permission is gone; the previous rule returns — for demo that is *"demo-affecting
   changes always pause for Kam"*.
2. **Do not renew it by inference.** A grant that was given once is evidence about that week, not
   about this one.
3. **Delete the row or move it below a `## Expired` heading with the date it lapsed** — never leave
   a dead grant looking live.
