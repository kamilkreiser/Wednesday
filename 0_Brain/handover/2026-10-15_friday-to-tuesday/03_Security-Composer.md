---
date: 2026-10-15
type: handover
project: Datasec/Datasec Security Composer
from: Friday → Tuesday
client: Datasec only
status: live
---

# Datasec Security Composer: handover (Friday → Tuesday, 2026-10-15)

## What it is (the project's CLAUDE.md is the source)
Datasec's own multi-tenant **Policy Composer** product (NOT HP SOW-01 work): it turns an engagement's answers into one HPSM
security policy and the documents that go with it. It was built inside HPSM (S39–S50, 2026-09-10 → 09-17), became standalone on
2026-09-24 (C-01), and was **fully separated from HPSM** on Kam's 2026-10-02 ruling ("please seperate fully", C-18). No HP
marks and no HP-NDA material in the repo.

## Where everything is
| What | Where |
|---|---|
| Project root | `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/` (quote it: spaces) |
| Code repo | `2_Project_Files/` → `git@github.com:datasecau/Datasec-Security-Composer.git` (renamed from HPSM-light 10-02). Its `README.md` is the technical front door. Fetch/push via `3_Access_Keys/composer_github_deploy_rw`. |
| Records repo | the project root, **LOCAL ONLY, no remote** (records main `06124b9e`, 2026-10-13). **Never tell a records seat to push** (B151 flagged a brief that did). |
| Worktrees | ~150 `_wt_b<nn>[base/rec/rp/ci…]` folders at the project root, one per brief. Many are finished. They take real disk on a nearly full drive. **Archiving them is a cleanup to propose to Kam, never to do silently** (lesson `2026-10-10_merge-and-archive-when-done-and-ready.md`). |
| Quarantines | `_quarantine_<date>_B<nn>_*`: root-copy strays a seat left behind, moved aside rather than deleted. Leave them. |
| Boot reads | `CLAUDE.md` → `1_Project_Definition/CLARIFICATIONS.md` → `1_Project_Definition/Reference_from_HPSM/HPSM_CLARIFICATIONS.md` (Composer rulings made while inside HPSM) |
| Briefs + STATUS | `1_Project_Definition/Briefs/`. Gate STATUS files often live in the gate's records worktree, e.g. `_wt_b153rec/1_Project_Definition/Briefs/2026-10-14_B153_STATUS.md`. **Glob both places when watching.** |
| Backlog | `BACKLOG.md` (no Jira board for Composer). Friday's 10-13 screen: `FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_composer_backlog_screen.md` |
| Demo site | URL + login in `4_Credentials/.env` (`COMPOSER_DEMO_URL/USER/PASSWORD`). Never in a document, screenshot or commit. The demo site is Kam's: click through it, never reconfigure it. |
| Demo deploy doc | `FRIDAY/2_Project_Files/friday/composer_demo_deploy.md` (shared repo): how Friday deployed to the demo |
| User guides | `1_Project_Definition/User_Guide/` (Paul's guide, newest `2026-10-09_Paul_v1_5`) |

## State at handover (measured 2026-10-15 ~10:5x AEDT)
- **main = `45591406`** (#78, B149 Lane W web fixes; gate B150 GO WITH NOTES). **Demo = `ef916ce2`** (behind main).
- **Open PR #79**: B152, Kam's approved words (12) and looks (L05, L06). Kam ruled **a** on cards `composer-words-comp19-b149-1013`
  and `composer-look-comp18-b149-1013` (10-14 06:57). Head **`fa5a0b6a0559db23c9702ab390a417d046eb6483`**. Gate **B153 = GO WITH NOTES**
  (14 rows byte-equal source/bundle/screen, 13 no-change rows untouched, NEW WORDS 0, L06 reach GO, W13 = 7 sentences GO, red-proof
  sample GO). Friday's completion check = GO. **It waited only on Code Security, which is now ENABLED.**
- **Open Kam card:** `composer-l05-setup-card-too-1014`. B153 N1: L05 (the approver email width change) also reaches the **Expert
  set-up card** (ApproversTable used at CreateEngagement.tsx:682 and ExpertSetupCard.tsx:167; Email column 143→533 px at 1280).
  Rec a = accept. Default: merge when Code Security allows, **nothing to demo until he taps**.

## NEXT WORK, in order
1. **Merge #79** once Kam taps the L05 card (or per the card's stated default: merge allowed, demo waits for his tap).
   CodeQL empty-commit trick if it does not start → `merge_when_green.sh datasecau/Datasec-Security-Composer 79 <head>` →
   parent/tree check → main ci ("Push on main") to the end.
2. **Demo deploy** of the new main under the push-to-demo grant, **once Kam re-confirms the grant is yours** (see 00_START_HERE).
   Carry B150-N1. Live-check the demo afterwards by clicking through, never by reconfiguring.
3. **Records seat** (local, no push): tickets **B153 N2** (long names still overflow) and **N7** (a flaky pre-existing ci.sh step);
   note B153 N3 (6 renamed tests) + N6 (B152 ran `git fetch` + `git worktree add` in the ROOT checkout: a deviation, measured,
   origin/main ef916ce2→45591406, 5 worktree entries). Records tidy: ~40 stale BACKLOG rows.
4. **Lane O** (db / docs / ops) from the 10-13 backlog screen; then Lane A/R.

## Guardrails specific to Composer
- Every customer-facing word and look is Kam's: words and looks go to him as card PACKS (pack.md + card.json + shots/; B151 is
  the model). A gate sweeps the AST and the bundle for NEW WORDS, with planted controls.
- Nothing goes to Paul or any human without Kam's explicit send. Paul's user guide is updated only when Kam asks.
- Brief seats to work ONLY in their own `_wt_*` worktree. The root `2_Project_Files` takes read-only verbs only (B152 broke this once).
