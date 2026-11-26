PR 2295: GO WITH NOTES (at head dbceb300851b6b76552614a25c0c1d03f6ac96bf; tier 1)

# QA GATE 420, tier 1: KS-2366 certification verify answers 'anchored' only for a confirmed anchor, plus the certification confirm path

Gate: claude-opus-5-5, findings-only. Started 2026-11-26 11:39:04 AEDT, finished about 12:05 AEDT (both from `date`).
Work: my own clone `_work/repo` (fresh `gh repo clone` as kksecura, not a copy of the builder's repo), worktrees `_work/head` (dbceb300851b), `_work/dev` (59e89c87719e), `_work/mut` (head, for mutants). Raw outputs: `_work/out/`. The gate's own test files: `_work/g420tests/` (copied into a tree for a run, then moved to `_work/moved/`. All trees show `git status --porcelain` empty afterwards).

## BLUF

- **Part 1 is conformant.** I ran 28 blob shapes against 3 callers, so 84 verify calls on the real router, and they give the same table the ruling asks for. Every unconfirmed, failed, simulated, malformed and odd-typed blob answers `false`. A confirmed anchor with a 64-hex hash and a valid or absent height answers `true`, and so does the chain-first `anchored:true` shape. The KS-1699 and KS-2239 behaviours do not change: every call answers 200, an anonymous caller gets 0 charges and `chargeEventId` null, a signed-in caller gets exactly 1 charge, and only a party sees the issuer. The verify route made **0 outbound calls and 0 writes in all 84 calls**. On develop the same matrix answers `true` for 25 of 27 non-empty shapes, which is the presence test this PR removes.
- **The new writer is sound.** Builder cells D1 to D7 plus 9 cells of my own pass on my own Postgres 15. It never matches a document row, another tenant, a confirmed blob, another anchor, NULL or empty inputs, or an injection-shaped anchorId. A malformed id throws. It never writes `status`, and two concurrent writes land exactly one.
- **The reach is bounded.** An anonymous GET answers 401. A non-party GET answers 404 and makes 0 anchor reads. A party GET makes 1 anchor read with the caller's own bearer, then 1 write and a re-read. A **socket proof** (real router, real repository, real Postgres, a stub anchoring service that is a real HTTP server) confirmed a certification end to end, and an anonymous verify then answered `true` without contacting anchoring.
- **Re-runs agree with the builder's figures, with one exception.** My figures: jest WHOLE 3770/3770 at head and 3738/3738 on develop. tsc rc 0 on both arms. check.cjs reports 0 new. eslint matches develop. shared vitest has only KS-278 failing, on both arms. I sampled 9 mutants: 7 were killed by their named cells, 1 was caught only by my own matrix, and 1 is equivalent. The exception is the builder's "220 environmental failures", which is 226.
- **No Blocker and no Major.** There are three Lows and six Notes. The main Low is that a certification whose anchor failed for good is re-read from anchoring on every party GET, forever. This follows from the approved "no failure write for certifications" design.

## Findings

### G420-1 (Low): the GET reconcile re-reads anchoring on every party GET for a certification it can never settle
- **FOUND:** a certification blob is written only on a `confirmed` decision (the approved design: no failure write, KS-1805 listed). A stale in-flight certification whose anchor row is `failed` therefore stays in flight for good. After `RECONCILE_STALE_MS` (15 min), every GET by a party does two things. It makes one `GET /api/anchors/:id` (3 s timeout). For a blob with `createAttempts`, it also makes one `POST /api/anchors/own-create` (5 s timeout; anchoring caches a `none` for 30 s). Nothing is ever written, so nothing stops it. The 10 legacy Kintsugi rows (no createAttempts, anchoredAt null) cost 1 anchor read per party GET. own-create short-circuits locally for them (`askOwnCreate` returns early when there are 0 timestamps, ownCreateClient.ts:68). A document, by contrast, records `anchor_failed`. The poller is bounded (60 x 10 s), so this applies to the GET path only.
- **TESTED:** gate matrix cell R-f: 5 party GETs of a stale certification whose stub row is `failed` gave **10 outbound calls** (anchor, own-create, x5) and **0 writes**. Control: R-g, the same row with a fresh `updatedAt`, gave 0 outbound calls. Control: R-b, a non-party, gave 0.
- **HOW:** `_work/out/g420m_head.log` (G420TABLE line `R-f`); harness: real certificationsRouter and real certificationAnchorSync behind a recording fetch interceptor.
- **Where:** `services/certificationAnchorSync.ts:136-147` (reconcile), `routes/certifications.ts:1187-1190` (call site). Only authenticated parties can trigger it, and it adds at most about 8 s of latency to such a GET. Suggest the KS-1805 follow-up (or a certification `anchor_failed` write) closes it.

### G420-2 (Low): no builder cell pins "a SIGNED-IN verify makes no anchoring call"
- **FOUND:** PIN R9 asserts no anchoring call for an ANONYMOUS verify only. An anonymous request carries no bearer, and the sync refuses to read without one. So a reconcile added to the verify route would pass R9 silently. That is the 2026-09-20 early-return class of gap: a negative-asserting cell made vacuous by a precondition.
- **TESTED:** gate mutant GM1 adds `await reconcileCertificationAnchorState(...)` to `verifyCertificationHandler`. It compiles (tsc rc 0). The builder's `ks2366-cert-verify-anchored-means-confirmed` file stayed green (9/9) and `ks2366-cert-anchor-confirm-path -t R9` stayed green. Only the gate matrix killed it (`SUBMITTED x party` went red). The source was restored and its sha256 matched.
- **HOW:** `_work/out/mutants_g420.json`.
- **Where:** `routes/certifications.ts:1341-1420`. The code at head is correct: my matrix shows 0 outbound calls for party and non-party callers. This is a test gap only. Adding one signed-in R9 cell would close it.

### G420-3 (Low): the "220 environmental failures" figure is 226, and the claim that they touch no changed file does not hold
- **FOUND:**
  - The READY and the PR body say "The other 220 failures are identical on both arms". The builder's own `evidence/integ_A_vs_C.txt` says C failed 226 (A: 232 = 226 + 6 of its own cells). My re-run, 32 files at head and 31 on develop (develop lacks the new file), gives **226 failed on both arms**, the identical 226 cells. The only differences are the 7 new D cells, which pass at head and are absent on develop.
  - The error classes (head):
    - 111 cells: TEST_APP_DATABASE_URL refusals.
    - 18: `platform_document_registry` absent.
    - 7: `secuura_app` role absent.
    - Schema gaps in a bare cluster: 120 log hits of 42P10 (ON CONFLICT with no unique constraint) and 23503 foreign-key errors.
    - `fetch failed` (no anchoring).
    - A KS-1310 port guard.
    - 1 TimeZone precondition (ks1114 expects UTC; my cluster was Australia/Sydney).
  - They are environmental and identical across arms. However, 5 failing files drive `POST /api/certifications/issue` in **routes/certifications.ts, a changed file**: ks1633, ks1538, ks1557-lineage, ks1557-verify and ks1508. They fail *before* the KS-2366 lines, at the 42P10, 23503 and fetch errors. So **the DB-backed issue and recertify path (`createAttempts` stored, the poller started) is not exercised against a database by anyone**. Only unit cells R1, R2 and R5, which use mocks, cover it.
- **TESTED:**
  - The whole integration config on both arms, on my own Postgres.
  - Then I added a NOSUPERUSER, NOBYPASSRLS `secuura_app` role with grants and re-ran 9 files on both arms. Result: 47 passed and 75 failed on each arm, identical per file. ks1402-invited-stub-holder (16/16) and ks1557-055-backfill (20/20) went green. The 5 certify-route files still fail for the same environmental reasons.
- **HOW:** `_work/out/integ_{head,dev}.json`, `integapp_{head,dev}.json`, `approle.log`. Partly mitigated by my socket proof P2 (the poller against the real repository and Postgres, G420-SP below). The issue route itself is still NOT TESTED against a database.

### G420-4 (Note): a stored `anchored: true` blob with status `submitted` answers true
- **FOUND:** `isAnchoredHonestly` accepts `anchored === true` OR `status === 'confirmed'` (verification.ts:140). A blob `{anchored:true, status:'submitted', txHash:<64 hex>}` therefore answers `blockchainAnchored: true` (matrix row ANCHORED_TRUE_SUBMITTED, all 3 callers).
- **Not a Blocker:**
  - It is exactly "the rule another verify surface already uses", which the ruling names.
  - **No certification writer at head stores `anchored`.** A grep of every service's src for `anchored: true` (outside tests) finds only response-time builders (verification.ts 999/1542/1564, verificationV2.ts 204) and openapi examples.
  - The writers of certification blobs (buildCertification, recertify, confirmedBlobOf, saveCertification as read, documents.ts legacy certify 864-873) never write it.
- **Recommendation:** whoever next adds a certification blob writer must not introduce `anchored`.

### G420-5 (Note): the SQL predicate alone does not refuse an anchor_failed, failed or simulated blob that names the same anchor
- **FOUND:** gate DB cell G6 wrote 1 row each over `status:'anchor_failed'`, `status:'failed'` and `simulated:true` blobs with the matching anchorId. G4 also writes onto a `deleted`-status row; status is kept. The guard is in JavaScript: `certificationAnchorInFlight`, re-checked on a fresh read in the poller (certificationAnchorSync.ts:115-116) and in the reconcile (:137) before `syncCertificationAnchor`.
- **Safe today:** no certification writer produces those states on a row that has an anchorId. A future KS-1805 failure writer would open a read-then-write race. Suggest moving the in-flight test into SQL then, as `writeAnchorBlobIf` does for `progress`.
- **HOW:** `_work/out/g420db_head.log`.

### G420-6 (Note): the expired-certification race writes the old blob back (the listed class, confirmed)
- **FOUND:** gate cell R-i: a stale, expired certification, with the reconcile's write matching 0 rows (a concurrent confirmer). The expiry `saveCertification` then wrote the pre-confirmation blob (status undefined, txHash null). After 15 quiet minutes the next reconcile heals it: the writer's predicate sees `submitted` again. This is the PR body's listed "save from a pre-confirmation read" item. An expired certification re-saves on every GET, so it heals only after 15 minutes with no GETs. Listed, not new.

### G420-7 (Note): staleness assumes the DB session TimeZone is UTC
- **FOUND:** on a cluster with TimeZone Australia/Sydney, the repository read `updated_at` 11 h in the future (`updatedAt 10:59Z` against `now 00:59Z`), so the reconcile never fired. Socket proof P1 failed for that reason alone. After `ALTER DATABASE ... SET timezone='UTC'` it passed. This is the same rule and the same exposure as the documents reconcile (`anchorStateSync.ts`, pre-existing; ks1114 pins UTC), and it fails in the safe direction (no read). Not introduced here.

### G420-8 (Note): the verify answer still returns the raw stored `blockchain` blob next to the honest flag
- Unchanged by this PR and pinned by the builder's K9. A simulated placeholder `txHash` or a `submitted` blob is still shown verbatim beside `blockchainAnchored:false`. Out of scope; recorded.

### G420-9 (Note): process disclosures (the gate's own)
- I used `cd` twice, inside a `bash <<EOF` subshell and only inside my own `_work` (`npx tsc` to build packages/shared per arm). Every later run used `cwd=` in a Python runner. There were no other deviations.
- **node_modules provenance:** cloned with `cp -c` from `s-w77-fix` after a lock-equality check (root, originate and shared lock sha256 equal on both arms). packages/shared `dist` was built by me on each arm.
- Mutant GM2 (the reconcile's own bearer gate removed) **survives as an EQUIVALENT**: `syncCertificationAnchor` refuses an empty bearer itself (:63).

## Part 1 conformance table (derived from code, measured on the real router)

Harness: the real `certificationsRouter` and real `certificationAnchorSync`. The certification repository, db, charges, notifications and events are mocked; auth is mocked to a principal. Requests go over a loopback express server, and every non-loopback fetch is recorded. Each certification is `issued`, unexpired, with its hash intact. Party = the issuer's userId; non-party = another same-tenant userId; signed-in calls send `Authorization`.

**Constant across ALL 84 calls (28 shapes x 3 callers), measured:**
- status 200 and `verified: true`;
- outbound calls 0, `writeCertificationAnchorConfirmedIf` calls 0, `saveCertification` calls 0;
- anonymous: charge calls 0, `chargeEventId` null, `issuer {id:null, did:null}`;
- party: charge calls 1, `chargeEventId` set, issuer id and did named;
- non-party: charge calls 1, `chargeEventId` set, `issuer {id:null, did:null}`.

| blob | blockchainAnchored (anon / party / non-party) | develop |
|---|---|---|
| none (undefined) | false / false / false | false |
| null | false / false / false | false |
| submitted (txHash null, pending-onchain, createAttempts) | false x3 | **true** |
| failed (status failed, anchorId null) | false x3 | **true** |
| anchor_failed (64-hex tx, height 10) | false x3 | **true** |
| anchor_failed + `anchored:true` | false x3 | **true** |
| simulated:true, `tx_sim_` hash | false x3 | **true** |
| simulated:'false' (truthy string), real hash, confirmed | false x3 (KS-1628 truthy rule) | **true** |
| confirmed, 64-hex hash, height 4242 | **true** x3 | true |
| confirmed, UPPER-case 64-hex | true x3 (REAL_TXHASH_RE is /i) | true |
| confirmed, height null | true x3 | true |
| confirmed, height '4242' (digit string) | true x3 | true |
| confirmed, non-hex hash | false x3 | **true** |
| confirmed, `tx_` + 61 hex | false x3 | **true** |
| confirmed, height 0 / -1 / '04' / 4.2 | false x3 each | **true** |
| status 'CONFIRMED' (upper) | false x3 | **true** |
| chain-first `{anchored:true, 64-hex, height 99}` | true x3 | true |
| `anchored:'true'` (string) | false x3 | **true** |
| `anchored:true` + status submitted + 64-hex (G420-4) | **true x3** | true |
| `__proto__`/`constructor`/`toString` own keys, no status | false x3 (no pollution: proto status ignored) | **true** |
| extra keys (confidence, anchoringStatus, nested) on a confirmed blob | true x3 | true |
| array blob / string 'confirmed' / boolean true | false x3 each | **true** |

Instrument: `_work/out/g420m_head.log` and `g420m_dev.log`. The full table (every column) is in the G420TABLE block. Control: on develop the same file answers `true` for every non-empty shape, and R-c (the party GET reconcile) is red there, so the harness discriminates.

## Part 2 and reach, measured

- **Writer (DB, my Postgres 15, superuser connection):** builder D1 to D7 7/7 green. Gate cells:
  - G1: a malformed id rejects and the row is unchanged.
  - G2: NULL tenant, NULL anchorId, empty anchorId and `g_a1' OR '1'='1` each write 0.
  - G3: a blob only in `metadata` (certification_metadata.blockchain is JSON null) is found and written in both copies.
  - G4: expired stays expired; a deleted row is written (G420-5).
  - G5: two concurrent writes, exactly 1 lands, and the stored hash is that one's.
  - G6: see G420-5.
  - G7: certification_metadata.blockchain = JSON false gives 0 rows (safe direction).
  - G8: status, content_hash, title and external_id are untouched and updated_at moves; a document row with a uuid external_id gives 0.
  - G9: other certification_metadata keys survive.
  - 16/16 green, rc 0.
- **Binding** (gate R-d, R-e and the builder's S2, S5, S6):
  - A confirmed row whose payloadTimestamp is not a create attempt gives no write (own-create none).
  - A row naming another documentId gives no write.
  - A different anchor cannot be written: the writer requires the stored `anchorId` to equal the one read, and the poller re-checks `certificationAnchorInFlight(cert) === anchorId` on a fresh read.
- **Reach:**
  - An anonymous GET is 401 with 0 outbound calls (R-a).
  - A non-party GET is 404 with 0 outbound calls and 0 writes (R-b); M12 shows the order is pinned by PIN R8.
  - A party GET (R-c) makes 1 `GET /api/anchors/a_sub` with the caller's bearer, 1 write keyed (id, tenant, anchorId) and 2 reads.
  - A write that throws still gives 200 with the stored blob (R-h).
  - A signed-in principal with no Authorization header causes 0 outbound calls (R-j).
- **Poller:**
  - Bearer expiry: anchoring answers 401, `fetchAnchorState` returns null, the poller continues, then exhausts after 60 x 10 s. The GET reconcile heals later (code read; same as the document poller).
  - Anchoring down: socket P3 against an unreachable port gave no write and a quiet exhaustion.
  - A refused anchor at issue: `anchoringStatus` failed and no poller (builder PIN R3; code read, certifications.ts 776).
- **G420-SP socket proof (built and run):** the real router, real certificationRepo, real certificationAnchorSync and real Postgres (TimeZone UTC). The stub anchoring is a real `http.Server` on 127.0.0.1 via `ANCHORING_SERVICE_URL`; only auth is mocked.
  - P1:
    1. An anonymous verify answers `false` with 0 stub hits.
    2. A non-party GET answers 404 with 0 stub hits.
    3. A party GET answers 200 with the blob `confirmed` and makes exactly 1 stub hit, `GET /api/anchors/g_sock_1` with `Bearer g420-socket`.
    4. The DB row is `status certified`, blob `confirmed`, txHash e5x32, blockHeight 321, and `confidence` dropped.
    5. An anonymous verify then answers `true` with 0 stub hits.
  - P2: the poller confirms over the socket. A second poller for the same anchor makes 1 read and writes nothing.
  - P3: see Poller above.
  - 3/3 green. `_work/out/socket_head.log`.

## Existing document behaviour

- `documentRepo.ts`: blob `da2c08ca4c38` at develop and at head, so **byte-equal**.
- `anchorStateSync.ts`: a word diff shows only `+export` x2 (`confirmedBlobOf`, `RECONCILE_STALE_MS`) and 2 comment lines; there are 0 import lines changed.
- Document suites (ks1384-r2b-*, ks535, ks587, ks1074, ks1333 and the rest) are green inside jest WHOLE at head, 3770/3770. The integration document suites are identical on both arms (226 identical failures, environmental; G420-3).

## Re-runs (my clone; each rc read from its own .rc file)

| stage | head | develop |
|---|---|---|
| originate tsc --noEmit | rc 0 (plant control: rc 2, 1 TS error, restored sha equal) | rc 0 |
| originate jest WHOLE | 251 files, 3770/3770, rc 0 | 249 files, 3738/3738, rc 0 |
| originate integration WHOLE (my PG15, superuser, Australia/Sydney) | 32 files, 420: 193 pass, 226 fail, 1 pending | 31 files, 413: 186 pass, 226 fail, 1 pending |
| same, 9 files with a secuura_app role added | 122: 47 pass, 75 fail | identical per file |
| packages/shared vitest WHOLE | 1747: 1746 pass, 1 fail (KS-278 wallet-signature) | identical |
| check.cjs services/originate | 349 files examined, 0 errors, 0 new | 345 files, 0 new |
| eslint, the 8 changed TS files | 0 errors; 1 warning, certificationRepo.ts:68 preserve-caught-error | the same warning on develop |

**Mutants:** 9 sampled. Each compiled (tsc rc 0) and was restored with its sha256 asserted.

| mutant | killed by | result |
|---|---|---|
| M1 (flag back to presence) | K1, K6 | KILLED |
| M3 (tenant predicate) | D2 | KILLED |
| M4 (never overwrite a confirmed blob) | D3 | KILLED |
| M5b (`external_id IS NULL` dropped) | D5 | KILLED |
| M7 (anchorId predicate) | D6 | KILLED |
| M12 (reconcile before the party check) | PIN R8 | KILLED |
| M10b (any document row accepted) | S6 | KILLED |
| GM1 (gate) | the gate matrix only | G420-2 |
| GM2 (gate) | none | EQUIVALENT |

Instrument: `_work/out/mutants_g420.json`.

**Test edits:** the ks1699v diff is exactly V-A9's two expectation rows flipped to `blockchainAnchored: false` plus a 4-line KS-2366 comment; there is no other change in the file. V-A9 still asserts its name: anonymous, 200, `verified:false`, the matching checks, 0 charges. None of the 48 suites that mock `../routes/verification` with a closed factory calls the certification verify route. 15 of them load the certifications router; a grep for `/verify` finds only an unrelated auth path in ks2275. So nothing is disarmed today; the latent trap is listed in the PR body.

**PR state re-read (gh as kksecura):** at 11:39 and again at 11:59 AEDT, PR 2295 open, head dbceb300851b6b76552614a25c0c1d03f6ac96bf, base develop 59e89c87719e76205c141e7a52f882b0693d0913 (unmoved), 10 files +905 -8.

## NOT TESTED

- The real anchoring service, a real Cardano confirmation, own-create against the chain, and anchoring's 30 s and 60 s cache behaviour (stubbed or recorded only).
- The gateway in front of originate, and multi-tenant mode (TenantPoolManager).
- The DB-backed issue and recertify routes end to end: they fail environmentally on a bare cluster on both arms (G420-3). Their new lines are covered by unit cells and by the socket proof of the poller only.
- RLS with a tenant GUC on the new writer: all my DB cells ran as superuser. The background poller's tenant scope relies on AsyncLocalStorage propagation, the same pattern as the document poller; read, not run.
- Bearer expiry against a real auth service (by code reading only). The 10 stuck Kintsugi certifications (LISTED, not covered by this PR; by design they now read `false`). Consumers outside `Blockchain/Dev`. Leg 16 for the other five services (I ran originate only). The docs-fragments checker. Legs 3, 4 and 8 of the pre-push hook (the builder's hook said INCOMPLETE, 13/16; not a pass). Any browser or deploy.
- I did not run the builder's remaining 13 mutants.

Cleanup: my Postgres (`/private/tmp/g420/pg_head`, loopback, port 58579) was stopped at 11:59 AEDT (`pg_ctl stop` rc 0), and its data was kept. I did not touch the builder's trees or clusters (s-w77-*): I only read them, and cloned node_modules from s-w77-fix with `cp -c`. Nothing was pushed, commented, written to Linear or GitHub, merged or deployed.
