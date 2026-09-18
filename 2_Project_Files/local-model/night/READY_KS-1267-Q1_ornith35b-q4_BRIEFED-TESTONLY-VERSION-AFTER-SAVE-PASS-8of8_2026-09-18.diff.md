# READY — KS-1267 Q1 half (Ornith, briefed, TEST_ONLY tier — the first live one) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = the fenced diff in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1267-ornith35b-night/out.md` (one test file; applied STRICT, no --recount).**

**Held 2026-09-18 17:27 by the 14:4x Wednesday seat after a source read.** Tip `52df64f84` (develop after #1042-#1045). Test file `services/originate/src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts` (jest). Brief `night/briefs/KS-1267.md` (search round 4).

## Source read
- ONE new cell: `saveDocument` throws once → `/version` answers 500 INTERNAL_ERROR with 0 provenance rows. It pins #1043's record-AFTER-save on /version (the gate's N43-1: Q1 read 0 red without it).
- The 6 '+' lines are IDENTICAL to the brief (0 missing, 0 extra). T1-T8 PASS: green at tip 27/27; tamper Q1 (record above the save, documents.ts:2063) reds EXACTLY the new cell, an assertion failure; controls green; documents.ts restored by sha256.
- **No product change.** Refs KS-1267 (NOT Closes: the Q3 /transfer-custody half waits for KS-1263). Tier 2 test-only.
**HELD. Not raised.**

---
## The model's output, verbatim

```diff
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts
@@ -199,4 +199,10 @@
       expect(r.rows).toHaveLength(0);
     });
+    it('KS-1267: saveDocument throws: 500, no row (the row is recorded only after the save)', async () => {
+      jest.requireMock('../repositories/documentRepo').saveDocument.mockImplementationOnce(async () => { throw new Error('ks1267 save failed'); });
+      const r = await version();
+      expect([r.status, r.code]).toEqual([500, 'INTERNAL_ERROR']);
+      expect(r.rows).toHaveLength(0);
+    });
     it('control: a version that is created records exactly one row, for the source, as version:watermark', async () => {
       const r = await version();
```
