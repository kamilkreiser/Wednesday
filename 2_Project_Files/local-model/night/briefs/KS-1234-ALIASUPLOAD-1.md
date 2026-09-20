# KS-1234 ALIASUPLOAD-1 PIN THAT THE /api/v1/nft/upload ALIAS IS NOT PARSED LIKE ITS TWIN — the 10 MB upload parser is mounted by PRE-REWRITE path (index.ts:422), so a non-JSON body on /api/nft/upload is refused 400 at the parser while the same body on /api/v1/nft/upload streams unparsed to the nft upstream and answers 200 — the real gateway over loopback with the file's own fake upstream — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one describe with one cell added, no product file** (written 05:1x on 2026-09-21, the #1106-#1111 batch gate's NOT-PINNED row ALIASUPLOADPARSERASYMMETRY, RE-TARGETED from `/api/documents/upload` to `/api/nft/upload` — see "What the cell pins")

File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts`
Tip: `362e51fe0db7e73d5557924902763fe3f10fd8c7`
Runner: `vitest`

Written from develop `362e51fe0db7e73d5557924902763fe3f10fd8c7` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 05:0x on 2026-09-21, read verbs only; the tree that carries the six #1106-#1111 squashes, #1108 = KS-1234 V1-ALIAS-BODYPARSE included). The test file at that tip is **94 lines** (blob `3f85887f7268`), read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/api-gateway/src/index.ts` (blob `4e7fc1174d54`, **1279 lines**, read whole around the parsers): `proxyPaths` at `:400-412` (`'/api/nft'` on `:408`), `shouldParseBody` at `:413` (judges the alias by its rewritten path), the guarded `express.json` / `urlencoded` at `:416-417`, **`const uploadBodyParser = express.json({ limit: '10mb' });` at `:420`, `app.use('/api/documents/upload', uploadBodyParser);` at `:421`, `app.use('/api/nft/upload', uploadBodyParser);` at `:422`** — mounted by PATH, and the path at that point is the caller's, because the `/api/v1/` -> `/api/` rewrite is `:560-563`, AFTER them. The nft proxy is `src/routes/proxy.ts:1130-1154` (`router.use('/api/nft', authenticateToken(false), <not-deployed guard>, proxy('nft', ...))`); a PARSED body is re-streamed by `onProxyReq` (`:310-317`, `proxyBodyToWrite` `:66-71`), an UNPARSED one pipes natively. This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest ^4.1.9`, `vitest.setup.ts` provisions `__TEST_JWT_PRIVATE_PEM`; no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `index.ts`, `routes/proxy.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1234 (#1108) made the `/api/v1/` alias of every proxyPaths route "exactly like its twin" for the four `shouldParseBody`-guarded middlewares. The #1106-#1111 gate's row ALIASUPLOADPARSERASYMMETRY (READ ONLY, "a cell question, not a tamper") noticed the exception: the two upload parsers at `:421-422` are mounted by the PRE-rewrite path, so `/api/<x>/upload` gets the 10 MB JSON parser and `/api/v1/<x>/upload` gets NO parser at all (at develop the alias got the 1 MB `express.json` through the old predicate). The gate named `/api/documents/upload` and asked for it to be measured first. **Measured: `/api/documents/upload` cannot carry the pin** — a JSON POST answers **405** on both spellings (the spec's `/api/documents/{id}` regex swallows `upload` and declares no POST; the spec has no `/api/documents/upload` path), a non-JSON body answers 400 (twin, the parser) / 405 (alias, the method gate) and no body reaches originate either way — a product finding for the owners (UPLOADROUTEDEAD, notes below), not a pin. `/api/nft/upload` carries it: it matches no spec regex, so both spellings reach the nft proxy; a VALID JSON body is indistinguishable (the twin is parsed and re-streamed as `JSON.stringify`, the alias pipes the same bytes — both `[200, ['<b>ks1234</b>']]`, measured); a NON-JSON body is the instrument that shows the asymmetry: the twin is refused **400** by `:422`'s parser before any proxy (no upstream hit), the alias is never parsed, streams the bytes to the nft upstream and answers **200** (one upstream hit whose recorded title is `-`, the harness's marker for a non-JSON body). This change adds ONE describe with ONE cell BEFORE the file's existing describe; the cell sends `'ks1234-not-json'` to both spellings and asserts `[[400, []], [200, ['-']]]` — the twin's `[status, hits]` whole, the alias's status and its hits' TITLES only (the alias's upstream URL is deliberately not asserted — see the HPM finding in the notes). TWO tampers red it, one per half: the parser ALSO mounted on the alias (`[[400, []], [400, []]]`), and the parser NOT mounted on the twin (`[[200, ['-']], [200, ['-']]]`). **It pins TODAY's asymmetry as a characterisation, not an endorsement**: whichever way the owners unify the upload parsers, this cell goes red on purpose and is rewritten with that decision.

## The exact change — ONE hunk in the test file

The new describe goes BETWEEN `:83` (`}`, the close of the file's `send` helper, the ONE leading context line) and `:84` (`describe('KS-1234: a JSON create on the /api/v1/documents alias must answer', () => {`, the ONE trailing context line, unique in the file). `}` alone occurs four times in the file (`:28`, `:32`, `:35`, `:83`), but the PAIR `}` then that `describe(` line occurs exactly once (`:83-84`), so the hunk is anchored. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts`.**

```
@@ -83,2 +83,9 @@
 }
+describe('KS-1234: the /api/v1/nft/upload alias is NOT parsed like its twin - a characterisation of the upload-parser asymmetry', () => {
+  it('RED KS-1234: a non-JSON body on POST /api/nft/upload is refused 400 by the 10 MB upload parser before any proxy, while the same body on POST /api/v1/nft/upload streams unparsed to the nft upstream and answers 200', async () => {
+    const twin = await send('POST', '/api/nft/upload', 'ks1234-not-json');
+    const alias = await send('POST', '/api/v1/nft/upload', 'ks1234-not-json');
+    expect([twin, [alias[0], alias[1].map((h) => h.split(' ')[2])]]).toEqual([[400, []], [200, ['-']]]);
+  }, 15000);
+});
 describe('KS-1234: a JSON create on the /api/v1/documents alias must answer', () => {
```

`describe`, `it` and `expect` are already imported by the file at `:9`, and `send` (`:74-83`) is the file's own helper (the real gateway on `127.0.0.1:0`, `x-api-key` = the file's `CREATE_KEY`, `content-type: application/json` on every request, a 3 s bound, `[status, hits since the mark]`) — you add NO import, NO helper and NO file-scope constant. Each hit is `"<METHOD> <url> <title>"` (`:54`) where `titleOf` (`:33-35`) answers `'-'` for a body that is not JSON, so `h.split(' ')[2]` is `'-'`. The new describe sits at file scope after the helpers and before the existing describe; the file's `beforeAll` / `afterAll` (`:40-71`) are file-scope hooks, so they wrap this describe too. The cell's timeout argument `15000` matches the file's three existing cells. The cell needs no port of its own, no database (`../db` is mocked at `:14-17`) and no real upstream (the fake at `:41-56` answers 200 to any unhandled URL and records the hit; `NFT_SERVICE_URL` points at it, `:58-59`).

## Cells

- `asymmetry` = `RED KS-1234: a non-JSON body on POST /api/nft/upload is refused 400 by the 10 MB upload parser before any proxy, while the same body on POST /api/v1/nft/upload streams unparsed to the nft upstream and answers 200`

## Red cells

The cell below is a GENUINE assertion-red: it fails under EACH tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1234: a non-JSON body on POST /api/nft/upload is refused 400 by the 10 MB upload parser before any proxy, while the same body on POST /api/v1/nft/upload streams unparsed to the nft upstream and answers 200

## Tampers

TWO single-line tampers, both on `index.ts:422` (one planted at a time; the checker restores by bytes between them). The From line is unique in the file (python whole-line scan: hits `[422]`; `uploadBodyParser` occurs on exactly three lines, `:420` the const, `:421` documents, `:422` nft; positive control `shouldParseBody`: 5 lines). `From` is the tip's line at that number, byte for byte; each `To` is valid TypeScript (`app.use` takes a path array; a comment line is valid; measured: the file loads and runs 6 cells under each). Each is one half of the asymmetry unified the other way — the two plausible "make the alias exactly like its twin" edits.

### PARSERONNFTALIAS — the 10 MB upload parser mounted on the alias too: both spellings parsed
File: `Blockchain/Dev/services/api-gateway/src/index.ts`
Line: 422
From:
```
app.use('/api/nft/upload', uploadBodyParser);
```
To:
```
app.use(['/api/nft/upload', '/api/v1/nft/upload'], uploadBodyParser);
```
Reds: `asymmetry`

### NFTPARSERUNMOUNTED — the 10 MB upload parser not mounted on the twin: neither spelling parsed
File: `Blockchain/Dev/services/api-gateway/src/index.ts`
Line: 422
From:
```
app.use('/api/nft/upload', uploadBodyParser);
```
To:
```
// KS-1234 tamper: the 10 MB upload parser is NOT mounted on /api/nft/upload
```
Reds: `asymmetry`

## Controls

- `control: POST /api/documents as application/json answers 200 and originate receives the body`
- `control: the /api/v1 alias itself is live - GET /api/v1/signatories answers 200 and reaches originate at /api/signatories`

*(Both are FULL `it(...)` titles of the file's existing cells at `:85` and `:88`, unchanged by this hunk, which inserts above the describe that holds them. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; no title is a prefix of another. Neither control touches `/api/nft`, so neither tamper can change its answer — they prove the gateway, the key validation, the exchange and the alias rewrite all still run while the RED cell reds on the one mount. The file's `:91` red-glyph alias cell is also green under both tampers but is left undeclared.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes. TWIN: `send` POSTs `'ks1234-not-json'` as `application/json` to `/api/nft/upload`; `enforceJsonContentType` passes it (the declared type is JSON); `shouldParseBody` is false (`'/api/nft'` prefix), `:416-417` skip; **`:422` parses it** — `express.json` throws `entity.parse.failed` (400) and the gateway's error handler answers **400**; nothing reaches the proxy: `[400, []]` (measured). ALIAS: the same body to `/api/v1/nft/upload`; `:416-417` skip (the predicate judges `/api/nft/upload`); **`:421-422` match nothing** (the path is still `/api/v1/nft/upload` here); `:561` rewrites `req.url` to `/api/nft/upload`; the method gate matches no spec entry; the nft mount validates the key against the fake and the proxy pipes the raw bytes; the fake records `POST /api/v1/nft/upload -` and answers 200: `[200, ['-']]` after the title map (measured). Together `[[400, []], [200, ['-']]]`.

Under **PARSERONNFTALIAS** `:422` also matches `/api/v1/nft/upload`, so the alias is parsed and refused the same way: `expected [ [ 400, [] ], [ 400, [] ] ] to deeply equal [ [ 400, [] ], [ 200, [ '-' ] ] ]`, an assertion red (measured). Under **NFTPARSERUNMOUNTED** the twin is no longer parsed and streams like the alias: `expected [ [ 200, [ 'POST /api/nft/upload -' ] ], [ 200, [ '-' ] ] ] to deeply equal [ [ 400, [] ], [ 200, [ '-' ] ] ]`, an assertion red (measured). Every existing cell stays green under both (measured: whole 686-cell suite under each tamper, 1 red — this cell).

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From line.** `index.ts` at `362e51fe0`, line 422 is `app.use('/api/nft/upload', uploadBodyParser);` (column 0), byte for byte; it occurs **once** (whole-line hits `[422]`; `:421` is the documents twin, a different line). The checker plants each tamper and restores it (T8 by sha256 after; tip blob `4e7fc1174d54`, file sha256 `9c57fc946261faa8` measured before each plant and after each restore).
- **Premise: the gate's claim, re-derived.** The batch gate's row: "`/api/documents/upload` gets the 10 MB JSON parser by its pre-rewrite mount; at the head `/api/v1/documents/upload` gets NO parse ... proxy.ts forwards an unparsed stream for a proxyPaths route, so 200 is the expected value to record — measure it first". Measured (`probe_gateway.tip.out`): `/api/documents/upload` JSON `[405, []]` both spellings (P1), non-JSON `[400, []]` / `[405, []]` (P2), multipart `[415, []]` (P3) — the 200 the gate expected does not exist on that path; `/api/nft/upload` JSON `[200, [...]]` both spellings (P4), non-JSON `[400, []]` / `[200, ['POST /api/v1/nft/upload -']]` (P5) — the asymmetry, on a route that is live. READ: `docs/openapi/secuura-api.yaml` has no `/api/documents/upload` and no `/api/nft/upload` path (`grep '^  /.*upload'`: one hit, `/api/nft/ipfs/upload`; positive control `^  /api/documents`: 12 paths, `^  /api/nft`: 18 paths); `/api/documents/{id}` (`:27635`) becomes `^/api/documents/[^/]+$` (`specRouteMap.ts:55`) and declares no POST (`index.ts:1057` -> 405); no spec regex matches `/api/nft/upload` (`index.ts:1052` falls through).
- **Premise: the anchor.** The test file is **94** lines; `:83` is `}` and `:84` is the unique `describe('KS-1234: a JSON create on the /api/v1/documents alias must answer', () => {`. Both context lines are non-blank, so no blank line is asked of you anywhere. The hunk has ONE leading and ONE trailing context line and is a pure insertion between them.
- **Premise: `+` lines that also occur at the tip.** Two, both added by this brief (so T4 accepts them): `  }, 15000);` (`:87`, `:90`, `:93`) and `});` (`:17`, `:71`, `:94`). No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). Titles use `:`, `-` and `/`, no em dash.
- **Premise: the runner.** `services/api-gateway/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9`, no jest — the builder auto-detects vitest and the `Runner:` line agrees.
- **Premise: the surface.** The real gateway over loopback with a fake upstream and mocked db; a connector key validated and exchanged against the fake; two spellings of one upload path observed. No user store, no session, no real JWT key beyond the harness's test pair, no product bytes. GATEWAY body-parser mount surface, test-only pin (allowed).

## Collision

**Same test file as TWO other hunks at this tip — DISJOINT, order-independent, measured.** (1) The READY `KS-1234-ALIASOTHERROUTES-1` (`@@ -88,1 +88,5 @@`, one cell BEFORE `:88`). (2) The sibling brief of this round `KS-1234-SECURITYMIDDLEWARESKIP-1` (`@@ -92,3 +92,10 @@`, two cells AFTER `:93`). This hunk inserts BEFORE `:84`. All SIX apply orders of the three hunks on the tip file give **one sha256 `68c8a00b2c8b9624`, 112 lines** (`collision_orders.v2.log`); every pair both ways gives one sha (this + ALIASOTHERROUTES: `95e2234ae41cd5d0`, 105 lines, either order; this + SECURITYMIDDLEWARESKIP: `3ca31008f120360f`, 108 lines, either order). The file with all three: **7/7** at the tip; the whole suite with all three: **687/687**. Tamper lines: ALIASOTHERROUTES plants `index.ts:413`, SECURITYMIDDLEWARESKIP plants `:458`, this plants `:422` — no shared line. (The sibling's first cut collided with THIS hunk's trailing `  }, 15000);` + `});` — fixed on the sibling's side with a second context line; recorded there.) No banked READY other than ALIASOTHERROUTES names this test file. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 05:0x, `--shared` scratch clone `m_clone_1` at `362e51fe0`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck-b/` and its `ALIASUPLOADPARSERASYMMETRY/`)

- Whole api-gateway suite at the bare tip: **70 files, 683/683** (`gateway_full_suite_before.out`). This file with this hunk AND the sibling SECURITYMIDDLEWARESKIP hunk at the tip: **6/6 green** (`gateway_file_tip_both.out`). Whole suite with both: **686/686** (`gateway_full_suite_after_both.out`).
- PARSERONNFTALIAS planted by bytes (hits `[422]`) -> this file **1 failed / 5 passed of 6**, the red = `asymmetry`, `expected [ [ 400, [] ], [ 400, [] ] ] to deeply equal ...` (`tamper_PARSERONNFTALIAS.out`); whole suite under it **1 failed / 685 passed** (`whole_under_PARSERONNFTALIAS.out`). Restored, sha256 `9c57fc946261faa8`.
- NFTPARSERUNMOUNTED planted by bytes (hits `[422]`) -> this file **1 failed / 5 passed of 6**, the red = `asymmetry`, `expected [ [ 200, ...(1) ], [ 200, [ '-' ] ] ] to deeply equal ...` (`tamper_NFTPARSERUNMOUNTED.out`); whole suite under it **1 failed / 685 passed** (`whole_under_NFTPARSERUNMOUNTED.out`). Restored, sha256 `9c57fc946261faa8`, `git diff --quiet` rc 0 (`measure_gateway.log`).
- (the golden checker run is appended below after the run)

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts`, then the hunk above exactly as shown (`@@ -83,2 +83,9 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (gateway body-parser mounts, loopback with a fake upstream — allowed). Refs KS-1234. NEVER Closes** — this cell pins an asymmetry the owners have not ruled on; it is rewritten on purpose when they do.
- **From the #1106-#1111 batch gate's NOT-PINNED table** (report `2026-09-21-batch1106-1111-tier1-r1/report.md`, row ALIASUPLOADPARSERASYMMETRY, "a cell question, not a tamper"), **RE-TARGETED** from `/api/documents/upload` (dead through the gateway — 405/415) to `/api/nft/upload`, and given TWO tampers because the row's "cell question" has two plausible unifications.
- **Findings for the owners, NOT pinned here on purpose:** (a) UPLOADROUTEDEAD — `POST /api/documents/upload` through the gateway answers 405 for JSON (spec `/api/documents/{id}` regex, no POST declared, no `/api/documents/upload` path) and 415 for multipart (`enforceJsonContentType`), both spellings; the gateway's own multipart inspector at `proxy.ts:551-617` is unreachable; (b) an HPM-proxied alias reaches the upstream at its ORIGINAL `/api/v1/...` URL (`POST /api/v1/nft/upload` is recorded upstream as `/api/v1/nft/upload` — `:561` rewrites `req.url`, http-proxy-middleware 2.0.10 forwards `req.originalUrl`); the cell therefore asserts the alias hit's TITLE only, not its URL, so it does not lock that behaviour in. The ALIASOTHERROUTES brief recorded the same finding for `/api/v1/timestamps`.
- **Not pinned here, said plainly:** `/api/documents/upload` in any form; the sanitizer's skip (the sibling SECURITYMIDDLEWARESKIP brief); a >1 MB or >10 MB body on either spelling (size limits are not driven).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1234 night/inputs/test_only_1234ALIASUPLOAD-1.json night/briefs/KS-1234-ALIASUPLOAD-1.md tip=362e51fe0db7e73d5557924902763fe3f10fd8c7 ctx=65536
```

## MEASURED — appended after the golden run (artefacts `runs/2026-09-21_gate1106rows-drafter-precheck-b/ALIASUPLOADPARSERASYMMETRY/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md` = the brief's own hunk, fresh `--shared` clone at `362e51fe0`, `gb_clone_5`, farmed by the harness's `prepare_clone.sh`): **RESULT: PASS (8/8)** — T1 one fenced block; T2 touched set == this test file only; T3 strict apply; T4 every `+` line byte-exact; T5 green at the tip 4/4; T6 PARSERONNFTALIAS red set == {asymmetry} and NFTPARSERUNMOUNTED red set == {asymmetry}, each an assertion failure; T7 both controls green under both; T8 `index.ts` restored to sha256 `9c57fc946261` after each. Source tracked-modified count 0 before and after (`prepare.out.log`, `checker.out.log`).
- Wrong variants REFUSED (fresh clone each, `golden_runs.log`): A — one `+` line altered (`['x']`): **FAIL T4**. B — an existing control cell removed with `-` lines: **FAIL T3** (the second hunk I hand-wrote had the wrong line count, so it was refused as a non-applying diff, not by T4's "nothing else of the tip is removed" — recorded as is; it does not prove T4's removal gate). C — the RED cell weakened to assert only that two answers came back, built into its OWN input (`input_variant_C_weak.json`): **FAIL T6 "reds NOTHING (0 of 4 cells failed)"** under BOTH tampers.
