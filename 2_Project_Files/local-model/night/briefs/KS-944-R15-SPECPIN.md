# KS-944 R15-SPECPIN - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 0 lines read whole)
File: `Blockchain/Dev/services/auth/src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `vitest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-944_ornith35b-q4_TESTONLY-SPECPIN-PASS-7of7_2026-09-17.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 2626 B sha256[:16] `25a6cc7721ccf6e2`, +57/-0.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 0 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/auth/src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts` at the tip: ABSENT - ONE NEW FILE. Mode: **NEW**.
- Tamper source: the old brief `night/briefs/KS-944.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-944: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-944.md.
- Generator notes: reds INFERRED as every non-CONTROL/COMPLETENESS cell (1) - no RED-prefixed title in the old patch; Wednesday confirms the set against the old READY header; tamper SPECPIN: the one-line From occurs 18x at the tip; WIDENED to a 3-line block starting at :1829 (the occurrence nearest the old line 1829) - an INFERENCE by line proximity; Wednesday confirms the site; Runner: vitest from the old brief header.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-944 (TEST-ONLY: a new services/auth vitest file pins the `security:` of all six /api/auth/wallet/ operations in auth.openapi.ts — the spec source the gateway's auth gate reads; red under the tamper that closes wallet authenticate with bearerAuth at :1829, controls green) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, strict, 2026-09-17 13:49
> # Source read by Wednesday (scratchpad cmp_brief.py): the test file's 57 `+` lines IDENTICAL to the brief fence (a mutated copy unequal); one new file, no product change; apply STRICT; A6 whole services/auth no new red; A7 tsc rc 0.
> # PR NOTES: Closes KS-944 (the test + red-proof are exactly the ticket's ask — confirm at raise; put the contrast in the PR body: the checker's A4 line + 751/751 green under the tamper with the file absent). TIER 2 by the gate tiers (test-only) unless the gate reads the gateway-auth semantics as tier 1. Not measured: ks570 (gateway test), the generated secuura-api.yaml drift step (preflight check:openapi, read not run). Brief night/briefs/KS-944.md; report night/briefs/NEXT_SEARCH_2026-09-17i.REPORT.md.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts` then ONE `@@ -0,0 +1,N @@` hunk, every line `+`, no context, no `-`. No product hunk. 

## The exact change
```
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

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `KS-944 R1 - exactly six wallet operations, the four public ones with an empty security list`
- `KS-944 CONTROL - link and unlink require bearerAuth, and the registry holds more than the wallet routes`  (CONTROL - green on both trees)

## Tampers
### SPECPIN
File: `Blockchain/Dev/services/auth/src/auth.openapi.ts`
Line: 1829
From:
```
  security: [],
  tags: ['Auth', 'Wallet'],
  summary: 'Verify a wallet signature (alias of /api/auth/wallet/verify)',
```
To:
```
  security: [{ bearerAuth: [] }], // TAMPER: KS-944 red-proof, wallet authenticate closed at the edge
  tags: ['Auth', 'Wallet'],
  summary: 'Verify a wallet signature (alias of /api/auth/wallet/verify)',
```
Reds: `KS-944 R1 - exactly six wallet operations, the four public ones with an empty security list`
(From located at the tip: 1 match(es); block tamper of 3 lines; the old brief/input said line 1829)

## Controls
- `KS-944 CONTROL - link and unlink require bearerAuth, and the registry holds more than the wallet routes`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/auth/src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
