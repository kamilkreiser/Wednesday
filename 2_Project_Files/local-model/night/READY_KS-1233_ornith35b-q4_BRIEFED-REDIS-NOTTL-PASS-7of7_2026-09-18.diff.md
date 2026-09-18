# READY — KS-1233 (Ornith, briefed) — PASS 7/7, HELD for QA

**Held 2026-09-18 10:3x by the 10:0x Wednesday seat.** Source-read done (below) — this is not a
bare checker pass.

| field | value |
|---|---|
| ticket | KS-1233 — in Redis mode platform-settings expires 24 h after the last admin write |
| run | `runs/2026-09-18_ks1233-ornith35b-night2` |
| model | ornith:35b, local, zero Claude tokens |
| tip | `f6669623ccae5ab445be6e0e73fb4f19ae2c89d1` (develop == #1032's merge) |
| product | `services/api-gateway/src/services/redis.ts` (blob `47659ee9c…`, 732 lines) |
| test | `src/__tests__/ks1233-in-redis-mode-platform-settings-expires.test.ts` (new) |
| size | 2 files, +59/-1 |
| verdict | **PASS (7/7)**, `red_first=yes`, `apply_mode=strict` |

## Why this one passed when the morning's four did not
**It had a brief.** `build_input.sh` reported `prompt source: WEDNESDAY BRIEF` rather than
`the ticket description`. The four brief-less inputs queued at 10:0x all failed — two on A4
RED-FIRST, one at A3. This is the same model on the same day.
Lesson: `0_Brain/learnings/2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md`.

## The checker's own evidence
- **A4 RED-FIRST: the cell fails at the untouched tip** — 1 failed / 3 run, **controls green**,
  assertion reds (not a crash, not a hang). This is the property all four morning runs lacked.
- **A5 GREEN-AFTER:** 3/3 pass with the product hunk.
- **A6:** whole api-gateway suite 588/588, **0 NEW reds** vs the untouched tip (baseline 585).
- **A7:** `tsc --noEmit` rc 0.
- **A3b/A3c/A3i:** every must_change site changed, matched by **line number + text**; every brief `+`
  line present **byte-exact including leading whitespace**, strict apply, no tip line re-added.

## Source read — my own, not the checker's
The fix is minimal and correct in shape: `platform-settings` is written with `set` (no expiry),
every other key keeps `setex(TTL.privacy)`. The comment states the consequence rather than the change,
which is the right way round. **A control cell pins that `notif-defaults` still gets `setex … 86400`,
so the model could not pass by removing the TTL globally** — that control is the reason I am
comfortable with a key-name equality test doing the branching.

**⚠ ONE GAP THE DIFF DOES NOT AND CANNOT COVER — flag it to QA and to the deploy:**
this fixes the **write** path only. **Any Redis that already holds `platform-settings` with a TTL
still carries that TTL**, so on an existing deployment the key will expire **once** after this ships,
and the allow-list fails open until the next admin write restores it. The code change alone does not
clear an expiry already set on a live key.
**Therefore:** this needs either a one-time `PERSIST` on the existing key at deploy, or a startup
re-write of `platform-settings`, or an explicit accepted-risk note. **That is a QA/deploy question,
not a defect in this diff** — do not hold the diff for it, but do not let it ship silently either.

**Severity context:** the failure mode is **fail-open on a connector allow-list**, which is why this
is worth doing properly rather than quickly.

## Status
**HELD.** Not raised, not gated, not merged. Under Kam's TESTED grant a merge needs a QA gate at head
plus my signed GO. Auth surfaces stay last; this is not one.

---

## The diff, verbatim

```diff
--- a/services/api-gateway/src/services/redis.ts
+++ b/services/api-gateway/src/services/redis.ts
@@ -682,4 +682,6 @@ export async function setNotificationSettings(key: string, data: object): Promis
   if (isRedisAvailable()) {
-    await redisClient!.setex(fullKey, TTL.privacy, JSON.stringify(data));
+    // KS-1233: platform-settings is CONFIGURATION, not a cache entry. Written with TTL.privacy it vanished 24 h after the last admin write and every connector allow-list then read as "no restriction" (fail open).
+    if (key === 'platform-settings') await redisClient!.set(fullKey, JSON.stringify(data));
+    else await redisClient!.setex(fullKey, TTL.privacy, JSON.stringify(data));
   } else {
     notificationSettingsStore.set(key, data);
--- /dev/null
+++ b/services/api-gateway/src/__tests__/ks1233-in-redis-mode-platform-settings-expires.test.ts
+/**
+ * =============================================================================
+ * KS-1233 - in Redis mode platform-settings must not expire
+ * =============================================================================
+ * redis.ts:683 wrote every notif:<key> with setex(..., TTL.privacy = 86400, ...)
+ * and the only writer of platform-settings is PUT /api/admin/settings
+ * (routes/admin.ts:1127), so 24 h after the last admin write the key was gone,
+ * verification.ts read the absence as integrations [] - no restriction - and
+ * every restricted connector became unrestricted (#1035 gate finding N-A).
+ *
+ * These cells drive the REAL services/redis over a FAKE ioredis that records
+ * every write and its expiry. No Redis server is started.
+ * =============================================================================
+ */
+import { describe, it, expect, beforeAll, vi } from 'vitest';
+
+const H = vi.hoisted(() => ({ writes: [] as Array<{ verb: string; key: string; ttl: number | null }> }));
+
+vi.mock('ioredis', () => ({
+  default: class FakeRedis {
+    constructor(_url?: string, _opts?: unknown) { /* initRedis only calls the methods below */ }
+    on(): this { return this; }
+    async connect(): Promise<void> { /* the fake is always connected */ }
+    async ping(): Promise<string> { return 'PONG'; }
+    async get(): Promise<string | null> { return null; }
+    async set(key: string, _value: string): Promise<string> { H.writes.push({ verb: 'set', key, ttl: null }); return 'OK'; }
+    async setex(key: string, ttl: number, _value: string): Promise<string> { H.writes.push({ verb: 'setex', key, ttl }); return 'OK'; }
+  },
```
