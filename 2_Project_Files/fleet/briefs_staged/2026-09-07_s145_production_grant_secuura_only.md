## BLUF — Kam has lifted the PRODUCTION ban for this week, SECUURA ONLY. It goes into your standing holds, with a flagging obligation attached. It does NOT unblock #885.
**Kam, panel 2026-09-07 12:07:38, verbatim:** *"Lift the production ban. This week we are allowed to
make production changes, but flag these when relevant or when making changes. Make the change
directly."*
**Scope confirmed by him at 12:10:40: *"Only secure."* — Secuura**, his Whisperflow rendering of
Secuura, which he corrected himself at 09:50:58 this morning. **Read as through Sunday 2026-09-13**;
`doctor.sh` warns after that date for this and the day's other two week-scoped grants.

## ⚠ IT DOES NOT UNBLOCK #885, AND WEDNESDAY TOLD HIM SO
The demo deploy was **never** held by the production ban. It is held because **the fix is wrong** —
it would write twelve plaintext addresses into an encrypted column, eleven of them the public demo
personas. **Nothing about this grant changes the NO GO.** Do not read it as permission to proceed.

## WHAT IT CHANGES FOR YOU
Production changes on **Secuura** are now inside scope this week rather than stopping for Kam.
**With a condition that is an obligation, not a courtesy:** *"flag these when relevant or when making
changes."*
1. **Every production change is FLAGGED to Wednesday — before it happens where there is time,
   immediately after where there is not** — with **what changed and WHERE** (environment,
   subscription, resource). Wednesday relays to Kam.
2. **Name the destination in the BLUF**, exactly as a commit names its remote and branch.
3. **The grant removes the pause, not the receipt.**

## WHAT REMAINS OUTSIDE IT — do not let a production grant absorb these
- **DATASEC PRODUCTION IS NOT COVERED.** Vision's live site and database in `datasec-sales-portal-rg`
  belong to the laptop seat and it has **no such grant**. Nothing you do touches Datasec.
- **A credential that live systems authenticate with is a ROTATION and still comes to Kam.** The
  published admin password in 128 files is the live case — he ruled `rotate-properly` and that ruling
  governs. **The production grant does not silently absorb it.**
- **External communication to any human.** Untouched. Peter and Stuart hear nothing.
- **Irreversible acts the grant does not itself imply** — history rewrites, credential deletion,
  destructive tenant operations.
- **Never argue an action into scope.** If it needs a clever reading of "production changes", it is
  outside it.

## STATE — unchanged, and nothing for you to start
#885 is **NO GO** at `6dbe63cae`; **Kam's two-round cap is SPENT** and the third-round card is on his
desk (`secuura-ks949-round3-cap-and-the-cutoff`, recommendation `split` — revert F1 only, ship F2–F5,
F1 gets its own round). **Nothing merges, nothing deploys, and you build nothing on #885 until he
rules.** Your KS-961 branch (`bb0502c80`) is fine where it is.

**The gate's finding you have not yet seen, and it is the one that matters:** the auth remediation —
the only path that would rewrite the row — **is disabled on prod-like environments** by
`PII_PLAINTEXT_CUTOFF` (2026-06-01, set nowhere in the repo). `decryptEmail` throws, `getUserById`
catches and returns null, and the remediation reads that as *"no pre-existing row to remediate"*.
**So round 3 alone may not remediate anything.** Do not design around that until Kam rules; it may
become its own ticket.

## PROVENANCE
- Both of Kam's messages | his panel 2026-09-07 12:07:38 and 12:10:40, read this action.
- The NO GO, the cutoff chain, the blast radius | the gate's mail
  `[QA -> Wednesday] Secuura KS-949 round 2 (#885, tier 1)`, 2026-09-07T02:02:46Z, quoted.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **12:07 + 12:10 — production ban lifted for the week, SECUURA ONLY, with a flagging obligation.**
  Lands in: this brief's HOLDS, and every subsequent Secuura brief's standing lines.
