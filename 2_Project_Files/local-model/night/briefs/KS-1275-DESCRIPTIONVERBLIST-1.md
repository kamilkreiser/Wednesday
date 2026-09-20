# KS-1275 DESCRIPTIONVERBLIST-1 PIN THE VERB LIST IN THE REGISTERED LifecycleEventRequest ACTION DESCRIPTION — the verbs it names as "must use their own routes" are exactly share, transfer-custody and revoke, each has a registered POST /api/documents/{id}/<verb> route, and none is a verb LIFECYCLE_EVENT_ACTIONS accepts — Wednesday's task for Ornith, TEST_ONLY, **ONE existing JEST test file, one hunk, one cell added, no product file** (written 2026-09-21 after the #1112-#1118 batch gate; its NOT-PINNED row DESCRIPTIONVERBLIST, KS-1275, measured 0 red of 808 at the #1115 head)

File: `Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts`
Tip: `7be81d5c9b109959b559e03652fb092c12de58e8`
Runner: `jest`

Written from develop `7be81d5c9b109959b559e03652fb092c12de58e8` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` on 2026-09-21, read verbs only; the tree that carries the seven #1112-#1118 squashes, #1115 = KS-1275 ORDERTHROUGHSPEC-1 included). The test file at that tip is **149 lines** (blob `27366baf3251`), read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/originate/src/originate.openapi.ts` (blob `2d1b48a0c7ea`, **3872 lines**): the `LifecycleEventRequestSchema` registration `:1736-:1758` — `action: z.enum(LIFECYCLE_EVENT_ACTIONS).openapi({` at `:1740`, `        description:` at `:1741`, and the description as TWO concatenated string lines, `:1742` `          'Lifecycle verb to record. Only verbs WITHOUT a dedicated endpoint are ' +` and **`:1743`** `          'accepted — share/transfer-custody/revoke etc. must use their own routes.',` (whole-line ×1 in the file; NOTE the em dash `—` is IN THE PRODUCT LINE and stays there — your `+` lines never contain it). The three verbs it names each have a registered route in the same file: `path: '/api/documents/{id}/revoke'` (`:1399`), `'/api/documents/{id}/share'` (`:1553`), `'/api/documents/{id}/transfer-custody'` (`:1675`), all `method: 'post'`. `LIFECYCLE_EVENT_ACTIONS` (`src/lifecycleActions.ts`) lists the verbs the generic endpoint ACCEPTS (`rename`, `delete`, `restore`, the share-* edits, `protect`, `note`, …) and by the module's own header excludes share / transfer-custody / revoke / certify / sign / upload. This service runs **JEST** (`package.json` `"test": "jest"`, `jest.config.js`, jest 29.7.0 with ts-jest; no vitest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `originate.openapi.ts`, `lifecycleActions.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

#1115 (KS-1275 ORDERTHROUGHSPEC-1) added the cell at `:143-:148` of this file: the REGISTERED `LifecycleEventRequest` and `LifecycleEventResponse` schemas publish `action` in the declared order of `LIFECYCLE_EVENT_ACTIONS` — the enum ORDER through the registry. The #1112-#1118 gate then planted `/rename` into the description's verb list (`share/transfer-custody/revoke` → `share/transfer-custody/revoke/rename`) and measured **0 red of 808**: the ticket's LITERAL symptom — a description that names a verb wrongly — is unpinned; a stale verb that the endpoint in fact ACCEPTS (rename is in `LIFECYCLE_EVENT_ACTIONS`) could be written into the published contract and nothing would notice. This change adds ONE cell, directly under the ORDERTHROUGHSPEC cell, that reads the REGISTERED artefact (not the source text): it finds the `LifecycleEventRequest` schema in `sharedRegistry.definitions` by `refId` exactly as `:146` does, reads `shape.action._def.openapi.metadata.description` (the same metadata path the file's own `requestBodyPropDescription` helper reads at `:51`; measured: that is where zod-to-openapi keeps `.openapi({ description })`), takes the slash-separated word before ` etc.` (`share/transfer-custody/revoke`, measured) and asserts THREE things in one `toEqual`: the verbs are exactly `['share', 'transfer-custody', 'revoke']`; every one of them has a registered `post` route at `'/api/documents/{id}/' + verb` (so a verb the contract sends integrators to "its own route" for really has one); and none of them is in `LIFECYCLE_EVENT_ACTIONS` (so the contract never tells integrators a verb the endpoint accepts must go elsewhere). **It pins TODAY's list**: if a dedicated route is ever added or removed and the description is updated on purpose, the cell goes red on purpose and its expected list is rewritten with that decision.

## The exact change — ONE hunk in the test file

The cell goes at the END of the file's single `describe('KS-978 — …')` block (`:58-:149`): after `:148` (`  });`, the close of the ORDERTHROUGHSPEC cell) and before `:149` (`});`, the close of the describe and the last line of the file). `  });` occurs many times, so the hunk carries THREE leading context lines — `:146` (`    const published = (refId: string) => …`, **unique in the file**), `:147` (`    expect([published('LifecycleEventRequest'), …`, unique) and `:148` (`  });`) — and ONE trailing context line (`:149`, `});`). Copy every line byte for byte. Every `+` line is ASCII only (the title uses `-`, never an em dash; the product's em dash is NOT in any `+` line — the cell splits on `' etc.'` and on `' '` instead). There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts`.**

```
@@ -146,4 +146,13 @@
     const published = (refId: string) => defs.filter((d) => d.type === 'schema' && d.schema?._def?.openapi?._internal?.refId === refId).map((d) => d.schema.shape.action.options);
     expect([published('LifecycleEventRequest'), published('LifecycleEventResponse')]).toEqual([[[...LIFECYCLE_EVENT_ACTIONS]], [[...LIFECYCLE_EVENT_ACTIONS]]]);
   });
+  it('RED KS-1275 DESCRIPTIONVERBLIST: the registered LifecycleEventRequest action description names exactly share, transfer-custody and revoke as the verbs with their own routes - each has a registered POST /api/documents/{id}/<verb> route and none is accepted by LIFECYCLE_EVENT_ACTIONS', async () => {
+    const { LIFECYCLE_EVENT_ACTIONS } = await import('../lifecycleActions');
+    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;
+    const request = defs.find((d) => d.type === 'schema' && d.schema?._def?.openapi?._internal?.refId === 'LifecycleEventRequest');
+    const description = String(request?.schema?.shape?.action?._def?.openapi?.metadata?.description ?? '');
+    const verbs = (description.split(' etc.')[0].split(' ').pop() ?? '').split('/');
+    const dedicated = (verb: string) => defs.some((d) => d.type === 'route' && d.route?.method === 'post' && d.route?.path === '/api/documents/{id}/' + verb);
+    expect([verbs, verbs.filter((verb) => !dedicated(verb)), verbs.filter((verb) => (LIFECYCLE_EVENT_ACTIONS as readonly string[]).includes(verb))]).toEqual([['share', 'transfer-custody', 'revoke'], [], []]);
+  });
 });
```

`sharedRegistry` is imported at `:24`, the side-effect import of `../originate.openapi` at `:30` registers everything, `AnyDef` is declared at `:32`; `describe`/`it`/`expect` are jest globals in this file (no import, as the file itself has none) — you add NO import and NO file-scope declaration. The cell's mocking shape is the file's own: none (a registry read after the side-effect import), and its `await import('../lifecycleActions')` copies `:144`. The `as readonly string[]` cast is what lets `.includes(verb)` type-check against the `as const` tuple under ts-jest; `'/api/documents/{id}/' + verb` is string concatenation (no template literal). No server, no port, no database, no network.

## Cells

- `verblist` = `RED KS-1275 DESCRIPTIONVERBLIST: the registered LifecycleEventRequest action description names exactly share, transfer-custody and revoke as the verbs with their own routes - each has a registered POST /api/documents/{id}/<verb> route and none is accepted by LIFECYCLE_EVENT_ACTIONS`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper declared for it and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1275 DESCRIPTIONVERBLIST: the registered LifecycleEventRequest action description names exactly share, transfer-custody and revoke as the verbs with their own routes - each has a registered POST /api/documents/{id}/<verb> route and none is accepted by LIFECYCLE_EVENT_ACTIONS

## Tampers

Two single-line tampers on `originate.openapi.ts`, both on `:1743` (the same From, planted one at a time and restored by bytes between them). The first is the gate's own row byte for byte (`/rename` inserted — a verb the endpoint ACCEPTS written into the "must use their own routes" list). The second replaces a real dedicated-route verb with one that has NO `/api/documents/{id}/<verb>` route (`revoke` → `certify`; `certify` is not a registered route — the certify flow's routes are `sign-cert` / `sign-wallet` — and not in `LIFECYCLE_EVENT_ACTIONS` either, so this tamper reds ONLY through the exact-list and the has-a-route checks, not through the accepted-verb check). The `From` occurs EXACTLY ONCE in the file as a whole line (python whole-line scan: hits `[1743]`; positive control `        description:` 19 hits). Each `To` is valid TypeScript (a string literal changed; measured: the whole suite runs under each). The checker plants each and restores the file by bytes.

### VERBLISTSTALE — an ACCEPTED verb (rename) is written into the dedicated-route list
File: `Blockchain/Dev/services/originate/src/originate.openapi.ts`
Line: 1743
From:
```
          'accepted — share/transfer-custody/revoke etc. must use their own routes.',
```
To:
```
          'accepted — share/transfer-custody/revoke/rename etc. must use their own routes.',
```
Reds: `verblist`

### VERBWITHOUTROUTE — a dedicated-route verb is replaced by one with no route (revoke -> certify)
File: `Blockchain/Dev/services/originate/src/originate.openapi.ts`
Line: 1743
From:
```
          'accepted — share/transfer-custody/revoke etc. must use their own routes.',
```
To:
```
          'accepted — share/transfer-custody/certify etc. must use their own routes.',
```
Reds: `verblist`

## Controls

- `RED KS-1275 ORDERTHROUGHSPEC: the REGISTERED LifecycleEventRequest and LifecycleEventResponse schemas publish action in the declared order of LIFECYCLE_EVENT_ACTIONS`
- `the POST /api/documents route is registered at all`
- `CONTROL: userUuid still says it is NOT an authorization input`

*(All three are FULL `it(...)` titles copied from the file at the tip — `:143`, `:63`, `:138` — unchanged by this hunk (the insertion is below all of them). For a JEST suite the checker matches a declared cell by its FULL title, never by a prefix; no title is a prefix of another. Under both tampers the ORDERTHROUGHSPEC control stays green — the enum's options are untouched by a description edit — and proves the registry is live and the same schema is being read; the other two prove the route registry and the neighbouring description reads still work. The file's other cells are also green under each tamper but are left undeclared.)*

## THE CELL — state it to yourself before you write a line

At the untouched tip the cell passes: the description string ends `… are accepted — share/transfer-custody/revoke etc. must use their own routes.`; `split(' etc.')[0]` keeps everything before ` etc.`, `.split(' ').pop()` takes its last word `share/transfer-custody/revoke`, `.split('/')` gives the three verbs; each has a registered `post /api/documents/{id}/<verb>` route (measured: the registry lists `post /api/documents/{id}/revoke`, `…/share`, `…/transfer-custody`); none is in `LIFECYCLE_EVENT_ACTIONS` → `[['share', 'transfer-custody', 'revoke'], [], []]` (measured). Under **VERBLISTSTALE** the verbs are four: the list differs, `rename` has no route (`[ 'rename' ]`) and `rename` IS accepted (`[ 'rename' ]`) — an assertion red on all three components (measured: `Expected - 2 / Received + 7`). Under **VERBWITHOUTROUTE** the verbs are `share, transfer-custody, certify`: the list differs and `certify` has no route (`[ 'certify' ]`); the accepted-verb component stays `[]` — an assertion red (measured: `Expected - 2 / Received + 4`). Every other cell stays green under each (measured: whole suite).

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From line.** `originate.openapi.ts` at `7be81d5c9`, line 1743 is `          'accepted — share/transfer-custody/revoke etc. must use their own routes.',` (10-space indent, one em dash), byte for byte; it occurs **once** as a whole line. The checker plants and restores it (T8 by sha256 after). The builder and checker carry the em dash as UTF-8 (`ensure_ascii=False`; planted by `encode('utf-8')`).
- **Premise: the gate's claim, re-derived.** No cell in originate's `__tests__` reads the `action` description: `git grep -n 'must use their own routes' <tip> -- services/originate/src/__tests__` = 0 hits (positive control: `LIFECYCLE_EVENT_ACTIONS` is in this file at `:144`, `:147`). The ORDERTHROUGHSPEC cell reads `.options` only. Agreed: unpinned.
- **Premise: the anchor.** The test file is **149** lines; `:146`-`:149` are non-blank, `:146` and `:147` are unique, `:149` is the describe's `});` and the last line. The hunk is a pure insertion with three leading and one trailing context line — no blank line is asked of you anywhere.
- **Premise: `+` lines that also occur at the tip.** Three, unavoidable and added by this brief (so T4 accepts them): `  });`, `    const { LIFECYCLE_EVENT_ACTIONS } = await import('../lifecycleActions');` and `    const defs = (sharedRegistry as unknown as { definitions: AnyDef[] }).definitions;` (the ORDERTHROUGHSPEC cell has the same two lines). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). The title uses `-`, `:`, `/`, `{`, `}`, `<`, `>`.
- **Premise: the runner.** `services/originate/package.json` at the tip has `"test": "jest"` and `jest` + `ts-jest` in devDependencies, `jest.config.js` beside it, no vitest — the builder detects jest and the `Runner:` line agrees.
- **Premise: the surface.** A registry read after the file's own side-effect import; no server, no port, no database, no network. Originate OpenAPI CONTRACT surface (documentation text), test-only pin — no product edit.

## Collision

`/usr/bin/grep -il '+++ b/.*ks978-published-contract-organizationuuid.test.ts' night/READY_*.md` = **1** of 253 READYs (KS-1275-ORDERTHROUGHSPEC-1) — and EVERY `+` line of it is already in the file at `7be81d5c9` (python: 6/6 present): merged as #1115, not banked. Positive control: the ks1234 file's `+++ b/` is in 4 READYs. `originate.openapi.ts` is named in 5 READYs: ORDERTHROUGHSPEC-1 and ORDER-1 (KS-1275, tampers on other lines) and **KS-1133-A / KS-1133-B / KS-794 — un-raised READYs that carry PRODUCT hunks elsewhere in this file** (the gate noted them too); none touches `:1740-:1743`: their `originate.openapi.ts` hunks start at old lines **1926 and 1983** (KS-1133-A — AFTER 1743, no shift) and **458 and 646** (KS-794 — BEFORE 1743: if it lands first, line 1743 moves down by its added lines and this brief's `Line: 1743` must be re-anchored; the From line stays unique, so the fix is the number only); KS-1133-B touches only a NEW test file. (The fenced diffs of KS-1133-A and KS-794 as extracted from their READY files are `corrupt patch` to `git apply --check` — a fence artefact of those READYs, not measured further here; KS-1133-B's applies at the tip and with this brief's VERBLISTSTALE planted, rc 0 both — `collision_originate2.log`.) No other brief of this round touches originate. Sequencing needed: none for the cells.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clone at `7be81d5c9`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_gate1112rows-drafter-precheck/DESCRIPTIONVERBLIST/`)

- **Tip:** `ls-remote` at 08:51 and 09:09 = `7be81d5c9b109959b559e03652fb092c12de58e8`; measurement clone `m_orig` HEAD = the tip; `prepare_clone.sh` rc 0 (28 shared dist entries; `prepare.measure.log`).
- **Where the description lives (probe, parked as `zzprobe-ks1275-desc.test.ts.txt`):** the registered `LifecycleEventRequest` schema is found once by `refId`; `shape.action._def.openapi` has the single key `metadata`, and `metadata.description` = `Lifecycle verb to record. Only verbs WITHOUT a dedicated endpoint are accepted — share/transfer-custody/revoke etc. must use their own routes.`; `action.description` and `_def.description` are undefined. The registry's routes include `post /api/documents/{id}/revoke`, `post /api/documents/{id}/share`, `post /api/documents/{id}/transfer-custody` (and no `…/certify`, no `…/rename`).
- **From line:** `          'accepted — share/transfer-custody/revoke etc. must use their own routes.',` whole-line hits `[1743]`; positive control `        description:` 19 hits.
- **File at the bare tip (jest 29.7.0):** **11 passed / 0 failed of 11** (`file_tip_bare.json`). Hunk `git apply` rc 0; **file with hunk: 12 / 0 of 12** (`file_tip_applied.json`).
- **Whole originate suite:** bare tip **808 / 0 of 808 in 67 files** (`whole_bare_tip.json`); with the hunk **809 / 0 of 809** (`whole_applied.json`).
- **Under VERBLISTSTALE:** file **11 / 1 of 12** — the ONE red is `verblist`: `expect(received).toEqual(expected) // deep equality — Expected - 2 / Received + 7`: verbs `["share","transfer-custody","revoke","rename"]`, no-route `["rename"]`, accepted `["rename"]`. Whole suite **808 / 1 of 809** — the same cell only. Restored by checkout: `originate.openapi.ts` sha256 `3056d0a26e5eb515` == tip blob, porcelain 0.
- **Under VERBWITHOUTROUTE:** file **11 / 1 of 12** — `verblist`: `Expected - 2 / Received + 4`: verbs `["share","transfer-custody","certify"]`, no-route `["certify"]`, accepted `[]`. Whole suite **808 / 1 of 809**. Restored: sha `3056d0a26e5eb515`, porcelain 0.
- **Controls under both tampers:** all three green (in the 11/12 each time).
- **Golden and variants:** see the drafter report (`runs/2026-09-21_gate1112rows-drafter-precheck/REPORT.md`, Row 3) — `golden_runs.log`.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts`, then the hunk above exactly as shown (`@@ -146,4 +146,13 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2 at the gate (originate contract text; no auth surface). Refs KS-1275.** **NEVER Closes** — KS-1275 is merged (#1115 pinned the order); this cell pins the description's verb list, the ticket's literal symptom.
- **From the #1112-#1118 batch gate's NOT-PINNED table** (report `2026-09-21_seatB-12th/gate/report.md:172`, row DESCRIPTIONVERBLIST). The gate's proposed cell asserted only "no named verb is accepted"; this brief adds the exact list and "every named verb has a route", and a second tamper (VERBWITHOUTROUTE) that only the added checks catch — stated here so the widening is visible.
- **Said plainly:** the exact-list component means a deliberate change to the description's examples (a new dedicated route, say `certify`) must also update this cell's expected list — one line, and the red says which.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1275 night/inputs/test_only_1275DESCRIPTIONVERBLIST-1.json night/briefs/KS-1275-DESCRIPTIONVERBLIST-1.md tip=7be81d5c9b109959b559e03652fb092c12de58e8 ctx=65536
```
