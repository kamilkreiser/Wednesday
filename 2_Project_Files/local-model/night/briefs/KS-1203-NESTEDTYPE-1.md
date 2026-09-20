# KS-1203 NESTEDTYPE-1 PIN THAT A NESTED data.documentType IS NOT A TYPE REFERENCE (the body admits UNTYPED, the catalogue is never read) — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 00:5x on 2026-09-21, from the #1102-#1104 gate's NOT-PINNED row NESTEDTYPEHONOURED)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts`
Tip: `778e6cfe2b6061d60ffcf3a57a951c84dc152b67`
Runner: `vitest`

Written from develop `778e6cfe2b6061d60ffcf3a57a951c84dc152b67` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 00:4x on 2026-09-21, read verbs only; the #1104 merge, the last of the #1102-#1104 batch). The test file at that tip is **72 lines**, read whole (blob `e05c6bd21f`, last changed by #1103 KS-1203 UNTYPED-1); its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts` (**279 lines**, read whole, last changed by #1014 — it did NOT move under #1102-#1104): `enforceDocumentTypeRules` at `:96-99`, its FIRST statement at `:100` (`  const typeRefRaw = body.documentType || body.type || '';`), the non-string guard at `:106-113`, the untyped admit at `:114-117`, the catalogue resolve at `:119`. This service runs **VITEST**.

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `enforcement.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

`enforceDocumentTypeRules` reads a type reference from exactly two top-level keys: `body.documentType` then `body.type` (`enforcement.ts:100`). A `documentType` nested inside `body.data` is NOT read: the body is untyped, the function admits it with an EMPTY `docType` at `:116`, and the catalogue (`redisService.getAllDocumentTypes`) is never consulted. The #1102-#1104 gate MEASURED this on the value table: the row `{ data: { documentType: 'DEGREE' } }` answers `[ok:true, docType:{}, 0 catalogue reads]` at the tip, and under the tamper below it moves to `[ok:true, docType:{id:'dt-1',code:'DEGREE',isActive:true}, 1 read]` while **0 of 675** api-gateway cells red — the #1103 UNTYPED-1 cell does not red it because its data-only shape carries `title`, not `documentType`. This change adds ONE cell to the KS-501 suite that calls the REAL `enforceDocumentTypeRules` IN PROCESS with the file's own mocked catalogue (seeded by its `beforeEach` with `DEGREE`) and asserts the triple `[ok, docType, catalogue reads]` is `[true, {}, 0]` for a nested `data.documentType: 'DEGREE'`. The catalogue-read count is the liveness element: the mocked catalogue DOES hold `DEGREE`, so a reader that honoured the nested key would resolve it (1 read, a populated docType). Every existing cell is unchanged. **It pins TODAY's behaviour and decides nothing about KS-1203** — the ticket's question (which keys name a document type) is Kam's; a fix that starts honouring `data.documentType` now arrives as a deliberate red in this suite instead of a silent change.

## The exact change — ONE hunk in the test file

The new cell goes at the end of the `describe('KS-501 non-string documentType', ...)` block opened at `:26`, directly above that block's closing line `});` (`:72`, the file's LAST line and the ONE trailing context line), i.e. directly after the #1103 UNTYPED-1 cell (`:64-71`). There is NO leading context: the line above (`:71`, `  });`) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts`.**

```
@@ -72,1 +72,5 @@
+  it('RED KS-1203: a NESTED data.documentType is not a type reference - it admits with an EMPTY docType and never consults the catalogue', async () => {
+    const result = await enforceDocumentTypeRules({ data: { documentType: 'DEGREE' } }, undefined);
+    expect([result.ok, (result as { docType?: unknown }).docType, vi.mocked(redisService.getAllDocumentTypes).mock.calls.length]).toEqual([true, {}, 0]);
+  });
 });
```

`enforceDocumentTypeRules` is already imported by the file at `:15` (`from '../services/enforcement'`), `vi` and `expect` at `:14`, and `redisService` at `:24` (`import * as redisService from '../services/redis'`, the module the file mocks at `:17-22`) — you add NO import and NO mock. The file's `beforeEach` (`:27-33`) already clears the mocks and seeds `getAllDocumentTypes` with `[{ id: 'dt-1', code: 'DEGREE', isActive: true }]`, so the cell needs no set-up of its own. `vi.mocked(...)` is the idiom the sibling suite `enforcement.test.ts` uses on the same mock (`:113`, `:156`). No app boot, no port, no database: the function is called directly.

## Cells

- `nestedtype` = `RED KS-1203: a NESTED data.documentType is not a type reference - it admits with an EMPTY docType and never consults the catalogue`

## Red cells

The cell below is a GENUINE assertion-red: it fails under the tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1203: a NESTED data.documentType is not a type reference - it admits with an EMPTY docType and never consults the catalogue

## Tampers

ONE single-line tamper on `enforcement.ts:100` (the FIRST statement of `enforceDocumentTypeRules`; the line occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1). It is the gate's NESTEDTYPEHONOURED row verbatim: the reader starts honouring a nested `data.documentType`. The `From` is the tip's line at that number, byte for byte, and the `To` is valid TypeScript (an optional chain on an `any` cast), so nothing fails to load and no cell reds for the wrong reason.

### NESTEDTYPEHONOURED — the reader also honours a nested data.documentType
File: `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts`
Line: 100
From:
```
  const typeRefRaw = body.documentType || body.type || '';
```
To:
```
  const typeRefRaw = body.documentType || body.type || (body.data as any)?.documentType || '';
```
Reds: `nestedtype`

## Controls

- `still passes through an absent/empty documentType`
- `RED KS-1203: a body carrying no resolvable documentType admits with an EMPTY docType and never consults the catalogue`

*(Both are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:53` and `:64` — each occurs exactly once in the file and neither is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix. The `:64` control (#1103's UNTYPED-1) is the liveness proof: it drives the SAME `enforceDocumentTypeRules` through the SAME mocked catalogue with seven untyped shapes — including `{ data: { title: 'no type here' } }`, the data-only shape WITHOUT a nested documentType — and stays green under the tamper (the gate measured 0 of 675). The file's other cells (`:35` it.each, `:47`, `:58`) are also green under the tamper but are left undeclared: the it.each title carries `%s` and the `:47` title carries backticks, neither a clean declared name.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: `body.documentType` and `body.type` are both `undefined` on `{ data: { documentType: 'DEGREE' } }`, so `:100` yields `''`; the non-string guard at `:106` is skipped (`''` is falsy); `typeRef` is `''` at `:114`; `:115-117` returns `{ ok: true, docType: {} }` before `resolveDocumentType` is ever called. `getAllDocumentTypes` was cleared by `beforeEach` and is called 0 times. The triple is `[true, {}, 0]`, exactly what the cell asserts.

Under **NESTEDTYPEHONOURED** `:100` yields `'DEGREE'` from the nested key; `:119` calls `resolveDocumentType('DEGREE')`, which reads the mocked catalogue ONCE and matches `code: 'DEGREE'`; the user is `undefined`, `creatorVerificationLevel` is absent, so `:147` returns `{ ok: true, docType: { id: 'dt-1', code: 'DEGREE', isActive: true } }`. The triple is `[true, { id: 'dt-1', code: 'DEGREE', isActive: true }, 1]` — assertion red on BOTH the docType and the read count. Every existing cell stays green: none of them carries a `data` key with a `documentType` inside (UNTYPED-1's data-only shape carries `title`), so `(body.data as any)?.documentType` is `undefined` for all of them and the `|| ''` fallback answers what `:100` answered before.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` line.** `enforcement.ts` at `778e6cfe2`, line 100 is `  const typeRefRaw = body.documentType || body.type || '';`, byte for byte; it occurs **exactly once** in the file (`grep -c -F -x`, 1). Re-derived at THIS tip by the scope anchor (the first statement after `export async function enforceDocumentTypeRules(` at `:96`), not by the gate's number — the file's last commit is #1014, before the batch, so the number happens to agree.
- **Premise: the gate's claim, re-derived.** `:100` reads only `body.documentType` and `body.type`; a nested `data.documentType` is invisible to it and the body admits at `:116` untyped. The gate measured the value-table delta under exactly this tamper (`[true, {}, 0]` -> `[true, {...DEGREE...}, 1]`) with 0 of 675 cells red.
- **Premise: the anchor.** The test file is **72** lines; `:72` is `});` (column 0, the file's last line, the ONLY column-0 `});` in the file, closing the `describe` opened at `:26`) and `:71` is `  });`. The trailing context line is non-blank and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: nothing pins this today.** `data: { documentType` occurs **0** times in `api-gateway/src/__tests__/` at the tip (`git grep`, with `vi.mocked` from the same tree as the positive control); the UNTYPED-1 cell's only `data` shape is `{ data: { title: 'no type here' } }`.
- **Premise: the in-process call.** The cell calls the exported function with a plain object and `undefined` user, exactly as `:40`, `:48`, `:54` and `:67` already do; the mocked `getAllDocumentTypes` returns the `beforeEach` catalogue on every call and `mock.calls.length` counts them.
- **Premise: no `+` line re-adds a tip line.** The only `+` line that also occurs at the tip is the closing `  });` (unavoidable for a new cell, and under the checker's 8-character floor).
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). The title uses `-`, not an em dash.
- **Premise: the runner.** `api-gateway/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9` in devDependencies (installed 4.1.10), with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this cell.
- **Premise: the live lane.** `enforcement.ts` IS a live-lane file (the KS-1203 ticket is In Progress, its fix is not this PR), but this brief writes ZERO product bytes; the tamper is planted and restored by bytes in the checker's clone only (T8).

## Collision

**Same test file as `KS-1203-WSTRIM-1` (both cells go in ONE file), at a DISJOINT location:** this brief inserts above `});` at `:72`; WSTRIM-1 inserts above the UNTYPED-1 cell at `:64`. Measured in the writing seat's clone (MEASURED below): with THIS diff applied first, WSTRIM-1's hunk applies strictly (its `:64` region is untouched); with WSTRIM-1 applied first, this hunk's `});` has moved from `:72` to `:76` and `git apply` lands it there by offset. **Queue order: NESTEDTYPE-1 then WSTRIM-1 is the both-strict order;** the reverse also applies (offset 4). Each brief is graded against the pinned tip on its own, so the queue's grading is order-independent; the order matters only for the raise (the second PR rebases onto the first). Product line: none touched.

## MEASURED by the writing seat (2026-09-21 00:5x, `--shared` scratch clone at `778e6cfe2`, node_modules farmed from the source checkout, source tracked-modified count 0 before and after)

- REAL `tasks/test_only/checker.sh` on this brief's own diff: **RESULT: PASS (8/8)**, `apply=strict` (header counts right: 4 `+` and 1 context = 5). T5 green at the tip 8/8 cells in the file; T6 NESTEDTYPEHONOURED reds exactly `nestedtype`, an assertion failure: `AssertionError: expected [ true, { id: 'dt-1', ...(2) }, 1 ] to deeply equal [ true, {}, +0 ]` — the gate's value-table delta, verbatim; T7 both controls green under it; T8 `enforcement.ts` restored by bytes (sha256 69709f07956e == tip blob) — 10708 -> 10744 bytes planted and back.
- Two WRONG variants refused at the named gates: a control declared as the PREFIX `still passes through` -> builder accepts, **checker FAIL T5** `DECLARED CELL NOT IN THE RUN: still passes through` (stopped at T5, no tamper planted); a tamper `Line: 99` (off by one) -> **builder REFUSED rc 2** naming the tip's `:99` (`): Promise<EnforcementResult> {`).
- Both-orders collision measurement (`collision_both_orders.sh`): order A (NESTEDTYPE-1 then WSTRIM-1) applies both hunks strictly at their declared lines; order B (WSTRIM-1 then NESTEDTYPE-1) applies WSTRIM-1 strictly and NESTEDTYPE-1 at `Hunk #1 succeeded at 76 (offset 4 lines)`. Both orders produce the SAME 80-line file (sha256 `fae6c65d54e7`).
- The combined file (both cells) run at the tip: **9/9**; under NESTEDTYPEHONOURED: 8/9 with exactly the NESTED cell red; under WHITESPACETYPETRIMMED: 8/9 with exactly the WSTRIM cell red; `enforcement.ts` restored clean after each.
- Whole api-gateway vitest suite with BOTH cells applied: **69 files, 680/680 green** (the gate measured 678/678 on the merged tree = this tip; +2 = the two cells). `tsc` not run: `tsconfig.json` excludes `src/__tests__`.
- Artefacts: `local-model/runs/2026-09-21_ks1203-notpinned-drafter-precheck/` (`nested/`, `wstrim/`: build.log, prepare.log, out.md, out.md.checker/, checker.log, var1_prefixcontrol/, var2_lineoffbyone/; `collision_both_orders.log`, `combined_run.log`, `full_suite_both.json`) — gitignored.
- NOT measured: no live stack was booted and no port was touched (the cell calls the function directly with a mocked catalogue); the HTTP `POST /api/documents` envelope for these two bodies is NOT exercised here; the model's own output has not run (this is the drafter's golden run).

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts`, then the hunk above exactly as shown (`@@ -72,1 +72,5 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2. Refs KS-1203** (a second characterisation pin beside #1103's UNTYPED-1). **NEVER Closes** — KS-1203's fix (which keys name a type) is Kam's ruling; this brief takes no part of it.
- **From a gate row:** the #1102-#1104 gate's NOT-PINNED row NESTEDTYPEHONOURED (VERDICT_mail_14-20-10Z.txt), tamper and proposed cell copied; the only edits are the ASCII `-` for the em dash in the title and the line's re-derivation at `778e6cfe2`.
- **Not pinned here, said plainly:** other nested spellings (`data.type`, `metadata.documentType`) are NOT pinned; one cell, one shape.
- **Collision:** the sibling brief `KS-1203-WSTRIM-1` in the same file at `:64` — see Collision above; raise NESTEDTYPE-1 first or rebase.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1203 night/inputs/test_only_1203NESTEDTYPE-1.json night/briefs/KS-1203-NESTEDTYPE-1.md ctx=65536
```
