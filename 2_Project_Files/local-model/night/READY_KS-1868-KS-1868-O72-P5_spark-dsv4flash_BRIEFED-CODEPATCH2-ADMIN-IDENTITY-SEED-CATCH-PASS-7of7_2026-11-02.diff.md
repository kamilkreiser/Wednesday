# READY — KS-1868-KS-1868-O72-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p5_admin_identity_seed_catch_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 11:50 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p5_admin_identity_seed_catch_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p5_admin_identity_seed_catch_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p5_admin_identity_seed_catch_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p5_admin_identity_seed_catch_unreadable_throw-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 11:50 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p5_admin_identity_seed_catch_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d9acf71a3fcc9b70a216a904d7339a8fc1ccf4a0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/routes/admin.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/api-gateway/src/routes/admin.ts
150	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: admin.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/routes/admin.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/routes/admin.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts 150 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 identity users seed catch reads the thrown value safely RED ks1868 R1 seed: a revoked Proxy thrown value is logged as a constant reason and the request carries on to a 200', 'KS-1868 identity users seed catch reads the thrown value safely RED ks1868 R2 seed: an Error whose message getter throws is logged as a constant reason and the request carries on to a 200']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1387 failed=0 | after: total=1391 failed=0` · `NEW reds: []` [baseline_suite.json total=1387 failed=0; after_suite.json total=1391 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts` (+150/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/routes/admin.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d9acf71a3fcc9b70a216a904d7339a8fc1ccf4a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p5_admin_identity_seed_catch_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o72_p5_admin_identity_seed_catch_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p5_admin_identity_seed_catch_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -1235,6 +1235,12 @@
       }
       log('info', '[Identity] Seeded demo organizations and identity users');
     } catch (err) {
-      log('warn', '[Identity] Seed skipped: ' + (err as Error).message);
+      let reason: string;
+      try {
+        reason = (err as Error).message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('warn', '[Identity] Seed skipped: ' + reason);
     }
   }
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-admin-identity-seed-catch-unreadable-throw.test.ts
@@ -0,0 +1,150 @@
+/**
+ * KS-1868: the demo-seed catch in routes/admin.ts (`seedIdentityOrgsIfEmpty`, run at the start of GET /api/admin/identity/users)
+ * logs `'[Identity] Seed skipped: ' + (err as Error).message` and lets the request carry on. That read can itself throw (a revoked
+ * Proxy throws on any property read; an Error whose `message` getter throws throws on `.message`), and then the catch escapes: the seed
+ * helper rejects and the whole request fails. The read now sits in its own try and falls back to the constant
+ * `unreadable thrown value`, so the seed is skipped and the request carries on, as it does for an ordinary Error.
+ *
+ * The handler under test is the LAST function of the route, taken from the route table and called directly with a fake request and
+ * response. The database stand-in is a plain function that rejects with the thrown value for the seed's COUNT query only (a vi.fn()
+ * could inspect a revoked Proxy before the code under test does).
+ */
+import { describe, it, expect, beforeEach, afterEach } from 'vitest';
+import type { Router } from 'express';
+import { createAdminRoutes, type AdminRouteDeps } from '../routes/admin';
+
+type Logged = { level: string; message: string; meta: unknown };
+type ResSeed = { statusCode: number; body: unknown; status(c: number): ResSeed; json(b: unknown): ResSeed };
+
+const ks = {
+  thrown: undefined as { value: unknown } | undefined,
+  logs: [] as Logged[],
+  queries: [] as string[],
+};
+
+function mkRes(): ResSeed {
+  const r: ResSeed = {
+    statusCode: 200,
+    body: undefined,
+    status(c) {
+      r.statusCode = c;
+      return r;
+    },
+    json(b) {
+      r.body = b;
+      return r;
+    },
+  };
+  return r;
+}
+
+function buildRouter(): Router {
+  return createAdminRoutes({
+    authenticateToken: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+    query: (text: string) => {
+      ks.queries.push(text);
+      if (text.includes('COUNT(*)')) {
+        if (ks.thrown) return Promise.reject(ks.thrown.value);
+        return Promise.resolve({ rows: [{ cnt: '1' }], rowCount: 1 });
+      }
+      return Promise.resolve({ rows: [], rowCount: 0 });
+    },
+    isDbAvailable: () => true,
+    redisService: {},
+    services: {},
+    log: (level: string, message: string, meta?: unknown) => {
+      ks.logs.push({ level, message, meta });
+    },
+  } as unknown as AdminRouteDeps);
+}
+
+function handlerFor(rt: Router, method: string, path: string): (req: unknown, res: unknown) => Promise<void> {
+  const layers = (rt as unknown as { stack: Array<{ route?: { path: string; methods: Record<string, boolean>; stack: Array<{ handle: (req: unknown, res: unknown) => Promise<void> }> } }> }).stack;
+  const layer = layers.find((l) => l.route && l.route.path === path && l.route.methods[method]);
+  if (!layer || !layer.route) throw new Error('route not found: ' + method + ' ' + path);
+  const stack = layer.route.stack;
+  return stack[stack.length - 1].handle;
+}
+
+/** Run the route handler. A handler that rejects leaves the response untouched at 200 with no body. */
+async function invoke(): Promise<ResSeed> {
+  const res = mkRes();
+  const req = {
+    params: {},
+    body: {},
+    query: {},
+    headers: {},
+    user: { userId: 'admin-72', role: 'SYSTEM_ADMIN', email: 'admin-72@test.io', verificationLevel: 'HIGH' },
+  };
+  await handlerFor(buildRouter(), 'get', '/api/admin/identity/users')(req, res).catch(() => undefined);
+  return res;
+}
+
+function revoked(): unknown {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+function getterError(): unknown {
+  return Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+}
+
+const seedLog = (): Logged | undefined => ks.logs.find((l) => l.level === 'warn' && l.message.startsWith('[Identity] Seed skipped'));
+const usersQueried = () => ks.queries.some((q) => q.includes('FROM users u'));
+
+const savedSeed = process.env.ENABLE_DEMO_SEED;
+
+beforeEach(() => {
+  ks.thrown = undefined;
+  ks.logs.length = 0;
+  ks.queries.length = 0;
+  process.env.ENABLE_DEMO_SEED = 'true';
+});
+
+afterEach(() => {
+  if (savedSeed === undefined) delete process.env.ENABLE_DEMO_SEED;
+  else process.env.ENABLE_DEMO_SEED = savedSeed;
+});
+
+describe('KS-1868 identity users seed catch reads the thrown value safely', () => {
+  it('control ks1868 C1 seed: an ordinary Error is logged with its message and the request carries on to a 200', async () => {
+    ks.thrown = { value: new Error('db boom 10.0.0.7') };
+    const res = await invoke();
+    expect(seedLog()?.message).toBe('[Identity] Seed skipped: db boom 10.0.0.7');
+    expect(usersQueried()).toBe(true);
+    expect(res.statusCode).toBe(200);
+    expect(res.body).toEqual({ success: true, users: [] });
+  });
+
+  it('control ks1868 C2 seed: with no seed failure nothing is logged as skipped and the request answers 200', async () => {
+    const res = await invoke();
+    expect(seedLog()).toBeUndefined();
+    expect(res.statusCode).toBe(200);
+    expect(res.body).toEqual({ success: true, users: [] });
+  });
+
+  it('RED ks1868 R1 seed: a revoked Proxy thrown value is logged as a constant reason and the request carries on to a 200', async () => {
+    ks.thrown = { value: revoked() };
+    const res = await invoke();
+    expect(seedLog()?.message).toBe('[Identity] Seed skipped: unreadable thrown value');
+    expect(usersQueried()).toBe(true);
+    expect(res.statusCode).toBe(200);
+    expect(res.body).toEqual({ success: true, users: [] });
+  });
+
+  it('RED ks1868 R2 seed: an Error whose message getter throws is logged as a constant reason and the request carries on to a 200', async () => {
+    ks.thrown = { value: getterError() };
+    const res = await invoke();
+    expect(seedLog()?.message).toBe('[Identity] Seed skipped: unreadable thrown value');
+    expect(usersQueried()).toBe(true);
+    expect(res.statusCode).toBe(200);
+    expect(res.body).toEqual({ success: true, users: [] });
+  });
+});
```
