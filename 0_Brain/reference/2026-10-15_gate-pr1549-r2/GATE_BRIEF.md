# Gate brief: PR 1549 (KS-1385) ROUND 2 of 2, DELTA, Opus tier 1

Commissioned by the Wednesday seat, 2026-10-15. Authority past the usage stop: Kam, terminal 2026-10-15 ~12:5x, "if anything needs to be pushed, merged or deployed, do that first as well". 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

- Head 80daaa78a2c7adf7196a41cdf240376d8c2bf75a (author's ls-remote; re-read refs/pull/1549/head yourself). Round-1 gated head b1801721d56b35d7982cbe5b103c740113aa70b9. Delta = three first-parent commits: ea799fd4 (merge of develop e67e0dc1), 12b87963 (round 2: CUSTODY_OPTION 'a' -> 'c' in services/anchoring/src/anchorOverwriteGuard.ts + the ks1385 integration test), 80daaa78 (merge of develop 53b429ed, the ks884 test-fixture cure). Live develop 53b429ed6b4bf4d23c0721bf573b9df1c858bc06.
- Round-1 verdict and evidence: 0_Brain/reference/2026-10-13_gate-pr1549/verdict.md + evidence.tgz beside it. Read it first: this round must close what it found.
- KAM'S RULINGS this round implements, verbatim: card secuura-ks1385-anchor-identity-needs-ps895-ruling-1013 = b "Latest event's identity wins" (2026-10-13 18:54); card secuura-ks1385-custodian-may-update-anchor-identity-1013 = c "Issuer, or anyone in the custodian's organisation" (Kam's live-board message 2026-10-14 11:15:54). KNOWN LIMIT, ruled by Wednesday 2026-10-15 02:17Z and carded to Kam (default keep): documents with NO issuer organisation (every certification) stay fail-closed, so (c) does not reach them; cell C-f pins that.
- Author's claims (NOT evidence): the only code change in round 2 is the constant; red-first 3 failed / 19 passed at (a) (W3, C0, C-d, red on behaviour); a three-arm matrix where only S6 (a colleague in the custodian's organisation) changes; mutation 27/27; anchoring integration 3 files / 30 tests; originate unit 109 / 1368; tsc and ESLint 0 with controls; in-hook 88/88.

## Gate
1. Diff b1801721d..80daaa78 by first-parent commit; confirm the merge commits bring in only develop's own changes, and round 2 is the constant plus comments plus cells.
2. Every round-1 finding: closed, still open, or superseded by Kam's (c); say which for each.
3. Re-run the red-first at (a) and green at (c) yourself, on a real Postgres of your own (secuura_app NOSUPERUSER NOBYPASSRLS for any RLS cell; pick a free port with lsof; avoid 55418, the J seat's).
4. Does (c) admit ONLY what Kam ruled? Probe: the custodian user; a colleague in the custodian's org; the issuer's org; a third org; a NULL-issuer row; a custodian whose organisation changed after the transfer (the author's Info: (c) reads the CURRENT organisation); a forged organizationId JWT claim reaching the guard. State the caller path from POST /api/anchors through the gateway, from source.
5. Mutation: re-run at least the author's g4, g8a, g8b, g12, g13 and two of your own on the constant/branch; comment-only control.
6. Merge prediction on the live tip with an overlap check and a planted conflicting control.

## Rules
Read-only on the project: your own clone under /private/tmp/claude-501/, fetch there. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; delete nothing (no rm, rmdir, find -delete). **Every loop or multi-step command goes in a script FILE run as `/bin/bash /abs/path/script.sh args`, never inline `bash -c '...'`.** If a step truly needs a permission dialog, write evidence/BLOCKED.txt and skip it, naming it in NOT tested. Write only here and in your scratch dir.

## Output
0_Brain/reference/2026-10-15_gate-pr1549-r2/verdict.md: VERDICT on line 1 naming the head, sha256/16 of the report on LINE 2 (delete line 2, sha256 the rest, first 16 hex), FOUND / TESTED / HOW, NOT tested, severities with file:line. Round 2 of 2 under the cap: a NO GO here ships the closed instances and tickets the residue rather than opening round 3. Merge only on Wednesday's head-bound GO; nothing deploys.
