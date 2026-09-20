# KS-1284 CHUNKED-DOCUMENTID-ROUNDTRIP-1 PIN THAT A SCHEMA-VALID 76-CHAR documentId / certId — the ONE class of caller field that CHUNKS on chain — READS BACK JOINED under metadata.documentId and metadata.certId on the chain source of GET /api/anchors/verify/:hash — the seam the #1105 gate measured but no cell drives — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 01:49 on 2026-09-21, #1105 gate NOT-PINNED row CHUNKED-DOCUMENTID-ROUNDTRIP)

File: `Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts`
Tip: `cbae988dbe90ebe556459ada2cb437eaf80e2402`
Runner: `vitest`

Written from develop `cbae988dbe90ebe556459ada2cb437eaf80e2402` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 01:49 on 2026-09-21, read verbs only; the #1105 squash-merge of KS-1175 + KS-1284, the commit that CREATED every file named here). The test file at that tip is **121 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (**130 lines**, read whole): `anchorIdentityView` at `:38-54`, `buildVerifyResponse` at `:68-130`, `const sec = onChain?.secuura || {}` at `:77`, the `metadata: {` object at `:106-128`, **`documentId: sec.documentId || row?.document_id || null,` at `:111`** and **`certId: sec.certId || sec.documentId || row?.document_id || null,` at `:112`** — the two lines that read the chain payload's document identifiers. The codec that makes the chain form is `Blockchain/Dev/services/anchoring/src/cardano/cardanoMetadatum.ts` (**91 lines**, read whole): `CARDANO_METADATA_STRING_MAX_BYTES = 64` at `:34`, `toCardanoMetadatum` at `:59-75` (a string over 64 UTF-8 bytes becomes an ARRAY of chunks, `:61`), `fromCardanoMetadatum` at `:78-91` (an all-string array is JOINED back, **`:81`**). This service runs **VITEST** (`package.json` `"test": "vitest run"`, `vitest ^4.1.9`, `vitest.config.ts` present, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `anchorReadback.ts`, `cardanoMetadatum.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1284 is the Cardano metadatum boundary: every on-chain text string is capped at 64 bytes, so `toCardanoMetadatum` splits a longer string into an array of chunks at tx build and `fromCardanoMetadatum` joins an all-string array back on the chain read (`cardanoMetadatum.ts:61`, `:81`). The #1105 gate measured (its codec_probe (a)) that a schema-valid 65-128-char `documentId` / `certId` — the ONE class of caller-supplied field that can legitimately exceed 64 bytes (`anchorSchema.ts` allows `documentId` and `certId` up to 128 chars) — chunks on chain and comes back as the joined string, but found NO cell that drives a chunked `documentId` through `buildVerifyResponse('chain', ...)`: the file's chain-source cell (`:88-99`) chunks only `identityCommitment` and asserts only `identityCommitment` and `identity`; `git grep -i -E "metadata\.(documentId|certId)"` over this test file at the tip: **0** lines (positive control: the file names `metadata.identity` / `metadata.identityCommitment` on `:82-83`, `:97-98`, `:102-104`). So the two ways this could silently loosen are unpinned: `buildVerifyResponse` stops reading the payload's `documentId` / `certId` (the pre-extraction closure read them from the DB row only; a "simplification" back to `row?.document_id` returns `null` for every chain-sourced verify), or the codec's join is lost and an ARRAY lands in the response under a field the OpenAPI declares `type: string`. This change adds ONE cell at the START of the `describe('buildVerifyResponse — GET /api/anchors/verify/:hash (R9)', ...)` block that builds a 76-char id, chunks a `{ secuura: { hash, documentId, certId } }` payload with the file's own `toCardanoMetadatum` import, asserts the fixture really is chunked (an array — the same guard idiom the file uses on `:90`), joins it back with `fromCardanoMetadatum`, calls `buildVerifyResponse('chain', ..., undefined, { hash, network: 'preview' })` and asserts `[metadata.documentId, metadata.certId]` equals `[id, id]`. Every existing cell is unchanged. **It pins TODAY's read-back of the one schema-valid field class that CAN chunk.**

## The exact change — ONE hunk in the test file

The new cell goes at the START of the `describe('buildVerifyResponse — GET /api/anchors/verify/:hash (R9)', ...)` block opened at `:79`, directly above that block's first cell (`:80`, `  it('db source: metadata.identity beside metadata.identityCommitment, from the logical payload', () => {`, the ONE trailing context line — it occurs exactly once in the file). There is NO leading context: the line above (`:79`, `describe('buildVerifyResponse — GET /api/anchors/verify/:hash (R9)', () => {`) stays and is not written (it carries an em dash, which is why it is not your anchor). Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts` then `+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts`.**

```
@@ -80,1 +80,8 @@
+  it('RED KS-1284: chain source: a 76-char documentId and certId that chunked on chain read back joined under metadata.documentId and metadata.certId', () => {
+    const id = 'doc-1-' + 'x'.repeat(70);
+    const chunked = toCardanoMetadatum({ secuura: { hash: 'c'.repeat(64), documentId: id, certId: id } }) as { secuura: Record<string, unknown> };
+    expect(Array.isArray(chunked.secuura.documentId)).toBe(true); // the fixture really is chunked (76 chars is over the 64-byte cap)
+    const body = buildVerifyResponse('chain', fromCardanoMetadatum(chunked), undefined, { hash: 'c'.repeat(64), network: 'preview' });
+    expect([body.metadata.documentId, body.metadata.certId]).toEqual([id, id]);
+  });
   it('db source: metadata.identity beside metadata.identityCommitment, from the logical payload', () => {
```

`describe`, `it` and `expect` are already imported by the file at `:14`, `buildVerifyResponse` at `:16`, and `toCardanoMetadatum` / `fromCardanoMetadatum` at `:17` — you add NO import and NO helper. The cell needs no app boot, no port, no chain and no database: `buildVerifyResponse` is a pure function called exactly as `:81`, `:95` and `:102-104` already call it, and the codec pair is the same pair `:67` and `:89-92` already call.

## Cells

- `roundtrip` = `RED KS-1284: chain source: a 76-char documentId and certId that chunked on chain read back joined under metadata.documentId and metadata.certId`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1284: chain source: a 76-char documentId and certId that chunked on chain read back joined under metadata.documentId and metadata.certId

## Tampers

Three single-line tampers, each on a line that occurs EXACTLY ONCE in its file (counted with `grep -c -F -x`, 1 each; positive control `grep -c -i documentid` over `anchorReadback.ts` is 2 = `:111` and `:112`, and `grep -c -i cardanoscan` over the same file is 3). They are the three shapes a loosening can take: the payload's `documentId` no longer read (`:111` falls back to the DB row, which a chain-sourced verify does not have — `null`), the payload's `certId` no longer read (`:112`, the same shape), and the codec's join lost (`cardanoMetadatum.ts:81` returns the chunk ARRAY, which then lands in the response verbatim). Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript (`row` is `any | undefined`; `fromCardanoMetadatum` returns `unknown` and `value` is `unknown[]` inside `Array.isArray`), so nothing fails to load and no cell reds for the wrong reason. The checker plants them ONE AT A TIME and restores the file by bytes between them. The third tamper ALSO reds the file's existing chain-source cell (`:88`, its `identityCommitment` stays an array, so the typed view returns `null` for it) — that cell is declared in its Reds and is NOT a control.

### DOCIDFROMROWONLY — the chain payload's documentId is no longer read (DB row only)
File: `Blockchain/Dev/services/anchoring/src/anchorReadback.ts`
Line: 111
From:
```
      documentId: sec.documentId || row?.document_id || null,
```
To:
```
      documentId: row?.document_id || null,
```
Reds: `roundtrip`

### CERTIDFROMROWONLY — the chain payload's certId is no longer read (DB row only)
File: `Blockchain/Dev/services/anchoring/src/anchorReadback.ts`
Line: 112
From:
```
      certId: sec.certId || sec.documentId || row?.document_id || null,
```
To:
```
      certId: row?.document_id || null,
```
Reds: `roundtrip`

### CODECJOINDROPPED — the chain reader no longer joins an all-string array (the chunks reach the response)
File: `Blockchain/Dev/services/anchoring/src/cardano/cardanoMetadatum.ts`
Line: 81
From:
```
      return (value as string[]).join('');
```
To:
```
      return value;
```
Reds: `roundtrip`, `chain source: the same object from a chunked chain payload once the reader has joined it`

## Controls

- `db source: metadata.identity beside metadata.identityCommitment, from the logical payload`
- `an anchor that predates the field reads identity: null and identityCommitment: null (both sources)`
- `CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:80`, `:101` and `:107` before this hunk, `:87`, `:108` and `:114` after it — each occurs exactly once in the file and none is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix. The other 6 existing cells (the 6 `anchorIdentityView` cells, `:52-76`) are also green under all three tampers but are left undeclared; the chain-source cell at `:88` is RED under CODECJOINDROPPED and is declared there, never here. The `:80` control proves the db source still reads the logical payload beside the new chain-source cell; the `:101` control proves the null path for both sources; the `:107` control is the KS-522/KS-726 shape (`cardanoScanUrl`, `simulated`, `contentHash`), which none of the three tampers touches.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: `'doc-1-' + 'x'.repeat(70)` is 76 ASCII chars = 76 bytes, over the 64-byte cap, so `toCardanoMetadatum` (`:59-75`) returns `secuura.documentId` and `secuura.certId` as arrays of 2 chunks (measured: `Array.isArray` true, length 2) while `hash` (exactly 64 bytes — the bound is inclusive) stays a string; `fromCardanoMetadatum` (`:78-91`) joins each all-string array back to the 76-char id; `buildVerifyResponse('chain', ...)` takes `sec = onChain.secuura` (`:77`), `row` is `undefined`, so `:111` reads `sec.documentId` = id and `:112` reads `sec.certId` = id. The asserted array is `[id, id]`.

Under **DOCIDFROMROWONLY** `:111` reads only `row?.document_id`, which is `undefined` for a chain-sourced verify, so `metadata.documentId` is `null`: the array reads `[null, id]` — assertion red. Under **CERTIDFROMROWONLY** `:112` does the same for `certId`: `[id, null]` — assertion red. Under **CODECJOINDROPPED** `fromCardanoMetadatum` returns the 2-chunk arrays unjoined, `:111`/`:112` pass them through (an array is truthy), and the array reads `[[chunk, chunk], [chunk, chunk]]` — assertion red; the existing `:88` cell also reds (its `identityCommitment` stays an array, `anchorIdentityView` types it `null`, `toBe(COMMITMENT)` fails — assertion, not a load error). Under ALL THREE, every declared control stays green: the `:80` db-source cell asserts only `identity`, `identityCommitment`, `documentType` and `occurredAt`; the `:101` cell asserts only nulls; the `:107` cell asserts `cardanoScanUrl`, `status`, `contentHash` and the simulated shape, none of which `:111`, `:112` or the join touch.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From lines.** `anchorReadback.ts` at `cbae988db`, line 111 is `      documentId: sec.documentId || row?.document_id || null,` and line 112 is `      certId: sec.certId || sec.documentId || row?.document_id || null,` (6-space indent), byte for byte; each occurs **exactly once** in the file (`grep -c -F -x`, 1 and 1). `cardanoMetadatum.ts` line 81 is `      return (value as string[]).join('');`, exactly once (`grep -c -F -x`, 1). The checker plants and restores them one tamper at a time (T8 by sha256 after each; tip blob ids `f49ffb6afaa…` for `anchorReadback.ts`, `aaaec6c6365…` for `cardanoMetadatum.ts`).
- **Premise: the gate's claim, re-derived.** The #1105 gate's NOT-PINNED row names `anchorReadback.ts:111-112` and says "no cell drives a chunked documentId through buildVerifyResponse('chain', ...)" — re-read at the tip: the chain-source cell `:88-99` chunks `LOGICAL` (only `identityCommitment` exceeds 64 bytes there — `documentId` is 26 chars) and asserts `source`, `identityCommitment`, `identity`; no cell in the file names `metadata.documentId` or `metadata.certId` (`grep -c -i -E 'metadata\.(documentid|certid)'`: 0; positive control the same grep for `metadata\.identity`: 9 lines). A 76-char `documentId` and `certId` are schema-valid (measured in the scratch clone: `anchorDocumentSchema.safeParse` succeeds for both).
- **Premise: the anchor.** The test file is **121** lines; `:80` is `  it('db source: metadata.identity beside metadata.identityCommitment, from the logical payload', () => {` (2-space indent, occurs exactly once in the file) and `:79` is the `describe(` line. The trailing context line is non-blank and unique, and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: `+` lines that also occur at the tip.** One, added by this brief (so T4 accepts it): `  });` (`:54` and others — unavoidable for a new cell). Every other `+` line is new to the file (`:89` declares `chunked` from `LOGICAL`, not from an inline payload; `:90` guards `identityCommitment`, not `documentId`). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick — the URLs and ids are built with `+`). The title uses `-`, `:` and `.`, no em dash.
- **Premise: the runner.** `anchoring/package.json` at the tip has `"test": "vitest run"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest`; `vitest.config.ts` includes `src/__tests__/**/*.test.ts` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this cell.
- **Premise: no live-lane collision.** `services/anchoring/**` was the #1105 builder's lane; #1105 is MERGED at this tip (`cbae988db` is the squash), so the lane's PR is closed — Wednesday confirms no other live seat owns anchoring before queueing. Held `READY_*` files whose diffs touch `services/anchoring/`: **2** (`READY_KS-1171-8j` — a NEW test file `ks1171-guard-3-s-re-poll-reads.test.ts`; `READY_KS-1172-B3` — `anchorSchema.ts` + `anchorSchema.test.ts`); READYs or briefs naming `anchorReadback`, `ks1175-anchor-readback`, `ks1175-identity-anchoring` or `cardanoMetadatum`: **0** (positive control: READYs touching `services/api-gateway/`: 55). `git log` on the test file, `anchorReadback.ts` and `cardanoMetadatum.ts` at the tip: all three CREATED by `cbae988db` (one commit each).
- **Premise: the surface.** The cell calls two pure codec functions and one pure response builder with inline fixtures. No user store, no session, no JWT, no product bytes. ANCHORING read-back surface, test-only pin (allowed).

## Collision

**Same test file as the sibling brief `KS-1175-EXPLORERBASE-PER-NETWORK-1` (this round) — DISJOINT hunks, same product file, DIFFERENT tamper lines.** That brief's hunk is `@@ -107,1 +107,6 @@` (inserts directly above the `CONTROL:` cell, trailing context `:107`); this hunk is `@@ -80,1 +80,8 @@` (inserts at the START of the same `describe`, trailing context `:80`). Both orders apply with `git apply` — measured in the MEASURED section: **this first, then EXPLORERBASE** applies this at `:80` and EXPLORERBASE's at `:114` (offset +7 — the `:107` context line is unique, so git locates it seven lines down); **EXPLORERBASE first, then this** applies both at their stated lines (this hunk's `:80` is above the other insertion, so it never shifts). The resulting file is byte-identical in both orders (sha256 compared) and runs 12/12 green at the tip. Tamper lines: this brief plants `:111`, `:112` and `cardanoMetadatum.ts:81`; EXPLORERBASE plants `:74` and `:75` — no shared line; each is planted-and-restored, none moves the other. Cross-reds: none of this brief's tampers reds EXPLORERBASE's cell (it asserts only `cardanoScanUrl`); neither of EXPLORERBASE's tampers reds this cell (it asserts only `metadata.documentId` / `certId`). The third brief of this round (`KS-1175-IDENTITY-EMPTY-OBJECT-1`) is in a DIFFERENT test file (`ks1175-identity-anchoring.test.ts`) and plants `anchorReadback.ts:52` — not a line this brief touches, and its cell does not reach `:111`/`:112`/the codec. The two held READYs under `services/anchoring/` (`KS-1171-8j`, `KS-1172-B3`) touch neither this test file nor any tamper line. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 01:49, `--shared` scratch clone at `cbae988db`, node_modules farmed from the source checkout, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_ks1105rows-drafter-precheck/`)

- Whole anchoring suite at the untouched tip: **319 cells, 318 passed, 1 failed** — the 1 red is `threadTokenMint.test.ts` "parameterises mint + spend with a deterministic per-seed policyId" (develop's own, `Could not serialize the data: Error: Unsupported type`; the gate's count is the same 318/319). `full_suite_tip.out`.
- The proposed cell as a probe file at the tip: **GREEN** (`probe_tip.out`; console: `chunked documentId isArray = true len 2`, `schema-valid 76-char documentId: true certId: true`).
- Tampers planted by bytes on the probe + the two existing KS-1175 files (`tamper_probe.log`): DOCIDFROMROWONLY → probe's row-2 cell red, 0 existing red; CERTIDFROMROWONLY → the same; CODECJOINDROPPED → probe's row-2 cell red + `chain source: the same object from a chunked chain payload once the reader has joined it` red, nothing else. Files restored clean (git diff --quiet) after each.
- (the golden checker run and the both-orders apply are appended below after the run)

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts` / `+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts`, then the hunk above exactly as shown (`@@ -80,1 +80,8 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (anchoring read-back surface, test-only pin — allowed). Refs KS-1284** (and KS-1175, whose read-back file this cell lives in; KS-721 for the chunking history). **NEVER Closes** — KS-1284 stays In Progress until the live sweep observes Blockfrost's real `json_metadata` shape for a chunked string (the gate's M-3 / merge addendum); this cell pins the in-process codec-to-response round trip, not the live chain.
- **From the #1105 gate's NOT-PINNED table** (report `2026-09-20-pr1105-tier1-r1/report.md`, row CHUNKED-DOCUMENTID-ROUNDTRIP, "no cell" at the gate's 319). The gate's proposed cell was re-derived and kept in substance; it gained the `Array.isArray` fixture guard (the file's own `:90` idiom) so a future raise of the 64-byte cap cannot turn the cell into a no-op, and the assertion was folded into one array so any of the three tampers reds the ONE cell.
- **Not pinned here, said plainly:** the live chain read in `index.ts:699` (`fromCardanoMetadatum` at the ONE chain-read site — the gate's T12 row, bootless-untested, not this round); the tx-build attach point `transaction.ts:114` (T13, not this round); the DB source with a long `documentId` (it never chunks — the DB holds the logical form).
- **Collision: same test file as `KS-1175-EXPLORERBASE-PER-NETWORK-1`, disjoint hunks (start of the describe vs above its last cell), both orders measured; three tamper lines, none shared** (measured above and in the MEASURED section).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1284 night/inputs/test_only_1284CHUNKED-DOCUMENTID-ROUNDTRIP-1.json night/briefs/KS-1284-CHUNKED-DOCUMENTID-ROUNDTRIP-1.md ctx=65536
```

## MEASURED — appended after the golden run (01:56, artefacts `runs/2026-09-21_ks1105rows-drafter-precheck/CHUNKED-DOCUMENTID-ROUNDTRIP/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md`, fresh `--shared` clone at `cbae988db`): **RESULT: PASS (8/8)** — T5 green at the tip 11/11 cells (10 + the new one); T6 DOCIDFROMROWONLY red set == {roundtrip}; CERTIDFROMROWONLY == {roundtrip}; CODECJOINDROPPED == {roundtrip, chain source: the same object from a chunked chain payload once the reader has joined it}; every red an assertion failure; T7 controls green under all 3; T8 `anchorReadback.ts` restored to sha256 `9a41f455eb22` and `cardanoMetadatum.ts` to `48497ffc0937` after each. Source tracked-modified count 0 before and after.
- All-orders apply with the two sibling briefs (`collision_all_orders.log`, 6 permutations): this hunk applies at `:80` in every order; EXPLORERBASE's applies at `:107` when first and at `:114` (offset +7) after this one; `ks1175-anchor-readback.test.ts` is **133 lines, sha256 `431b51cb378e933c`** and `ks1175-identity-anchoring.test.ts` **227 lines, sha256 `ee1cbe52ea87bc02`** after EVERY permutation.
- Both files with all three cells at the tip (`combined_run.log`): **64/64 green** (12 + 52); under each of the 6 tampers of the round the red set is exactly what each brief declares (this brief's three: 1, 1, 2). Whole anchoring suite with all three cells: **322 cells, 321 passed, 1 failed** — the same develop-own `threadTokenMint` red as at the tip (319/318/1).
