# READY — KS-1868-KS-1868-O97-P8 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p8_gateway_health_dashboard_check_service_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 17:36 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p8_gateway_health_dashboard_check_service_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p8_gateway_health_dashboard_check_service_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p8_gateway_health_dashboard_check_service_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p8_gateway_health_dashboard_check_service_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 17:36 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p8_gateway_health_dashboard_check_service_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `de8d208a8426747b3a752309e08167fa0de4b2ff`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
11	1	Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts
88	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (10 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: health-dashboard.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts 11 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts 88 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 health dashboard reads a probe failure safely RED ks1868 R1 a revoked Proxy reports the service down with a constant reason', 'KS-1868 health dashboard reads a probe failure safely RED ks1868 R2 an Error whose message getter throws reports the service down with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1566 failed=0 | after: total=1570 failed=0` · `NEW reds: []` [baseline_suite.json total=1566 failed=0; after_suite.json total=1570 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts` (+11/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts` (+88/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `de8d208a8426747b3a752309e08167fa0de4b2ff` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p8_gateway_health_dashboard_check_service_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o97_p8_gateway_health_dashboard_check_service_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p8_gateway_health_dashboard_check_service_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts b/Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts
@@ -83,4 +83,14 @@
-    if (error instanceof DOMException && error.name === 'AbortError') {
+    let readable = true;
+    try {
+      void (error instanceof Error && error.message);
+      void (error instanceof DOMException && error.name);
+    } catch {
+      readable = false;
+    }
+
+    if (!readable) {
+      errorMessage = 'unreadable thrown value';
+    } else if (error instanceof DOMException && error.name === 'AbortError') {
       errorMessage = 'timeout';
     } else if (error instanceof Error) {
       errorMessage = error.message;
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts
@@ -0,0 +1,88 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+// KS-1868: the gateway health dashboard (src/routes/health-dashboard.ts) probes each deployed service; when the probe's fetch
+// fails, checkService reads the thrown value as `error instanceof DOMException && ... : error instanceof Error ? error.message`,
+// unguarded. When the value cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws)
+// the catch itself throws, so checkService rejects, the aggregate drops the settled-rejected result silently, and the service
+// is ABSENT from the dashboard instead of reported down. The service list is a plain stand-in with one deployed service; the
+// global fetch is a plain function rejecting with the cell's value (stubbed, removed after each cell); fake timers keep the
+// 5 s abort timer from outliving the cell; the handler is read off the router stack; no network.
+const h = vi.hoisted(() => ({ toThrow: undefined as unknown }));
+
+vi.mock('../config/services', () => ({
+  services: { svc: { url: 'https://svc.example.test', healthPath: '/health' } },
+}));
+
+import router from '../routes/health-dashboard';
+
+type Got = { code: number | undefined; body: { services?: Record<string, unknown> } | undefined };
+
+async function dashboard(value: unknown): Promise<Got> {
+  h.toThrow = value;
+  vi.stubGlobal('fetch', () => Promise.reject(h.toThrow));
+  const layer = (router as unknown as { stack: Array<{ route?: { path: string; stack: Array<{ handle: (...a: unknown[]) => unknown }> } }> }).stack.find(
+    (l) => l.route?.path === '/dashboard',
+  );
+  const handle = layer!.route!.stack[0].handle;
+  const out: Got = { code: undefined, body: undefined };
+  const res = {
+    status(c: number) {
+      out.code = c;
+      return res;
+    },
+    json(b: { services?: Record<string, unknown> }) {
+      out.body = b;
+      return res;
+    },
+  };
+  await handle({}, res);
+  return out;
+}
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+const down = (error: string) => ({ status: 'down', latencyMs: expect.any(Number), url: 'https://svc.example.test', error });
+
+describe('KS-1868 health dashboard reads a probe failure safely', () => {
+  beforeEach(() => {
+    vi.useFakeTimers();
+  });
+
+  afterEach(() => {
+    vi.useRealTimers();
+    vi.unstubAllGlobals();
+  });
+
+  it('control ks1868 C1 an ordinary Error reports the service down with its message', async () => {
+    const out = await dashboard(new Error('connect boom'));
+    expect(out.body?.services?.svc).toEqual(down('connect boom'));
+  });
+
+  it('control ks1868 C2 a thrown plain string reports the service down with the generic text', async () => {
+    const out = await dashboard('plain text failure');
+    expect(out.body?.services?.svc).toEqual(down('Unknown error'));
+  });
+
+  it('RED ks1868 R1 a revoked Proxy reports the service down with a constant reason', async () => {
+    const out = await dashboard(revokedProxy());
+    expect(out.body?.services?.svc).toEqual(down('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws reports the service down with a constant reason', async () => {
+    const out = await dashboard(getterThrows());
+    expect(out.body?.services?.svc).toEqual(down('unreadable thrown value'));
+  });
+});
```
