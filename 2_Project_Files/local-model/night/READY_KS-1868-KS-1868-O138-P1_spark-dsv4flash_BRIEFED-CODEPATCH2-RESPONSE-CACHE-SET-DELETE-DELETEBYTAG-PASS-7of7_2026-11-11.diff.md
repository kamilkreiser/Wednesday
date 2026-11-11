# READY — KS-1868-KS-1868-O138-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p1_shared_response_cache_redis_set_delete_and_delete_by_tag_catches_guard_the_thrown_value_read/out.md.checker/patch.diff`** (from `ls` at 15:50 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p1_shared_response_cache_redis_set_delete_and_delete_by_tag_catches_guard_the_thrown_value_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p1_shared_response_cache_redis_set_delete_and_delete_by_tag_catches_guard_the_thrown_value_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o138_p1_shared_response_cache_redis_set_delete_and_delete_by_tag_catches_guard_the_thrown_value_read/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 15:50 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p1_shared_response_cache_redis_set_delete_and_delete_by_tag_catches_guard_the_thrown_value_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/cache/response-cache.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/cache/response-cache.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/packages/shared/src/cache/response-cache.ts
158	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: response-cache.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/cache/response-cache.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/cache/response-cache.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts 158 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/cache/response-cache.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 the Redis response cache store reads a failure safely RED ks1868 R1 delete: a revoked Proxy rejection is logged as a constant reason and the call does not throw', 'KS-1868 the Redis response cache store reads a failure safely RED ks1868 R2 delete: an Error whose message getter throws is logged as a constant reason and the call does not throw', 'KS-1868 the Redis response cache store reads a failure safely RED ks1868 R3 deleteByTag: a revoked Proxy rejection is logged as a constant reason and the call does not throw', 'KS-1868 the Redis response cache store reads a failure safely RED ks1868 R4 deleteByTag: an Error whose message getter throws is logged as a constant reason and the call does not throw', 'KS-1868 the Redis response cache store reads a failure safely RED ks1868 R5 set: a revoked Proxy rejection is logged as a constant reason by the store itself', 'KS-1868 the Redis response cache store reads a failure safely RED ks1868 R6 set: an Error whose message getter throws is logged as a constant reason by the store itself']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1623 failed=1 | after: total=1632 failed=1` · `NEW reds: []` [baseline_suite.json total=1623 failed=1; after_suite.json total=1632 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/cache/response-cache.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts` (+158/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/cache/response-cache.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p1_shared_response_cache_redis_set_delete_and_delete_by_tag_catches_guard_the_thrown_value_read/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o138_p1_shared_response_cache_redis_set_delete_and_delete_by_tag_catches_guard_the_thrown_value_read/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p1_shared_response_cache_redis_set_delete_and_delete_by_tag_catches_guard_the_thrown_value_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/cache/response-cache.ts b/Blockchain/Dev/packages/shared/src/cache/response-cache.ts
--- a/Blockchain/Dev/packages/shared/src/cache/response-cache.ts
+++ b/Blockchain/Dev/packages/shared/src/cache/response-cache.ts
@@ -125,5 +125,11 @@
       );
     } catch (error) {
-      logger.error('[ResponseCache] Failed to set cache', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('[ResponseCache] Failed to set cache', { error: reason });
     }
   }
@@ -133,5 +139,11 @@
       await this.redis.del(`${this.prefix}${key}`);
     } catch (error) {
-      logger.error('[ResponseCache] Failed to delete cache', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('[ResponseCache] Failed to delete cache', { error: reason });
     }
   }
@@ -145,5 +157,11 @@
       }
     } catch (error) {
-      logger.error('[ResponseCache] Failed to delete by tag', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('[ResponseCache] Failed to delete by tag', { error: reason });
     }
   }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-store-write-unreadable-throw.test.ts
@@ -0,0 +1,158 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: the Redis-backed response cache store logs a failed delete, a failed delete-by-tag and a failed set instead of failing the
+// caller. Each catch read the caught value with `error instanceof Error ? error.message : String(error)` before its logger.error line.
+// Both reads can themselves throw (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`),
+// so the catch itself threw, the log line was lost and the failure reached the caller. Each of the three now logs the constant
+// `unreadable thrown value` for such a value; an ordinary Error is still logged with its own message.
+// The redis stand-in is a plain object with plain functions, not vi.fn(): a spy inspects what it rejects with and could itself fail
+// on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  error: vi.fn(),
+}));
+
+vi.mock('../logger', () => ({
+  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
+}));
+
+import { initializeRedisCache, invalidateCache, invalidateCacheByTag, responseCache } from '../cache/response-cache';
+
+const redis = {
+  get: () => Promise.resolve(null),
+  setex: () => Promise.reject(h.toThrow),
+  del: () => Promise.reject(h.toThrow),
+  smembers: () => Promise.reject(h.toThrow),
+  sadd: () => Promise.resolve(1),
+};
+
+type Outcome = { threw: boolean };
+
+async function runDelete(): Promise<Outcome> {
+  initializeRedisCache(redis);
+  try {
+    await invalidateCache('ks1868');
+    return { threw: false };
+  } catch {
+    return { threw: true };
+  }
+}
+
+async function runDeleteByTag(): Promise<Outcome> {
+  initializeRedisCache(redis);
+  try {
+    await invalidateCacheByTag('ks1868');
+    return { threw: false };
+  } catch {
+    return { threw: true };
+  }
+}
+
+async function runSet(): Promise<Outcome> {
+  initializeRedisCache(redis);
+  const req = { method: 'GET', headers: {}, originalUrl: '/ks1868', url: '/ks1868' };
+  const res = {
+    statusCode: 200,
+    json: (_b?: unknown) => res,
+    setHeader: () => undefined,
+    getHeader: () => undefined,
+  };
+  await responseCache({ ttl: 60 })(req as never, res as never, (() => undefined) as never);
+  res.json({ ok: 1 });
+  await new Promise((r) => setTimeout(r, 20));
+  return { threw: false };
+}
+
+const LOGGED = (msg: string) => h.error.mock.calls.filter((c) => c[0] === msg);
+const revoked = () => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+const getterThrows = () =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 the Redis response cache store reads a failure safely', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.error.mockReset();
+  });
+
+  it('RED ks1868 R1 delete: a revoked Proxy rejection is logged as a constant reason and the call does not throw', async () => {
+    h.toThrow = revoked();
+    const out = await runDelete();
+    expect(out.threw).toBe(false);
+    expect(LOGGED('[ResponseCache] Failed to delete cache')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to delete cache')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 delete: an Error whose message getter throws is logged as a constant reason and the call does not throw', async () => {
+    h.toThrow = getterThrows();
+    const out = await runDelete();
+    expect(out.threw).toBe(false);
+    expect(LOGGED('[ResponseCache] Failed to delete cache')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to delete cache')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 deleteByTag: a revoked Proxy rejection is logged as a constant reason and the call does not throw', async () => {
+    h.toThrow = revoked();
+    const out = await runDeleteByTag();
+    expect(out.threw).toBe(false);
+    expect(LOGGED('[ResponseCache] Failed to delete by tag')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to delete by tag')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 deleteByTag: an Error whose message getter throws is logged as a constant reason and the call does not throw', async () => {
+    h.toThrow = getterThrows();
+    const out = await runDeleteByTag();
+    expect(out.threw).toBe(false);
+    expect(LOGGED('[ResponseCache] Failed to delete by tag')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to delete by tag')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R5 set: a revoked Proxy rejection is logged as a constant reason by the store itself', async () => {
+    h.toThrow = revoked();
+    await runSet();
+    expect(LOGGED('[ResponseCache] Failed to set cache')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to set cache')[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(LOGGED('[ResponseCache] Cache write error')).toHaveLength(0);
+  });
+
+  it('RED ks1868 R6 set: an Error whose message getter throws is logged as a constant reason by the store itself', async () => {
+    h.toThrow = getterThrows();
+    await runSet();
+    expect(LOGGED('[ResponseCache] Failed to set cache')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to set cache')[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(LOGGED('[ResponseCache] Cache write error')).toHaveLength(0);
+  });
+
+  it('control ks1868 C1 delete: an ordinary Error is logged with its own message and the call does not throw', async () => {
+    h.toThrow = new Error('redis down');
+    const out = await runDelete();
+    expect(out.threw).toBe(false);
+    expect(LOGGED('[ResponseCache] Failed to delete cache')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to delete cache')[0][1]).toEqual({ error: 'redis down' });
+  });
+
+  it('control ks1868 C2 deleteByTag: an ordinary Error is logged with its own message and the call does not throw', async () => {
+    h.toThrow = new Error('redis down');
+    const out = await runDeleteByTag();
+    expect(out.threw).toBe(false);
+    expect(LOGGED('[ResponseCache] Failed to delete by tag')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to delete by tag')[0][1]).toEqual({ error: 'redis down' });
+  });
+
+  it('control ks1868 C3 set: an ordinary Error is logged with its own message by the store itself', async () => {
+    h.toThrow = new Error('redis down');
+    await runSet();
+    expect(LOGGED('[ResponseCache] Failed to set cache')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to set cache')[0][1]).toEqual({ error: 'redis down' });
+    expect(LOGGED('[ResponseCache] Cache write error')).toHaveLength(0);
+  });
+});
```
