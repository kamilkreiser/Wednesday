# Gate brief: GATE E2 = PR #1569 (KS-1509) + PR #1571 (KS-1619 part 3), TIER 2 through-code, batched (disjoint files), Sonnet

Commissioned by the Wednesday seat, 2026-10-18 ~21:5x AEDT, under model routing v1.0 (Kam approved 20:55:59). Tier-2 gates run on Sonnet. If you find anything security-shaped, say so on line 1 and Wednesday hands the PR to a tier-1 Opus gate. Seat R 47th raised both PRs on develop 1197ab38a. Live develop is 833984fc94acf6bc00ff8e5d6642fa768dd44e09 (re-read it). 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- **#1569 KS-1509 (1 of 7 sites)**, head 1f5d868b69bab7e67389098984a5fc6a604bbbc6:
  - services/originate/src/services/anchorStateSync.ts: markDocumentAnchorFailed carries an unknown prior blockHeight forward as null, not a fabricated 0. A real height is kept, and a confirmed anchor is never written.
  - __tests__/ks1333-sync-writers-persist-null-not-zero.test.ts.
  - It is an unmodified Spark patch.
- **#1571 KS-1619 part 3**, head fe69faba83a034b5ec4df905be8c9c8daa3e0355:
  - services/api-gateway/src/routes/verification.ts:1579: the GET /api/document-types catch log uses fail500's describer (routes/batch.ts:24-29).
  - __tests__/ks1543-document-types-catch-logs-the-error.test.ts.
  - It is an unmodified Spark patch.
- **Author's claims (NOT evidence):**
  - KS-1509: red-first 2/12, green 14/14, originate 1371 -> 1375.
  - KS-1619 p3: red-first 3/6, green 9/9, api-gateway 1170/1170, tsc 0.

## Gate
1. Diff each PR by hunk at its head: nothing outside the named files.
2. Red-first and green yourself for each named test at the live tip.
3. #1569: grep every READER of `blockHeight` in originate and the services that consume its blob. Does any reader do arithmetic or comparison on it, or assume a number where it now gets null? Name each reader and what it does with null.
4. #1571: the describer is byte-identical to fail500's (string-compare it). The log never carries a field VALUE (plant a secret in a thrown object).
5. At least two mutants per product hunk, plus a comment-only control. Run the owning suite and tsc, before and after.
6. Merge prediction on the live develop for each PR alone and both in each order. Include an overlap check and a planted conflicting control.

## Rules
- Read-only on the project. Work in your own clone under /private/tmp/claude-501/ (git clone --shared from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, origin set to git@github.com:Secuura/Distributed_Secuura.git, fetch with that checkout's core.sshCommand).
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker.
- Never cd, and delete nothing.
- **Every loop goes in a script FILE run as `/bin/bash /abs/path/script.sh`, never inline `bash -c`.**
- Write only in this folder and your scratch dir.

## Output
- Write 0_Brain/reference/2026-10-18_gate-E2-pr1569-pr1571/verdict.md.
- Lines 1-2: one verdict line per PR (GO / GO WITH NOTE / NO GO), each naming its head.
- Line 3: the sha256/16 of the report (delete line 3, sha256 the rest, take the first 16 hex characters).
- Then FOUND / TESTED / HOW, NOT tested, and severities with file:line.
- Final line: `WALL-CLOCK: <minutes>`.
- This is round 1 of 2.
