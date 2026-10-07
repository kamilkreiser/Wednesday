# READY — KS-1364-IPFSPINUNPIN-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-nft-ipfs-pin-unpin-size/out.md.checker/patch.diff`** (from `ls` at 02:58 2026-10-08; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-nft-ipfs-pin-unpin-size/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-nft-ipfs-pin-unpin-size/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 02:58 2026-10-08 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-nft-ipfs-pin-unpin-size/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `46c3e20cfbd21acee0c67d544180c33deaa4c8ef`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts , Blockchain/Dev/services/nft-certificate/src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts` (product) and `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	2	Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts
62	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1364: three nft POSTs publish a REQUIRED request body RED KS-1364 NP1: POST /api/nft/ipfs/pin marks its request body required', 'KS-1364: three nft POSTs publish a REQUIRED request body RED KS-1364 NP2: POST /api/nft/ipfs/unpin marks its request body required', 'KS-1364: three nft POSTs publish a REQUIRED request body RED KS-1364 NP3: POST /api/nft/metadata/estimate-size marks its request body required']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=48 failed=0 | after: total=54 failed=0` · `NEW reds: []` [baseline_suite.json total=48 failed=0; after_suite.json total=54 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +65/-2 test=src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts` (+3/-2 per numstat.out) and the test file `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts` (+62/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `46c3e20cfbd21acee0c67d544180c33deaa4c8ef` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-nft-ipfs-pin-unpin-size/input.json`. Brief (given by --brief; its `# ` heading names KS-1364): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-nft-ipfs-pin-unpin-size/KS-1364.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-nft-ipfs-pin-unpin-size/checker.out`.

```diff
--- a/Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts
+++ b/Blockchain/Dev/services/nft-certificate/src/nft-certificate.openapi.ts
@@ -1144,7 +1144,7 @@
   summary: 'Pin a CID to ensure persistence',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: NftIpfsPinRequestSchema } } },
+    body: { content: { 'application/json': { schema: NftIpfsPinRequestSchema } }, required: true },
   },
   responses: {
     200: {
@@ -1169,7 +1169,7 @@
   summary: 'Unpin a CID',
   security: [{ bearerAuth: [] }],
   request: {
-    body: { content: { 'application/json': { schema: NftIpfsPinRequestSchema } } },
+    body: { content: { 'application/json': { schema: NftIpfsPinRequestSchema } }, required: true },
   },
   responses: {
     200: {
@@ -1259,6 +1259,7 @@
   request: {
     body: {
       content: { 'application/json': { schema: NftMetadataSizeRequestSchema } },
+      required: true,
     },
   },
   responses: {
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1364-nft-ipfs-pin-unpin-estimate-size-body-required.test.ts
@@ -0,0 +1,62 @@
+// KS-1364 (85 request bodies not marked required): the published contracts for POST /api/nft/ipfs/pin,
+// POST /api/nft/ipfs/unpin and POST /api/nft/metadata/estimate-size did not mark the request body required, so a
+// spec-driven caller (Schemathesis) may send no body at all. Each handler (routes/nft.routes.ts) safeParses the body
+// with a zod object that has required fields (cid; storageTier and privacyLevel) and answers 400 on failure, so an
+// absent body (express.json() leaves it as {}) is always refused. The spec now says each body is required - the
+// shapes the KS-1364 nft carves landed in this file. This file renders the document the generator publishes, from
+// the shared registry the nft-certificate module populates on import. No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../nft-certificate.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'nft-certificate (ks1364 ipfs pin)', version: '0.0.0' }) as AnyObj;
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function bodyRef(path: string): string | undefined {
+  return operation(path, 'post')?.requestBody?.content?.['application/json']?.schema?.$ref;
+}
+
+describe('KS-1364: three nft POSTs publish a REQUIRED request body', () => {
+  it('RED KS-1364 NP1: POST /api/nft/ipfs/pin marks its request body required', () => {
+    expect(operation('/api/nft/ipfs/pin', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 NP2: POST /api/nft/ipfs/unpin marks its request body required', () => {
+    expect(operation('/api/nft/ipfs/unpin', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('RED KS-1364 NP3: POST /api/nft/metadata/estimate-size marks its request body required', () => {
+    expect(operation('/api/nft/metadata/estimate-size', 'post')?.requestBody?.required).toBe(true);
+  });
+
+  it('control KS-1364 NPC1: the three bodies keep their request schemas and their bearerAuth', () => {
+    expect({
+      pin: bodyRef('/api/nft/ipfs/pin'),
+      unpin: bodyRef('/api/nft/ipfs/unpin'),
+      size: bodyRef('/api/nft/metadata/estimate-size'),
+    }).toEqual({
+      pin: '#/components/schemas/NftIpfsPinRequest',
+      unpin: '#/components/schemas/NftIpfsPinRequest',
+      size: '#/components/schemas/NftMetadataSizeRequest',
+    });
+    for (const p of ['/api/nft/ipfs/pin', '/api/nft/ipfs/unpin', '/api/nft/metadata/estimate-size']) {
+      expect(operation(p, 'post')?.security).toEqual([{ bearerAuth: [] }]);
+    }
+  });
+
+  it('control KS-1364 NPC2: the request components still list their required fields', () => {
+    const s: AnyObj = doc.components?.schemas ?? {};
+    expect(s.NftIpfsPinRequest?.required).toEqual(['cid']);
+    expect(s.NftMetadataSizeRequest?.required).toEqual(expect.arrayContaining(['storageTier', 'privacyLevel']));
+  });
+
+  it('control KS-1364 NPC3: the landed KS-1364 nft carves keep their required bodies', () => {
+    expect(operation('/api/nft/record', 'post')?.requestBody?.required).toBe(true);
+    expect(operation('/api/nft/verify/transaction', 'post')?.requestBody?.required).toBe(true);
+  });
+});
```

**Appended by Wednesday 02:58 2026-10-08 (not written by hold_ready):** this pass was REVIEWED on 2026-10-05 (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-05_KS-1364-nft-ipfs-pin-unpin-size/REVIEW.md`, verdict "HOLD (ready to raise)") but no READY file was written then, so no raise seat saw it until the 2026-10-08 03:00 delta screen found it (`0_Brain/reference/2026-10-08_spark-screen/SCREEN_0300.md`). The raise also needs the YAML companion `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1364-nft-ipfs-pin-unpin-size/openapi-yaml.companion.diff`. The screen measured both nft passes + both companions applying strict at develop eae08a3f441c, alone and stacked, and the pair together marks 10 of 10 nft request bodies required. The raise carries `Refs KS-1449` (the spec half of KS-1449; its runtime half needs a live sweep after).
