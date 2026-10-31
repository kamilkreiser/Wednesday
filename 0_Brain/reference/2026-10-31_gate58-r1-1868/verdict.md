## QA GATE 58, TIER 1, ROUND 1: KS-1384 R1 #1868
(Opus, Sat 31 Oct 2026. Findings only: nothing was fixed, pushed, commented, merged or touched in Linear. Evidence is in `evidence/`.)

**Head.** #1868 = **13fdd7f31f22e9cd3aa0709c2bc60e0f6050429f**, read with ls-remote at the start and at the end; unchanged (`evidence/lsremote_{start,end}.txt`).
- Base: F-b #1858 = c39f61fe2def (gate 57 GO WITH NOTES), unchanged.
- Delta: c39f61fe2def..13fdd7f31f22, one commit, 10 files, +961/-12. That matches W.
- develop was 644452e4af6d at the start. `git merge-tree` of the head with it is clean (0 conflicts). develop moved to df99b04720b8 during the gate; I did not re-merge against it.

## VERDICT: **GO WITH NOTES**
- **Concurrent double-pay is CLOSED.** It is reproduced at c39f61fe and gone at the head, on real Postgres with parallel connections.
- **Nothing is fix-before-merge on its own.** No path I found pays more at the head than at the base.
- **Two items should be closed before the train DEPLOYS**, in R1 round 2 or in R2, by Wednesday's ruling:
  - G58-F1: the takeover race. The holder has no deadline.
  - G58-F2: a confirmed anchoring row reads as "absent".
- **G58-F3 is cross-service.** It sits in anchoring, outside R1's file set.

## Q1 DOUBLE-PAY: CLOSED (probe `evidence/probe/gate58-r1-probe.integration.test.ts.ran`)
**Instrument:**
- The REAL documents router, documentRepo and db layer run on real Postgres 15 (container `gate58-pg`, repo `docker/init`, applied=57 failed=0).
- Anchoring is a REAL loopback HTTP fake that keeps one row per document, the `ON CONFLICT (document_id, network)` reset shape. It counts POST /api/anchors, which is the fee point.
- The calls are genuine parallel HTTP requests.

| Cell | c39f61fe (product files swapped in, positive control) | 13fdd7f3 head, superuser | head, `secuura_app` (RLS, tenant GUC) |
|---|---|---|---|
| Q1a 2 parallel, anchor_failed | **2 POSTs**, [202,202] | **1 POST**, [202,409] | 1 POST, [202,409] |
| Q1b 10 parallel | **10 POSTs** | **1 POST**, nine 409 | 1, nine 409 |
| Q1c 8 parallel, blob-less | **8 POSTs** | **1 POST** | 1 |
| Q1d lock-forced: a locker holds FOR UPDATE until **5 distinct backends** wait on the row lock, then commits | **5 POSTs** | **1 POST** | 1 (5 waiters) |
| Q1e sequential retry after a 202 | 400, 1 POST | 400, 1 POST | same |

Logs: `probe_base_c39f.log`, `probe_head.log`, `probe_head_app_role.log`. pg_stat_database showed 12023 tuple writes over the session.

## Q2 THE CLAIM
- **Takeover at 10 min:** holds at 9 min and is taken at 11 min (Q2c).
- **Release guarded on the token:** a stale holder's 503 release leaves the takeover's claim in place (Q2b: tokenA ≠ tokenB, the claim still equals tokenB, and B then POSTs once).
- **Takeover race (G58-F1): BOTH CAN POST.** See Findings.
  - Q2a: A's in-flight read was held and A's claim backdated 11 min. B took over and POSTed. A's read was then answered with the live state, and A got 409 (safe).
  - **Q2a-stale:** the same, except A's read answered with the pre-B state (404). Result: **2 POSTs, A 202 and B 202**. A's outcome write matched 0 rows and was only logged.
  - Control without the backdate: B gets 409 and there is 1 POST.

## Q3 M4 AND A FIRST POST THAT LANDED (G58-F2)
- **Q3a.** The blob is pending with a claim that made it, crashed after its POST 11 min ago. The anchoring row is **confirmed**. Result: **202 and a second POST**; the fake row is reset to pending.
  - Controls: with the row submitted, 409 and 0 POSTs. With the claim only 5 min old, 409.
  - At c39f the blob shape is new. The pre-R1 equivalent, a blob-less document whose holder crashed after the POST, POSTs again.
- **Q3b.** The blob is anchor_failed and names its anchor; the row is **confirmed** (adopted, or the create path lost the 202). Result: **a second POST at the head AND at c39f** (pre-existing).
- **Q3c.** A plain `{status:'pending'}` blob with no anchorId and no claim now gets **409 for ever**; before, it got 400 for ever. It is not claimable. This is a NOTE only: I found no writer that produces it.
- **M4 itself behaves as stated.** A crashed pre-POST claimant is re-claimable after 10 min, and the in-flight read then decides.

## Q4 IN-FLIGHT READ FAILURES
- **Originate side: fail-CLOSED.**
  - Fetch error: 503 with Retry-After 60, 0 POSTs, and its own claim released (Q4a).
  - A 500 from anchoring: 503, 0 POSTs (Q4b).
  - A 2xx without an anchors list: 503, 0 POSTs (Q4b).
  - A hung read: 0 POSTs while it hangs (Q4d).
- **No timeout.** Neither `readInFlightAnchor` nor the POST passes a signal (documents.ts:1547, 1572). That feeds F1.
- **Anchoring side: fail-OPEN (G58-F3).**
  - anchoring `dbGetAnchorsByDocument` swallows any DB error into `[]`, and the handler (index.ts:1004-1012) answers the same 404 "No anchors found". `!isDbAvailable()` does the same.
  - R1 reads that 404 as ABSENT when the tenants match and the blob names no anchorId.
  - Q4c reproduces the shape: holder crashed, row still **submitted**, read answers the swallowed 404. Result: **a second POST**.
  - The anchoring side is by reading; the originate decision is measured.

## Q5 SCOPE: CLEAN
- All 10 files are under `services/originate/src`.
- **Product:** documentRepo.ts (+132: three functions), documents.ts (retry route only), and the new reanchorInFlight.ts.
- **Changed existing tests** (ks1293, ks1385, ks1814, ks520) are adapters only: the mocks for the three new repo functions, and a GET answer. Nothing is weakened; ks1814 P10 now asserts the claim token on the write.
- **Behaviour change:** a non-production unreadable in-flight state now gets 503 instead of 202 plus a failed blob. As W stated.
- **The undeclared 409 is the known R2 gap**, not counted.

## Q6 MUTANTS (`evidence/mut/`; each applied by a unique anchor, restored with `git show` and verified by sha256 `4a7b3925…` and `d72b6c0f…`)
| Mutant | My cells | W's integration (12) | W's unit (34) |
|---|---|---|---|
| M1 live-claim term → TRUE | **KILLED** by Q1a-d, Q2c, Q2a-control | killed (3 red) | survives |
| M2 TTL `<` → `>` | **KILLED** by Q1a-d, Q2b, Q2c | killed (4) | survives |
| M3 TTL = 0 | **KILLED** by Q1b-d, Q2c, Q2a-control | killed (2) | survives |
| M4 release not guarded on its token | **KILLED** by Q2b | killed (z8) | survives |
| M5 route ignores the claim's row count | **KILLED** by Q1a-d | survives | killed (1) |
| M6 route ignores an in-flight row | **KILLED** by Q2a, Q3a-control | survives | killed (z6) |

- The first M4 and M6 forms failed to compile (an unused parameter, and narrowing). They are recorded as `*.INVALID_ts.*` and were replaced by type-safe forms.
- W's SQL-mocking unit cells survive every SQL mutant, as designed; the real-Postgres file kills them.

## FINDINGS
**G58-F1 (MAJOR, narrow; documents.ts:1530-1600). The claim is a 10-minute lease, but the holder has no deadline and does not re-check its claim before it POSTs.**
- Mechanism:
  - A claimant whose in-flight read answers "absent" and whose POST reaches anchoring's upsert more than 10 min after its claim can be overtaken.
  - The takeover reads no row and POSTs.
  - Then the original POSTs too, and that is two fees (Q2a-stale).
- Neither fetch has a timeout. Node's defaults are about 300 s for headers per request, with body inactivity on top. A process freeze or a stalled anchoring call can exceed 10 min.
- Not a regression: c39f POSTs twice with no stall at all.
- Fix shapes, W's choice:
  - `AbortSignal.timeout` on both calls, summing well under REANCHOR_CLAIM_TTL_MS. The route already uses 5-10 s elsewhere.
  - and/or a conditional "still mine" UPDATE that refreshes `retryClaimedAt` immediately before the POST, with 0 rows meaning no POST.
- Q2a-stale is the cell that pins it.

**G58-F2 (MAJOR, pre-existing; reanchorInFlight.ts IN_FLIGHT_STATUSES). A `confirmed` anchoring row is read as ABSENT, so the retry re-POSTs a document that is already anchored.**
- Reached by:
  - Q3a: a holder that crashed after its POST, once its claim is stale (blob-less document).
  - Q3b: an anchor_failed blob whose row was later confirmed, for example a create-path 202 that was lost.
- anchoring's upsert resets a confirmed row and submits again.
- W assigns "the own-create lookup" to R2.
- **R2's gate must check that it also covers Q3a and Q3b.** Otherwise R1 should treat a confirmed row with the same content hash as 409 (or heal).

**G58-F3 (MINOR here, cross-service; anchoring index.ts:1004 and dbGetAnchorsByDocument). anchoring answers a failed DB read with the "no rows" 404, so R1's fail-closed read is fail-open in exactly the crashed-holder case it exists for (Q4c).**
- Out of R1's file set. It needs an anchoring change (5xx on a read error), or a ticket.

**Notes:**
- **N1:** Q3c, a claimless pending blob, now gets 409 for ever instead of 400. No writer was found.
- **N2:** an outcome write that matches 0 rows still answers 202 and starts the poller (stated by W).

## COUNTS (Node v26.8.1, NOT LTS)
- **Install:** `npm ci --ignore-scripts` at Blockchain/Dev (1795 packages), then a build of @secuura/shared and the Prisma generate.
- **Originate unit (jest):** 155/155 suites, **1898/1898**. This matches W.
- **W's R1 cells:**
  - unit 34/34 at the head;
  - the retry-route file at c39f: **11 of 13 red**, which matches W;
  - real-Postgres claim file: 12/12.
- **tsc (originate tsconfig):** 0 errors. Positive control: a planted TS2322 gives rc 2.
- **My probe:** head 15/19. The 4 reds are F1 (Q2a-stale), F2 (Q3a, Q3b) and F3 (Q4c); those cells assert the safe outcome. c39f: 17/19 red.

## SPARK SHADOW AND CALIBRATION
- **spark_gate.sh** (`… 1868 13fdd7f3… c39f61fe… ks1384-r1-retry-route.test.ts`): "merge-base (empty) · diff 0 files". **This is the base-side instrument fault from gates 48, 49 and 57, and it recurs.** BASE reported 13/13; the truth is 2/13, measured.
- **spark_review.py:** run on the clean c39f..13fd diff with `--linear-env /dev/null`. It returned **NO GO**.

| Spark finding | Gate 58 | Calibration |
|---|---|---|
| Major: the repo SQL is not restricted to test data | The tenant-scoped product SQL is correct | False |
| Major: the integration test may run on a shared DB | Hygiene, not the PR's defect | Noise |
| Major: documents.ts route changes are not in the diff | They are in the diff (+70/-12) | **False** |
| Major: the route tests pass on base | Produced by the instrument fault; truth 11/13 red | Instrument-true |
| Major / Minor: integration and in-flight files not run | True of the facts I gave it; I ran them (12/12, and 34/34 unit) | Instrument-true |
| Minor: the mocked 404 body may differ from anchoring's | It equals anchoring's ABSENT body. Near F3, but F3 was not stated. | Partial at best |
| Verdict NO GO | GO WITH NOTES | **Disagrees** |

Score: 0 true, 1 partial, 3 instrument-true, 3 false or noise. **It missed F1, F2 and F3.**

## UNMEASURED
- The real anchoring service: F3's swallow is by reading, and F2's re-submit of a confirmed row follows from the upsert, also by reading.
- Any chain, wallet or box.
- Whether F0b's family logic would stop the second build in F1 or F2.
- The real Node/undici stall lengths: F1 is forced by backdating the claim.
- Two originate processes (behaviour should match, since the claim is in SQL).
- Node 24 LTS.
- eslint, hook legs, the four platform suites, check:openapi.
- R2.
- Design rev 4: it is not in the repo.

## HOW
- **Clone:** `git clone --shared --no-checkout` from gate 48's clone into the non-existent `repo/`, with toplevel asserted before any fetch. Push URL is `no_push_qa_gate`; fetch uses the Blockchain deploy key.
- **Product swaps:** done only in my clone and restored by sha. The probe was copied into src only for its runs and kept as `*.ran`. `git status` was clean before teardown.
- **Hygiene:**
  - No git write verb was run in !CODING.
  - W's `s-w13-pg` was not touched.
  - `gate58-pg` was stopped and removed by name.
  - The clone, the spark worktree and the scratch init copies were deleted.
  - Every PID I started has exited.
