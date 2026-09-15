# READY — KS-1133 Part A (both verify routes' DESCRIPTIONS in originate.openapi.ts publish their hash-alias precedence — Kam's 2026-09-13 `accept-split` ruling, checklist items 1+2) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on the RETRY (attempt 1 refused at A3d: the model had marked the brief's context lines `summary:`/`description:` as `+`; the retry, carrying its accepted test section, emitted the two lines only), run `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-15_ks1133-ornith35b-night4/retry`, 2026-09-15 23:50
# Source read by me (Wednesday): the two product `+` lines are the brief's byte-for-byte — one new first string term after each `description:` (v1 :1928 → 'providedHash → contentHash → documentHash → hash — hash is read LAST … (v2 reads it FIRST …)'; v2 :1984 → 'hash → providedHash → contentHash → documentHash — hash is read FIRST (v1 reads it LAST …)'); nothing removed; A3c 2/2 + A3d clean; A4 red 3/5 at the tip (assertion reds, controls green), A5 5/5, A6 no new red across services/originate, A7 tsc rc 0. The test (ks978 registry-reading shape) reads each route's description off sharedRegistry; the retry's only difference from attempt 1's accepted test is the third cell's title in double quotes (an apostrophe) — same cells.
# PR NOTES for the Sunday raising seat: (1) bundle with READY_KS-1133-B (the v2 route cell) as ONE PR; regenerate docs/openapi/secuura-api.yaml from the .openapi.ts sources (the spec is generated; the served spec is bind-mounted) and run check:openapi; (2) v1's behavioural cell already exists — ks1103-verify-hash-field.test.ts P1 — cite it, do not duplicate; (3) checklist item 4: the VerifyRequest description at originate.openapi.ts:551 lists 'documentId, hash, title, contentHash' — an incomplete alias set (providedHash/documentHash are accepted at :742) — the ticket says fix it only if the sentence is touched; the PR seat decides; (4) the inserted term sits FIRST in each concatenation so the precedence sentence leads the published description.

```diff
--- a/services/originate/src/__tests__/ks1133-verify-routes-publish-hash-precedence.test.ts
+++ b/services/originate/src/__tests__/ks1133-verify-routes-publish-hash-precedence.test.ts
@@ -0,0 +1,60 @@
+/**
+ * KS-1133 — both verify routes publish their hash-alias precedence
+ */
+import { sharedRegistry } from '@secuura/shared';
+// Importing for the side effect: it registers the paths and schemas on the
+// shared registry so we can read them back.
+import '../originate.openapi';
+
+type AnyDef = Record<string, any>;
+
+const V1 = '/api/verification/verify';
+const V2 = '/api/v2/verification/verify';
+
+function postRoute(path: string): AnyDef {
+  const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
+  const route = defs.find((d) => d.type === 'route' && d.route?.method === 'post' && d.route?.path === path);
+  return route?.route as AnyDef;
+}
+
+function description(path: string): string {
+  return String(postRoute(path)?.description ?? '');
+}
+
+describe('KS-1133 — both verify routes publish their hash-alias precedence', () => {
+  // CONTROL: proves the harness reaches the code by confirming registration.
+  it('KS-1133 control — both verify routes are registered at all', () => {
+    expect(postRoute(V1)).toBeDefined();
+    expect(postRoute(V2)).toBeDefined();
+  });
+
+  // 🔴 Untouched v1 description carries neither phrase → toContain fails.
+  it('🔴 KS-1133 — v1 publishes providedHash → contentHash → documentHash → hash, hash read LAST', () => {
+    expect(description(V1)).toContain('providedHash → contentHash → documentHash → hash');
+    expect(description(V1)).toContain('read LAST');
+  });
+
+  // 🔴 Untouched v2 description carries neither phrase → toContain fails.
+  it('🔴 KS-1133 — v2 publishes hash → providedHash → contentHash → documentHash, hash read FIRST', () => {
+    expect(description(V2)).toContain('hash → providedHash → contentHash → documentHash');
+    expect(description(V2)).toContain('read FIRST');
+  });
+
+  // 🔴 Neither phrase exists in either description before the fix.
+  it("🔴 KS-1133 — each description names the OTHER route's order, so the split is visible from either side", () => {
+    expect(description(V1)).toContain('v2 reads it FIRST');
+    expect(description(V2)).toContain('v1 reads it LAST');
+  });
+
+  // CONTROL: existing descriptions still present after the insert-only edit.
+  it('KS-1133 control — the existing descriptions are still there', () => {
+    expect(description(V1)).toContain('Single source of truth for document verification');
+    expect(description(V2)).toContain('KS-584 P3.');
+  });
+});
--- a/services/originate/src/originate.openapi.ts
+++ b/services/originate/src/originate.openapi.ts
@@ -1926,0 +1926 @@ sharedRegistry.registerPath({
   summary: 'Verify a document (canonical endpoint)',
   description:
+    'KS-1133 hash-alias precedence on THIS route: providedHash → contentHash → documentHash → hash — `hash` is read LAST, so legacy bodies keep their answer (v2 reads it FIRST; the split is by ruling, 2026-09-13). ' +
     'Single source of truth for document verification across all environments ' +
@@ -1983,0 +1984 @@ sharedRegistry.registerPath({
   summary: 'Verify a document — list contract (v2)',
   description:
+    'KS-1133 hash-alias precedence on THIS route: hash → providedHash → contentHash → documentHash — `hash` is read FIRST (v1 reads it LAST; the split is by ruling, 2026-09-13). ' +
     'KS-584 P3. v1 collapses the same-hash registration set to one row; v2 returns EVERY ' +
```
