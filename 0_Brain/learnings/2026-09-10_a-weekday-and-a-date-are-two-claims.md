---
date: 2026-09-10
type: correction
source: self-caught at boot, seat s-w-1541 — the grant Kam gave at 15:24 was recorded one day too long
status: live
tier: W
---

# A weekday NAME and a calendar DATE are two claims — an expiry written from one and dated from the other extends itself in the direction nobody checks

**The lesson:** Kam's grant was *"until the end of the week."* The previous seat read that as
"end of Sunday", told him so in chat as **"end of Sunday the thirteenth"** — correct — and then
wrote the artefacts as **"END OF SUNDAY 2026-09-14"**. 14 September 2026 is a **Monday**. The
weekday was right, the date was wrong, and because both appeared in the same phrase the sentence
*looked* self-checking. Nobody re-derived one from the other.

**Why it matters more than a typo:** this was the expiry on a **demo deploy authority**. The error
ran in the permissive direction — one extra day of a signature-class permission Kam never granted —
and `EXPIRING-GRANTS.md` exists precisely so a time-scoped instruction cannot quietly become
permanent. **The mechanism built to stop the drift was itself carrying the drift.**

**And it had already propagated, because the wrong date was in the HEADLINE.** Three artefacts
(`EXPIRING-GRANTS.md`, the grant lesson file's headline + `expires:` field + body) and therefore
**both generated digests**. The retrieval handle is the thing every future seat reads first, so an
error there is not one wrong file — it is the wrong fact delivered at every boot.

## How to apply

1. **Never write a weekday and a date in the same claim without deriving one from the other.**
   `date -j -f "%Y-%m-%d" "<date>" "+%A"` costs nothing and answers it. If they disagree, the
   *weekday* is usually what Kam actually meant — it is what he said aloud.
2. **On any expiry, prefer the derived date and record the derivation**, not the one that "looks
   like the weekend".
3. **When an expiry is wrong, check which direction.** Permissive errors on a signature class
   (deploy, prod, money, external comms) are corrected immediately and reported; restrictive ones
   can wait for Kam.
4. **A wrong fact in a HEADLINE is already everywhere.** Fix the source file, then regenerate BOTH
   digests and grep every artefact for the old value — the correction note will still match, so
   read the hits rather than counting them.
5. This is the operative half of [[2026-09-07_read-the-clock-at-boot]]: reading the clock tells you
   *today*; it does not check the arithmetic on a date someone else wrote down.

Related: [[2026-09-10_deploy-both-boxes-grant-expires-sunday]] ·
[[2026-09-06_a-scoped-override-carries-its-own-expiry]] ·
[[2026-09-07_read-the-clock-at-boot]]
