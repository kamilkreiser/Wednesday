---
date: 2026-10-05
type: grant
source: Kam, live board 2026-10-05 16:21:39 (view=wednesday), as the note on card secuura-connector-allowlist-missing-setting-ks1256-1005
status: live
tier: W
expires: 2026-10-31 (end of Saturday; `date -j` confirms Saturday)
---

# Grant: through October, deploy everything that is READY to BOTH kintsugi and demo, without a card per deploy

**His words, verbatim (16:21:39):**
> *"for the month of October, keep pushing, keep publishing, deploy all that works and is ready but only when its ready.  Deploy to both servers, demo and kintsugi"*

**The operative case, so the headline matches it:** a Secuura change has merged on a QA gate GO and Wednesday is deciding whether a deploy needs Kam's tap, or whether demo waits for Peter's nod. **Until the end of Saturday 31 October it does not: deploy it, kintsugi first, then demo, and report the deploy.**

**Wednesday's reading, said back to him on the panel at 16:2x with a correction offer:**
1. "Ready" = merged on a QA gate GO **and** verified at source by Wednesday. Unmerged, ungated or unverified work is not ready.
2. **Kintsugi first** (his 2026-09-10 rule): deploy, then a live sweep on kintsugi; **demo after** kintsugi is swept clean.
3. For October this **lifts "demo waits for Peter's nod"** (EXPIRING-GRANTS TESTED-grant row and the 09-11 grant's demo clause). Wednesday's reading, flagged to him.
4. **Unchanged:** production (does not exist; still his), money, external communication to Peter or Stuart, anything irreversible; the KS-535 wallet rule (kintsugi never shares demo's `PLATFORM_WALLET_MNEMONIC`); Phase 0 re-tag before building, build-all-then-swap, migrations in the middle; flag every deploy in the report.
5. A migration on live data (KS-1401) rides the kintsugi deploy he ruled (card `secuura-tenant-isolation-migration-ks1401-1005` = a); it reaches demo only under this grant's "ready" test, after kintsugi has run it clean.

**How to apply:**
1. Every deploy brief names this file and the ruled card(s) as its authority, and states the box, the develop SHA and the rollback tag.
2. Report each deploy to Kam on the panel after it is verified on the running box: what went where, the SHA, what the live sweep found. The grant removes the pause, not the receipt.
3. **Expiry is a check, not a note:** the row in `tasks/EXPIRING-GRANTS.md`; on 1 November demo returns to Peter's nod and each deploy returns to Kam's tap. Do not renew by inference.

**Family:** [[2026-09-10_kintsugi-first-then-demo-behind-gates]] · [[2026-09-10_deploy-both-boxes-grant-expires-sunday]] (the September precedent, same shape) · [[2026-09-11_secuura-we-approve-and-merge-our-own-tested-work]] (its demo clause is lifted for October) · [[2026-09-06_a-scoped-override-carries-its-own-expiry]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5).
