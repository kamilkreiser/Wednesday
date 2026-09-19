# READY — KS-1230-N97-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1230-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` of that dir, 06:12; test_only → patch.diff only).

**Held 06:12 2026-09-20 by the 03:3x Wednesday seat (the morning session) after a source read.** Tip `e47019878` (tree 706de830). Pins a null allow-list LAST of two (the first non-null) and LAST of four (N97-1, the #1097-#1099 gate NOT-PINNED rows LASTOF2NULLMIXED / LASTOF4NULL). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief (10/10); run input sha256 188dc9aa4d87 = the queued input. Content control: the sibling N92-1 brief (same file) holds 2/10 of these lines (generic closers) — a CONTENT comparison, not path-level (ledger 2026-09-20 R-1). Raise: Refs KS-1230, never Closes. KS-1230 stays In Progress.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[LASTOF4NULL] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts mode=modify runner=vitest cells=17 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
@@ -173,1 +173,11 @@
+  it('RED KS-1230 N97-1: a NULL allow-list LAST of two integrations, the first non-null, is stored as null and the first unchanged', async () => {
+    const res = await dispatch(h.router, { integrations: [{ id: 'ks1230-u1', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }, { id: 'ks1230-u2', config: { allowedDocumentTypes: null } }] });
+    const lastOf2Mixed = ((h.writes[0]?.value as any)?.integrations ?? []).map((x: any) => x?.config?.allowedDocumentTypes);
+    expect([res._status, h.writes.length, lastOf2Mixed]).toEqual([200, 1, [['SSD_DOCUMENT'], null]]);
+  });
+  it('RED KS-1230 N97-1: a NULL allow-list LAST of four integrations is stored as null, the three before it unchanged', async () => {
+    const res = await dispatch(h.router, { integrations: [{ id: 'ks1230-v1', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }, { id: 'ks1230-v2', config: { allowedDocumentTypes: ['PASSPORT'] } }, { id: 'ks1230-v3', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }, { id: 'ks1230-v4', config: { allowedDocumentTypes: null } }] });
+    const lastOf4 = ((h.writes[0]?.value as any)?.integrations ?? []).map((x: any) => x?.config?.allowedDocumentTypes);
+    expect([res._status, h.writes.length, lastOf4]).toEqual([200, 1, [['SSD_DOCUMENT'], ['PASSPORT'], ['SSD_DOCUMENT'], null]]);
+  });
 });
```
