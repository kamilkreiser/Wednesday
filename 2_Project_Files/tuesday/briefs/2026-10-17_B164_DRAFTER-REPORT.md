# B164 DRAFTER REPORT · records seat for the MPS gate findings of 16-17 Oct + merge comments for PRs #45-#72
Written 2026-10-17 07:56 AEDT by Tuesday's drafter. Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-17_B164_SEAT-R_mps-records-gate-findings.md`.

## BLUF
- **87 non-blocking candidates** from six gates + the 153 half. They go into **24 grouped tickets**, **2 finding comments**, **36 merge comments**, **24 BACKLOG rows** (+ a Jira line on 3 existing rows), and **21 skips**. Expected last line: `DONE: B164 24 tickets filed, 2 comments, 36 merge comments, 21 skipped (closed/duplicate)`.
- **No gate finding is already its own ticket.** The board's highest key is MPSCALC-188 and nothing was created today (`created >= "2026-10-17"` → 0). Dedupe hits fall into two groups:
  - 17 items are residuals of EXISTING tickets whose acceptance the gate measured NOT met. They go into comments on those tickets (13 in merge comments, 4 in 2 finding comments).
  - 1 item is a duplicate (self-approval → MPSCALC-137).
- **All 28 PRs (#45-#72) merged 36 tickets with no Jira update.** Every ticket is still `Backlog`, and a search for the merge shas finds 0 (control `0f8ad97` → 8). So the gap is wider than #69/#71/#72: it covers all 36 tickets.
- **No transition** on any ticket. The project's own rule (`history.md:276`) is: *"Jira not transitioned (no project rule moves a ticket on merge)"*. The workflow has no merged or deployed state (Backlog / Selected for Development / In Progress / Done). Hosted is card-per-deploy on `0f8ad97`.
- **UNMEASURED:** nothing on the "MPSCALC-153 governed half". It is established below.
- **8 items need Kam (K1-K8).** They are flagged, NOT filed.

## Candidates per gate
| Source | Candidates | → tickets (items) | → comments (items) | KAM-only | Skipped |
|---|---|---|---|---|---|
| B157 (`2026-10-16_B157_STATUS.md`, 13 findings, 10 proposed rows) | 13 | 9 items → R01-R06 | 3 (MC 174, 165, 163) | 0 (+K2 half of C05) | 1 rec (B157-11) |
| B158 (`…_B158_STATUS.md`, B158-1..-14 + parity note) | 15 | 4 → R07, R08 | 5 (MC 174 ×1, 151; CMT 158 ×2, 150) | 1 (B158-11 → K1) | 5 closed (-1, -2, -3, -6, -14) |
| B159 (`…_B159_STATUS.md`, B159-1..-14 + 3 REPORTs) | 17 | 8 → R03, R09-R13 | 3 (MC 147, 170 ×2) | 2 (B159-7 → K6; REPORT ii → K8) | 3 closed (-1, -2, -6), 1 dup (REPORT i → MPSCALC-137) |
| B161 (`2026-10-17_B161_STATUS.md`, B161-1..-17) | 17 | 12 → R07, R14-R17 | 1 (MC 105) | 1 (B161-10 → K3) (+K4 half of C49) | 1 closed (-15), 2 rec (-8, -9) |
| B162 (`…_B162_STATUS.md`, -1..-8, 6 REPORTs, register row + 2 clauses) | 16 | 10 → R18-R21 | 4 (MC 147) | 1 (REPORT g → K6) (+K5 half of C70) | 1 rec (REPORT d) |
| B163 (`…_B163_STATUS.md`, -3..-7, OPEN (a); -1/-2 live) | 8 | 5 → R07, R22, R23 | 1 (CMT 158) | 0 | 2 live (B163-1, -2: B103 ADDENDUM-4) |
| MPSCALC-153 governed half | 1 | 1 → R24 | 0 | 0 | 0 |
| **Total** | **87** | **49 → 24 tickets** | **17 items → 2 + (in) 36** | **5 (+4 halves)** | **21 incl. KAM-only** |

**Closed by a later gate, NOT to be filed:**
- B158-1, -2, -3 closed in behaviour (B163 :4-6).
- B158-6 (B163 :198), B158-14 (B163 :305).
- B159-1, B159-2 (own shapes), B159-3 (test), B159-6 (behaviour) (B162 :343-346).
- B161-15 (#71 merged with checks SUCCESS).

**Live round, not filed:** B163-1 and B163-2 (lane D, ADDENDUM-4).

**Lane D's next round, not filed:** B163 OPEN (a) together with B158-8. Only a pointer comment goes on MPSCALC-158.

## The MPSCALC-153 governed half (established, not UNMEASURED)
Searched: `grep -i 153` over `Briefs/2026-10-16_B10*_STATUS.md` and the Briefs folder.
- **Source:** `B100_STATUS.md:393-396` + `2026-10-16_B100_ANSWER-1_153-keep-values-split-ticket.md`.
- **What it is:** MPSCALC-153's acceptance says *"values live in a governed setting or source table, not in code"*. Lane A built the hint with the ruled values in `web/src/components/infoHintWords.ts`.
- **Tuesday's ruling (ANSWER-1 (a)):** keep the values, leave 153 open, and *"Propose ONE new BACKLOG row/ticket for that half"*.
- **What exists:** BACKLOG `[B100-2]` (`BACKLOG.md:1561`) and Jira comment 39508. It was never ticketed (`text ~ "\"governed setting\""` → 1, 153 itself).
- **Action:** file R24, and append its key to `[B100-2]`.

## PR enumeration (the coordinator's addition)
- **Tool:** a read-only `gh api -X GET …/pulls?state=closed&per_page=100` under `<project>/4_Credentials/.gh-config` (`gh auth status`: kamilDatasec). The `gh` path worked, so git log was not needed.
- **Result:** **28 PRs merged at or after 2026-10-16T05:00Z (#45-#72).**
- **Controls:**
  - #44 (04:04:54Z) falls outside the window.
  - `ls-remote` main = `798fe98…` = #72's merge commit.
  - Tuesday's daily note 07:33 says "28 MPS PRs merged (#45-#72)".
  - 0 PRs are open.
- **36 tickets.** #47, #50, #51 and #59 are stacks. #68 is lane A's stack of 6. #60 and #62 both touch MPSCALC-174, so 174 gets one comment. **#70 (B160) has no ticket, so it gets no comment.**
- **Cleared by:**
  - #45-#53: tier-2 review at source (`2026-10-16_MPS-TIER2-REVIEW.md`).
  - #54: Tuesday's at-source review 16:48.
  - #55-#60: gate B157.
  - #61-#62: gate B158.
  - #63-#67: gate B159.
  - #68: tier-2 HOLD → refine → Tuesday's re-review of `32baa15` (no QA gate, although the review called 153 "tier-1-suspect").
  - #69: gate B162.
  - #70-#72: gate B161.

## Needs Kam (flagged in the brief's FOR KAM; NOT filed)
- **K1** A deal-usage proposal shows no usage charge (customer document; B158-11, carried).
- **K2** New words for a feedback-only 401 (R06 builds the behaviour; B157-5).
- **K3** A refused negative is shown under "values beyond the technical limits", with the raw code and JSON path (B161-10).
- **K4** Every deploy leaves a copy of the hosted overlay, with costs, on the operator's machine with no expiry (B161-4).
- **K5** Rental and proposal "Option(s)" headers, including the customer caption "Configured options (included in the base charge)" (B162-8).
- **K6** Colour-panel options reach rental quotes by pool tier, and purchase costs by the device pool tier (B159-7, B162 g). This is pricing reach.
- **K7** Entra script runbook: later runs need both flags (B159-12).
- **K8** At the deploy carrying #67, four-role sign-ins lose the act-as switch (B159 REPORT ii).

**Not Kam, but pricing-adjacent:**
- R08 is tier-1 with `calc-register`: blocked calculations still carry priced figures.
- R09 is a pre-existing Major: a plain Seller can price a repeated BOM line.
- R24 covers customer-facing pricing guidance values (ruled by Kam on 16 Oct, K-04).
- The X-23 cent-shift clause (R25 / the 147 comment) describes existing rounding, not a new rule.

## For Tuesday (decisions the seat cannot make)
1. **No transition on merge** follows the project's rule. If you want merged tickets moved, say so before launch. The seat will otherwise STOP if it finds a conflicting rule.
2. **R14** (PRE-1 widening, `[B107-2]`: "a ruling") and **R16** (WHO-before-WHAT order) carry `needs-ruling`. Both rulings are yours. R14 must land before the first hosted `overlay.json`.
3. **R17** (`scripts/package.sh`) and **R24** (server + price-book files) are in no lane's file list. You assign them.
4. **R25:** writing the K-06 calculation-register row (+ 2 clauses) is a records write the seat is NOT given. It is yours or a later records brief's.
5. **MPSCALC-153** stays open, as ANSWER-1 said, even though its unmet half moves to R24. You may want to close 153 once R24 exists.
6. **Found in passing:** an existing Jira comment on MPSCALC-157 quotes a branch name `b109/mpscalc-157-…` that carries a person's first name (lane G's branch). It is not in this seat's write scope (no edits to existing comments). Noted for your name-hygiene ledger.
7. `BACKLOG.md` and `history.md` hold other seats' uncommitted edits (`git status`: ` M BACKLOG.md`, ` M 5_Project_History/history.md`). The seat appends and does NOT commit.

## Method and limits (what I measured, what I did not)
- **Read whole:** the six gate STATUS files (B161 and B163 in two reads), B163's brief, B99's brief, `JIRA.md`, `BACKLOG.md` (head and `:1500-1607`), B103 ADDENDUM-2 and -4, B100 ANSWER-1, and the 153 lines of B100 STATUS. B104 STATUS `:228-236` was read in part.
- **Jira:** GET only, with my own client (scratchpad `b164/jget.py`). Credentials were read by name from the project `.env` inside the process and never printed.
  - 91 JQL searches (3 + 65 + 23), recorded with counts in the brief's table. The middle batch is saved in `b164/dedupe.tsv`.
  - Controls: `PRE-1` → 3, `zzqxvbw` → 0.
  - Statuses read for the 36 merged tickets and 17 hit tickets. Transitions read once (MPSCALC-147).
- **Not done:**
  - I did not read the calculation register file itself (`Architecture/2026-09-30_workbook-calculation-register.md`).
  - I did not check whether lane D's ADDENDUM-4 round will add a `ToDto` test. R23 assumes it will not, because ADDENDUM-4 names only B163-1 and B163-2.
  - I did not re-verify hosted (`0f8ad97`, cited from `B156_STATUS.md:243`).
- **Grouping judgement:** a hit on a ticket the gate measured MET is treated as RELATED, so a new ticket is filed and the related key is named. A hit on a ticket whose acceptance is NOT met is EXISTING, so it gets a comment. The brief states this rule for the seat (rule 2), so a fresh dedupe can only move rows from FILE to comment.
