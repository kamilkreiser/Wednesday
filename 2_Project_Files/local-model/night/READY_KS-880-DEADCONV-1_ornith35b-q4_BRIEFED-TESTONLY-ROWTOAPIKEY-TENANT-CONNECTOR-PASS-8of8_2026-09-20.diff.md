# READY — KS-880-DEADCONV-1 (Ornith, briefed, test_only, vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks880-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 23:50 2026-09-20). Checker T3: strict `git apply --check` at the tip PASS; `apply=strict` in its SUMMARY line.

**Held 23:50 2026-09-20 by the 23:4x Wednesday seat after a source read.** Tip `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`. Adds ONE cell to `services/security/src/__tests__/row-converters.test.ts` pinning that the dead `converters.ts` `rowToApiKey` maps NEITHER `tenantId` NOR `connectorId` — a row carrying both columns comes back without either key (KS-880's stated defect, pinned as today's behaviour).

**Source read (Wednesday, same action):** 10 `+` lines, all 10 byte-present in `night/briefs/KS-880-DEADCONV-1.md`; 0 `-` lines; touched-file set = the one test file (checker T2); crossed control: the sibling WALLET-1 brief's `+` lines present 1 of 10 (a shared closing line) — path-level and content-level distinct. Model wall 10 s, 330 tokens, first sample, round 1 (no rebrief spent).

**Tampers (checker T6, each reds exactly the new cell; T8 restored by bytes):** TENANTMAPPED — `converters.ts:125` (`organizationId: r.organization_id as string,`, appends a tenantId mapping); CONNECTORMAPPED — `:135` (`expiresAt: …`, appends a connectorId mapping). Both From lines byte-checked by Wednesday at `git show dc061f2bb…:…/security/src/converters.ts` before queueing, each unique in the file.

**Checker (23:48):** `RESULT: PASS (8/8)`; T5 cells present by full title (14 cells in the suite after the add); T7 controls green under both tampers.

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); `services/security` vitest; `Refs KS-880` (the ticket asks for the product fix — this pins the defect as a red-under-fix cell, it does not close it). Partition: `services/security/src/__tests__/row-converters.test.ts` — touched by no live seat (Seat B 10th: api-gateway/originate test files; Seat A 15th: services/anchoring). Banked with KS-1234, KS-1279, KS-1223 → FOUR for the next raise seat.

---
--- a/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts
@@ -154,1 +154,11 @@
+  it('RED KS-880: the dead converters.ts rowToApiKey maps NEITHER tenantId NOR connectorId - a row carrying both columns comes back without either key', () => {
+    const row = {
+      id: 'key_2', organization_id: 'org_1', tenant_id: 'a0000000-0000-4000-8000-000000000002', connector_id: 'conn_1',
+      name: 'connector-2', key_hash: 'h', key_prefix: 'sk_t_', scopes: '["read:docs"]',
+      rate_limit: '100', rate_limit_window: '60', last_used_at: null, usage_count: '0', is_active: true,
+      expires_at: null, created_at: '2026-04-01T00:00:00Z',
+    };
+    const k = rowToApiKey(row);
+    expect([k.organizationId, 'tenantId' in k, 'connectorId' in k]).toEqual(['org_1', false, false]);
+  });
 });
