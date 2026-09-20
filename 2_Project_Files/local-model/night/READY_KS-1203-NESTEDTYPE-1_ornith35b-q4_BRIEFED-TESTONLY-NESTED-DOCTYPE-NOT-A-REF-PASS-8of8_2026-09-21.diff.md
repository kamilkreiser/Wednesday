# READY — KS-1203-NESTEDTYPE-1 (Ornith, briefed, test_only, vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1203-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 00:44 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS.

**Held 00:44 2026-09-21 by the 23:4x Wednesday seat after a source read.** Tip `778e6cfe2b6061d60ffcf3a57a951c84dc152b67` (the #1102–#1104 tip). Adds ONE cell to `api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts` (the file #1103 merged) pinning the #1102–#1104 gate's NOT-PINNED row NESTEDTYPEHONOURED: a NESTED `data.documentType` is not a type reference — it admits with an EMPTY docType and never consults the catalogue (today's behaviour). Source: the gate's row, measured 0 of 675 at head / 0 of 678 on the batch tree.

**Source read (Wednesday, same action):** 4 `+` lines, all 4 byte-present in `night/briefs/KS-1203-NESTEDTYPE-1.md`; 0 `-`; one test file (T2); sibling WSTRIM-1 control 1/4 (a shared closing line). First sample, round 1.

**Tamper (T6 reds exactly the cell; T8 restored by bytes):** NESTEDTYPEHONOURED on `enforcement.ts:100` (scope anchor: first statement of `enforceDocumentTypeRules(` at :96; From `  const typeRefRaw = body.documentType || body.type || '';` — byte-checked by Wednesday at the tip, count 1) → the gate's To verbatim. Controls (full titles) green under it.

**Collision (measured by the drafter, both orders):** its sibling KS-1203-WSTRIM-1 edits the SAME file at a disjoint location (:64 vs :72); both orders yield one 80-line file (sha `fae6c65d54e7`); grading is order-independent; **for the raise, land NESTEDTYPE-1 first** (WSTRIM-1's hunk applies at "offset 4" after it) or rebase the second. Combined file 9/9 at the tip; whole api-gateway 680/680 with both (drafter's precheck at 778e6cfe2).

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); api-gateway vitest; `Refs KS-1203` (a characterisation pin; the ticket's fix is not this). One PR with WSTRIM-1 when it lands (same file), or this one alone. Partition: the ks501 file is owned by no live seat (Seat B 11th's six files exclude it; Seat A 15th is anchoring).

---
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts
@@ -72,1 +72,5 @@
+  it('RED KS-1203: a NESTED data.documentType is not a type reference - it admits with an EMPTY docType and never consults the catalogue', async () => {
+    const result = await enforceDocumentTypeRules({ data: { documentType: 'DEGREE' } }, undefined);
+    expect([result.ok, (result as { docType?: unknown }).docType, vi.mocked(redisService.getAllDocumentTypes).mock.calls.length]).toEqual([true, {}, 0]);
+  });
 });
