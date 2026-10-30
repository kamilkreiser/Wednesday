STARTABLE: YES (after your stamp; one caution: the edited row may stay green with the rule removed, the kit has an outcome rule for that, see Q-1)

# B950 drafter report (Sonnet 5.5, 2026-10-30 about 16:05 to 16:40 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B950_SEAT-H72_hpsmpoc-399-sidebar-spec-wait.md` (101 lines; 9 four-underscore lines = 8 slots + the last line; 0 non-ASCII). Read-only everywhere else: `gh api -X GET`, one Jira GET, no write, no cd, no test or build run. Nothing written in the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H72` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet`) adds ONE commit on `b950/hpsmpoc-399-sidebar-spec-wait` off main `37bc6323`, one path `web/e2e/shell-sidebar.spec.ts`, inside lines 320-328 only: a wait for the Customers list before the second `noSideScroll`, then the scratch-plant table (globals.css line 65 removed in `wt-b950-mut` only) with the `wider text` row as the live-plant control. Gate after: tier 2, G2.

## Facts re-measured
- main = `37bc632362c21cc8688ba70d305e88b18700d323`. Spec blob `7985e86c...`, 434 lines, sha256 `c419dd6e...`. #249's patch of the spec: 3 add / 3 del at lines 11, 370, 417: **no line moved; row still at 320, wider-text row still at 335.** The sweep pointers are right.
- Row lines 320-328; the only wait is the h1 heading (line 324). `noSideScroll` (`e2e/axe.ts` 49-69) judges `scrollWidth > clientWidth`.
- Rule: `globals.css` line 65, file 125 lines, unchanged at 37bc6323.
- **Trap found:** the Customers table is `hidden md:block` (CustomerManagement.tsx line 248, `data-scroll-x`), so at 390 it is display:none. A wait copied from row 335 (`[data-scroll-x] th button` visible) would time out at 390. Kit Step 1 / Q-2.
- Intersection: open PRs 245, 248, 250, 251, 252: shared 0. Live branches b928-b937 (except b930), b944, b945: shared 0. **b930 lists the path but is the landed #249 branch (its spec blob equals main's); the kit says so and gives the landed-vs-live test.** Controls 1 / 0.
- Ports 9810-9819: 0 listeners. Load 14.40 at 16:07. Model `claude-sonnet-5-5` (models_latest.json line 23).
- HPSMPOC-399 re-read: item B908-6 and Done-when quoted verbatim; 0 comments; control 0 hits.

## D-decisions
- D-1: the plant is a scratch worktree with a production build (the config serves `npm run start`, so a CSS edit needs a rebuild); the unchanged `wider text` row is the control that the plant bites.
- D-2: the Done-when has two outcomes; kit decides by measurement. If the edited row is still green with the rule removed, record it as intentionally weaker (comment), add no stress.
- D-3: one commit, hunks only inside base lines 320-328, program-checked.
- D-4: the spec runs in both `desktop` and `tablet` projects (config testIgnore); kit runs both and compares to base counts.

## Q-questions (default)
- Q-1: if the waited row stays green at all five widths with the rule removed, accept "recorded as intentionally weaker" (comment only) rather than stronger stress? Default YES (the ticket allows it; row 335 carries the guarantee).
- Q-2: wait element at 390? Default: branch on `size.width`; 390 waits for the first customer link/card shown, 768+ waits for `[data-scroll-x] th button`.
- Q-3: gate round? Default tier 2, round 1 of 2, class 'test-only spec row'.
- Target READY 120 / hard stop 180 minutes. Default YES.

## Reasons not to launch now
None blocking. Load was 14.4 (a production build plus Playwright is heavy: launch_when_cool). B944 (lists) will change the Customers markup; the kit warns of a possible rebase.

## UNMEASURED
Whether the row goes red with the rule removed; the wait element at 390; spec counts; build time under load.
