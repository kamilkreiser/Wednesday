STARTABLE: YES (after your stamp; one finding below changes the lane's edit list from the sweep's and does not block: three existing unit files need a one-line mock each)

# B956 drafter report (Sonnet 5.5, 2026-10-30 about 17:15 to 17:55 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B956_SEAT-H76_hpsmpoc-378-steps-6-8.md` (142 lines; 9 four-underscore lines = 8 slots + the last line, counted by a python line scan; at-sign slot pattern 0; non-ASCII lines 0; typed backslash-u escapes 0). Read-only everywhere else: `gh api -X GET` under the project `.gh-config`; Jira GET through `.tools/b649/jira.py` (`python3 -I -B`); no `cd`, no hosted HTTP, no ref written, no message. Nothing was written in the project's `1_Project_Definition/Briefs/` folder.

## BLUF
Seat `Datasec/HPSM-POC-H76` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, ports 9850-9859) restyles steps 6 to 8 and Metrics (4 screens, 2 components) on one new branch `b956/hpsmpoc-378-steps-6-8` off main `332dcc6f`, changes two lines to pass `showNext` (Narrative Previous before approval), edits the existing `web/e2e/step-previous.spec.ts` with the one browser row for `showNext` false, adds two new UNIT test files, and changes one line in each of three existing unit files. Tier-2 gate after (G2 line 109); builder row C2 line 92.

## Tickets re-read by Jira GET (scope and Done-when quoted in the kit)
HPSMPOC-378 (scope "restyle only; no behaviour change"; AC 1 to 3), HPSMPOC-402 (hand-offs 1 and 2 quoted; Done-when "Previous shows on the Narrative and Assessment steps before approval and submission, a browser row exercises showNext false, ..."), HPSMPOC-401 (read for the table Note, not this lane). 0 comments on each.

## Facts re-measured (instrument; control)
- **Main and PRs:** `commits/main` = `332dcc6f3324158cc6b2d7297aa9ef47cfd33f94`; open PRs #248, #250, #251, #252, #253; `compare e21d8044...332dcc6f` = 40 files, none of the lane's paths (grep -x -F -f; control: a planted path reads one more).
- **Intersection:** 24 paths (22 existing + 2 new) against every open PR's files and `compare/main...<b>` for all 22 `b9*` refs: **live lanes b928 to b949 and all open PRs: 0 shared.** 5 hits came only from the stale 2026-10-02 branches `b97/gate-b99-notes` (164 behind; 4 files) and `b97/internal-notes` (165 behind; `NextEngagementScreen.tsx`). Not lanes; the kit says so and does not stop on them. **`step-previous.spec.ts` is in no other branch, PR or landing** (the STOP condition for the spec holds clear).
- **Line pins:** `NarrativeScreen.tsx:165` `{approved && <NextStep from="narrative" />}` and `ApiNarrative.tsx:216` `{approvedNow && <NextStep from="narrative" />}` both correct at `332dcc6f` (the sweep's numbers survive; the files are 168 and 219 lines).
- **Ports:** `lsof -nP -iTCP:9850-9859 -sTCP:LISTEN` 0; no pane `H76`; load1 7.30 at 17:16.
- **Model:** rows L6:85 (control), C2:92, G2:109; `models_latest.json:23` `claude-sonnet-5-5`.
- **Test counts:** ApiNarrative 9 files 38 `it(`; ServiceReport 4 files; `MetricsScreen.alias` 10; `ReportScreen.order` 1; only `ServiceReport.withheld` line 61 and `ApiNarrative.provenance` line 32 contain a class word.

## Sweep pointers WRONG or incomplete (what is true)
1. **The sweep and HPSMPOC-402 omit that the ticket's own fix breaks existing tests.** Removing the `approved &&` / `approvedNow &&` guard makes `NextStep` mount in every state. (a) `ApiNarrative.staleCard.test.tsx` line 10 mocks `NextStep` ignoring `showNext`, so rows 34 and 43 (`next-step` absent for a stale card) go red. (b) `ApiNarrative.test.tsx` and `ApiNarrative.readRetry.test.tsx` render `ApiNarrative` with no `NextStep` mock and no `CustomerProvider`; `useCustomer()` throws outside a provider (`CustomerContext.tsx` line 13), so both go red. Six sibling test files already carry the stand-in. The kit makes it one line per file (D-3) and tells the seat to say so, because AC 1 says "unchanged apart from class or layout assertions". Predicted, not run.
2. **The sweep's YOURS for H17 does not name the two new unit files or the 3 test edits.** The kit does.
3. **Browser reach:** the non-live Playwright suite walks the demo customer (prototype session), so it reaches `PrototypeNarrative` only. `ApiNarrative`'s `showNext` can be pinned by unit rows only; the kit says so (NOT TESTED).
4. **The spec's own comment (lines 10 to 12)** says the draft narrative and the unsubmitted assessment are left out "on purpose"; the kit has the seat remove only the Narrative half of that sentence.

## D-decisions (mine, in the kit)
D-1 base `332dcc6f`. D-2 the spec EDIT is allowed (ticket names the file; the standing line bars only a new file); no Assessment rows. D-3 three one-line mock changes. D-4 unit rows pin `ApiNarrative`; `NarrativeScreen` unit row with a stated fallback. D-5 no word added or removed. D-6 restyle bounded by the landed frame (922 / 762 / 904 / 748 px columns). D-7 target READY 150, hard stop 240. D-8 Sonnet, tier-2 gate. D-9 width/axe/44 px proofs from an uncommitted scratch spec.

## Q-questions for Tuesday (words first; each with a default)
- **Q-W1 (words):** the design's own words for these four steps ("Template text . unapproved", "Human approval required", "Regenerate from reviewed findings", "Approve summary", "Mark report issued", "Proposed next service engagement", "Customer automation metrics") are NOT adopted; the app already has its own. Default: **adopt none; the page's strings are byte-equal** (a program proves removed 0, added 0; the changed-string table is expected empty). Say if you want any of them.
- **Q-1:** may the seat change the three existing-test mock lines (D-3)? Default **YES** (forced by the intended behaviour; precedent in six siblings). If NO, the alternative needs a `NextStep` change, which is frozen; the seat stops.
- **Q-2:** the Assessment half of -402 (rows `05-assessment-start`, `06-assessment-answered` in the same spec) belongs to H15 (B954). Default: **this lane adds no Assessment rows; tell the B954 drafter that `step-previous.spec.ts` is B956's file** (or let H15 add its rows after B956 lands, as a follow-up commit on the same file). One of the two must be said at the stamp, or the two kits collide on the spec.
- **Q-3:** gate round. Default **round 1 of 2, class "journey-steps restyle"** (as the sweep's G2 note says).
- **Q-4:** hard stop 240 and target READY 150? Default YES.
- **Q-5:** `customer/ApiSteps.tsx` (H15) defines `ApiMetrics`, which the service-path Metrics step renders; the kit forbids editing it. Default: **restyle around it; any needed change inside it is a STOP for Tuesday.**

## Stamp slots (recommended defaults)
STAMP: `STAMPED <time> AEDT 2026-10-30 by Tuesday s207`, brief read whole with this report, D-1 to D-8 accepted, Q-W1 adopt none, Q-1 YES, Q-2 as chosen, Q-3 round 1 of 2. KEYS: HPSMPOC-378, HPSMPOC-402 hand-offs 1 (Narrative) and 2. LAUNCH WINDOW: until the evening, launch_when_cool load1 below 7. Stamped by: Tuesday s207. Launch authority: the 10:07:23 commission and the standing grants (as the B944 stamp). Hard stop and target READY: 240 / 150. Head and main at launch: `332dcc6f...`, no `b956*` ref, open PRs as read. Model receipt line: the one in the guidance paragraph.

## Reasons the seat should not launch now
None blocking. Load is the only reason (7.3 to 20 today); the kit is written not to depend on launch time (launch_when_cool). Tuesday must answer Q-2 before B954 launches, or both kits edit `step-previous.spec.ts`.

## UNMEASURED
Suite counts; Chromium; the four screens' appearance on the landed frame; axe; whether `NarrativeScreen` renders in a unit harness (D-4 gives a fallback); `ReportScreen.tsx` lines 1-150, `ServiceReport.tsx` lines 1-60 and `ApiNarrative.tsx` lines 60-120 not read; the other e2e specs only by grep.

## Outside-the-fences disclosure
No fence breached. Scratch only in `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/8a8e5624-4358-43cb-ab64-af03ddbc5b41/scratchpad/drafters/b956/` (a tarball of `332dcc6f`, path lists, Jira output). No file written in the project's Briefs folder.
