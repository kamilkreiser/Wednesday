# READY — KS-1435-KS-1435-1 (Spark DeepSeek V4 Flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1435-transfer-reject-signature-typed/out.md.checker/patch.diff`** (from `ls` at 11:57 2026-10-07; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1435-transfer-reject-signature-typed/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1435-transfer-reject-signature-typed/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1435-transfer-reject-signature-typed/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1435-transfer-reject-signature-typed-control/out.md.checker/patch.diff` rc 0, Wednesday late-morning seat).

**Held 11:57 2026-10-07 by Wednesday late-morning seat after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1435-transfer-reject-signature-typed/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `69f2045af2a4f5f0b83b2f76c62514512abdc7b5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/transfer/src/index.ts , Blockchain/Dev/services/transfer/src/__tests__/transfer.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/transfer/src/index.ts` (product) and `Blockchain/Dev/services/transfer/src/__tests__/transfer.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	0	Blockchain/Dev/services/transfer/src/index.ts
47	0	Blockchain/Dev/services/transfer/src/__tests__/transfer.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/transfer/src/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/transfer/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/transfer/src/__tests__/transfer.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/transfer.test.ts fails at the untouched tip (2 failed / 55 run; controls green; assertion reds)` [red_first.json: failed=2 of total=55; red cell(s): ['Transfer Service — HTTP API POST /api/transfers/:id/reject RED KS-1435 TR1: an object signature is refused with 400 and the transfer stays pending', 'Transfer Service — HTTP API POST /api/transfers/:id/reject RED KS-1435 TR2: a numeric signature is refused with 400']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/transfer.test.ts passes with the product hunk (55 passed / 55 run)` [green_after.json: failed=0 of total=55, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=76 failed=0 | after: total=79 failed=0` · `NEW reds: []` [baseline_suite.json total=76 failed=0; after_suite.json total=79 failed=0]
- A6 [verbatim]: `PASS A6 whole services/transfer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/transfer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +48/-0 test=src/__tests__/transfer.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/transfer/src/index.ts` (+1/-0 per numstat.out) and the test file `Blockchain/Dev/services/transfer/src/__tests__/transfer.test.ts` (+47/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `69f2045af2a4f5f0b83b2f76c62514512abdc7b5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1435-transfer-reject-signature-typed/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-07_KS-1435-transfer-reject-signature-typed/checker.out`.

```diff
--- a/Blockchain/Dev/services/transfer/src/index.ts
+++ b/Blockchain/Dev/services/transfer/src/index.ts
@@ -411,2 +411,3 @@
   reason: z.string().min(1),
+  signature: z.string().optional(),
 });
--- a/Blockchain/Dev/services/transfer/src/__tests__/transfer.test.ts
+++ b/Blockchain/Dev/services/transfer/src/__tests__/transfer.test.ts
@@ -977,2 +977,49 @@
     });
+
+    // KS-1435: the published TransferRejectRequest declares `signature` as a string, but
+    // rejectTransferSchema did not, so zod dropped a wrong-typed one and the reject ran (200).
+    it('RED KS-1435 TR1: an object signature is refused with 400 and the transfer stays pending', async () => {
+      const createRes = await httpReq('POST', '/api/transfers', validTransferBody());
+      const id = createRes.data.data.id;
+
+      const res = await httpReq('POST', `/api/transfers/${id}/reject`, {
+        rejectorId: uuid(),
+        rejectorRole: 'new_owner',
+        reason: 'Wrong-typed signature',
+        signature: {},
+      });
+
+      expect(res.status).toBe(400);
+      const after = await httpReq('GET', `/api/transfers/${id}`);
+      expect(after.data.data.status).toBe('pending_approval');
+    });
+
+    it('RED KS-1435 TR2: a numeric signature is refused with 400', async () => {
+      const createRes = await httpReq('POST', '/api/transfers', validTransferBody());
+      const id = createRes.data.data.id;
+
+      const res = await httpReq('POST', `/api/transfers/${id}/reject`, {
+        rejectorId: uuid(),
+        rejectorRole: 'new_owner',
+        reason: 'Numeric signature',
+        signature: 42,
+      });
+
+      expect(res.status).toBe(400);
+    });
+
+    it('control KS-1435 TRC1: a string signature is accepted and the reject runs', async () => {
+      const createRes = await httpReq('POST', '/api/transfers', validTransferBody());
+      const id = createRes.data.data.id;
+
+      const res = await httpReq('POST', `/api/transfers/${id}/reject`, {
+        rejectorId: uuid(),
+        rejectorRole: 'new_owner',
+        reason: 'Signed rejection',
+        signature: '0xabc123',
+      });
+
+      expect(res.status).toBe(200);
+      expect(res.data.data.status).toBe('rejected');
+    });
   });
```
