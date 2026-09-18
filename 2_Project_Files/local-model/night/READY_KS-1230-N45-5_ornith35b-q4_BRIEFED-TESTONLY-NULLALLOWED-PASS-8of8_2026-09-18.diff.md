# READY — KS-1230 N45-5 (Ornith, briefed, TEST_ONLY) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = the fenced diff in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1230-ornith35b-night2/out.md` (one test file; STRICT apply).**

**Held 2026-09-18 17:45 by the 14:4x Wednesday seat after a source read.** Tip `52df64f84`. Closes the #1042-#1045 batch gate's finding N45-5 (a follow-up to merged #1045).

## Source read
- one cell: a NULL allowedDocumentTypes is stored with 200 (no restriction, the KS-1204 reader contract); tamper NULLREFUSED at admin.ts:1132 reds exactly the new cell.
- The 4 '+' lines are IDENTICAL to the brief (0 missing, 0 extra, 0 '-'). T1-T8 PASS incl. T3 strict, T5 green at tip, T6 exact red sets (assertions), T7 controls, T8 restore by sha256.
- **No product change.** Refs KS-1230 (the ticket stays In Progress per §5f). Test-only, tier 2.
**HELD. Not raised.**

---
## The model's output, verbatim

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts
@@ -127,3 +127,7 @@
     expect([a._status, b._status, h.writes.length]).toEqual([200, 200, 2]);
   });
+  it('KS-1230 N45-5: a NULL allow-list is stored with 200 (null means no restriction, as KS-1204 reads it)', async () => {
+    const res = await dispatch(h.router, withTypes(null));
+    expect([res._status, h.writes.length]).toEqual([200, 1]);
+  });
 });
```
