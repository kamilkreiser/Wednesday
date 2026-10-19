VERDICT: NO GO at head b7de864640032c3b118c5aaa9e4e45b777ef67af (tier 1, round 1 of 2; landing tree 0cd7fa8095b46f2401724612ef14aca6f66561ad on develop a0da739b6954d42333640ea190d877f031803c7f; 1 blocker, 9 notes)

# Gate AI1: PR #1623 (KS-1633), Opus, tier 1, round 1 of 2

Gate: claude-opus-5-5, row G1. Findings only. Nothing written under `!CODING`, no push, no GitHub or Linear writes.
Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/ai1/` (my own clone `repo/`, logs `logs/`, mutants `mut/`, probe `probe/`).
Scratch PostgreSQL 15.14 on 127.0.0.1:55421, TCP only (`-k ''`), timezone UTC. Provisioned from `docker/init/*` plus the project runner: **54 applied, 0 failed**. The server was started with PGHOST/PGPORT/PGUSER set to itself, so the dblink in `00-create-platform-db.sql` connects to this server and no other. My first start did not have them set, and that one dblink call reached the default unix socket and failed there with `role "secuura" does not exist`, so nothing was created on that server. I then wiped and re-provisioned my own database. Harness assumption N4: the `tenants` table is not in the tenant DB, so I loaded `docker/init-platform/01-platform-schema.sql` into it (1 error, `idx_vault_token already exists`) and re-applied the product's own `secuura_app` grant line.

## Heads
- At start: develop `f321e95aa`, #1623 `b7de86464` (ls-remote; both match the brief).
- **Before the verdict (10:14Z): develop had MOVED to `a0da739b6`** (KS-1402, 6 files, all `transfer-custody`/`documents.ts`). #1623 is still `b7de86464`.
- merge-tree on the start develop gives `ffb064f00e54…`, which is the author's prediction (it equals the head's own tree, because the merge-base is develop). **On the LIVE develop it gives `0cd7fa8095b4…`.** Overlap between develop's move and the PR's files is **0**; control: the PR's list against itself gives **6**.
- Three-dot `origin/develop...b7de86464` lists **the PR's 6 files** exactly: ks1228, ks1538 (unit), ks1633 (new), ks543, `certificationRepo.ts`, `certifications.ts`.
- Every count below was re-run on the live landing tree `0cd7fa80` (detached commit `49e0ccb6d` in my clone), unless it is marked as run at the head tree.

## BLOCKER

**B1. The provisional write now runs before the production 503, so in production, with anchoring unavailable, any save-time refusal replaces today's 503.** The provisional write is `services/originate/src/routes/certifications.ts:507`. The production 503 is `:549`. On develop the 503 came first and nothing was saved.
Measured through the real router on scratch PG as `secuura_app`, develop's product files against the head's. Status and body are compared byte-for-byte after uuids and timestamps are normalised. Both tenancy modes give the same result:

| case (NODE_ENV=production, anchoring on a closed port) | develop | head |
|---|---|---|
| C12: the Platform S connector principal `connector:platform-s:<guid>`, no holderId (KS-1659's 22P02 shape, the live connector shape) | **503** SERVICE_UNAVAILABLE "Blockchain anchoring service is temporarily unavailable…" | **400** BAD_REQUEST "Certification payload contains values that cannot be stored" |
| C11: a NUL byte inside `data` (22P05) | **503** (same body) | **400** (same body as above) |
| C13p: the certification write throws a non-pg error | **503** (same body) | **500** INTERNAL_ERROR "Failed to issue certification" |

Controls:
- With anchoring UP, C12c and C11c answer **400 on both sides**. They are genuinely save-time refusals.
- C02, the plain production 503, is **identical on both sides**.

None of these differences is an echo of a new internal id. The ruling asked for "every response byte-identical", so this is a contract change on a path that can be reached in production. By the same logic a transient DB failure at that point would now return the KS-203 503 with a different message ("Certification service is temporarily overloaded"). I reasoned that last case from `:806-819` and did not measure it.

## Answers to the brief's questions

**Q1. Byte-identical responses?** **20 cases** per mode, both modes:
- **16 identical:** success; prod 503; non-prod failure 201; holderId not a uuid, 400; holderId unknown, 400; type missing, 400; unauthenticated, 401; role not permitted, 403; KS-1538 legacy document of another user, 403, with own-document control 201; KS-1557 parent of another user, 403, also in production with anchoring down; persist-then-500 in production, 503; plus the 400 controls.
- **1 differs only by a new-id echo:** C10c's `derivedDocumentId` `doc-<ms>-<certId8>`. Exempt.
- **3 differ:** B1.
- Side effects: on develop, C11c/C12c/C13n each left **1 orphan anchor**. On the head they leave **0**. That is the fix working.

**Q2. Compensating delete:**
- It runs inside `withTenant` (`certificationRepo.ts:156`). That sets both `app.tenant_id` and `app.current_tenant_id` (`db.ts:329-336` / `:357-359`).
- `removed !== 1` is logged as a failed compensation (`certifications.ts:558`).
- psql as `secuura_app` (rolbypassrls f), the author's finding reproduced:
  - outside a transaction: `DELETE 0`, row still present;
  - inside a transaction with only `app.tenant_id` (the author's mis-key): `DELETE 0`;
  - positive control, inside a transaction with `app.current_tenant_id`: `DELETE 1`, and the row is gone.
- VC FK: **no product code inserts into `verifiable_credentials`.** The grep found only DDL and indexes; the positive control is the `INSERT INTO documents` hit in certificationRepo. So through the product, a fresh certification cannot hold a credential before the compensation runs.
- With a credential planted between the write and the delete (probe S3, both modes): the delete throws 23503 (`verifiable_credentials_document_id_fkey`), the response is the **identical 503**, **1 row remains with no anchor**, and **1 error line names the id**.

**Q3. Orphan anchors.** My stub persists the anchor before it answers, the same as the author's. ORDER is green, and the stub saw the provisional row at anchor time.
- After the anchor POST the only step that can throw is the second save (`:589`). Every later step is caught.
- **One failure leaves an orphan: anchoring persists its row and then answers non-2xx (or times out) in production.** Probe S2, persist-then-500: **1 new orphan anchor on the head and 1 on develop**. The compensation deletes the row the anchor names. This is not a regression, but the PR's "removes the window rather than narrowing it" overstates it (see N2). The same case outside production keeps the row ('failed'): 0 orphans.
- Reverse direction (a documents row with no anchor where today there is none):
  - the delete throws or removes 0 rows (measured: DELETE-FAILS, S3);
  - a crash between `:507` and the anchor POST (reasoned);
  - the multi-tenant tenant-pool split in N4 (reasoned).

**Q4. Kam's (b).** Measured in both modes:
- After a failed anchoring outside production, the stored `certification_metadata.blockchain` is `{status:'failed', anchoringStatus:'failed', anchorId:null}`.
- On the accepted path it is `{anchoringStatus:'submitted', anchorId:<id>}` with no `status`.
- **The state between the two writes, read from inside the anchoring stub, is `{status:'failed', anchoringStatus:'failed'}`.** That is exactly what a crash would leave.
- /recertify (head `:1296`/`:1335`, base `:1290`) is byte-unchanged: a 219-line diff came out empty, and its F4-2 cell passes.
- A crash was NOT reproduced: no process was killed mid-request.

**Q5. F4-3 and save counts.**
- The F4-3 diff matches the claim: old `calls[0]`; new asserts 2 calls, the provisional `{failed, null}`, and reads the last call.
- Planted single-write regressions both red F4-3 ("Expected length 2, Received 1"), with tsc 0:
  - M5a: no provisional, one save after the anchor;
  - M5b: provisional only.
- F4-2 is untouched by the diff and passes.
- My grep found the save-count assertions in ks444 ×4, ks1213 ×2, ks1538-unit ×5, ks543 ×2, ks1557-int ×2 and ks1538-int ×1, and all of them pass. I could not reconstruct the author's exact five-file, 205-cell set.

**Q6. N2 ordering pin.** M6 moves the KS-1557 access check after the cycle walk (tsc 0). It reds exactly the pin (403 expected, 422 received). KS-1557 integration still passes **13/13**, ks1633 passes 6/6 and ks1538-int passes 10/10, as the claim says.

**Q7. Red-first, mutants, landing:**
- New suite **6/6 MT=false, 6/6 MT=true** at the head tree and again at the landing tree.
- Red-first against develop's product: **3/6 fail** (ORDER, ORPHAN, DELETE-FAILS), both modes. F4-3 (new) reds against develop's product.
- My mutants on the compensation (tsc 0 for each):
  - M8, no delete: reds UNCHANGED-503 and DELETE-FAILS.
  - M7c, the delete runs with `app.current_tenant_id` cleared (a silent DELETE 0): reds UNCHANGED-503.
  - **M7b, `removed !== 1` changed to `removed < 0`: survives everything** (see N3).
  - M7, the bare module `prisma`: survives, and is equivalent in-request (see N3).
- Originate full unit suite on the landing tree: **125 suites / 1506 tests / 0 failed** (the same at the head tree).
- `tsc --noEmit -p services/originate`: 0.
- Test files type-checked with a scratch tsconfig that includes `src/__tests__`: **0 errors over 145 test files**. Positive control: a planted TS2322 in a scratch test file gives rc 2.

## Notes

- **N1.** On the accepted path `saveCertification` runs twice, and each call inserts a `certification_events` ISSUE row (`certificationRepo.ts:263`). Every accepted certification now has **2 ISSUE events, and the first records `anchoringStatus:'failed'`**. Measured: develop 1 event (`submitted`); head 2 (`failed`, `submitted`), both modes. No in-repo reader exposes it today: `getLineageEvents` is only filtered for RECERTIFY. It is still a lasting provenance record that says an anchor failed when it did not. This is a ruling question for Wednesday.
- **N2.** The orphan-anchor class is not fully closed. In production, when anchoring persists and then fails to answer 2xx (500, or the 10 s timeout at `:538`), the compensating delete removes the row that the anchor names: S2 measured 1 orphan on the head. This is the same as develop, but the code comment at `:463-467` and the PR claim "removes the window".
- **N3.** The "anything but 1 is a failed compensation" arm (`:558`) is unpinned: M7b survives all suites. Also, the UNCHANGED-503 cell does not prove that `withTenant` is needed in-request. A bare module-`prisma` delete (M7) also passes, because the KS-458 GUC proxy already scopes it inside the request context.
- **N4.** Reasoned, not measured. With MULTI_TENANCY_ENABLED=true and a real `req.tenantPool`, the provisional row is written through `req.db` (the tenant's pool, `index.ts:225`), but `withTenant` always uses `tenantManager.getDefaultPool()` (`db.ts:328`). For a tenant with its own database, the compensation would delete 0 rows from the default DB, log, and leave the row. The harness (mine and the author's) never sets `req.tenantPool`, so the MT=true runs do not exercise this.
- **N5.** M5b (provisional only, so every accepted certification stays stored 'failed', i.e. off-chain-only forever) is caught **only** by the mock-based unit F4-3. The real-PG ks1633 suite passes it 6/6, because no cell reads the stored state after success.
- **N6.** The provisional "failed" state is visible to concurrent readers (for example the tenant list endpoint) for the whole anchoring round trip, which can be up to the 10 s timeout. The PR calls it "sub-second". The stored state is conservative, so this is wording, not a defect.
- **N7.** Out of scope: /recertify still anchors before it saves (anchor POST before the `:1296` check, save at `:1339`), so the same orphan-anchor class remains on that route.
- **N8.** Develop moved during the gate: the landing tree is now `0cd7fa80` on `a0da739b6`, not the predicted `ffb064f0`. Overlap is 0 (control 6), and everything was re-run on the new tree.
- **N9.** The new suite's setup needs a `tenants` table in the tenant DB. The header says "these cells seed both", but they seed only the row (N4's assumption is real; I supplied the table from the platform schema).

## Integration suites (only originate is touched)
- RUN on the landing tree, both modes: ks1633-certify-writes **6/6, 6/6**; ks1557-lineage-certify **13/13, 13/13**; ks1538-legacy-certify (integration) **10/10, 10/10**.
- RUN, my probe (scratch only): 22/22 cells executed per mode per product.
- NOT tested: every other originate `*.integration.test.ts`, including develop's new ks1402 suite; the four Docker platform suites; anchoring, api-gateway and the other services (untouched by the PR).

## Not run
- No process kill in the crash window (reasoned only).
- No real separate tenant database (N4 reasoned).
- No concurrency.
- No lineage-cycle 422 through the real router (pinned only by the mocked unit cell).
- The KS-203 transient-503 combination with production anchoring failure (reasoned).
- No Docker, no live box, eslint not run.

c3731f58012923bf6c231bd64bb7e7516a2119cdf98991f80badba819610465a
