# READY — KS-2011-KS-2011-O143-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2011_o143_p1_api_gateway_redis_fallback_notification_settings_expire_after_the_redis_ttl/out.md.checker/patch.diff`** (from `ls` at 18:12 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2011_o143_p1_api_gateway_redis_fallback_notification_settings_expire_after_the_redis_ttl/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2011_o143_p1_api_gateway_redis_fallback_notification_settings_expire_after_the_redis_ttl/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2011_o143_p1_api_gateway_redis_fallback_notification_settings_expire_after_the_redis_ttl/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 18:12 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2011_o143_p1_api_gateway_redis_fallback_notification_settings_expire_after_the_redis_ttl/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `fcd178ff34fa3b289baeb1c1fb6783161bec3e0d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/services/redis.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/services/redis.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
13	0	Blockchain/Dev/services/api-gateway/src/services/redis.ts
75	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (13 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: redis.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/services/redis.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/services/redis.ts 13 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts 75 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/services/redis.ts` (hunks=4, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=3 of total=7; red cell(s): ['KS-2011 the fallback notification settings expire after the Redis TTL RED ks2011 R1: a per-user entry older than 24 hours is dropped by a cleanup', 'KS-2011 the fallback notification settings expire after the Redis TTL RED ks2011 R2: a shared-namespace entry other than platform-settings older than 24 hours is dropped by a cleanup', 'KS-2011 the fallback notification settings expire after the Redis TTL RED ks2011 R3: a cleanup drops the stale entry and keeps the fresh one written beside it']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1886 failed=0 | after: total=1893 failed=0` · `NEW reds: []` [baseline_suite.json total=1886 failed=0; after_suite.json total=1893 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/services/redis.ts` (+13/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts` (+75/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/services/redis.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `fcd178ff34fa3b289baeb1c1fb6783161bec3e0d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2011_o143_p1_api_gateway_redis_fallback_notification_settings_expire_after_the_redis_ttl/input.json`. Brief (given by --brief; its `# ` heading names KS-2011): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2011_o143_p1_api_gateway_redis_fallback_notification_settings_expire_after_the_redis_ttl/KS-2011.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_2011_o143_p1_api_gateway_redis_fallback_notification_settings_expire_after_the_redis_ttl/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/services/redis.ts b/Blockchain/Dev/services/api-gateway/src/services/redis.ts
--- a/Blockchain/Dev/services/api-gateway/src/services/redis.ts
+++ b/Blockchain/Dev/services/api-gateway/src/services/redis.ts
@@ -683,1 +683,4 @@
+// KS-2011: the two notification-settings Maps below carry no expiry of their own. This Map records when each entry was written (key `n:<key>` or `u:<userId>`)
+// so cleanupFallbackStores can drop entries older than TTL.privacy, the lifetime the Redis branch gives them. `platform-settings` is configuration (KS-1233) and is never recorded.
+const notificationFallbackWrittenAt = new Map<string, number>();
 const notificationSettingsStore = new Map<string, object>();
@@ -700,3 +703,4 @@
   } else {
+    if (key !== 'platform-settings') notificationFallbackWrittenAt.set(`n:${key}`, Date.now());
     notificationSettingsStore.set(key, data);
   }
@@ -729,3 +733,4 @@
   } else {
+    notificationFallbackWrittenAt.set(`u:${userId}`, Date.now());
     userNotificationSettingsStore.set(userId, data);
   }
@@ -752,3 +757,11 @@
     }
   }
+  // KS-2011: notification settings written in fallback mode expire after TTL.privacy, as they do in Redis; platform-settings is never recorded, so it never expires.
+  for (const [recorded, writtenAt] of notificationFallbackWrittenAt.entries()) {
+    if (now - writtenAt > TTL.privacy * 1000) {
+      notificationFallbackWrittenAt.delete(recorded);
+      if (recorded.startsWith('n:')) notificationSettingsStore.delete(recorded.slice(2));
+      else userNotificationSettingsStore.delete(recorded.slice(2));
+    }
+  }
 }
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks2011-notification-fallback-settings-expire-after-the-redis-ttl.test.ts
@@ -0,0 +1,75 @@
+import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
+import * as redisService from '../services/redis';
+
+// KS-2011 (gate 197 G197-F2): in the in-memory fallback mode of services/redis.ts the two notification-settings Maps are written when Redis
+// is not available and are never pruned: cleanupFallbackStores touches only the brute-force and rate-limit stores. The Redis branch gives
+// the same values a 24 hour TTL (TTL.privacy), except `platform-settings`, which is configuration and is written without one (KS-1233).
+// The cells never call initRedis, so the module stays in its fallback (asserted). Only Date is faked, so the pruning is driven by calling
+// cleanupFallbackStores directly after moving the clock; no interval or timer is involved.
+const HOUR_MS = 60 * 60 * 1000;
+const T0 = new Date('2026-11-11T00:00:00Z').getTime();
+
+beforeEach(() => {
+  vi.useFakeTimers({ toFake: ['Date'] });
+  vi.setSystemTime(T0);
+});
+afterEach(() => {
+  vi.useRealTimers();
+});
+
+function advanceHours(hours: number): void {
+  vi.setSystemTime(Date.now() + hours * HOUR_MS);
+}
+
+describe('KS-2011 the fallback notification settings expire after the Redis TTL', () => {
+  it('control ks2011 C0: the module is in its in-memory fallback', () => {
+    expect(redisService.isRedisAvailable()).toBe(false);
+  });
+
+  it('control ks2011 C1: a per-user entry younger than 24 hours survives a cleanup', async () => {
+    await redisService.setUserNotificationSettings('ks2011-c1', { success: true });
+    advanceHours(23);
+    redisService.cleanupFallbackStores();
+    expect(await redisService.getUserNotificationSettings('ks2011-c1')).toEqual({ success: true });
+  });
+
+  it('control ks2011 C2: platform-settings is configuration and survives a cleanup 48 hours after its write', async () => {
+    await redisService.setNotificationSettings('platform-settings', { general: { platformName: 'ks2011' } });
+    advanceHours(48);
+    redisService.cleanupFallbackStores();
+    expect(await redisService.getNotificationSettings('platform-settings')).toEqual({ general: { platformName: 'ks2011' } });
+  });
+
+  it('control ks2011 C3: a rewrite restarts the clock, so an entry rewritten 23 hours in is still there at 25 hours', async () => {
+    await redisService.setUserNotificationSettings('ks2011-c3', { v: 1 });
+    advanceHours(23);
+    await redisService.setUserNotificationSettings('ks2011-c3', { v: 2 });
+    advanceHours(2);
+    redisService.cleanupFallbackStores();
+    expect(await redisService.getUserNotificationSettings('ks2011-c3')).toEqual({ v: 2 });
+  });
+
+  it('RED ks2011 R1: a per-user entry older than 24 hours is dropped by a cleanup', async () => {
+    await redisService.setUserNotificationSettings('ks2011-r1', { success: true });
+    advanceHours(24.01);
+    redisService.cleanupFallbackStores();
+    expect(await redisService.getUserNotificationSettings('ks2011-r1')).toBeNull();
+  });
+
+  it('RED ks2011 R2: a shared-namespace entry other than platform-settings older than 24 hours is dropped by a cleanup', async () => {
+    await redisService.setNotificationSettings('ks2011-r2', { v: 1 });
+    advanceHours(24.01);
+    redisService.cleanupFallbackStores();
+    expect(await redisService.getNotificationSettings('ks2011-r2')).toBeNull();
+  });
+
+  it('RED ks2011 R3: a cleanup drops the stale entry and keeps the fresh one written beside it', async () => {
+    await redisService.setUserNotificationSettings('ks2011-r3-old', { v: 'old' });
+    advanceHours(23);
+    await redisService.setUserNotificationSettings('ks2011-r3-new', { v: 'new' });
+    advanceHours(2);
+    redisService.cleanupFallbackStores();
+    expect(await redisService.getUserNotificationSettings('ks2011-r3-old')).toBeNull();
+    expect(await redisService.getUserNotificationSettings('ks2011-r3-new')).toEqual({ v: 'new' });
+  });
+});
```

> NOTE (operator o143, 2026-11-11): Design call by the operator, not in the ticket: entries older than TTL.privacy (24 h, the Redis lifetime) are pruned by a written-at Map; platform-settings never expires (KS-1233). Four insert-only hunks; Wednesday read the + lines at source.
