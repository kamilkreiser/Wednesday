## BLUF

Product bytes in the originate documents route and shareRepo, plus two structural cells, three mock
surfaces, and the behavioural rollback suite for the integration config.

/share wrote its recipients one statement at a time, and /transfer-custody wrote the custody event and
the owner flip separately - its comment accepted that window in writing ("Prisma's $executeRaw doesn't
compose nicely ... we accept a small window where the event row exists without the doc-owner update").
A refusal at recipient k > 1, or a throw between the two transfer writes, left rows behind for an action
that did not happen, and since KS-1228 with no action_provenance row either. Both are now ONE transaction.

WHY withTenant AND NOT db.$transaction - the measurement that changed this ticket's shape.
`req.db` / the `prisma` export is a Proxy (db.ts:157-187) that wraps ONLY the four raw SQL methods, each
in its OWN $transaction carrying set_config(..., is_local=true). `$transaction` is not in that set, so
`db.$transaction(...)` falls through bound to the REAL client with NO tenant GUC - and the proxy's own
comment states the consequence: "No scope -> call through directly (fail-closed: zero tenant rows)". The
obvious implementation of this ticket would have shipped a write that silently matches nothing.
`withTenant()` (db.ts:302-336) is what composes: ONE checked-out client, BEGIN, both set_config GUCs, the
callback, then COMMIT or ROLLBACK. Handed that open client, createPoolProxy queries it directly instead
of re-bundling (db.ts:24-26), which ks458-db-tenant-guc.test.ts:111 already pins.

WHY IT IS UNCONDITIONAL, NOT "(req as any).db WHEN PRESENT" - measured, with the call sites:
  - services/originate/src/index.ts:225 sets `(req as any).db = getRequestPrisma(req)` inside middleware
    mounted at :219, BEFORE app.use('/api/documents', documentsRouter) at :270 - gated on
    MULTI_TENANCY_ENABLED === 'true'.
  - services/originate/src/routes/adminConfig.ts:30 also sets it, on a different router.
  - deployment/azure/services.bicep:798 sets MULTI_TENANCY_ENABLED to 'true'; docker-compose.yml defaults
    it to false at all 11 services, so local and the VM demo do not take that path today.
On that path `req.db` is createPoolProxy(pool), which bundles BEGIN + set_config + COMMIT around EACH
statement. A chooser honouring req.db would therefore give two transactions again - the very defect this
ticket removes - on exactly the deployment shape that has multiple tenants. So req.db is not consulted.

Errors THROW out of the callbacks rather than returning a response: a `return res.json(...)` inside a
withTenant callback resolves it normally and COMMITS the partial write. The response mapping happens
after the rollback.

createShare's `db` parameter is widened to `DbClient | TenantTx`. It only ever calls $executeRaw (twice);
DbClient = typeof prisma required $disconnect, which TenantTx does not carry and createShare never uses.
Widened on that one signature; the other two in the file are untouched.

Test evidence
- Touched: routes/documents.ts, repositories/shareRepo.ts, three test files' `../db` mocks, and a new
  integration suite. No byte outside services/originate.
- Ran: originate jest --runInBand 74 suites / 865 tests, rc 0 (bare baseline 863 -> 865, the two
  structural cells). tsc --noEmit rc 0. packages/shared vitest 46 files / 918 tests rc 0 on a re-run;
  the first run returned 5 TIMEOUTS and ZERO assertion failures (the four KS-1155 repo-walk guards plus
  threadToken at 40231 ms against its 30000 ms budget, which is KS-1155's fix-shape 3). Both runs reported.
- STRUCTURAL red-proof, ran and built: at head the ks1228 file reads 29/29 green. With the writes SPLIT
  (the owner flip moved off the tx client, and withTenant moved inside the recipient loop) it reads
  2 failed / 27 passed, and the two are EXACTLY the new G-S1 and G-S2 cells. Restored byte-identical
  by sha256.
- The mock surface was measured, not blanket-edited: 38 suites mock '../db'; a tightened grep predicted
  3 would need withTenant, and the suite run confirmed exactly those 3 failed (ks1228, ks697, ks739).
  Each mock hands the callback the SAME client that suite already observes.
- NOT RUN, and OWED AT THE GATE: the BEHAVIOURAL rollback cells. A mock cannot roll back, so the unit
  harness cannot prove them at all. They are written as
  src/__tests__/ks1263-multi-write-rolls-back.integration.test.ts for jest.integration.config.js against
  a real Postgres, covering D1/D2 (a throw after the first of two share rows leaves ZERO) and C7 (a throw
  after the custody INSERT leaves ZERO), plus a COMMIT control. The suite is DB-gated and never silently
  skipped. VERIFIED THAT IT LOADS: run without a database it compiles, imports and reaches beforeAll,
  failing with its own setup error rather than a parse or import failure - so it will not arrive at the
  gate unable to run. It should be run once per withTenant branch where the stack allows:
  MULTI_TENANCY_ENABLED=false (the Prisma interactive-transaction branch) and =true (the pool branch).
  If the stack cannot bring up the multi-tenant shape, the pool-branch proof stays a KS-1263 residual and
  is not implied.
- Preflight legs: 12/15 ran; legs 3, 4, 8 NOT run (local stack not up). This PR HAS a route-handler
  surface, so those legs are OWED AT THE GATE.
- Migrations + config: none.


Refs KS-1263

🤖 Generated with [Claude Code](https://claude.com/claude-code)
