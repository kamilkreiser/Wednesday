# Gate brief: pull request 1548 (KS-1598, the follow-up set from the pull request 1539 gate), Opus, THROUGH-CODE weight (an authorisation guard is touched, so Opus; no runtime stack)

Commissioned by the Wednesday seat. 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

## What you are gating
- Head 9d974c4b516cc665a6c5d3b26b06eae22c09a9b3 (Wednesday's own ls-remote of refs/pull/1548/head = the author's), base develop 026c2d1614065c79fc8d96007ac0d80f19fb9363 (author). develop has since MOVED: Wednesday's ls-remote just now read d53d80cbb2d50a5525c3d881a2da7a31eba67fb5 (expected to be pull request 1546's squash, unconfirmed). Four files under Blockchain/Dev/services/security: src/index.ts, and three test files (ks1570b-concurrent-replace-is-not-a-union.integration.test.ts, ks888-failed-mint-save-issues-no-key.test.ts, ks1570b-admin-scope-route.integration.test.ts). +176/-7.
- The source verdict: 0_Brain/reference/2026-10-13_gate-pr1539-r2/verdict.md (read its m1, m2, n1-n5 and the F1/F10 cases).
- Author's claims (NOT evidence): m1 the ONE real defect: index.ts status guard `status = 'active'` -> `lower(status) = 'active'` (migration 046 folds case at :34/:41/:47); ACTIVE/Active 404 -> 200; control 'DELETED' stays 404. Sweep of the route: m1 the only unfolded comparison (eight sites argued in the body). m2: audit-chain whole-array + per-link assertion; E3 two concurrent mixed-case writers with a waiter seen. n1 two doubled semicolons. n2 six INFRA fixture cells for 53300/57P01, green on arrival, COVERAGE only (the classifier at :1136 already matches by SQLSTATE class). n3 documented. n4 message rename. bd11c34e carried as labelled defence in depth (hashtext(lower(...)) at the lock); its false comment rewritten. Mutants R2, R3, R10, R11, m1r killed; R4 killed ONLY by E2's source-text assertion, behaviourally equivalent (E3 green under it). Security unit 31 files/343, integration 7 files/95, tsc clean. The commit was amended (message only, tree 4627f0429b05491eb3acdf164297c5e329ba41bd unchanged).

## Gate (through-code: read and run the cells; no stack)
1. Diff develop(026c2d16)..9d974c4b by file and hunk; only the four files; classify every hunk (behaviour / test / comment).
2. m1: read the guard and migration 046 yourself. Does lower(status) = 'active' admit ANY status value the CHECK permits that should NOT be live (whitespace, mixed-case variants of another status, NULL)? Run the cells; add any missing negative control you find. Confirm the impact framing (platform-role-only route).
3. The sweep: re-walk the eight sites yourself and say whether any comparison in that route still fails to fold case where the data can differ in case.
4. m2/E3: does E3 really prove serialisation (a waiter observed), and would it go red under R2/R3? Re-run the author's mutants R2, R3, R4, R10, R11, m1r yourself, with a comment-only control, rejecting any kill whose failures carry an empty message; add two of your own.
5. bd11c34e: confirm it is behaviour-neutral given UUID_TEXT, and that the rewritten comment is now true.
6. Merge prediction on the LIVE develop tip (re-read it yourself): overlap scan with a planted control, merge-tree with a conflicting negative control.

## Rules
Read-only on the project: clone --shared into YOUR scratchpad and fetch there. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; never delete; never rm inside bash -c. Your own Postgres on a free port (lsof first); avoid 55413, 55414, 55418, 55419, 55436, 55440, 55463. Write only here and in your scratchpad (raw outputs under evidence/, never a directory named out); npm/tar outputs to explicit absolute paths in your scratchpad.

## Output
0_Brain/reference/2026-10-13_gate-pr1548/verdict.md: VERDICT on line 1, sha256/16 of the report on LINE 2 (delete line 2, sha256 the rest, first 16 hex), FOUND / TESTED / HOW, NOT tested, severities with file:line. Merge only on Wednesday's head-bound GO. Nothing deploys from this verdict.
