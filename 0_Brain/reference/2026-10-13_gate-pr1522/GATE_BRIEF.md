# Gate brief: Secuura Platform K PR #1522 (KS-1512 option A), SONNET tier 2, through code + local runtime

Commissioned 2026-10-13 ~05:2x AEDT by the Wednesday seat.

## What you are gating
- PR #1522, ticket KS-1512 option A, author Seat K 7th (Secuura/Blockchain-K). Two commits on one branch: 499f11964fc0 (a windowed read of the platform half of the audit-log page) and 119d362050666949e8b564dd3c175b5661f237a5 (an OVERALL deadline for the whole paging).
- Head `119d362050666949e8b564dd3c175b5661f237a5` and develop `425ad3e00ae40ddbce6ead62c127c610e2e67a16`, both read by Wednesday with `git ls-remote` at commission. K reports: 2 files, +344 -10, api-gateway only.
- Wednesday's ruling the amendment implements: the budget is the EXISTING per-call timeout (PLATFORM_UPSTREAM_TIMEOUT_MS, default 8000 ms) reused for the WHOLE paging; when it is spent, the platform half is DISCARDED exactly as a failed window is; each window's timeout = min(8000, budget remaining); no window starts once nothing is left; no new number or cap.
- K's own claims (NOT evidence; re-measure what matters): red-first 3 of 18 red (H, L, M); 12 mutants + a no-mutation control all exact; landing tree 2703f08c1ad0 (cherry-pick onto 425ad3e0) 118 files / 1146 tests 0 failed; ESLint, tsc, check:test-types clean; push hook 13/16 legs ran, 3 skipped, none failed.

## How to get the code (READ-ONLY on the project)
- The project checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ-ONLY: no git write verb there. `git clone --shared` it into YOUR scratchpad and fetch `refs/pull/1522/head` and `develop` in that clone using the project's `core.sshCommand` (read it with `git -C <checkout> config --get core.sshCommand`, and the URL with `config --get remote.origin.url`). Assert the head sha first.
- No pushes, no GitHub/Linear writes, no contact with any server or box, no real secrets in output.

## What to check
1. The ruling, item by item, against the diff: one budget = the existing timeout; the per-window min(); no window after the budget is spent; a spent budget discards the platform half (never keeps a partial page); a single-window page behaves exactly as the old route did.
2. What the caller sees on a degrade (HTTP status, rows, total): confirm K's statement that it is identical to today's failed-window behaviour and that nothing else (headers, totals, ordering, offset maths) changed for the non-degraded path.
3. The real-time cells (K's warning: real timers, 400 ms margins). Run the new test file at least 5 times and the gateway suite twice; report any flake with timings. Say whether the margins are adequate or a fake-timer form is needed.
4. Run the landing tree (head merged/cherry-picked onto develop 425ad3e0 in your clone): gateway suite, lint, tsc, check:test-types. Compare counts with develop.
5. Mutants: kill at least the four budget mutants K names (per-window timeout not cut; no budget; half budget; keep partial rows) yourself and confirm the cells that redden.
6. K's residual: a stalled response BODY in the last window is outside the per-call timer (fetchWithTimeout clears at headers). Confirm or refute by reading fetchWithTimeout; say whether this PR made it worse, the same, or better.
7. Anything else in the diff: error handling, the env read at module load, logging of tokens or tenant data.

## Output
- Write `0_Brain/reference/2026-10-13_gate-pr1522/verdict.md` (this folder only, plus your scratchpad).
- Head under test and how obtained; every number with its instrument and a control; FOUND / TESTED / HOW; what was NOT tested.
- VERDICT: GO / GO WITH NOTE / NO GO, Majors and Minors with file:line, the reproducing shape and the minimal fix.
