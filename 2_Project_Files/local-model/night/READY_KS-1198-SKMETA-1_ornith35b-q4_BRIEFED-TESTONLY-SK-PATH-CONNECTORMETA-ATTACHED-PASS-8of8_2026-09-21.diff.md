# READY — KS-1198-SKMETA-1 (Ornith, briefed, test_only, vitest, AUTH SURFACE → tier 1) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1198-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:37 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; Wednesday's own strict apply in a scratch repo at the tip rc 0; the run's patch is BYTE-IDENTICAL to the brief's golden hunk (`cmp`).

**Held 01:37 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `778e6cfe2b6061d60ffcf3a57a951c84dc152b67` (develop is `cbae988db` = #1105 on top; its 12 files touch neither `auth.test.ts` nor `middleware/auth.ts` — empty `diff --stat` against a 12-file control). Adds ONE cell at the START of the `describe('authenticateToken')` block in `api-gateway/src/__tests__/auth.test.ts` pinning TODAY's sk_-path behaviour: a validated `sk_` key's `ConnectorMeta` is attached as `req.connectorMeta` (`auth.ts:322`, the ONE setter in the gateway), scopes intact, principal role `connector`, next called once — the ONLY input the connector gates (`verification.ts:1201-1239`, `:1257-1267`, `health.ts:39-43`) read. **Scope stated:** the Bearer path with a connector JWT — KS-1198's DEFECT — is deliberately NOT pinned (a pin there would decide between the ticket's two fix shapes); this pins the half both shapes keep. **NEVER Closes KS-1198** — Refs only; the product decision stays open.

**Source read (Wednesday, same action):** 9 `+` lines, all 9 byte-equal (ordered) to `night/briefs/KS-1198-SKMETA-1.md`; 0 `-`; one test file (T2); crossed control vs KS-1244's 15 `+` lines: 1/15 shared (a closing `});`) — content-level, same file. First sample, round 1 (model wall: 334 eval tokens).

**Tampers (T6 each reds exactly `skmeta` by assertion; T7 controls green; T8 restored, sha `9abef1c21164` = tip blob):** METADROPPED — `middleware/auth.ts:322` `      (req as any).connectorMeta = meta;` (count 1 at the tip by `grep -c -F -x`, control `connectormeta` -i = 5, byte-checked by Wednesday) → `= undefined`; METAWIDENED — same line → meta with `scopes: ['*']`. Controls: 3 full `it` titles (`:147`, `:159`, `:218`), green under both.

**Checker (01:35):** `RESULT: PASS (8/8)`; green at the tip 17/17 cells. The drafter's own precheck did NOT complete before the 23:4x seat rotated (its MEASURED section is unfilled) — so the whole-suite count with the cell is UNMEASURED here; the raise seat measures api-gateway whole (678 bare at 778e6cfe2 per Seat B 11th) → expect 679 with this cell alone, and 680 with KS-1244's.

**Collision note (measured by Wednesday, both orders in a scratch repo at the tip):** same test file as the held `READY_KS-1244-JOINEDKEY-1` — disjoint hunks (this `@@ -136,1 +136,10 @@` at the block's START; KS-1244's `@@ -211,1 +211,16 @@` at its END). Both orders apply rc 0 and produce the SAME file (sha256 `651b0add92b45c42…`, 309 lines = 285 + 9 + 15); bad-context control rc 1. Same product file as held KS-1238-F1i (`:299`), KS-1205-F3 (`:300`), KS-1244 (`:276/:279`) — no shared tamper line. **Raise KS-1244 and KS-1198 in ONE PR on `auth.test.ts`, KS-1244's hunk first in the diff (higher line numbers later)** — or as two PRs in either order.

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); `Refs KS-1198` (and KS-480); **auth surface → TIER 1 at the gate, pushed LAST in its batch.** Partition: `auth.test.ts` owned by no live seat (Seat B 11th's six files exclude it — its STATUS 15:28Z). **Banked for the NEXT raise seat: FIVE — KS-1203 NESTEDTYPE-1 + WSTRIM-1 (one PR), KS-1283 PROVADMIN-1, KS-1244 JOINEDKEY-1 + KS-1198 SKMETA-1 (one PR, auth.test.ts).**

---
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts
@@ -136,1 +136,10 @@
+    it('RED KS-1198: an sk_ key validated on the API-key path attaches the validated key metadata as req.connectorMeta, scopes intact, for the connector gates to read', async () => {
+      const meta = { connectorId: 'c-meta', scopes: ['documents:write'], organizationId: 'org1', tenantId: 't1', tenantSlug: 'one', rateLimit: 100, rateLimitWindow: 60 };
+      apiKeyCache.set('sk_meta', { result: meta, expiresAt: Date.now() + 60000 });
+      fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: {} }) });
+      const req = makeReq({ headers: { 'x-api-key': 'sk_meta' } });
+      const res = makeRes(), next = vi.fn();
+      await authenticateToken(true)(req, res as any, next);
+      expect([next.mock.calls.length, res._status, (req as any).user?.role, (req as any).connectorMeta]).toEqual([1, 0, 'connector', meta]);
+    });
     it('skips auth when required=false and no token is present', async () => {
