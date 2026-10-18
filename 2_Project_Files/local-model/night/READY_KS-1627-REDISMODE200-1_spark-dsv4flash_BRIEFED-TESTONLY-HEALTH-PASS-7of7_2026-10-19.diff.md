# READY — KS-1627-REDISMODE200-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1627_p2/out.md.checker/patch.diff`** (from `ls` at 07:16 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1627_p2/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1627_p2/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 07:16 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1627_p2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/api-gateway/src/services/health.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	1	Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (21 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 24 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 21 line(s) byte-exact incl. leading whitespace (of 21; 24 line(s) added by the apply)` [a3i_indent.out: `OK 21 line(s) byte-exact incl. leading whitespace (of 21; 24 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/api-gateway/src/services/health.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `7dd1d26940cec8d1` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/services/health.ts:53)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1627_p2_071101/clone/Blockchain/Dev/services/api-gateway/src/services/health.ts:53: '    if (redisService.isRedisAvailable?.() === false) {' -> '    if (redisService.isRedisAvailable?.() === false || true) {'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/api-gateway/src/services/health.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 53. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts fails at the untouched tip (1 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=1 of total=5; red cell(s): ['KS-1627 - the real redis module in its fallback state makes GET /api/connector/info refuse RED KS-1627 R3: with the real module in REDIS mode (over a fake ioredis) the stored list is read and answered with 200, never refused']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1195 failed=0 | after: total=1196 failed=0` · `NEW reds: []` [baseline_suite.json total=1195 failed=0; after_suite.json total=1196 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +24/-1 test=src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts` (+24/-1 per numstat.out); the product `Blockchain/Dev/services/api-gateway/src/services/health.ts` is the tamper target and is byte-unchanged (sha256 7dd1d26940cec8d1, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `83ed01af70fd5ed6cca9ac66f28ddcb8a1034105` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1627_p2/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1627_p2/KS-1627.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1627_p2/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1627-info-reader-real-redis-fallback-refuses.test.ts
@@ -14,2 +14,2 @@
-import { describe, it, expect, beforeAll, afterAll } from 'vitest';
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
 import express from 'express';
@@ -21 +21,16 @@
+const FAKE = vi.hoisted(() => ({ store: new Map<string, string>() }));
+
+// KS-1627 R3: a fake ioredis (the ks1233 shape, with a store) so the REAL services/redis module can be put in Redis mode by initRedis().
+vi.mock('ioredis', () => ({
+  default: class FakeRedis {
+    constructor(_url?: string, _opts?: unknown) { /* initRedis only calls the methods below */ }
+    on(): this { return this; }
+    async connect(): Promise<void> { /* the fake is always connected */ }
+    async ping(): Promise<string> { return 'PONG'; }
+    async get(key: string): Promise<string | null> { return FAKE.store.get(key) ?? null; }
+    async set(key: string, value: string): Promise<string> { FAKE.store.set(key, value); return 'OK'; }
+    async setex(key: string, _ttl: number, value: string): Promise<string> { FAKE.store.set(key, value); return 'OK'; }
+  },
+}));
+
 const CONNECTOR_ID = 'ks1627-c1';
@@ -67,2 +82,10 @@
   });
+
+  it('RED KS-1627 R3: with the real module in REDIS mode (over a fake ioredis) the stored list is read and answered with 200, never refused', async () => {
+    expect(await realRedis.initRedis()).toBe(true);
+    expect(realRedis.isRedisAvailable()).toBe(true);
+    await realRedis.setNotificationSettings('platform-settings', { integrations: [{ id: CONNECTOR_ID, config: { allowedDocumentTypes: ['KS1627_REDIS_DOC'] } }] });
+    const r = await getInfo();
+    expect([r.status, r.body?.id, r.body?.allowedDocumentTypes]).toEqual([200, CONNECTOR_ID, ['KS1627_REDIS_DOC']]);
+  });
 });
```
