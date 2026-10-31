## QA GATE 68, TIER 1: KS-1384 R2a, #1874 (delta 7ed460cc4258...31d146678)
(Opus, Sun 1 Nov 2026, commissioned by Wednesday. Findings only. Nothing was fixed, pushed, commented, approved or merged, and nothing was written to GitHub or Linear. Evidence is in `evidence/`, scripts in `scripts/`.)

**BLUF: GO WITH NOTES.**
- **No money cell pays more at the head than at 7ed460cc.** I measured 50 cells on real Postgres under `secuura_app`: gate 65's 25, and 25 of my own with rows shaped like real anchoring's rows.
  - Every cell R2a targets goes down. R3-crash goes 1→0, R4-502 2→1, gate 58's Q3b 1→0, and gate 65's Q2c-writer (G65-F3) 2→1.
  - Every other cell is unchanged.
- **Gate 65's condition (c) is MET.** R3-crash pays once (0 more POSTs) and R4-502 pays once (1 POST in all). That holds with gate 65's probe unchanged (sha256 3be022f8…) and also with my real-shaped rows.
- **The author's 22/25 reproduces exactly.** Each of the three reds is explained correctly at source (Q1).
- **G58-F3 is real and caller-safe.** Restoring the fail-open 404 in anchoring kills f3a, f3b and f3g. No product caller relied on the 404 for a database fault.
- **The decideInFlight order does not affect fees.** All three refusals run the same `release()` and POST nothing. The two order mutants (W's, and mine with the landed check before the in-flight loop) survive every money cell and die only on message cells.
- **All 9 of my merge-resolution mutants are KILLED.** So is my anchoring mutant.

**What is not clean:**
- **G68-F1 (MINOR, money, latent).** R2a's "already anchored" check compares the row's network, which anchoring writes from ITS OWN `CARDANO_NETWORK`, with ORIGINATE's `CARDANO_NETWORK || 'preprod'`.
  - Wherever the two services are configured differently, every landed anchor reads as "another network", and the retry pays again on that same row. Measured: N-R3 1 POST, N-Q3b 1, N-R4 2. The base pays the same, so this is not a regression; R2a's G58-F2 fix simply does nothing in that configuration.
  - Two deploy descriptors in the repo configure it that way (`services.bicep` and `docker-stack.yml`), and a third does when its variable is unset (`docker-compose.production.yml`).
  - The live VM compose stack is consistent.
  - W's harness cannot see this: its fake writes the request's network into the row.
- **G68-F2 (NOTE, instrument).** Gate 65's probe, re-run at R2a, mostly exercises R2a's fail-safe default and not the real comparison. Its fake rows carry no `contentHash` or `network`.
  - Proof: G68-M2 (the merge drops round 3's marker) is killed by **0 of its 25 cells**.
  - The conclusion of condition (c) still holds; I re-established it with real-shaped rows.
- **G68-F3 (NOTE).** Residual: a confirmed row whose stored hash differs from the document's is paid for again on every retry (2 at head and at base). Anchoring's upsert never updates `content_hash`.
- **G68-F4 (NOTE, liveness).** An "already anchored" document is 409 until R2b heals it. This is stated by W.
- **G68-F5 (NOTE).** Spec and claims nits.

**Merge onto develop:** NOT clean. The conflicts are train-level (G61-F2), not this gate's blocker, and none is in the delta's hunks. The count changed during the gate:
- At the start, develop a3b42157 gave 12 conflicts.
- At the end, develop had moved to 2bc1a0b2 (F0b #1854 merged), which gives **8**.

**Heads:**
- **START** (2026-10-31T19:53:10Z, `git ls-remote`, `evidence/lsremote_start.txt`):
  - `refs/pull/1874/head` = `31d1466788bea96f6175b595c8fb3078229668be`
  - develop = `a3b421570456aebd756cee4633d9f5f9bdcae86d`
  - `refs/pull/1868/head` = `7ed460cc4258…`
- **END** (2026-10-31T20:47:46Z, `evidence/lsremote_end.txt`):
  - `refs/pull/1874/head` = `31d1466788bea96f6175b595c8fb3078229668be` (unchanged)
  - develop = `2bc1a0b2b99d6723599e4d8f35fc93e2dff3e19a` (moved)
  - `refs/pull/1868/head` unchanged
- This GO is a statement about **31d146678** only.

## VERDICT: GO WITH NOTES
- **Fix-before-merge: none.** No cell pays more at the head than at the base.
- **Conditions** (priority is Wednesday's):
  - (a) **G68-F1 is closed before R2a runs anywhere except the compose VM**, or it is carried as a named item in R2b or in a round 2. The fix shapes are under G68-F1. R2a is already deploy-held with F0, F-b, R1 and R2b.
  - (b) R2b's gate re-runs `evidence/probe/gate68-r2a-probe.integration.test.ts` and not only gate 65's probe. At R2b the N-* cells must read 0, 1 and 1 POSTs, or the network leg must be ruled acceptable.
  - (c) The train still needs its develop rebase (G61-F2). There are 8 conflicts at 2bc1a0b2.

## FINDINGS

**G68-F1 · MINOR · money, latent, not a regression.** (Code: `reanchorInFlight.ts` `isLandedForThisContent`, :117-125; `documents.ts`:1559; anchoring `index.ts`:513 and :1523-1557.) R2a's landed check compares anchoring's network with originate's. Where the two differ, a landed anchor is paid for again.
- **Mechanism:**
  1. Anchoring stores `network: CARDANO_NETWORK`, its own environment variable (index.ts:513). It ignores the `network` field in the request body, because `anchorDocumentSchema` does not read it.
  2. The route passes `process.env.CARDANO_NETWORK || 'preprod'`, which is originate's.
  3. `isLandedForThisContent` returns false when both values are readable and they differ.
  4. With no marker, the decision falls through to ABSENT. The retry POSTs, and anchoring upserts `ON CONFLICT (document_id, network)` on **its own network**, which is the same confirmed row. A second fee follows.
  - The rule's premise is that a row on another network is "not this route's anchor". That is false when a single anchoring service writes every row.
  - In this case the rule fails toward paying, the opposite of the stated principle ("fail toward not paying").
- **Measured** with probe68 (real Postgres, app role; anchoring's fake stores its own network, the way the real service does):

| Cell | 7ed460cc | head |
|---|---|---|
| N-R3: R3-crash, anchoring on preview, originate at its default preprod | 1 POST | **1** |
| N-Q3b: anchor_failed blob, row confirmed on preview | 1 | **1** |
| N-R4: R4-502, anchoring on preview | 2 | **2** |
| N-P3b: marked, then the mismatch | 1 | 1 (the marker rule still refuses) |
| N-ctl control: both on preview | 1 | **0** |
| N-case: row network "Preprod" | 1 | 0 |

- **Configurations** (READ ONLY; at 31d146678):
  - `deployment/azure/services.bicep`: originate sets no `CARDANO_NETWORK`, so it uses 'preprod'. Anchoring gets 'preview' (:1191). Mismatch.
  - `deploy/docker-swarm/docker-stack.yml`: originate unset; anchoring 'preview' (:124). Mismatch.
  - `docker-compose.production.yml` (an override): anchoring `${CARDANO_NETWORK:-mainnet}`; originate inherits the base `${CARDANO_NETWORK:-devnet}`. A mismatch when the variable is unset.
  - `docker-compose.yml` (the live VM stack, per DEPLOYMENT-ARCHITECTURE.md): both `${CARDANO_NETWORK:-devnet}`. Consistent.
  - Not checked: the VM's `.env`, which I did not read (secrets rule).
- **Why W's cells pass:** the r2a integration fake stores `network: String(req.body.network)` (`ks1384-r2a-landed-anchor-and-closed-read.integration.test.ts`:93). The row's network therefore always equals the route's, and (f2g) pins "another network → POST" as the intended branch.
- **Fix shapes (W's choice):**
  - (a) Drop the network leg. Anchoring keeps one row per (document, its own network), so any confirmed row it returns is on the network a POST would pay on.
  - (b) Or treat a readable network mismatch as anchored, or as unavailable (fail closed).
  - (c) In every case, set originate's `CARDANO_NETWORK` in the bicep and swarm descriptors, and consider a boot check that it equals anchoring's.
- **Regression test the owner should add:** a fake that stores ITS OWN network and an originate environment with a different one, on R3-crash and Q3b shapes, expecting 0 POSTs.
- **Evidence class:** MEASURED AT RUNTIME (probe68, N-*); deploy reach READ ONLY.
- **Spark:** missed it.

**G68-F2 · NOTE · instrument (gate 65's probe at R2a; W's "22/25" and condition (c)).** Gate 65's fake returns `{id, status}` rows only.
- Under R2a, a confirmed row with no hash and no network is "anchored" by the fail-safe default. So gate 65's 25 cells, and W's re-run of them, go through the fail-safe branch and never compare a hash or a network.
- **Measured:** G68-M2, in which the merge loses round 3's `postOutcomeUnknown` and the marker is ignored, is killed by **0 of probe65's 25 cells**. It is killed by 3 of probe68's cells, by 1 of W's r1r3 and by 1 of W's retry-route cells.
- G68-M9, in which the merge keeps a marker rule that skips confirmed rows, is killed **only** by probe68 (N-P3b, H-diff-marked). **None of W's 83 cells** catches it.
- The conclusion still stands. With real-shaped rows on a consistent network, R3-crash pays 0 (S-R3), R4-502 pays 1 in all (S-R4) and P3b pays 1 (S-P3b). Ten parallel retries on R3-crash pay 0.
- **Recommendation (MEASURED AT RUNTIME):** the train's probes carry the real `formatAnchorResponse` fields from now on.

**G68-F3 · NOTE · residual, not stated, not a regression (anchoring index.ts:1523-1557, upsert update list).**
- A confirmed row with a readable DIFFERENT hash is deliberately "not this content's anchor", so the retry POSTs (W's f2e).
- But the upsert never updates `content_hash`. The row keeps the old hash, so it never matches, and each later pass through an `anchor_failed` blob pays again.
- H-diff-repeat: **2 POSTs at the head and at base**.
- Reachability needs a document whose `content_hash` changes in place after anchoring, with its blob back at `anchor_failed`. That is NOT established: I did not trace the `/version` handler. Severity is NOTE pending that trace.

**G68-F4 · NOTE · liveness, stated by W.** The 'anchored' 409 releases the claim and writes nothing:
- An `anchor_failed` blob stays as it is. A claim-made blob is removed (O-5: the blob becomes null).
- Every later retry is 409 "already anchored" until R2b's resolver heals it. Measured on S-again: head 409/409/409 with 0 POSTs; base 202 and then 400 with 1 POST.
- This is money-safe. The deploy hold already ties R2a to R2b.

**G68-F5 · NOTE · spec and claims.**
- (i) The (d1) title says "naming all **three** messages" but asserts four. The file header says "R2a adds a third message". Both are stale text. The test body is right.
- (ii) In (d2), `toContain('60')` cannot fail on its own while '600' is present ('60' is a substring of it). A bound like `/\b60\b/` would make it independent.
- (iii) The first 409 message ("A re-anchor for this document is already in progress, or it is anchored") is asserted only as spec text in (d1). No route cell asserts it as a response body (grep over every originate test file except my probes). The other three are asserted at route level.
- (iv) The 503's Retry-After description names 60 and 600. The production POST-failure 503 (documents.ts, the `else` branch, "Blockchain anchoring service is temporarily unavailable") sends **no** Retry-After, and the spec does not say "absent otherwise".
- (v) Anchoring's new 503 description on the by-document route is asserted by no test. `check:openapi` only proves the yaml matches the source.
- (vi) The 400 "Document is already anchored" and the new 409 "This document is already anchored (…)" are near-identical texts under two statuses. A client-facing note, no more.
- (vii) **W's claims verified:**
  - 157 suites / 1933 cells.
  - 44/44 real Postgres.
  - 183 test files, 0 tsc errors (plus 1 helper file, so 184 files under `__tests__`).
  - check:openapi rc 0.
  - Anchoring 729/728 with threadTokenMint the only red.
  - W's statement "Anchoring: not re-run" was honest.
  - The flow fragment does state the order. The cheat fragment does not, and that is acceptable for a cheat sheet.

## Q1. Condition (c), and gate 65's set at this head
- **Gate 65's probe unchanged** (sha256 `3be022f8…`, copied into the tree for the runs only): head **22/25**, base 7ed460cc **19/25** (`evidence/probe65_head_app.log`, `evidence/probe65_base7ed4_app.log`).
  - R3-crash: base 202 (1 POST), head 409 (0). **Pays once.**
  - R4-502: base B 202 (2 POSTs), head B 409 (1). **Pays once.**
  - Q2c-writer: base 2 POSTs, head 1. R2a closes G65-F3's cell.
- **The three reds at the head, checked at source:**
  - **R1-wedge** (D 409, E 409, 2 POSTs) is G65-F1. The delta does not touch `documentRepo.ts`, so it is unchanged here. The claim that R2b fixes it is not tested here.
  - **R2-f3** (1 POST) is red because of the fake. The cell makes the fake answer the OLD swallowed 404; originate reads a 404 as absent and POSTs. With the real anchoring at this head:
    - the failed read answers 503: f3a (SELECT throws) and f3b (DB unavailable) are 503 with fixed text, and f3g carries no DB error text. These are anchoring's own cells, green at the head.
    - my mutant G68-A1, which restores that 404, kills exactly f3a, f3b and f3g (`evidence/mut/G68-A1.anchoring.log`).
    - originate turns that 503 into 503 Retry-After 60 with 0 POSTs. That holds for a marked document (F-503m) and for an unmarked crashed holder (F-503u).
    - control F-404u: the same document under the old 404 POSTs once, so the cell can see a fee.
    - So gate 58's Q4c and gate 65's G65-F2 (iii) are closed **at anchoring's by-document route**.
    - The by-id route's document-id fallback still fails open (`dbGetAnchorsByDocument`, kept on purpose). Its only product caller passes an anchorId (`anchorStateSync.ts`:125), never a document id.
  - **Q2b-past** (2 POSTs at head and base) is round 3's residual 2, unchanged.

## Q2. decideInFlight order and the merge resolutions
- **The order:** in-flight rows, then landed (confirmed for this content and network), then the marker rule (any row), then absent. That matches the merge message and Wednesday's 17:44:28Z ruling. Measured:
  - O-1: marker plus a confirmed matching row gives "already anchored", 0 POSTs, marker kept, claim released.
  - O-2: submitted on preview plus confirmed on preprod gives "still in flight".
  - O-3: marker plus a failed row gives "may have landed".
  - O-4: no marker plus a failed row gives 202, 1 POST (the liveness control).
- **Fees do not depend on the order.** All three refusals call the same `release()` and POST nothing.
- **Mutants** (`scripts/mutants.py`, `evidence/mutants_run.log`, `evidence/mut/`):
  - Method: every anchor asserted to its exact count; the mutation asserted present on disk before any job ran; scoring per cell against the unmutated baseline; every product file restored from `git show 31d14667:` with sha256 checked.
  - Jobs per mutant: W's r2a (10) and r1r3 (14) real-Postgres files, W's in-flight-decision (30) and retry-route (29) unit files, and probe68 (25). Probe65 (25) was added for M2 and M4.
  - Baseline: all green, except probe68's 4 measured residual reds (N-R3, N-Q3b, N-R4, H-diff-repeat) and probe65's 3. Those are never counted as kills.

| Mutant | Result | Killed by |
|---|---|---|
| G68-M1 (W's order mutant): marker rule before the landed check | KILLED, fee-neutral | W's (order); my O-1. **No money cell** |
| G68-M2: merge loses `postOutcomeUnknown` | KILLED | W r1r3 (1), W route (1), probe68 N-P3b, H-diff-marked, O-3. **probe65: 0** |
| G68-M3: merge loses R2a's hash and network (both undefined) | KILLED (liveness: refuses legitimate POSTs) | W r2a f2e and f2g, W route (1), probe68 H-diff |
| G68-M4: merge drops the 'anchored' branch (falls through to the POST) | KILLED | W r2a 5, W r1r3 4, W route 3, probe68 12, probe65 7 |
| G68-M5: landed check before the in-flight loop | KILLED, fee-neutral | W (L6); my O-2 |
| G68-M6: network compared case-sensitively | KILLED | W infl (1); N-case |
| G68-M7: `sha256:` prefix not stripped | KILLED | W r2a f2h, W infl, H-prefix |
| G68-M8: any status can read as landed | KILLED | W (D2), W route, O-4 |
| G68-M9: marker rule skips confirmed rows | KILLED **only by probe68** | N-P3b, H-diff-marked |
| G68-A1 (anchoring): restore the fail-open 404 | KILLED | f3a, f3b, f3g |

## Q3. Who else calls the by-document route (frame: `git grep 'anchors/document'` at 31d146678, the whole repo, 111 lines; `evidence/callers_anchors_document_head.txt`)
**Product code** (services, packages, frontends):
- Only originate's `reanchorInFlight.ts` calls the route. It reads 503 as unavailable (measured above).
- `certifications.ts`:551 is a comment.
- `anchorReadGate.ts`, `honestAnchor.ts` and `specRouteMap.ts` are comments or the route map.
- No frontend calls it.

**Suites:**
- `systemTest/schemathesis/.../fixtures/platform_ops.py`:289 maps 404 to "no anchors" and raises on any other non-2xx. Its docstring says *"a broken endpoint must not read as an absent anchor"*, so the 503 is what it wants.
- `test_anchor_read_honesty.py` polls for a 200 and fails at its deadline on anything else. That is unchanged on a healthy DB.
- k6 `smoke.ts` checks for a 200.
- The tenant-isolation runner expects 403 or 404 on a foreign tenant. The KS-1822 refusal is still 404 (f3d, green).

**Nothing relied on the 404 for a database fault.** The 503 was already declared through `commonErrorResponses[503]`, so schema conformance holds. READ ONLY for the suites; I did not run them.

## Q4. The four 409s and the 503
- **Spec:** `originate.openapi.ts` declares one 409 naming four messages and a 503 Retry-After header. The yaml is regenerated.
- **check:openapi:** rc 0 (`evidence/check_openapi.log`, 416 example blocks). Positive control: one planted word in the 409 description gives "CHECK FAIL", rc 1 (`evidence/check_openapi_control.log`). The source was restored and `git status` is clean.
- **Messages reached at runtime** (probe68 logs the body text):
  - "still in flight" (O-2)
  - "already anchored" (S-*)
  - "may have landed" (O-3, H-diff-marked, N-P3b)
  - "already in progress, or it is anchored": reached as a 409 status (probe65 P1e and S-par race losers); its text is asserted nowhere at route level (G68-F5 iii).
- **Retry-After:** 60 measured (F-503m), 600 measured (probe65 P3a-d). The third 503 sends none (G68-F5 iv).

## Q5. Anchoring, at this head
The author did not run anchoring.
- **Unit (vitest 4.1.12):** 51/52 files, **728/729**. The red is threadTokenMint, "parameterises mint + spend…", at 51.6 s (an emulator round-trip). The delta does not touch it. I did not prove it host-dependent. (`evidence/anchoring_unit_head.log`)
- **Integration, app role, gate68-pg:** 10/10 files, **122/122** (`evidence/anchoring_integ_head.log`). The first run, with the superuser only, refused 3 files loudly because they need `TEST_APP_DATABASE_URL`. That was my setup (`…_superuser_only.log`).
- **Scratch merge onto develop: NOT RUN.** Blocker: anchoring `index.ts` conflicts with develop, at a3b42157 and at 2bc1a0b2 (lines 32-36, 48-55 and 1791-1795 in the merge-tree; the delta's hunks at 1021 and 1744-1759 merge clean). A merged anchoring tree cannot be built without resolving another member's conflicts, which is not mine to author.
- **Originate at the head:**
  - Unit: 157/157 suites, **1933/1933** (`evidence/unit_head_full.log`).
  - W's real-Postgres files, app role: **44/44** (`evidence/w_integ_head_app.log`).
  - tsc on the product: rc 0.
  - tsc with all 184 files under `__tests__` (my probes excluded): rc 0.
  - tsc positive control: a planted TS2322 gives rc 2.

## Q6. Fee counts, base 7ed460cc against head (every money cell; POSTs counted on arrival)

| Cell | base | head |
|---|---|---|
| probe65 P1a-e, P3a-d, Q2a-*, Q2b-in, Q2c-route, Q2d-* | same as gate 65's head | same (1 each) |
| probe65 P5, P5b | 0 | 0 |
| probe65 **R3-crash** | 1 | **0** |
| probe65 **R4-502** | 2 | **1** |
| probe65 **Q2c-writer** | 2 | **1** |
| probe65 R2-f3 (fake 404) | 1 | 1 |
| probe65 Q2b-past | 2 | 2 |
| probe65 R1-wedge | 2 | 2 |
| probe68 S-R3, S-Q3b, S-par, S-again, O-5 | 1 each | **0 each** |
| probe68 S-R4 | 2 | **1** |
| probe68 S-P3b, N-P3b, O-4, H-diff | 1 | 1 |
| probe68 N-ctl, N-case, H-prefix, H-nohash | 1 | **0** |
| probe68 N-R3, N-Q3b | 1 | 1 (G68-F1) |
| probe68 N-R4 | 2 | 2 (G68-F1) |
| probe68 H-diff-repeat | 2 | 2 (G68-F3) |
| probe68 O-1, O-2, O-3, H-diff-marked, F-503m, F-503u | 0 | 0 |
| probe68 F-404u (control) | 1 | 1 |

**No cell pays more at the head.** Probe68 is 10/25 at base and 21/25 at the head (`evidence/probe68_base7ed4_app.log`, `evidence/probe68_head_app.log`). For the base runs, the three originate product files were swapped to 7ed460cc and restored, with the sha256 check rc 0 (`evidence/swap_base_7ed4.out`).

## SPARK (run first)
- **`spark_gate.sh`**, base `develop`, three originate unit files, `--work /private/tmp/gate68_spark_work2`:
  - rc 0.
  - Merge-base dc8c210c, so the diff is the whole train: 73 files, +9381/-282.
  - **HEAD: 62/62.**
  - BASE: does not compile, because `reanchorInFlight` and R2a's symbols are absent on develop. That is true, and it says nothing about this delta.
  - **Run 1 was my own instrument fault:** `@secuura/shared` was not yet built, so one file showed TS2307 with 0 tests, and the script reported files_failed=1 with failed=0 (`evidence/spark/facts_run1_unbuilt_shared/`). Rerun after the build.
- **`spark_review.py`** on the 7ed4..31d1 delta, with the commit messages as the body: attempt 1 hit a repetition abort; attempt 2 was valid. Verdict **NO GO** (`evidence/spark/review_delta/review.json`).

| Spark finding | Gate 68 | Calibration |
|---|---|---|
| Major: marker plus a different hash or network gives maybe-landed and refuses, contradicting "proceeds as before" | The behaviour is real (H-diff-marked 409). It is round 3's intended rule and money-safe. "No test covers it" is true of W's cells (G68-M9) | Partial |
| Major: anchoring's 503 is undeclared or has no Retry-After | The description IS updated. No Retry-After on anchoring's 503 is true, but its only product consumer converts it | Partial (mostly false) |
| Major: the mutant and cell counts are unmeasured | Instrument scope | Noise |
| Minor: the anchored branch does not heal the blob | G68-F4, stated | True (stated) |
| Minor: the fail-safe on a missing hash refuses a legitimate re-anchor | Real rows always carry `content_hash` (NOT NULL) | Partial |
| Minor: no Retry-After on anchoring's 503 (duplicate) | As above | Noise |
| Notes ×2 | True and stated | Noise |
| Verdict NO GO | GO WITH NOTES | **Disagrees** |

- **It missed:** G68-F1 (the network leg; the only money finding), G68-F2, G68-F3, and the develop conflicts.
- Score: 1 true, 3 partial, 3 noise.

## NOT TESTED (Rule 2)
- **A real anchoring service end to end with originate.** The probes use a loopback fake. Anchoring's 503 was measured in anchoring's own cells with its DB layer mocked. No real Postgres fault was injected under the real service.
- **Real Cardano.** Rows were confirmed by hand. Lease expiry was forced by backdating `retryClaimedAt`.
- **The live VM's actual `CARDANO_NETWORK` values.** Its `.env` was not read, so G68-F1's live reach is by the compose file only.
- **Whether a document's `content_hash` can change in place** (G68-F3 reachability; `/version` not traced).
- **Node 24 LTS.** Everything ran on **Node v26.8.1, which is not an LTS line** (`evidence/node_version.txt`).
- eslint, the docs-fragments check, the four platform suites, the shell suites, a running stack, any chain or box.
- Whether threadTokenMint is host-dependent.
- **The scratch merge onto develop** (conflicts, see Q5).
- W's 15 mutants and W's red-before claims for the 30 new R2a cells: I did not re-run them at a46c251e.
- The PR body: `gh` was not used from this seat.
- R2b's claims (the R1-wedge fix, part 4).
- **Concurrency of an anchored refusal against a holder's outcome write.** My parallel cells use one shape (S-par).

## HOW
- **Clone:** `repo/`, made with `git clone --shared --no-checkout` from gate 65's clone.
  - `core.sshCommand` is set to the Blockchain deploy key, as copied. The push URL is `no_push_qa_gate`. It is a promisor with filter blob:none.
  - `git rev-parse --show-toplevel` equalled the clone directory before every fetch and write.
  - Refs were fetched into `refs/gate/*`.
  - Nothing was written under `/Volumes/DevMASTER/!CODING`.
- **Install:** `npm ci --ignore-scripts` (1795 packages, rc 0), then the `@secuura/shared` build (rc 0) and the Prisma generate (rc 0).
- **DB:** container **gate68-pg** (postgres:15-alpine, loopback, random port, `max_connections=1000`).
  - Init came from scratch copies of the repo's `docker/init` and `docker/init-platform`.
  - Migrations ran inside the container with the repo's `scripts/run-migrations.sh`: applied=57, failed=0 (`evidence/migrate.log`; the password count in the log is 0).
  - The passwords were generated with `openssl rand` into the scratchpad `pw.env` (0600) and scrubbed from every log.
  - The cells ran as `secuura_app`, with the superuser used for seeding.
  - The container is **stopped** (Exited 0).
  - gate65-pg was still up from gate 65. I did not touch it; Wednesday's call.
- **Jest/vitest:** `scripts/jest_run.sh` (nice 10; waits while load1 > 8, and it waited several times; `--runInBand` for single files, 2 workers for the units). Load1 was 6-11 during the runs. No timeout-only red occurred.
- **Probes:** `evidence/probe/gate68-r2a-probe.integration.test.ts` (mine) and gate 65's file unchanged. Both were copied into `src/__tests__` only for the runs, then moved to the scratchpad `_quarantine_2026-11-01/`. Nothing was removed. `git status` in the clone is empty at the end.
- **Time split:** setup ~25%, test design and execution ~55%, investigation ~20%.
