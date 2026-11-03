# READY — KS-1868-KS-1868-O96-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p5_shared_redis_client_connect_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 15:50 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p5_shared_redis_client_connect_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p5_shared_redis_client_connect_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p5_shared_redis_client_connect_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p5_shared_redis_client_connect_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 15:50 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p5_shared_redis_client_connect_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/shared/src/cache/redis-client.ts } + { Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/shared/src/cache/redis-client.ts` (product) and `Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/shared/src/cache/redis-client.ts
103	0	Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: redis-client.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/shared/src/cache/redis-client.ts`; test(s): `Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/shared/src/cache/redis-client.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts 103 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/shared/src/cache/redis-client.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 RedisClient.connect reads a connect failure safely RED ks1868 R1 a revoked Proxy is rethrown as is and a constant reason logged', 'KS-1868 RedisClient.connect reads a connect failure safely RED ks1868 R2 an Error whose message getter throws is rethrown as is and a constant reason logged']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=13 failed=0 | after: total=17 failed=0` · `NEW reds: []` [baseline_suite.json total=13 failed=0; after_suite.json total=17 failed=0]
- A6 [verbatim]: `PASS A6 whole services/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/shared/src/cache/redis-client.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts` (+103/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/shared/src/cache/redis-client.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p5_shared_redis_client_connect_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o96_p5_shared_redis_client_connect_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p5_shared_redis_client_connect_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/shared/src/cache/redis-client.ts b/Blockchain/Dev/services/shared/src/cache/redis-client.ts
--- a/Blockchain/Dev/services/shared/src/cache/redis-client.ts
+++ b/Blockchain/Dev/services/shared/src/cache/redis-client.ts
@@ -135,6 +135,12 @@
       await this.client.connect();
     } catch (error) {
-      logger.error('Redis failed to connect', { error: String(error) });
+      let reason: string;
+      try {
+        reason = String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Redis failed to connect', { error: reason });
       throw error;
     }
   }
diff --git a/Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-client-connect-catch-unreadable-throw.test.ts
@@ -0,0 +1,103 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: RedisClient.connect (src/cache/redis-client.ts) catches a failed connect, logs `{ error: String(error) }` and
+// rethrows the ORIGINAL value so the caller sees what Redis raised. The `String(error)` read is unguarded. When the value
+// cannot be read (a revoked Proxy throws on String(); an Error whose `message` getter throws, throws in
+// Error.prototype.toString) the catch itself throws a TypeError first, so the caller never sees the original value and
+// nothing is logged. The ioredis class is a plain class whose connect() rejects with the cell's value; the logger is a
+// plain recorder; no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  errors: [] as unknown[][],
+  warns: [] as unknown[][],
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    debug: () => undefined,
+    info: () => undefined,
+    warn: (...args: unknown[]) => {
+      h.warns.push(args);
+    },
+    error: (...args: unknown[]) => {
+      h.errors.push(args);
+    },
+  },
+}));
+
+vi.mock('ioredis', () => ({
+  default: class FakeRedis {
+    on(): this {
+      return this;
+    }
+    connect(): Promise<void> {
+      return Promise.reject(h.toThrow);
+    }
+  },
+}));
+
+import { redisClient } from '../cache/redis-client';
+
+/** What connect() rejected with, or 'resolved'. */
+// Boxed on purpose: a promise that resolves with a revoked Proxy throws when it reads `.then` on it.
+async function connectOutcome(): Promise<{ caught: unknown }> {
+  try {
+    await redisClient.connect();
+    return { caught: 'resolved' };
+  } catch (e) {
+    return { caught: e };
+  }
+}
+
+const logged = (): unknown[][] => h.errors.filter((a) => String(a[0]).includes('Redis failed to connect'));
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
+describe('KS-1868 RedisClient.connect reads a connect failure safely', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.errors = [];
+    h.warns = [];
+  });
+
+  it('control ks1868 C1 an ordinary Error is rethrown as is and its text logged', async () => {
+    const value = new Error('connect refused');
+    h.toThrow = value;
+    expect((await connectOutcome()).caught === value).toBe(true);
+    expect(logged()[0][1]).toEqual({ error: 'Error: connect refused' });
+  });
+
+  it('control ks1868 C2 a thrown plain string is rethrown as is and that text logged', async () => {
+    const value = 'plain text failure';
+    h.toThrow = value;
+    expect((await connectOutcome()).caught === value).toBe(true);
+    expect(logged()[0][1]).toEqual({ error: 'plain text failure' });
+  });
+
+  it('RED ks1868 R1 a revoked Proxy is rethrown as is and a constant reason logged', async () => {
+    const value = revokedProxy();
+    h.toThrow = value;
+    expect((await connectOutcome()).caught === value).toBe(true);
+    expect(logged()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is rethrown as is and a constant reason logged', async () => {
+    const value = getterThrows();
+    h.toThrow = value;
+    expect((await connectOutcome()).caught === value).toBe(true);
+    expect(logged()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
