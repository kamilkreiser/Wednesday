# READY — KS-855-SCOPETABLE-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks855-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks855-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/855SCOPETABLE-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, drain sitting: expected_plus 82/82 in the diff; reds matched 2/2; golden IDENTICAL).

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 82/82 in the diff; reds matched 2/2; golden IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks855-ornith35b-night/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks855-the-oauth-available-scopes-list-is.test.ts` (new). `+` lines 82 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 4/4 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `SCOPETABLE` → red exactly ['KS-855 R1 - the OAuth list, split by membership in SCOPES, i', 'KS-855 R2 - every SCOPES member the OAuth list does not offe']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks855-ornith35b-night/input.json`. Brief: `night/briefs/KS-855-SCOPETABLE-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks855-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks855-the-oauth-available-scopes-list-is.test.ts
@@ -0,0 +1,82 @@
+/**
+ * KS-855: the OAuth scope list and the shared SCOPES vocabulary are two lists,
+ * and this file pins how they relate.
+ *
+ * The OAuth list offers four names the shared vocabulary does not hold, and it
+ * does not offer most of the shared vocabulary, subjects:erase included. Nothing
+ * pinned that, so a name could arrive in one list and never in the other with
+ * every suite green. A change to either list must now be an edit of this table.
+ */
+import { describe, it, expect, vi } from 'vitest';
+
+vi.mock('../db', () => ({
+  query: vi.fn(async () => ({ rows: [], rowCount: 0 })),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+import { AVAILABLE_SCOPES } from '../services/oauth';
+import { SCOPES } from '@secuura/shared/security/scopes';
+
+const EXPECTED_CELLS = 3;
+let CELLS_RUN = 0;
+const SHARED: string[] = [...SCOPES];
+
+describe('KS-855 - the OAuth scope list and SCOPES relate exactly as this table says', () => {
+  it('KS-855 R1 - the OAuth list, split by membership in SCOPES, is exactly these two groups', () => {
+    CELLS_RUN += 1;
+    expect([
+      AVAILABLE_SCOPES.filter((s) => !SHARED.includes(s)).sort(),
+      AVAILABLE_SCOPES.filter((s) => SHARED.includes(s)).sort(),
+    ]).toEqual([
+      ['admin:read', 'admin:write', 'verify:read', 'webhooks:manage'],
+      ['certifications:read', 'certifications:write', 'documents:read', 'documents:write', 'users:read'],
+    ]);
+  });
+  it('KS-855 R2 - every SCOPES member the OAuth list does not offer is named here', () => {
+    CELLS_RUN += 1;
+    expect(SHARED.filter((s) => !AVAILABLE_SCOPES.includes(s)).sort()).toEqual([
+      'analytics:export',
+      'analytics:read',
+      'anchors:read',
+      'anchors:write',
+      'certifications:delete',
+      'certifications:revoke',
+      'certifications:share',
+      'certifications:sign',
+      'documents:assign',
+      'documents:delete',
+      'documents:download',
+      'documents:rename',
+      'documents:revoke',
+      'documents:share',
+      'documents:transfer-custody',
+      'documents:unassign',
+      'documents:upload',
+      'issuer-certs:read',
+      'issuer-certs:revoke',
+      'issuer-certs:sign',
+      'issuer-certs:write',
+      'kyc:read',
+      'kyc:submit',
+      'organizations:register',
+      'subjects:erase',
+      'users:write',
+      'verification:read',
+    ]);
+  });
+  it('KS-855 CONTROL - both lists load, and the OAuth list holds nine distinct resource:verb names', () => {
+    CELLS_RUN += 1;
+    expect([
+      AVAILABLE_SCOPES.length,
+      new Set(AVAILABLE_SCOPES).size,
+      AVAILABLE_SCOPES.every((s) => s.split(':').length === 2),
+      SHARED.includes('subjects:erase'),
+    ]).toEqual([9, 9, true, true]);
+  });
+  it('KS-855 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
