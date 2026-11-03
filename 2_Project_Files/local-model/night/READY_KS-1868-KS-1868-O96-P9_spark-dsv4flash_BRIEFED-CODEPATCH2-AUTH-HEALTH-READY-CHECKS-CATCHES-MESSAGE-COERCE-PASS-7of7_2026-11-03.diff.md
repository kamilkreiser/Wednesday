# READY — KS-1868-KS-1868-O96-P9 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p9_auth_health_ready_checks_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 16:11 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p9_auth_health_ready_checks_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p9_auth_health_ready_checks_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p9_auth_health_ready_checks_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p9_auth_health_ready_checks_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:11 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p9_auth_health_ready_checks_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/health.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/health.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/auth/src/routes/health.ts
134	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: health.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/health.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/health.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts 134 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/health.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 auth readiness probe reads a dependency failure safely RED ks1868 R1 database: a revoked Proxy gives a 503 report with a constant reason', 'KS-1868 auth readiness probe reads a dependency failure safely RED ks1868 R2 database: an Error whose message getter throws gives a 503 report with a constant reason', 'KS-1868 auth readiness probe reads a dependency failure safely RED ks1868 R3 redis: a revoked Proxy gives a 503 report with a constant reason', 'KS-1868 auth readiness probe reads a dependency failure safely RED ks1868 R4 redis: an Error whose message getter throws gives a 503 report with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1623 failed=1 | after: total=1629 failed=0` · `NEW reds: []` [baseline_suite.json total=1623 failed=1; after_suite.json total=1629 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/health.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts` (+134/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/health.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p9_auth_health_ready_checks_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o96_p9_auth_health_ready_checks_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p9_auth_health_ready_checks_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/health.ts b/Blockchain/Dev/services/auth/src/routes/health.ts
--- a/Blockchain/Dev/services/auth/src/routes/health.ts
+++ b/Blockchain/Dev/services/auth/src/routes/health.ts
@@ -38,6 +38,12 @@
     ]);
     return { status: 'healthy', latency: Date.now() - start };
   } catch (error) {
-    return { status: 'unhealthy', message: String(error) };
+    let message: string;
+    try {
+      message = String(error);
+    } catch {
+      message = 'unreadable thrown value';
+    }
+    return { status: 'unhealthy', message };
   }
 }
@@ -58,6 +64,12 @@
     ]);
     return { status: 'healthy', latency: Date.now() - start };
   } catch (error) {
-    return { status: 'unhealthy', message: String(error) };
+    let message: string;
+    try {
+      message = String(error);
+    } catch {
+      message = 'unreadable thrown value';
+    }
+    return { status: 'unhealthy', message };
   }
 }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts
@@ -0,0 +1,134 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+// KS-1868: the readiness probe of the auth service (GET /health/ready, src/routes/health.ts) builds its checks with
+// checkRedis and checkDatabase; each catch answers `{ status: 'unhealthy', message: String(error) }` so a dependency
+// failure becomes a 503 report. The `String(error)` read is unguarded. When the value cannot be read (a revoked Proxy
+// throws on String(); an Error whose `message` getter throws, throws in Error.prototype.toString) the catch throws, so the
+// handler REJECTS and the probe answers nothing where an ordinary Error gives the 503 report. The database module and the
+// session module are plain stand-ins (the dependency under test rejects with the cell's value, the other is absent or
+// not connected); fake timers keep the 3 s race timer from outliving the cell; no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  mode: 'db' as 'db' | 'redis',
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => h.mode === 'db',
+  query: () => Promise.reject(h.toThrow),
+}));
+
+vi.mock('../services/session', () => ({
+  getRedisClient: () => (h.mode === 'redis' ? { ping: () => Promise.reject(h.toThrow) } : null),
+}));
+
+import { healthRoutes } from '../routes/health';
+
+type Settled = { rejected: boolean; code: number | undefined; body: { checks?: Record<string, unknown> } | undefined };
+
+/** Runs the /ready handler read off the router stack. */
+async function ready(): Promise<Settled> {
+  const layer = (healthRoutes as unknown as { stack: Array<{ route?: { path: string; stack: Array<{ handle: (...a: unknown[]) => unknown }> } }> }).stack.find(
+    (l) => l.route?.path === '/ready',
+  );
+  const handle = layer!.route!.stack[0].handle;
+  const out: Settled = { rejected: false, code: undefined, body: undefined };
+  const res = {
+    status(c: number) {
+      out.code = c;
+      return res;
+    },
+    json(b: { checks?: Record<string, unknown> }) {
+      out.body = b;
+      return res;
+    },
+  };
+  try {
+    await handle({}, res);
+  } catch {
+    out.rejected = true;
+  }
+  return out;
+}
+
+const unhealthy = (message: string) => ({ status: 'unhealthy', message });
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
+describe('KS-1868 auth readiness probe reads a dependency failure safely', () => {
+  beforeEach(() => {
+    vi.useFakeTimers();
+    h.toThrow = undefined;
+    h.mode = 'db';
+  });
+
+  afterEach(() => {
+    vi.useRealTimers();
+  });
+
+  it('control ks1868 C1 database: an ordinary Error gives a 503 report with its text', async () => {
+    h.mode = 'db';
+    h.toThrow = new Error('db down');
+    const out = await ready();
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body?.checks?.database).toEqual(unhealthy('Error: db down'));
+  });
+
+  it('control ks1868 C2 redis: a thrown plain string gives a 503 report with that text', async () => {
+    h.mode = 'redis';
+    h.toThrow = 'plain text failure';
+    const out = await ready();
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body?.checks?.redis).toEqual(unhealthy('plain text failure'));
+  });
+
+  it('RED ks1868 R1 database: a revoked Proxy gives a 503 report with a constant reason', async () => {
+    h.mode = 'db';
+    h.toThrow = revokedProxy();
+    const out = await ready();
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body?.checks?.database).toEqual(unhealthy('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R2 database: an Error whose message getter throws gives a 503 report with a constant reason', async () => {
+    h.mode = 'db';
+    h.toThrow = getterThrows();
+    const out = await ready();
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body?.checks?.database).toEqual(unhealthy('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R3 redis: a revoked Proxy gives a 503 report with a constant reason', async () => {
+    h.mode = 'redis';
+    h.toThrow = revokedProxy();
+    const out = await ready();
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body?.checks?.redis).toEqual(unhealthy('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R4 redis: an Error whose message getter throws gives a 503 report with a constant reason', async () => {
+    h.mode = 'redis';
+    h.toThrow = getterThrows();
+    const out = await ready();
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(503);
+    expect(out.body?.checks?.redis).toEqual(unhealthy('unreadable thrown value'));
+  });
+});
```
