# READY — KS-1230-N92-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1230-ornith35b-night/out.md.checker/patch.diff`** (from `ls`, 03:25).

**Held 03:25 2026-09-20 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `c87458bdd`. Pins a null first of two (mixed) and first of four (N92-1). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control mostly absent. Source: the #1092-#1096 gate's NOT-PINNED rows. Raise: Refs KS-1230, never Closes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[FIRSTOF4NULL] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts mode=modify runner=vitest cells=15 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
@@ -163,1 +163,11 @@
+  it('RED KS-1230 N92-1: a NULL allow-list FIRST of two integrations, the second non-null, is stored as null and the second unchanged', async () => {
+    const res = await dispatch(h.router, { integrations: [{ id: 'ks1230-t1', config: { allowedDocumentTypes: null } }, { id: 'ks1230-t2', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }] });
+    const firstOf2Mixed = ((h.writes[0]?.value as any)?.integrations ?? []).map((x: any) => x?.config?.allowedDocumentTypes);
+    expect([res._status, h.writes.length, firstOf2Mixed]).toEqual([200, 1, [null, ['SSD_DOCUMENT']]]);
+  });
+  it('RED KS-1230 N92-1: a NULL allow-list FIRST of four integrations is stored as null, the three after it unchanged', async () => {
+    const res = await dispatch(h.router, { integrations: [{ id: 'ks1230-q1', config: { allowedDocumentTypes: null } }, { id: 'ks1230-q2', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }, { id: 'ks1230-q3', config: { allowedDocumentTypes: ['PASSPORT'] } }, { id: 'ks1230-q4', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }] });
+    const firstOf4 = ((h.writes[0]?.value as any)?.integrations ?? []).map((x: any) => x?.config?.allowedDocumentTypes);
+    expect([res._status, h.writes.length, firstOf4]).toEqual([200, 1, [null, ['SSD_DOCUMENT'], ['PASSPORT'], ['SSD_DOCUMENT']]]);
+  });
 });
```
