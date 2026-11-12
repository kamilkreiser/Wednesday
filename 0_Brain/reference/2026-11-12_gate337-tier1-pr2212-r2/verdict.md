PR 2212: GO WITH NOTES (at head 3a4ca8f63c57; tier 1; round 2 of 2)

Gate 337, tier 1 (Opus), round 2 of 2, one session, 2026-11-12 08:22Z to 08:42Z (19:22 to 19:42 AEDT). Findings only: nothing was fixed, posted, mailed, pushed or merged, and nothing was written to Linear, GitHub or a board.

**Why GO WITH NOTES, in one paragraph:** every gate-335 finding this round had to close is closed, and each closure was reproduced here, not taken from the READY. G335-2212-1 (the Major): R5 is red at the round-1 head with the exact RangeError and green at 3a4ca8f6. Probes at 120,000, 125,000, 200,000 and 500,000 failed events show the head keeps every event in order, resolves, and survives the interval timer with no unhandled rejection and no exit. Develop also keeps every event, but in reverse order and 80 times slower at 500,000. G335-2212-5: C3 kills the push-to-the-back mutant. G335-2212-2 is corrected in the body, and -3 and -4 are stated. On Q4, the new `this.eventBuffer = failed.concat(this.eventBuffer)` is safe. Nothing outside `flush()` and `log()` holds the array. The reassignment reads the live buffer synchronously after the last `await`. A 500-seed deterministic interleaving fuzz gives a byte-identical delivery sequence to the round-1 head, with no loss and no duplicates. The residue is four Notes or Info items, none blocking: a false sentence in the new test's comment, one test gap, and two Info items on cost.

## Where things ran

- **My clone:** every write verb ran in `scratch/repo` (`scratch/setup.sh`, a copy of gate 335's): `--filter=blob:none`, sparse checkout, the project deploy key as `core.sshCommand`, and `p2212` checked out. Fetch and merge-tree ran only there. I did not touch the shared Secuura checkout or the seat's worktree.
- **node_modules:** a symlink to gate 313's `r2` install (vitest 4.1.12, tsc 5.9.3), the same as gate 335. Node v26.8.1 (NOT the LTS line), macOS arm64.
- **vitest:** `scratch/run.py` (gate 335's, re-pathed). It runs the package's own script, `node scripts/require-vitest.cjs && vitest run`, with cwd = `packages/shared`. It waits for load1 < 8 before every run, and the start loads were 3.68 to 7.99, printed in `out/runall.txt`. After every swap it restores the file and checks the blob: `restored 29569eea3a92 OK` every time. The test file was restored to `46e778b5a71f` after the planted cell. At the end, `git status` showed only the node_modules symlink.
- **Probes:** esbuild bundles of `audit-logger.ts` at develop (a65b5cf8), r1 (3b0e8031) and r2 (29569eea), with gate 335's stub logger (`scratch/probe/{dev,r1,r2}/`). The scripts are `big2.cjs` (new), `probe.cjs` and `overlap.cjs` (gate 335's), and `fuzz.cjs` (new). Raw output is in `out/big2.jsonl`, `out/probe.jsonl`, `out/probe_overlap.jsonl`, `out/fuzz.jsonl` and `out/fuzz_mutants.jsonl`.

## Pins

| when | develop | refs/pull/2212/head |
|---|---|---|
| start, 08:22:00Z (`scratch/pins_start.txt`) | ed5b86ea20aebcf8585838a5ed2ca7959f3fd62b (= commission) | 3a4ca8f63c57cb0b1b02c81da3505cb8065d3fe3 (= commission) |
| end, 08:41:03Z (`scratch/pins_end.txt`) | **fa2d60ca8ceec35299bf934c9c8d2bf74a330c8d (MOVED)** | unchanged |

**Develop moved during the gate.** fa2d60ca is **PR 2211's squash** (GraphQL: MERGED 08:22:42Z, mergeCommit = fa2d60ca), "Refs KS-1931 … GDPR erasure cascade".
- It touched exactly 2 files: `services/kyc/src/index.ts` (+4 -2) and one new kyc test (+151).
- It touched 0 files under `packages/`, as the commission predicted. This was measured.

**Shape:** head = 2 commits on acee38da: 4d40bb49 (round 1) plus 3a4ca8f6 (round 2, a fast-forward with no rewrite). `git diff 4d40bb49 3a4ca8f6` contains exactly one product line (plus its comment) and the 62-line R5 and C3 addition. GraphQL: OPEN, not draft, base develop, headRefOid = pin, 2 commits, 2 files, +213 -4, MERGEABLE, closingIssuesReferences 0.

## Q1. G335-2212-1 closed? Yes, measured.

**In the suite** (whole packages/shared each time):

| run | R5 result |
|---|---|
| red first, audit-logger = r1's 3b0e8031 (`out/redfirst_r1.json`) | **FAILS**: `promise rejected "RangeError: Maximum call stack size excee…" instead of resolving` (2.1 s). The other 7 cells pass. The run has 2 failed of 1,631 (R5 + wallet). |
| head (`out/whole_head.json`) | **passes** (2.26 s at load about 4 to 7) |
| mutant M8, the round-1 `unshift(...failed)` put back into the head | FAILS with the same RangeError |

**Probe, one flush of N failing events, then a second failing flush, then recovery** (`big2.cjs`; `/usr/bin/time -l` max RSS; load1 3.7 to 4.4):

| N | build | 1st flush | kept, oldest first | 2nd failing flush | after recovery: delivered, in order | fail-flush time | max RSS |
|---|---|---|---|---|---|---|---|
| 120,000 | develop | resolved | 120,000, **reversed** | kept | 120,000, in order (two reversals) | 2.0 s | 220 MB |
| | r1 | resolved | 120,000 | kept | 120,000 | 0.22 s | 229 MB |
| | r2 | resolved | 120,000 | kept | 120,000 | 0.23 s | 226 MB |
| 125,000 | r1 | **rejected RangeError, buffer 0** | lost | n/a | **0** | 0.23 s | 205 MB |
| | r2 | resolved | 125,000 | kept | 125,000 | 0.22 s | 234 MB |
| 200,000 | develop | resolved | 200,000, reversed | kept | 200,000 | 6.2 s | 276 MB |
| | r1 | **rejected, buffer 0** | lost | n/a | **0** | 0.35 s | 273 MB |
| | r2 | resolved | 200,000 | kept | 200,000 | 0.35 s | 313 MB |
| **500,000** | develop | resolved | 500,000, reversed | kept | 500,000 | **74.9 s** (and 85.5 s for the 2nd; 161 s wall) | 448 MB |
| | r1 | **rejected, buffer 0** | lost | n/a | **0** | 1.1 s | 479 MB |
| | r2 | **resolved** | **500,000** | kept | **500,000, in order** | **0.90 s** (and 0.95 s for the 2nd) | **554 MB** |

At 500,000, nothing else breaks at head: the flush resolves, order is kept, and the time is linear (0.35 s at 200k, 0.9 s at 500k). Develop's per-event `unshift` is quadratic: 6.2 s at 200k and 75 s at 500k, so the head is 80 times faster there. The head's peak RSS is about 100 MB above develop's at 500k (G337-2212-4, Info).

**Interval timer (line 141, no catch), real 50 ms interval, child process** (`out/probe.jsonl`):

| case | develop | r1 | r2 |
|---|---|---|---|
| 130,000 failing, with listener | 0 unhandled, buffer 130,000 | 1 unhandled, buffer 0 | **0 unhandled, buffer 130,000** |
| 130,000 failing, no listener | exit 0 | **exit 1** | **exit 0**, buffer 130,000 |
| 200,000 failing, no listener | exit 0, buffer 200,000 | exit 1, buffer 0 | **exit 0, buffer 200,000** |
| 2 events, logger throws, no listener | **exit 1**, buffer 0 | exit 0, buffer 2 | exit 0, buffer 2 |

By reading the code, `flush()` at head has no remaining rejection path short of OOM:
- the `[...this.eventBuffer]` array literal has no argument limit;
- `onEvent` is caught;
- `String(error)` is guarded;
- `logger.error` is guarded;
- `concat` takes a single argument.

## Q2. G335-2212-5 closed? Yes. Gate 335's full mutant list re-run at the new head, plus 4 more.

Whole suite each time (`scratch/mkmut.py`, `scratch/mut/*.ts`, `out/mut_*.json`). Each "failed" count includes the known wallet-signature red.

| mutant | failed | killed by |
|---|---|---|
| M1 unshift per event (develop's order) | 5 | R1, R2, R4, R5 |
| M2 log before push (after the guarded log) | 1 | **survives**, equivalent (as in gate 335) |
| M3 drop the inner try/catch | 3 | R3, R4 |
| M4 put back (concat) inside the loop | 4 | R1, R2, R4 (duplicates: `[A, B, A]`). See the note below. |
| M5 push after the throwing log | 3 | R3, R4 |
| **M6 failed appended at the BACK** (`this.eventBuffer.concat(failed)`) | 2 | **C3** (`expected [ 'KS1923_Z', 'KS1923_A' ] to deeply equal [ 'KS1923_A', 'KS1923_Z' ]`). **The kill is reproduced; G335-2212-5 is closed.** |
| M7 reversed before the put-back | 5 | R1, R2, R4, R5 |
| M8 round-1 `unshift(...failed)` | 2 | R5 (RangeError) |
| M9 put back `failed` only, dropping events logged during the flush | 2 | C3 (`[A]`) |
| M10 reverse loop of single `unshift`s (gate 335's other suggested fix) | 1 | **survives**: an equivalent alternative fix, slower (R5 7.3 s vs about 2 s) |
| **M11 concat onto a STALE reference** (the array assigned at flush start, not the live `this.eventBuffer`) | 1 | **SURVIVES**: G337-2212-2 |

**Note on M4:** the first M4 run hung for more than 4 minutes. R5's 200,000 failures make the in-loop concat quadratic, and vitest's 30 s timeout cannot stop it. I killed my own vitest worker; the restore still ran and checked OK. I then re-ran M4 with R5 deselected (`-t '^(?!.*R5 200,000).*$'`, `out/mut_M4_noR5.json`), and it was killed by R1, R2 and R4.

**Survivors:**
- M2 and M10 are equivalent.
- **M11 is real and untested.** The production code is correct (Q4), but no cell would catch a regression to a stale reference.

## Q3. Body

Read through GraphQL (`scratch/prbody2212.txt`, 14,378 chars, equal to the READY's figure).
- **G335-2212-2 is corrected.** The tier line now says "no production code imports this `AuditLogger` today, so the change is real but inactive". "Before this deploys" names `services/shared/src/security/audit.ts` as the live logger and says the change runs nowhere even after a rebuild. "every service" occurs once, only as a quote of the corrected sentence. The wire-or-retire decision is left to the board.
- **G335-2212-3 and -4 are stated** in the Round 2 section, accurately (my probes reproduce chain2 A,B 2/2 and chain3 B,A,C 0/3 at r2, identical to r1).
- **Refs only:** the title says `Refs KS-1923`, closingIssuesReferences is 0, and a close-word scan found no close word followed by a key. "piece 1 of 2" is present once, NO-PAIR is present, and the Linear URL is present.
- The Round 2 section is accurate against my measurements. Its R5 time of "1.18 s" is the seat's; I measured 1.5 to 2.3 s under higher load.
- The body says nothing about how R5 behaves at develop. The test file does, and it is wrong (G337-2212-1).

## Q4. Anything new from the reassignment? No defect. One test gap.

- **References to `eventBuffer`:** `grep -rn -i eventBuffer` over the sparse `Blockchain/Dev` (node_modules and dist excluded) finds 7 hits, all in `audit-logger.ts`:
  - the declaration (118);
  - the `push` and the length check in `log()` (269, 272);
  - `flush()`: the empty check, the copy and the reassign (313, 315, 316);
  - the put-back (336).
  
  There is no getter, no exported accessor and no test that reaches in, so nothing can hold the old array. The type is `private`.
- **Reassignment is not new:** `flush()` already reassigned `this.eventBuffer = []` at line 316 at develop, so array identity was never stable.
- **Concurrent flush:** the put-back reads `this.eventBuffer` at the moment it runs, which is synchronous after the loop's last `await`. Events that `log()` pushed during the flush, and any concurrent flush's own put-back, are therefore kept.
- **Measured** (`fuzz.cjs`): 500 seeds of random `log()` and `flush()` interleavings, with `maxBatchSize` 5 so `log()` triggers nested flushes, and a flaky async sink scheduled on microtasks so each seed is deterministic.

  | build | determinism control (same seed twice) | lost | duplicates | rejections | identical delivery sequence to r1 |
  |---|---|---|---|---|---|
  | r1 | 500 of 500 same | 0 | 0 | 0 | n/a |
  | r2 | n/a | 0 | 0 | 0 | **500 of 500** |
  | dev (differs, as a sensitivity control) | n/a | 0 | 0 | 0 | 0 of 500 |
  | **M11 stale reference (positive control)** | n/a | **events lost in 500 of 500 seeds** | duplicates in 481 of 500 seeds | n/a | 0 of 500 |
  | M6 push to back | n/a | 0 | 0 | n/a | 0 of 500 |

  So the fuzz would catch the stale-reference bug, and r2 is behaviour-identical to r1 at small sizes.
- **gate 335's two-overlapping-flush probe:** X, A at develop, r1 and r2. This is pre-existing, as gate 335 said.

## Q5. Suite, tsc, merge-tree

| run | load1 at start | files | tests | failed | rc |
|---|---|---|---|---|---|
| head (`whole_head`) | 3.68 | 82 | 1,631 | 1 (wallet-signature) | 1 |
| red first r1 (`redfirst_r1`) | 5.76 | 82 | 1,631 | 2 (R5 + wallet) | 1 |
| red first develop (`redfirst_develop`) | 6.98 | 82 | 1,631 | **6** (R1 to R5 + wallet). R5 fails on ORDER, 15.3 s | 1 |
| planted cell (`planted_cell`) | 7.04 | 82 | 1,632 | 2 (planted + wallet) | 1 |

- **Whole-ness:** the head report's 82 files are set-equal to a walk of `src/__tests__/**/*.test.ts` (82).
- **The one red:** `wallet-signature.test.ts` › "accepts a valid wallet signature over the message", identical in every run. The counts match the READY (82 / 1,631 / 1 failed).
- **tsc:**
  - `tsc --noEmit -p packages/shared/tsconfig.json`: rc 0, 0 lines.
  - With the test files (`scratch/tsc/tsconfig.tests.json`): rc 2, **24 error lines, line-for-line identical to gate 335's r1 output** (`diff` empty), and 0 naming audit-logger or ks1923.
  - **Planted control** (`scratch/tsc/planted.ts`, a string assigned to a number): rc 2, 25 lines, and the extra line names `planted.ts`.
- **Merge-tree onto the END develop fa2d60ca** (`out/merge_tree_end.txt`): rc 0, tree c63d1561.
  - Merge-base in both argument orders = acee38da.
  - develop to merged: exactly the PR's 2 files (+205; +8 -4).
  - head to merged: exactly develop's 4 moved files (PR 2209's auth pair and PR 2211's kyc pair).
  - **Survival control:** kyc `index.ts` merged = develop's d08288dc, not the head's cdd06301. The ks1931 test merged = develop's 52bc61a6, which is absent at head.
  - The PR's files merged = the head's blobs (29569eea, 46e778b5).
  - The start-of-gate merge-tree onto ed5b86ea (`out/merge_tree.txt`) was also rc 0, with the same controls.
- **Census:** GraphQL found 101 open PRs and 445 file rows (`scratch/census_rows_gql.tsv`).
  - `audit-logger.ts` is touched by [2212] only, and the ks1923 test by [2212] only.
  - Under `packages/shared/src/security/`: [2066, 2212]. As gate 335 found, 2066 touches `keyRevokePolicy.ts`, which is disjoint.
  - Controls: `services/auth/src/routes/users.ts` gives [2075, 2201], and an absent path gives [].
- **Load:** every suite started below 8. `run.py` waited twice (8.40 and 8.88).

## Findings

- **G337-2212-1 (Note, the test's comment is wrong, measured): the comment above R5 says "it passes at develop, whose per-event unshift has no argument limit". At develop, R5 FAILS.** The failure is `expected false to be true` on the in-order check, after 15.3 s.
  - Develop keeps all 200,000 events but in reverse order, so the order check fails.
  - The half about no argument limit is true. The claim that R5 passes is not.
  - This is a comment line only, with no product effect. It is worth a one-word fix when the file is next touched, because a reader using it to judge develop would be misled.
- **G337-2212-2 (Note, test gap; the product is correct): M11, a put-back onto a stale reference to the buffer, survives the suite.**
  - The safety of `this.eventBuffer = failed.concat(this.eventBuffer)` depends on reading the LIVE buffer after the last `await`.
  - No cell runs a flush that triggers a nested or concurrent flush. C3 logs during a flush, but with `maxBatchSize` 1000, so no second flush runs.
  - The deterministic fuzz kills M11 (events lost in all 500 seeds) and shows the head is correct.
  - **Residue for piece 2 or a ticket:** one cell with `maxBatchSize: 1` where `onEvent` logs during a failing flush.
- **G337-2212-3 (Info): two mutants survive and are equivalent.**
  - M2 (log before push), as in gate 335.
  - M10 (reverse-loop unshift): same behaviour, slower (R5 7.3 s against about 2 s). Not a defect.
- **G337-2212-4 (Info, measured, cost): `concat` allocates a new array of size failed + buffer on every failing flush.**
  - At 500,000 events the head's peak RSS is 554 MB, against 448 MB at develop: about +100 MB of transient copies, because `events`, `failed` and the concat result coexist.
  - Time is linear: 0.9 s against develop's 75 s.
  - The real bound on the backlog is piece 2 (KS-1923's unbounded buffer, pre-existing). Nothing here warrants a change in this PR.
- **G337-2212-5 (Info, gate conduct):**
  - node_modules is symlinked from gate 313's r2 install, and the runtime is Node 26 (not LTS).
  - The probes are esbuild bundles with a stub logger.
  - My first `probe.cjs` batch ran under zsh, so the unquoted scenario strings did not split. The "persist" and "timer" rows came back empty, and I re-ran the batch under bash (`scratch/probe/runall.sh`). Only the bash run is reported.
  - The first M4 run hung (quadratic in R5), and I killed my own vitest worker. M4 was re-run with R5 deselected.
  - Develop moved during the gate (PR 2211, services/kyc only). It was measured and the merge-tree was redone at the end pin.

**Round-2 cap ledger:**
- **Closed, and they ship:**
  - G335-2212-1 (the Major): R5 red at r1 and green at r2, with probes to 500k and the timer.
  - G335-2212-2: body corrected.
  - G335-2212-3 and -4: stated in the body.
  - G335-2212-5: M6 killed by C3. The large-backlog cell exists (R5).
- **Residue that becomes tickets or piece-2 scope (non-blocking):**
  - G337-2212-1: the R5 comment's develop claim.
  - G337-2212-2: a nested-flush cell pinning the live-buffer read.
  - Still open from gate 335 and the seat's own NOT-run list: a cell with `hashIntegrity: true`, and the unbounded buffer and retry policy (piece 2).

## NOT TESTED

- Node 24 (LTS).
- Other `--stack-size` values and V8 builds.
- A real audit sink or a real `logger`.
- An OOM ceiling beyond 500,000 events.
- Any service suite (no importer).
- The four platform suites.
- eslint, docs-fragments, `audit:gate`, and the pre-push hook legs (the seat's figures were not reproduced).
- A fresh `npm ci` at the head.
- The merged tree c63d1561 through the suite (develop's moves are services-only).
- The Linear KS-1923 ticket and the seat's comment b258fd85.
- The seat's worktree `s-r110-ks1923` and its `evidence/row1923r2/`.
- The Spark shadow review (not commissioned this round).
