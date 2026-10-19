VERDICT: GO WITH NOTE at head b30e401ff208... (tier 2, round 1 of 2; landing tree 0e6318c745c7a6ac328fab4c4da5f6d029f66e30 on develop 11af03696c9bd966580e52605cb2a361d9c3d29b; 0 blockers, 3 notes)

## BLUF

The PR is what it says: one markdown file and one test file, no product byte. I measured every claim and found none false; three small notes.

- **Heads:** #1653 = `b30e401ff208940f6e44b44696dd4ab1ff141a98`, develop = `11af03696c9bd966580e52605cb2a361d9c3d29b` by `ls-remote` at start (10:37 AEDT) and end (10:41 AEDT). Neither moved. Merge-base `cd63883c62a9`.
- **Q1:** three-dot set is exactly 2 files (BACKLOG.md, one m365 test). No tier escalation.
- **Q2:** NK1 closed both ways (wording and a cell). BK-X1 (Math.random bytes) is red in V4 ALONE, by assertion, 206 passed / 1 failed. Five further mutants of mine behave as expected.
- **Q3:** the backlog cell exists, passes alone (1 passed / 19 skipped), and reds at the pre-fix parent (positive control). The docs change is accurate except one line-number cite (NB3).
- **Q4:** no cell vanished or changed status on the landing; the four renamed cells are matched by id.
- **Q5:** merge-tree clean; m365 `tsc --noEmit` rc 0 on the landing; landing suite 22 files / 213 tests / 0 failed.

## Findings: blockers

None.

## Findings: notes

**NB1. V4 is coupled to the call shape `crypto.randomBytes`, not to "a CSPRNG".**
- My mutant X6 replaced `randomUrlToken` with `crypto.randomFillSync(Buffer.alloc(32)).toString('base64url')`, a legitimate CSPRNG source. tsc rc 0. V4 goes red (`expected 'lPPm…' to be 'q6ur…'`; all else passes, 206/1).
- That is a false alarm in the safe direction (a refactor to another CSPRNG API would need V4 updated), not a hole. The cell's title says "drawn from the CSPRNG" but pins `crypto.randomBytes`. Cosmetic; one clause in the title or comment would say so.

**NB2. Header comment reflow artefact.** In the test file's header the NK1 paragraph runs straight into the old sentence on one long line: `...V4 now pins provenance. PKCE is defence in depth here (the client is confidential, so redeeming a code still needs` (line 21 of the head file), then the old continuation `ENTRA_CLIENT_SECRET), ...`. Reads fine, is just an over-long line. Cosmetic.

**NB3. BACKLOG cite ":292 -> :279" does not match any develop state.** The cell is at line 263 before the fix (`372c636aa`), 270 at the fix (`2672fedeb`), and 279 at `343a7b4e2` (a later KS-695 commit, = develop now). `:292` was the entry's own cite from another tree, so "moved from :292 to :279" is true of the entry's record but not of develop's history. The PR does already warn that line numbers depend on the tree. The substantive claims (fixed by `2672fedeb` / #1337, suite green, cell present and passing, widened not removed) all hold.

## Findings: confirmations

**Q1 test/docs-only, measured**
- `git diff --numstat develop...pr1653`: `BACKLOG.md` 20/1; `m365-integration/src/__tests__/ks1677-the-pkce-verifier-is-secret-and-random.test.ts` 43/5. `--name-status`: two `M`. Nothing else.
- `develop..pr1653` (two-dot) shows 5 files because it folds in develop's newer commits (#1651/#1652: the ks1682 test deleted, token-manager.ts, a vc-issuer test); those are not this PR. Control that the three-dot is right: the PR has exactly 2 commits (`git log develop..pr1653`: `8c406557b` BACKLOG, `b30e401ff` test).
- Non-test, non-docs bytes: 0. Tier 2 stands.

**Q2 NK1 closed**
- Wording: V2 relabelled SHAPE with its limit in its own body; header, describe title and cell map updated; `grep -i csprng` on the head file lists only the NK1 note, the V4 line, the describe title and V4. No remaining claim that V1-V3 pin CSPRNG.
- Mutants run at the head against the FULL m365 suite, tsc rc 0 before every arm, source restored and sha256 asserted after every arm, no file failed to load:

| arm | tsc | passed/failed | red cells |
|---|---|---|---|
| BASELINE (head) | 0 | 207 / 0 | none |
| **BK-X1** `Math.random` 32 bytes base64url (BK1's mutant, re-applied) | 0 | 206 / 1 | **V4 only**, assertion `expected 'mfqG…' to be 'q6ur…'` |
| X2 draw `crypto.randomBytes(32)` then ignore it, use Math.random | 0 | 206 / 1 | V4 only |
| X3 baked constant `Buffer.alloc(32,0xab)` (is V4 pinning the draw, not a constant?) | 0 | 199 / 8 | V4 (via its post-stub `not.toBe`), V1, V2, V3, R6, R17, R18, R19 |
| X4 verifier-only Math.random in index.ts, state/binding stay CSPRNG | 0 | 206 / 1 | V4 only |
| X5 state and binding Math.random, verifier stays CSPRNG (expect V4 pass) | 0 | 207 / 0 | none (V4 correctly scoped to the verifier) |
| X6 `crypto.randomFillSync` legit CSPRNG | 0 | 206 / 1 | V4 only (NB1) |

- BK-X1 is killed by V4 alone, so the author's claim reproduces. V1, V2, V3 pass it. The red is an assertion, not a load failure.

**Q3 BACKLOG entry**
- `2672fedeb` ("KS-888: widen the KS 764 call-site guard...(#1337)") is an ancestor of develop.
- The cell exists at `packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts:279`; sibling `the sweep can SEE a new revoke surface (the guard on the guard)` at `:312`.
- At develop `11af0369`: `vitest run <file> -t "CALL_SITES matches every revoke surface"` gives `1 passed | 19 skipped`, ✓ 397 ms. Control for the filter: a nonsense `-t` gives `20 skipped`, so the filter selects.
- Positive control that the cell can fail: at `2672fedeb^` the same command is `×` (`AssertionError: expected '/** ... to match /isActive\s*=\s*false;...`). So the fix is what turns it green.
- Whole `packages/shared` suite at develop: 52 files / 994 tests / 0 failed (author's figure, reproduced).
- BACKLOG.md at develop: `- [ ]` 34, `- [x]` 16; at the head 33 and 17. The entry stays at line 1244 in both. Of its diff only the heading line is deleted (1 deleted line); the original record is untouched below the new block.
- The deferral claim is real: the entry text says the fix "belongs with KS-888's owner". NB3 for the one cite.
- Not verifiable by me: "it was cited as a reason to distrust a green suite while measuring an unrelated PR" (a process statement).

**Q4 no weakening (m365 suite, cells by file + full name)**
- develop `11af0369`: 22 files / 212 passed / 0 failed. Head `b30e401f` alone: 21 files / 207 / 0 (it lacks #1652's ks1682 file, which is why it has 21). Landing: 22 files / 213 passed / 0 failed / 0 pending.
- Landing vs develop: no status change. Four "vanished" names are the describe-title rename ("...secret, and it comes from the CSPRNG" to "...secret, random, and drawn from the CSPRNG"); matched by id, V0, V1, V3 identical after the prefix, V2 retitled on purpose. New: V4 only. 212 + 1 = 213.

**Q5 landing**
- `git merge-tree --write-tree develop pr1653` clean, rc 0, tree `0e6318c745c7a6ac328fab4c4da5f6d029f66e30`. A local `--no-ff` merge on a scratch branch gives the same tree (commit sha differs from the author's `7df2199daafd`, which is a commit sha and not comparable; I do not have the author's tree figure to compare).
- `tsc --noEmit` in `services/m365-integration` on the landing: rc 0.

## FOUND / TESTED / HOW

- Clone: `git clone --shared` of the spark cache into `scratchpad/gate_bp1/src`; the cache lacked the PR ref, so I added a `gh` remote with repo-local `core.sshCommand` (read-only deploy key) and fetched `refs/pull/1653/head` and `develop` (fetch only, no push).
- Install: `npm ci --ignore-scripts` in `Blockchain/Dev` (1937 packages, rc 0), `packages/shared` built rc 0. Every npm, tsc and vitest call went through `scripts/inrepo.py`, which asserts the child cwd is inside the clone. No `cd`, no Docker.
- Suites: vitest `--reporter=json` of the full m365 suite at develop, head, landing; cells compared programmatically.
- Mutants: `scripts/mut.py` (exact-count replace asserted, tsc first, sha256 restore asserted). Outputs in `out/`.
- Scratch folder: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bp1/`.

## NOT RUN

- Docker and the four platform suites (barred, and no stack); preflight (not run; the PR touches no runtime surface).
- Other services' suites (auth, api-gateway, vc-issuer): not run; the diff is one m365 test and a markdown file.
- The #1651/#1652 content: not reviewed, only their effect on the landing.
- GitHub CI checks for #1653; the KS-1677 ticket comment (no Linear access).
- The author's N1 PR (#1654) is a separate gate.
- V4 under the other Node crypto entry points (`webcrypto.getRandomValues`, `randomUUID`) other than X6 randomFillSync: not tried.

## Wall-clock

10:37 AEDT start to about 10:44 AEDT verdict, about 7 minutes.

sha256 of the file without its first and last line (method: sed '1d;$d' verdict.md | shasum -a 256): 6e608a529f886c2afaca3b13c4ffebfefe1347adae38a36c025a7e95dc727052
