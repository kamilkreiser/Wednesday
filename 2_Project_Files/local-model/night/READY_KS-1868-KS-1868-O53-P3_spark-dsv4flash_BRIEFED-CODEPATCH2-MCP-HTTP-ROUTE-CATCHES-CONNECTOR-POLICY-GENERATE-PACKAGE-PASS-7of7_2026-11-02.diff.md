# READY — KS-1868-KS-1868-O53-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o53_p3_mcp_http_route_catches_get_connector_get_policy_post_generate_package/out.md.checker/patch.diff`** (from `ls` at 07:06 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o53_p3_mcp_http_route_catches_get_connector_get_policy_post_generate_package/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o53_p3_mcp_http_route_catches_get_connector_get_policy_post_generate_package/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o53_p3_mcp_http_route_catches_get_connector_get_policy_post_generate_package/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o53_p3_mcp_http_route_catches_get_connector_get_policy_post_generate_package-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:06 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o53_p3_mcp_http_route_catches_get_connector_get_policy_post_generate_package/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/mcp-server/src/http-server.ts } + { Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/mcp-server/src/http-server.ts` (product) and `Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	6	Blockchain/Dev/services/mcp-server/src/http-server.ts
204	0	Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: http-server.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/mcp-server/src/http-server.ts`; test(s): `Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/mcp-server/src/http-server.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts 204 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/mcp-server/src/http-server.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (9 failed / 15 run; controls green; assertion reds)` [red_first.json: failed=9 of total=15; red cell(s): ["KS-1868 'GET /connector' catch reads the thrown value safely RED ks1868 R1 GET /connector: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 'GET /connector' catch reads the thrown value safely RED ks1868 R2 GET /connector: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 'GET /connector' catch reads the thrown value safely RED ks1868 R3 GET /connector: a thrown STRING is logged by its kind only, never its value", "KS-1868 'GET /policy' catch reads the thrown value safely RED ks1868 R1 GET /policy: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 'GET /policy' catch reads the thrown value safely RED ks1868 R2 GET /policy: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 'GET /policy' catch reads the thrown value safely RED ks1868 R3 GET /policy: a thrown STRING is logged by its kind only, never its value", "KS-1868 'POST /generate-package' catch reads the thrown value safely RED ks1868 R1 POST /generate-package: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500", "KS-1868 'POST /generate-package' catch reads the thrown value safely RED ks1868 R2 POST /generate-package: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500", "KS-1868 'POST /generate-package' catch reads the thrown value safely RED ks1868 R3 POST /generate-package: a thrown STRING is logged by its kind only, never its value"]]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (15 passed / 15 run)` [green_after.json: failed=0 of total=15, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=86 failed=0 | after: total=101 failed=0` · `NEW reds: []` [baseline_suite.json total=86 failed=0; after_suite.json total=101 failed=0]
- A6 [verbatim]: `PASS A6 whole services/mcp-server suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/mcp-server: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/mcp-server/src/http-server.ts` (+3/-6 per numstat.out) and the test file `Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts` (+204/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/mcp-server/src/http-server.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o53_p3_mcp_http_route_catches_get_connector_get_policy_post_generate_package/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o53_p3_mcp_http_route_catches_get_connector_get_policy_post_generate_package/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o53_p3_mcp_http_route_catches_get_connector_get_policy_post_generate_package/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/mcp-server/src/http-server.ts b/Blockchain/Dev/services/mcp-server/src/http-server.ts
--- a/Blockchain/Dev/services/mcp-server/src/http-server.ts
+++ b/Blockchain/Dev/services/mcp-server/src/http-server.ts
@@ -224,8 +224,7 @@
     const result = await getConnectorInfo();
     res.status(result.status).json(result.data);
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
-    console.error('[mcp-http] GET /connector failed:', message);
+    console.error('[mcp-http] GET /connector failed:', describeThrown(err));
     res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -235,8 +234,7 @@
     const result = await getVerificationPolicy();
     res.json(result.data);
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
-    console.error('[mcp-http] GET /policy failed:', message);
+    console.error('[mcp-http] GET /policy failed:', describeThrown(err));
     res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
   }
 });
@@ -289,8 +287,7 @@
       res,
     );
   } catch (err: unknown) {
-    const message = err instanceof Error ? err.message : String(err);
-    console.error('[mcp-http] POST /generate-package failed:', message);
+    console.error('[mcp-http] POST /generate-package failed:', describeThrown(err));
     if (!res.headersSent) {
       res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
     }
diff --git a/Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/mcp-server/src/__tests__/ks1868-mcp-http-route-catches-p3-unreadable-throw.test.ts
@@ -0,0 +1,204 @@
+/**
+ * KS-1868: the three log-only route catch blocks below read the caught value with `err instanceof Error ? err.message : String(err)`
+ * only to put it in a `console.error` line. That read can itself throw (a revoked Proxy throws on `instanceof`; an Error whose `message`
+ * getter throws throws on `.message`), and inside an async Express 4 handler the rejection is not caught: the request gets no
+ * response and Node sees an unhandled rejection. Each catch now logs `describeThrown(err)` (the helper KS-1901 added to this module),
+ * whose read cannot throw, and answers the same constant 500 as before.
+ *
+ * Routes covered here: GET /connector, GET /policy, POST /generate-package.
+ *
+ * The module binds a port and runs a production guard on import, so `express`, the shared guard, the api client, the hasher and the
+ * package generator are replaced and the route handlers are captured and called directly: no port is bound, no network is touched.
+ * The stand-ins are plain functions, not vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy before
+ * the code under test saw it.
+ */
+import { describe, it, expect, vi, beforeAll, beforeEach, afterEach } from 'vitest';
+import type { MockInstance } from 'vitest';
+
+const ks = vi.hoisted(() => ({
+  routes: {} as Record<string, (req: unknown, res: unknown) => Promise<void>>,
+  queue: [] as Array<{ value: unknown }>,
+  genThrow: undefined as { value: unknown } | undefined,
+}));
+
+vi.mock('express', () => {
+  const app = {
+    use: () => app,
+    get: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {
+      ks.routes['GET ' + p] = f;
+    },
+    post: (p: string, f: (req: unknown, res: unknown) => Promise<void>) => {
+      ks.routes['POST ' + p] = f;
+    },
+    listen: () => ({}),
+  };
+  const express = Object.assign(() => app, { json: () => () => undefined });
+  return { default: express };
+});
+vi.mock('@secuura/shared', () => ({
+  enforceProductionConfig: () => undefined,
+  rejectNulBytes: () => () => undefined,
+}));
+vi.mock('../api-client.js', () => {
+  const next = () => {
+    const n = ks.queue.shift();
+    if (!n) throw new Error('test setup: queue empty');
+    return Promise.reject(n.value);
+  };
+  return {
+    registerDocument: next,
+    verifyDocument: next,
+    listDocuments: next,
+    getWorkflowInstance: next,
+    getConnectorInfo: next,
+    getVerificationPolicy: next,
+  };
+});
+vi.mock('../hashing.js', () => ({
+  hashFile: () => Promise.resolve('sha256:0'),
+  extractFileName: (p: string) => p,
+  hashBuffer: () => 'sha256:0',
+}));
+vi.mock('../package-generator.js', () => ({
+  generatePackage: () => (ks.genThrow ? Promise.reject(ks.genThrow.value) : Promise.resolve()),
+}));
+
+type Res53 = {
+  statusCode: number;
+  body: unknown;
+  headersSent: boolean;
+  status(c: number): Res53;
+  json(b: unknown): Res53;
+  setHeader(k: string, v: string): void;
+};
+
+function mkRes(): Res53 {
+  const r: Res53 = {
+    statusCode: 200,
+    body: undefined,
+    headersSent: false,
+    status(c) {
+      r.statusCode = c;
+      return r;
+    },
+    json(b) {
+      r.body = b;
+      return r;
+    },
+    setHeader() {
+      /* headers are not asserted here */
+    },
+  };
+  return r;
+}
+
+const CONST500 = {
+  success: false,
+  error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' },
+};
+
+let spy53: MockInstance<typeof console.error>;
+
+/** Everything passed to console.error, one line per call; a non-string argument shows as <<non-string:type>>. */
+function errLog(): string {
+  return spy53.mock.calls
+    .map((args) => args.map((x) => (typeof x === 'string' ? x : '<<non-string:' + typeof x + '>>')).join(' '))
+    .join('\n');
+}
+
+type Case53 = { route: string; answer: unknown; arm: (v: unknown) => unknown };
+
+const CASES53: Case53[] = [
+  {
+    route: 'GET /connector',
+    answer: CONST500,
+    arm: (v) => {
+      ks.queue.push({ value: v });
+      return { body: {}, query: {}, params: {} };
+    },
+  },
+  {
+    route: 'GET /policy',
+    answer: CONST500,
+    arm: (v) => {
+      ks.queue.push({ value: v });
+      return { body: {}, query: {}, params: {} };
+    },
+  },
+  {
+    route: 'POST /generate-package',
+    answer: CONST500,
+    arm: (v) => {
+      ks.genThrow = { value: v };
+      return { body: { agentType: 'cursor', apiKey: 'k-1' }, query: {}, params: {} };
+    },
+  },
+];
+
+/** Run one route handler. A handler that rejects (the defect) leaves the response untouched at 200, so the cell's assertions fail. */
+async function invoke(route: string, req: unknown): Promise<Res53> {
+  const res = mkRes();
+  await ks.routes[route](req, res).catch(() => undefined);
+  return res;
+}
+
+beforeAll(async () => {
+  await import('../http-server.js');
+});
+
+beforeEach(() => {
+  ks.queue.length = 0;
+  ks.genThrow = undefined;
+  spy53 = vi.spyOn(console, 'error').mockImplementation(() => undefined);
+});
+
+afterEach(() => {
+  spy53.mockRestore();
+});
+
+describe.each(CASES53)('KS-1868 $route catch reads the thrown value safely', (c) => {
+  it(`RED ks1868 R1 ${c.route}: a revoked Proxy thrown value is logged as a constant reason and the route still answers its constant 500`, async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    const res = await invoke(c.route, c.arm(proxy));
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(c.answer);
+    expect(errLog()).toContain('unreadable thrown value');
+  });
+
+  it(`RED ks1868 R2 ${c.route}: an Error whose message getter throws is logged as a constant reason and the route still answers its constant 500`, async () => {
+    const getterThrows = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const res = await invoke(c.route, c.arm(getterThrows));
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(c.answer);
+    expect(errLog()).toContain('unreadable thrown value');
+  });
+
+  it(`RED ks1868 R3 ${c.route}: a thrown STRING is logged by its kind only, never its value`, async () => {
+    const res = await invoke(c.route, c.arm('S3CR3T-STRING-MARKER'));
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(c.answer);
+    expect(errLog()).toContain('non-Error string thrown');
+    expect(errLog()).not.toContain('S3CR3T-STRING-MARKER');
+    expect(errLog()).not.toContain('<<non-string');
+  });
+
+  it(`control ks1868 C1 ${c.route}: an ordinary Error logs its message and the answer is the constant 500 without it`, async () => {
+    const res = await invoke(c.route, c.arm(new Error('ordinary boom 10.0.0.7')));
+    expect(res.statusCode).toBe(500);
+    expect(res.body).toEqual(c.answer);
+    expect(JSON.stringify(res.body)).not.toContain('ordinary boom');
+    expect(errLog()).toContain('ordinary boom 10.0.0.7');
+  });
+
+  it(`control ks1868 C2 ${c.route}: the log line keeps its route prefix`, async () => {
+    await invoke(c.route, c.arm(new Error('ordinary boom')));
+    expect(errLog()).toContain('[mcp-http] ' + c.route + ' failed:');
+  });
+});
```
