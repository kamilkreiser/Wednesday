STARTABLE: YES (after your stamp; launch via launch_when_cool, the machine is full; one product-owner item below does not block)

# B954 drafter report (Sonnet 5.5, 2026-10-30 about 17:00 to 17:40 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B954_SEAT-H74_hpsmpoc-375-steps-1-2.md` (143 lines; 9 four-underscore lines = 8 slots + the last line, by `grep -c -E '_''_''_''_'` and a python scan; at-sign slot pattern 0; non-ASCII 0 after one repair, see Disclosure). Read-only everywhere else: gh `-X GET` under the project `.gh-config`, Jira GET through `.tools/b649/jira.py` (python3 -I -B), a tarball of `332dcc6f` in scratch, no `cd`, no ref, no write to the project, no message.

## BLUF
Seat `Datasec/HPSM-POC-H74` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, rows C2 line 92 and G2 line 109, both re-read) restyles Profile, Assessment, QuestionBlock, ApiSteps and the snapshot files onto the shared bar and card, and mounts ONE `NextStep from="assessment" showNext={locked}` after the submit bar so "Previous: Profile" shows before submission. Branch `b954/hpsmpoc-375-steps-1-2` off `332dcc6f`, ports 9830-9839, stop at READY FOR QA, tier-2 gate after.

## Tickets re-read by Jira GET (0 comments each)
HPSMPOC-375: scope "restyle only, using the shared components. No behaviour, route or data change."; it has no Done-when line, so the kit quotes its three acceptance criteria. HPSMPOC-402: hand-off 1 Assessment part and the whole Done-when are quoted; the kit states that only "Previous shows on the Assessment step before submission" is this lane's.

## Facts measured (instrument; control)
- Main `332dcc6f` (`commits/main`); open PRs #248, #250, #251, #252, #253: shared with the 20 lane paths 0 each (`grep -c -x -F -f`; control: a list with `AssessmentScreen.tsx` reads 1). `compare e21d8044...332dcc6f` (40 files): 0 shared. 26 live `b9*` refs: 0 shared on 24; **2 stale branches share a file** (`b92/invisible-chars` -> `QuestionCard.tsx`, `b97/internal-notes` -> `SnapshotResult.tsx` and its test): both have MERGED PRs (#77, #81), merge bases from 30 Sep / 1 Oct, 165-169 behind main: not live. The kit says report, do not stop.
- Sibling lanes H16 (11 files), H17 (22), H18 (23), expanded from the sweep by program against the tarball: 0 shared with H15.
- `AssessmentScreen.tsx:127` is `<NextStep from="assessment" />` (confirmed) but it sits ONLY in the locked branch; unlocked there is no step navigation. `ApiSteps.tsx:179` (API path) already shows both links. `previousStep("assessment")` = Profile. `NextStep` is not changed: `showNext={false}` gives Previous only.
- Siblings tests: the five screens have NO unit test of their own; the lane's 8 snapshot tests hold 45 `it` rows. Outside tests that render them: `CustomerHeading.alias`, `ApiProfile`, `LoadFailed.states`, `EngagementOverview`, `draft-density`, plus `industries.test.tsx` (source scan: keep `useCustomerEyebrow(`).
- Model: `models_latest.json` line 23 `claude-sonnet-5-5`; model-routing rows L6:85, C2:92, G2:109, G-cap:111; `brief_seat.sh:24` defaults to opus.
- Pane H74 not taken (live: H59, H63, H66, H68, H69, H70, H71, H73, G219, G222, G223); ports 9830-9839 `lsof` 0; `matching-refs/heads/b954` 0; load 8.76 10.27 10.74 at 17:15.

## Product-owner item (not changed by this lane)
The #245 gate's finding is real and measured: `shell/CustomerShell.tsx` lines 81-89 (`questionsChip`) counts EVERY applicable question ("n of m questions answered", the "1 of 3"), while `AssessmentScreen.tsx` line 98 counts SCORED applicable questions only ("n of m scored questions answered", the "0 of 2"). One screen, two counts. Needs a product-owner choice (one count, or the words made to say why they differ). Recorded in the kit's FOR TUESDAY item 1.

## D-decisions (in the kit)
D-2 one NextStep always mounted, `showNext={locked}`, after the submit bar (new Tab stop last). D-3 ApiAssessments/ApiProfile untouched. D-4 shared bar UNLABELLED (a label adds a new accessible name). D-5 chip untouched. D-6 the committed browser row belongs to H17's `step-previous.spec.ts`. D-7 `useSnapshot.ts` and pages byte-equal by default (imported outside the lane). D-9 no new spec. D-10 READY 150 / hard stop 240.

## Q-questions for Tuesday (each with a default)
- Q-1 (WORDS): any new word? Default NONE; the Previous label comes from `NextStep`; the design's words ("N of 16 answered", "Draft content", "Skip for now") are not adopted. Builder prints an expected-empty changed-string table.
- Q-2: progress bars unlabelled and `Card` swaps (with `as="div"`) allowed where the box is identical? Default YES to both.
- Q-3: who adds the committed browser row for showNext false? Default: put `"05-assessment-start": "Previous: Profile"` (and the 06 row) into B956's (H17) kit, since the file is H17's; H15 proves it in a scratch spec only. If B956 is already stamped, Tuesday adds it after both land.
- Q-4: the doubled rule (NextStep's `border-t` under the submit bar's). Default: builder drops the submit bar's own `border-t pt-6` only if the screenshots show a doubled line.
- Q-5: gate round. Default round 1 of 2, class "steps 1-2 restyle".
- Q-6: hard stop. Default READY 150, stop 240.

## Stamp slots, recommended defaults
STAMP: accept D-1..D-10, Q-1..Q-6 as above. KEYS: HPSMPOC-375, HPSMPOC-402 hand-off 1 (Assessment part). LAUNCH WINDOW: until about 19:30 via launch_when_cool at load1 below 7. Authority: the usual grants. Head: `332dcc6f`, no `b954*` ref.

## Reasons not to launch now
Machine load (8-10 with 12 seats). Launching after B956 is drafted/stamped is cleaner for Q-3 but not required. No file coupling with any open PR.

## UNMEASURED
Suite counts; rendering at any width; axe; the Feedback pill over the new link at 390 px; `Card as="div"` against the snapshot tests.

## Disclosure
One non-ASCII character (a middle dot in a quoted suffix) slipped into the first write; found by a python scan and replaced by words. Final: 0 non-ASCII. No file was written in the project's Briefs folder. Scratch only under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/8a8e5624-4358-43cb-ab64-af03ddbc5b41/scratchpad/drafters/b954/`.
