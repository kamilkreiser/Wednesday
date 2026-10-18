PR #1579 (KS-1623 N3) head 76de780c20421cf963d53273571776c1e2e8a97a: GO WITH NOTE (nothing security-shaped; the note is a coupling gap, section S1)
PR #1580 (KS-1624 F1 a) head fcc1451c7bfed310d2d38e63386c9b687c1ad2a4: GO (nothing security-shaped)
sha256/16: 5651dadf9221874f

# Gate G3 verdict, tier 2 through-code, Sonnet, round 1 of 2

Live develop re-read by ls-remote at the end: 6184eaa0af75c1e27eb69bbff67a7790ef494b5f (unchanged). Both PR heads re-read and match the brief. Scratch: g3/ (clones `repo`, `repo2`, scripts `t1579.sh`, `t1579b.sh`, `t1580.sh`, outputs `t1579.out`, `t1580.out`). Node v24.7.0, tsc 5.9.3 via Blockchain/Dev/node_modules/.bin/tsc (asserted, never npx). `npm ci --ignore-scripts` then `npm run build -w packages/shared` rc 0 in both clones.

## FOUND

Security: none. Both PRs are a comment + source-text test, and an export + banner. No input, auth, SQL or tenant behaviour changes. The SQL predicate in verification.ts:1467 is untouched (`git diff` shows only comment line 1445).

### #1579
- Hunk diff vs merge-base 6184eaa0a: exactly the two named files, +45/-1. Product hunk is the one comment line `services/originate/src/routes/verification.ts:1445`, now `Absent, another tenant's, draft, revoked, deleted, expired and the sentinel all answer ONE not-found body.` The SQL it describes (`:1467`, `lower(btrim(d.status)) NOT IN ('draft', 'revoked', 'deleted', 'expired')`) matches the comment.
- S1 (NOTE, low): the test does not compare the comment with the SQL. It compares the SQL with a HARDCODED list (`['draft','revoked','deleted','expired']`, test CONTROL 2) and the comment with hardcoded names (`deleted`, `expired`, and the five CONTROL words). Consequences, all measured:
  - SQL gains a status, comment unchanged: RED, but on CONTROL 2 ("the query hides exactly ..."), a pin on the list, not a comment/SQL comparison.
  - SQL gains a status AND comment names it: still RED (CONTROL 2). A legitimate widening must edit the test list too (loud, by design).
  - Gap: widen SQL with `suspended` AND update the test's list, leave the comment untouched: 5/5 GREEN. This is the original KS-1623 defect class (summary goes stale while SQL moves) and the suite cannot catch it, because the comment is only checked for the two names `deleted`/`expired`. A future status would need a third RED cell, or the comment check derived from the parsed SQL list (`for (const s of statuses) expect(SUMMARY).toContain(s)`). Not blocking: the PR's stated artefact is today's comment, which is correct.
- The coupling the author flagged (CONTROL matches `lower(btrim(d.status)) NOT IN (` literally): confirmed. A legitimate widening of btrim fails LOUDLY, not silently. Measured: `lower(btrim(d.status, ' '))` and `lower(trim(d.status))` both give 2 failed (CONTROL 1 `HIDDEN` null, CONTROL 2 empty list); the message is a generic `expect(...).not.toBeNull()` failure with no hint that the regex is the cause, so a future editor needs to read the test header. Only one occurrence of that predicate text exists in verification.ts (count 1), so the first-match `exec` cannot bind to a wrong predicate today. Reordering the SQL list fails loudly too (toEqual is order-sensitive), which is stricter than the meaning needs but safe.
- Wrapping the summary comment over two lines fails loudly (4 failed: CONTROL 1, CONTROL 3, both RED cells).

### #1580
- Hunk diff: exactly the three named files, +41/-5. `verify.ts:5` adds `export` to `SECUURA_API_URL` (still the `.replace(/\/+$/, '')`-stripped base), `index.ts` imports it (line 4) and the banner prints `${SECUURA_API_URL}`; ks812 test moves with it.
- Import-time behaviour: unchanged. `verify.ts` top level runs ONE thing, the `process.env.SECUURA_API_URL` read + `.replace` (line 5); no network, timers or listeners. `webhook.ts` line 3 already imports `./verify` on develop, so `verify.ts` was already evaluated at startup. Compiled `index.js` require order is express, @secuura/shared, ./webhook, ./verify; `./verify` is already cached when index requires it. What runs at import now that did not before: nothing (net zero; the only new thing is the `./verify` import statement in index.ts, resolved from cache). (`whatsapp.ts` reads env lazily in arrow functions; `webhook.ts` reads VERIFY_TOKEN in a handler.)
- Banner measured by compiling both sides to scratch and starting the real `index.js` with PORT=0 (killed after 2s). Develop vs PR:
  - unset: `https://demo-pk.secuura.net` both.
  - `https://x.test`: `https://x.test` both.
  - `https://x.test/`: develop `https://x.test/` (raw), PR `https://x.test` (stripped).
  - `https://x.test//base///`: develop `https://x.test//base///`, PR `https://x.test//base`.
  - empty string: default host both.
  So the banner now prints the value the bot actually requests (matches verifyHash URL building). This is the intended fix.
- Behaviour change worth knowing (not a defect): `verify.ts` now has a public export, so any future importer of `./verify` gets the same module-level constant evaluated at first import (already true for the private const).

## TESTED

1. Hunk diff of each PR vs merge-base 6184eaa0a (both merge-bases = live develop): only the named files. PASS.
2. Red-first and green at live tip 6184eaa0a:
   - #1579 test file placed on develop: 3 passed / 2 failed (the 2 RED cells `names deleted`, `names expired`); at PR head 5/5. Matches author's 3/2 -> 5/5.
   - #1580 PR ks812 on develop source: 8 passed / 3 failed (banner cell, exported-base slashes, exported-base default); at PR head 11/0. Develop's own ks812: 7/0. Matches author's 8/3 -> 11/0.
3. #1579 plant/restore (all restored; `git status` clean, `restored? identical`):
   | mutant | result |
   |---|---|
   | comment drops `expired` | 1 failed (RED expired) |
   | comment drops `deleted` | 1 failed (RED deleted) |
   | SQL gains `suspended`, comment lacks | 1 failed (CONTROL 2) |
   | SQL gains `suspended`, comment names it | 1 failed (CONTROL 2) |
   | SQL gains `suspended` AND test list updated, comment untouched | 5/5 GREEN (gap S1) |
   | product hunk reverted (= develop comment) | 2 failed |
   | comment-only control (`all` -> `ALL`) | 5/5 green |
   | `btrim(d.status, ' ')` / `trim(d.status)` | 2 failed each (loud) |
   | SQL list reordered | 1 failed |
   | comment wrapped to two lines | 4 failed |
   (An earlier sed for "drops expired" did not apply, diff 0; it was corrected and re-run in `t1579b.sh`: 1 failed.)
4. #1580 mutants, each restored (`restored: identical`):
   | mutant | ks812 | connector tsc |
   |---|---|---|
   | remove `export` | 9/2 | rc 2 |
   | drop `.replace` strip | 8/3 | rc 0 |
   | banner reverts to raw env | 10/1 | rc 0 |
   | banner raw env with default | 10/1 | rc 0 |
   | drop the import | 10/1 | rc 2 |
   | default host changed in verify.ts | 9/2 | rc 0 |
   | comment-only (verify.ts) | 11/0 | rc 0 |
   | comment-only (index.ts, trailing comment) | 11/0 | rc 0 |
5. Suites, before/after: originate jest at PR #1579 head 112 suites / 1393 passed (develop 111 / 1388; +1 suite, +5 tests = the new file); originate `tsc --noEmit` rc 0. Connector `tsc -p connectors/whatsapp-bot/tsconfig.json --noEmit` rc 0 at #1580 head (5.9.3). Full shell runner `scripts/run-shell-suites.sh`: PR #1580 head 91 passed / 0 failed / 0 skipped (of 91); develop 91/0/0 (same file count; ks812 gains 4 cells inside one file).
6. Merge prediction on live develop (via `git merge`/`merge-tree --write-tree` in scratch clone repo2): #1579 alone clean, #1580 alone clean; merge #1579 then #1580 clean, tree `526bc67b37d39627a5d23c103bf60e64741fda2f`; merge #1580 then #1579 clean, same tree `526bc67b37d39627a5d23c103bf60e64741fda2f`. Matches R's prediction 526bc67b37d3 in both orders (and the full 40-hex is what R prefixed). File-set overlap between the two PRs: 0 files. Planted conflicting controls (a branch editing the same comment line; a branch editing the same banner line): both conflict (rc 1, stage 1/2 entries for verification.ts and index.ts), so the clean results above are real, not a blind merge-tree.

## NOT tested

- Did not run the originate DB-backed integration suites (jest.integration.config.js) or any Docker/CI job; the brief forbids Docker. The PR does not touch behaviour they cover.
- #1579 jest runs used the unit config only (`jest.config.js`); the integration config was not run.
- The banner was measured by compiling with the connector tsconfig and running `node index.js` with NODE_PATH pointing at Blockchain/Dev/node_modules (the connector has no node_modules of its own); a production Docker image build of the connector was not attempted.
- GitHub PR state (CI status, reviews, comments) was not read; heads were verified by ls-remote only.
- Did not run shell runner on #1579 head (author said it was not re-run by subtree-id measurement; #1579 touches no shell file, and the runner at develop and at #1580 head was green 91/0).
- Linear tickets KS-1623/KS-1624 not read (brief forbids writes; no read needed).

## Severities

- S1 LOW (note, not blocking): `services/originate/src/__tests__/ks1623-title-lookup-summary-names-every-hidden-status.test.ts` (new file, the two RED cells at the end and CONTROL 2 at about line 27): comment is not derived from the parsed SQL list, so a future SQL widening that also updates the test list leaves the comment stale and green. Suggest as a follow-up card, not a change to this PR.
- S2 INFO: the btrim coupling fails loudly but with an uninformative message (`expect(HIDDEN).not.toBeNull()`); consider a `message` in a future touch. `verification.ts:1467` is the predicate it binds to.
- No HIGH/MEDIUM findings on either PR.

WALL-CLOCK: 26
