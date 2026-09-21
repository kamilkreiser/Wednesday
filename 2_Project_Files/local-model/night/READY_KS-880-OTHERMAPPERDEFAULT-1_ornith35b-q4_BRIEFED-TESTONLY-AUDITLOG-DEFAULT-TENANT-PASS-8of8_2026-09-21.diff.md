# READY — KS-880-OTHERMAPPERDEFAULT-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 16:13 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1119rows-drafter-precheck/OTHERMAPPERDEFAULT/out.md.checker/patch.diff` rc 0, Wednesday 13:5x seat, 2026-09-21).

**Held 16:13 2026-09-21 by Wednesday 13:5x seat, 2026-09-21 after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night2/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts` (modify). `+` lines 8 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 8/8 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `AUDITTENANTRAW` → red exactly ['RED KS-880: rowToAuditLog answers the default tenant for a r']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night2/input.json`. Brief: `night/briefs/KS-880-OTHERMAPPERDEFAULT-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts
@@ -110,4 +110,12 @@
     const DEFAULT_TENANT = 'a0000000-0000-4000-8000-000000000001';
     expect([rowToApiKey({ ...base }).tenantId, rowToApiKey({ ...base, tenant_id: null }).tenantId, rowToApiKey({ ...base, tenant_id: '' }).tenantId, rowToApiKey({ ...base, tenant_id: 't9' }).tenantId]).toEqual([DEFAULT_TENANT, DEFAULT_TENANT, DEFAULT_TENANT, 't9']);
   });
+  it('RED KS-880: rowToAuditLog answers the default tenant for a row whose tenant_id is missing, null or empty, and passes a stored tenant_id through', async () => {
+    const { rowToAuditLog } = await import('../index');
+    const base = {
+      id: 'a1', action: 'login', resource_type: 'user', success: true, created_at: new Date().toISOString(),
+    };
+    const DEFAULT_TENANT = 'a0000000-0000-4000-8000-000000000001';
+    expect([rowToAuditLog({ ...base }).tenantId, rowToAuditLog({ ...base, tenant_id: null }).tenantId, rowToAuditLog({ ...base, tenant_id: '' }).tenantId, rowToAuditLog({ ...base, tenant_id: 't9' }).tenantId]).toEqual([DEFAULT_TENANT, DEFAULT_TENANT, DEFAULT_TENANT, 't9']);
+  });
 });
```
