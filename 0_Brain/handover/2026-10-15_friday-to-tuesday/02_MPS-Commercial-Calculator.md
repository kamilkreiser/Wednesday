---
date: 2026-10-15
type: handover
project: Datasec/Datasec MPS Commercial Calculator
from: Friday → Tuesday
client: Datasec only
status: live
---

# MPS Commercial Calculator: handover (Friday → Tuesday, 2026-10-15)

## What it is (the project's CLAUDE.md is the source)
A **guided MPS quote builder** for HP Managed Print Services deals, to be sold to HP MPS partners (internal Datasec project).
The flow: discovery → recommended HP devices → fleet → device options and HP software term licences → **deterministic server-side
pricing** (Synnex Core/Growth/Scale tiering, configured capital, supplies cost-per-page, finance annuity, target-GP gross-up,
base + mono/colour click, GP, contract value, GST) → review/approval/immutable snapshots → customer-safe and internal exports.
**The workbook's formulas are the calculation rules**
(`1_Project_Definition/Architecture/2026-09-30_workbook-calculation-register.md`). Related to HPSM but **separate**: no
shared code, repo, tickets or runtime (Kam, 2026-09-30).

## Where everything is
| What | Where |
|---|---|
| Project root | `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/` (quote it: spaces) |
| Code repo | `2_Project_Files/` → `git@github.com:datasecau/MPS-Commercial-Calculator.git`. ⚠ The root checkout sits on an old branch (`b03/api`); seats work in worktrees under `2_Project_Files/.tools/wt-*`. Never build in the root checkout. |
| Records repo | the project root itself, **LOCAL ONLY, no remote** (records main `12554b7`). Never tell a records seat to push it. |
| Boot reads | `CLAUDE.md` → `1_Project_Definition/CLARIFICATIONS.md` (C-nn rulings; 464 lines) → `1_Project_Definition/Questions_and_Answers/00_QUESTIONS_FOR_KAM.md` |
| Briefs + STATUS | `1_Project_Definition/Briefs/` (newest: B97, 2026-10-14) |
| Jira | project **MPSCALC**, board **608**: https://team-1634009483756.atlassian.net/jira/software/c/projects/MPSCALC/boards/608 (tickets through MPSCALC-135 filed) |
| Hosted | `https://app-mpscalc-showcase-u6agl3edszqvs.azurewebsites.net` (`/health` → 200). Datasec agent-controllable env; see the project's SETUP_RUNBOOK for tenant/SP. |
| Users | **Paul Waite** (Datasec, `Paul.waite@datasec.com.au`) uses the hosted calculator and gives feedback. The 10-12 mail "[MPS Calculator] How you and Paul sign in" covers sign-in. |
| Rental words pack | `FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-14_mps_rental_book_words_pack.md` (shared repo) |

## State at handover (measured 2026-10-15 ~10:5x AEDT)
- **main = `e2990622`** (#40, B94 rental full proposal book; gate B95 GO WITH NOTES; main ci 38418311905 green).
- **Hosted = `b9a3d769`** (B92, deployed + live-checked 10-13 22:23; Paul emailed CC Kam). So hosted is behind main by #40.
- **Open PR #41**: B97, the three Kam-approved rental-book word fixes (Kam ruled **a** on card `mpscalc-rental-book-words-1014`
  at 10-14 06:57). Head **`7dd8dc8d93a3bacd0e58c6ea5c8d856973f2f6dc`**. Friday's tier-2 review at source = **GO** (3 files: rental.ts,
  RentalDocument.tsx, one test; strings byte-equal to the pack; seat 6/6 red-on-main/green-on-head, Vitest 608/608, fit checks
  macOS + Linux). **It waited only on GitHub Code Security, which is now ENABLED.**

## NEXT WORK, in order
1. **Merge #41.** If CodeQL has not started on the PR, push an empty commit with the identical tree (API, fast-forward). Then
   `merge_when_green.sh datasecau/MPS-Commercial-Calculator 41 <head-sha>` → confirm parent/tree → read main ci to the end.
   ⚠ **Expect the .NET Pkcs advisory** (GHSA-846f-f764-76mx) that turned HPSM-POC main red on 10-14 to hit MPS's next ci
   too, if MPS's API is .NET. If it does, the fix is HPSM-POC's B248 shape: pin `System.Security.Cryptography.Pkcs` 9.0.21 the repo's
   way, tier 2. Never dismiss the alert.
2. **Hosted deploy** of the new main (ships `b9a3d769..main` = #40 rental book + #41). Use the B92 brief's shape
   (`FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B92_SEAT-F_hosted-deploy-b9a3d76.md`); rollback = the hosted
   `b9a3d769` package. Card Kam first (MPS hosted has been card-per-deploy). Then your OWN live check: `/health` 200, and the
   served `assets/index-*.js` must differ from the previous build's and equal the seat's built name. Then tell Paul (CC Kam)
   what changed, but only on Kam's word.
3. **Records seat:** comment MPSCALC-129 (B97); record the **three unrecorded card rulings** from 10-12/10-13 (Paul invite ×2,
   hosted bf60fe8) as C-entries; tickets from B95/B97 notes.
4. **Paul's guest-redeemed check:** has Paul redeemed his guest invite? It needs a seat with Graph read.

## Guardrails specific to MPS
- Pricing is deterministic and server-side. Any number change needs a workbook-register row and a red-first test.
- Customer-facing words are Kam's. New words go to him as a words card (the 10-14 pack is the model). No seat ships
  unapproved words; a gate sweeps for NEW WORDS.
- Nothing to Paul, HP or any partner without Kam's explicit send.
