# BLUF — Datasec/Vision_Sales_Portal: QUICKQUOTE DEPENDENCY ROUND (the 14 open Dependabot alerts). Kam ruled card quickquote-dependabot-14-round-1013 = (a) "Commission it now" (live board, 2026-10-16 12:13:02 AEDT, view=tuesday). Triage all 14, fix what can be fixed with the smallest dependency changes, ticket the rest, through a QA gate, merged to QuickQuote main through CodeQL on Tuesday's GO. NO deploy. Send a PLAN CONFIRMATION first.

**Scope, read narrowly.** QuickQuote dependencies only (datasecau/vision_hpas-quickquote, `stage3/`). The portal, ATTIO and the rest of the Vision backlog stay paused (2026-09-29).

## READ FIRST (all in the Vision_Sales_Portal folder)
1. `CLAUDE.md` WHOLE (the QuickQuote section, the production boundaries).
2. Your newest `5_Project_History/history.md` entry (the 2026-10-13 v2.35 round: QuickQuote v2.35 LIVE, image v0.6.3-tool2.35-3dd15bc; rollback v0.6.2-tool2.34-108bbb4 kept) and `1_Project_Definition/CLARIFICATIONS.md` (C-13, C-16, C-17).
3. Your 2026-10-13 fix-round brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-10-13_vision_qq_ci_codeql_fixround.md` (Tuesday's tree, read-only to you): the same round shape, gates and holds.

## MEASURED BY TUESDAY (2026-10-16 ~12:2x AEDT, read-only, Vision's GH_CONFIG_DIR)
- QuickQuote main = 3dd15bcc09 (gh api commits/main; 2026-10-13T00:44:55Z), the v2.35 merge.
- Open Dependabot alerts (gh api dependabot/alerts?state=open): **14 — critical 1, high 7, medium 6**, all in `stage3/package-lock.json`: #16 critical proxy-addr; brace-expansion #9 #10 #11 #12 (high) #13 #14 (medium); ip-address #5 #6 #8 #15 (medium); basic-ftp #7 (high); extract-zip #1 #4 (high).
- Open Dependabot PRs: #2 ip-address 10.5.0 -> 10.7.4, #4 proxy-addr 2.0.7 -> 2.0.8, #5 brace-expansion (all /stage3). The card said basic-ftp and extract-zip arrive through the PDF engine and extract-zip had no patched version on 10-13: UNMEASURED today, check.

## WHAT TO DO
1. For each of the 14: the dependency path (`npm ls <pkg>`), whether it is reachable in the running app (the code read that shows it), the fixed version, and the smallest change (take the Dependabot PR's bump, an `overrides` entry, or a parent upgrade). PRIOR-WORK CHECK first (git log -S on the lock for each package).
2. Prefer ONE PR for the round (one test pass proves it), unless a change is risky enough to stand alone (a major version, the PDF engine): say which and why. Close or supersede the Dependabot PRs only by merging their change, never by closing them unmerged without saying so.
3. A fix that cannot be made (no patched version) is a ticket with the reachability reading. **A Dependabot or CodeQL alert is FIXED, never dismissed by a seat** (dismissal is Kam's).
4. PLAN CONFIRMATION (below). Wait.
5. After Tuesday's answer: build on a branch named for the round; PR; CodeQL + tests.yml green on the PR (tests.yml was red on main for a known set before the 10-13 round: say the state now); the app's own suites green; a PDF-generation check if the PDF engine's tree changes; READY FOR QA with PRIOR WORK + NOT TESTED. Merge only on Tuesday's GO after the gate, through the PR. Check the merge does not trigger a deploy, and say what you read.

## HOLDS (standing)
- PRODUCTION: live QuickQuote (hpas-quickquote-rg) and the Vision Sales Portal (datasec-sales-portal-rg) are production. No deploy, no publish, no release image build, no Azure change. Rollback images stay in ACR untouched.
- The local unpushed merge 8b29136 in the QuickQuote checkout and any registered build worktree: do not realign, prune or delete; report their state only.
- No reply to any human. Never delete (move aside). Every factual sentence names its instrument or says "unmeasured".

## RULED BY KAM, NOT YET IN AN ARTEFACT
- quickquote-dependabot-14-round-1013 = a, "Commission it now" (2026-10-16 12:13:02, live board, view=tuesday). Record it as your next C-number with the round's BLUF.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- None new beyond the 2026-10-13 fix-round brief's holds.

PROVENANCE:
- QuickQuote main 3dd15bcc09 and the 14 alerts by number and severity | gh api repos/datasecau/vision_hpas-quickquote/... with GH_CONFIG_DIR=/Volumes/Laptop-DEV/!CODING/Datasec/Vision_Sales_Portal/4_Credentials/.gh-config | read 2026-10-16
- Kam's ruling | /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tools/kam_msgs.sh, source=live - Tuesday's tree, not yours | read 2026-10-16

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-16 12:17

## PLAN CONFIRMATION
Mail `[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation` with your seat identity (pane id, cockpit name, claude pid), launcher preflight warnings VERBATIM, the 14-row table (path, reachable?, fixed version, change), the PR split, and the tests you will run. Then wait. Your wake is Tuesday's mail plus a tap.
-- Tuesday
