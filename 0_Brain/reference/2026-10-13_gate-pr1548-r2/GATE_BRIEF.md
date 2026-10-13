# Gate brief: pull request 1548 (KS-1598) fix round 1, DELTA, Opus, through-code weight

Commissioned by the Wednesday seat. 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- Head 03bdfc3205e13e4d610ebd1163ab1273ba03d151 (Wednesday's own ls-remote of refs/pull/1548/head = the author's). One commit on the round-1 gated head 9d974c4b516cc665a6c5d3b26b06eae22c09a9b3; two files. develop = 92d1316ffe31cb13b3f7e843e7891225383b2f84 (Wednesday's ls-remote).
- Round-1 verdict: 0_Brain/reference/2026-10-13_gate-pr1548/verdict.md (GO WITH NOTE, m1 the U+0130 fold, i1-i6; hash 20fb01665917ef45). Its cells and tools are in evidence.tgz beside it (cell H, X4/X5 mutants, gate1548-g-status).
- Author's claims (NOT evidence): m1 `lower(status COLLATE "C") = 'active'` at the one site; U+0130 cells -> 404, the ASCII 'ACTIVE' control -> 200. A 27-cell vocabulary spectrum whose list is checked against pg_get_constraintdef('users_status_vocabulary'). X4 killed (17 red). Text i1/i3/i4 corrected. i6 filed as KS-1601. KS-1554 commented: nothing type-checks services/security tests, so the author's "tsc clean" claim was vacuous for the test tree; it built a program that does. KS-1602 filed (a hook-timeout skip in ks742 under load).

## Gate
1. Diff 9d974c4b..03bdfc32 by hunk; nothing outside the two files; classify behaviour vs test vs comment.
2. Re-run your round-1 cell H and X5 on the new head: the U+0130 spellings -> 404 with no row, ASCII spellings unchanged. Check whether ANY other non-ASCII fold (other Unicode case mappings the libc collation folds to 'active', e.g. fullwidth or Kelvin-sign style mappings, any that lower() maps into the ASCII range) still passes the guard under COLLATE "C"; enumerate, do not sample.
3. The spectrum: does the pg_get_constraintdef cell really fail if the vocabulary changes (plant one)? Are all 27 cells reaching the route (a real assertion message on every red)?
4. Type-check the changed test file yourself with a program that includes it (the author says the repo's tsconfig excludes tests), with a planted error as the control.
5. Re-run the author's 7 mutants (reject empty-message kills), plus X4, X5 and two of your own; include a comment-only control.
6. Merge prediction on the LIVE develop tip (re-read it yourself): overlap with a planted control, merge-tree with a conflicting negative control.

## Rules
Read-only on the project: clone --shared into YOUR scratchpad and fetch there. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; never delete; never rm inside bash -c. Your own Postgres on a free port (lsof first); avoid 55413, 55414, 55418, 55419, 55436, 55440, 55463, 55471, 55477, 55549. Write only here and in your scratchpad (raw outputs under evidence/, never a directory named out); npm/tar outputs to explicit absolute paths in your scratchpad.

## Output
0_Brain/reference/2026-10-13_gate-pr1548-r2/verdict.md: VERDICT on line 1, sha256/16 of the report on LINE 2 (delete line 2, sha256 the rest, first 16 hex), FOUND / TESTED / HOW, NOT tested, severities with file:line. Round 2 of 2 under the cap. Merge only on Wednesday's head-bound GO; nothing deploys.
