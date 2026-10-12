# QA gate: Secuura Platform K PR #1503 (KS-1180 P-1005-3)

Head sha: 2e6e86278cd25df574af6cb9315b9aaa9c2474d7 (confirmed from the bundle; parent = base)
Base sha: 06d33fb4b321c77270ff958f9db6accc5a622da8 (is an ancestor of origin/develop, which is now 2 commits ahead at 037575399cbaa5456e4df6cae6627717a19ea225)
Gate: independent Sonnet-tier, 2026-10-12. Client scope: Secuura only.

## VERDICT: GO

PR #1503 is a true one-line, comment-only change, and the new comment is accurate: `persistedAnchored` is the only reader of `_source`, and it uses it to keep a statusless tier-2 blob out of the tier-1-only on-chain carve-out.

## By my runs
All runs in my own clone (scratchpad gate1503/clone), head checked out, `npm ci --ignore-scripts` in Blockchain/Dev, packages/shared built first (tsc rc=0). Scripts are in scratchpad gate1503/scripts.
1. Diff: `git diff 06d33fb4b321 2e6e86278c` is 1 file, 1 insertion, 1 deletion, `-U0` shows only line 381 of Blockchain/Dev/services/api-gateway/src/routes/verification.ts. Code before the `//` is identical (`_source: 'anchor_store',`). The commit is the single child of base (rev-list count 1).
2. Build comparison (api-gateway tsconfig, 0 tsc diagnostics for every variant, 140 emitted files each):
   - `--removeComments`, base vs head: `diff -rq` empty, all 140 files byte-identical (the .js.map files too).
   - Plain build (comments kept), base vs head: exactly two files differ, `routes/verification.js` (one line, 282, the comment) and `routes/verification.js.map` (mapping lines 282 and 283 only; no other map field differs; 1360 lines both).
   - Base was built by swapping only that one file in place in the same directory, so source-map paths are identical (my first attempt with a sibling dir produced bogus map diffs; discarded, not a finding).
   - Positive control: one-token change `'anchor_store'` -> `'anchor_stor'` on line 381: the `--removeComments` emit differs in `verification.js` and `verification.js.map`. So the comparison can see a code change.
   - The file was restored afterwards (tree clean of tracked changes).
3. Reader grep across the head tree (`git grep -w _source`, node_modules excluded): the only hits are
   - verification.ts:381 (the writer, `makeFetchDocFromAnchorStore`), :377 and :717 (comments), :734 (the one code reader: `persistedStatus == null && (doc as any)._source !== 'anchor_store'`);
   - tests: ks1073-tier-2-verify-has-no-statusless.test.ts (writes `_source` into fixtures at 200-206, comments at 6 and 13), ks1123-...empty-string.test.ts:202 (comment);
   - unrelated: React `_getVersion(r._source)` in three minified website bundles and a python helper `def _source(...)` in systemTest/schemathesis.
   - Quoted/bracket forms (`['_source']`, `'_source':`) return nothing. Positive control: the same grep returns the known lines 381 and 734.
   - No telemetry reader exists in any service, frontend, script or doc.
4. Claim check: `doc` is the object returned by `fetchDocFromAnchorStore` (line 531) which sets `_source: 'anchor_store'` (381). At :730-735, `persistedAnchored` = real hash && real height && not simulated && (status 'confirmed' || (status == null && `_source !== 'anchor_store'`)). So the marker excludes a statusless tier-2 blob from the carve-out, which the comment at 717-719 and the ks1073 tests (5 tests) confirm. The old text "marker for downstream telemetry" was false; the new one is true.
5. Tests: `vitest run` over the whole api-gateway suite at head: 112 files passed, 1076 tests passed, rc=0 (superset of the 59 files mentioning verification/persistedAnchored; ks1073 file ran, 5 tests green).

## Findings
- Major: none.
- Minor: none.
- Note 1: base 06d33fb4b321 is not the current develop tip (2 commits ahead, 6 files, originate/anchorStateSync/blockHeight area). Those commits do not touch the api-gateway verification.ts, so the line-381 change should merge cleanly; I did not test a merge.
- Note 2: the new comment is a single ~170-character line (the neighbouring comments use multi-line blocks); cosmetic only. It also says "tier-2 marker" while `lookupSource` (line ~528) is a separate local variable; no confusion in code.
- Note 3: the `(doc as any)._source` read is untyped, so a rename of the field would not be caught by tsc; the ks1073 tests are the guard. This is why "load-bearing" is a fair label.

## NOT tested
- Docker, integration/e2e, deployed behaviour, CI on the PR itself; GitHub-side state (checks, review, merge status) not read.
- Merge against current develop tip.
- Non-api-gateway services' builds (not touched by the diff).
- Lint/prettier on the long line.
