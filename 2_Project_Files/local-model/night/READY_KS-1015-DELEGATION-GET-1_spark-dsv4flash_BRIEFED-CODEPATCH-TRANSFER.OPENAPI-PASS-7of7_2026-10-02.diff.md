# READY — KS-1015-DELEGATION-GET-1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-02_KS-1015-delegation-get/out.md.checker/patch.diff`** (from `ls` at 06:17 2026-10-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-02_KS-1015-delegation-get/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-02_KS-1015-delegation-get/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-02_KS-1015-delegation-get/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1015-delegation-get/precheck/out.md.checker/patch.diff` rc 0, Spark brief-writer sub-agent for Wednesday, session 73252fd5).

**Held 06:17 2026-10-02 by Spark brief-writer sub-agent for Wednesday, session 73252fd5 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-02_KS-1015-delegation-get/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `88e8877a2a0d6a626b9c2a7c4b71d3a909e6f94e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/transfer/src/transfer.openapi.ts , Blockchain/Dev/services/transfer/src/__tests__/ks1015-delegation-get-spec-declares-envelope.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/transfer/src/transfer.openapi.ts` (product) and `Blockchain/Dev/services/transfer/src/__tests__/ks1015-delegation-get-spec-declares-envelope.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
23	1	Blockchain/Dev/services/transfer/src/transfer.openapi.ts
79	0	Blockchain/Dev/services/transfer/src/__tests__/ks1015-delegation-get-spec-declares-envelope.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (23 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 23 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/transfer/src/transfer.openapi.ts byte-exact incl. leading whitespace (apply mode strict): OK 23 line(s) byte-exact incl. leading whitespace (of 23; 23 line(s) added by the apply)` [a3i_indent.out: `OK 23 line(s) byte-exact incl. leading whitespace (of 23; 23 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/transfer/src/transfer.openapi.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/transfer/src/__tests__/ks1015-delegation-get-spec-declares-envelope.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1015-delegation-get-spec-declares-envelope.test.ts fails at the untouched tip (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1015: GET /api/delegations/{id} publishes the envelope its handler returns RED KS-1015 D1: the 200 body is the success/data envelope, not the bare Delegation record', 'KS-1015: GET /api/delegations/{id} publishes the envelope its handler returns RED KS-1015 D2: data carries the Delegation component and the chain, both required', 'KS-1015: GET /api/delegations/{id} publishes the envelope its handler returns RED KS-1015 D3: the chain declares the fields buildDelegationChain returns, invalidReason optional']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1015-delegation-get-spec-declares-envelope.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=70 failed=0 | after: total=76 failed=0` · `NEW reds: []` [baseline_suite.json total=70 failed=0; after_suite.json total=76 failed=0]
- A6 [verbatim]: `PASS A6 whole services/transfer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/transfer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +102/-1 test=src/__tests__/ks1015-delegation-get-spec-declares-envelope.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/transfer/src/transfer.openapi.ts` (+23/-1 per numstat.out) and the test file `Blockchain/Dev/services/transfer/src/__tests__/ks1015-delegation-get-spec-declares-envelope.test.ts` (+79/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `88e8877a2a0d6a626b9c2a7c4b71d3a909e6f94e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-02_KS-1015-delegation-get/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-02_KS-1015-delegation-get/checker.out`.

```diff
--- a/Blockchain/Dev/services/transfer/src/transfer.openapi.ts
+++ b/Blockchain/Dev/services/transfer/src/transfer.openapi.ts
@@ -1193,7 +1193,29 @@
     400: commonErrorResponses[400],
     200: {
       description: 'Delegation',
-      content: { 'application/json': { schema: DelegationSchema } },
+      // KS-1015 (sweep 2026-09-29): the handler (routes/delegations.ts, GET /:id) answers a success/data
+      // envelope carrying the delegation and the chain buildDelegationChain() returns, not a bare Delegation,
+      // so the spec follows the runtime. The Delegation component is unchanged and is referenced inside data.
+      content: {
+        'application/json': {
+          schema: successEnvelope(
+            z
+              .object({
+                delegation: DelegationSchema,
+                chain: z
+                  .object({
+                    rootDelegatorId: z.string(),
+                    chain: z.array(z.record(z.string(), z.unknown())),
+                    totalDepth: z.number().int(),
+                    isValid: z.boolean(),
+                    invalidReason: z.string().optional(),
+                  })
+                  .passthrough(),
+              })
+              .passthrough(),
+          ),
+        },
+      },
     },
     401: commonErrorResponses[401],
     404: commonErrorResponses[404],
--- /dev/null
+++ b/Blockchain/Dev/services/transfer/src/__tests__/ks1015-delegation-get-spec-declares-envelope.test.ts
@@ -0,0 +1,79 @@
+// KS-1015 (sweep 2026-09-29): the published contract for GET /api/delegations/{id} declared a bare Delegation
+// record (id, delegatorId, delegateId, ...) as its 200 body, while the handler (routes/delegations.ts, GET /:id)
+// answers { success, data: { delegation, chain } }, the chain being what buildDelegationChain() returns.
+// Schemathesis flagged the 200 as response_schema_conformance. The spec now follows the runtime. This file renders
+// the document the generator publishes, from the shared registry the transfer module populates on import.
+// No server, no database, no network.
+import { describe, it, expect } from 'vitest';
+import { generateOpenApiDocument } from '@secuura/shared';
+import '../transfer.openapi';
+
+type AnyObj = Record<string, any>;
+
+const doc = generateOpenApiDocument({ title: 'transfer (ks1015 pin)', version: '0.0.0' }) as AnyObj;
+
+const ONE = '/api/delegations/{id}';
+
+function operation(path: string, method: string): AnyObj | undefined {
+  return doc.paths?.[path]?.[method];
+}
+
+function body(path: string, method: string, status: string): AnyObj | undefined {
+  return operation(path, method)?.responses?.[status]?.content?.['application/json']?.schema;
+}
+
+describe('KS-1015: GET /api/delegations/{id} publishes the envelope its handler returns', () => {
+  it('RED KS-1015 D1: the 200 body is the success/data envelope, not the bare Delegation record', () => {
+    const s = body(ONE, 'get', '200');
+    expect({ ref: s?.$ref, required: s?.required, success: s?.properties?.success }).toEqual({
+      ref: undefined,
+      required: ['success', 'data'],
+      success: { type: 'boolean', enum: [true] },
+    });
+  });
+
+  it('RED KS-1015 D2: data carries the Delegation component and the chain, both required', () => {
+    const d = body(ONE, 'get', '200')?.properties?.data;
+    expect({
+      required: [...(d?.required ?? [])].sort(),
+      delegation: d?.properties?.delegation?.$ref,
+      chain: d?.properties?.chain?.type,
+    }).toEqual({
+      required: ['chain', 'delegation'],
+      delegation: '#/components/schemas/Delegation',
+      chain: 'object',
+    });
+  });
+
+  it('RED KS-1015 D3: the chain declares the fields buildDelegationChain returns, invalidReason optional', () => {
+    const c = body(ONE, 'get', '200')?.properties?.data?.properties?.chain;
+    const types = Object.fromEntries(Object.entries(c?.properties ?? {}).map(([k, v]) => [k, (v as AnyObj).type]));
+    expect({ types, required: [...(c?.required ?? [])].sort() }).toEqual({
+      types: { rootDelegatorId: 'string', chain: 'array', totalDepth: 'integer', isValid: 'boolean', invalidReason: 'string' },
+      required: ['chain', 'isValid', 'rootDelegatorId', 'totalDepth'],
+    });
+  });
+
+  it('control KS-1015 C1: the GET operation keeps bearerAuth, its path parameter id, and its 404', () => {
+    const op = operation(ONE, 'get');
+    expect(op?.security).toEqual([{ bearerAuth: [] }]);
+    expect((op?.parameters ?? []).map((q: AnyObj) => q.in + ':' + q.name + ':' + q.required)).toEqual(['path:id:true']);
+    expect(Object.keys(op?.responses ?? {})).toEqual(expect.arrayContaining(['200', '404']));
+  });
+
+  it('control KS-1015 C2: the Delegation component stays published with its required fields', () => {
+    expect([...(doc.components?.schemas?.Delegation?.required ?? [])].sort()).toEqual(
+      ['createdAt', 'delegateId', 'delegationType', 'delegatorId', 'id', 'status', 'validFrom'],
+    );
+  });
+
+  it('control KS-1015 C3: the sibling list and per-document operations keep their own envelopes', () => {
+    expect({
+      list: body('/api/delegations', 'get', '200')?.$ref,
+      perDoc: body('/api/delegations/document/{documentId}', 'get', '200')?.$ref,
+    }).toEqual({
+      list: '#/components/schemas/DelegationListResponse',
+      perDoc: '#/components/schemas/DelegationDocumentListResponse',
+    });
+  });
+});
```

> (Added BY HAND 06:18 2026-10-02 by the Spark brief-writer sub-agent for Wednesday, session 73252fd5; hold_ready has no field for it.) **Raise-seat step the model does not do:** the PR also needs the regenerated `Blockchain/Dev/docs/openapi/secuura-api.yaml`. Apply `night/briefs/KS-1015-delegation-get/KS-1015.openapi-yaml.companion.diff` (+38/-1; `git apply --check` rc 0 at `88e8877a`), or run `npm run generate-openapi` and confirm, then `npm run check:openapi`. Measured at `88e8877a`: the model's files alone give `generate-openapi -- --check` rc 1; with the companion, `check:openapi` rc 0 (405 example blocks). Commit as `Refs KS-1015` (narrows one untriaged pair; does NOT close the ticket).
