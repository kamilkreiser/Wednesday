STARTABLE: YES - kit written, stamp_check exits 0 (111 of 111, drafter's run), nine Stamp slots empty. Every edit was applied to scratch copies at main and checked byte for byte; nothing compiled, tested, applied or deployed.

# B1750 drafter report (SEAT-M166, MPS settings-file fix; Kam's ruling a of 2026-11-19 18:39)
Saved by Tuesday (s293) from the Opus drafter's in-session reply. Condensed by Tuesday; the kit is the authority. Figures are
the DRAFTER's. THE KIT IS NOT READ BY TUESDAY AND NOT STAMPED.

## Files
Kit `2026-11-19_B1750_SEAT-M166_mps-infra-settings-file-fix.md` (353 lines, 61208 bytes, ASCII; the only GUIDs in it are two
synthetic ones for a local check); sidecar `.measured` 111 lines. Scratch `fleet/state/s293/d1750/`. Base: MPS main
e036c9661afab6f4339b53095afd37eb06026d5c (read 18:41:15; 0 open PRs; the repository is private).

## The shape, per scope item (seven paths, ONE commit, no ticket key: no ticket covers this)
1. **Feedback setting:** one line after the templates line in `infra/modules/showcase.bicep`:
   `MpsCalc__Feedback__Path: '/home/data/feedback/'` (value from the 13 October record `B73_STATUS.md:146` and
   `docs/API.md:885`; equal by hash to the value the 16 November seat saved; the deploy confirms the live value by hash).
2. **The two client ids: option (ii), the apply REFUSES rather than blanks.** In `main.bicep` both id parameters lose
   their empty default and must be exactly 36 characters; in the parameter file the empty fallback is removed. The ids
   are NOT written into the repository (0 occurrences in the code tree today). Cost: the two-pass first deploy of
   2026-10-10 cannot be repeated as written on a new site (the README edit says so).
   **Q1 FOR TUESDAY:** Kam's card said the fix "pins the sign-in ids"; (ii) does not pin them literally, it makes
   blanking impossible. The alternative (i) writes both ids into the parameter file: the literal reading, but it puts
   the ids on GitHub for the first time: that would go to Kam first. Default (ii).
3. **Budget start:** the `main.bicep` default becomes the fixed date '2026-10-01' (CI compiles main.bicep alone). What
   the budget service accepts on an update is UNMEASURED: the deploy what-if must show no change to startDate.
4. **The guard:** a committed names-only list `infra/env/showcase.app-setting-names.txt` (18 names, sorted) and six new
   rows in `test_infra.py` (four properties, two that prove the guard fires). 29 tests now, 35 after (static count).
   **CORRECTION to the commission:** a CI test cannot see the hosted site, so a HAND-SET setting cannot turn CI red; the
   test catches the file and the list drifting apart. Comparing the LIVE names against the list is the deploy's job.
5. **Predicted apply difference** against the 17 names of 16 November: today (main e036c966): added Templates path,
   REMOVED Feedback path. After this lane (18 names): added `MpsCalc__Templates__Path` only, removed none, changed 0 of
   the 10 shared fixed values; the 7 values built from expressions match only if the deploy supplies the same ids.
6. **Docs (developer docs, C-109):** `docs/API.md` (two missing rows in the hosted-configuration table; the feedback
   bullet at :885-886 corrected: it named a person and a seat; one paragraph saying the file replaces every setting);
   `infra/README.md` (what an apply changes; the build-params sentence; the empty-ids sentence).

## Recommended slots
Builder Sonnet row C2 (every byte frozen; a contradicting fact is a STOP); gate G1 OPUS; branch push only; Tuesday opens
the PR; head-pinned squash after 9 checks. Q2 the fixed date in main.bicep; Q3 the list in infra/env/; Q4 docs edits as
frozen; Q5 no ticket key; Q6 G1 Opus. No question needs the product owner unless Tuesday prefers Q1 (i).

## Corrections to the B1749 report
Its kit is stale (main moved to e036c966); after this lane an apply without the two ids refuses instead of blanking;
MPSCALC-225 (Done) records that deploy seats take the API id from the site's public sign-in config; the overlay setting
was also set by hand once (`B24_STATUS.md:57`) but matches the file; 2026-10-10 is the only apply on record.

## UNMEASURED
Every test result after the edits (35 passing, both validate.sh runs, all mutants); whether Bicep 0.48.1 build-params stops
on an unset variable; how the length rule compiles and whether lint warns; whether Azure refuses an empty id before writing;
what the budget service accepts on a startDate update and the live budget start; today's live settings; panes, disk,
gitleaks.

## Disclosure
During one read of an old STATUS table the drafter's tool output showed about the first 20 characters of each client id;
they are in no file and no output it produced.
