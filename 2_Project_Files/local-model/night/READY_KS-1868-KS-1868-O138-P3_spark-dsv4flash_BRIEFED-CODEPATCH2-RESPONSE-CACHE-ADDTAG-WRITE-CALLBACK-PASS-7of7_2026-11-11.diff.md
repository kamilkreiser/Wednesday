# READY — KS-1868-KS-1868-O138-P3 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p3_shared_response_cache_add_tag_and_write_callback_catches_guard_the_thrown_value_read/out.md.checker/patch.diff`** (from `ls` at 16:01 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p3_shared_response_cache_add_tag_and_write_callback_catches_guard_the_thrown_value_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p3_shared_response_cache_add_tag_and_write_callback_catches_guard_the_thrown_value_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o138_p3_shared_response_cache_add_tag_and_write_callback_catches_guard_the_thrown_value_read/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 16:01 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p3_shared_response_cache_add_tag_and_write_callback_catches_guard_the_thrown_value_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/cache/response-cache.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/cache/response-cache.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/packages/shared/src/cache/response-cache.ts
139	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: response-cache.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/cache/response-cache.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/cache/response-cache.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts 139 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/cache/response-cache.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 the response cache addTag and write callback read a failure safely RED ks1868 R1 addTag: a revoked Proxy rejection is logged as a constant reason with no unhandled rejection', 'KS-1868 the response cache addTag and write callback read a failure safely RED ks1868 R2 addTag: an Error whose message getter throws is logged as a constant reason with no unhandled rejection', 'KS-1868 the response cache addTag and write callback read a failure safely RED ks1868 R3 write callback: a revoked Proxy rejection of the store write is logged as a constant reason with no unhandled rejection', 'KS-1868 the response cache addTag and write callback read a failure safely RED ks1868 R4 write callback: an Error whose message getter throws is logged as a constant reason with no unhandled rejection']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1623 failed=1 | after: total=1629 failed=1` · `NEW reds: []` [baseline_suite.json total=1623 failed=1; after_suite.json total=1629 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/cache/response-cache.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts` (+139/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/cache/response-cache.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p3_shared_response_cache_add_tag_and_write_callback_catches_guard_the_thrown_value_read/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o138_p3_shared_response_cache_add_tag_and_write_callback_catches_guard_the_thrown_value_read/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p3_shared_response_cache_add_tag_and_write_callback_catches_guard_the_thrown_value_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/cache/response-cache.ts b/Blockchain/Dev/packages/shared/src/cache/response-cache.ts
--- a/Blockchain/Dev/packages/shared/src/cache/response-cache.ts
+++ b/Blockchain/Dev/packages/shared/src/cache/response-cache.ts
@@ -153,5 +153,11 @@
       await this.redis.sadd(`${this.tagPrefix}${tag}`, key);
     } catch (error) {
-      logger.error('[ResponseCache] Failed to add tag', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('[ResponseCache] Failed to add tag', { error: reason });
     }
   }
@@ -331,4 +337,10 @@
         // Store in cache
         defaultStore.set(cacheKey, cachedResponse, ttl + staleWhileRevalidate).catch(err => {
-          logger.error('[ResponseCache] Cache write error', { error: err instanceof Error ? err.message : String(err) });
+          let reason: string;
+          try {
+            reason = err instanceof Error ? err.message : String(err);
+          } catch {
+            reason = 'unreadable thrown value';
+          }
+          logger.error('[ResponseCache] Cache write error', { error: reason });
         });
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-add-tag-and-write-callback-unreadable-throw.test.ts
@@ -0,0 +1,139 @@
+import { describe, it, expect, vi, beforeAll, afterAll, beforeEach } from 'vitest';
+
+// KS-1868: two more catches of the response cache read the caught value with `error instanceof Error ? error.message : String(error)` before
+// their logger.error line: the Redis store's `addTag` and the middleware's `.catch` callback on the cache write (`Cache write error`).
+// Neither is awaited, so when the read itself throws (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on
+// `.message`) the log line is lost AND the rejection is unhandled. Each now logs the constant `unreadable thrown value` for such a value and
+// raises no unhandled rejection; an ordinary Error is still logged with its own message.
+// The redis and store stand-ins are plain objects with plain functions, not vi.fn(): a spy inspects what it rejects with and could itself fail
+// on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  error: vi.fn(),
+  unhandled: 0,
+}));
+
+vi.mock('../logger', () => ({
+  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
+}));
+
+import { initializeRedisCache, setDefaultCacheStore, responseCache } from '../cache/response-cache';
+
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+beforeAll(() => {
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+});
+afterAll(() => {
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+
+async function respond(tags: string[]): Promise<void> {
+  const req = { method: 'GET', headers: {}, originalUrl: '/ks1868', url: '/ks1868' };
+  const res = {
+    statusCode: 200,
+    json: (_b?: unknown) => res,
+    setHeader: () => undefined,
+    getHeader: () => undefined,
+  };
+  await responseCache({ ttl: 60, tags })(req as never, res as never, (() => undefined) as never);
+  res.json({ ok: 1 });
+  await new Promise((r) => setTimeout(r, 30));
+}
+
+async function runAddTag(): Promise<void> {
+  initializeRedisCache({
+    get: () => Promise.resolve(null),
+    setex: () => Promise.resolve('OK'),
+    del: () => Promise.resolve(1),
+    smembers: () => Promise.resolve([]),
+    sadd: () => Promise.reject(h.toThrow),
+  });
+  await respond(['ks1868-tag']);
+}
+
+async function runWriteCallback(): Promise<void> {
+  setDefaultCacheStore({
+    get: () => Promise.resolve(null),
+    set: () => Promise.reject(h.toThrow),
+    delete: () => Promise.resolve(),
+    deleteByTag: () => Promise.resolve(),
+  });
+  await respond([]);
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
+describe('KS-1868 the response cache addTag and write callback read a failure safely', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.error.mockReset();
+    h.unhandled = 0;
+  });
+
+  it('RED ks1868 R1 addTag: a revoked Proxy rejection is logged as a constant reason with no unhandled rejection', async () => {
+    h.toThrow = revoked();
+    await runAddTag();
+    expect(h.unhandled).toBe(0);
+    expect(LOGGED('[ResponseCache] Failed to add tag')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to add tag')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 addTag: an Error whose message getter throws is logged as a constant reason with no unhandled rejection', async () => {
+    h.toThrow = getterThrows();
+    await runAddTag();
+    expect(h.unhandled).toBe(0);
+    expect(LOGGED('[ResponseCache] Failed to add tag')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to add tag')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 write callback: a revoked Proxy rejection of the store write is logged as a constant reason with no unhandled rejection', async () => {
+    h.toThrow = revoked();
+    await runWriteCallback();
+    expect(h.unhandled).toBe(0);
+    expect(LOGGED('[ResponseCache] Cache write error')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Cache write error')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 write callback: an Error whose message getter throws is logged as a constant reason with no unhandled rejection', async () => {
+    h.toThrow = getterThrows();
+    await runWriteCallback();
+    expect(h.unhandled).toBe(0);
+    expect(LOGGED('[ResponseCache] Cache write error')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Cache write error')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('control ks1868 C1 addTag: an ordinary Error is logged with its own message', async () => {
+    h.toThrow = new Error('redis down');
+    await runAddTag();
+    expect(h.unhandled).toBe(0);
+    expect(LOGGED('[ResponseCache] Failed to add tag')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Failed to add tag')[0][1]).toEqual({ error: 'redis down' });
+  });
+
+  it('control ks1868 C2 write callback: an ordinary Error is logged with its own message', async () => {
+    h.toThrow = new Error('redis down');
+    await runWriteCallback();
+    expect(h.unhandled).toBe(0);
+    expect(LOGGED('[ResponseCache] Cache write error')).toHaveLength(1);
+    expect(LOGGED('[ResponseCache] Cache write error')[0][1]).toEqual({ error: 'redis down' });
+  });
+});
```
