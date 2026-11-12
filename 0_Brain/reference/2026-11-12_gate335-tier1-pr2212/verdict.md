PR 2212: NO GO (at head 4d40bb4925f8; tier 1; round 1)

Gate 335, tier 1 (Opus), one session, 2026-11-12 07:35Z to 07:53Z (18:35 to 18:53 AEDT). Findings only: nothing was fixed, posted, mailed, pushed or merged, and nothing was written to Linear, GitHub or a board.

**Why NO GO, in one paragraph:** the PR fixes what it says for small batches: order, the throwing logger, and the timer rejection from a throwing logger are all measured. But its one new line, `this.eventBuffer.unshift(...failed)`, spreads the whole failed list into a single call. On Node v26.8.1 that throws `RangeError: Maximum call stack size exceeded` once about 125,000 events fail in one flush. Measured: 120,000 resolves, 125,000 rejects. When it throws, the buffer has already been emptied and `failed` is a local, so **every buffered audit event is lost**, and `flush()` rejects. From the interval timer (line 141, no catch) that is an unhandled rejection, and the process **exits 1**. Develop, with its per-event `unshift`, kept all 130,000 and 200,000 events, with no rejection and no exit (G335-2212-1). A sustained sink outage is the only way to build such a backlog, and that is the case an audit buffer exists for. The fix is one line, plus one cell. Mitigating fact: **no production code imports this AuditLogger at all** (G335-2212-2), so nothing is at risk today. That is why this is a round-1 NO GO on a cheap fix rather than an incident.

## Where things ran

- **My clone:** every write verb ran in `scratch/repo`: a fresh `git clone --filter=blob:none` with sparse checkout (`scratch/setup.sh`), the project deploy key as the clone's `core.sshCommand`, and `p2212` checked out. Fetch and merge-tree ran only there. In the shared Secuura checkout I ran read verbs only (`GIT_OPTIONAL_LOCKS=0`).
- **node_modules:** `Blockchain/Dev/node_modules` is a symlink to gate 313's `r2` install (vitest 4.1.12, tsc 5.9.3), as gates 331 to 334 did. r2's commit 1c5ca4bb36c0 differs from the head's `package-lock.json` by 5 added and 92 removed lines (nodemon removal). packages/shared declares no runner of its own and uses the root install (KS-1317).
- **Restored after each run:** every swap of `audit-logger.ts` and the planted test cell was restored and checked by blob: audit-logger `3b0e803169dd`, ks1923 test `c80ef6c4bf07`. In the clone, `git status` shows only the node_modules symlink.
- **How vitest ran:** `scratch/run.py`, with cwd = `packages/shared`. It runs `node scripts/require-vitest.cjs` and then `vitest run`: the package's own script, with absolute paths. tsc ran by absolute path with `-p`. Nothing ran from the WEDNESDAY working directory.
- **Probes:** esbuild bundles of `audit-logger.ts` at each build, with a stub logger (`scratch/probe/{head,dev}/audit-logger.cjs`, `probe.cjs`, `overlap.cjs`, `runall.sh`). Raw output: `out/probe.jsonl`, `out/probe_overlap.jsonl`, `out/probe_stderr.txt`.
- **Machine and load:** Node v26.8.1 (NOT the LTS line), macOS arm64. load1 ran 4 to 10 during the session. `run.py` waits for load1 < 8 before every suite run, and every suite started at load1 between 4.3 and 7.9 (printed in each run's output).

## Pins

| when | develop | refs/pull/2212/head |
|---|---|---|
| start, 07:35:36Z (`scratch/pins_start.txt`) | ed5b86ea20aebcf8585838a5ed2ca7959f3fd62b (= commission) | 4d40bb4925f884c863551e3d7ab7e18bcac2ec11 (= commission) |
| end, 07:52:31Z (`scratch/pins_end.txt`) | unchanged | unchanged |

Neither pin moved during the gate.

**Shape:**
- One commit 4d40bb49 on acee38da1ce7. `merge-base` in both argument orders = acee38da; `rev-list develop..head` = 1.
- GraphQL: OPEN, not draft, base develop, headRefOid = pin, 1 commit, 2 files, +151 -4, MERGEABLE, closingIssuesReferences 0.

**What moved on develop:** one commit, acee38da to ed5b86ea, "Refs KS-2021: a Pwned Passwords padding row (count 0)…". It is **PR 2209's squash** (GraphQL: MERGED 07:34:39Z, mergeCommit = ed5b86ea).
- It touched `services/auth/src/services/password.ts` (+6 -2) and one new auth test (+87).
- It touched 0 files under `packages/`.

**Merge-tree:** `merge-tree --write-tree origin/develop p2212` gives rc 0, tree e14f33a5c769 (`out/merge_tree.txt`).
- develop to merged: exactly the PR's 2 files (+143 and +8 -4).
- head to merged: exactly develop's 2 moved auth files.
- **Control that develop's lines survive:** `password.ts` merged = develop's 70efe281f672, not the head's f7f463e02bf8. The ks2021 test merged = develop's 9b5e9a56abab, which is absent at the head.
- The PR's 2 files merged = the head's blobs (3b0e803169dd, c80ef6c4bf07).

## Q1. Correctness: red/green and mutants

**Red first** (`out/t_redfirst_develop.log`, `out/redfirst_develop.json`): whole suite with `audit-logger.ts` set to develop's blob a65b5cf8540c and the new test kept, 5 failed of 1,629 tests.
- R1 failed: `[B,A]` vs `[A,B]`.
- R2 failed: `[B,C,A]` vs `[B,A,C]`.
- R3 failed: `'rejected'` vs `'resolved'`.
- R4 failed: `[]` vs `[A,B]`.
- The fifth failure is the known wallet-signature red.
- **C1 and C2 pass at develop.**
- At head, all 6 cells pass (Q5).
- The seat's red-first claim is reproduced exactly.

**Mutants** (whole packages/shared suite each; `scratch/mkmut.py`, `scratch/mut/*.ts`, `out/t_mut_*.log`). Each "failed" count includes the known wallet-signature red.

| mutant | failed | killed by |
|---|---|---|
| M1 unshift per event (develop's order), push kept | 4 | R1, R2, R4 |
| **M2 log before push** (push after the GUARDED log) | 1 | **SURVIVES**, equivalent: with the log inside its own try/catch, nothing can run between the log and the push |
| M3 drop the inner try/catch | 3 | R3, R4 |
| M4 `unshift(...failed)` inside the loop, after each failure | 4 | R1, R2, R4 (duplicates and reorder) |
| M5 push after the THROWING (unguarded) log | 3 | R3, R4 |
| **M6 `push(...failed)` to the BACK of the buffer instead of the front** | 1 | **SURVIVES**: no cell logs an event during a flush, so "in front of anything logged during the flush" is unpinned |
| M7 `unshift(...failed.reverse())` after the loop | 4 | R1, R2, R4 |

All five of the commission's mutants are killed except M2, which is equivalent. My added M6 survives (G335-2212-5).

## Q2. Audit-trail integrity: the hash chain

**How it is computed (from reading the code):**
- `hash` is computed in `log()` (lines 241 to 266), at **enqueue**: `sha256(JSON.stringify({...event, previousHash: this.previousHash}))`.
- `this.previousHash` is then advanced (line 265).
- `flush()` never touches `hash`, `previousHash` or the event object, at develop or at head.
- **`previousHash` is NOT stored on the event:** the `AuditEvent` type has `hash` only, and the probe reads `'previousHash' in event` as false at both builds. A verifier can check the chain only by replaying events in log order.

**Measured** (probe `chain2` and `chain3`, `hashIntegrity: true`; `out/probe.jsonl`):

| scenario | build | delivery order on retry | same objects, hashes unchanged | chain verifies in DELIVERY order | in LOG order |
|---|---|---|---|---|---|
| A, B both fail, then recover | develop | B, A | yes | 0/2 | 2/2 |
| | head | **A, B** | yes | **2/2** | 2/2 |
| A fail, B ok, C fail, then recover | develop | B, C, A | yes | 1/3 | 3/3 |
| | head | B, A, C | yes | **0/3** | 3/3 |

**Plain answer: this PR does NOT change chain semantics.**
- Nothing is re-hashed or re-chained at either build.
- The hashes are fixed at `log()`.
- The only change is the order in which `onEvent` sees retried events.
- When every event in a flush fails, head now delivers in chain order. When a success sits between failures, delivery is still out of chain order at head: the successes go first. This is the PR's own cell R2 (`[B, A, C]`). So the test header's sentence "the audit hash chain did not verify in delivery order" is only half cured (G335-2212-4).

**Consumers that verify the chain: none.**
- `previousHash` appears in exactly 1 file, 3 times (`audit-logger.ts`), over all of `Blockchain/Dev`. Control: the same grep shape with `security/scopes` finds 8 service importers.
- Beyond that, no code outside packages/shared's own tests imports this AuditLogger at all (G335-2212-2).

## Q3. The empty catch around logger.error

**Swallows in `flush()` at head:**
1. `catch { reason = 'unreadable thrown value' }`: pre-existing (KS-1868), and it does not swallow the event.
2. The new `try { logger.error(...) } catch { }`.

The onEvent `catch` itself is not a swallow, because the event is kept. The body's statement "the only swallow" is true of the new code.

**What goes unlogged:** only the failure line, and only when the logger itself throws. The event is kept.

**Persistent failure** (probe `persist`: 5 events, 10 flushes, sink always failing):

| logger | build | buffer after each flush | flush rejects | logger.error calls |
|---|---|---|---|---|
| works | develop | 5 ×10 | 0 | 50 |
| works | head | 5 ×10 | 0 | 50 |
| throws | develop | **0** ×10 (all 5 lost on the first flush) | 1 | 1 |
| throws | head | 5 ×10 (kept) | 0 | 50 attempted, all swallowed |

**Infinite retry and unbounded growth:**
- **Pre-existing:** no retry cap, no backoff, no drop policy. The buffer grows without limit while the sink is down, at both builds. The body says so, and it is KS-1923's piece 2.
- **From reading the code (pre-existing):** once the buffer holds `maxBatchSize` (100) or more, every `log()` call awaits a full `flush()` of the whole backlog (line 272). During an outage each new audit event therefore costs one `onEvent` attempt per buffered event.
- **New at head:** with the logger AND the sink both failing persistently, the backlog now grows **silently**. At develop it was lost, also silently. So the empty catch cannot hide events, but it can hide the outage. That is the trade the body describes; graded Note in G335-2212-3.
- **New at head:** the growth now ends in G335-2212-1 at about 125,000 events.

## Q4. Timer path (line 141, `this.flush()` with no catch)

Measured with a real 50 ms interval, in a child process, with and without an `unhandledRejection` listener (`out/probe.jsonl`, scenario `timer`):

| case | develop | head |
|---|---|---|
| 2 events, sink fails, **logger throws**, listener | 1 unhandled rejection, buffer 0 (lost) | **0 unhandled**, buffer 2 (kept) |
| same, no listener | **process exit 1**, buffer 0 | exit 0, buffer 2 |
| 2 events, sink fails, logger works | exit 0, buffer 2 | exit 0, buffer 2 |
| **130,000 events, sink fails**, listener | 0 unhandled, buffer 130,000 | **1 unhandled (RangeError), buffer 0** |
| same, no listener | exit 0, buffer 130,000 | **process exit 1, buffer 0** |

- **The rejection path the PR targets is closed:** a throwing logger no longer rejects `flush()`, and the timer no longer crashes the process on it. Measured.
- **The PR opens a new one**, the spread-argument RangeError, which reaches the same unguarded timer (G335-2212-1).
- `flush()` can therefore **still reject at head**. The body's "a logger that throws no longer … rejects `flush()`" is true as worded, but the body's summary implies that flush no longer rejects at all, and that is not true.

**Threshold** (`probe big N`, one flush, sink failing):

| N | develop | head |
|---|---|---|
| 1,000 | resolved, buffer 1,000 | resolved, buffer 1,000 |
| 120,000 | resolved, buffer 120,000 | resolved, buffer 120,000 (0.6 s) |
| 125,000 | resolved, buffer 125,000 | **rejected RangeError, buffer 0** |
| 130,000 | resolved, buffer 130,000 (3.7 s) | **rejected RangeError, buffer 0** |
| 200,000 | resolved, buffer 200,000 | **rejected RangeError, buffer 0** |

- A plain `node -e` control shows the same thing without the PR's code: `[].unshift(...arr)` is OK at 120,000 and throws at 130,000 on this Node.
- The limit depends on the stack size and the V8 build, so it is not a fixed constant.

## Q5. Suite and controls

| run | load1 at start | files | tests | rc |
|---|---|---|---|---|
| head (`whole_head`) | 4.29 | 82 (81 passed, 1 failed) | 1,628 passed / 1 failed of 1,629 | 1 |
| red first, audit-logger = develop a65b5cf8 (`redfirst_develop`) | 6.56 | 82 | 5 failed (R1 to R4 + wallet) / 1,629 | 1 |
| planted failing cell appended to the ks1923 test (`planted_cell`) | 7.83 | 82 | 2 failed (planted + wallet) / 1,630 | 1 |
| 7 mutants (table in Q1) | 6.77 to 7.93 | 82 | | 1 each |

- **The one red at head:** `wallet-signature.test.ts` › "accepts a valid wallet signature over the message", the known red. It is identical in every run.
- **Whole-ness:** the head JSON report's 82 file names are set-equal to a walk of `src/__tests__/**/*.test.ts` (82). Develop's 81 files / 1,623 tests = 82 − 1 file and 1,629 − 6 cells, consistent with the seat's figures.
- **tsc:**
  - `tsc --noEmit -p packages/shared/tsconfig.json` (tests excluded): rc 0, 0 lines.
  - With the test files (`scratch/tsc/tsconfig.tests.json`, extending the package config; `typeRoots` pointed at the symlinked install): rc 2, **24 error lines**, all in 12 existing test files, none in either touched file. This equals the seat's count.
  - I did not plant a type error. The 24 pre-existing errors show that this instrument reports errors.
- **Digest STANDARD** (`digest.py --kind vitest`, Spark UP; `out/digest/`):
  - whole_head: CHECKED FAIL, 1 failed (raw rc 1).
  - redfirst_develop: CHECKED FAIL, 5 with the right names (raw rc 1).
  - planted_cell: CHECKED FAIL, 2 (raw rc 1).
  - mut_M2: CHECKED FAIL, 1 (raw rc 1).
  - mut_M6: CHECKED FAIL, 1 (raw rc 1).
  - Every verdict agrees with its raw rc and with the counts. Every run was rc 1 because of the known red, so G331-2209-5's blind spot (rc 1 with all green) was not exercised.

## Q6. Census

**Callers of `AuditLogger.flush` and services importing this module: ZERO in production code.**
- A case-insensitive grep for `audit-logger|auditlogger` over the whole sparse tree finds only:
  - `packages/shared/package.json` (the `./security/audit-logger` subpath export);
  - the source;
  - the two audit-logger tests (ks1868, ks1923);
  - `services/shared/src/security/{audit,index}.ts`. These hold a **different** `AuditLogger` class, with no buffer, no flush and no hash, which does not import packages/shared's.
- `git grep` over the full `Blockchain/` tree at p2212 gives the same 6 files.
- The Secuura checkout at 0e6479d7b (2026-11-10, all top-level trees) adds only two KS-1868 fragment HTML files under `Projects Documents/`.
- `initializeAuditLogger` and `getAuditLogger`: 0 callers outside the file itself.
- `packages/shared/src/index.ts` does not re-export the module.
- **Positive control:** the same grep shape for `security/scopes` finds 8 importer files under `services/` (18 across the Secuura checkout).

**Open PRs** (`scratch/census_gql.py`: 101 open PRs, 444 file rows, each PR's files paged and asserted against totalCount; rows in `scratch/census_rows_gql.tsv`):

| path | open PRs |
|---|---|
| `packages/shared/src/security/audit-logger.ts` | [2212] |
| `…/ks1923-audit-logger-flush-keeps-failed-events-in-order.test.ts` | [2212] |
| `…/ks1868-audit-logger-flush-unreadable-throw.test.ts` (the sibling cells) | [] |
| anything under `packages/shared/src/security/` | [2066, 2212]; 2066 touches `keyRevokePolicy.ts` only, which is disjoint |

- **Positive control:** `services/auth/src/routes/users.ts` gives [2075, 2201].
- **Negative control:** an absent path gives [].

## Q7. PR body

Read through GraphQL (`scratch/prbody2212.txt`, 9,824 chars).

- **Tier-1 statement:** first and bold. Present.
- **The behaviour change:** true as measured for the order and for the throwing logger (Q1, Q3, Q4). It omits the new RangeError path (G335-2212-1).
- **"packages/shared, which every service imports" and "each image would need a rebuild for the change to run anywhere":** literally true of the package, but misleading for this module. No service imports or instantiates this AuditLogger, so the change runs nowhere after a rebuild either (G335-2212-2).
- **"Events carry a hash made when they are logged, linked to a previousHash (lines 260 to 265)":** correct about when the hash is made. Events do not carry `previousHash` (Q2), and the body does not claim they do.
- **"the timer … a rejection from flush() was an unhandled rejection" (by reading):** confirmed by measurement at develop: process exit 1 (Q4).
- **NOT-run list:** honest. The persistent-failure run, the timer probe and the chain verifier were not run by the seat; this gate ran all three.
- **Refs only:** the title says `Refs KS-1923`, closingIssuesReferences is 0, and there is no close word.
- **"piece 1 of 2":** stated.
- **NO-PAIR:** present, as ruled.
- **Linear URL:** present.

## Spark shadow review (calibration row only, not the verdict)

Driver: `scratch/spark_run.sh`. The work dir is `spark_work_2212` in the session scratchpad; copies are in `scratch/spark/`. One attempt, 37.6 s, `valid: true`, `missing_inputs: ["ticket text"]`.

**Deterministic half:**
- head 4d40bb49 (tip), merge-base acee38da, base tip ed5b86ea.
- Diff: 2 files, +151 -4.
- Targeted on the HEAD (ks1923 + ks1868): 9 passed / 0 failed.
- On the BASE product code: 5 passed / 4 failed.
- All of this equals mine: the 4 are R1 to R4.

**Spark verdict: NO GO** (3 Major, 2 Minor, 2 Notes). It matches my verdict by coincidence, for different reasons:
1. **Major, "the timer unhandled rejection was not measured":** framing only. The body labels it "by reading", and I measured it true at develop (exit 1).
2. **Major, "claims the fix makes the hash chain verify in delivery order":** wrong. The body makes no such claim and says that verification is NOT measured.
3. **Major, provenance "not verified":** wrong. Its evidence quote was flagged not found in the input, and the head and merge-base it cites equal the body's.
4. **Minor, no cell pins the unbounded growth:** true but weak. It is piece 2's scope and the body states it.
5. **Minor, eslint comparison unsupported:** fair as a wording note. The error is in an untouched file; I did not run eslint.
6. **Notes:** ticket text missing; "piece 1 of 2" unverifiable.

**Recall against this gate's findings:**
- G335-2212-1 (the actual Major): missed.
- G335-2212-2: missed.
- G335-2212-3: partial (Minor 1).
- G335-2212-4 and G335-2212-5: missed.

**False positives:** 3 (Majors 1 to 3).

## Findings

- **G335-2212-1 (Major, introduced by this diff, measured): `this.eventBuffer.unshift(...failed)` throws a RangeError once about 125,000 events fail in one flush, and then every buffered audit event is lost and the process can exit.**
  - **The mechanism:** spread arguments are bounded by the stack. On Node v26.8.1 the call is fine at 120,000 and throws at 125,000.
  - **What is lost:** `this.eventBuffer` was emptied at line 316 and `failed` is a local, so on the throw the whole backlog is gone.
  - **How it surfaces:** `flush()` rejects.
    - From `log()` (when the buffer is at `maxBatchSize` or more) the caller's audit call rejects.
    - From the interval timer, the rejection is unhandled, and the process exits 1 with no listener (measured).
  - **Develop at the same sizes** (130,000 and 200,000): resolved, every event kept, no exit.
  - **When it fires:** only after a sustained sink outage has built the backlog, which is the situation an audit buffer exists for. The PR's stated goal is "a throwing logger can no longer lose events".
  - **Fix (one line):** a reverse loop `for (let i = failed.length - 1; i >= 0; i--) this.eventBuffer.unshift(failed[i]);` or `this.eventBuffer = failed.concat(this.eventBuffer);`. Either keeps the oldest-first order and has no argument limit.
  - **Plus one cell:** for example 200,000 failing events retained with no rejection.
  - **Why Major and not lower:** it is a new loss-of-all-events and process-exit path in a tier-1 audit surface, measured at both builds. The one mitigating fact is G335-2212-2.
- **G335-2212-2 (Minor, pre-existing, scope fact; affects how the change is described): no production code uses this AuditLogger.**
  - Zero importers of `packages/shared/src/security/audit-logger.ts` outside its own two tests (Q6, with controls).
  - The services' live audit logger is `services/shared/src/security/audit.ts`, a different class with no buffer or flush.
  - So the commission's framing ("the audit trail every service writes through") and the body's "every service imports … each image would need a rebuild for the change to run anywhere" overstate reach. Today the change, and G335-2212-1, are latent.
  - Recommend the body say so, and the board decide whether the module should be wired in or retired. That decision is not this PR's to make.
- **G335-2212-3 (Note, measured): with both the sink and the logger failing persistently, the backlog now grows silently.**
  - At develop it was dropped on the first flush. Neither build logs anything in that state.
  - The empty catch is the only new swallow, and it never hides an event.
  - The infinite retry with no backoff, the unbounded growth, and the per-`log()` full-backlog flush at 100 or more events are all pre-existing. They are piece 2's ground.
- **G335-2212-4 (Note, measured): the hash chain is unchanged in semantics, and only partly fixed in delivery order.**
  - Hashes are made at `log()` and are never recomputed. `previousHash` is not carried on the event.
  - At head, retries are in chain order only when every event of the flush failed. With a success between failures, delivery is B, A, C, which is 0/3 verifiable in delivery order. That is the PR's own R2 expectation.
  - Two overlapping flushes (timer plus log-triggered) can also put a later event before an earlier one: X, A at both builds (`out/probe_overlap.jsonl`), so this is pre-existing.
  - The test header's claim about the chain should be read in that light.
  - No consumer verifies the chain (`previousHash` appears only in the source file).
- **G335-2212-5 (Note, test gap):**
  - M6 (failed events appended at the BACK of the buffer) survives. No cell logs an event during a flush, so the "ahead of anything logged during the flush" sentence in the body is unpinned.
  - No cell runs with `hashIntegrity: true`.
  - No cell covers a large backlog (G335-2212-1).
  - M2 survives, but it is equivalent.
- **G335-2212-6 (Info, gate conduct):**
  - node_modules is symlinked from gate 313's r2 install.
  - Node 26 (not LTS).
  - The probes used esbuild bundles of the source with a stub logger, not the vitest harness.
  - The test-file tsc needed `typeRoots` because of the symlink.
  - No planted tsc error.
  - The Spark work dir was in the session scratchpad.
  - load1 briefly exceeded 8 between runs; every suite run started below 8.

One Major (introduced, one-line fix), one Minor (pre-existing scope), three Notes. Round 2 needs: the spread replaced, one large-backlog cell, and the body's reach sentence corrected.

## NOT TESTED

- Node 24 (LTS), where the spread limit may differ.
- The RangeError threshold under other `--stack-size` values or other V8 builds.
- A real audit sink or a real `logger` module. The vitest runs use the stand-in; the probes use a stub.
- Memory or OOM behaviour of the unbounded buffer at either build.
- The suites of any service, since none imports the module.
- The four platform suites, eslint, docs-fragments, `npm run audit:gate`, and the pre-push hook and its legs.
- A fresh `npm ci` at the head.
- The merged tree e14f33a5 through the suite. Develop's move is services/auth only.
- The Linear KS-1923 ticket text and the seat's comment 884487b2 (not read).
- The seat's worktree `worktrees/s-r110-ks1923`. My evidence is the pushed head.
