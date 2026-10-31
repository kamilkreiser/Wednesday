# READY — KS-1868-O38-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p2_shared_response_cache_read_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 14:44 2026-10-31; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p2_shared_response_cache_read_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p2_shared_response_cache_read_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p2_shared_response_cache_read_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p2_shared_response_cache_read_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 14:44 2026-10-31 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p2_shared_response_cache_read_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `9e1eb55fde5338d0ad95848736cbd013d7b7f651`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/cache/response-cache.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/cache/response-cache.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/packages/shared/src/cache/response-cache.ts
90	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: response-cache.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/cache/response-cache.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/cache/response-cache.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts 90 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/cache/response-cache.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-1868 responseCache reads a cache-read failure safely RED ks1868 R1 a revoked Proxy rejection logs a constant reason and falls through to next()', 'KS-1868 responseCache reads a cache-read failure safely RED ks1868 R2 an Error whose message getter throws logs a constant reason and falls through to next()']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1081 failed=1 | after: total=1084 failed=1` · `NEW reds: []` [baseline_suite.json total=1081 failed=1; after_suite.json total=1084 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/cache/response-cache.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts` (+90/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/cache/response-cache.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `9e1eb55fde5338d0ad95848736cbd013d7b7f651` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p2_shared_response_cache_read_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o38_p2_shared_response_cache_read_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o38_p2_shared_response_cache_read_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/cache/response-cache.ts b/Blockchain/Dev/packages/shared/src/cache/response-cache.ts
--- a/Blockchain/Dev/packages/shared/src/cache/response-cache.ts
+++ b/Blockchain/Dev/packages/shared/src/cache/response-cache.ts
@@ -296,5 +296,11 @@
         }
       }
     } catch (error) {
-      logger.error('[ResponseCache] Cache read error', { error: error instanceof Error ? error.message : String(error) });
+      let reason: string;
+      try {
+        reason = error instanceof Error ? error.message : String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('[ResponseCache] Cache read error', { error: reason });
     }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts
@@ -0,0 +1,90 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: the responseCache middleware must still log its cache-read error and fall through to
+// the origin handler (`next()`) when the cache store's `get` rejects with a value that cannot be
+// read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on
+// `.message`). A cache failure must never fail the request.
+// The store stand-in is a plain object with plain functions, not vi.fn(): a spy inspects what it
+// rejects with and could itself fail on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  error: vi.fn(),
+}));
+
+vi.mock('../logger', () => ({
+  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
+}));
+
+import { responseCache, setDefaultCacheStore } from '../cache/response-cache';
+
+type Outcome = { threw: boolean; nextCalls: number };
+
+async function run(): Promise<Outcome> {
+  setDefaultCacheStore({
+    get: () => Promise.reject(h.toThrow),
+    set: () => Promise.resolve(),
+    delete: () => Promise.resolve(),
+    deleteByTag: () => Promise.resolve(),
+  });
+  const out: Outcome = { threw: false, nextCalls: 0 };
+  const req = { method: 'GET', headers: {}, originalUrl: '/ks1868', url: '/ks1868' };
+  const res = {
+    statusCode: 200,
+    json: () => res,
+    setHeader: () => undefined,
+    getHeader: () => undefined,
+  };
+  const next = () => {
+    out.nextCalls++;
+  };
+  try {
+    await responseCache({ ttl: 60 })(req as never, res as never, next as never);
+  } catch {
+    out.threw = true;
+  }
+  return out;
+}
+
+const READ_ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]).includes('Cache read error'));
+
+describe('KS-1868 responseCache reads a cache-read failure safely', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.error.mockReset();
+  });
+
+  it('control ks1868 C1 an ordinary Error still logs its message and falls through to next()', async () => {
+    h.toThrow = new Error('redis down');
+    const out = await run();
+    expect(out.threw).toBe(false);
+    expect(out.nextCalls).toBe(1);
+    expect(READ_ERRORS()).toHaveLength(1);
+    expect(READ_ERRORS()[0][1]).toEqual({ error: 'redis down' });
+  });
+
+  it('RED ks1868 R1 a revoked Proxy rejection logs a constant reason and falls through to next()', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.toThrow = proxy;
+    const out = await run();
+    expect(out.threw).toBe(false);
+    expect(out.nextCalls).toBe(1);
+    expect(READ_ERRORS()).toHaveLength(1);
+    expect(READ_ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and falls through to next()', async () => {
+    h.toThrow = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const out = await run();
+    expect(out.threw).toBe(false);
+    expect(out.nextCalls).toBe(1);
+    expect(READ_ERRORS()).toHaveLength(1);
+    expect(READ_ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
