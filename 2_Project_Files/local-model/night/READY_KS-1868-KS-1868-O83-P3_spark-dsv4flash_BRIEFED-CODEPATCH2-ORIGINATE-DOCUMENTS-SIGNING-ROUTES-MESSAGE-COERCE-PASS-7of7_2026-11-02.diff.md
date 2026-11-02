# READY — KS-1868-KS-1868-O83-P3 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p3_originate_documents_signing_routes_catches_coerce_message/out.md.checker/patch.diff`** (from `ls` at 22:05 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p3_originate_documents_signing_routes_catches_coerce_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p3_originate_documents_signing_routes_catches_coerce_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p3_originate_documents_signing_routes_catches_coerce_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p3_originate_documents_signing_routes_catches_coerce_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 22:05 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p3_originate_documents_signing_routes_catches_coerce_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `58b5042ccdb5a06a213ba53f5d4f7644f5f52549`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/documents.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/documents.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/originate/src/routes/documents.ts
236	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: documents.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/documents.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/documents.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts 236 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/documents.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (9 failed / 13 run; controls green; assertion reds)` [red_first.json: failed=9 of total=13; red cell(s): ['KS-1868 the originate document signing routes log text for a hostile thrown value RED ks1868 R1 POST /:id/sign: a revoked Proxy thrown value logs the constant reason and the route answers 500', 'KS-1868 the originate document signing routes log text for a hostile thrown value RED ks1868 R2 POST /:id/sign: an Error whose message is a null-prototype object logs the constant reason and the route answers 500', 'KS-1868 the originate document signing routes log text for a hostile thrown value RED ks1868 R3 POST /:id/sign: an Error whose message is a Symbol logs the Symbol text and the route answers 500', 'KS-1868 the originate document signing routes log text for a hostile thrown value RED ks1868 R4 POST /:id/sign-cert: a revoked Proxy thrown value logs the constant reason and the route answers 500', 'KS-1868 the originate document signing routes log text for a hostile thrown value RED ks1868 R5 POST /:id/sign-cert: an Error whose message is a null-prototype object logs the constant reason and the route answers 500', 'KS-1868 the originate document signing routes log text for a hostile thrown value RED ks1868 R6 POST /:id/sign-cert: an Error whose message is a Symbol logs the Symbol text and the route answers 500', 'KS-1868 the originate document signing routes log text for a hostile thrown value RED ks1868 R7 POST /:id/sign-wallet: a revoked Proxy thrown value logs the constant reason and the route answers 500', 'KS-1868 the originate document signing routes log text for a hostile thrown value RED ks1868 R8 POST /:id/sign-wallet: an Error whose message is a null-prototype object logs the constant reason and the route answers 500', 'KS-1868 the originate document signing routes log text for a hostile thrown value RED ks1868 R9 POST /:id/sign-wallet: an Error whose message is a Symbol logs the Symbol text and the route answers 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (13 passed / 13 run)` [green_after.json: failed=0 of total=13, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2189 failed=0 | after: total=2202 failed=0` · `NEW reds: []` [baseline_suite.json total=2189 failed=0; after_suite.json total=2202 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/documents.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts` (+236/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/documents.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `58b5042ccdb5a06a213ba53f5d4f7644f5f52549` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p3_originate_documents_signing_routes_catches_coerce_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o83_p3_originate_documents_signing_routes_catches_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p3_originate_documents_signing_routes_catches_coerce_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/documents.ts b/Blockchain/Dev/services/originate/src/routes/documents.ts
--- a/Blockchain/Dev/services/originate/src/routes/documents.ts
+++ b/Blockchain/Dev/services/originate/src/routes/documents.ts
@@ -1363,7 +1363,13 @@
         signedAt: now,
       });
     } catch (error) {
-      logger.error('Failed to sign document', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = String(error instanceof Error ? error.message : error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Failed to sign document', { error: reason });
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to sign document' } });
     }
   },
@@ -3464,8 +3470,14 @@
         sigJsonUrl: `/api/documents/${newExternalId}/sig-json`,
       });
     } catch (error) {
+      let reason: string;
+      try {
+        reason = String(error instanceof Error ? error.message : error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
       logger.error('Failed to sign document via issuer cert', {
-        error: error instanceof Error ? error.message : String(error),
+        error: reason,
       });
       return res.status(500).json({
         success: false,
@@ -3653,8 +3665,14 @@
         sigWallet: sigWalletEnvelope,
       });
     } catch (error) {
+      let reason: string;
+      try {
+        reason = String(error instanceof Error ? error.message : error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
       logger.error('Failed to sign document via wallet', {
-        error: error instanceof Error ? error.message : String(error),
+        error: reason,
       });
       return res.status(500).json({
         success: false,
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-documents-signing-routes-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,236 @@
+// KS-1868: three document SIGNING routes of originate (POST /:id/sign, POST /:id/sign-cert and POST /:id/sign-wallet) log
+// `error: <reading of the caught value>` in their outer catch as `error instanceof Error ? error.message : String(error)`, unguarded. A revoked Proxy
+// makes `instanceof` throw inside the catch, and an Error whose `message` getter returns a revoked Proxy, a null-prototype object or a Symbol hands the
+// logger a value it cannot format; the route then never answers. The cells make the first document read reject with such a value and assert the route
+// answers the constant 500, nothing is written and the logged reason is text (the constant when it cannot be turned into text). The rejection is thrown
+// by the document read itself, which has no inner catch on these three routes, and it comes before any signing, any signature check and any write.
+// Controls pin an ordinary Error and a thrown plain string (a non-Error is logged as its own text). A hang is a null answer (abort signal), not a jest
+// timeout. Harness: the ks466 malformed-id suite (same module mocks). Nothing is written.
+const mockState: { toThrow: unknown; errored: unknown[][]; reads: number; writes: number } = {
+  toThrow: undefined,
+  errored: [],
+  reads: 0,
+  writes: 0,
+};
+
+process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';
+process.env.SIMULATE_ANCHORING = 'true';
+
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: (..._args: unknown[]) => {
+    mockState.reads += 1;
+    return Promise.reject(mockState.toThrow);
+  },
+  listDocuments: jest.fn(),
+  saveDocument: (..._args: unknown[]) => {
+    mockState.writes += 1;
+    return Promise.resolve({ dbId: '99999999-9999-4999-8999-999999999999', inserted: true });
+  },
+  updateDocument: (..._args: unknown[]) => {
+    mockState.writes += 1;
+    return Promise.resolve(undefined);
+  },
+  getSigningRequest: jest.fn(),
+  saveSigningRequest: (..._args: unknown[]) => {
+    mockState.writes += 1;
+    return Promise.resolve(undefined);
+  },
+  deleteSigningRequest: jest.fn(),
+  generateContentHash: jest.fn(() => 'a'.repeat(64)),
+  seedDemoDocuments: jest.fn(async () => undefined),
+  assertNoCycle: jest.fn(async () => undefined),
+}));
+
+jest.mock('../repositories/shareRepo', () => ({
+  createShare: jest.fn(),
+}));
+
+jest.mock('../repositories/lifecycleEventRepo', () => ({
+  createLifecycleEvent: jest.fn(),
+  setLifecycleEventAnchor: jest.fn(),
+  listLifecycleEvents: (..._args: unknown[]) => {
+    mockState.reads += 1;
+    return Promise.reject(mockState.toThrow);
+  },
+}));
+
+jest.mock('../events', () => ({
+  publishEvent: jest.fn(async () => undefined),
+  EventTypes: {
+    DOCUMENT_CREATED: 'document.created',
+    DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred',
+    DOCUMENT_VERSIONED: 'document.versioned',
+  },
+}));
+
+jest.mock('../services/threadTokenClient', () => ({
+  mintAndRegisterThreadToken: jest.fn(async () => ({})),
+}));
+
+jest.mock('../routes/verification', () => ({
+  registerInPlatformRegistry: jest.fn(async () => undefined),
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (req: any, _res: unknown, next: () => void) => {
+    req.user = { userId: '11111111-2222-4333-8444-555555555555', role: 'ISSUER_ADMIN' };
+    next();
+  },
+}));
+
+jest.mock('../middleware/rbac', () => ({
+  isAllowedByRoleOrScope: () => true,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    debug: () => undefined,
+    warn: () => undefined,
+    error: (...args: unknown[]) => {
+      mockState.errored.push(args);
+    },
+  },
+}));
+
+import express from 'express';
+import { documentsRouter, publicDocumentsRouter } from '../routes/documents';
+
+const app = express();
+// Same mount order as index.ts: public router first, then the auth-gated one.
+app.use('/api/documents', express.json(), publicDocumentsRouter);
+app.use('/api/documents', express.json(), documentsRouter);
+
+const DOC = 'doc-ks1868-lookup-target';
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  const address = server.address();
+  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
+});
+
+afterAll(() => server?.close());
+
+beforeEach(() => {
+  mockState.toThrow = undefined;
+  mockState.errored.length = 0;
+  mockState.reads = 0;
+  mockState.writes = 0;
+});
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+/** An Error whose `message` getter succeeds and returns the (non-string) value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+/** The logged `error` field of the logger call that carries this first argument, as a string; the type name when it is not one. */
+const reasonOf = (first: string): string => {
+  const calls = mockState.errored.filter((c) => c[0] === first);
+  if (calls.length !== 1) return '<' + calls.length + ' calls>';
+  const v = (calls[0][1] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+
+let unhandled = 0;
+const onUnhandled = () => {
+  unhandled += 1;
+};
+beforeAll(() => {
+  process.on('unhandledRejection', onUnhandled);
+});
+afterAll(() => {
+  process.removeListener('unhandledRejection', onUnhandled);
+});
+beforeEach(() => {
+  unhandled = 0;
+});
+
+async function call(method: string, path: string, body?: unknown): Promise<{ status: number; code: string | undefined } | null> {
+  try {
+    const res = await fetch(`${baseUrl}${path}`, {
+      method,
+      headers: { 'content-type': 'application/json' },
+      body: body === undefined ? undefined : JSON.stringify(body),
+      signal: AbortSignal.timeout(1500),
+    });
+    const payload = (await res.json()) as { error?: { code?: string } };
+    return { status: res.status, code: payload.error?.code };
+  } catch {
+    return null;
+  }
+}
+
+const SIGN: [string, string, string, unknown] = ['POST', `/api/documents/${DOC}/sign`, 'Failed to sign document', { signature: 'ks1868-signature', nonce: 'ks1868-nonce' }];
+const SIGN_CERT: [string, string, string, unknown] = ['POST', `/api/documents/${DOC}/sign-cert`, 'Failed to sign document via issuer cert', {}];
+const SIGN_WALLET: [string, string, string, unknown] = ['POST', `/api/documents/${DOC}/sign-wallet`, 'Failed to sign document via wallet', { walletAddress: 'addr_test1ks1868', signature: 'ab', key: 'cd' }];
+
+async function route(r: [string, string, string, unknown], thrown: unknown, reason: string): Promise<void> {
+  mockState.toThrow = thrown;
+  expect(await call(r[0], r[1], r[3])).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+  expect(unhandled).toBe(0);
+  expect(mockState.errored).toHaveLength(1);
+  expect(reasonOf(r[2])).toBe(reason);
+  expect(mockState.reads).toBe(1);
+  expect(mockState.writes).toBe(0);
+}
+const CONSTANT = 'unreadable thrown value';
+
+describe('KS-1868 the originate document signing routes log text for a hostile thrown value', () => {
+  it('control ks1868 C1 POST /:id/sign: an ordinary Error is logged with its own message and the route answers 500', async () => {
+    await route(SIGN, new Error('Connection terminated unexpectedly'), 'Connection terminated unexpectedly');
+  });
+
+  it('control ks1868 C2 POST /:id/sign-cert: an ordinary Error is logged with its own message and the route answers 500', async () => {
+    await route(SIGN_CERT, new Error('Connection terminated unexpectedly'), 'Connection terminated unexpectedly');
+  });
+
+  it('control ks1868 C3 POST /:id/sign-wallet: an ordinary Error is logged with its own message and the route answers 500', async () => {
+    await route(SIGN_WALLET, new Error('Connection terminated unexpectedly'), 'Connection terminated unexpectedly');
+  });
+
+  it('control ks1868 C4 POST /:id/sign: a thrown plain string is logged as its own text and the route answers 500', async () => {
+    await route(SIGN, 'plain boom', 'plain boom');
+  });
+
+  it('RED ks1868 R1 POST /:id/sign: a revoked Proxy thrown value logs the constant reason and the route answers 500', async () => {
+    await route(SIGN, revokedProxy(), CONSTANT);
+  });
+
+  it('RED ks1868 R2 POST /:id/sign: an Error whose message is a null-prototype object logs the constant reason and the route answers 500', async () => {
+    await route(SIGN, withMessage(Object.create(null)), CONSTANT);
+  });
+
+  it('RED ks1868 R3 POST /:id/sign: an Error whose message is a Symbol logs the Symbol text and the route answers 500', async () => {
+    await route(SIGN, withMessage(Symbol('ks1868')), 'Symbol(ks1868)');
+  });
+
+  it('RED ks1868 R4 POST /:id/sign-cert: a revoked Proxy thrown value logs the constant reason and the route answers 500', async () => {
+    await route(SIGN_CERT, revokedProxy(), CONSTANT);
+  });
+
+  it('RED ks1868 R5 POST /:id/sign-cert: an Error whose message is a null-prototype object logs the constant reason and the route answers 500', async () => {
+    await route(SIGN_CERT, withMessage(Object.create(null)), CONSTANT);
+  });
+
+  it('RED ks1868 R6 POST /:id/sign-cert: an Error whose message is a Symbol logs the Symbol text and the route answers 500', async () => {
+    await route(SIGN_CERT, withMessage(Symbol('ks1868')), 'Symbol(ks1868)');
+  });
+
+  it('RED ks1868 R7 POST /:id/sign-wallet: a revoked Proxy thrown value logs the constant reason and the route answers 500', async () => {
+    await route(SIGN_WALLET, revokedProxy(), CONSTANT);
+  });
+
+  it('RED ks1868 R8 POST /:id/sign-wallet: an Error whose message is a null-prototype object logs the constant reason and the route answers 500', async () => {
+    await route(SIGN_WALLET, withMessage(Object.create(null)), CONSTANT);
+  });
+
+  it('RED ks1868 R9 POST /:id/sign-wallet: an Error whose message is a Symbol logs the Symbol text and the route answers 500', async () => {
+    await route(SIGN_WALLET, withMessage(Symbol('ks1868')), 'Symbol(ks1868)');
+  });
+});
```
