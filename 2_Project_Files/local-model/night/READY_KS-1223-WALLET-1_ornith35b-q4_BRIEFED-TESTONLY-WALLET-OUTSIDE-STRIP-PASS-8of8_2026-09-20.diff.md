# READY — KS-1223-WALLET-1 (Ornith, briefed, test_only, vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1223-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 23:31 2026-09-20). Strict `git apply --numstat` → `6 0 …/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts`. ONE test file, **zero product bytes** (0 non-test `+++` headers).

**Held 23:31 2026-09-20 by the 21:2x Wednesday seat after a source read.** Tip `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`. Adds one cell to the KS-1041 strip suite pinning that `x-wallet-address` is OUTSIDE the edge strip (`utils/trustHeaders.ts`): a client-sent value survives `stripTrustHeaders` while the trust headers are removed. **`Refs KS-1223`, never a closing word** — the ticket's referral half (`referrals.ts:55`) is not pinned.

**Why it is worth having.** KS-1223 asks whether the wallet header should be trusted-stripped; today it is not, and nothing asserted either way. The cell makes the current contract explicit so the ticket's fix round has a red to flip — a characterisation pin, not an endorsement.

**Source read (Wednesday, same action):** 6 `+` lines in the one test file; the declared cell `walletoutside` (full title in the brief) present; no product file touched.

**Tampers (checker T6, each reds exactly the new cell; restored by bytes):** WALLETINPATTERN — `trustHeaders.ts:40` adds `|wallet` to the alternation; BAGDELETESWALLET — `:52` adds an explicit delete of `x-wallet-address`. Both `From` lines byte-checked at the tip by Wednesday (unique, 1 hit each).

**Checker (23:30):** `RESULT: PASS (8/8)`, apply strict, T5 cells present by full title. **Drafter's pre-queue measurements:** real checker on the brief's own diff PASS 8/8 (draft + placed); `prefix-declared control` → FAIL T5 `DECLARED CELL NOT IN THE RUN`; predicate-only cell → FAIL T6 `reds NOTHING`; api-gateway suite 674 → 675 green; tsc rc 0.

**For the raise seat:** strict apply; test-only (STOP on any product byte); api-gateway vitest 675 expected; `Refs KS-1223`. Partition: the ks1041 test file is disjoint from Seat B 10th's three PRs, KS-1234 (index.ts) and Seat A's anchoring/**. Bank with KS-1234 and KS-1279 for the next raise seat.

---
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts
@@ -113,1 +113,7 @@
+  it('RED KS-1223: x-wallet-address is OUTSIDE the edge strip - a client-sent value survives stripTrustHeaders while the trust family is removed', () => {
+    expect(isStrippedTrustHeader('x-wallet-address')).toBe(false);
+    const headers: Record<string, unknown> = { 'x-wallet-address': 'addr_client_supplied', 'x-user-id': 'user-1', authorization: 'Bearer real-token' };
+    stripTrustHeaders(headers);
+    expect([headers['x-wallet-address'], headers['x-user-id'], headers.authorization]).toEqual(['addr_client_supplied', undefined, 'Bearer real-token']);
+  });
 });
