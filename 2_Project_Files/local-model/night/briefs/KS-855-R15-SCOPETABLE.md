# KS-855 R15-SCOPETABLE - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 0 lines read whole)
File: `Blockchain/Dev/services/auth/src/__tests__/ks855-the-oauth-available-scopes-list-is.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `vitest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-855_ornith35b-q4_TESTONLY-SCOPETABLE-PASS-7of7_2026-09-17.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 3099 B sha256[:16] `500f8ca4aa5ccc3e`, +82/-0.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 0 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/auth/src/__tests__/ks855-the-oauth-available-scopes-list-is.test.ts` at the tip: ABSENT - ONE NEW FILE. Mode: **NEW**.
- Tamper source: the old brief `night/briefs/KS-855.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-855: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-855.md.
- Generator notes: reds INFERRED as every non-CONTROL/COMPLETENESS cell (2) - no RED-prefixed title in the old patch; Wednesday confirms the set against the old READY header; Runner: vitest from the old brief header.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them on the date in the file name; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-855 (TEST-ONLY: a new services/auth vitest file pins the exact relationship between the OAuth available-scopes list (services/oauth.ts:57-66, 9 names) and SCOPES (packages/shared scopes.ts, 32 names) — red under the tamper at oauth.ts:66, controls green) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, strict, 2026-09-17 14:15
> # Source read by Wednesday (scratchpad cmp_brief.py): the test file's 82 `+` lines IDENTICAL to the brief fence (a mutated copy unequal); one new file, no product change; A6 no new red; A7 tsc rc 0.
> # PR NOTES: `Refs KS-855` (NOT Closes — the two false header comments in packages/shared/src/security/scopes.ts are still owed). Option P of the DEFAULTS report (local-model/night/briefs/DEFAULTS_2026-09-17_KS805-855-839.REPORT.md), Wednesday's call: no consumer, contract or authorisation change. TIER 2 (test-only). The real gap the analysis found (app registration accepts any scope) is a SEPARATE ticket the raising seat files.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/auth/src/__tests__/ks855-the-oauth-available-scopes-list-is.test.ts` then ONE `@@ -0,0 +1,N @@` hunk, every line `+`, no context, no `-`. No product hunk. 

## The exact change
```
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

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `KS-855 R1 - the OAuth list, split by membership in SCOPES, is exactly these two groups`
- `KS-855 R2 - every SCOPES member the OAuth list does not offer is named here`
- `KS-855 CONTROL - both lists load, and the OAuth list holds nine distinct resource:verb names`  (CONTROL - green on both trees)

## Tampers
### SCOPETABLE
File: `Blockchain/Dev/services/auth/src/services/oauth.ts`
Line: 66
From:
```
  'admin:write',           // Admin write operations
```
To:
```
  'subjects:erase',        // TAMPER: KS-855 red-proof, a shared scope arrives unpinned
```
Reds: `KS-855 R1 - the OAuth list, split by membership in SCOPES, is exactly these two groups`, `KS-855 R2 - every SCOPES member the OAuth list does not offer is named here`
(From located at the tip: 1 match(es); the old brief/input said line 66)

## Controls
- `KS-855 CONTROL - both lists load, and the OAuth list holds nine distinct resource:verb names`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/auth/src/__tests__/ks855-the-oauth-available-scopes-list-is.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
