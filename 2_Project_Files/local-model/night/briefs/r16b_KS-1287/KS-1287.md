# KS-1287 R16B-PATHREQUIRED - Wednesday's task for Ornith: the published OpenAPI path parameter `index` of `GET /api/status/{id}/check/{index}` renders `required: false` (the only optional path parameter in the spec; Schemathesis 4.27.5 Schema Error) because `z.coerce.number()` parses `null` as `0` and zod-to-openapi v7 reads that as nullable - pin `required: true` through the `.openapi({ param: { required: true } })` metadata at `vc-issuer.openapi.ts:1496` (ONE product hunk: one `-` line, two `+` lines) and pin it with ONE NEW vitest file that generates the document in-process (code_patch, VITEST, written 15:41:35 AEST on 2026-09-22 by Wednesday's feed14 drafter from `vc-issuer.openapi.ts` read at develop 3bad652d1: 1628 lines)
Tip: `3bad652d17cf111c1e2e1bed1ae7686894637487`
Runner: `vitest`

## Premises (measured by the feed14 drafter in a scratchpad clone of origin detached at the tip; Wednesday re-derives before queueing)
- Ticket KS-1287 (Backlog, P3, assignee kamil.kreiser, no PR attached; board read at boot): `docs/openapi/secuura-api.yaml` publishes the `in: path` parameter `index` of `GET /api/status/{id}/check/{index}` (`operationId: getStatusByIdCheckByIndex`) with `required: false`; OpenAPI 3 requires `required: true` on every path parameter; Schemathesis 4.27.5 reports it as a run-level Schema Error (KS-1285's after-sweep). The ticket names the mechanism as "not verified" - it IS verified here.
- The mechanism, REPRODUCED in-process at the tip (`runs/2026-09-22_feed14-drafter-precheck/repro_1287_tip.log`): importing `vc-issuer.openapi.ts` and calling `generateOpenApiDocument(...)` exactly as `scripts/generate-openapi.ts` does prints `{"name":"index","in":"path","required":false,"schema":{"type":"integer","minimum":0}}` for the operation, `id` beside it `required: true`. zod-to-openapi 7.3.4 computes a parameter's `required` as `!isOptional() && !isNullable()` (`dist/index.mjs:1019`), and zod's `isNullable()` is `safeParse(null).success` - `z.coerce.number()` coerces `null` to `0`, which is a nonnegative integer, so `isNullable()` is `true` for the coerce chain (`false` for the plain `z.number().int().nonnegative()` control) and the flag renders `false`. The same mechanism produced KS-423's `[integer, "null"]` type rendering, which the `.openapi({ type: 'integer' })` pin on this line already overrides for the TYPE - it does not override `required`.
- The fix, TRIALLED at the tip (`repro_1287_fix.log`): the lib spreads the `param` metadata over the computed `{ schema, required }` (`Object.assign({ schema, required }, buildParameterMetadata(param))`) and `.openapi()` MERGES nested `param` objects, so `param: { required: true }` on the schema survives the registry's own `.openapi({ param: { name, in } })` wrap; with the one-line change the same generation prints `required: true` for `index` and the schema stays `{ type: 'integer', minimum: 0 }`. `param:` metadata is used nowhere else in the service openapi files (git grep 0 hits; control `openapi({` 31 hits in this file) - this is its first use, and it is the lib's documented override.
- `vc-issuer.openapi.ts` at the tip: last touched by `a9b63bbd7` (2026-09-02); the site is `:1496` with offset 0. The lines: `:1492` `  request: {`; `:1493` `    params: z.object({`; `:1494` `      id: z.string(),`; `:1495` the KS-423 comment (it carries a double-quote character - it is CONTEXT, copy it byte for byte); `:1496` the `index` line; `:1497` `    }),`; `:1498` `  },`; `:1499` `  responses: {`. No blank line is asked of you as context.
- The test is a NEW vitest file that imports `../vc-issuer.openapi` (the registration side-effect) and `generateOpenApiDocument` from `@secuura/shared`, generates the document in-process and reads the operation's `parameters` - the shape `packages/shared/src/__tests__/openapi-operation-ids.test.ts` uses (it generates the document from the registry and walks `doc.paths`). No database, no server, no mock. Two RED cells by assertion at the tip (`indexParam.required` is `false`; the walk over every vc-issuer operation lists exactly `get /api/status/{id}/check/{index} index` as an optional path parameter), two CONTROL cells green on both trees (the operation is registered with its two path params `['id', 'index']` and operationId `getStatusByIdCheckByIndex`; `id` is `required: true` and `index` keeps `type: 'integer'`, `minimum: 0`). Measured at the tip in the clone: `2 failed | 2 passed (4)` (`vitest_1287_tip.log`).
- Every `+` line (product and test) is ASCII-only, backslash-free, `$`-free and carries NO double-quote character (asserted by the writer script); strings are single-quoted.
- Collision check: `vc-issuer` is in NEITHER round-19 lane (Seat B 19th = originate/kyc/security/packages/shared/systemTest/performance; Seat C 19th = repo-root CLAUDE.md/.githooks/docs/scripts/Start_Up/systemTest/schemathesis - `exclusion_set.log`: 47 paths, none under `services/vc-issuer/`); no held READY of 2026-09-2[0-2] names `vc-issuer.openapi.ts`; not one of the tickets Kam's counter sent to Claude; not an auth/MFA/OAuth PRODUCT edit (an OpenAPI metadata pin on a status-list route). The committed `docs/openapi/secuura-api.yaml` is NOT in this task (Seat C 19th's `docs/` directory; the CI drift gate `check:openapi` will ask for a regeneration at raise time - the raiser runs `npm run generate-openapi` then).

## What is wrong (one paragraph)
`Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts:1496` declares the `index` path parameter of `GET /api/status/{id}/check/{index}` as `z.coerce.number().int().nonnegative().openapi({ type: 'integer', minimum: 0 })`. zod-to-openapi decides a parameter's `required` flag from the schema alone: `!isOptional() && !isNullable()`. The coerce wrapper turns `null` into `0`, which the chain accepts, so the schema reports itself nullable and the generator publishes `required: false` - illegal for an `in: path` parameter and the only such parameter in the spec. The fix pins the flag through the parameter metadata the lib provides for exactly this: `param: { required: true }` inside the existing `.openapi({...})` call, plus a one-line comment naming why (the KS-423 comment above it explains the TYPE pin; this explains the REQUIRED pin). Nothing else changes: the runtime coercion stays (the handler still receives a number), the type pin stays, `id` stays. NOT in this task: the committed yaml, the handler in `routes/status.ts`, the other `z.coerce` sites in this file (they are query/body params where an optional flag is legal), the KS-423 comment at `:1495` (context - copy it as it is).

## The exact change - ONE EDIT in the product file (one hunk; copy the header)
E1 (hunk 1, header `@@ -1493,7 +1493,8 @@`) - the one `-` line is the tip's `:1496`; the two `+` lines are the KS-1287 comment and the same `index:` line with `, param: { required: true }` added inside the `.openapi({...})` object. Leading context `:1493-:1495` (`    params: z.object({`, `      id: z.string(),`, the KS-423 comment - all three STAY), trailing context `:1497-:1499` (`    }),`, `  },`, `  responses: {` - all STAY). Old side 7 lines, new side 8.
```
@@ -1493,7 +1493,8 @@
     params: z.object({
       id: z.string(),
       // KS-423: pin the emitted type (coerce+nonnegative renders [integer, "null"]).
-      index: z.coerce.number().int().nonnegative().openapi({ type: 'integer', minimum: 0 }),
+      // KS-1287: coerce parses null as 0, so the lib reads the param as nullable and publishes required: false - pin it.
+      index: z.coerce.number().int().nonnegative().openapi({ type: 'integer', minimum: 0, param: { required: true } }),
     }),
   },
   responses: {
```
There are exactly 2 `+` lines in the product hunk; the `-` line is the tip's `:1496` exactly; every context line keeps its leading space (`    params: z.object({` has four spaces at the tip, so its context line has five). The `:1495` context line carries `"null"` with double quotes - that is a CONTEXT line copied from the tip, and the no-double-quote rule is on `+` lines only. Do NOT touch `:1493-:1495` or `:1497-:1499` beyond copying them as context.

## THIS IS VITEST
`repo.test_runner` begins with `vitest`. `describe/it/expect` are imported from `'vitest'`; NO `jest.*`, no `vi.mock` needed (the suite generates the document from the registry; it opens no database and no port).

## The test - one NEW vitest file that generates the OpenAPI document in-process (the openapi-operation-ids shape)
File: `Blockchain/Dev/services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 55), every line with a leading `+` (a blank line is a lone `+`). Copy every line byte for byte - single quotes only, no double-quote character, no backslash, ASCII only, no `$` anywhere.
```
+/**
+ * KS-1287: GET /api/status/{id}/check/{index} published its path parameter index as required: false - the only
+ * optional path parameter in the spec (OpenAPI 3 requires required: true on every in: path parameter; Schemathesis
+ * 4.27.5 reports it as a Schema Error). Mechanism, measured in-process: zod-to-openapi v7 computes required as
+ * not-isOptional and not-isNullable, and z.coerce.number() parses null as 0, so the coerce wrapper reads as
+ * nullable. The one-site fix pins required: true through the param metadata. This suite generates the document
+ * in-process from vc-issuer.openapi.ts the way scripts/generate-openapi.ts does.
+ */
+import { describe, it, expect } from 'vitest';
+import '../vc-issuer.openapi';
+import { generateOpenApiDocument } from '@secuura/shared';
+
+type Param = { name: string; in: string; required?: boolean; schema?: { type?: string; minimum?: number } };
+type Operation = { operationId?: string; parameters?: Param[] };
+
+const doc = generateOpenApiDocument({ title: 'ks1287', version: '0.0.0' }) as unknown as {
+  paths: Record<string, Record<string, Operation>>;
+};
+const op = doc.paths['/api/status/{id}/check/{index}'].get;
+const params = op.parameters ?? [];
+const indexParam = params.find((p) => p.name === 'index');
+const idParam = params.find((p) => p.name === 'id');
+
+function optionalPathParams(): string[] {
+  const out: string[] = [];
+  for (const [routePath, item] of Object.entries(doc.paths)) {
+    for (const [method, operation] of Object.entries(item)) {
+      for (const p of operation.parameters ?? []) {
+        if (p.in === 'path' && p.required !== true) out.push(method + ' ' + routePath + ' ' + p.name);
+      }
+    }
+  }
+  return out;
+}
+
+describe('KS-1287: the index path parameter of GET /api/status/{id}/check/{index} is published required', () => {
+  it('RED KS-1287 A: the index path parameter renders required: true', () => {
+    expect(indexParam?.required).toBe(true);
+  });
+
+  it('RED KS-1287 B: no vc-issuer operation publishes an optional in: path parameter', () => {
+    expect(optionalPathParams()).toEqual([]);
+  });
+
+  it('control: the operation and its two path parameters are registered', () => {
+    expect(op.operationId).toBe('getStatusByIdCheckByIndex');
+    expect(params.filter((p) => p.in === 'path').map((p) => p.name)).toEqual(['id', 'index']);
+  });
+
+  it('control: the id sibling renders required: true and index keeps its pinned integer schema', () => {
+    expect(idParam?.required).toBe(true);
+    expect(indexParam?.schema?.type).toBe('integer');
+    expect(indexParam?.schema?.minimum).toBe(0);
+  });
+});
```
LINE DISCIPLINE: the INPUT JSON shows this brief's line breaks as the two characters backslash and n inside a JSON string - DECODE them. Every one of the 55 `+` lines above is its OWN physical line of your diff, each starting with its own `+`; NEVER join two lines with a backslash-n pair (a `+` line that carries a backslash is a FAIL). Cells (the two RED cells by assertion at the tip, the two controls green on both trees; nothing optional):
- RED `it('RED KS-1287 A: the index path parameter renders required: true')` - `indexParam?.required` must be `true`. At the tip it is `false` - the red, by assertion; after E1 it is `true`.
- RED `it('RED KS-1287 B: no vc-issuer operation publishes an optional in: path parameter')` - `optionalPathParams()` walks every path and method of the generated document and lists each `in: path` parameter whose `required` is not `true`; must be `[]`. At the tip it is `['get /api/status/{id}/check/{index} index']` - the red; after E1 `[]`.
- CONTROL `it('control: the operation and its two path parameters are registered')` - `op.operationId` is `'getStatusByIdCheckByIndex'` and the path params are `['id', 'index']` - green on both trees (proves the import registered the operation; an empty registry would not pass).
- CONTROL `it('control: the id sibling renders required: true and index keeps its pinned integer schema')` - `idParam?.required` `true`, `indexParam?.schema?.type` `'integer'`, `indexParam?.schema?.minimum` `0` - green on both trees (proves E1 changes only the flag, not the KS-423 type pin).

## Red cells
- RED KS-1287 A: the index path parameter renders required: true
- RED KS-1287 B: no vc-issuer operation publishes an optional in: path parameter

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:1496` - **must change**: `      index: z.coerce.number().int().nonnegative().openapi({ type: 'integer', minimum: 0 }),` - E1 (the one `-` line; re-emitted as a `+` with `, param: { required: true }` added inside the `.openapi({...})` object, under a new KS-1287 comment line)
* `:1494` - (correct) `      id: z.string(),` - stays (E1's second leading context line; `id` already renders `required: true`)
* `:1497` - (correct) `    }),` - stays (E1's first trailing context line)
* `:1499` - (correct) `  responses: {` - stays (E1's last trailing context line)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts` / `+++ b/Blockchain/Dev/services/vc-issuer/src/vc-issuer.openapi.ts` with the ONE E1 hunk (header `@@ -1493,7 +1493,8 @@`, one `-` line, two `+` lines), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1287-status-check-index-path-param-is-required.test.ts` (one `@@ -0,0 +1,55 @@` hunk, all `+`); paths repo-rooted (`Blockchain/Dev/...`, never `services/...`); no double quote, no backslash, no non-ASCII character in any `+` line; every `+` line's `(` / `)`, `[` / `]` and `{` / `}` counts are EXACTLY the fence's - one extra `)` on a `+` line is a FAIL; every context line keeps its leading space; EVERY diff line on its own physical line - never a backslash-n pair joining lines (decode the INPUT JSON's escapes); the cell titles EXACTLY as listed.
