## QA GATE 61, TIER 1, DELTA: KS-1384 R1 round 2, #1868
(Opus, Sun 1 Nov 2026, commissioned by Wednesday. Findings only: nothing was fixed, pushed, commented, approved or merged, and nothing was written to GitHub or Linear. Evidence is in `evidence/`, scripts in `scripts/`.)

**BLUF: NO GO, on one narrow finding that a cheap change can fix.** Round 2 closes G58-F1 as claimed. With the takeover race reproduced on real Postgres, round 1 (13fdd7f3) pays **2 fees** in all three race shapes, and the head pays **1**. The new re-check kills MR3 (the token conjunct dropped): W's t1b kills it, and so do my P1b and P1c. **But round 2 opens a new double-fee path through the 10 s POST timeout (G61-F1).** Take a POST that anchoring accepts but answers slowly (more than 10 s and less than Node's default ~300 s). Round 1 waits, learns the anchorId, and pays **once**. The head aborts at 10 s, keeps the claim, and answers 503 with **Retry-After 600**. By then the landed anchor has confirmed (the route's own comment puts that at ~30-60 s), and a `confirmed` row reads as "nothing in flight" (G58-F2, still open). So the retry the 503 tells the client to make pays a **second fee**. Measured: P3b and P3c pay 1 at base and 2 at the head. That is a path that pays more at the head than at the base, on the money path, in the round whose purpose is "never pays twice". The PR's own comment says such a retry "reads anchoring's row in flight and is refused". That holds only while the row is unconfirmed. Everything else holds:
- W's 20 real-Postgres cells pass under the app role with RLS on.
- The unit suite is 1904/1904.
- **15 of my 16 mutants** are killed. The survivor is the tenant conjunct, an expected equivalent under random tokens; see Q4.
- The delta touches only what it says.

Separately, the PR **does not merge cleanly onto current develop** (7 conflicts, all from F-a's lineage, none in the delta): G61-F2.

- PR https://github.com/Secuura/Distributed_Secuura/pull/1868 · KS-1384 R1 round 2 · author Seat W 14th
- **Heads at START** (2026-10-31T13:11:29Z, i.e. Sun 1 Nov 00:11 AEDT, `git ls-remote`): `refs/pull/1868/head` = `a46c251e1419d48bb8a50519e7ee0e306ad2fbe1`, develop = `bf6a43631df1e9c1cd6935a0e63ad74c62a0b48c` (`evidence/lsremote_start.txt`)
- **Heads at END** (2026-10-31T14:04:47Z, i.e. 01:04 AEDT): `refs/pull/1868/head` = `a46c251e1419d48bb8a50519e7ee0e306ad2fbe1`, **unchanged**. develop **moved** to `1ae193f79a124cadfa7c2a3ce72fe1ae76305af0` (KS-1788 #1827). That move touches none of the three product files. Re-merged against it: the same 7 conflicts (`evidence/lsremote_end.txt`, `evidence/merge_tree_develop_end.txt`).
- Gated head of round 1: `13fdd7f31f22` (gate 58). Delta: `13fdd7f31f22..a46c251e1419`, one commit, 10 files, +533/-2 (`evidence/delta_namestatus.txt`).
- Clone: `0_Brain/reference/2026-11-01_gate61-r1r2-1868/repo`, created new (the path did not exist). It is `--shared --no-checkout` from gate 59's clone and made a blob:none promisor. `git rev-parse --show-toplevel` equalled the clone directory before every fetch and write. The push URL is `no_push_qa_gate`.
- Host: Apple Silicon Mac, **Node v26.8.1 (not LTS)**, jest 29.7.0, PostgreSQL 15 (container `gate61-pg`, the repo's `docker/init` plus `scripts/run-migrations.sh`: applied=57 failed=0).

## VERDICT: NO GO
Fix-before-merge: **G61-F1** only. It is a small change in the retry route's timeout branch; the fix shapes are below. If Wednesday rules instead that R2a's G58-F2 fix covers it, the condition is that R2a's gate runs P3b and P3c (cells in `evidence/probe/`) and both pay once. In that case the merge could be GO WITH NOTES, but R1 must not deploy without R2a.

## FINDINGS
**G61-F1 · MAJOR · fix-before-merge (documents.ts:1637-1641 with reanchorInFlight.ts IN_FLIGHT_STATUSES). A POST that times out but landed pays a second fee on the retry its own 503 asks for. Round 1 paid once.**
- **Mechanism, by reading:**
  - anchoring `POST /api/anchors` persists the row, then calls `processAnchor` (the fee) without awaiting it, then answers 202 (anchoring index.ts:529, :577, :581).
  - So a POST answered after 10 s is a slow row write. Anchoring finishes it after originate has aborted.
  - At the head, the timeout branch keeps the claim and answers 503 with `Retry-After: 600` (= REANCHOR_CLAIM_TTL_MS). It writes no anchorId, so the blob stays `anchor_failed`.
  - A retry at or after 600 s takes over the stale claim and reads anchoring. The row is `confirmed` by then, and `IN_FLIGHT_STATUSES` (pending/submitting/submitted) calls that ABSENT (G58-F2). The re-check passes because it is the retry's own fresh claim, so the retry POSTs.
  - anchoring's `ON CONFLICT (document_id, network)` upsert resets the confirmed row and submits again (gate 58, by reading).
- **Measured (probe on real Postgres, app role; `evidence/probe_head_app.log`, `evidence/probe_base_13fd_app.log`).** The fake writes the row first and answers 202 at 12 s.

| Cell | 13fdd7f3 (round 1) | a46c251e (head) |
|---|---|---|
| P3a slow POST; row still in flight after the lease | A 202 at 12.0 s, blob names the anchorId; B 400, C 400; **1 POST** | A 503 at 10.0 s, Retry-After 600, claim kept; B 409; after the lease C 409 (in flight); **1 POST** |
| **P3b** slow POST that landed; the row confirms inside the lease; retry after the lease | A 202, anchorId learnt; C 400; **1 POST** | A 503, Retry-After 600; B 409; after the lease **C 202: 2 POSTs** |
| **P3c** 202 headers sent, body stalls 12 s (anchoring ACCEPTED); confirms; retry after the lease | A 202; C 400; **1 POST** | A 503 at 10.0 s (the abort fires during `anchorResp.json()`, so a 202 that was received is thrown away); after the lease **C 202: 2 POSTs** |
| P3d POST never answers | A hangs until the test's 60 s timeout (no bound) | A 503 at 10.0 s; B 409; claim kept, same token; 1 POST |

- **Why it is the delta's:**
  - At round 1 the same slow POST eventually succeeds: Node's fetch waits up to its ~300 s header default.
  - The blob learns the anchorId, so every later retry gets 400.
  - The head converts the whole 10-300 s band into "unknown outcome". Its only safety net is the in-flight read, and that net has the G58-F2 hole exactly when the anchor has succeeded.
  - `Retry-After: 600` points well-behaved clients at that moment.
- **The PR's claim is contradicted.** The route comment (:1634-1635) and the flow fragment ("after them, the in-flight read sees anchoring's row") are true only while the row is unconfirmed. W's t7 never steps past the lease, and its fake writes the row only when the held POST is released, so it cannot see this.
- **Fix shapes, W's choice:**
  - (a) On the timeout path, record the unknown outcome on the blob, for example `retryPostUnknownAt` kept with the claim. Then make the next claimant treat any anchoring row for the document as landed (409, or heal to that row), `confirmed` included, so it never POSTs.
  - (b) Narrower: in `decideInFlight`, a `confirmed` row is not ABSENT when the blob carries a claim that timed out. This is the G58-F2 fix scoped to this branch.
  - (c) A mitigation only, not a fix: raise REANCHOR_POST_TIMEOUT_MS toward the lease (for example 5 min, so the bounded read plus POST stays well under 10 min). That shrinks the band back toward round 1's.
- **Pin:** P3b and P3c in `evidence/probe/gate61-r1r2-probe.integration.test.ts`.

**G61-F2 · MINOR for this gate, train-level · the PR head does not merge cleanly onto develop bf6a4363.**
- `git merge-tree --write-tree bf6a4363 a46c251e` gives rc 1 with **7 conflicts** (`evidence/merge_tree_develop.txt`):
  - anchoring `index.ts`, `reconciler.ts`, `anchorSubmission.ts` and `anchorStatusUpdate.ts`;
  - two ks1384-fa anchoring tests (add/add);
  - originate `ks1293-originate-suite-is-hermetic.test.ts`.
- Cause: develop's bf6a4363 is **F-a #1838**, merged at 23:51 AEDT on 10-31, after W's 22:49 commit. The PR stack carries its own pre-merge F-a lineage.
- Round 1's head 13fdd7f3 conflicts identically (7, `evidence/merge_tree_develop_r1head.txt`).
- **None of the 10 delta files** is among develop's 344 changed files since the merge-base dc8c210c. The train needs a rebase or merge onto develop before it lands. That is not R1r2's defect.

**G61-F3 · NOTE, not a regression (documentRepo.ts confirmReanchorClaim WHERE). The re-check has no status guard.** Claim refuses `revoked`/`deleted` rows, and the outcome write refuses a `confirmed` blob. The re-check, the last statement before the fee, checks only the token and the lease.
- **Measured (P5):** a revoke lands while the holder is in its in-flight read, then the read answers 404. The result is **1 POST** at both base and head: a fee spent on a revoked document. The document stays `revoked`, because the outcome write preserves terminal states.
- Adding `AND status NOT IN ('revoked','deleted')` and a not-`confirmed` blob condition to the re-check would close it at no cost.

**G61-F4 · NOTE (claims accuracy).**
- (i) "6 red at 13fdd7f31f22" for the real-Postgres file **reproduces exactly**: t1, t1b, t4, t5, t6 and t7 red; the controls t2 and t3 green.
- (ii) "5 of the 6 unit cells red at 13fdd7f31f22" **cannot be reproduced cell by cell**. At 13fdd7f3 product code the unit file does not compile (TS2339: `REANCHOR_READ_TIMEOUT_MS`/`REANCHOR_POST_TIMEOUT_MS` do not exist), so jest collects 0 tests (`evidence/w_unit_retry_route_at_base_13fd.log`). UNVERIFIED as stated.
- (iii) The test header's remark that in (t1) "the lease conjunct alone refuses A" is not quite right. B's outcome write drops BOTH claim keys, so in t1 the token conjunct (NULL ≠ token) and the lease conjunct (NULL) both refuse A. That is why MR3 survives t1 and needs t1b. It is also why my M2, the lease neutralised, survives t1 and P1a and is caught only by t4.

## Q1. G58-F1 re-check: can two POSTs happen at the head?
**No, in every takeover shape I could build.** Real router, documentRepo and db layer on real Postgres, app role `secuura_app` with RLS on and the tenant GUC bound. Anchoring is a real loopback fake that counts POSTs on arrival.

| Cell | 13fdd7f3 | head a46c251e |
|---|---|---|
| P1a Q2a-stale, gate 58 verbatim (A held in its read; claim backdated 11 min; B takes over and POSTs; A's read answers the pre-B 404) | **2 POSTs**, A 202, B 202 | **1 POST**, A 409, B 202 |
| P1b the same, but B's POST is still in flight (held) when A re-checks | **2 POSTs** | **1 POST**, A 409 |
| P1c B has taken the claim but is itself still in its read when A re-checks | **2 POSTs** | **1 POST**, A 409, then B 202 |
| P1d control, no backdate | 1 POST, B 409 | 1 POST, B 409 |
| P1e ten parallel retries against a stale claim | 1 POST | 1 POST |

- W's own t1-t7 are green at the head (8/8), and 6/8 are red at round 1 as claimed (`evidence/w_r1r2_integ_at_base_13fd.log`).
- **Residuals, stated by W and not closed:**
  - A process frozen for longer than the lease between the re-check's commit and the POST leaving the socket.
  - A re-check UPDATE that waits more than ~10 min on a lock or a DB stall. `refreshedAt` is computed before the statement is sent, so it is stale-dated on commit.
  - Both clocks are the app's `new Date()`, not the DB's `NOW()`, so replica clock skew counts against the lease. It would need a skew of about 9m50s to matter. Not measured.

## Q2. The t1b gap: does round 2 kill MR3?
- Gate 58's Q6 has no "MR3" (its mutants are M1-M6).
- The t1b gap is W's own: per the flow fragment, "the token mutant's first valid form survived the 7-cell file, which is how (t1b) was found and added".
- I applied MR3 as **G61-M1** (confirm's `->>'retryClaim' = ${token}` replaced with `${token}::text IS NOT NULL`, which keeps the parameter used).
- Result: **KILLED.** In W's real-Postgres file only **(t1b)** "the takeover's POST is still in flight when A re-checks" goes red, as W says. My P1b and P1c also go red. W's unit file (19) does not kill it, since it mocks the SQL.

## Q3. The 10 s POST-timeout path
- **Code path** (documents.ts:1588-1641): `fetch(..., { signal: AbortSignal.timeout(REANCHOR_POST_TIMEOUT_MS) })` → `catch` → `isTimeoutError` (name `TimeoutError` or `AbortError`) → a warn log, `Retry-After: 600`, 503. There is no `release`, no `writeReanchorOutcome` and no poller. The claim stays with A's token and A's refreshed `retryClaimedAt`.
- **Inside the lease: proved.** No retry pays a second fee:
  - W's t7: an immediate retry gets 409, 1 POST.
  - My P3a and P3d: B 409, the claim kept with the same token, 1 POST.
  - Mutants M8 (release on timeout), M9 (timeout sent down R1's failure path), M10 (signal removed) and M14 (TimeoutError not recognised) are each killed.
- **After the lease: NOT proved, and refuted when the outcome was a success that confirmed.** See G61-F1 (P3b, P3c: 2 POSTs at the head, 1 at round 1).
- **The abort also covers the body read.** A 202 whose body stalls is treated as unknown (P3c: 503 at 10.0 s).

## Q4. My own mutants (`scripts/mutants.py`, `evidence/mut/`, `evidence/mutants_run.log`)
- **Method:**
  - Each mutant is a set of edits, and every anchor is asserted unique (count == 1).
  - Each run covers W's real-Postgres file (8), W's unit file (19) and my probe (10).
  - Scoring is per cell against the unmutated baseline. The baseline is 8/8, 19/19, and probe 7/10: P3b, P3c and P5 are red there and are never counted as kills.
  - Each mutant is restored with `git show a46c251e:<file>` and the sha256 is checked against the head blob after every mutant.

| # | Mutant | W real-Postgres (8) | W unit (19) | Gate 61 probe (10) | Result |
|---|---|---|---|---|---|
| G61-M1 | (=MR3) confirm: token conjunct dropped | killed (1): (t1b) | survives | killed (2): P1b; P1c | **KILLED** |
| G61-M2 | confirm: lease conjunct neutralised (lease effectively 100 years) | killed (1): (t4) | survives | survives | **KILLED** |
| G61-M3 | confirm: lease boundary doubled (20 min) | killed (1): (t4) | survives | survives | **KILLED** |
| G61-M4 | confirm: lease NOT renewed (both copies keep the old retryClaimedAt) | killed (1): (t5) | survives | survives | **KILLED** |
| G61-M5 | confirm: lease renewed in metadata only, not the authoritative certification_metadata copy | killed (1): (t5) | survives | survives | **KILLED** |
| G61-M6 | route: re-check result ignored | killed (3): (t1); (t1b); (t4) | killed (1): (t9) | killed (3): P1a; P1b; P1c | **KILLED** |
| G61-M7 | route: re-check moved BEFORE the in-flight read | killed (4): (t1); (t1b); (t4); (t5) | killed (2): (t9); (t9) | killed (3): P1a; P1b; P1c | **KILLED** |
| G61-M8 | route: a timed-out POST releases the claim | killed (1): (t7) | killed (2): (t10); (t10) | killed (1): P3d | **KILLED** |
| G61-M9 | route: a timed-out POST goes down R1's failure path | killed (1): (t7) | killed (2): (t10); (t10) | killed (1): P3d | **KILLED** |
| G61-M10 | route: the POST's signal removed | killed (1): (t7) | killed (1): (t8) | killed (1): P3d | **KILLED** |
| G61-M11 | route: timed-out POST answers Retry-After 60 (inside the lease) | killed (1): (t7) | killed (2): (t10); (t10) | survives | **KILLED** |
| G61-M12 | route: re-check failure does not release | killed (1): (t4) | killed (1): (t9) | survives | **KILLED** |
| G61-M13 | in-flight read: signal removed | killed (1): (t6) | killed (1): (t8) | survives | **KILLED** |
| G61-M14 | isTimeoutError: TimeoutError not recognised | killed (1): (t7) | killed (2): (t10); (t10) | killed (1): P3d | **KILLED** |
| G61-M15 | POST timeout 11 min (longer than the lease) | killed (1): (t7), on the re-run (`evidence/mutants_rerun_M15.log`); run 1 lost `beforeAll` to the 30 s hook timeout, which turned all 8 red, so it is not counted | killed (1): (t8) | killed (1): P3d | **KILLED** |
| G61-M16 | confirm: tenant conjunct dropped | survives | survives | survives | **SURVIVED** |

**15/16 killed.**
- **G61-M16** (the re-check's tenant conjunct dropped) survives everywhere. That is expected: the token is a random UUID, so tenant plus token is never needed beyond the token, and W says no kill is claimed for it. The tenant conjunct is defence in depth.
- **Thin spots:**
  - M2 (lease neutralised) and M3 (lease doubled) are each killed by **(t4) alone**, since my probe cells all involve a takeover, which the token catches.
  - M4 and M5 (no renewal) are killed by **(t5) alone**.
  - W's unit file kills none of M1-M5, as expected for SQL mutants under a SQL mock.
- **Harness note:** W's real-Postgres file lost `beforeAll` (initDb) to the 30 s hook timeout once in 20 runs here. W saw it too. It is a flake source, but it never produced a false green.

## Q5. Scope and merge
- **Scope: clean.** 10 files: three product files (documentRepo.ts +36, documents.ts +30/-2 in the retry route only, reanchorInFlight.ts +19/-1), one new real-Postgres test, the retry-route unit file (+114), and three test adapters (ks1385, ks1814, ks520: `confirmReanchorClaim` added to the repo mock, +3 each). There are also two doc fragments.
- This matches the commit message. No other route is touched, and no assertion in an existing test is weakened.
- **Merge onto develop bf6a4363: NOT clean** (G61-F2). That comes from the train, not the delta.

## Q6. Node
Everything ran on **Node v26.8.1, which is not an LTS line**. Node 24 LTS: **UNMEASURED.** The timeout semantics depend on it: `AbortSignal.timeout` rejects with a `TimeoutError` DOMException, and undici's defaults apply.

## COUNTS (Node v26.8.1, not LTS)
- Install: `npm ci --ignore-scripts` at Blockchain/Dev (1795 packages, rc 0), then the `@secuura/shared` build (rc 0) and the originate Prisma generate (rc 0).
- **Originate unit (jest, head):** 155/155 suites, **1904/1904**, rc 0 (`evidence/unit_head_full.log`). Matches W.
- **W's real-Postgres cells, head, app role:** ks1384-r1r2-stale-claimant 8 + ks1384-r1-reanchor-claim 12 = **20/20** (`evidence/w_integ_r1r2_head_app.log`). Matches W.
- **W's r1r2 file at round-1 product code:** 6 failed / 2 passed (t1, t1b, t4, t5, t6, t7 red; t2, t3 green). Matches W.
- **W's unit retry-route file at round-1 product code:** does not compile (0 collected). See G61-F4.
- **My probe:** head 7/10, the reds being P3b and P3c (G61-F1) and P5 (G61-F3). Round 1: 5/10, the reds being P1a, P1b, P1c (G58-F1), P3d (hangs: no bound) and P5.
- **tsc** (`-p services/originate/tsconfig.json --noEmit`, product files; that tsconfig excludes tests): **0 errors**, rc 0. Positive control: a planted TS2322 gives rc 2 (`evidence/tsc_head.log`, `evidence/tsc_control.log`). W's "tsc with all 179 test files" was not re-run in that form.

## SPARK SHADOW AND CALIBRATION
- **spark_gate.sh** (`2_Project_Files/local-model/gate/spark_gate.sh`; the brief's `fleet/spark_gate.sh` does not exist). Run as `… repo 1868 a46c251e… 13fdd7f3… ks1384-r1-retry-route.test.ts --node-modules <clone>/Blockchain/Dev/node_modules --work <scratchpad>/gate61_spark --out evidence/spark/facts`: rc 0 in 34 s.
- **No npm-workspace hoisting break this time.** The head run of the unit file was 19/19 (true).
- **The base-side instrument fault from gates 48, 49, 57 and 58 recurs**: "merge-base (empty) · diff 0 files", BASE 19/19. The truth is that the file does not compile at base.
- **Root cause found:**
  - `shadow_facts.py:27` runs `git merge-base <head> origin/<base-ref>`. When base-ref is a sha, `origin/<sha>` does not resolve, so `mb` is empty.
  - The diff is therefore empty and `prod` is empty, so no product file is swapped back and "BASE" is the head.
  - It also overwrites spark_gate's correct `diff.patch` with an empty one (`evidence/spark/facts/diff.patch`, 0 bytes).
  - spark_gate.sh itself resolves a sha base correctly (it falls back to `<ref>^{commit}`). shadow_facts.py does not.
- **spark_review.py:**
  - Inputs: the clean 13fd..a46c patch (`evidence/spark/delta_13fd_a46c.patch`), the commit message as the PR body (the PR body itself was not readable from this seat), and `--linear-env /dev/null` (ticket text unavailable).
  - Result: rc 0, verdict **NO GO** (`evidence/spark/review/review.json`).

| Spark finding | Gate 61 | Calibration |
|---|---|---|
| Major: confirmReanchorClaim can update rows "created by other processes or humans" (no test-only filter) | The tenant- and token-scoped product SQL is correct; a random-UUID token cannot be matched by accident | **False** |
| Major: the root cause is "inferred from code reading, not measured" | Measured twice: gate 58 Q2a-stale, and my P1a-c at 13fdd7f3, 2 POSTs each | **False** |
| Major: the unit file passes 19/19 on base, contradicting the red-first claim | Produced by the instrument fault; the truth is that it does not compile at base, and the real-Postgres file is 6/8 red | Instrument-true (and close to G61-F4 ii by accident) |
| Major: t8 checks only that the mock fetch received the signal | True of t8; real enforcement is t6 and t7 on real Postgres, green, and M10, M13 and M15 are killed by them | Partial / noise |
| Minor: the integration file is not run by the runner | True of the facts it was given; I ran it (8/8, 6/8 red at base) | Instrument-true |
| Minor: tsc and eslint unmeasured in facts | True of the facts; tsc measured here | Instrument-true |
| Note: t8 checks the values, not enforcement | Same as above | Noise |
| Verdict NO GO | NO GO | **Agrees, for the wrong reasons** |

- Score: 0 true, 1 partial, 3 instrument-true, 3 false or noise.
- **It missed G61-F1** (the timeout double fee, the reason for this verdict), G61-F2 (develop conflicts) and G61-F3 (no status guard).
- The verdicts agree by coincidence.

## UNMEASURED
- The real anchoring service. That its POST finishes and spends the fee after the client aborts, and that its upsert re-submits a confirmed row, are both established by reading only. Real POST latencies are also unmeasured.
- Real Cardano confirmation times. The probe sets the row `confirmed` by hand.
- Real stall lengths. Lease expiry is forced by backdating `retryClaimedAt`, as gate 58 and W did.
- Two originate processes, clock skew between replicas, and a re-check UPDATE stalled on a lock for minutes.
- Node 24 LTS.
- eslint, check:openapi, the docs-fragments check, the four platform suites, a running stack, any chain or box.
- W's own 10 mutants. I do not have them; I ran 16 of my own, and MR3 is the same edit as W's token mutant.
- The PR body and GitHub base branch. `gh` under the Blockchain project's config is not authenticated (`evidence/pr1868.err`; `evidence/pr1868.json` is an empty leftover from that attempt). W's claims are quoted from the commit message and the two fragments instead.
- The merged tree's test suite (the merge does not apply cleanly).
- R2 and R2a.

## HOW
- **Fetch:** `git ls-remote` with the Blockchain deploy key at START and END. The clone is new, under this gate folder, `--shared` from gate 59's clone. It was made a promisor (blob:none), because the first fetch failed "pack has 14 unresolved deltas" without that. The PR head and develop were fetched into `refs/gate/*`. Toplevel was asserted before every fetch and write.
- **DB:** container `gate61-pg` (postgres:15-alpine, loopback-only random port, passwords generated per run and kept in the scratchpad, never in evidence). Migrations ran inside the container with the repo's runner (`evidence/migrate.log`; a check confirmed the password does not appear in the log).
- **Jest:** `scripts/jest_run.sh` (superuser for seeding; the router under `secuura_app`). Logs are scrubbed of both passwords.
- **Base runs:** `scripts/swap_base_run.sh` swaps the three product files to 13fdd7f3 in my clone, runs the jobs, restores from `git show a46c251e:` and checks sha256 (`evidence/head_product.sha256`: all OK).
- **Probe:** `evidence/probe/gate61-r1r2-probe.integration.test.ts`, copied into `src/__tests__` only for its runs and removed before teardown.
- **Hygiene:** no git write verb was run in !CODING, and W's `s-w13-pg` was not touched and is still running. `gate61-pg` was stopped and removed by its recorded container ID (`7ad7ce00e075…`). Spark's worktree was removed with `git worktree remove`. The probe was moved out of the clone, kept as `evidence/probe/*.ran` and byte-identical (cmp rc 0). The clone is clean (`git status` empty) at the head and is **kept** (deletes are refused here; gate 59 kept its clone too). No process with this gate's paths is left. The secret scan of evidence, scripts and verdict for both generated passwords and the compose default found none; the positive control `secuura_app` matched.

**Heads at END:** PR `a46c251e1419d48bb8a50519e7ee0e306ad2fbe1` (unchanged) · develop `1ae193f79a124cadfa7c2a3ce72fe1ae76305af0` (moved from bf6a4363 during the gate; 7 conflicts against it too).
