# READY — KS-1236-SUBMITLEVEL-1 (Ornith, briefed, test_only, vitest, AUTH SURFACE → tier 1) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1236-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 03:29 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp`, Wednesday).

**Held 03:29 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402` (develop at the hold). Adds TWO cells to the same auth test file pinning TODAY's submit-side level-ordering guard (`users.ts:1267`, `if (targetIndex <= currentIndex)`, `LEVEL_ORDER`): a target level EQUAL to the current level, and one BELOW it (a downgrade), are each refused 400 BAD_REQUEST before any store read or INSERT — unpinned today (0 test hits). Refs KS-1236; NEVER Closes.

**Source read (Wednesday, same action):** 14 `+` lines (one hunk `@@ -165,1 +165,15 @@`), all 14 byte-equal to `night/briefs/KS-1236-SUBMITLEVEL-1.md`; 0 `-`; one test file; patch BYTE-IDENTICAL to the golden. First sample, round 1.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** EQUALADMITTED (`<=`→`<`) reds exactly `samelevel`; GUARDNEVERFIRES (`<= currentIndex`→`< 0`) reds both cells — both on `users.ts:1267` (From byte-matches the tip, count 1, control `LEVEL_ORDER` 3, checked by Wednesday); received `[200, undefined, 1, 2]` vs `[400, 'BAD_REQUEST', 0, 0]`; T8 restored by bytes. Controls: 3 full `it` titles. Whole auth suite (drafter): 779/779 → 781/781.

**Checker:** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 twice (`runs/2026-09-21_round23-drafter-precheck/`).

**Collision (measured by Wednesday in a scratch repo at the tip):** KS-1006's two hunks (`@@ -56,1 +56,2 @@`, `@@ -120,1 +121,10 @@`) and KS-1236's (`@@ -165,1 +165,15 @@`) on the SAME test file apply in BOTH orders → one sha `f9f0b7fce6009962`, 244 lines (220+10+14); bad-context control rc 1. Drafter: combined file 14/14 green, whole auth suite 782/782, each of the four tampers reds exactly its own brief's cells (`KS-1006/cross_*.out`). No held READY touches this test file; no live seat owns the auth service's tests (Seat B 11th's six files are api-gateway/timestamping/security/scripts).

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte — these pin an AUTH surface under Wednesday's reading that test-only pins on auth are in and product edits out, Kam's list item 6); auth vitest 779 at the tip → 782 with both; **raise KS-1006 + KS-1236 as ONE PR on this file, KS-1006's hunks first in the diff; AUTH → TIER 1 at the gate, pushed LAST in its batch.**

---
--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts
@@ -165,1 +165,15 @@
+  it('RED KS-1236: a target level EQUAL to the current level is refused 400 BAD_REQUEST before any store read or INSERT', async () => {
+    user('u-1236-same');
+    (state.users.get('u-1236-same') as Record<string, unknown>).verificationLevel = 'ENHANCED';
+    state.caller = { userId: 'u-1236-same', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
+    expect([r.status, code(r.json), state.rows.size, dbQuery.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0, 0]);
+  });
+  it('RED KS-1236: a target level BELOW the current level (a downgrade) is refused 400 BAD_REQUEST before any store read or INSERT', async () => {
+    user('u-1236-down');
+    (state.users.get('u-1236-down') as Record<string, unknown>).verificationLevel = 'HIGH';
+    state.caller = { userId: 'u-1236-down', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/verification', { targetLevel: 'ENHANCED' });
+    expect([r.status, code(r.json), state.rows.size, dbQuery.mock.calls.length]).toEqual([400, 'BAD_REQUEST', 0, 0]);
+  });
 });
