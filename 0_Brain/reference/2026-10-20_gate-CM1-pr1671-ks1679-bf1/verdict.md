VERDICT: GO WITH NOTE at head 1b7e896220df1be0f6d4111e85292318ab5e5b87 (tier 2, round 1 of 2; landing tree fa88e7b755d8260cd916e48883e6ad62e44b7171 on develop 561a6c5b528289f4d7ecd19f9c069501e925e9ea; 0 blockers, 2 notes)

# Gate CM1 - PR #1671 (KS-1679, gate BF1 N1) - verdict

Tier 2 CONFIRMED: 1 file, test-only, zero product bytes. `git diff --numstat develop...pr` is exactly `12 0 Blockchain/Dev/services/originate/src/__tests__/ks1679-the-same-caller-spread-still-overwrites.test.ts`. `routes/certifications.ts` sha256 on the PR head equals develop's: `6abd05c5ea2f25f15116332b05a1fdbb4ff91c44ae1fff12537976c154ad46fa`.

## BLUF
R6 does what BF1 N1 asked. Against a truthiness log gate, each of the four falsy values fails on its own, for each of the two keys, by assertion, and the failing `[key, planted, ...]` pair is named in the message. The count claim holds (1576 -> 1577, 135 files, 0 vanished, 1 new). The landing tree and heads match the claim. I found no blocker. Two notes: the live PR body could not be read, and the sibling KS 1508 / KS 1660 gap remains open (stated by the author, not a defect here).

## Heads (ls-remote at start 14:4x AEDT and at end 14:48:50 AEDT, via the Blockchain deploy key, read-only)
- PR #1671 head `1b7e896220df1be0f6d4111e85292318ab5e5b87` both times; develop `561a6c5b528289f4d7ecd19f9c069501e925e9ea` both times. Equal to the claim.
- merge-base `f01ba49da56d3d55204caa02ab3348f94d63b9c0`; branch is 1 ahead, 4 behind. `git merge-tree --write-tree develop pr` printed a tree and nothing else (no conflict section): `fa88e7b755d8260cd916e48883e6ad62e44b7171`. Equal to the claimed landing tree. Controls: not develop's tree (`033c3ebd146f...`), not the PR head's tree (`c0313d4adf9d...`).

## Findings (Q by Q)
1. **Scope: PASS.** 1 file +12/-0. The 12 added lines are identical (as a line set, via diff) to the added lines of the Spark's `patch.diff` (`.../spark_secuura_2026-10-20_ks_1679_p2/out.md.checker/patch.diff`, 12 added lines).
2. **R6 pins N1: PASS.** The cell loops `['', null, 0, false]` x `['certificationId', 'certifiedAt']` = 8 requests; line 175 asserts status 201 and that the row value is not the planted one; line 176 asserts exactly one log line for that key. Lines on live develop: `if (droppedCertificationId !== undefined) {` at certifications.ts:654, `if (droppedCertifiedAt !== undefined) {` at :657 (each anchor unique; PR file identical to develop). Reproduced mutants, each compiled (service-program `tsc --noEmit` rc 0) and ran 14 of 14 cells, red by assertion (`expect(received).toEqual(expected)`, no TypeError):
   - BF1-tamper (`if (droppedCertificationId) {`): R6 only, pair `["certificationId", "", 1 vs 0]`
   - M7 (`if (droppedCertifiedAt) {`): R6 only, pair `["certifiedAt", "", ...]`
   - M8 (`!= null`, both lines): R6 only, pair `["certificationId", null, ...]`
   - M9 (`typeof === 'string'`, both lines): R6 only, pair `["certificationId", null, ...]`
   - M10 (`if (false as boolean) {` at :654): R4 + R6, pair `["certificationId", "", ...]`
3. **Truthy vs presence: PASS, per value.** A loop stops at its first failure, so aggregate red could hide three of four values. I therefore mutated one value at a time: gate `X !== undefined && X !== <v>` for v in `''`, `null`, `0`, `false`, on each key (8 mutants). Every one went red in R6 only, failing at line 176 with exactly its own pair and count `1 expected, 0 received`: `["certificationId","",...]`, `["certifiedAt","",...]`, `["certificationId",null,...]`, `["certifiedAt",null,...]`, `["certificationId",0,...]`, `["certifiedAt",0,...]`, `["certificationId",false,...]`, `["certifiedAt",false,...]`. The truthy-only mutant on both keys (OWN-truthy-both) fails first at `["certificationId","",...]`. So each of the four values is individually necessary. Further own mutants, all compiling and red by assertion:
   - OWN-log-twice-certifiedAt (logs twice): R5 + R6, pair `["certifiedAt","",  1 vs 2]` (the "exactly once" half is pinned)
   - OWN-gates-swapped (each key's gate reads the other's variable): R4 + R5 + R6
   - OWN-row-keeps-falsy-plant (falsy plants survive into the stored row, logs untouched): R6 only, failing at line 175: `["certificationId","",201, false expected vs true]` (the "dropped from the row" half is pinned; R1-R3 stay green, so only R6 sees it)
   - OWN-row-keeps-null-only: R6 only, line 175, pair `["certificationId", null, 201, ...]`
   Every mutant restored from an in-memory original, restore asserted by sha256 after each, and `git status --short` on the clone empty at the end.
4. **Counts by cell NAME: PASS.** Whole originate jest suite, keyed by `fullName`: develop 135 files / 1576 passed / 0 failed; PR head 135 files / 1577 passed / 0 failed; 0 vanished; 1 new: `KS-1679 the drop is logged without the value RED KS-1679 R6: a FALSY planted value (empty string, null, 0, false) is dropped AND logged for both keys, not only a truthy one`. Names unique in both runs; no non-passing status at head; the jest `numFailedTests` agreed with the name-set (0/0). Positive control for the vanished/new reader: it reported the new R6 cell, so the diff is live.
5. **Known gap stated: PARTIAL, see Note 1.** The commit message does not name the gap. The author's local PR-body file (`.../5_Project_History/2026-10-20_seatD-26th/evidence/prbody-B.md`, lines 95-98) states "This cell does NOT cover the KS 1508 and KS 1660 gates", and lines 100-101 state the null-`rec` TypeError failure mode. That is the author's local copy, not the live PR body.
6. **Type-check and merge: PASS.** The originate tsconfig excludes tests (KS 1090): the service program lists the test file 0 times (`--listFilesOnly`), my child program (extends the service config, `exclude: []`, includes all of `src`) lists it 1 time and compiles with rc 0, 0 errors. Positive control: appending `const x: number = 'x';` to the test made the child program fail rc 2 with TS2322 at the appended line (and TS6133); file restored, sha256 asserted equal to `b8bc9f1f42503f2c2b3412426b55249b8b830d26296d86a69d2184c5838ccbee`. merge-tree clean (above).

## Notes
1. **Live PR body not read.** `gh` has no login in the Blockchain `.gh-config` (`gh auth status`: not logged in) and no token was available, so I could not confirm the live body of #1671 states the KS 1508 / KS 1660 gap; I read the author's local copy instead. Wednesday or the author should glance at the live body. Not a code finding.
2. **The sibling gap is real and open.** The cell covers only the two KS-1679 keys. The KS 1508 (`versionedById`, :648) and KS 1660 (`parentDocumentId`, :651) log gates have the same `!== undefined` shape and the same truthy-only blind spot in their tests; I did not mutate them. Follow-up is the author's open question to Wednesday, not a condition of this merge.

Minor, no action: the cell's `r.rec.data[key]` is read while building the expectation, so a route that returned 500 would give a runtime TypeError red rather than an assertion red. Still red; none of the 18 mutants above does that.

## FOUND / TESTED / HOW
- FOUND: a 12-line test-only change; no product byte; the new cell kills every log-gate mutant tried (truthy-only, `!= null`, `typeof string`, disabled gate, swapped gates, double log, per-value skips) and the row-retains-falsy mutants.
- TESTED: 18 mutants in all (5 reproduced from the author, 13 own), whole originate suite on develop and PR head, child-program type-check with positive control, merge-tree, scope diff, patch-vs-Spark line equality.
- HOW: clone `--shared` of the Spark cache into `.../scratchpad/gate_cm1/src`, fetched `refs/pull/1671/head` and develop from GitHub using the Blockchain deploy key (read-only); `npm ci --ignore-scripts --prefix .../Blockchain/Dev`; built `packages/shared`; `npm run generate --prefix services/originate`; jest via `npm test --prefix services/originate` (JSON output); mutation runner in the scratchpad `tools/mut.py` (outside the clone); `@electric-sql/pglite` was not needed (no m365 file run).

## NOT RUN
- The four platform suites, any other service's tests, lint, the pre-push gate legs, Docker, any live stack: one in-process jest cell touches none of them.
- No mutants on the KS 1508 / KS 1660 gates (out of this PR's scope).
- Live PR body (see Note 1). No GitHub or Linear writes made.

## Wall-clock
14:42:47 to about 14:52 AEDT (about 9 minutes).

sha256 of `sed '1d;$d' verdict.md | shasum -a 256`: 3be93aa3cfc5094591e8a2f371ac330076c25ac5265d746dda658d649c4d11fd
