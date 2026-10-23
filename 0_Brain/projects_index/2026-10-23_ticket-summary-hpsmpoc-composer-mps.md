---
date: 2026-10-23
type: board-summary
source: Kam's live-board ask 11:04:14 ("active (and backlog) ticket summary for HPSM-Poc, Security Composer and MPS calculator"); Jira read-only, paged to the last page (isLast=true); Composer from its BACKLOG.md
status: snapshot — 2026-10-23 ~11:15 AEDT
---

# Datasec — ticket summary: HPSM-POC · Security Composer · MPS Calculator

## BLUF
- **HPSM-POC (Jira HPSMPOC):** 325 tickets · **122 open** (3 In Progress, 119 Backlog) · 203 Done. 27 of the open ones wait on you or HP.
- **MPS Calculator (Jira MPSCALC):** 316 tickets · **302 open, all Backlog** (0 In Progress) · 14 Done. 23 are labelled needs-ruling.
- **Security Composer:** has **no Jira board** (key PCOMP was never created; you ruled "keep parked", C-71). Its board is `BACKLOG.md`: 358 rows · **~77 open** · **11 waiting on you** · 11 partly done · 259 closed/fixed/ruled.
- **Caveat:** Jira status lags the work. MPS was deployed today while its board shows 0 In Progress (302 Backlog, 14 Done); three HPSM-POC "In Progress" tickets haven't been touched for 1–3 weeks. Read the counts as the board's view, not as measured progress.

## Recommendation
No action needed. If you want one thing: the **6 High-priority MPS tickets** (care packs and purchase usage, listed below) are the clearest next build lane, and **HPSMPOC-237** is a money decision that's been waiting.

## Detail

### HPSM-POC — Jira HPSMPOC (keys 1–325, all 325 returned)
| Status | Count |
|---|---|
| In Progress | 3 |
| Backlog | 119 |
| Done | 203 |

Open by type: 112 Tasks, 9 Epics, 1 Sub-task. By priority: High 4 · Medium 108 · Low 7 · Lowest 3.

**In Progress (all stale):**
- HPSMPOC-87: customer questions, using the 16 as the base (DRAFT for Kam). Last updated 10-01.
- HPSMPOC-90: feedback button sends each submission to Jira and emails you. Last updated 10-06.
- HPSMPOC-91: client collateral packs (pre-, during- and post-engagement). Last updated 10-16.

**High:** the three above, plus HPSMPOC-94 (guided expert remediation) and HPSMPOC-97 (HP follow-ups from 29 Sep).

**Open by epic:** WS8 DevOps/QA 17 · Commercial & Governance 14 · WS6 HP Recommendation 6 · WS1, WS4, WS7 4 each · WS2 3 · WS3, WS5 2 each · 56 have no epic. Most of those 56 are gate findings and test follow-ups.

**Waiting on you or HP (27):**
- owner-kam: -3 (executed POC SOW), -6 (name the PO and security SME), -20 (prototype PO approval), -51 (manual-delivery baseline)
- Awaiting HP: -82 to -86 (Security Manager, Quick Assess, Control Hub, firmware tool, Fleet Assessment), -97, -166, -181, -241
- needs-kam: -90, -91, -94, -162 to -168 (C-34 playbook set), -237 (**money:** browser read latency), -242 (Paul's showcase feedback placeholder), -257, -268 (.NET runtime)

**Most recent activity (10-22):** -148, -177, -178, -187, -204, -310 (being worked through today's merges), -224 (telemetry, **ended by your ruling** after B505 NO GO), -321 to -325 (new gate findings).

### MPS Calculator — Jira MPSCALC (keys 1–316, all 316 returned)
| Status | Count |
|---|---|
| In Progress | 0 |
| Backlog | 302 |
| Done | 14 |

Open by type: 284 Tasks, 15 Epics, 3 Bugs. By priority: High 6 · Medium 270 · Low 26. 227 have no epic; "Questions for Kam" (MPSCALC-15) holds 17.

**High (6):**
- -140: import care packs into the price book
- -141: Synnex price-book coverage
- -142: new "Care pack" item class
- -148: inventory picker that adds several items at once
- -150: purchase usage redesign
- -151: software licence must cover the whole term, paid upfront

**Bugs (3):** -90, -91, -92 (source version store and document checks).

**needs-ruling (23):** -95, -109, -112, -113, -128, -129, -137, -144, -153, -157, -159, -177, -188, -202, -204, -222, -224, -226, -228, -229, -230, -261, -316.

**Most recent activity (10-20/21):** gate findings -289, -299, -304 to -311, -316, and the v2/v3/v4 feature items -245, -249.

### Security Composer — `BACKLOG.md` (no Jira)
358 rows. Classified by the leading state word in each row:
| Class | Rows |
|---|---|
| Closed / fixed / deployed / ruled | 259 |
| Open / deferred / backlog | 77 |
| Waiting on you (KAM'S CALL, ready for review, blocked on approval) | 11 |
| Partly done (half deployed, mixed) | 11 |

- **33 of the 77 open rows are one plan, the SRO_VIC lanes L0–L9** (rows #328–#362). Your K1–K10 rulings are in. Most rows are "not started", and later lanes wait on L1–L3.
- **Waiting on you (11, as the rows read today; some date from September and may already be settled by later rulings):**
  - Ready for review: #1, #17, #21 (Paul's guide v1.2/v1.3 and the two examples)
  - Your words: #35 (Seat C wording)
  - Calls from the gates: #54, #55 and #101 (KAM'S CALL)
  - #73: B41 UX proposal
  - #249 and #252: the E8 content release and its deploy
  - #329: SRO_VIC questions, ready for you to send to Paul
- Classification caveat: this is a regex over each row's first state word. "Partly done" and some "FIXED (not deployed)" rows are judgement calls; 99 rows contain the words "not deployed", some of them in history text.

### How measured
Jira: `/rest/api/3/search/jql` paged with nextPageToken until isLast=true (4 pages each). Totals are cross-checked against the key range: HPSMPOC 1..325 = 325 unique, MPSCALC 1..316 = 316 unique. Note: `fleet/board_count.sh` refused both boards because it does not page past Jira's 100-row page. That refusal is correct, but it means the tool cannot count any board over 100.
