NO GO (G188-F1)
# QA Gate 188 (Tier 1, round 1): PR 2000 / KS-1561 verify certifies only for the original registrant

## Subject
- Repo Secuura/Distributed_Secuura, PR 2000, branch feature/ks-1561-verify-presents-a-later-hash-only-registrant-as-the.
- **Start** (09:32:18Z, ls-remote): head `d03b03046d76591aec3e5a3aa4176fb4e5b78e04`, develop `17c559555f31386fe4ec7a816677a2903db9cd76`. Merge-base `d92b849ece732cd04e283bfcb0ee9e8bd6989631` (measured in my clone, the same as the commission says).
- **End** (09:45:20Z, ls-remote): head `d03b03046d76` **unchanged**. Develop **moved** to `fe3f1371244890d7b609daa82d0c129cbcf67e0c`, which adds 1 commit (KS-1868, vc-issuer only, 6 files, 0 in originate). It does not touch the PR's files.
- **Merge tree, for the merge seat:**
  - head onto `17c559555f31`: rc 0, tree `5bb0da5bd0bdc7ddb6a6d4d9c7a3df7461fcba19`. Measured at the start and again at the end.
  - head onto the current develop `fe3f1371244890d7`: rc 0, tree `eb4893a841eb8e87dc14313b396dd43becd21e85`.
- Host: Node v26.8.1, npm 11.19.0, TypeScript 5.9.3, jest 29.7.0 (ts-jest). PostgreSQL 15 keg (Homebrew), run as my own cluster: unix socket only, under the workdir.
- **Not run on:** Node 24, kintsugi or demo, a deployed stack, Docker.
- Dependencies: one `npm ci --ignore-scripts` of services/originate in my `clone --shared`, matching the head lock (431 MB). df read 2.6 GiB free at the start and 2.0 GiB at the end.
- **Harness deviation (disclosed).** `@secuura/shared` is a monorepo workspace link and is not part of originate's lock.
  - My harness config (`jest.gate.config.js`, `tsconfig.gate.json`) maps it, read-only, to the shared checkout's `packages/shared/dist`.
  - `packages/shared` has the same source tree (`d94503e350c8`) at base, at head and at the checkout's HEAD.
  - Every verify suite wraps that module in `makeSharedMock`, which turns each function into a jest.fn.
  - That dist is older than its source: it lacks `signEmitterHop` and `zod3-compat`. So 1 neighbour suite could not load here (see NOT tested).
  - Nothing was written to the checkout. Its git status shows 3 untracked files that I did not write.

**Method.**
- I read the full diff and drove the real `verificationRouter` and `verificationV2Router` over HTTP on 127.0.0.1. Only the DB, the tenant manager and the chain fetch were mocked.
- I ran base against head by overlaying the base blobs of the two route files in my clone, then restored them with `git checkout <head>` and checked sha256 (verification.ts `d38281800e37daf6`, verificationV2.ts `b74625744a688d43`).
- I wrote my own cell file with my own fixtures (`harness/gate188-matrix.test.ts`). Its row-set mock MODELS the route's SQL: it applies `ORDER BY certified_at DESC NULLS LAST` and `LIMIT n` to the fixture. The seat's mocks return rows in whatever order they are handed.
- One SELECT was read on the real engine (PostgreSQL 15, schema `docker/init/01-schema.sql` at the head).
- The base-vs-head direction was computed by a script that reads what each cell recorded.
- I ran my own 8 mutants.
- Every zero below has a control run in the same action.

## Findings

### G188-F1 — MAJOR — FIX-BEFORE-MERGE: the "original" is computed over a truncated row set, so 24 later certified copies bring Seat J's outcome back on every path
- **FOUND:**
  - `certificationEligibility(rows)` takes D1's MIN(created_at) over the rows the route FETCHED. Every row-set fetch is `ORDER BY certified_at DESC NULLS LAST LIMIT 24` (VERIFY_ROWSET_LIMIT): verification.ts :594 (cross-tenant), :694-695 (verify-file), :1154-1155 (/verify), :1220-1221 (chain-first), and verificationV2.ts :295-296 and :329-330.
  - An uncertified original has certified_at NULL and sorts LAST. A certified original whose certification is older also sorts below newer ones.
  - So once 24 or more later rows are certified, the original is not in the set. The earliest fetched row (the later registrant's first copy) is then treated as "the original", and its holder's certification is presented.
  - D1 says the original is MIN(created_at) over **the hash's row set**, not over the 24 most recently certified rows.
  - Nothing stops one owner from registering the same bytes many times. `documents` has no unique key on content_hash: the conflict target is `external_id` (documentRepo.ts saveDocument), and 01-schema.sql has no unique index on content_hash. The legacy certify UPDATE sets `certified_at = NOW()` on each copy (certifications.ts :801-811).
  - Code comments in the repo name a real 576-row same-hash group (verificationV2.ts, the parity-sweep note). Groups larger than 24 rows exist in data, adversarial or not.
- **TESTED:**
  - Cell N-TRUNC: B registers H first (uncertified). A (a different owner, org NULL) registers H 24 more times and certifies each copy.
  - Head result: verify, verify-file, cross-tenant and v2 each present `certified: true`, `cert-a-24`, documentId `gate188-a24`. The planted issuer name `ZQX-PLANTED-ISSUER-A` is in the body on verify, verify-file and v2. v2 returns count 24, all A's copies, and B is absent.
  - Base gives the same result, so this is **not a regression**. It is the ruled outcome failing on the paths this PR changes.
  - Control N-TRUNC-23 (23 copies, so B is still inside the 24): head presents B, not certified, on all 4 paths. Base presents A certified on all 4.
  - Real engine: on PG15, the head's verify-file row-set SELECT, run against the real `documents` and `organizations` tables, returns `original_in_fetched_set = t` with 23 copies and `f` with 24. The earliest row in the fetched set becomes A's copy 1 (10:31Z instead of 10:00Z). See `runs/pg_trunc.txt`.
  - Not driven: registering and certifying 24 copies through the real `POST /documents` and `POST /certifications/issue` (rate limits, quotas, the KS-1538 access rule at volume). I did not measure whether this is reachable in production.
- **HOW:**
  - `bash runjest.sh head_matrix 'src/__tests__/gate188' --verbose` with GATE_OUT set to `runs/head_matrix.jsonl`. The same run at base gives `runs/base_matrix.jsonl`.
  - `psql -v n=23|24 -f harness/pg_trunc.sql` (transaction rolled back).
  - A fix shape that fits the ruling: identify the original from an UNTRUNCATED source, for example a separate `MIN(created_at)` read, or a row-set ordered by `created_at ASC` for the original rows, or always fetch the earliest rows. Then add a >24-row cell whose mock (or real engine) applies the route's ORDER BY and LIMIT.

### G188-F2 — MINOR: v1 judges "original" over the caller's own tenant only, while v2 judges it over every tenant, so the two disagree when the original is in another tenant
- **FOUND:**
  - v1 `/verify` (and verify-file) uses the local tenant's rows whenever any exist. crossTenantLookup and D4's ORDER BY run only when the local set is EMPTY.
  - v2 `matchesForHash` judges eligibility over local plus cross-tenant rows.
  - Case: B (the original, created 10:00) is in tenant 2, and A (later, certified) is in the caller's tenant.
    - Head v1 presents A's certification (`cert-a-split`), the same as base.
    - Head v2 presents B, uncertified, count 1, and leaves A out.
  - So on head, v2 matches[0] is not v1's answer (Q5's "matches[0] equals v1"). The parity sweep (`scripts/verify/ks584-p3-parity-sweep.mjs`) would report a mismatch for such groups. At base, v1 and v2 agreed: both presented A.
  - Head is not more permissive than base here, and v1 is unchanged from base.
- **TESTED:** cell N-SPLIT, with mocked tenant pools and registry. Base: green (agree). Head: red (v1 gives `gate188-a0`, v2 gives `gate188-b0`). Not measured: which tenant an anonymous Platform S verifier's `req.db` is bound to in pool mode, and whether one hash is spread across tenants in real data.
- **HOW:** `runs/head_matrix.jsonl` and `runs/base_matrix.jsonl`, cell N-SPLIT. This is a scope question for Wednesday: does D1's "row set" for v1 include other tenants? It is not FIX-BEFORE-MERGE on my reading of the ruling.

### G188-F3 — INFO: the seat's mocks cannot see ORDER BY or LIMIT, and its SQL cells are text matches
- **FOUND:**
  - The seat's `mockRows` returns its fixture as given, whatever the statement says. So no seat cell could have reached F1.
  - S1-S4, V7, V8 and X-REG assert statement TEXT. They are honest and red-first, but they are not an engine run. The seat states that a real Postgres run was NOT done.
  - My PG15 read covers only the verify-file row-set SELECT (column list, join, ORDER BY, LIMIT). It does not cover the D4 registry statement or the chain-first SELECT. I only READ that `platform_document_registry` has `id` and `created_at` (01-platform-schema.sql).
- **TESTED / HOW:** reading `ks1561-verify-original-registrant-certifier.test.ts` :173-181, and `runs/pg_trunc.txt`.

### G188-F4 — INFO (PRE-EXISTING, base = head): a later registrant's certified row is still shown as certified when looked up BY ITS OWN ID
- **FOUND:**
  - `respondExistenceOnly` (verification.ts :1061-1110, :1430) and the v2 documentId strategy (verificationV2.ts :437-461) present the NAMED row's own `status` and `buildCertification`. They answer `verified: false` and make no hash claim.
  - The seat's claim "unchanged" holds: no diff hunk touches :1061-1110. v2's by-id query is `LIMIT 1`, so `certificationEligibility(rows)` runs over a one-row set and its output is unchanged.
  - This is outside D1-D4 as worded ("verify(H)"). I list it so nobody assumes the by-id path was narrowed.
- **TESTED / HOW:** read at the head (the `git diff` hunk list), not driven.

## What passed (measured)
- **Q1 scope:**
  - `git diff --name-only d92b849e d03b0304` lists exactly the 6 files in the READY.
  - Pattern `api-gateway|migration|/config|.env|docker|prisma|package(-lock).json`: 0 hits. Control: the same pattern on the base history log hit 3.
- **Q2, the ruled outcome on Seat J's case** (my fixtures: B first, A later and certified, both org NULL, owners differ):
  - Head: verify, verify-file, cross-tenant and v2 all present B, `isCertified false`, and no certification.
  - v2 ids are `['gate188-b0']` with count 1. The planted issuer name, `cert-a-planted` and A's documentId are absent from all 4 serialized bodies.
  - Base: all 4 paths present `cert-a-planted`.
  - Control J-CONTROL (A holds the original): the planted name is visible on verify, verify-file and v2. On cross-tenant, `scopeTenantFields` nulls the issuer, so the name instrument cannot fire there; the planted certification ID is visible on all 4. So for cross-tenant the zero rests on the cert-id instrument.
- **Q3 over-blocking:** 7 shapes, each run on 4 paths except the lineage shape. Every one still presents its certification on head, and on base.
  - P1: the original holder certifies its own row.
  - P2: the same owner re-registers and certifies the later row (owner id in different case).
  - P3: same non-null org, different user.
  - P4: a KS-1557 lineage child of the original, certified by B's colleague (run on verify, verify-file and v2).
  - P5: rows tied at the earliest created_at.
  - P6: a single registrant.
  - P7: both certified. Head shows the original's older `cert-b-old`, not the newest `cert-a-new` (base showed `cert-a-new`).
  - Negative N-lineage-later (lineage child of the LATER row): head presents nothing, base presented it.
  - The seat's 14 P cells: green at head.
- **Q4, every reader at head:**
  - verification.ts:
    - `selectVerifiableRow` :285-298: gated (candidates :288-289).
    - `siblingCertification` :421-434: gated (:429 certified sibling, :433 evidence).
    - crossTenantLookup :617 and :628: through those two functions.
    - verify-file :790, :796-798 and :802: the selected row plus the gated sibling.
    - `buildResponse` :1007-1020: its single caller (:1345) passes the selected `docRow` plus the gated sibling. Cross-tenant `rows=[crossDoc]` is already a selection.
    - chain-first :1223 and :1234: `selectVerifiableRow` over a SELECT that now carries the identity columns.
    - `respondExistenceOnly` :1061-1110: the named row only, unchanged (G188-F4).
    - KS-1557 `resolveTrustedCertificationEvidence` :378-415: builds evidence only, and every presentation of that evidence is gated.
    - `chainBlobOfRow` :194 reads chain state, not certification.
  - verificationV2.ts:
    - `ownRowCertification` :133-142: `buildCertification` is ungated, but only `presentable` rows (:374) reach it on the hash path. Evidence is gated (:141).
    - `buildMatch` :164 and `matchRank` :253: over `presentable` only.
    - by-id :461: a one-row set.
  - Every path that can present ANOTHER row's certification goes through eligibility. The gap is F1 (an incomplete input set), not a missed reader.
- **Q5 v2 ruling (A):** an ineligible certified match is absent from matches and from the count (J: count 1). No field of it appears (the planted name and cert id grep, with the control). matches[0] equals v1's answer on every single-tenant cell (J, P1-P7). The exception is N-SPLIT (F2).
- **Q6 direction:**
  - Predicate: head presents a certification (v1 `checks.isCertified`; v2 any match certified or carrying a certification) where base presented none.
  - **Head more permissive than base: 0/48 cells**, across 12 shapes (11 shapes × 4 paths, plus the 4 lineage cells).
  - 32/48 are equal and 16 changed, every one toward less certification or the original's certification.
  - Control: the same script with base and head swapped flags 12/48. No HOLD-FOR-KAM condition on direction. No signature class (no production, money, human message or irreversible action) is touched.
- **Q7 fixtures :195 and :213:**
  - The diff has 13 added and 1 removed non-header lines. 0 expect lines; the 2 lines that matched "expect" are comments saying "No expect line changed".
  - All changes are `owner_user_id: P3_OWNER` or a comment.
  - With the BASE version of that test file on the HEAD routes, exactly those 2 cells go red (`runs/head_p3_basefixture.txt`). So the edit is needed and limited to them. Each cell still tests its title (order certified, then confirmed-tx, then oldest; and millisecond-precise certified_at).
- **Q8 my mutants:** 8 applied, 8 KILLED, 0 survived, 0 invalid. I counted the raw table in `runs/mutants.json`, and each file was restored to its pristine sha256.
  - M1, tie rule reduced to one original: killed by C11 and P5.
  - M2, same-owner clause off: C8, V6, P2.
  - M3, MIN inverted to MAX: 21 cells.
  - M4, identity compare made case-sensitive: killed only by my P2. **The seat's suite does not cover case.**
  - M5, same-org clause off: C9, P3.
  - M6, sibling evidence gate off: C7, N-lineage-later.
  - M7, v2 `presentable` filter off: V1, J, P7, N-TRUNC-23.
  - M8, selection candidates ungated: 10 cells.
- **Red first:**
  - Seat's new file: at base, 17 red by ASSERTION and 14 green. At head, 31/31. So I reproduced the seat's 17/14.
  - My file: at base J, P7, N-lineage-later and N-TRUNC-23 are red. At head they are green, apart from F1 (N-TRUNC) and F2 (N-SPLIT).
- **Neighbours at head:**
  - ks1561, ks584-verify-row-selection, ks584-p3-verify-list, ks584-p3-auth-error-classification, ks1557-trusted-certification-evidence, and two ks1628 suites: 132/132 across 7 suites.
  - `tsc --noEmit` (gate tsconfig): 0 errors in routes/verification*.ts. 9 errors elsewhere, all from the stale shared dist (TS2305 and TS2307 on `@secuura/shared` exports, plus their TS7006 follow-ons), in files this PR does not touch.

## NOT tested
- Node 24, kintsugi or demo, the live verify after deploy, and real Platform S traffic (excluded by design).
- The full originate suite. The 4 platform suites. Lint.
- `ks1628-deprecated-documents-verify-is-removed`: it could not load against the stale shared dist (`signEmitterHop` missing). This is environmental, not the PR.
- A real-Postgres run of the D4 registry statement and of the chain-first SELECT (read only), and of any route end to end (the routes ran on mocks; one SELECT ran on PG15).
- Whether F1 can be reached through the real register and certify APIs at volume (rate limits, quotas, KS-1538). Whether F2's tenant split occurs in data, and which tenant an anonymous verifier binds to.
- The lineage forward walk (`hasNewerCertifiedVersion` and newerVersions, which follow descendants, not same-hash rows): read, not driven.
- Over 8 tenants in v2's registry enumeration (`ORDER BY tenant_id LIMIT 8`, pre-existing): if the original's tenant falls outside those 8, v2 has the same class of truncation as F1. Read, not driven.

## Plain answer for Kam
- For the ordinary case this PR does what you ruled. When a second organisation registers the same file later and certifies its copy, verify now shows the original registrant's document as not certified, and no longer shows "certified by" the latecomer. Every way of verifying tested here behaves that way.
- It never makes anything look MORE certified than before.
- But it decides who is "original" from only the 24 most recently certified copies. A latecomer who registers and certifies the same file 24 times pushes the real original out of view, and gets "certified by" them back. I measured this on the real database query and the real verify code.
- That is a short fix (find the earliest registration from the full set) and should land before merge.
- A smaller gap: when the original sits in a different customer tenant, the old verify and the new list verify can now give different answers. That needs a ruling, not a fix.
