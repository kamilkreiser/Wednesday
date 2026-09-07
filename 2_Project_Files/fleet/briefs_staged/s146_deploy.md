# DEPLOY GO — Kam lifted my hold. develop `632f16dfe` to the demo. Precondition first, and read §4 before the receipt.

## BLUF
**Kam, panel 13:40, verbatim:** *"Also, there are a number of items in tested but not deployed. Feel
free to deploy."* **My hold is lifted by its owner and this is his word, not my inference.**

**DEPLOY: develop `632f16dfe62f4c498a73ca09a39cadaf6eeab764`** — read at origin by Wednesday at 13:3x
and unmoved since #885 merged. **DESTINATION, named because a deploy states it:** the **Secuura DEMO**
environment (the running **VM**, not the retired Container Apps estate), on the **Founders Hub**
tenant `efc17e5f-…`, subscription `a0ee7d32-…`. **If your deploy path targets anything else, STOP and
mail me.**

**This is inside Kam's week-scoped production grant (Secuura only, read as through Sunday
2026-09-13). Insert it at the head of your queue, ahead of KS-952.**

## 1. THE PRECONDITION, FIRST — s145 put it in the deploy plan and it is your step 1
**s145's own carried residue:** *the seed sits inside the same `try` as `migrateDatabase`, so a
migration throw skips it.* And **F1 was REVERTED in #885**, so `ON CONFLICT (email)` is back and
**KS-962 records that the api-gateway user seed throws 42P10 on every boot and has never seeded.**

**Establish, before deploying, whether a throwing seed can break or partially-apply this deploy.**
That is a measurement, not a judgement. **If it can: STOP and mail me — do not deploy and do not work
around it.** If it cannot (because it already throws on the running box and the deploy is unaffected),
**say so with what you measured**, and proceed.

## 2. WHAT ELSE TO CHECK BEFORE YOU PUSH THE BUTTON
- **`ls-remote` immediately before**: develop must still be `632f16dfe`. If it has moved, stop — it
  would mean something merged that nobody gated.
- **Use the repo's OWN deploy path.** Do not invent one and do not hand-roll steps.
- **Nothing from #888 is in this deploy** — that branch is unmerged and under gate. Do not include it,
  do not rebase anything onto it, do not touch it.

## 3. AFTER — verify the ARTEFACT, not the exit code
**A green deploy script is not evidence that the thing is live.** Probe the running demo for content
that is only true of `632f16dfe`, and report what you probed. **Read-only probes only — no login
attempts, no writes, no restarts beyond what the deploy path itself performs.**
Then: **the five merges present by CONTENT on the deployed build**, the demo answering, and anything
that changed for a user.

## 4. 🔴 THE RECEIPT MUST NOT IMPLY SOMETHING IT DOES NOT DO
**NOTHING IN THIS DEPLOY REMEDIATES KAM'S OWN ROW.** The fix that would have is the one the `split`
took out of #885; it lives in **KS-962 and KS-963** and it is not here. **Kam knows this — I told him
twice, leading with it — and the receipt must not quietly suggest otherwise.**

Say plainly what ships: the `//` rate-limiter bypass fix, the rate-limit key-poisoning fix, the push
guard and its message fix, the demo-admin work from #885's F2–F5, and round 1's fictional identity.
**And say plainly what does not: his address is untouched by this deploy.**

## 5. FLAG IT — his standing condition on the production grant
His grant came with *"flag these when relevant or when making changes."* **I am flagging it to him on
the panel in this same action, before it runs.** Your job is the receipt afterwards: what changed,
where, and what did not.

## 6. BOUNDS
**No history rewrite. No credential change on a running system. No second probe of anything. No
contact with any human.** **Never delete — quarantine.** **No Azure, no credits, no Founders Hub
investigation** — Kam killed that subject at 13:06; this brief names the tenant only so you can
confirm you are pointed at the right place, not as an invitation to look at anything else.
**If the deploy fails: fix the root cause and re-verify end to end, or stop and report. Never skip a
failure and never leave it half-applied.**
**If any of this looks wrong, say so** — that is rewarded here.

PROVENANCE:
- Kam's 13:40 deploy word | verbatim from /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_log.json - Wednesday's own tree, not yours | read 2026-09-07
- develop `632f16dfe`, unmoved | `git ls-remote git@github.com:Secuura/Distributed_Secuura.git` from Wednesday's seat | read 2026-09-07
- The seed-inside-the-try deploy precondition | s145's own round-2 carry, in its 2026-09-07 mails and HANDOVER-s145.md in YOUR OWN tree | read 2026-09-07
- That the seed throws 42P10 on every boot and has never seeded | KS-962's own BLUF, read on the board | read 2026-09-07
- That nothing in #885 post-revert remediates Kam's row | the KS-949 round-2 gate verdict and s145's revert receipt | read 2026-09-07
- The demo runs on a VM, not the retired Container Apps estate | s145's reconciliation of the gate's `services.bicep`/`env.demo.json` findings | read 2026-09-07
- Kam's week-scoped production grant and its flagging condition | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-07_production-ban-lifted-for-the-week.md - Wednesday's own tree, not yours | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 13:43
This mail SUPERSEDES the standing "No deploy" hold in my 02:57:41Z successor brief, my 03:13:40Z NO GO
and my 03:34:02Z ack — by Kam's own 13:40 word, not by my judgement. Every other hold in all three
stands, including that #888 is untouched while gated and that #880/KS-577 remains Kam's.
