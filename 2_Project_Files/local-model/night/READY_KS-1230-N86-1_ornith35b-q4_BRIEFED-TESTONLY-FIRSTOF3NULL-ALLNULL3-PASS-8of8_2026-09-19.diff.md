# READY — KS-1230-N86-1 (Ornith, briefed, test_only) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1230-ornith35b-night5/out.md.checker/patch.diff`** (from `ls`, 23:51).

**Held 23:51 2026-09-19 by the 18:0x Wednesday seat after a source read** (woken on the verdicts by the background waiter). Tip `4273adfac`. Pins a null allow-list first of three and all-null (N86-1; FIRSTOF3NULL reds both cells, declared). Test-only: 0 `-` lines, one file under `__tests__/`; every `+` line = the brief; crossed control (the other round-16 briefs) mostly absent. Source: the #1084-#1091 gate's NOT-PINNED rows. Raise: Refs KS-1230, never Closes.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS T7[ALLNULL3] every control green under the tamper
T6 summary: 2/2 tamper(s) red exactly their declared set
T7 summary: controls green under all 2 tamper(s)
T8 summary: all 2 tamper file(s) restored by bytes
SUMMARY test_only file=Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts mode=modify runner=vitest cells=13 tampers=2 apply=strict
RESULT: PASS (8/8)

## Diff
```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
@@ -153,1 +153,11 @@
+  it('RED KS-1230 N86-1: a NULL allow-list FIRST of three integrations is stored as null, the two after it unchanged', async () => {
+    const res = await dispatch(h.router, { integrations: [{ id: 'ks1230-f1', config: { allowedDocumentTypes: null } }, { id: 'ks1230-f2', config: { allowedDocumentTypes: ['SSD_DOCUMENT'] } }, { id: 'ks1230-f3', config: { allowedDocumentTypes: ['PASSPORT'] } }] });
+    const firstOf3 = ((h.writes[0]?.value as any)?.integrations ?? []).map((x: any) => x?.config?.allowedDocumentTypes);
+    expect([res._status, h.writes.length, firstOf3]).toEqual([200, 1, [null, ['SSD_DOCUMENT'], ['PASSPORT']]]);
+  });
+  it('RED KS-1230 N86-1: three NULL allow-lists are all stored as null', async () => {
+    const res = await dispatch(h.router, { integrations: [{ id: 'ks1230-a1', config: { allowedDocumentTypes: null } }, { id: 'ks1230-a2', config: { allowedDocumentTypes: null } }, { id: 'ks1230-a3', config: { allowedDocumentTypes: null } }] });
+    const allNull3 = ((h.writes[0]?.value as any)?.integrations ?? []).map((x: any) => x?.config?.allowedDocumentTypes);
+    expect([res._status, h.writes.length, allNull3]).toEqual([200, 1, [null, null, null]]);
+  });
 });
```
