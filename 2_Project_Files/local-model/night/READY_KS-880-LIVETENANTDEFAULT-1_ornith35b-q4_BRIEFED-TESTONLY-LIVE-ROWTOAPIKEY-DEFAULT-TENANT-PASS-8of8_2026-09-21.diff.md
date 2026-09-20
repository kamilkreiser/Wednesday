# READY — KS-880-LIVETENANTDEFAULT-1 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 04:44 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck/LIVETENANTDEFAULT/out.md.checker/patch.diff` rc 0, the 04:3x Wednesday seat).

**Held 04:44 2026-09-21 by the 04:3x Wednesday seat after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night/out.md.checker`, not typed).** Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7`. Touches ONE file: `Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts` (modify). `+` lines 9 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 7/7 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `LIVETENANTRAW` → red exactly ['RED KS-880: rowToApiKey answers the default tenant for a row']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night/input.json`. Brief: `night/briefs/KS-880-LIVETENANTDEFAULT-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks880-ornith35b-night/checker.out`.

```diff
--- a/Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts
@@ -103,2 +103,11 @@
   });
+  it('RED KS-880: rowToApiKey answers the default tenant for a row whose tenant_id is missing, null or empty, and passes a stored tenant_id through', () => {
+    const base = {
+      id: 'k4', organization_id: 'o1', name: 'n', key_hash: 'h',
+      key_prefix: 'sk_test', scopes: '[]', rate_limit: 100, rate_limit_window: 60,
+      usage_count: 0, is_active: true, created_at: new Date().toISOString(),
+    };
+    const DEFAULT_TENANT = 'a0000000-0000-4000-8000-000000000001';
+    expect([rowToApiKey({ ...base }).tenantId, rowToApiKey({ ...base, tenant_id: null }).tenantId, rowToApiKey({ ...base, tenant_id: '' }).tenantId, rowToApiKey({ ...base, tenant_id: 't9' }).tenantId]).toEqual([DEFAULT_TENANT, DEFAULT_TENANT, DEFAULT_TENANT, 't9']);
+  });
 });
```
