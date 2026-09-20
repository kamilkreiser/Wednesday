# KS-1275 ORDERTHROUGHSPEC-1 PIN THAT THE REGISTERED LifecycleEventRequest AND LifecycleEventResponse SCHEMAS PUBLISH action IN THE DECLARED ORDER OF LIFECYCLE_EVENT_ACTIONS — the order the spec is generated from, read from the registry itself, not from the constant — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 02:18 on 2026-09-21, #1102-#1104 batch gate NOT-PINNED row ORDERTHROUGHSPEC)

File: `Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts`
Tip: `cbae988dbe90ebe556459ada2cb437eaf80e2402`
Runner: `jest`

Written from develop `cbae988dbe90ebe556459ada2cb437eaf80e2402` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 02:18 on 2026-09-21, read verbs only; the #1105 squash-merge, which carries #1102 = KS-1275 ORDER-1 already merged). The test file at that tip is **143 lines** (blob `22485a7ab3c5`), read whole; its full content is in `files[...]` of your input. The product the cell drives is `Blockchain/Dev/services/originate/src/originate.openapi.ts` (blob `2d1b48a0c7ea`, **3872 lines**): `LifecycleEventRequestSchema = sharedRegistry.register('LifecycleEventRequest', z.object({ action: z.enum(LIFECYCLE_EVENT_ACTIONS).openapi({ ... }), ... }))` at `:1736-1757` with the enum line at **`:1740`**, and `LifecycleEventResponseSchema = sharedRegistry.register('LifecycleEventResponse', z.object({ ..., action: z.enum(LIFECYCLE_EVENT_ACTIONS), ... }))` at `:1759-` with the enum line at **`:1765`**. The constant is `Blockchain/Dev/services/originate/src/lifecycleActions.ts:38-63` (sixteen verbs, `as const`). This service runs **JEST** (`package.json` `"test": "jest"`, `jest ^29.7.0`, `ts-jest ^29.4.11`, `jest.config.js` preset ts-jest; no vitest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `originate.openapi.ts`, `lifecycleActions.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

`LIFECYCLE_EVENT_ACTIONS` is consumed in three published places: the two `z.enum(LIFECYCLE_EVENT_ACTIONS)` registrations in `originate.openapi.ts` (`:1740` request, `:1765` response), whose array order is what `check:openapi` generates into `docs/openapi/secuura-api.yaml` (`LifecycleEventRequest.properties.action.enum`), and the 400 body's `Accepted: ${LIFECYCLE_EVENT_ACTIONS.join(', ')}` in `routes/documents.ts:2416`. #1102's ORDER-1 cell (`lifecycleEventRepo.test.ts`, merged) pins the CONSTANT's order; the #1102-#1104 gate then measured that **no cell reads the REGISTERED schema's enum order or the committed yaml** — a hand-edit of the registration to a different literal (or a reversed/re-sorted copy of the constant) would publish a different order while ORDER-1 stays green (the gate's row: "the PUBLISHED enum order ... pinned only through the constant"). This file already imports `sharedRegistry` (`:24`) and `'../originate.openapi'` for its registration side effect (`:30`) and reads `(sharedRegistry as unknown as { definitions: AnyDef[] }).definitions` (`:36`) — it is the ONE test in the service that reads the registry, so the cell lives here. This change adds ONE cell at the END of the file's single `describe` that finds the two `type === 'schema'` definitions whose `_def.openapi._internal.refId` is `LifecycleEventRequest` / `LifecycleEventResponse` (each registered exactly once — measured, 115 definitions after import), reads `schema.shape.action.options` (zod's enum values, in registration order) and asserts BOTH equal `[...LIFECYCLE_EVENT_ACTIONS]` — the constant pulled in with a dynamic `await import('../lifecycleActions')` inside the cell so the hunk stays ONE hunk (no import line added at the top). Every existing cell is unchanged. **It pins TODAY's registered order, read from the registry the spec is generated from.**

## The exact change — ONE hunk in the test file

The new cell goes at the END of the `describe('KS-978 — the published contract describes the organizationUuid bind', ...)` block opened at `:58`, directly above that block's closing line `});` (`:143`, the ONE trailing context line — the only column-0 `});` in the file, it occurs exactly once). There is NO leading context: the line above (`:142`, `  });`, the CONTROL cell's close) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts`.**

```
@@ -143,1 +143,7 @@
+  it('RED KS-1275 ORDERTHROUGHSPEC: the REGISTERED LifecycleEventRequest and LifecycleEventResponse schemas publish action in the declared order of LIFECYCLE_EVENT_ACTIONS', async () => {
+    const { LIFECYCLE_EVENT_ACTIONS } = await import('../lifecycleActions');
+    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
+    const published = (refId: string) => defs.filter((d) => d.type === 'schema' && d.schema?._def?.openapi?._internal?.refId === refId).map((d) => d.schema.shape.action.options);
+    expect([published('LifecycleEventRequest'), published('LifecycleEventResponse')]).toEqual([[[...LIFECYCLE_EVENT_ACTIONS]], [[...LIFECYCLE_EVENT_ACTIONS]]]);
+  });
 });
```

`describe`, `it` and `expect` are jest globals (the file uses them bare at `:58`, `:63`, `:64`); `sharedRegistry` is imported at `:24` and `AnyDef` is the file's own type alias at `:32` — you add NO top-level import and NO helper; `LIFECYCLE_EVENT_ACTIONS` comes from the dynamic `import('../lifecycleActions')` on the cell's second line (a pure module: one `as const` array, no imports). The cell needs no mock, no app boot, no port and no database: the registry was filled by the file's own `import '../originate.openapi'` at `:30` (that module imports only `@secuura/shared`, `./lifecycleActions` and `./utils/erasureMarker` — no route module, no db), exactly as `:36` already reads it.

## Cells

- `registeredorder` = `RED KS-1275 ORDERTHROUGHSPEC: the REGISTERED LifecycleEventRequest and LifecycleEventResponse schemas publish action in the declared order of LIFECYCLE_EVENT_ACTIONS`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1275 ORDERTHROUGHSPEC: the REGISTERED LifecycleEventRequest and LifecycleEventResponse schemas publish action in the declared order of LIFECYCLE_EVENT_ACTIONS

## Tampers

Two single-line tampers on `originate.openapi.ts`, one per registration (each line occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1 and 1; positive control `grep -c -i 'LIFECYCLE_EVENT_ACTIONS'` over the same file: 3 lines, the import at `:35` plus these two). Each is the loosening the gate named: the registration no longer publishes the declared order while the constant itself is unchanged, so ORDER-1 (which reads the constant) stays green. `From` is the tip's line at that number, byte for byte, and `To` is valid TypeScript under ts-jest's default diagnostics (`[...LIFECYCLE_EVENT_ACTIONS].reverse() as unknown as typeof LIFECYCLE_EVENT_ACTIONS` — a `string[]` cast back to the readonly tuple type `z.enum` requires; measured: no load error, no type error, the run reports 19 cells with one assertion red). The checker plants each and restores the file by bytes. **Frame, stated plainly:** in THIS test file no existing cell reads the lifecycle registrations (the ten cells read the `POST /api/documents` route's request body and 403 description), and in the whole originate suite no other cell reads them either (measured: 807 of 808 green under each tamper, the one red being this cell; the existing 807 all green).

### REQREGREVERSED — the REQUEST registration publishes a reversed copy of the constant
File: `Blockchain/Dev/services/originate/src/originate.openapi.ts`
Line: 1740
From:
```
      action: z.enum(LIFECYCLE_EVENT_ACTIONS).openapi({
```
To:
```
      action: z.enum([...LIFECYCLE_EVENT_ACTIONS].reverse() as unknown as typeof LIFECYCLE_EVENT_ACTIONS).openapi({
```
Reds: `registeredorder`

### RESREGREVERSED — the RESPONSE registration publishes a reversed copy of the constant
File: `Blockchain/Dev/services/originate/src/originate.openapi.ts`
Line: 1765
From:
```
    action: z.enum(LIFECYCLE_EVENT_ACTIONS),
```
To:
```
    action: z.enum([...LIFECYCLE_EVENT_ACTIONS].reverse() as unknown as typeof LIFECYCLE_EVENT_ACTIONS),
```
Reds: `registeredorder`

## Controls

- `the POST /api/documents route is registered at all`
- `CONTROL: userUuid still says it is NOT an authorization input`

*(Both are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:63` and `:138`, unchanged line numbers after this hunk since the insertion is below both — each occurs exactly once in the file and neither is a prefix of any other title. For a JEST suite the checker matches a declared cell by its FULL title, never by a prefix. The other 8 existing cells (10 at the tip minus the two controls) are also green under both tampers but are left undeclared. The `:63` control proves the registry is populated at all (the file's own discriminator, `:59-62`); the `:138` control is the file's own CONTROL cell, reading a request-body description through the same `definitions` array the new cell reads.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: `import '../originate.openapi'` (`:30`) registered 115 definitions (measured); exactly one `type === 'schema'` definition carries `refId === 'LifecycleEventRequest'` and exactly one `'LifecycleEventResponse'` (`OpenAPIRegistry.register` in `@asteasolutions/zod-to-openapi` 7.3.4 pushes `{ type: 'schema', schema: zodSchema.openapi(refId) }` — the refId lands at `_def.openapi._internal.refId`); `schema.shape.action` is the `ZodEnum` built from `LIFECYCLE_EVENT_ACTIONS` and its `.options` is the sixteen verbs in registration order (measured: `rights-unassign, share-revoke, ..., certified, verified` for both); `[...LIFECYCLE_EVENT_ACTIONS]` is the same sixteen in declaration order. The asserted array is `[[[...sixteen]], [[...sixteen]]]`.

Under **REQREGREVERSED** the request registration's `.options` is the sixteen REVERSED: the first slot reads `[['verified', 'certified', ..., 'rights-unassign']]` — assertion red (`expect(received).toEqual(expected) // deep equality`, `- Expected - 15 / + Received + 15`, measured). Under **RESREGREVERSED** the same on the second slot. Under both, every existing cell of this file stays green (none reads a lifecycle registration), and `lifecycleEventRepo.test.ts`'s ORDER-1 cell stays green (it reads the constant, which is unchanged) — that is exactly the gap this cell closes.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From lines.** `originate.openapi.ts` at `cbae988db`, line 1740 is `      action: z.enum(LIFECYCLE_EVENT_ACTIONS).openapi({` (6-space indent) and line 1765 is `    action: z.enum(LIFECYCLE_EVENT_ACTIONS),` (4-space indent), byte for byte; each occurs **exactly once** in the file (`grep -c -F -x`, 1 and 1). The checker plants and restores each (T8 by sha256 after; tip blob `2d1b48a0c7ea`, sha256 `3056d0a26e5eb515...` measured after every restore).
- **Premise: the gate's claim, re-derived.** The #1102-#1104 gate's row ORDERTHROUGHSPEC says no cell reads the registered schema's enum order or the committed yaml. Re-read at the tip: `git grep` of the originate tests for `originate.openapi` / `sharedRegistry` finds only this file (`:24`, `:30`) — and its ten cells read the `POST /api/documents` route only; `lifecycleEventRepo.test.ts` (8 cells incl. ORDER-1) imports the CONSTANT, never the registration. The gate's proposed cell targeted `lifecycleEventRepo.test.ts` with its own registry import; this brief moves it to the file that ALREADY imports the registry and the registration module, so the change is ONE hunk with no import line, and pins BOTH registrations (`:1740` and `:1765`) in one assertion. The gate's worry that importing `../originate.openapi` "imports the route modules" is refuted by reading `:35-40` of that file: its imports are `@secuura/shared`, `./lifecycleActions` and `./utils/erasureMarker` only.
- **Premise: the anchor.** The test file is **143** lines; `:143` is `});` (column 0, occurs exactly once in the file — every cell closes with the 2-space `  });`) and `:142` is `  });`. The trailing context line is non-blank and unique, and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: `+` lines that also occur at the tip.** One, added by this brief (so T4 accepts it): `  });` (`:65` and others — unavoidable for a new cell). Every other `+` line is new to the file (`:36`'s `const defs = ...` is 2-space indented; the new line is 4-space, a different byte string). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). The title uses `:`, `_` and plain words, no em dash.
- **Premise: the dynamic import.** `await import('../lifecycleActions')` inside an `async` cell under ts-jest (`module: commonjs`) compiles to a deferred `require` — measured here as a probe cell at the tip: green, and the destructured constant is the sixteen verbs. `lifecycleActions.ts` has no imports and no side effects.
- **Premise: the runner.** `Runner: jest` is in `services/originate/package.json` (`"test": "jest"`, devDependency `jest ^29.7.0`, `ts-jest`); no `vitest` anywhere in that package.json, so detection is unambiguous and the pin only confirms it. The checker runs `npx jest src/__tests__/ks978-published-contract-organizationuuid.test.ts` from `Blockchain/Dev/services/originate`.
- **Premise: the surface.** The cell reads an in-memory registry filled at import and one `as const` array. No user store, no session, no JWT, no chain, no db, no port, no product bytes. ORIGINATE published-contract surface, test-only pin (allowed).

## Collision

**No other brief of this round touches this test file or `originate.openapi.ts`** — the three held anchoring READYs (`KS-1284-CHUNKED-DOCUMENTID-ROUNDTRIP-1`, `KS-1175-EXPLORERBASE-PER-NETWORK-1`, `KS-1175-IDENTITY-EMPTY-OBJECT-1`) and the three new-file anchoring briefs of this wave are in `services/anchoring`; no hunk overlap possible, no shared tamper file. Of the existing `night/READY_*`, `READY_KS-1275-ORDER-1` (merged in #1102, its hunk is in the tip at `lifecycleEventRepo.test.ts:82-85`) is the sibling pin this cell complements — it plants tampers on `lifecycleActions.ts:39` and `:60` (the constant), never on `originate.openapi.ts`; `READY_KS-1133-A` and `READY_KS-794` (09-15) each carry a PRODUCT hunk on `originate.openapi.ts` — KS-1133-A two description strings after `:1926` / `:1983` (old pre-`Blockchain/Dev` paths), KS-794 a `fileSize` field after `:458` / `:646` — both far from `:1740` / `:1765` and neither is in the tip (`grep -c` of their `+` text at `cbae988db`: 0 and 0), so if they ship before this cell the two tamper line NUMBERS shift while the From lines stay unique — Wednesday re-counts `:1740` / `:1765` before queueing beside them; `READY_KS-1133-B` is a new test file, no product hunk. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clone at `cbae988db`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_wave3-drafter-precheck/ORDERTHROUGHSPEC/`)

- Whole originate suite at the untouched tip: **807 cells, 807 passed** (`full_suite_tip.out`; the gate's count after #1102 is the same 807/807). With the golden hunk applied: **808 cells, 808 passed** (`full_suite_applied.out`). The applied file alone: 11/11 (`file_tip_applied.out`).
- The proposed cell as a probe file at the tip: **GREEN** (`probe_tip.out`; console: both `.options` arrays are the sixteen verbs in declared order, `n: 115` definitions).
- Tampers planted by bytes (`tamper_probe.log`, probe + `ks978` + `lifecycleEventRepo` = 19 cells): REQREGREVERSED → 18 passed, **1 red = the new cell** (`expect(received).toEqual(expected)`), planted sha256 `b092b49304f4`; RESREGREVERSED → the same, planted sha256 `eb792dee994c`. File restored (`git diff --quiet` rc 0, sha256 back to `3056d0a26e5eb515`) after each. Re-measured with the golden hunk applied in place (`tamper_applied.log`): the same 18/1. Whole suite under each tamper with the hunk applied (`tamper_whole.log`): **808 cells, 807 passed, 1 failed = this cell** both times — 0 existing cells red.
- (the golden checker run is appended below after the run)

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts`, then the hunk above exactly as shown (`@@ -143,1 +143,7 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (originate published-contract read-back, test-only pin — allowed). Refs KS-1275** (and KS-978 for the file it sits in). **NEVER Closes** — KS-1275's own fix (`originate.openapi.ts:1847-1861` hand-enumerating the KS-387/389/415 verbs) is NOT this cell and is not measured here.
- **From the #1102-#1104 gate's NOT-PINNED table** (report `2026-09-20-batch1102-1104-tier1-r1/report.md`, row ORDERTHROUGHSPEC; the gate's tamper `z.enum([...LIFECYCLE_EVENT_ACTIONS].reverse() as unknown as typeof LIFECYCLE_EVENT_ACTIONS)` on `:1740` is planted and measured here, plus its `:1765` twin). The gate's proposed cell was re-homed from `lifecycleEventRepo.test.ts` (which would need a registry import and the side-effect import) to this file (which has both), and widened to both registrations.
- **Not pinned here, said plainly:** the committed yaml's enum order (`docs/openapi/secuura-api.yaml:6908-6923`) — `check:openapi` (CI) regenerates and diffs the yaml against these registrations, so a stale yaml is that gate's catch, not a jest cell's; the 400 body's `Accepted:` join (`routes/documents.ts:2416`) — a route cell needing the documents router's mocks, out of this file's scope.
- **Collision: none** (see Collision).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1275 night/inputs/test_only_1275ORDERTHROUGHSPEC-1.json night/briefs/KS-1275-ORDERTHROUGHSPEC-1.md ctx=65536
```

## MEASURED — appended after the golden run (02:22, artefacts `runs/2026-09-21_wave3-drafter-precheck/ORDERTHROUGHSPEC/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md`, fresh `--shared` clone at `cbae988db`, `drafter2_clone_3`): **RESULT: PASS (8/8)** — T3 strict apply; T4 6/6 `+` lines byte-exact; T5 green at the tip 11/11 cells (10 + the new one); T6 REQREGREVERSED and RESREGREVERSED each red set == {registeredorder}, an assertion failure; T7 both controls green under both; T8 `originate.openapi.ts` restored to sha256 `3056d0a26e5e` (150298 bytes) after each. Source tracked-modified count 0 before and after.
- Whole originate suite: 807/807 at the tip → 808/808 with the cell (measured above, `full_suite_applied.out`).
- Input rebuilt from the corrected Collision paragraph before the checker ran (`build.log`: RUNNER PINNED jest by the brief's Runner: line, detected jest only).
