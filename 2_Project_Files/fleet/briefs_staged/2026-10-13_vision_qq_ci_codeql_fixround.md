# BLUF — Datasec/Vision_Sales_Portal: QUICKQUOTE QUALITY FIX ROUND. Kam ruled card quickquote-ci-red-codeql-14-1013 = (a) "Commission a fix round now" (live board, 2026-10-13 09:46:52 AEDT, view=tuesday). Triage the failing tests.yml suite on QuickQuote main and the 14 open code-scanning alerts, fix what is real, ticket the rest, through a QA gate, merged to QuickQuote main through CodeQL on Tuesday's GO. NOTHING is published or deployed: publishing is Kam's card, every time. Send a PLAN CONFIRMATION first; build nothing before Tuesday answers.

**Scope, read narrowly.** This round is QuickQuote quality only (tests + code-scanning alerts on datasecau/vision_hpas-quickquote). The portal, ATTIO and the rest of the Vision backlog stay paused (2026-09-29).

## READ FIRST (all in the Vision_Sales_Portal folder)
1. `CLAUDE.md` WHOLE, especially the QuickQuote section and the production boundaries.
2. Your newest `5_Project_History/history.md` entry (yesterday's v2.34 round: PR #3, merge 108bbb4, deployed v0.6.2-tool2.34-108bbb4) and `1_Project_Definition/CLARIFICATIONS.md` (C-13, C-16).
3. The QuickQuote repo's `.github/workflows/tests.yml` and the last failing run's log.

## MEASURED BY TUESDAY (2026-10-13 06:0x AEDT, read-only, Vision's GH_CONFIG_DIR)
- tests.yml on main FAILS: run 38216888489 on 108bbb4 (2026-10-12T07:17:10Z); also failure on e408904 (36334735633) and 986f7b8 (36282811446), 2026-09-27. Yesterday's merge report named "the same known 9" failing tests (relayed from the v2.34 seat's MERGED, not re-derived here).
- Code scanning on datasecau/vision_hpas-quickquote: 14 open alerts (gh api code-scanning/alerts?state=open: 9 high, 5 medium).

## WHAT TO DO
1. TESTS: list every failing test on main with its failure line. For each: a real product defect, a test that is wrong or stale, or an environment difference (say which, with the instrument). PRIOR-WORK CHECK first: why each failing test was written (git log -S / blame) and when it went red.
2. ALERTS: list all 14 (number, rule, severity, file:line). For each: a real issue (fix), a false positive (say why, with the code read), or out of scope. **A CodeQL alert is FIXED in the code, never dismissed by a seat** (Datasec org policy; dismissal is Kam's call, so a false positive becomes a card for Kam, not a dismissal).
3. Propose the build: what you fix this round, what you ticket, the tier per change (anything touching auth, quoting arithmetic or the feedback endpoint is tier 1), red-first cells, and whether any change alters what a user sees (if it does, screenshots go to Kam).
4. Plan confirmation (below). Wait.
5. After Tuesday's answer: build on a branch named for the round; PR; CodeQL + tests.yml green on the PR; READY FOR QA with PRIOR WORK + NOT TESTED. Merge to QuickQuote main only on Tuesday's GO after the gate, through the PR (the org ruleset requires CodeQL on a PR). Check the merge does not trigger a deploy (ACR tasks / webapp source), and say what you read.

## HOLDS (standing)
- PRODUCTION: the live QuickQuote (hpas-quickquote-rg) and the Vision Sales Portal (datasec-sales-portal-rg) are production. No deploy, no publish, no image build for release, no Azure change. Rollback image v0.6.1-tool2.33-986f7b8 stays in ACR untouched.
- The local unpushed merge 8b29136 in the QuickQuote checkout and the registered v2.34 build worktree: do not realign, prune or delete either; report their state only.
- No reply to any human. Never delete (move aside). Every factual sentence names its instrument or says "unmeasured". QuickQuote's own style tokens only.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-10-13 09:46:52, card quickquote-ci-red-codeql-14-1013 = a, verbatim above. Write it into CLARIFICATIONS.md and mail back the C-number.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- The 2026-09-29 pause stands for everything outside QuickQuote feedback (C-13) and this round.

PROVENANCE:
- Kam's ruling | live board via /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_msgs.sh (09:46:52 row) | read 2026-10-13
- tests.yml runs and alert counts | gh run list / gh api code-scanning on datasecau/vision_hpas-quickquote | read 2026-10-13
- v2.34 state (108bbb4, image tags, 8b29136) | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md DELTA 176 | read 2026-10-13

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-13 09:49

## PLAN CONFIRMATION
Mail `[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation` with your seat identity (pane id, cockpit name, claude pid), what you read, the full test and alert tables with your proposal per row, and any launcher preflight warnings VERBATIM. Then wait. Your wake is Tuesday's mail plus a tap.
-- Tuesday
