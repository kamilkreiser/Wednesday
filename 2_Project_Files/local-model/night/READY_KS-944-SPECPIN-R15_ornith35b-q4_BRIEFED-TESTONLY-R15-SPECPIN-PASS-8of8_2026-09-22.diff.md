# READY — KS-944-SPECPIN-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks944-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:15 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks944-ornith35b-night/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_r15feed2-drafter-precheck/944SPECPIN-R15/out.md.checker/patch.diff` rc 0, Wednesday 00:05 seat, drain sitting: expected_plus 57/57 in the diff; reds matched 1/1; golden IDENTICAL).

**Held 01:15 2026-09-22 by Wednesday 00:05 seat, drain sitting: expected_plus 57/57 in the diff; reds matched 1/1; golden IDENTICAL after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks944-ornith35b-night/out.md.checker`, not typed).** Tip `581ed7fa124b85c7c2da89ac05d52f99c2502911`. Touches ONE file: `Blockchain/Dev/services/auth/src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts` (new). `+` lines 57 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 3/3 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `SPECPIN` → red exactly ['KS-944 R1 - exactly six wallet operations, the four public o']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks944-ornith35b-night/input.json`. Brief: `night/briefs/KS-944-SPECPIN-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks944-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts
@@ -0,0 +1,57 @@
+/**
+ * KS-944: the api-gateway decides whether a wallet operation needs a bearer by
+ * reading the security list each operation declares in the published spec.
+ *
+ * The auth spec source registers six wallet operations. Four are public by
+ * design and declare an empty security list; link and unlink declare bearerAuth.
+ * Nothing pinned those values, so flipping one closed a public route at the edge
+ * while every suite stayed green. This file reads the real registrations.
+ */
+import { describe, it, expect } from 'vitest';
+import '../auth.openapi';
+import { sharedRegistry } from '@secuura/shared';
+
+const EXPECTED_CELLS = 2;
+let CELLS_RUN = 0;
+
+// every route definition the auth spec module registered
+function routes(): any[] {
+  return (sharedRegistry as any).definitions.filter((d: any) => d.type === 'route');
+}
+
+// each wallet operation as method, path and its declared security, sorted
+function walletOps(): string[] {
+  return routes()
+    .filter((d: any) => String(d.route.path).startsWith('/api/auth/wallet/'))
+    .map((d: any) => {
+      const sec: any = d.route.security;
+      const label = sec === undefined ? 'unstated' : sec.length === 0 ? 'public' : sec.map((s: any) => Object.keys(s).join('+')).join(',');
+      return d.route.method + ' ' + d.route.path + ' ' + label;
+    })
+    .sort();
+}
+
+describe('KS-944 - the wallet operations declare the security the gateway enforces', () => {
+  it('KS-944 R1 - exactly six wallet operations, the four public ones with an empty security list', () => {
+    CELLS_RUN += 1;
+    expect(walletOps()).toEqual([
+      'delete /api/auth/wallet/unlink bearerAuth',
+      'get /api/auth/wallet/status/{walletAddress} public',
+      'post /api/auth/wallet/authenticate public',
+      'post /api/auth/wallet/challenge public',
+      'post /api/auth/wallet/link bearerAuth',
+      'post /api/auth/wallet/verify public',
+    ]);
+  });
+  it('KS-944 CONTROL - link and unlink require bearerAuth, and the registry holds more than the wallet routes', () => {
+    CELLS_RUN += 1;
+    const guarded = walletOps().filter((op) => op.includes('/wallet/link ') || op.includes('/wallet/unlink '));
+    expect([guarded, routes().length > 6]).toEqual([
+      ['delete /api/auth/wallet/unlink bearerAuth', 'post /api/auth/wallet/link bearerAuth'],
+      true,
+    ]);
+  });
+  it('KS-944 COMPLETENESS - every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
