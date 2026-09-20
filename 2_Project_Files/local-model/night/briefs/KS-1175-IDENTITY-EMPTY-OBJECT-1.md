# KS-1175 IDENTITY-EMPTY-OBJECT-1 PIN THAT identity: {} ON THE REQUEST IS ACCEPTED, ANCHORS NO IDENTITY KEY, AND READS BACK identity: null ON THE VIEW, NEVER {} — the schema-to-builder-to-view chain for the EMPTY block, which the #1105 gate measured but no cell drives — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 01:52 on 2026-09-21, #1105 gate NOT-PINNED row IDENTITY-EMPTY-OBJECT)

File: `Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts`
Tip: `cbae988dbe90ebe556459ada2cb437eaf80e2402`
Runner: `vitest`

Written from develop `cbae988dbe90ebe556459ada2cb437eaf80e2402` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 01:52 on 2026-09-21, read verbs only; the #1105 squash-merge of KS-1175 + KS-1284, the commit that CREATED every file named here). The test file at that tip is **220 lines**, read whole; its full content is in `files[...]` of your input. The products the cell drives are `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` (`identitySchema` at `:142-155`, every field `.optional()`; `identity: identitySchema.optional()` at `:214`; `IDENTITY_FIELDS` at `:130-138` — the same seven the test file's own `SEVEN` lists at `:39`; `buildFlatAnchorMetadataPayload` at `:261-`, the seven `!== undefined` spreads at `:306-312`) and `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (**130 lines**, read whole): `anchorIdentityView` at `:38-54`, the field loop at `:41-49`, and **`identity: Object.keys(identity).length > 0 ? identity : null,` at `:52`** — the ONE line that turns an empty identity object into `null`. This service runs **VITEST** (`package.json` `"test": "vitest run"`, `vitest ^4.1.9`, `vitest.config.ts` present, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `anchorReadback.ts`, `anchorSchema.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1175's contract (anchorReadback.ts header `:16-17`): `identity` on the read-back is the object of whichever of the seven non-PII fields were anchored, "or null when none were — an anchor that predates the field reads `identity: null`, never `{}`". The #1105 gate measured that a request carrying `identity: {}` (S sending the block with nothing in it) is accepted by the schema, anchors NO identity key, and reads back `identity: null` on all three surfaces — and found that the head's R9 cells cover only the ABSENT case (`ks1175-anchor-readback.test.ts` "legacy row -> null/null"); no cell sends `identity: {}` through the schema -> builder -> view chain (`grep -c -F 'identity: {}'` over this test file at the tip: 0; positive control `grep -c -F 'identity: {'` (the fixtures with content): 12 lines). So the two ways this could silently loosen are unpinned end to end: the builder starting to anchor keys for an empty block (a truthiness spread on `data.identity` would write seven `undefined`-valued keys, which the tx codec then has to carry), or the view returning `{}` instead of `null` (the `:52` guard dropped — S would then compare `{}` against its local identity and record a false mismatch). This change adds ONE cell at the START of the `describe('KS-1175 negative controls — ...', ...)` block that parses `{ ...BASE_BODY, identity: {} }` with the file's own `anchorDocumentSchema`, asserts the parse succeeds, builds the payload with the file's own `buildFlatAnchorMetadataPayload`, and asserts in one array that no `SEVEN` field is a key of `secuura` and that `anchorIdentityView(secuura).identity` is `null` — the view being pulled in with a dynamic `await import('../anchorReadback')` inside the cell so the hunk stays ONE hunk (no import line added at the top of the file). Every existing cell is unchanged. **It pins TODAY's end-to-end handling of the empty block.**

## The exact change — ONE hunk in the test file

The new cell goes at the START of the `describe('KS-1175 negative controls — the two guards the widening keeps (R5, R7; green before AND after)', ...)` block opened at `:175`, directly above that block's first cell (`:176`, `  it('R5: an unknown key inside identity is stripped and its free text never reaches the payload', () => {`, the ONE trailing context line — it occurs exactly once in the file). There is NO leading context: the line above (`:175`, the `describe(` line — it carries an em dash, which is why it is not your anchor) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts` then `+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts`.**

```
@@ -176,1 +176,8 @@
+  it('RED KS-1175: identity: {} on the request anchors no identity key and reads back identity: null on the view, never {}', async () => {
+    const { anchorIdentityView } = await import('../anchorReadback');
+    const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, identity: {} });
+    expect(result.success).toBe(true);
+    const sec = buildFlatAnchorMetadataPayload(anchorDocumentSchema.parse({ ...BASE_BODY, identity: {} }), 'preview').secuura;
+    expect([SEVEN.filter((k) => k in sec), anchorIdentityView(sec).identity]).toEqual([[], null]);
+  });
   it('R5: an unknown key inside identity is stripped and its free text never reaches the payload', () => {
```

`describe`, `it` and `expect` are already imported by the file at `:17`, `anchorDocumentSchema` and `buildFlatAnchorMetadataPayload` at `:19`, and `BASE_BODY` (`:21-24`) and `SEVEN` (`:39`) are the file's own constants — you add NO top-level import and NO helper; `anchorIdentityView` comes from the dynamic `import('../anchorReadback')` on the cell's second line (the module is pure: it imports `./anchorSchema` and `./verifyAnchorStatus`, never `index.ts`). The cell needs no app boot, no port, no chain and no database: zod and two pure functions, exactly as `:92` (`buildFlatAnchorMetadataPayload(anchorDocumentSchema.parse(BASE_BODY), 'preview').secuura`) already calls them.

## Cells

- `emptyidentity` = `RED KS-1175: identity: {} on the request anchors no identity key and reads back identity: null on the view, never {}`

## Red cells

The cell below is a GENUINE assertion-red: it fails under the tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1175: identity: {} on the request anchors no identity key and reads back identity: null on the view, never {}

## Tampers

One single-line tamper on `anchorReadback.ts:52` (the ONE line that maps an empty identity object to `null`; it occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1; positive control `grep -c -i 'identity'` over the same file is well above 1). It is the loosening the gate named: the `Object.keys(...).length > 0` guard dropped, so the view hands S `{}` where the contract says `null`. `From` is the tip's line at that number, byte for byte, and `To` is valid TypeScript (the shorthand property `identity,` — `identity` is the `Record<string, unknown>` declared at `:40`, assignable to `Record<string, unknown> | null`), so nothing fails to load and no cell reds for the wrong reason. The checker plants it and restores the file by bytes. **Frame, stated plainly:** in THIS test file no existing cell calls `anchorIdentityView` (`grep -c -i -E 'anchoridentityview|anchorreadback'`: 0 at the tip), so the tamper reds exactly the new cell here; in the SIBLING file `ks1175-anchor-readback.test.ts` the same tamper reds 4 existing cells (the absent-identity cells — measured, listed in MEASURED), which the checker does not run for this brief. What this cell adds over those four is the front half of the chain — `identity: {}` accepted by the schema and anchoring no key — and the end-to-end read of it.

### EMPTYIDENTITYKEPT — the view returns the empty object instead of null
File: `Blockchain/Dev/services/anchoring/src/anchorReadback.ts`
Line: 52
From:
```
    identity: Object.keys(identity).length > 0 ? identity : null,
```
To:
```
    identity,
```
Reds: `emptyidentity`

## Controls

- `R5: an unknown key inside identity is stripped and its free text never reaches the payload`
- `omits every identity key when no identity block is sent`
- `still accepts K-internal calls that send no identity at all (block stays optional)`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:176`, `:91` and `:56` before this hunk, `:183`, `:91` and `:56` after it — each occurs exactly once in the file and none is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix. The other 48 existing cells of this file (51 at the tip: R1 x3, R2 x10 = the seven-carry + 7 `it.each` + the FALSE boolean + the omit cell, R3 x31 = 16 arms + 14 `it.each` + the object-shape cell, R4 x4, R5 + R7 + the no-array guard = 3; minus the three controls) are also green under the tamper but are left undeclared. The `:176` control is the R5 strip guard beside the new cell in the same `describe`; the `:91` control is the ABSENT-block twin of this cell's front half (no identity at all -> no key), which the new cell extends to the EMPTY block; the `:56` control proves the schema still accepts a body with no identity.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: `identitySchema` (`anchorSchema.ts:142-155`) is a `z.object` of optional fields, so `{}` parses to `{}` (measured: `parsed identity = {}`), `result.success` is true; `buildFlatAnchorMetadataPayload` spreads a field only when `data.identity?.<field> !== undefined` (`:306-312`), so for `{}` none of the seven keys is written (measured: `identity keys in secuura = []`); `anchorIdentityView(sec)` loops `IDENTITY_FIELDS`, finds every value `undefined` and `continue`s (`:43`), leaves `identity` as `{}`, and `:52` maps it to `null` (measured: `view = {"identityCommitment":null,"identity":null}`). The asserted array is `[[], null]`.

Under **EMPTYIDENTITYKEPT** `:52` returns the empty object itself: the array reads `[[], {}]` — assertion red on the second slot (`expected {} to be null`, measured). Under it, every existing cell of this file stays green: none calls `anchorIdentityView` or imports `anchorReadback` (0 lines), so `:52` is reached by the new cell alone.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From line.** `anchorReadback.ts` at `cbae988db`, line 52 is `    identity: Object.keys(identity).length > 0 ? identity : null,` (4-space indent), byte for byte; it occurs **exactly once** in the file (`grep -c -F -x`, 1). The checker plants and restores it (T8 by sha256 after; tip blob id `f49ffb6afaa…`).
- **Premise: the gate's claim, re-derived.** The #1105 gate's NOT-PINNED row says "the head's R9 'legacy row -> null/null' cell covers the ABSENT case; no cell sends `identity: {}` through the schema -> builder -> view chain". Re-read at the tip: this file's `:56-60` (no identity) and `:91-94` (no identity -> no key) are the absent case on the front half; `ks1175-anchor-readback.test.ts:55-61` and `:101-105` are the absent case on the view; `identity: {}` appears in neither file (`grep -c -F 'identity: {}'`: 0 and 0). The gate's proposed cell used `IDENTITY_FIELDS` and `anchorIdentityView`, neither imported by this file — this brief uses the file's own `SEVEN` (the same seven names, `:39` vs `anchorSchema.ts:130-138`) and a dynamic import for the view, so the change stays ONE hunk with no import line.
- **Premise: the anchor.** The test file is **220** lines; `:176` is `  it('R5: an unknown key inside identity is stripped and its free text never reaches the payload', () => {` (2-space indent, occurs exactly once in the file) and `:175` is the `describe(` line. The trailing context line is non-blank and unique, and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: `+` lines that also occur at the tip.** Two, both added by this brief (so T4 accepts them): `  });` (`:47` and others — unavoidable for a new cell) and `    expect(result.success).toBe(true);` (`:44`, `:52`, `:58`, `:181` — the file's own idiom, reused verbatim). Every other `+` line is new to the file. No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). The title uses `:`, `{}` and `,`, no em dash.
- **Premise: the dynamic import.** `await import('../anchorReadback')` inside an `async` cell is the same idiom the KS-753 MOCKVERIFIED-1 golden diff used (`await import('crypto')`, PASS 8/8 on 2026-09-21); measured here as a probe cell at the tip: green, and `anchorIdentityView` resolved from the dynamic import returns the same `null`. vitest transforms the TS module regardless of `tsconfig`'s `commonjs` module setting; `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this cell.
- **Premise: the runner.** `anchoring/package.json` at the tip has `"test": "vitest run"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest`; `vitest.config.ts` includes `src/__tests__/**/*.test.ts` — the builder auto-detects vitest and the `Runner:` line above agrees with it.
- **Premise: no live-lane collision.** `services/anchoring/**` was the #1105 builder's lane; #1105 is MERGED at this tip (`cbae988db` is the squash), so the lane's PR is closed — Wednesday confirms no other live seat owns anchoring before queueing. Held `READY_*` files whose diffs touch `services/anchoring/`: **2** (`READY_KS-1171-8j` — a NEW test file; `READY_KS-1172-B3` — `anchorSchema.ts` + `anchorSchema.test.ts`, a product file this cell CALLS but no line this brief tampers); READYs or briefs naming `anchorReadback` or `ks1175-identity-anchoring`: **0** (positive control: READYs touching `services/api-gateway/`: 55). `git log` on the test file and on `anchorReadback.ts` at the tip: both CREATED by `cbae988db`.
- **Premise: the surface.** The cell runs zod and two pure functions with an inline body. No user store, no session, no JWT, no chain, no product bytes. ANCHORING request-schema + read-back surface, test-only pin (allowed).

## Collision

**Different test file from the two sibling briefs of this round** (`KS-1284-CHUNKED-DOCUMENTID-ROUNDTRIP-1` and `KS-1175-EXPLORERBASE-PER-NETWORK-1`, both in `ks1175-anchor-readback.test.ts`) — no hunk overlap possible; all three hunks applied in every order give the same two files (measured in the MEASURED section: 6 permutations, identical sha256 per file). Same product file (`anchorReadback.ts`) as both siblings, DIFFERENT tamper line: this brief plants `:52`; the siblings plant `:74`, `:75`, `:111`, `:112` and `cardanoMetadatum.ts:81` — no shared line; each is planted-and-restored, none moves the other. Cross-reds: this tamper reds NO cell of the siblings' new cells (CHUNKED asserts `metadata.documentId`/`certId`, EXPLORERBASE asserts `cardanoScanUrl`; neither reads `identity`) — but it DOES red 4 existing cells of the siblings' FILE (`ks1175-anchor-readback.test.ts:55`, `:58`, `:72`, `:101` — the absent-identity cells, measured), which is the sibling file pinning `:52` for the absent case, not a collision. None of the siblings' tampers reds this cell (`:74`/`:75` are the explorer base, `:111`/`:112` the document ids, the codec join is never called here). `READY_KS-1172-B3` modifies `anchorSchema.ts` — Wednesday re-checks that its hunk does not change `identitySchema` (`:142-155`) or the seven spreads (`:306-312`) before queueing both; it does not touch this test file. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 01:52, `--shared` scratch clone at `cbae988db`, node_modules farmed from the source checkout, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_ks1105rows-drafter-precheck/`)

- Whole anchoring suite at the untouched tip: **319 cells, 318 passed, 1 failed** — the 1 red is `threadTokenMint.test.ts` "parameterises mint + spend with a deterministic per-seed policyId" (develop's own; the gate's count is the same 318/319). `full_suite_tip.out`.
- The proposed cell as a probe file at the tip: **GREEN** (`probe_tip.out`; console: `identity keys in secuura = [] parsed identity = {} view = {"identityCommitment":null,"identity":null}`), including the dynamic-import variant.
- Tamper planted by bytes on the probe + the two existing KS-1175 files (`tamper_probe.log`): EMPTYIDENTITYKEPT → probe's row-4 cell red (`expected {} to be null`) + 4 cells of `ks1175-anchor-readback.test.ts` red (`returns null / null for a legacy row that predates both fields`, `returns null / null for a missing or empty payload (...)`, `never invents a key: ...`, `an anchor that predates the field reads identity: null and identityCommitment: null (both sources)`), **0 cells of `ks1175-identity-anchoring.test.ts` red**. File restored clean (git diff --quiet) after.
- (the golden checker run and the all-orders apply are appended below after the run)

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts` / `+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts`, then the hunk above exactly as shown (`@@ -176,1 +176,8 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (anchoring request schema + read-back, test-only pin — allowed). Refs KS-1175** (and KS-240 for the strip posture the cell sits beside). **NEVER Closes** — KS-1175 stays In Progress (the §5f live sweep is owed; deploy/anchor are Kam's).
- **From the #1105 gate's NOT-PINNED table** (report `2026-09-20-pr1105-tier1-r1/report.md`, row IDENTITY-EMPTY-OBJECT, "not planted" — the tamper `Object.keys(identity).length > 0 ? identity : null` -> `identity` is the gate's own suggestion, planted and measured here). The gate's proposed cell was re-derived: `IDENTITY_FIELDS` -> the file's `SEVEN`, `anchorIdentityView` via dynamic import, three asserts folded into two so the hunk is one cell with no import line.
- **Not pinned here, said plainly:** the view's `{}` -> `null` for the ABSENT case (pinned by the sibling file's four cells, which the same tamper reds); the live GET /:id and verify surfaces (the §5f sweep); a builder truthiness regression that would write `undefined`-valued keys for `{}` (a one-line tamper on `:306` would also red six `it.each` cells of this file, so it was not declared — the front-half assertion `SEVEN.filter(...)` still catches it).
- **Collision: different test file from the two siblings; same product file, tamper line `:52` shared with none; the sibling file's absent-identity cells red under this tamper by design** (measured above and in the MEASURED section).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1175 night/inputs/test_only_1175IDENTITY-EMPTY-OBJECT-1.json night/briefs/KS-1175-IDENTITY-EMPTY-OBJECT-1.md ctx=65536
```

## MEASURED — appended after the golden run (01:56, artefacts `runs/2026-09-21_ks1105rows-drafter-precheck/IDENTITY-EMPTY-OBJECT/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md`, fresh `--shared` clone at `cbae988db`): **RESULT: PASS (8/8)** — T5 green at the tip 52/52 cells (51 + the new one); T6 EMPTYIDENTITYKEPT red set == {emptyidentity}, an assertion failure (`expected [ [], {} ] to deeply equal [ [], null ]`); T7 controls green; T8 `anchorReadback.ts` restored to sha256 `9a41f455eb22`. Source tracked-modified count 0 before and after.
- All-orders apply with the two sibling briefs (`collision_all_orders.log`, 6 permutations): this hunk applies at `:176` in every order (its file is touched by no sibling); `ks1175-identity-anchoring.test.ts` is **227 lines, sha256 `ee1cbe52ea87bc02`** and `ks1175-anchor-readback.test.ts` **133 lines, sha256 `431b51cb378e933c`** after EVERY permutation.
- Both files with all three cells at the tip (`combined_run.log`): **64/64 green** (12 + 52); under EMPTYIDENTITYKEPT with both files run together: 5 red = this cell + the 4 absent-identity cells of the sibling file (as stated in Collision); under the siblings' 5 tampers this cell stays green. Whole anchoring suite with all three cells: **322 cells, 321 passed, 1 failed** — the same develop-own `threadTokenMint` red as at the tip (319/318/1).
