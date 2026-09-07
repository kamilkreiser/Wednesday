---
date: 2026-09-07
type: pickup
scope: SECUURA + Wednesday's own work. Datasec belongs to the LAPTOP seat — see NEXT-PICKUP-DATASEC-LAPTOP.md and do not touch it.
source: replaced WHOLESALE at the 65% checkpoint by the 12:3x seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — ~14:05 AEST Sunday. ONE seat live (deploying). #888 is a GO awaiting its merge.

**Run `2_Project_Files/tools/kam_rulings_today.sh` before writing anything — read EVERY line.**
Mail timestamps are UTC ≈ AEST−10. Voice allowed. **ROTATION BAND 80–90% (Kam 10:49); 70% is a
CHECKPOINT ONLY.** The watcher's corrected wording is confirmed live — a 65% wake at 14:05 cited
"band is 80-90, Kam 09-07 … do NOT wind down and do NOT rotate".

## 🔴 KAM'S LIVE INSTRUCTIONS TODAY — all four still operative
1. **13:06 — the Azure/Founders Hub CREDIT subject is KILLED.** *"Do not worry about the Azure
   credits. Kill all tickets and all elements that query this."* **13:10: "clawed credits" = CLAUDE
   credits** — the cost he named is our own re-litigation burn. **(NB: "Azure" as a SQL file in the
   repo is a different subject and is live — see §AZURE below.)**
2. **13:23 — the unit of a ticket is the TEST PASS.** One test proves it → one ticket, items inside.
   Split only on separate workloads or separate fixes. **This governs CREATION, not retrofit.**
3. **13:40 (a) — board judgement calls are ours.** *"use the findings to action the tickets… happy for
   you to take this and make judgment calls as I focus on the dataset project."* **No time window.**
   **Does NOT cover:** Peter's/Stuart's tickets, deletion, #880, KS-61, the signature classes.
4. **13:40 (b) — the deploy hold is LIFTED by its owner.** *"there are a number of items in tested but
   not deployed. Feel free to deploy."*

**He is heads-down on a "dataset project". Queue NOTHING for him. Every ask carries its own default.**

## 🔴 FIRST ACTION — check the deploy, then the merge
**`%152` (s146) has been deploying develop `632f16dfe` to the Secuura DEMO since ~13:44** (SSH to the
demo VM; ctx 44% at 14:05). **Read its receipt before anything else.**

**Then: MERGE #888 at `9710cc1fde36109f3ad6fc34d792801d4357fab9` — that SHA, no amendment.** It came
back **GO-with-findings** at 03:56:49Z, round 2 of 2, all five findings CLOSED and measured. The merge
GO is already sent and deliberately DEFERRED behind the deploy receipt (moving develop under an
in-flight deploy is the gated-subject-moving failure).

## 🔴 THE TWO OPEN MAJORS — both PRE-EXISTING, both equally open on develop
**F3-RESIDUE.** With BOTH rows present (the `…0020` id carrying a different address + a distinct row
holding `admin@secuura.com`), the id-row UPDATE throws **23505** on `users_email_lookup_hash_uniq`,
the `catch` at `userRepo.ts:1506` swallows it and `continue`s — **so the entire F3 fix NEVER RUNS.**
Proved by ISOLATION (neuter only the id guard → the email arm works perfectly) and a CROSS-SHA control
(round-1's file reproduces it). **AND A GREEN CELL ASSERTS IT IS HANDLED** — it passes only because
the vitest `db` double returns `{rows:[]}` and cannot enforce a unique index. **⚠ THE F3-RESIDUE TICKET DOES NOT EXIST YET — Wednesday referred to it in three mails as though it
did, and s146 correctly REFUSED to invent an identifier** (citing this morning's KS-964 branch
mislabel). **The newest issue on the board is KS-967.** The unique-index measurement is parked on
**KS-966** with an explicit note that it moves to the residue ticket when filed. **FILING IT IS THE
NEXT BOARD ACTION** — after the deploy receipt, by s146 or its successor. **Ticket + the
misleading cell = a follow-up, NOT an amendment to #888.** Fix-shapes: email-row-first ordering, or
make the id rewrite conditional on `!emailRowIsDistinct`, or one transaction. **The regression test
must run against a REAL Postgres — a mock cannot express this defect.**

**§AZURE — round 1's biggest NOT-TESTED, now measured, and it is a condition on any future deploy.**
On `deployment/azure/migrate/init.sql`: **no `email_lookup_hash`, no `tenant_id`/`tenant_slug`, 0 of 3
`auth_find_user_by_email_*` functions.** The remediation **errors out and does not run at all.**
**So if the demo box carries the Azure-init schema, deploying #888 remediates NOTHING there.**
s146's KS-960 note ("no FK, so it is docker/init") is **evidence, not a measurement.** **Wednesday
asked s146 to capture the schema SHAPE (column/function names only, no row data) as part of verifying
its own deploy — and told it to REFUSE if it thinks that is a widening of Kam's spent probe
authorisation.** Check which it did.

**THREE live possibilities for Kam's row and none excluded:** remediated · skipped by the 23505 ·
nothing runs (Azure schema).

## BOARD — catalogue delivered and executed; both board seats CLOSED
`5_Project_History/catalogue-2026-09-07/` — the one page, the 323-row appendix, and
**`HIERARCHY-CONSUMERS-2026-09-07.md`**. **Board 280 open.** 11 archived, 6 held with the reason ON
each ticket ("so the next sweep does not re-propose it"), 0 deleted, 0 of Peter's/Stuart's touched.

**THE RESTRUCTURE IS CANCELLED — do not re-propose it.** Linear allows ONE PARENT PER ISSUE; **207
issues already sit under 26 parents** (control: `parent:{null:true}` → 750), and **the EXTRANET
republishes the hierarchy** (`linear-report.ts:542/353/111`). Review streams win the slot — Kam
adopted them as the process. **Archiving preserves the parent link; re-parenting is not free.**
**88 → 50 is a description, not an instruction.**

**Still Kam's:** the 13 outranked (now 11 archived / 6 held), the legacy set, KS-642/644/681 (resolved
at source — evidence was in the comment bodies), KS-418's false AWS premise in three shipped docs
(**queued for s146, a code seat**).

## S146's QUEUE AFTER THE MERGE
KS-952 (**ONE mechanism, TWO ASYMMETRIC RULES** — `/check` strict, `/reset` NOT; **KS-645 stays
Duplicate**) → the KS-418 doc fix → KS-966 items 3+4 (**item 4 opens with the MEASUREMENT**).
**#889 (KS-597) is open.** **KS-967 filed for F4** — `no-tracked-credentials.sh`'s own self-test at
`:51-53` ASSERTS the `.env.example` exclusion, so any fix must change that self-test deliberately.

## WHAT WEDNESDAY GOT WRONG TODAY — carried so a successor does not repeat it
- **Ratified s145's site-8 split; the gate falsified it.** A claim about the PRODUCT is not a shape.
- **7 of 17 tickets in an archive list were wrong** — a classification list is a REPRESENTATION.
- **Extrapolated a CREATION rule into a RETROFIT** — read the verb.
- **Called a 60-ticket restructure "reversible"** with nothing establishing the blast radius.
- **Fifth raise of the Azure credit subject** — the prior-ruling gate now has a CARD-ID LINEAGE leg
  (`decision_queue.sh`, backup `.pre-0907-cardid`); three of the four Founders Hub cards would now be
  refused at creation.

## ⚠ LEDGER SIZE — measured, not actioned
**`_ledger.md` is 332 KB, LARGER than the 276 KB by-tier boot digest** — the exact condition of Kam's
card `wed-ledger-boot-cost`, **still unruled**. It grew ~65 KB this afternoon (17 rows from the 12:3x
seat). **CLAUDE.md 3c archives rows older than ~3 days; the 09-05 rows are 2 days old and were
DELIBERATELY NOT moved** — the rule is a cadence, not a lever to hit a size target. **Do not re-card
it** (Kam is heads-down and the card exists); the measurement is now line 5 of the consolidation KPI,
where it will be acted on beside the board's 30% number.

## 📨 A DATASEC/NEXUSAI REPORT LANDED AND IS **NOT THIS SEAT'S** — do not answer it
**RESOLVED 15:1x: the laptop seat IS ALIVE** — it pushed `cb646a4a` at 15:08 (*"hook: self-locating
project root — it was bricking the T9 seat"*). A rejected push told Wednesday that, better than the
question did. **So the report has an owner. Leave it.** **And PULL BEFORE EVERY WRITE — that is twice
today origin moved under this seat.** Do NOT `git stash push` before `pull --rebase`: the rebase
autostashes by itself and doing both produced a 12-file conflicted pop (resolved, quarantined at
`5_Project_History/_quarantine_2026-09-07_rebase-conflicts/`, all stashes kept).
**05:09:46Z, `[Datasec/NexusAI -> Wednesday] RD-361/362/363/364 FILED · cat-1 = 102 of 285 ·
Marketplace blockers named`.** Subject read; **body deliberately NOT read and NOT acted on.**
**Kam partitioned the machines at 11:01: Secuura here, Datasec on the LAPTOP.** That agent was
unpaused and briefed by the LAPTOP seat, not this one — answering it would mean ruling on a thread
whose brief this seat has never seen. **Leave it.**

**The one live risk:** Kam said at 11:25 he would resume the laptop *"at 3 when the rate limit
resumes"*. It is past that. **If the laptop seat is NOT up, this report sits unanswered** — and
Marketplace blockers matter, since Kam ruled the Marketplace objective at 10:48. **Flagged to him as
one line with a default: if he is silent, it stays for the laptop seat and this note is the record.**

## ⏱ THE ETA IS THE DISCRIMINATOR — tap at 16:15 if there is no receipt
**The waker fires on COMPLETION, not progress** (DONE · STOPPED_LOW_DISK · process-death). **A HUNG
build — stuck, not dead, not finished — matches none of the three and would leave everyone asleep.**
That gap is real and is accepted deliberately rather than fixed: polling on suspicion costs a seat's
turn every time and the seat is at 53%.

**So the ETA is the instrument. Build ETA ~16:05 AEST (11/31 at 04:41Z, ~4.4 min/service).**
**IF 16:15 PASSES WITH NO RECEIPT: tap `%152` for a one-call build count.** A count that has not moved
since 04:41Z means hung, and that is a stop-and-diagnose, not a wait. **The repeated frozen-pane
alerts are the clock** — use them, do not just dismiss them.

## ⚠ THE FROZEN-BUSY WATCHER WILL CRY WOLF UNTIL ~16:05
`%152` is **dormant BY DESIGN** — Wednesday told it to wait cheaply and it built a correct three-class
waker (DONE · STOPPED_LOW_DISK · process-death). **`wake_watch.sh:146-150` has no per-episode
suppression: once `fcnt >= 6` it re-fires on every qualifying tick.** So expect repeated frozen-busy
alerts on that pane until the build finishes. **Triage them with ONE combined command** (inbound-only
inbox + `pane_prompt_check.sh` + shell count), not three. **Do NOT re-arm the watcher while the deploy
depends on it** — fix shape recorded for the next quiet point: reset `fcnt` on fire, or a `fired_$key`
marker cleared when the hash changes.

## STANDING
No `cd` (hook). Taps ≤200 chars, **every tap has a verified mail behind it**. `<<'EOF'` for every
brief; **`-F -` with a quoted heredoc for commit messages** (an unescaped `"` in `-m` broke one today).
Never delete — quarantine/archive. **Read the verb against the WRITE list before any `git -C` outside
WEDNESDAY.** **What merges must be what was gated.** **Search before you file — by SYMBOL/PATH/ERROR
STRING, never your own phrasing.**
