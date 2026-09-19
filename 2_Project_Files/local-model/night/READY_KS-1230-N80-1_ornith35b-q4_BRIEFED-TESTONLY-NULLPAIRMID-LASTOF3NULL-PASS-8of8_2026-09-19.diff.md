# READY — KS-1230-N80-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1230-ornith35b-night4/out.md.checker/patch.diff`** (from `ls`, 19:56).

**Held 19:56 2026-09-19 by the 18:0x Wednesday seat after a source read** (late: passed 19:0x, found unheld at the 19:56 G7 tap). Tip `ba1210afc`. Pins a null pair mid-list and a null last of three (N80-1). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control (the other three round-14 briefs) mostly absent. Source: the #1077-#1083 gate's NOT-PINNED rows. Raise: Refs KS-1230, never Closes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[LASTOF3NULL] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts mode=modify runner=vitest cells=11 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
@@ -143,1 +143,11 @@
+  it('RED KS-1230 N80-1: NULL allow-lists at 2 and 3 of four integrations are both stored as null, their neighbours unchanged', async () => {
+    const res = await dispatch(h.router, { integrations: [{ id: 'ks1230-p1', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }, { id: 'ks1230-p2', config: { allowedDocumentTypes: null } }, { id: 'ks1230-p3', config: { allowedDocumentTypes: null } }, { id: 'ks1230-p4', config: { allowedDocumentTypes: ['PASSPORT'] } }] });
+    const pairMid = ((h.writes[0]?.value as any)?.integrations ?? []).map((x: any) => x?.config?.allowedDocumentTypes);
+    expect([res._status, h.writes.length, pairMid]).toEqual([200, 1, [['SSD_DOCUMENT'], null, null, ['PASSPORT']]]);
+  });
+  it('RED KS-1230 N80-1: a NULL allow-list LAST of three integrations is stored as null, the two before it unchanged', async () => {
+    const res = await dispatch(h.router, { integrations: [{ id: 'ks1230-l1', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }, { id: 'ks1230-l2', config: { allowedDocumentTypes: ['PASSPORT'] } }, { id: 'ks1230-l3', config: { allowedDocumentTypes: null } }] });
+    const lastOf3 = ((h.writes[0]?.value as any)?.integrations ?? []).map((x: any) => x?.config?.allowedDocumentTypes);
+    expect([res._status, h.writes.length, lastOf3]).toEqual([200, 1, [['SSD_DOCUMENT'], ['PASSPORT'], null]]);
+  });
 });
```
