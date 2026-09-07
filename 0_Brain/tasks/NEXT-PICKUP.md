---
date: 2026-09-07
type: pickup
scope: SECUURA + Wednesday's own work. Datasec belongs to the LAPTOP seat — see NEXT-PICKUP-DATASEC-LAPTOP.md and do not touch it.
source: replaced WHOLESALE at the 50% checkpoint by the 12:3x seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ~13:2x AEST Sunday. TWO SEATS LIVE. #888 is at ROUND 2 OF 2. The board catalogue is running.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything — and read EVERY line.**
Mail timestamps are UTC ≈ AEST−10. Voice allowed (06:00–23:00).
**ROTATION BAND IS 80–90% (Kam 09-07 10:49).** 70% is a CHECKPOINT ONLY. The launcher and the watcher
both carry the correct band; trust a wake that cites "Kam 09-07 10:49".

## 🔴 KAM'S TWO LIVE INSTRUCTIONS, both from the last twenty minutes
1. **13:06 — the Azure/Founders Hub subject is KILLED.** *"We're going in circles. Do not worry about
   the Azure credits. Kill all tickets and all elements that query this."* **13:10: "clawed credits" =
   CLAUDE credits** — the cost he named is **our own re-litigation burn**, not Azure billing.
   **Do not query Azure, the subscription, or the credit. Do not card it. It is closed.**
2. **13:21 — clear as you go.** *"Keep clearing these and addressing them. If there's any that can be
   addressed quickly, please do so."* The catalogue seat is widened from classifying to clearing,
   board-side.

## 🔴 FIRST ACTION: #888 ROUND 2 OF 2 — the cap is one NO GO from spent
**PR #888 `023acccf8` (KS-966 items 1+2) came back NO GO** from its tier-1 gate at 03:11:06Z.
**A second NO GO SPENDS THE CAP** — the closed instances ship and the residue is ticketed; no round 3
without Kam. The fix round was relayed to s146 at 03:13:40Z, **ahead of KS-597**, because F1 is live.

- **F1 BLOCKER, driven at runtime:** `Blockchain/Dev/.env.example:125` ships the retired literal, and
  `docs/DEPLOYMENT.md:381` + `developer-portal.html:382` both say `cp .env.example .env`. **The admin
  seeds ACTIVE AND LOGINABLE on the retired credential.** The PR's fail-closed branch is never reached
  on the documented path. Fix: blank the value, keep the key, add the regression cell.
- **F2 MAJOR:** the fail-closed hint at `userRepo.ts:1358/:1364` is hard-coded to
  `DEMO_SECUURA_PASSWORD` — wrong for `admin@secuura.com`, which THIS PR newly routes there.
- **F3 MAJOR:** the remediation is keyed on `getUserById`, so an `admin@secuura.com` row under any
  other id survives **ACTIVE with its old hash** (gate scenario S4, driven).
- **SITE 8 is item-1 work that did not ship** — see the retraction below.
- **F4, report-only, its own ticket:** **no gate in the repo can see F1.**
  `check-no-default-passwords.sh` scans only `services/`+`packages/`; `no-tracked-credentials.sh`
  **excludes `.env.example` by design.**

### ⚠ A RATIFICATION OF WEDNESDAY'S THAT THE GATE FALSIFIED — do not re-inherit it
Wednesday told s145 its **site-8 split** was right, scoreboarded it, and repeated it to Kam. **Wrong.**
`environment.ts:185`'s `??` arm is the **terminal fallback of the same chain**; substituting `''`
changes no routing; the argument contradicts the same PR's own `api-client.ts`; and it is **PINNED
GREEN by `environment.test.ts:91`**, which asserts the retired literal. **The named w=88 rule: a claim
about the PRODUCT is not a shape.** Scoreboard struck through in place; s145's 1.0 kept.

## FLEET — two seats, both healthy at the checkpoint
- **`%152` s146 (builder)** — ctx 25%. On #888 round 2. Queue after it: **KS-597's PR** (`af640e809`,
  0 PRs exist; Kam ruled `afterfix` on the 95k backfill — its own round AFTER the fix merges), then
  **KS-952** (cross-tenant rate-limit; **ONE mechanism, TWO ASYMMETRIC RULES** — `/check` strict
  derive-from-principal, `/reset` NOT, because a blanket bind breaks a real capability; **KS-645 stays
  `Duplicate`, do not reopen**), then **KS-966 items 3+4** with **item 4 opening on a MEASUREMENT**.
- **`%153` Blockchain-B (catalogue)** — ctx 17%. Board-only, no code. Widened to clear as it goes.
- **QA pane closed** after its verdict (listeners 25 → 25).

## THE CATALOGUE'S FIRST ANSWER — 293 open, and the headline is not "legacy"
**88 of 293 (30%) have a GUARD, GATE or TEST HARNESS as their subject rather than the product, and
72 of those were created in the LAST SEVEN DAYS.** Most exist because of gates Wednesday
commissioned. **Put to Kam as a measurement with a three-way split requested, NOT as a verdict.**
- **Legacy cluster, one cause:** six tickets presuppose a working GitHub Actions. **2,000 runs across
  20 pages, 100% `startup_failure`, back to 2026-08-20 — ≥18 days**, 16 dead workflow files.
- **KS-418 is worse than stale:** its false *"pending full AWS migration"* premise has **propagated
  into THREE PUBLISHED DOCS** (`systemTest/CLAUDE.md:1895`,
  `systemTest/docs/how_to_test_secuura.md:502`, `systemTest/performance/docs/quick_start.md:286`).
  There is no AWS migration. **Queued for a CODE seat, not the catalogue seat.**
- **The 23 in `Tested Not Deployed` are NOT archived** — the seat refused Wednesday's blanket
  authorisation and was right: **the deploy is held, so those tickets ARE the deploy manifest.**
  They archive AT DEPLOY TIME.
- **KS-869** sits in `Tested Not Deployed` with an **OPEN PR #880** — and **#880 stays KAM'S**.
- **Namespace trap:** PR numbers and KS numbers overlap. **PR #885 ≠ KS-885.**

## 🔴 THE DEPLOY — still HELD, deliberately
**Nothing merged today remediates Kam's own row** — the fix that would have is the one the `split`
took out. A deploy ships four real improvements and would imply a fifth. **It goes ONCE, after #888
clears.** Kam has an active deploy grant and a production grant (**Secuura only, this week, read as
through Sun 2026-09-13**). **A gate GO is not a deploy GO.**

## MECHANISM BUILT THIS SEAT — and it is the one that stops the circling
`decision_queue.sh` **leg 2: CARD-ID LINEAGE.** Leg 1 scored Kam's PROSE against a card's words minus
stopwords — and **`secuura` is a stopword**, so his two 09-05 closing messages shared ONE scoring word
with the 09-07 card when the gate needs two. **He closes subjects with pronouns** ("this", "the hub"),
never the subject's nouns. Leg 2 matches a new card's id tokens against **cards he has already ruled**.
**Five cells exercised; two defects found only by RUNNING it** (a guessed field name that made the fire
cell pass silently; a flat rarity ceiling that went blind on the subjects raised most often — the
identical flaw it fixes). **Three of the four Founders Hub cards would now be refused at creation.**
Backup `decision_queue.sh.pre-0907-cardid`.

## STANDING
No `cd` (hook-enforced). **Every tap ≤200 chars and every tap has a MAIL behind it**, verified by
`preview` non-null or by `say --mail`. `<<'EOF'` for every brief. **Name a branch from a ticket that
EXISTS** (#888's says KS-964 and means KS-966 — a disclosed mislabel, do not re-report it).
**Client-facing communication is ticket comments only; Kam sends any WhatsApp.** **#880/KS-577 stays
Kam's. KS-61 stays quarantined and is Stuart's.** **Never delete — quarantine.** **Read the verb
against the WRITE list before any `git -C` outside WEDNESDAY** (hook-enforced since 12:0x).
**What merges must be what was gated.**
