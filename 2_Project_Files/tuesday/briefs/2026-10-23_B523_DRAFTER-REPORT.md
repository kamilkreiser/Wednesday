# B523 drafter report (G56 gate kit, HPSM-POC PR #196), 2026-10-23 12:08-12:20 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B523_SEAT-G56_hpsmpoc-b510-gate-tier2.md` (73 lines), byte-identical `.pre-stamp` beside it (`cmp` ok).

## Open slots
- Four-underscore lines in the kit: **9** = 8 Stamp slot lines (lines 29-36: STAMP, LAUNCH WINDOW, Stamped by, Launch authority, Hard stop, Head/main/check-runs, Round rule, Model receipt) + the last line `READ-WHOLE-BY-TUESDAY: ____` (line 73). Measured with `/usr/bin/grep -c -E '_''_''_''_'` = 9 (control: the same grep on the B506 template reads 0, it being stamped). The Stamp section states "The unstamped copy reads 9 lines".
- `@[A-Z_]+@` count 0; non-ASCII bytes 0 (one middle-dot pair in the quoted findings was replaced with `|`); no person name, no decision-card id (grep controls run on the kit); I deliberately did not quote the ci.yml/audit-dev.mjs comment lines that hold a name and a card id.

## What I read
Whole: B506 kit (template), B507 kit (round-2 conventions), the builder's B510 STATUS, the B510 brief. Partially: B479 STATUS lines 170-190 (finding B479-1 quoted from `:174`), B491 STATUS line 247 (B491-13). Through GitHub: PR 196 metadata, compare, commits, check-runs, code-scanning, `ci.yml` greps, the full patches of `e2e.mjs`, `ci.yml`, `audit-dev.mjs` and the test file.

## Facts and sources (all measured about 12:10 AEDT, read-only)
- PR #196 open, head `b510/hpsmpoc-479-1-runner-env` = `5a0fc03b19dec74106ccd5a1e66dc0c2cb7814db` = `refs/pull/196/head` (`ls-remote`); base main `4db192b025732a35e6070a7d235ba93f26b8e23a`; ahead 2 behind 0; 4 files, +206 -9; `mergeable` true, `mergeable_state` blocked (`gh api pulls/196`). Merge ref `24c88141c7ff55092d190a7fab11a51f9ba580d0`.
- Per-file numstat: `e2e.mjs` 50/6 (hunks 3, 41, 6), test 154/1, `ci.yml` 1/1, `audit-dev.mjs` 1/1 (`compare`). Both commits carry the `Co-Authored-By: Claude Sonnet 5.5` trailer (`commits/<sha>` message tails); one parent each.
- 13 new rows counted from the test patch (1 + 2 via `it.each` + 1 + 1 + 1 + 3 source-text + 4 CLI); the one removed test line is the import-list line; a `node:child_process` import is added.
- Check-runs at 12:10: 13 listed, 4 completed (CodeQL neutral; dependency review, gitleaks, Analyze (actions) success), 9 in progress; `web e2e` legs and `web (Next.js)` not yet present. Alerts on `refs/pull/196/head` open = 0 and unfiltered = 0 (so no row-returning control exists on this ref; the kit names alert 12 of PR 193 and main as controls). Analyses so far: python 0, actions 0. Main open alerts 0. Required contexts of main: five, listed in the kit.
- `ci.yml` at the head: `pull_request:` line 17, job `web unit tests (vitest)` line 450, job `web (Next.js)` line 526; no `TZ` hit in my grep (the grep was case-sensitive with a `TZ` alternative; the gate must re-grep with a positive control, which the kit says).
- Open PRs: #196 only. Panes: tuesday, fleet-monitor, HPSM-POC-H1/H2/H3/F3, MPS-M1, Security-Composer-J4; no G56. `.tools/b510*` exist (builder's, not the gate's); no `b523` paths; no `refs/heads/b52*` on origin.
- Port block **8670-8679**: `lsof` over 8600-8699 empty (rc 1); briefs' allocations: B510 8560-8569, B512-B516 8600-8619, B517-B522 within 8620-8669; word-bound grep for `867x` over all briefs matched 0 files. The positive control (a scratch line holding 8670) was not run; the kit asks the gate to bind one.
- load1 10.53 / 9.95 / 8.39 at 12:10 (kit warns the gate to wait).
- Builder claims (RELAYED, from its STATUS): 188/2271 -> 188/2284, rows 79 -> 92, audit-dev 11, 14 of 14 mutants, M6a/M6b killed only by the source-text order row.

## Where the template did not fit (and what I did)
- The task named `2026-10-22_B491_STATUS.md`; only `2026-10-23_B491_STATUS.md` exists. The kit cites the real name and says so.
- The template's escalation list stops on any `.github/**` byte; here `ci.yml` is in scope (comment-only), so the kit scopes the stop to non-comment bytes and other `.github/**` files.
- No TZ matrix, no BD-style 10 cells: replaced with two pools; the template's "test-only, no product byte" framing became "runner script + test + two comment edits" with product-side mutants N1-N15 (plus controls c0-c3, c2b, cw-weak).
- B506's lead on the child process environment does not apply (the CLI rows pass an explicit env); replaced by an outer-environment check (Check 4c).
- The kit's CodeQL control differs from the template (nothing to return on the PR ref).
- Added leads specific to this PR: hard-coded ports 8560/8561/8563 in the rows (builder's block, now free), `.next` presence changing `hasBuild`, text-satisfying behaviour mutants (N12, N13), the names the web reads beyond the pair, `startApi` inheritance, and a hard rule never to run the order check without `--no-such-flag`.

## UNMEASURED
No npm, vitest, node, fetch, worktree or mutant was run. Not measured: that the 13 rows are green anywhere (builder claim only), the exact row names as the JSON reporter prints them, whether `web/.next` appears after `typegen`, the exact row-kill claims for N-mutants, whether the H-seat briefs touch the four paths (their briefs name those files only as another lane's or as not theirs, by a 5-line grep, not a full read), the B507 STATUS (cited by the builder, not read by me), the HPSMPOC-328 ticket (relayed by the builder), CI on the merge ref, B510 STATUS line numbers inside the B479 STATUS beyond what I quoted. The 13-row split by `it.each` was counted from the patch, not from a run.
