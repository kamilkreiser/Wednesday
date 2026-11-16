STARTABLE: YES (kit 78 lines, sidecar 75 of 75 measured, stamp_check rc 0; the dialog is NOT wider than 390 px at main, so the ticket's STOP case does not fire)
# B1642 DRAFTER REPORT: SEAT-M153, MPS lane M-E2 (MPSCALC-409)

## BLUF
Kit `tuesday/briefs/2026-11-16_B1642_SEAT-M153_mps-lane-me2-dialog-box-390.md` (78 lines) plus sidecar `.measured`. It appends two tests to `web/e2e/dashboard-390.spec.ts` (owned path: that one file; siblings M-F and M-S2 own `FleetLineIdTests.cs` and `web/src/api/stub/{purchaseQuotes.ts,stubApi.test.ts}`: disjoint). **Measured finding that shapes the kit:** the dialog is the `aside.drawer` (`Drawer.tsx:11`) inside a fixed backdrop with `justify-content: flex-end` (`styles.css:123`, box rule `:124`). At 390 px it reads left 0, right 390 (not wider). But a dialog widened with inline `min-width: 600px` reads left -210, right 390: the widening runs off the LEFT edge, so the ticket's "right edge no further than clientWidth" would stay GREEN on a dialog 210 px too wide. The kit therefore checks both edges (Q1) and plants `min-width`. Page `scrollWidth` stayed 390 in every plant, confirming the ticket's stated limit.

## Facts re-measured (instruments in the sidecar)
- Main 56bfe232cbf4c98a9752f949f1f279d755565750 (gh GET ref, 21:54); open PRs 0; `b1642` refs 0 (control `b1623` 1).
- Spec at main: 55 lines, 3 `test(` lines, 5 tests at run time; form row `:36`, control `:44`, `openHome` `:12`. (A first read of 5 `test(` lines was taken on my own reference copy in the tree; caught and corrected in kit and sidecar.)
- Reference spec (87 lines, in `fleet/state/s284/b1642/ref/`): 7 passed on unmodified main (stub mode, port 9971); eslint rc 0; `pdftotextTimeout` scanner 14 passed; 0 non-ASCII lines.
- Mutants on scratch copy: mE1 `.drawer` + `min-width: 600px` -> new row RED `dialog left -210 right 390 vs clientWidth 390`, control GREEN, 6 passed 1 failed; mE2 control `minWidth` 390px -> control RED, 6 passed 1 failed; both undone (`cmp` equal / file recopied).
- `playwright --list`: stub 275 tests/19 files -> 277 with the rows; api-off 157/8 both ways.
- Port block 9970-9979: 0 listeners before and after every run; load about 7.9; Node v24.21.0 from HPSM-POC `.tools/node24/bin`; ticket 409 has 0 comments, status Backlog; held/dropped check: pickup file 0 hits, daily note line 134 is a creation mention only.

## Inputs table (rule 4)
Every step reads only things at BASE or made by an earlier step: Step 1 clone and baseline (base); Step 2 predictions (Step 1 output); Step 3 edits the existing file (base) and writes two tests; Step 4 mutants need the Step 3 file and `styles.css:124` (base); Step 5 checks need Steps 3-4 and the base ref; Step 6 commit needs 5; Step 7 push needs 6. No step needs a file a later step makes.

## D-decisions
- D1 Two tests appended below `:55`, no existing line touched (the ticket's "existing five rows unchanged"; the check is `git diff -U0` removed lines 0).
- D2 The control plants inline `min-width: 600px`, because it is the plant the right-edge-only reading misses.
- D3 Row sized S, one commit, no part B/C, no package, no config edit.
- D4 Launch name `Datasec/MPS-M153`, port 9971 (block 9970-9979 all free).

## Questions for Tuesday (each with a default)
- Q1 Check BOTH edges (left >= 0 and right <= clientWidth) rather than the ticket's right edge only? Default YES (measured reason above; it stays inside the ticket's words "the dialog's own box").
- Q2 Append the two rows and leave the form row at `:36` as it is? Default YES.

## UNMEASURED
Whole vitest/eslint/tsc and both whole browser steps at a seat's head; the CodeQL pre-scan for this repo; hosted CI; the interaction with M-S2's stub edits (M-S2 not yet written; the kit says Tuesday re-runs on merged main); the entra build (not in scope).

## Outside-the-fences disclosure
Read-only or scratch only: `gh api -X GET` (ref, tarball) under the project GH_CONFIG_DIR; Jira GET via `jdesc.py` copied from the SWEEP-2150 scratch (not a seat's `.tools`); read B1623's kit, sidecar and STATUS; a scratch tarball with `npm ci --offline --ignore-scripts` and loopback Playwright runs on port 9971 under `fleet/state/s284/b1642/` (no project repo write, no ref write, no hosted host); `lsof`, `tmux list-panes`, `uptime`, `df`. No `cd`, push, PR, Jira write, mail, board, az, deploy; `decision_queue.sh` not run.

DRAFTED B1642: kit 78 lines, sidecar rc 0, questions 2
