# READY — KS-591-MINTUPLOADFEE-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-nft-mint-upload-fee/out.md.checker/patch.diff`** (from `ls` at 02:58 2026-10-08; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-nft-mint-upload-fee/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-nft-mint-upload-fee/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 02:58 2026-10-08 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-nft-mint-upload-fee/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3ce8cd4026a6e3241413e9c7533d5a84d10c1c79`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts , Blockchain/Dev/services/nft-certificate/src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts` (product) and `Blockchain/Dev/services/nft-certificate/src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	1	Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts
61	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-591: POST /api/nft/mint, POST /api/nft/ipfs/upload and PUT /api/nft/admin/platform-fee publish a REQUIRED request body RED KS-591 NM1: POST /api/nft/mint marks its request body required', 'KS-591: POST /api/nft/mint, POST /api/nft/ipfs/upload and PUT /api/nft/admin/platform-fee publish a REQUIRED request body RED KS-591 NM2: POST /api/nft/ipfs/upload marks its request body required', 'KS-591: POST /api/nft/mint, POST /api/nft/ipfs/upload and PUT /api/nft/admin/platform-fee publish a REQUIRED request body RED KS-591 NM3: PUT /api/nft/admin/platform-fee marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=48 failed=0 | after: total=54 failed=0` · `NEW reds: []` [baseline_suite.json total=48 failed=0; after_suite.json total=54 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +64/-1 test=src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts` (+3/-1 per numstat.out) and the test file `Blockchain/Dev/services/nft-certificate/src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts` (+61/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3ce8cd4026a6e3241413e9c7533d5a84d10c1c79` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-nft-mint-upload-fee/input.json`. Brief (given by --brief; its `# ` heading names KS-591): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-591-nft-mint-upload-fee/KS-591.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-nft-mint-upload-fee/checker.out`.

```diff
--- a/Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts
+++ b/Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts
@@ -848,7 +848,7 @@
   summary: 'Mint an NFT-backed certificate',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: NftMintRequestSchema } } },
+    body: { content: { 'application/json': { schema: NftMintRequestSchema } }, required: true },
   },
   responses: {
     201: {
@@ -1119,6 +1119,7 @@
   request: {
     body: {
       content: { 'application/json': { schema: NftIpfsUploadRequestSchema } },
+      required: true,
     },
   },
   responses: {
@@ -1285,6 +1286,7 @@
   request: {
     body: {
       content: { 'application/json': { schema: NftPlatformFeeUpdateRequestSchema } },
+      required: true,
     },
   },
   responses: {
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks591-nft-mint-upload-fee-body-required.test.ts
@@ -0,0 +1,61 @@
+// KS-591 (positive_data_acceptance register): the published contracts for POST /api/nft/mint,
+// POST /api/nft/ipfs/upload and PUT /api/nft/admin/platform-fee did not mark the request body required, so a
+// spec-driven caller (Schemathesis) sent no body at all and each handler (routes/nft.routes.ts, a zod object with
+// required keys via safeParse) answered 400. Those zod objects reject an absent body, so the spec now says the body
+// is required - the KS-1364 shape. This file renders the document the generator publishes, from the shared
+// registry the nft-certificate module populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../nft-certificate.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'nft-certificate (ks591 mint/upload/fee pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string, method: string): string | undefined {
+  return operation(path, method)?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-591: POST /api/nft/mint, POST /api/nft/ipfs/upload and PUT /api/nft/admin/platform-fee publish a REQUIRED request body', () => {
+  it('RED KS-591 NM1: POST /api/nft/mint marks its request body required', () => {
+    expect(operation('/api/nft/mint', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-591 NM2: POST /api/nft/ipfs/upload marks its request body required', () => {
+    expect(operation('/api/nft/ipfs/upload', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-591 NM3: PUT /api/nft/admin/platform-fee marks its request body required', () => {
+    expect(operation('/api/nft/admin/platform-fee', 'put')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-591 NMC1: the three bodies keep their request schemas and all three operations keep bearerAuth', () => {
+    expect({
+      mint: bodyRef('/api/nft/mint', 'post'),
+      upload: bodyRef('/api/nft/ipfs/upload', 'post'),
+      fee: bodyRef('/api/nft/admin/platform-fee', 'put'),
+    }).toEqual({
+      mint: '#/components/schemas/NftMintRequest',
+      upload: '#/components/schemas/NftIpfsUploadRequest',
+      fee: '#/components/schemas/NftPlatformFeeUpdateRequest',
+    });
+    expect(operation('/api/nft/mint', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/nft/ipfs/upload', 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    expect(operation('/api/nft/admin/platform-fee', 'put')?.security).toEqual([{ bearerAuth: [] }]);
+  });
+
+  it('control KS-591 NMC2: the request components still list required fields, which is why an absent body is refused', () => {
+    const s: AnyObj = doc.components?.schemas ?? {};
+    expect(s.NftMintRequest?.required).toEqual(expect.arrayContaining(['certificationId', 'walletAddress', 'chain']));
+    expect(s.NftIpfsUploadRequest?.required).toEqual(expect.arrayContaining(['data', 'filename', 'originalMimeType']));
+    expect(s.NftPlatformFeeUpdateRequest?.required).toEqual(expect.arrayContaining(['percentage', 'fixed']));
+  });
+
+  it('control KS-591 NMC3: the KS-1364 sibling POST /api/nft/record keeps its required body', () => {
+    expect(operation('/api/nft/record', 'post')?.requestBody?.required).toBe(true);
+  });
+});
```

**Appended by Wednesday 02:58 2026-10-08 (not written by hold_ready):** this pass was REVIEWED on 2026-10-05 (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-591-nft-mint-upload-fee/REVIEW.md`, verdict "HOLD (ready to raise)") but no READY file was written then, so no raise seat saw it until the 2026-10-08 03:00 delta screen found it (`0_Brain/reference/2026-10-08_spark-screen/SCREEN_0300.md`). The raise also needs the YAML companion `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-591-nft-mint-upload-fee/openapi-yaml.companion.diff`. The screen measured both nft passes + both companions applying strict at develop eae08a3f441c, alone and stacked, and the pair together marks 10 of 10 nft request bodies required. The raise carries `Refs KS-1449` (the spec half of KS-1449; its runtime half needs a live sweep after).
