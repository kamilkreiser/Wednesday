# READY — KS-1244-JOINEDKEY-1 (Ornith, briefed, test_only, vitest, AUTH SURFACE → tier 1) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1244-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:16 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS.

**Held 01:16 2026-09-21 by the 23:4x Wednesday seat after a source read.** Tip `778e6cfe2b6061d60ffcf3a57a951c84dc152b67`. Adds ONE cell to `api-gateway/src/__tests__/auth.test.ts` (the direct driver of `authenticateToken` with `apiKeyCache` and a stubbed fetch) pinning TODAY's behaviour on a REQUIRED mount: a repeated `x-api-key` (two individually valid keys joined by Node) is refused 401 with no principal and no Bearer fall-through, in either order. **Scope stated:** the optional-mount fall-through — KS-1244's DEFECT — is deliberately NOT pinned; the refusal message is not asserted (fix-robust). A characterisation pin on an auth surface; the ticket's fix (refuse a repeated key outright) is not this. KS-1244 stays OPEN.

**Source read (Wednesday, same action):** 15 `+` lines, all 15 byte-present in `night/briefs/KS-1244-JOINEDKEY-1.md`; 0 `-`; one test file (T2); sibling KS-1283 control 0/15. First sample, round 1.

**Tampers (T6 each reds exactly `joined` by assertion; T8 restored, sha `9abef1c21164` = tip blob):** SPLITFIRST — `middleware/auth.ts:276` `    const apiKey = req.headers['x-api-key'] as string | undefined;` (count 1 at the tip, control `x-api-key` = 3 lines, byte-checked by Wednesday) → `?.split(',')[0]?.trim()`; FALLTHROUGH — `:279` `    if (presentedKey && !meta && required) {` (count 1) → `&& !String(apiKey).includes(',')`. Controls: 3 full `it` titles, green under both.

**Checker (01:15):** `RESULT: PASS (8/8)`; whole api-gateway 678/678 bare → 679/679 with the cell (drafter's precheck, `runs/2026-09-21_ks1244-drafter-precheck/`). Drafter's unmeasured, carried: a real two-header-line HTTP request through Express (no server booted); the connector-token exchange under SPLITFIRST beyond the fetch mock.

**Collision note:** held READYs KS-1238-F1i (`auth.ts:299`) and KS-1205-F3 (`:300`) tamper the same product file on different lines in their own test files — no shared line, no shared test file.

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); api-gateway vitest 679 expected; `Refs KS-1244`; **auth surface → TIER 1 at the gate, pushed LAST in its batch.** Partition: `auth.test.ts` owned by no live seat. **Banked for the NEXT raise seat: FOUR — KS-1203 NESTEDTYPE-1 + WSTRIM-1 (one PR), KS-1283 PROVADMIN-1, KS-1244 JOINEDKEY-1.**

---
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts
@@ -211,1 +211,16 @@
+    it('RED KS-1244: a repeated x-api-key (two individually valid keys joined by Node) on a required mount is refused 401 with no principal and no Bearer fall-through, in either order', async () => {
+      const meta = { connectorId: 'c-joined', scopes: ['read'], organizationId: 'org1', tenantId: 't1', tenantSlug: 'one', rateLimit: 100, rateLimitWindow: 60 };
+      apiKeyCache.set('sk_first', { result: meta, expiresAt: Date.now() + 60000 });
+      apiKeyCache.set('sk_second', { result: meta, expiresAt: Date.now() + 60000 });
+      fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { valid: false } }) });
+      const outcomes: unknown[] = [];
+      for (const joined of ['sk_first, sk_second', 'sk_second, sk_first']) {
+        const req = makeReq({ headers: { 'x-api-key': joined, authorization: 'Bearer ' + buildTestToken({ sub: 'u-beside', role: 'user' }) } });
+        const res = makeRes();
+        const next = vi.fn();
+        await authenticateToken(true)(req, res as any, next);
+        outcomes.push([joined, next.mock.calls.length, res._status, res._json?.success, res._json?.error?.code, (req as any).user?.role]);
+      }
+      expect(outcomes).toEqual([['sk_first, sk_second', 0, 401, false, 'UNAUTHORIZED', undefined], ['sk_second, sk_first', 0, 401, false, 'UNAUTHORIZED', undefined]]);
+    });
   });
