# KS-1120 R15-F2 - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 0 lines read whole)
File: `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1120-f2-db-miss-falls-through-to-memory.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `vitest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1120-F2_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 4472 B sha256[:16] `1cda5b10d1096a4e`, +109/-0.
- The old patch at the tip: strict rc 128 / --recount rc 0 / --directory=Blockchain/Dev rc 128 / -R rc 128 -> effective mode **--directory+--recount**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1120-f2-db-miss-falls-through-to-memory.test.ts` at the tip: ABSENT - ONE NEW FILE. Mode: **NEW**.
- Tamper source: the old brief `night/briefs/KS-1120.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1120: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-1120-F3.md, KS-1120.md, KS-1120.md.f2-held-2026-09-15.
- Generator notes: Runner: vitest INFERRED for vc-issuer (vitest.config.ts present; package.json lists both) - Wednesday confirms.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them at tip 2026-09-15; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1120-F2 — Ornith ornith:35b-q8_0 PASS 7/7 first run on q8 (the q4 twin is held beside it; either may be raised), TEST-ONLY mode, 2026-09-15 12:33 — tip develop M55 48e65c435
> # Run: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-15_ks1120-ornith35b-q8_0-night. Cells as the brief's; red under the tamper, green at the tip. HELD for a Secuura seat.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode --directory+--recount - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1120-f2-db-miss-falls-through-to-memory.test.ts` then ONE `@@ -0,0 +1,N @@` hunk, every line `+`, no context, no `-`. No product hunk. 

## The exact change
```
+/**
+ * KS-1120 F-2 - TEST ONLY. The DB-miss path in `getPresentation` falls through
+ * to the in-memory store; this file pins that behaviour so a future tamper
+ * (`return undefined` after the DB miss) reddens these cells immediately.
+ */
+
+import { describe, it, expect, beforeAll, vi } from 'vitest';
+
+// Controllable stand-ins for ../db - each describe scripts its own behaviour.
+const dbMock = vi.hoisted(() => ({
+  isDbAvailable: vi.fn<() => boolean>(() => false),
+  query: vi.fn<(sql: string, params?: unknown[]) => Promise<{ rows: any[] }>>(),
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => dbMock.isDbAvailable(),
+  query: (sql: string, params?: unknown[]) => dbMock.query(sql, params),
+}));
+
+// Silence the winston logger the way db.retry.test.ts does.
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+type Router = (rq: any, rs: any, nx: (e?: unknown) => void) => void;
+type Mods = { router: Router; errorHandler: any };
+
+async function freshModules(): Promise<Mods> {
+  vi.resetModules();
+  const { presentationRoutes } = await import('../routes/presentations');
+  const { errorHandler } = await import('../middleware/errorHandler');
+  return { router: presentationRoutes as unknown as Router, errorHandler };
+}
+
+function dispatch(mods: Mods, method: string, url: string, body?: unknown): Promise<{ status: number; body: any }> {
+  return new Promise((resolve, reject) => {
+    const req: any = { method, url, baseUrl: '', originalUrl: url, headers: {}, body };
+    const res: any = {
+      statusCode: 200,
+      status(code: number) {
+        this.statusCode = code;
+        return this;
+      },
+      json(payload: unknown) {
+        resolve({ status: this.statusCode, body: payload });
+        return this;
+      },
+    };
+    const next = (err?: unknown) => {
+      if (err) mods.errorHandler(err as Error, req, res, () => {});
+      else reject(new Error(`route did not match ${method} ${url}`));
+    };
+    mods.router(req, res, next);
+  });
+}
+
+function getById(mods: Mods, id: string) {
+  return dispatch(mods, 'GET', `/${encodeURIComponent(id)}`);
+}
+
+function baseCredential(): Record<string, unknown> {
+  return {
+    '@context': ['https://www.w3.org/2018/credentials/v1'],
+    id: 'urn:uuid:ks1120-test-credential',
+    type: ['VerifiableCredential'],
+    issuer: 'did:prism:secuura_test_issuer',
+    issuanceDate: '2026-01-01T00:00:00Z',
+    credentialSubject: { documentHash: 'ab'.repeat(32) },
+  };
+}
+
+describe('KS-1120 F-2 - DB path with a memory-only row answers 200 via the fallback', () => {
+  let mods: Mods;
+  let storedId: string;
+
+  beforeAll(async () => {
+    dbMock.isDbAvailable.mockReturnValue(true); // THE DB PATH - difference from ks1020's memory describe
+    dbMock.query.mockReset();
+    dbMock.query.mockRejectedValue(new Error('insert refused in test')); // seed INSERT fails -> row lives ONLY in memory
+    mods = await freshModules();
+    const created = await dispatch(mods, 'POST', '/', { credentials: [baseCredential()] });
+    expect(created.status).toBe(201);
+    storedId = created.body.presentation.id;
+  });
+
+  it('RED KS-1120 F-2 - a row present in memory and absent from the DB answers 200', async () => {
+    const r = await getById(mods, storedId);
+    expect(r.status).toBe(200);
+    expect(r.body?.presentation?.id).toBe(storedId);
+  });
+
+  it('RED KS-1120 F-2 - exactly one exact-id SELECT ran, then memory answered', async () => {
+    dbMock.query.mockReset();
+    dbMock.query.mockResolvedValue({ rows: [] }); // every later SELECT is a DB MISS
+    const r = await getById(mods, storedId);
+    expect(r.status).toBe(200);
+    const calls = dbMock.query.mock.calls as Array<[string, unknown[]]>;
+    expect(calls.length).toBeGreaterThan(0);
+    const hasExactSelect = calls.some(([sql]) => String(sql).includes('WHERE id = $1') && (calls.find(([_, p]) => p?.[0] === storedId)));
+    expect(hasExactSelect).toBe(true);
+  });
+
+  it('KS-1120 control - an unknown id is 404 on the DB-miss path', async () => {
+    dbMock.query.mockReset();
+    dbMock.query.mockResolvedValue({ rows: [] });
+    const r = await getById(mods, 'urn:uuid:not-stored');
+    expect(r.status).toBe(404);
+  });
+});
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1120 F-2 - a row present in memory and absent from the DB answers 200`
- `RED KS-1120 F-2 - exactly one exact-id SELECT ran, then memory answered`
- `KS-1120 control - an unknown id is 404 on the DB-miss path`  (CONTROL - green on both trees)

## Tampers
### F2
File: `Blockchain/Dev/services/vc-issuer/src/routes/presentations.ts`
Line: 128
From:
```
  const exact = memPresentationStore.get(id);
```
To:
```
  const exact = Array.from(memPresentationStore.entries()).find(([k]) => k.startsWith(id))?.[1]; // TAMPER: a prefix scan
```
Reds: `RED KS-1120 F-2 - a row present in memory and absent from the DB answers 200`, `RED KS-1120 F-2 - exactly one exact-id SELECT ran, then memory answered`
(From located at the tip: 1 match(es); the old brief/input said line 128)

## Controls
- `KS-1120 control - an unknown id is 404 on the DB-miss path`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/vc-issuer/src/__tests__/ks1120-f2-db-miss-falls-through-to-memory.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
