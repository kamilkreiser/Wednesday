# READY — KS-1509-NULLHEIGHT-1 (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1509_p1/out.md.checker/patch.diff`** (from `ls` at 20:38 2026-10-18; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1509_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1509_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1509_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); change lines (`+`/`-`, ordered) IDENTICAL in every file; body lines (context included) DIFFER in anchorStateSync.ts (run 10 vs golden 12 body lines — context, since the change lines are equal) (identical in ks1333-sync-writers-persist-null-not-zero.test.ts); hunk headers identical; APPLIED RESULT IDENTICAL: both patches applied strictly (`git apply -p1`, scratch tempdir) to the tip content carried in input.json['files'] yield byte-identical files (ks1333-sync-writers-persist-null-not-zero.test.ts/anchorStateSync.ts, sha256 equal).

**Held 20:38 2026-10-18 by Wednesday 2026-10-18 20:3x (read at source) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1509_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d0c5d2e0ef8bf8c1e70f9684503c5fb3a3e53c4f`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/services/anchorStateSync.ts , Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	3	Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
34	1	Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (4 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 4 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/services/anchorStateSync.ts byte-exact incl. leading whitespace (apply mode strict): OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)` [a3i_indent.out: `OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts fails at the untouched tip (2 failed / 14 run; controls green; assertion reds)` [red_first.json: failed=2 of total=14; red cell(s): ['KS-1509 - the failed-anchor writer keeps an unknown block height NULL RED KS-1509 F1 a prior blob whose blockHeight is null is written back as null, not 0', 'KS-1509 - the failed-anchor writer keeps an unknown block height NULL RED KS-1509 F2 a prior blob with no blockHeight key is written with blockHeight null, not 0']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts passes with the product hunk (14 passed / 14 run)` [green_after.json: failed=0 of total=14, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1368 failed=0 | after: total=1372 failed=0` · `NEW reds: []` [baseline_suite.json total=1368 failed=0; after_suite.json total=1372 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +38/-4 test=src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (+4/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts` (+34/-1); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0c5d2e0ef8bf8c1e70f9684503c5fb3a3e53c4f` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1509_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1509_p1/KS-1509.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1509_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
+++ b/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
@@ -188,6 +188,7 @@ export async function markDocumentAnchorFailed(
       // KS-1004: carry the chain facts forward rather than nulling them. A tx
-      // that failed on chain still has a hash worth keeping; `?? null` / `?? 0`
-      // reproduce the previous values exactly for the no-hash case.
+      // that failed on chain still has a hash worth keeping; `?? null` keeps the
+      // no-hash case's null. KS-1509: an unknown height stays null as well (the
+      // KS-1333 direction), never a fabricated 0; a real prior height is kept.
       txHash: prior?.txHash ?? null,
-      blockHeight: prior?.blockHeight ?? 0,
+      blockHeight: prior?.blockHeight ?? null,
       ...(prior?.network ? { network: prior.network } : {}),
--- a/Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1333-sync-writers-persist-null-not-zero.test.ts
@@ -32,3 +32,3 @@ jest.mock('../utils/logger', () => ({
 
-import { pollAnchorUntilConfirmed, reconcileDocumentAnchorState } from '../services/anchorStateSync';
+import { markDocumentAnchorFailed, pollAnchorUntilConfirmed, reconcileDocumentAnchorState } from '../services/anchorStateSync';
 import type { DocumentRecord } from '../repositories/documentRepo';
@@ -128 +128,34 @@ describe('KS-1333 item 4 - an unknown block number is persisted as NULL, never a
 });
+
+// KS-1509 (one of its seven sites; documents.ts and the two verification heal paths are NOT changed here): the failed-anchor
+// writer markDocumentAnchorFailed carried an unknown prior height forward as `?? 0`, so a document that a KS-1333 writer had
+// stored with a NULL height got a fabricated 0 back the moment its anchor failed. It now carries null forward; a real prior
+// height is still kept, and a confirmed anchor is still never written.
+describe('KS-1509 - the failed-anchor writer keeps an unknown block height NULL', () => {
+  async function failWith(blockchain: Record<string, unknown>): Promise<Record<string, any>> {
+    mockGetDocument.mockResolvedValue(docWithBlob(blockchain));
+    await markDocumentAnchorFailed('doc-ks1333', 'tenant-1', 'anchor_1', 'ks1509 chain failure');
+    return writtenBlob();
+  }
+
+  it('RED KS-1509 F1 a prior blob whose blockHeight is null is written back as null, not 0', async () => {
+    const blob = await failWith({ txHash: null, blockHeight: null, status: 'submitted', anchorId: 'anchor_1' });
+    expect([blob.status, 'blockHeight' in blob, blob.blockHeight]).toEqual(['anchor_failed', true, null]);
+  });
+
+  it('RED KS-1509 F2 a prior blob with no blockHeight key is written with blockHeight null, not 0', async () => {
+    const blob = await failWith({ txHash: null, status: 'submitted', anchorId: 'anchor_1' });
+    expect([blob.status, 'blockHeight' in blob, blob.blockHeight]).toEqual(['anchor_failed', true, null]);
+  });
+
+  it('CONTROL KS-1509 F3 a real prior height and hash are carried forward unchanged', async () => {
+    const blob = await failWith({ txHash: REAL_TX, blockHeight: 4242, status: 'submitted', anchorId: 'anchor_1' });
+    expect([blob.status, blob.txHash, blob.blockHeight]).toEqual(['anchor_failed', REAL_TX, 4242]);
+  });
+
+  it('CONTROL KS-1509 F4 a confirmed anchor is never downgraded: nothing is written', async () => {
+    mockGetDocument.mockResolvedValue(docWithBlob({ txHash: REAL_TX, blockHeight: null, status: 'confirmed', anchorId: 'anchor_1' }));
+    await markDocumentAnchorFailed('doc-ks1333', 'tenant-1', 'anchor_1', 'ks1509 late failure');
+    expect(mockUpdateDocument).not.toHaveBeenCalled();
+  });
+});
```
