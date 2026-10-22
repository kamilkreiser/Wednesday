# B507 DRAFTER REPORT (read-only drafter for Tuesday), 2026-10-23 10:10-10:20 AEDT

Brief written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B507_SEAT-G55_hpsmpoc-b502-round2-gate-tier2.md` (86 lines). Tier 2 (Sonnet), round 2 of 2 (the cap), pane `Datasec/HPSM-POC-G55`, ports 8550-8559.

## Measured by the drafter (GET / read-only only)
- Head: `ls-remote` b461 = `refs/pull/193/head` = `01cb77c646c5575603922cfc2a9d40eed5d4460f`; PR open, 5 commits, 14 files, `mergeable` true, state `clean`.
- Delta `a3a4679...01cb77c6`: ahead 1, behind 0, files exactly `web/scripts/e2e.mjs` (+30 -4) and `web/src/e2e-runner.test.ts` (+138 -5) = 168 / 9, matching the builder. One parent `a3a4679`. Message has the trailer; it does not name alert 12 or the PR (the brief says not to demand it).
- Delta patch of `e2e.mjs` read: new exports `markerStep` and `markSeed`; `liveApiRun` calls them; `recordMarker` body untouched. The test-file patch was NOT read (numstat only), flagged in the brief.
- Alert 12 instance `fixed` (commit 53052201), open on PR ref 0, without `state=open` 1 (control), four analyses at `01cb77c6` with 0 results. Main-ref open alerts NOT read (the brief says so).
- Check-runs at 10:10: 20 of 20 completed success.
- Main MOVED since round 1: `ee26d9fc` to `7c9f66c2` (the other lane's PR 194 merged); the merge ref was regenerated (`67bb2270`). The brief makes the gate read its parents and which merge ref CI used.
- Ports: 8550-8599 free; 8530-8533 and 8537 are other seats' (G53); allocations B501..B506 = 8490-8549 so 8550-8559 is free. Panes: no G55; G53, T1, F1 live. `b507*` refs and trees absent (control 7 / b198 present).

## What the brief adds over B504
- THE CAP RULE at the top and a mandatory `SHIP / TICKET` section: per finding B504-1..6 `CLOSED (ships)` or `REMAINS (ticket ...)`; NO GO does not open round 3; a third commit is a refuse.
- Check 2: per-finding CLOSED / NOT CLOSED criteria with the named mutants (W1 W3 W5 / G4 / G9 / G8 x3 / umask matrix / real-CLI exit 2). Check 3: the battery re-run with the full round-1 survivor list (W1, W3, W5, G4, G9, G8 x3, G7a, X3, X5, G1-u077, U, G3), c0 under 000/002/020/022/027/077, the round-1 property mutants as regression, and the red-proof P0 against the a3a4679 code. Check 4: round-1 passing properties (MP1-MP4, refusals, 0600/0700 under umask 000, no tmpdir fallback, purpose cross-process, override wins). Checks 5-8: suites (2118 -> 2127, 70 -> 79, lost 0 added 9), CodeQL/checks/merge/overlap, interaction, process.
- B504 conventions kept: Step 0 / 0b with the split-pattern slot count (verified: 10 lines unstamped, control fires), at-sign count 0, non-ASCII 0, STATUS-only channel, findings only, own clone and worktrees, two locks, load rule, fixed apiq.sh, controls that can fail, alert instance state, CI complete before a GO, no person's name, no card id, the other nine stamp slots, last line `READ-WHOLE-BY-TUESDAY: ____`. B504's tree and scripts are marked "not yours".

## Drafter leads placed in the brief (to MEASURE, not findings)
(i) G7a / W1b / G7b are killed only by the source-text row and `liveApiRun` itself is undriven; (ii) the atomic row is an inode row, so own mutant G4b (unlink then in-place write) may stay green; (iii) own mutant G8d (clock-derived six-character suffix) x3; (iv) empty-string override message in `markSeed`; (v) falsy identity writes nothing; (vi) line-by-line comparison of the four replaced source-text assertions plus a whitespace control c2b; (vii) program scan of every fixture write for a missing mode; (viii) scratch leftovers; (ix) which merge ref the 20 check-runs ran on.

## Judgement calls to check
- I defined "killed = red on a named row" (a source-text kill counts and is reported as one), so G7a / W1b / G7b do not hold B504-1 open by themselves; W1, W3, W5 must be red on an executing row. Tuesday may tighten this.
- B504-5 is a Minor that makes the finding NOT CLOSED but is never a NO GO alone (the addendum promoted it, the severity list keeps it Minor).
- The three slot-line labels beyond STAMP / LAUNCH WINDOW follow B504's list exactly (nine slot lines plus the last line = 10).

## Fences kept
Only the two files written. No git write verbs, no worktree, no fetch, no HTTP to any app host; `gh` GET only under the project's `GH_CONFIG_DIR` (project account verified, handle not quoted). No `decision_queue.sh`. One `cd` attempt was refused by the hook and re-issued without it. No person's name or card id in the brief (verified by grep: the only hits are the rule text "decision_queue.sh" and "no decision-card id").
