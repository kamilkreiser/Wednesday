# KS-1203 UNTYPED-1 PIN THAT AN UNTYPED BODY RESOLVES NO DOCUMENT TYPE AT ALL — AN EMPTY docType AND NO CATALOGUE LOOKUP — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 2026-09-20, round 23)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts`
Tip: `e470198783bcb1ef0eac94780f87579974051423`
Runner: `vitest`

Written from develop `e470198783bcb1ef0eac94780f87579974051423` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" log -1 e47019878`, read verbs only; the tip of the #1097-#1099 merge, 2026-09-20 05:54:10 +1000). The test file at that tip is **64 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts` (**279 lines**, read whole): `enforceDocumentTypeRules` at `:96-198`, specifically the type-reference read at `:100` and the no-type early return at `:115-117`. This service runs **VITEST**.

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `enforcement.ts` or any other product file: the behaviour is already right at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1203 reports that a connector whose key is restricted to `['SSD_DOCUMENT']` can still create a document of the DEFAULT type by sending no type at all, and it rests on one READ premise stated in its own Detail section: *"at the gateway no type is created"* — the gateway resolves nothing, forwards the body, and originate stores it as `DOCUMENT`. That premise lives in exactly one place. `enforceDocumentTypeRules` reads its type reference at `:100` from **two** key spellings only — `body.documentType` and `body.type` — and at `:115-117` an empty reference returns `{ ok: true, docType: {} }` BEFORE the catalogue is consulted at `:119`/`:127`. That is what makes all eight of the gate's shapes admit: an untyped body, `documentType: ''`, `type: ''`, the ignored spellings `DocumentType` / `document_type` / `Type`, and an untyped `data` carrier all leave the reference empty, so there is no resolved type for any allow-list to test and Redis is never asked. The suite pins none of it: the file's existing `:53` cell sends `{}` and asserts only `result.ok === true` — it never reads `docType`, so it is blind both to a default type being invented and to a new key spelling being honoured, which are precisely the two directions KS-1203's owner decision can go ("apply the allow-list to the resolved default type, or require a restricted connector to name a type"). This change adds ONE cell that drives seven untyped shapes through the real `enforceDocumentTypeRules` and asserts each returns `[true, {}]` and that the catalogue is never consulted. Every existing cell is unchanged. **It pins TODAY's behaviour and decides nothing about KS-1203**, whose recommendation is explicitly *"Not built. Owner's choice"* — this brief does not take that choice; it makes the premise the choice rests on visible to the suite.

## The exact change — ONE hunk in the test file

The new cell goes at the end of the `describe('KS-501 non-string documentType', ...)` block opened at `:26`, directly above that block's closing line `});` (`:64`, the file's LAST line and the ONE trailing context line). There is NO leading context: the line above (`:63`, `  });`) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts`.**

```
@@ -64,1 +64,8 @@
+  it('RED KS-1203: a body carrying no resolvable documentType admits with an EMPTY docType and never consults the catalogue', async () => {
+    const untypedShapes = [{}, { documentType: '' }, { type: '' }, { DocumentType: 'SSD_DOCUMENT' }, { document_type: 'SSD_DOCUMENT' }, { Type: 'SSD_DOCUMENT' }, { data: { title: 'no type here' } }];
+    for (const body of untypedShapes) {
+      const result = await enforceDocumentTypeRules(body, undefined);
+      expect([result.ok, (result as { docType?: unknown }).docType]).toEqual([true, {}]);
+    }
+    expect(redisService.getAllDocumentTypes).not.toHaveBeenCalled();
+  });
 });
```

`enforceDocumentTypeRules` is already imported by the file at `:15` and `redisService` at `:24` — you add NO import. The cell needs no app boot, no port and no database: `enforceDocumentTypeRules` is an exported async function over a plain object, and the file's existing `vi.mock('../services/redis', ...)` at `:17-22` plus the `beforeEach` at `:27-33` (which calls `vi.clearAllMocks()` and seeds a one-entry catalogue) are the only doubles in play — your cell adds none and changes none. The seven shapes are the gate's own list minus `__proto__.type`, which is deliberately NOT included: whether `body.type` sees a `__proto__` payload depends on how the body was constructed (a JSON-parsed `__proto__` is an own property, an object literal's is a prototype set), and a cell whose result turns on that is a cell that grades the fixture rather than the product.

## Cells

- `untypednotype` = `RED KS-1203: a body carrying no resolvable documentType admits with an EMPTY docType and never consults the catalogue`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1203: a body carrying no resolvable documentType admits with an EMPTY docType and never consults the catalogue

## Tampers

Two single-line tampers on two DIFFERENT lines of `enforcement.ts`. They are KS-1203's own decision space, inverted: the first honours the ignored key spellings, the second invents a default type for an untyped body. Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript, so nothing fails to load and no cell reds for the wrong reason.

### SPELLINGSHONOURED — the ignored key spellings start resolving a type
File: `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts`
Line: 100
From:
```
  const typeRefRaw = body.documentType || body.type || '';
```
To:
```
  const typeRefRaw = body.documentType || body.type || body.DocumentType || body.document_type || body.Type || '';
```
Reds: `untypednotype`

### UNTYPEDGETSADEFAULT — an untyped body resolves a DEFAULT document type
File: `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts`
Line: 116
From:
```
    return { ok: true, docType: {} };
```
To:
```
    return { ok: true, docType: { code: 'DOCUMENT', isDefault: true } };
```
Reds: `untypednotype`

## Controls

- `still passes through an absent/empty documentType`
- `resolveDocumentType is total: a non-string returns null rather than throwing`

*(Both are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:53` and `:58` — and each occurs exactly once in the file and is not a prefix of any other title. For a VITEST or JEST suite the checker matches a declared cell by its FULL title, never by a prefix; the prefix rule in `build_test_only_input.sh`'s header is documented for BASH suites. Measured 2026-09-20 on the KS-1275 round-1 FAIL: two controls declared as prefixes came back `DECLARED CELL NOT IN THE RUN`. The first control is the strongest liveness proof available in this file — it drives the SAME early-return branch at `:115-117` that UNTYPEDGETSADEFAULT mutates, and stays green there because it asserts only `result.ok`. The file's other three cells are an `it.each` whose titles are `%s`-substituted at run time, and `:47`, whose title contains BACKTICKS and therefore cannot be written inside a backticked control line; all four are green under both tampers but are left undeclared rather than risk the name.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes. For every one of the seven shapes `body.documentType` and `body.type` are both absent or `''`, so `:100` yields `''`, the non-string guard at `:106` is skipped, `typeRef` is falsy at `:115`, and `:116` returns `{ ok: true, docType: {} }` — before `resolveDocumentType` (`:119`) and before the catalogue re-read (`:127`), so the mocked `getAllDocumentTypes` is never called.

Under **SPELLINGSHONOURED** the fourth shape (`DocumentType: 'SSD_DOCUMENT'`) now yields the reference `'SSD_DOCUMENT'`; the seeded catalogue holds only `DEGREE`, so `resolveDocumentType` returns null, `registered.length > 0`, and the call answers `400 UNKNOWN_DOCUMENT_TYPE` — the cell fails by assertion on `[false, undefined]` against `[true, {}]`. Under **UNTYPEDGETSADEFAULT** every shape still admits but `docType` is `{ code: 'DOCUMENT', isDefault: true }`, so the first iteration already fails by assertion. Under BOTH, every existing cell stays green: the three `it.each` cells and `:47` send a TRUTHY non-string on `documentType` / `type`, so they return `400 VALIDATION_ERROR` at `:106-113` and never reach either tampered site's effect; `:53` sends `{}` and asserts only `result.ok === true`, which is true under both; and `:58` calls `resolveDocumentType` directly, which neither tamper touches.

## Premises (measured — by reading the tip, NOT by running anything)

- **Premise: the two `From` lines.** `enforcement.ts` at `e47019878`, line 100 is `  const typeRefRaw = body.documentType || body.type || '';` and line 116 is `    return { ok: true, docType: {} };`, byte for byte. Line 100's text occurs **exactly once** in the file. Line 116's text occurs **twice** (`:116` and `:136`, the empty-catalogue pass-through) — this is a SINGLE-LINE tamper, which the checker plants strictly by line index after a byte-equality check at that index, so the twin at `:136` is not ambiguity. It is named here so nobody re-reads it as one.
- **Premise: the anchor.** The test file is **64** lines; `:64` is `});` (column 0, the file's last line, closing the `describe` opened at `:26`) and `:63` is `  });`. The trailing context line is non-blank and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: nothing pins this today.** The file's six cells are the three `it.each` non-string cells (`:35-45`), `:47`, `:53` and `:58`. Only `:53` sends an untyped body, and it asserts `result.ok` alone — `docType` is never read anywhere in the file, and none of the ignored spellings (`DocumentType`, `document_type`, `Type`) appears in it.
- **Premise: no `+` line re-adds a tip line.** `untypedShapes`, `KS-1203`, `document_type` and `no type here` occur **0** times in the test file at the tip. The only `+` line that also occurs at the tip is the closing `  });` (unavoidable for a new cell).
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted).
- **Premise: the runner.** `api-gateway/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest` anywhere — the builder auto-detects vitest and the `Runner:` line above agrees with it. `vitest.config.ts` sets `setupFiles: ['./vitest.setup.ts']` (the KS-184 RS256 keypair) and no `include` narrowing, so this file runs under the default pattern as it does today.
- **Premise: no live-seat collision.** The live Secuura seat is on PRs #1100/#1101 in `services/api-gateway/src/__tests__/ks1230*` and `ks1215*`. This brief's file is `ks501-enforcement-non-string-doctype.test.ts` and its product file is `services/enforcement.ts` — neither is one of those, and no held `READY_*` carries a hunk in either.
- **Premise: is this suite known red?** No ticket on the board claims the api-gateway vitest suite is red — the known-red claim (KS-1051) names the **services/originate JEST** suite, which is a different service and a different runner, and is why this brief was not written into originate. Positive evidence for this suite at this exact tip: the KS-1282 N99-1 brief records the whole api-gateway vitest suite measured **671/671 green** in a `--shared` scratch clone at `e47019878`. That measurement is ANOTHER SEAT'S, quoted, not re-run here.

## NOT MEASURED — state this in the READY

**No suite was run for this brief and no scratch clone was made.** The writing seat was barred from running any test suite and from touching any local port (a live PostgreSQL of unknown ownership sits on 127.0.0.1:5432), so this brief carries **no** tip-suite count, **no** per-tamper red count and **no** checker pre-run. The "reds exactly one cell" claim above is REASONED FROM SOURCE — every one of the file's six existing cells was read and walked against both tampers — **not measured**. **Before this is queued, run the real checker on the brief's own diff in a `--shared` scratch clone at the tip** — the expected result is `ks501-enforcement-non-string-doctype.test.ts` green at the tip with one extra cell (7 cells), and each tamper reding exactly `untypednotype` and nothing else.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts`, then the hunk above exactly as shown (`@@ -64,1 +64,8 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2. Refs KS-1203** (and KS-501, whose file this is; KS-1176 is the parent gate). **NEVER Closes** — KS-1203's recommendation is *"Not built. Owner's choice"*, and this brief takes no part of that choice. The default-type behaviour it pins is the status quo the owner will rule on.
- **Not from a gate cell.** This is a completeness pin in the N97-1 / N99-1 / KS-1275 species: the ticket's load-bearing READ premise ("at the gateway no type is created") is provably invisible to the suite today, and both tampers are the two shapes a fix could take — so whichever way Kam rules, the ruling arrives as a deliberate change to this cell rather than as a silent one.
- **Surface note:** `enforcement.ts` sits beside auth checks (`meetsVerificationLevel`, `requireMFA`) but this cell touches NONE of them — it never constructs a user, never reaches `:143-177`, and the tampers are on the type-reference read and the no-type early return. No credential, session, token or MFA path is exercised. Flagging it so the auth-goes-last order is applied with the facts.
- **Adjacency to the live seat, stated:** KS-1203's subject (`allowedDocumentTypes`) is thematically near the live seat's `ks1230-settings-write-validates-allowed-document-types.test.ts`. There is no file overlap and no product-file overlap; the adjacency is named so Wednesday can hold it if she would rather the whole allow-list theme wait for #1100/#1101 to land.
- `__proto__.type`, one of the gate's eight shapes, is deliberately excluded — see the note under the fence.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1203 night/inputs/test_only_1203UNTYPED-1.json night/briefs/KS-1203-UNTYPED-1.md ctx=65536
```
