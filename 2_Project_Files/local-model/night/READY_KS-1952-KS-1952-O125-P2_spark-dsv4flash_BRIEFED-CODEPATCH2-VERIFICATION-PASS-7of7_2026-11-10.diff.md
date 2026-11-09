# READY — KS-1952-KS-1952-O125-P2 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1952_o125_p2_gateway_verification_route_answers_503_to_a_typed_create_while_redis_is_unavailable/out.md.checker/patch.diff`** (from `ls` at 03:26 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1952_o125_p2_gateway_verification_route_answers_503_to_a_typed_create_while_redis_is_unavailable/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1952_o125_p2_gateway_verification_route_answers_503_to_a_typed_create_while_redis_is_unavailable/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1952_o125_p2_gateway_verification_route_answers_503_to_a_typed_create_while_redis_is_unavailable/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1952_o125_p2_gateway_verification_route_answers_503_to_a_typed_create_while_redis_is_unavailable/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1952_o125_p2_gateway_verification_route_answers_503_to_a_typed_create_while_redis_is_unavailable-control-r5/out.md.checker/patch.diff` rc 0, Wednesday spark operator o125).

**Held 03:26 2026-11-10 by Wednesday spark operator o125 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1952_o125_p2_gateway_verification_route_answers_503_to_a_typed_create_while_redis_is_unavailable/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/verification.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1952-a-typed-create-answers-503-while-redis-is-unavailable.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	0	Blockchain/Dev/services/api-gateway/src/routes/verification.ts
2	1	Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts
117	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1952-a-typed-create-answers-503-while-redis-is-unavailable.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: verification.ts`
- CODE_PATCH2 (rung 3, 1 product files + 2 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/verification.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts`, `Blockchain/Dev/services/api-gateway/src/__tests__/ks1952-a-typed-create-answers-503-while-redis-is-unavailable.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/verification.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1952-a-typed-create-answers-503-while-redis-is-unavailable.test.ts 117 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1952-a-typed-create-answers-503-while-redis-is-unavailable.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=2 of total=9; red cell(s): ['KS-1952 a typed create answers 503 while Redis is unavailable RED ks1952 R1: Redis down, documentType named: 503 SERVICE_UNAVAILABLE, enforcement never runs, the connector shape', 'KS-1952 a typed create answers 503 while Redis is unavailable RED ks1952 R2: Redis down, the type named in the legacy `type` field: 503, enforcement never runs']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1882 failed=0 | after: total=1887 failed=0` · `NEW reds: []` [baseline_suite.json total=1882 failed=0; after_suite.json total=1887 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=1 tests=2 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (+7/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts` (+2/-1); 3 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/verification.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1952_o125_p2_gateway_verification_route_answers_503_to_a_typed_create_while_redis_is_unavailable/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1952_o125_p2_gateway_verification_route_answers_503_to_a_typed_create_while_redis_is_unavailable/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/verification.ts
@@ -922,2 +922,9 @@
       // --- Enforcement: validate document type rules ---
+      // KS-1952 (Kam's card secuura-ks1952-redis-down-doctype-rules-1110 = a): while Redis is unavailable the catalogue reads EMPTY, and
+      // enforcement passes a typed create with none of its rules. Refuse it with the connector allow-list's own 503 (line 840). Keyed on
+      // availability, NOT on an empty catalogue; an untyped create reads no catalogue and still goes on to enforcement.
+      if ((body.documentType || body.type) && !redisService.isRedisAvailable()) {
+        res.status(503).json({ success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Document type configuration is currently unreadable; refusing until it can be read' } });
+        return;
+      }
       const enforcement = await enforceDocumentTypeRules(body, req.user);
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks466-documents-enforcement-envelope.test.ts
@@ -57,3 +57,4 @@
     isDbAvailable: () => false,
-    redisService: {} as never,
+    // KS-1952: the route asks redisService.isRedisAvailable() before a typed create reaches enforcement; this fixture's Redis is up.
+    redisService: { isRedisAvailable: () => true } as never,
     services: {},
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1952-a-typed-create-answers-503-while-redis-is-unavailable.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1952-a-typed-create-answers-503-while-redis-is-unavailable.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1952-a-typed-create-answers-503-while-redis-is-unavailable.test.ts
@@ -0,0 +1,117 @@
+import { describe, expect, it, beforeAll, afterAll, afterEach, vi } from 'vitest';
+import express from 'express';
+import type { Server } from 'node:http';
+import type { AddressInfo } from 'node:net';
+import type { RequestHandler } from 'express';
+
+// KS-1952 (Kam's card secuura-ks1952-redis-down-doctype-rules-1110 = a, 2026-11-10 02:55:20): while Redis is unavailable the document-type
+// catalogue reads EMPTY and enforcement passes a typed create with none of its rules. POST /api/documents naming a documentType (or the
+// legacy `type`) must answer 503 SERVICE_UNAVAILABLE, the code the connector allow-list refusal uses (routes/verification.ts line 841),
+// while redisService.isRedisAvailable() is false, and enforcement must not run. The rule keys on availability, NOT on emptiness: Redis up
+// still reaches enforcement (an empty catalogue passes there, line 137 of services/enforcement.ts), and an untyped create is unchanged.
+// Harness: the real verification router over loopback HTTP (the ks1256 pattern), a signed-in ISSUER_ADMIN (a document-write role, no connector), enforcement replaced by
+// a spy that answers ok, and ONE knob: what isRedisAvailable() reports.
+let available = true;
+const availableSpy = vi.fn(() => available);
+const enforceSpy = vi.fn(async () => ({ ok: true as const, docType: {} }));
+const workflowSpy = vi.fn(async () => ({ gated: true as const, response: { success: true, data: { ks1952: 'past-enforcement' } } }));
+
+let gateway: Server;
+let gatewayPort: number;
+const realFetch = globalThis.fetch;
+const originate = { url: 'http://127.0.0.1:1' };
+
+beforeAll(async () => {
+  globalThis.fetch = (async () => ({ ok: false, status: 404, json: async () => ({}), text: async () => '' })) as never;
+  const { createVerificationRoutes } = await import('../routes/verification');
+  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
+  const app = express();
+  app.use(
+    createVerificationRoutes({
+      authenticateToken: () => (req, _res, next) => {
+        (req as { user?: unknown }).user = { userId: 'u-ks1952', email: 'ks1952@secuura.io', role: 'ISSUER_ADMIN', verificationLevel: 'standard', tenantId: 't1' };
+        next();
+      },
+      mockBodyParser,
+      query: vi.fn(async () => ({ rows: [] })) as never,
+      isDbAvailable: () => true,
+      redisService: {
+        getPendingDocument: vi.fn(async () => null),
+        deletePendingDocument: vi.fn(async () => undefined),
+        getAllDocumentTypes: vi.fn(async () => []),
+        getAllWorkflowInstances: vi.fn(async () => []),
+        isRedisAvailable: availableSpy,
+        getNotificationSettings: vi.fn(async () => null),
+        getRejectedDocument: vi.fn(async () => null),
+        setRejectedDocument: vi.fn(async () => undefined),
+        getWorkflowDocumentMapping: vi.fn(async () => null),
+        getWorkflowInstance: vi.fn(async () => null),
+        setWorkflowInstance: vi.fn(async () => undefined),
+      } as never,
+      services: { originate, anchoring: originate } as never,
+      log: () => undefined,
+      memWorkflowToDocumentMap: new Map(),
+      memRejectedDocuments: new Map(),
+      dbSaveRejection: vi.fn(async () => undefined),
+      ADMIN_ROLES: ['ADMIN', 'admin'],
+      enforceDocumentTypeRules: enforceSpy as never,
+      createWorkflowInstanceIfRequired: workflowSpy as never,
+    }),
+  );
+  gateway = app.listen(0, '127.0.0.1');
+  await new Promise<void>((r) => gateway.once('listening', () => r()));
+  gatewayPort = (gateway.address() as AddressInfo).port;
+});
+
+afterAll(async () => {
+  globalThis.fetch = realFetch;
+  await new Promise<void>((r) => gateway.close(() => r()));
+});
+
+afterEach(() => {
+  available = true;
+});
+
+/** POST /api/documents as a signed-in user; returns [status, error code or the past-enforcement marker, enforcement calls, error message]. */
+async function create(body: Record<string, unknown>): Promise<[number, unknown, number, unknown]> {
+  enforceSpy.mockClear();
+  workflowSpy.mockClear();
+  const r = await realFetch('http://127.0.0.1:' + gatewayPort + '/api/documents', {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' },
+    body: JSON.stringify({ title: 'KS-1952', contentHash: 'c'.repeat(64), ...body }),
+  });
+  const json = (await r.json()) as { error?: { code?: unknown; message?: unknown }; data?: { ks1952?: unknown } };
+  return [r.status, json.error?.code ?? json.data?.ks1952, enforceSpy.mock.calls.length, json.error?.message];
+}
+
+const REFUSED_MESSAGE = 'Document type configuration is currently unreadable; refusing until it can be read';
+
+describe('KS-1952 a typed create answers 503 while Redis is unavailable', () => {
+  it('RED ks1952 R1: Redis down, documentType named: 503 SERVICE_UNAVAILABLE, enforcement never runs, the connector shape', async () => {
+    available = false;
+    expect(await create({ documentType: 'SECURE' })).toEqual([503, 'SERVICE_UNAVAILABLE', 0, REFUSED_MESSAGE]);
+  });
+
+  it('RED ks1952 R2: Redis down, the type named in the legacy `type` field: 503, enforcement never runs', async () => {
+    available = false;
+    const [status, code, enforcementCalls] = await create({ type: 'SECURE' });
+    expect([status, code, enforcementCalls]).toEqual([503, 'SERVICE_UNAVAILABLE', 0]);
+  });
+
+  it('control ks1952 C1: Redis up, documentType named: reaches enforcement and is created (a fresh boot with an empty catalogue passes there)', async () => {
+    const [status, code, enforcementCalls] = await create({ documentType: 'SECURE' });
+    expect([status, code, enforcementCalls]).toEqual([201, 'past-enforcement', 1]);
+  });
+
+  it('control ks1952 C2: Redis down, UNTYPED create: unchanged, reaches enforcement and is created', async () => {
+    available = false;
+    const [status, code, enforcementCalls] = await create({});
+    expect([status, code, enforcementCalls]).toEqual([201, 'past-enforcement', 1]);
+  });
+
+  it('control ks1952 C3: Redis up, `type` named: reaches enforcement and is created', async () => {
+    const [status, code, enforcementCalls] = await create({ type: 'SECURE' });
+    expect([status, code, enforcementCalls]).toEqual([201, 'past-enforcement', 1]);
+  });
+});
```

---
## Operator o125 footer (appended after the hold; not generated by hold_ready.py)
**TIER 1 GATE OWED** (security enforcement, live API change; Kam's card secuura-ks1952-redis-down-doctype-rules-1110 = a, 2026-11-10 02:55:20). SITE: `routes/verification.ts` (not `services/enforcement.ts`): the enforcement.ts form turned 22 existing cells red in 7 other test files (control run `...ks_1952_o125_p1_...-control`, suite_delta.out). Carries a one-line fixture fix in `ks466-documents-enforcement-envelope.test.ts` (`redisService: {}` gains `isRedisAvailable`). 503 shape = the connector path's (`success:false, error:{code:'SERVICE_UNAVAILABLE', message}`). Typed creates by ANY caller now 503 for the length of a Redis outage; local/E2E runs with no Redis that create typed documents: UNMEASURED. Same file as the KS-1855 half-two hold (hunks at 377 and 922: stack applies clean by `patch -p1 -N`; stacked suite NOT run).
