# READY — KS-944 (TEST-ONLY: a new services/auth vitest file pins the `security:` of all six /api/auth/wallet/ operations in auth.openapi.ts — the spec source the gateway's auth gate reads; red under the tamper that closes wallet authenticate with bearerAuth at :1829, controls green) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, strict, 2026-09-17 13:49
# Source read by Wednesday (scratchpad cmp_brief.py): the test file's 57 `+` lines IDENTICAL to the brief fence (a mutated copy unequal); one new file, no product change; apply STRICT; A6 whole services/auth no new red; A7 tsc rc 0.
# PR NOTES: Closes KS-944 (the test + red-proof are exactly the ticket's ask — confirm at raise; put the contrast in the PR body: the checker's A4 line + 751/751 green under the tamper with the file absent). TIER 2 by the gate tiers (test-only) unless the gate reads the gateway-auth semantics as tier 1. Not measured: ks570 (gateway test), the generated secuura-api.yaml drift step (preflight check:openapi, read not run). Brief night/briefs/KS-944.md; report night/briefs/NEXT_SEARCH_2026-09-17i.REPORT.md.

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
