# READY — KS-1006-WRONGCODE-1 (Ornith, briefed, test_only, vitest, AUTH SURFACE → tier 1) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1006-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 03:29 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp`, Wednesday).

**Held 03:29 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402` (develop at the hold). Adds ONE cell (+ one mock line `updateUserOrThrow`) to `auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts` pinning TODAY's `/me/mfa/disable`: with MFA enabled and a secret stored, a six-character code that cannot be a TOTP is refused 400 `Invalid verification code` (`users.ts:1105`, `verifyTOTP`; `me/mfa` had 0 hits in the auth tests). A characterisation pin on an auth surface; KS-1006's own ask is not decided by it. Refs KS-1006; NEVER Closes.

**Source read (Wednesday, same action):** 10 `+` lines (two hunks), all 10 byte-equal to `night/briefs/KS-1006-WRONGCODE-1.md`; 0 `-`; one test file; the run's patch BYTE-IDENTICAL to the drafter's golden (`cmp`). First sample, round 1.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** VERIFYINVERTED and PRESENCEINVERTED, both on `users.ts:1105` (From byte-matches the tip, count 1 by `grep -c -F -x`, control `verifyTOTP` 3, checked by Wednesday); each reds exactly `wrongcode` (`[200, undefined, undefined]` vs `[400, 'Invalid verification code', …]`); T8 restored by bytes. Controls: 3 full `it` titles.

**Checker:** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 twice (`runs/2026-09-21_round23-drafter-precheck/`).

**Collision (measured by Wednesday in a scratch repo at the tip):** KS-1006's two hunks (`@@ -56,1 +56,2 @@`, `@@ -120,1 +121,10 @@`) and KS-1236's (`@@ -165,1 +165,15 @@`) on the SAME test file apply in BOTH orders → one sha `f9f0b7fce6009962`, 244 lines (220+10+14); bad-context control rc 1. Drafter: combined file 14/14 green, whole auth suite 782/782, each of the four tampers reds exactly its own brief's cells (`KS-1006/cross_*.out`). No held READY touches this test file; no live seat owns the auth service's tests (Seat B 11th's six files are api-gateway/timestamping/security/scripts).

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte — these pin an AUTH surface under Wednesday's reading that test-only pins on auth are in and product edits out, Kam's list item 6); auth vitest 779 at the tip → 782 with both; **raise KS-1006 + KS-1236 as ONE PR on this file, KS-1006's hunks first in the diff; AUTH → TIER 1 at the gate, pushed LAST in its batch.**

---
--- a/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts
@@ -56,1 +56,2 @@
+    updateUserOrThrow: vi.fn(async () => null),
     updateUserPlatformScope: vi.fn(async (id: string) => {
@@ -120,1 +121,10 @@
+describe('KS-1006 - POST /me/mfa/disable verifies the code against a stored secret before disabling the factor', () => {
+  it('RED KS-1006: with MFA enabled and a secret stored, a six-character code that cannot be a TOTP is refused 400 Invalid verification code', async () => {
+    user('u-1006-wrong');
+    Object.assign(state.users.get('u-1006-wrong') as Record<string, unknown>, { mfaEnabled: true, mfaSecret: 'JBSWY3DPEHPK3PXP' });
+    state.caller = { userId: 'u-1006-wrong', role: 'USER', tenantId: 'tenant-default' };
+    const r = await call('POST', '/me/mfa/disable', { code: 'abcdef' });
+    expect([r.status, code(r.json), (r.json.error as Row | undefined)?.message]).toEqual([400, 'BAD_REQUEST', 'Invalid verification code']);
+  });
+});
 beforeEach(() => {
