## QA GATE 65, TIER 1, DELTA: KS-1384 R1 round 3, #1868
(Opus, Sun 1 Nov 2026, commissioned by Wednesday. Findings only: nothing was fixed, pushed, commented, approved or merged, and nothing was written to GitHub or Linear. Evidence is in `evidence/`, scripts in `scripts/`.)

**BLUF: GO WITH NOTES.** Round 3 closes G61-F1 and G61-F3 as claimed, measured on real Postgres under the app role:
- Gate 61's P3b and P3c pay **2 fees at a46c251e and 1 at the head**. P3a and P3d pay 1 at both.
- Gate 61's P5 (a revoke during the read) pays **1 at the base and 0 at the head**. My P5b (deleted) gives the same result.
- **No new double-pay path is opened** by the m5 claim edge, the marker clear, the m7 path or the 25 s budget, in every interleaving I built. That includes five claimants of an m5 blob queued on one row lock (5 distinct waiters, then 1 POST).
- W's 14 + 8 + 12 real-Postgres cells pass (34/34), and 11 of the 14 new ones are red at a46c251e as claimed. The unit suite is 1918/1918. tsc is clean with every test file.
- MUTANTS_SUMMARY

What is not clean:
- **One new liveness regression (G65-F1, MINOR).** A blob-less document that goes through a marker cycle and then has a failed POST in production is left as a bare `{status:'pending'}` blob, which no claim can take: 409 for ever. Round 2 left the same document retryable (measured: base D 202, head D/E 409).
- **W's residual list is accurate but incomplete (G65-F2, NOTE).** Every one of the following pays a second fee at the head, and identically at the base, so none is a regression:
  - A holder that **dies** between its POST and the mark. That needs no 10-minute freeze, only a restart during a POST window of 20 s at most.
  - A **non-2xx from an intermediary** after anchoring persisted.
  - Anchoring's **fail-open 404 (G58-F3)**, which the marker's clear trusts as "no row".
- **The m7 cell's "later writer" preserves the marker (G65-F3, NOTE).** The repo's actual anchor_failed writer, `markDocumentAnchorFailed`, replaces the blob and drops it. In-repo it is latent, because no caller reaches an anchorId-less blob.
- **Claims nits (G65-F4).**

The develop conflicts are unchanged: still 7, none of them in the delta (train-level, G61-F2).

- PR https://github.com/Secuura/Distributed_Secuura/pull/1868 · KS-1384 R1 round 3 · author Seat W 14th
- **Heads at START** (2026-10-31T17:36:51Z, i.e. Sun 1 Nov 04:36 AEDT, `git ls-remote`): `refs/pull/1868/head` = `7ed460cc4258d7aee16f9f65ca150d50b22ed453`, develop = `32e8fe25cb24e8357605a693b01050e51c3d4007` (`evidence/lsremote_start.txt`).
- **Heads at END:** see the last line.
- Gated round-2 head: `a46c251e1419` (gate 61, NO GO). Delta: `a46c251e1419..7ed460cc4258`, one commit, 11 files, **+1012/-78**, matching the brief (`evidence/delta_stat.txt`, `evidence/delta_namestatus.txt`).
- Clone: `0_Brain/reference/2026-11-01_gate65-r1r3-1868/repo`, created new (the path did not exist). It is `--shared --no-checkout` from gate 61's clone, made a blob:none promisor with the Blockchain deploy key as its `core.sshCommand`. `git rev-parse --show-toplevel` equalled the clone directory before every fetch and write. The push URL is `no_push_qa_gate`.
- Host: Apple Silicon Mac, **Node v26.8.1 (not LTS)**, jest 29.7.0, PostgreSQL 15 (own container `gate65-pg`, ID `7096e55edb12…`, the repo's `docker/init` plus `scripts/run-migrations.sh`: applied=57 failed=0, `evidence/migrate.log`).
- The PR body is **not readable** from this seat: `gh` under the Blockchain project's config is not authenticated (`evidence/pr1868.err`). W's claims are quoted from the commit message (`evidence/commit_msg.txt`) and the two round-3 fragments, which carry the residual list verbatim.

## VERDICT: GO WITH NOTES
- **Nothing is fix-before-merge.** No path pays more at the head than at a46c251e. Every money cell the delta targets goes from 2 (or 1) fees to 1 (or 0).
- Conditions, by Wednesday's ruling:
  - (a) G65-F1 (the wedge) is fixed in a round 4 or carried as a named R2b item. It is liveness only, and it is new in this round.
  - (b) **G58-F3 (anchoring's fail-open 404) joins the deploy hold.** The W fragment's hold names F0, F-b, R2a and R2b, not G58-F3. Round 3 makes the 404 the *only* thing that clears a maybe-landed marker (G65-F2 iii).
  - (c) R2a's gate re-runs my R3-crash and R4-502 cells (in `evidence/probe/`); both must pay once.
  - The train still needs its develop rebase (G61-F2).

## FINDINGS
**G65-F1 · MINOR · new in round 3, liveness (documentRepo markReanchorPostUnknown + releaseReanchorClaim + claimDocumentForReanchor). After a marker cycle, a blob-less document whose next POST fails in production is wedged at 409 for ever.**
- **Mechanism:**
  1. The mark drops `retryClaimMadeBlob`.
  2. A later claimant reads "no row". Its re-check removes the marker, and it POSTs.
  3. If that POST ends on R1's failure path in production (anchoring 5xx or 4xx, a refused connection), the route releases.
  4. The release no longer deletes the claim-made blob, because the flag is gone. It strips the claim keys and leaves `{status:'pending'}` with no anchorId, no claim and no marker.
  5. The claim's pending disjunct needs `retryClaim` or the marker, so nothing can claim it. The route's JS check lets it through as `wedgedPending`, and every retry gets **409 for ever**.
- This is gate 58's N1 shape ("no writer found"). Round 3 is that writer.
- **Measured** (probe `R1-wedge`; `evidence/probe_head_app.log`, `evidence/probe_base_a46c_app.log`). A's POST never persists; after the lease, C gets a 500 in production.

| | a46c251e | head |
|---|---|---|
| Blob after C | absent (released, MadeBlob) | `{"status":"pending"}` |
| Next retries | D 202, E 400 | D 409, E 409 |

- Money-safe: the document cannot be anchored at all. W's m6 pins the marker clear only on an `anchor_failed` blob, so it does not see this.
- Fix shapes, W's choice:
  - (a) The re-check, when it removes a marker from a `pending` blob with no anchorId, restores `retryClaimMadeBlob: true`. Its own POST has not happened yet, and "no row" was just read.
  - (b) Or the release treats a `pending`, anchorId-less, marker-less blob as removable.

**G65-F2 · NOTE · residuals: W's four are accurate, the list is incomplete.** Every cell below is measured. The same result at a46c251e means it is not a regression.
- **(i) W's residual 1 understates its reach.** W: "a holder frozen for longer than the lease between its post and its marker write leaves no marker". A holder that **dies** in that window (a deploy, an OOM, a container restart) also leaves no marker, and so does a mark that **throws** (a DB error gives a 500 before the 503). The window is at most ~20 s. It needs no freeze, because the kept claim simply lapses.
  - After the lease, a confirmed row reads as absent (G58-F2), and the retry POSTs.
  - `R3-crash` (claim kept, no marker, row confirmed): **1 POST at head and at base.** This is G58-F2 Q3a, still open; R2a must close it.
- **(ii) W's residual 3 covers more than "a connection reset".** Any **non-2xx answered after anchoring persisted** takes the same path: a 502/503/504 from an ingress, or anchoring crashing after `dbPersistAnchor` behind a proxy. `postReanchor` calls it `answered`, the route sends it down R1's failure path, and the re-check has already removed any marker.
  - `R4-502`: **2 POSTs at head and at base.** R2a's "landed-anchor" answer covers it only if the row has confirmed. A row still `failed` reads as absent, as before.
- **(iii) Not stated: the marker trusts the 404.** The only way a maybe-landed marker clears is anchoring answering 404 "no row". Anchoring answers exactly that 404 when its DB read fails (G58-F3, gate 58 by reading).
  - `R2-f3` (marked, row confirmed, read answers the swallowed 404): **1 POST at the head**, a second fee, where the design intends 0. At base it is 1 too.
  - Not a regression, but the marker design adds a dependency on G58-F3 and does not name it. Hence condition (b).
- **W's residual 2 is accurate, and now measured.** W: "a request that reaches anchoring and stalls there for longer than the lease before its persist commits". `Q2b-past`: A's POST is held unpersisted, A 503 and marked; after the lease C reads no row, clears and POSTs; then A persists. Result: **2 POSTs at head and at base.** The in-lease variant `Q2b-in` is **1 at the head, 2 at the base** (an improvement): the kept claim refuses the immediate retry.
- **W's residual 4 is accurate.** A marked document stays refused on any row, a failed one included (m1, my Q2a-chain: ten parallel retries, all 409). This is liveness until R2b.

**G65-F3 · NOTE · latent (anchorStateSync markDocumentAnchorFailed vs the m7 marker). The marker survives only writers that preserve unknown blob keys. The repo's own anchor_failed writer does not.**
- W's m7 simulates "a later writer marks the blob anchor_failed" with `jsonb_set` on `status`, which keeps the marker.
- The real writer, `markDocumentAnchorFailed`, replaces the blob through `updateDocument` (KS-1058: only `threadToken` is carried forward), and that drops both the marker and the claim keys.
- `Q2c-writer` (m7, then the real writer, then the confirmed row): **2 POSTs at the head**, and at base too.
- **Unreachable in-repo today.** Its only callers are the poller and the read-time reconcile, and both need a `blob.anchorId`, which an m7 blob does not have. The m7 blob itself is 400 "already anchored" (statusless, `Q2c-route`: 1 POST).
- So it is a note: any future or operator writer of an anchorId-less blob must carry `retryPostUnknown*` forward, and the cell would pin it better with the real writer.

**G65-F4 · NOTE (claims accuracy).**
- (i) The commit message says the real-Postgres file has "**13** on real Postgres"; it has **14** (the fragments say 14). The brief's 14 is right.
- (ii) Wednesday's relay of the claim that a "2xx JSON with no id is recorded as unknown on the blob" is loose. The code takes the **success** path (202, outcome written, no poller) and puts the marker into the outcome blob. The commit message and the fragment say so correctly.
- (iii) W's "11 of 14 red at a46c251e1419, three controls green" **reproduces exactly**: red u1, u2, u3, u4, u4b, m1, m3, m4, m5, m6, m7; green m2, m2b, m2c (`evidence/w_r1r3_integ_at_base_a46c.log`).
- (iv) "tsc with all **181** originate test files": I count **182** files under `src/__tests__` with my probe excluded. Both give 0 errors.
- (v) The t8 change replaces `[5000, 10000]` with `[5000]` plus "a distinct, unaborted AbortSignal". The POST's deadline values are no longer asserted in that file. The new post-deadlines file (7) covers them, and my G65-M14 is killed (see Q5).

## Q1. G61-F1: closed?
**Yes.** The probe runs on real Postgres under `secuura_app` (RLS on), with gate 61's harness and fake (row written before the answer; POSTs counted on arrival).

| Cell | a46c251e (round 2) | 7ed460cc (head) |
|---|---|---|
| P3a slow POST, row still in flight after the lease | A 503 (10.0 s), B 409, C 409; **1 POST** | A 503 (10.0 s), blob marked, claim kept; B 409, C 409; **1 POST** |
| **P3b** slow POST that LANDED, the row confirms, retry after the lease | A 503, B 409, **C 202: 2 POSTs** | A 503 marked, B 409, **C 409 (maybe-landed): 1 POST** |
| **P3c** 202 headers, body stalls 12 s, confirms, retry after the lease | A 503, **C 202: 2 POSTs** | A 503 (10.0 s, `accepted-body-lost`, marked), **C 409: 1 POST** |
| P3d POST held (never answers) | A 503, B 409, claim kept, no marker; **1 POST** | A 503, B 409, claim kept, marker set; **1 POST** |

- At head, P3c's 503 comes after 10 s of *body* wait (the 12 s stall outlasts the body deadline). With headers at 8 s and the body at 6 s, W's u3 learns the anchorId. My Q2d-a (headers 9.5 s, body +9.5 s) gives **202 at 19.0 s**, and Q2d-b (body +11 s) gives **503 marked at 19.5 s**.
- Logs: `evidence/probe_head_app.log`, `evidence/probe_base_a46c_app.log`. W's u1 and u2 agree.

## Q2. New double-pay paths opened by round 3?
- **(a) The m5 edge (a marked pending blob with no claim is claimable).** No double pay.
  - `Q2a-lock`: a locker holds `FOR UPDATE`, and **5 distinct backends** wait on the claim UPDATE (pg_stat_activity, counted by pid). The locker commits: statuses [202,409,409,409,409], **1 POST**.
  - `Q2a-par`, ten parallel retries: **1 POST**.
  - `Q2a-race`, a MARKED blob with a stale claim and ten parallel retries: **1 POST**.
  - Why: under READ COMMITTED a queued claim re-evaluates its WHERE on the winner's row. The live-claim conjunct is a separate AND, so the m5 disjunct cannot bypass it (M12 below widens exactly that and is killed).
  - `Q2a-chain`, the real path: a blob-less document gets a slow landed POST (marked), the row confirms, after the lease B gets 409 and leaves the m5 state, then ten parallel retries are all 409. **1 POST.** At base the same chain pays 2.
- **(b) Can a marker be cleared while a maybe-landed POST is in flight?**
  - Inside the lease, no. The kept claim refuses: `Q2b-in`, **1 POST** at head against 2 at base.
  - Past the lease, yes: that is W's residual 2, measured above (`Q2b-past`: 2 at both).
  - A marker written after a claimant's read makes the re-check refuse (W's m3; my G65-M8 is killed). The only clear is the re-check, and it requires the exact marker read. I found no other path that clears it early.
- **(c) After the m7 success write plus marker, can a writer flip the blob to claimable without the marker?**
  - Not in-repo. No writer reaches an anchorId-less blob. The route answers 400 on the statusless m7 blob (`Q2c-route`, 1 POST).
  - With the repo's own wholesale writer called on it: yes, 2 POSTs (G65-F3).
- **(d) The 25 s budget against the 600 s lease.**
  - The lease is refreshed by the re-check immediately before the POST. Nothing awaits between that commit and `fetch` (the body and `anchorIdentityFields` are synchronous).
  - The header timer is armed before `fetch`, and the body timer only after a 2xx. Measured worst case: 19.5 s from POST start to the mark, against a 600 s lease.
  - **No path starts a POST after the lease could be taken over**, except the residuals already stated by gate 61 and W: a freeze longer than the lease, or a re-check UPDATE stalled on a lock for more than 10 min (stale-dated `refreshedAt`). Both are unchanged.
  - The mark write itself has no deadline. A stalled or failed mark leaves no marker; that is G65-F2 (i).

## Q3. W's residuals
See G65-F2.
- Residual 1 is accurate, but its reach is wider (death or a mark error, not only a freeze longer than the lease).
- Residual 2 is accurate, and now measured (2 POSTs).
- Residual 3 is accurate, but it also covers any non-2xx after persist.
- Residual 4 is accurate.
- **Unstated:**
  - The dependency on G58-F3's fail-open 404 (measured, a second fee).
  - The G65-F1 wedge (new).
  - The marker's fragility against wholesale blob writers (G65-F3, latent).

## Q4. G61-F3
**Closed.**
- P5 (revoked during the read): **1 POST at base and 0 at head**; the head answers 409 and the document stays `revoked`.
- P5b (deleted): **1 at base, 0 at head**.
- W's u4 and u4b agree. G65-M10 and G65-M11 (status guard / confirmed guard dropped) are killed.

## Q5. My own mutants (`scripts/mutants.py`, `evidence/mut/`, `evidence/mutants_run.log`)
- **Method:**
  - Each mutant is a set of edits. Every anchor is asserted to its exact count (1, or 2 where both blob copies are edited).
  - Each run covers W's r1r3 file (14), W's r1r2 file (8), W's retry-route unit file (26), W's post-deadlines file (7) and my probe (25).
  - Scoring is per cell, keyed by the full test name, against the unmutated baseline.
    - The baseline is 14/14, 8/8, 26/26 and 7/7.
    - The probe baseline is 19/25. The six reds are Q2b-past, Q2c-writer, R1-wedge, R2-f3, R3-crash and R4-502, and they are never counted as kills.
  - After every mutant, each product file is restored with `git show 7ed460cc:<file>` and its sha256 is checked against the head blob.

MUTANT_TABLE

## Q6. Scope and merge
- **Scope: clean.** The 11 files are:
  - Three product files: documentRepo.ts (+72), documents.ts (+170/-78 around the retry route's POST only), and reanchorInFlight.ts (+84).
  - Two new test files (the r1r3 real-Postgres file and the post-deadlines unit file).
  - The retry-route unit file (+119; t8 adapted, see G65-F4 v).
  - A comment-only correction in the r1r2 test header (G61-F4 iii).
  - Four doc fragments (two new, two corrected).
- That matches the commit message. No other route is touched, and the documents.ts diff is confined to the anchor-retry handler and its imports.
- **Merge onto develop b331ffb8: NOT clean, unchanged.** `git merge-tree --write-tree` gives rc 1 with the **same 7 conflicts** as gate 61 (four anchoring sources, two ks1384-fa add/add tests, and ks1293-originate-suite-is-hermetic). Round 2's head also gives 7 against it (`evidence/merge_tree_develop.txt`, `evidence/merge_tree_develop_r2head.txt`). None of the 11 delta files is among develop's 386 changed files since the merge-base dc8c210c. Train-level, G61-F2; not counted against this round.

## Q7. Node
Everything ran on **Node v26.8.1, which is not an LTS line** (`evidence/node_version.txt`). Node 24 LTS: **UNMEASURED.** `postReanchor`'s classification depends on the runtime:
- `AbortController.abort(DOMException('TimeoutError'))` rejecting `fetch` before the headers and `resp.text()` after them;
- an undici reset being a `TypeError` (and so `failed`).

## COUNTS (Node v26.8.1, not LTS)
- **Install:** `npm ci --ignore-scripts` at Blockchain/Dev (1795 packages, rc 0), then the `@secuura/shared` build (rc 0) and the originate Prisma generate (rc 0).
- **Originate unit (jest, head, 2 workers):** 156/156 suites, **1918/1918**, rc 0 (`evidence/unit_head_full.log`). This matches W's "156 / 1918".
- **W's real-Postgres cells, head, app role:** r1r3 14 + r1r2 8 + reanchor-claim 12 = **34/34**, rc 0 (`evidence/w_integ_head_app.log`). This matches W.
- **W's r1r3 file at a46c251e product code:** 11 failed, 3 passed, as claimed.
- **My probe (25 cells):**
  - Head: 19/25. The reds are the six residual cells: Q2b-past, Q2c-writer, R1-wedge, R2-f3, R3-crash and R4-502. Each asserts the safe outcome, so a red is a measured extra fee, or the wedge.
  - a46c251e: 12/25. Additional reds: P3b, P3c, P5, P5b, Q2a-lock and Q2a-chain (2 POSTs), Q2b-in (2 POSTs), and Q2d-a (503 at 10 s, the anchorId lost).
  - At base, Q2a-lock is red because the m5 blob is not claimable (0 waiters, all 409). That is not a fee.
- **tsc:**
  - Product files (`-p services/originate/tsconfig.json --noEmit`): **0 errors**, rc 0 (`evidence/tsc_head.log`).
  - With every file under `src/` (182 test files; my probe excluded): **0 errors**, rc 0 (`evidence/tsc_head_with_tests.log`).
  - Positive control: a planted TS2322 under the same config gives rc 2 (`evidence/tsc_control.log`).

## SPARK SHADOW AND CALIBRATION
- **spark_gate.sh** with base `develop`:

  ```
  … repo 1868 7ed460cc… develop ks1384-r1-retry-route.test.ts ks1384-r1r3-post-deadlines.test.ts --node-modules <clone>/Blockchain/Dev/node_modules --work <scratchpad>/gate65_spark --out evidence/spark/facts
  ```

  - rc 0 in 65 s. Merge-base dc8c210c, so the diff is the **whole train**: 67 files, +8654/-274.
  - HEAD: 33/33 (true).
  - BASE: both files fail to compile, because `reanchorInFlight` does not exist on develop. That is true for develop, but it says nothing about the round.
  - **With a branch base, the sha-base fault of gates 48-61 does not recur**: the merge-base resolved.
- **spark_review.py** run 1, on spark's own train diff: the prompt was 1.72 M characters (diff 0.6 M plus touched files 1.1 M), and the server answered **HTTP 400** with no review (`evidence/spark/spark_review.stdout`). **This is a new instrument fault.** With base `develop`, a mid-train PR produces a prompt the Spark cannot take.
- Run 2, on the a46c..7ed4 delta (`evidence/spark/delta_a46c_7ed4.patch`), with the commit message as the PR body and `--linear-env /dev/null`: rc 0, 483 s, 361 K prompt tokens, verdict **NO GO** (`evidence/spark/review_delta/review.json`).

| Spark finding | Gate 65 | Calibration |
|---|---|---|
| Major: the mark is not token-guarded, so a stalled holder can mark a newer claimant's blob, and that claimant's re-check compares against its own read | Intended. A late mark makes that claimant's re-check refuse (W m3, my M8 killed), and that is the safe direction. The only fee case is a newer claimant that has already POSTed, which is W's residual 1 | **False** (it presents the safety property as the defect) |
| Major: with the marker, any row means 409, so a document is refused permanently | W's residual 4 (liveness until R2b), stated | Partial (true, and stated) |
| Minor: "13 on real Postgres", but the file has 14 | Same as G65-F4 (i) | **True** |
| Minor: "t8-t10 moved to round 3" is inaccurate; they were modified in place | The commit means they moved to round-3 semantics | Noise |
| Note: the r1r2 change is comment-only | True, and it is what the commit says | Noise |
| Verdict NO GO | GO WITH NOTES | **Disagrees** |

- Score: 1 true, 1 partial, 1 false, 2 noise.
- **It missed:** G65-F1 (the wedge), G65-F2 (iii) (the G58-F3 dependency), G65-F3 (the wholesale writer), the unchanged develop conflicts, and every measured residual.

## UNMEASURED
- The real anchoring service. Three things are by reading only:
  - That it persists before the fee and before the 202 (index.ts:529, :577, :581 at the head, read here and true).
  - That its upsert re-submits a confirmed row.
  - G58-F3's swallowed 404.
- Real POST latencies, ingress behaviour (which intermediary answers what, after how long), and real crash windows.
- Real Cardano confirmation. The probe sets rows `confirmed` by hand.
- Real stall lengths. Lease expiry is forced by backdating `retryClaimedAt`, as gates 58 and 61 and W did.
- Two originate processes, replica clock skew, and a re-check or mark UPDATE stalled on a lock or a DB outage for minutes.
- A mark write that throws (G65-F2 i is by reading; R3-crash seeds the post-crash state).
- Node 24 LTS.
- eslint, check:openapi, the docs-fragments check, the four platform suites, a running stack, any chain or box.
- W's 15 mutants. I do not have them; I ran 18 of my own.
- The PR body and the GitHub base branch (`gh` is unauthenticated; `evidence/pr1868.err`).
- The merged tree (the merge does not apply cleanly).
- R2a and R2b.

## HOW
- **Fetch:** `git ls-remote` with the Blockchain deploy key at START and END. The clone is new, under this gate folder, `--shared` from gate 61's clone, a promisor (blob:none) with `core.sshCommand` set to the deploy key for lazy blob fetches. The PR head and develop were fetched into `refs/gate/*`. Toplevel was asserted before every fetch and write. Spark's run fetched `origin/develop` into the same clone and added its worktree under the scratchpad.
- **DB:**
  - Container `gate65-pg` (postgres:15-alpine, loopback-only random port, `max_connections=1000`). The passwords were generated per run with `openssl rand` and kept in the scratchpad `pw.env` (0600), never in evidence. Init came from a scratch copy of the repo's `docker/init` and `docker/init-platform`.
  - Migrations ran inside the container with the repo's runner. The SU password was scrubbed from the log, with a count of 0 verified.
- **Jest:** `scripts/jest_run.sh` (superuser for seeding; the router under `secuura_app`; `nice -n 10`; waits while load1 > 16; `--runInBand` for single files, `--maxWorkers=2` for the unit suite). Logs are scrubbed of both passwords.
- **Base runs:** `scripts/swap_base_run.sh` checks the three product files against the head blobs, swaps them to a46c251e in my clone, runs the jobs, restores them from `git show 7ed460cc:` and checks sha256: all OK, restore-check rc 0, and `git status` empty for the product dirs (`evidence/swap_base_a46c.out`).
- **Probe:** `evidence/probe/gate65-r1r3-probe.integration.test.ts`, copied into `src/__tests__` only for its runs and removed before teardown. It keeps gate 61's P1a-e, P3a-d and P5, and adds P5b, Q2a-lock/par/chain/race, Q2b-in/past, Q2c-route/writer, Q2d-a/b and R1-R4.
- **Load:** load1 was 5-12 during the runs (gate 64 running alongside). No timeout-only red occurred.
- HYGIENE
