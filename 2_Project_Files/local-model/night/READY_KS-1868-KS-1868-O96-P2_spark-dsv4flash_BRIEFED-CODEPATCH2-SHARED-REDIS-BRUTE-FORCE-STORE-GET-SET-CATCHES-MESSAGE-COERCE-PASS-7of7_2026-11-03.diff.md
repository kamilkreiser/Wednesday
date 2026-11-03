# READY — KS-1868-KS-1868-O96-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p2_shared_redis_brute_force_store_get_set_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 15:46 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p2_shared_redis_brute_force_store_get_set_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p2_shared_redis_brute_force_store_get_set_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p2_shared_redis_brute_force_store_get_set_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p2_shared_redis_brute_force_store_get_set_catches_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 15:46 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p2_shared_redis_brute_force_store_get_set_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/shared/src/security/redis-security-store.ts } + { Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/shared/src/security/redis-security-store.ts` (product) and `Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/shared/src/security/redis-security-store.ts
111	0	Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: redis-security-store.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/shared/src/security/redis-security-store.ts`; test(s): `Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/shared/src/security/redis-security-store.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts 111 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/shared/src/security/redis-security-store.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 RedisBruteForceStore reads a Redis failure safely RED ks1868 R1 get: a revoked Proxy gives null and logs a constant reason', 'KS-1868 RedisBruteForceStore reads a Redis failure safely RED ks1868 R2 get: an Error whose message getter throws gives null and logs a constant reason', 'KS-1868 RedisBruteForceStore reads a Redis failure safely RED ks1868 R3 set: a revoked Proxy resolves and logs a constant reason', 'KS-1868 RedisBruteForceStore reads a Redis failure safely RED ks1868 R4 set: an Error whose message getter throws resolves and logs a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=13 failed=0 | after: total=19 failed=0` · `NEW reds: []` [baseline_suite.json total=13 failed=0; after_suite.json total=19 failed=0]
- A6 [verbatim]: `PASS A6 whole services/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/shared/src/security/redis-security-store.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts` (+111/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/shared/src/security/redis-security-store.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `ca2b2aa350ac557fc70dfc5d70f15dc9a78ea5b8` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p2_shared_redis_brute_force_store_get_set_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o96_p2_shared_redis_brute_force_store_get_set_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o96_p2_shared_redis_brute_force_store_get_set_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/shared/src/security/redis-security-store.ts b/Blockchain/Dev/services/shared/src/security/redis-security-store.ts
--- a/Blockchain/Dev/services/shared/src/security/redis-security-store.ts
+++ b/Blockchain/Dev/services/shared/src/security/redis-security-store.ts
@@ -135,7 +135,13 @@
     try {
       return await redisClient.get<BruteForceRecord>(`${this.prefix}${key}`);
     } catch (error) {
-      logger.error('RedisBruteForceStore error getting record', { error: String(error) });
+      let reason: string;
+      try {
+        reason = String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('RedisBruteForceStore error getting record', { error: reason });
       return null;
     }
   }
@@ -148,6 +154,12 @@
       const ttl = Math.ceil((lifetimeMs || this.defaultLifetime * 1000) / 1000);
       await redisClient.set(`${this.prefix}${key}`, record, ttl);
     } catch (error) {
-      logger.error('RedisBruteForceStore error setting record', { error: String(error) });
+      let reason: string;
+      try {
+        reason = String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('RedisBruteForceStore error setting record', { error: reason });
     }
   }
diff --git a/Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts b/Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/shared/src/__tests__/ks1868-redis-brute-force-store-get-set-unreadable-throw.test.ts
@@ -0,0 +1,111 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: RedisBruteForceStore.get and RedisBruteForceStore.set (src/security/redis-security-store.ts) catch a
+// Redis failure, log it as `{ error: String(error) }` and answer a fallback (get: null; increment: a count of 1) so a
+// cache failure never fails the request. The `String(error)` read is unguarded. When the value cannot be read (a revoked
+// Proxy throws on String(); an Error whose `message` getter throws, throws in Error.prototype.toString) the catch itself
+// throws, so the call REJECTS where an ordinary Error gives the fallback. The Redis client is a plain object of plain
+// functions rejecting with the cell's value (not vi.fn(): a spy inspects what it rejects with); the logger is a plain
+// recorder; no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  errors: [] as unknown[][],
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    debug: () => undefined,
+    info: () => undefined,
+    warn: () => undefined,
+    error: (...args: unknown[]) => {
+      h.errors.push(args);
+    },
+  },
+}));
+
+vi.mock('../cache/redis-client', () => ({
+  CACHE_TTL: { SESSION: 300 },
+  redisClient: {
+    get: () => Promise.reject(h.toThrow),
+    set: () => Promise.reject(h.toThrow),
+    delete: () => Promise.resolve(true),
+    exists: () => Promise.resolve(false),
+  },
+}));
+
+import { RedisBruteForceStore } from '../security/redis-security-store';
+
+type Settled = { threw: boolean; value: unknown };
+
+/** The call's result, or threw:true when it rejects (an assertion can then fail on it). */
+async function settle(call: () => Promise<unknown>): Promise<Settled> {
+  try {
+    return { threw: false, value: await call() };
+  } catch {
+    return { threw: true, value: undefined };
+  }
+}
+
+const logged = (needle: string): unknown[][] => h.errors.filter((a) => String(a[0]).includes(needle));
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
+const getAnswer = async (): Promise<Settled> => settle(() => new RedisBruteForceStore().get('k'));
+const setAnswer = async (): Promise<Settled> =>
+  settle(() => new RedisBruteForceStore().set('k', { attempts: 1, lastAttempt: 1 }));
+
+describe('KS-1868 RedisBruteForceStore reads a Redis failure safely', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.errors = [];
+  });
+
+  it('control ks1868 C1 get: an ordinary Error gives null and logs its text', async () => {
+    h.toThrow = new Error('redis down');
+    expect(await getAnswer()).toEqual({ threw: false, value: null });
+    expect(logged('error getting record')[0][1]).toEqual({ error: 'Error: redis down' });
+  });
+
+  it('control ks1868 C2 set: a thrown plain string resolves and logs that text', async () => {
+    h.toThrow = 'plain text failure';
+    expect(await setAnswer()).toEqual({ threw: false, value: undefined });
+    expect(logged('error setting record')[0][1]).toEqual({ error: 'plain text failure' });
+  });
+
+  it('RED ks1868 R1 get: a revoked Proxy gives null and logs a constant reason', async () => {
+    h.toThrow = revokedProxy();
+    expect(await getAnswer()).toEqual({ threw: false, value: null });
+    expect(logged('error getting record')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 get: an Error whose message getter throws gives null and logs a constant reason', async () => {
+    h.toThrow = getterThrows();
+    expect(await getAnswer()).toEqual({ threw: false, value: null });
+    expect(logged('error getting record')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 set: a revoked Proxy resolves and logs a constant reason', async () => {
+    h.toThrow = revokedProxy();
+    expect(await setAnswer()).toEqual({ threw: false, value: undefined });
+    expect(logged('error setting record')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 set: an Error whose message getter throws resolves and logs a constant reason', async () => {
+    h.toThrow = getterThrows();
+    expect(await setAnswer()).toEqual({ threw: false, value: undefined });
+    expect(logged('error setting record')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
