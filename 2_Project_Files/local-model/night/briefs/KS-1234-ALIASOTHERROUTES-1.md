# KS-1234 ALIASOTHERROUTES-1 PIN THAT THE /api/v1 ALIAS OF A proxyPaths ROUTE OTHER THAN documents IS ALSO LEFT UNPARSED — a JSON POST to /api/v1/timestamps reaches the upstream with its body byte-equal (a title the sanitizer would rewrite arrives intact) — the real gateway over loopback with the file's own fake upstream — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 04:20 on 2026-09-21, the #1106-#1111 batch gate's NOT-PINNED row ALIASWIDENINGOTHERROUTES, re-targeted — see Notes)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts`
Tip: `362e51fe0db7e73d5557924902763fe3f10fd8c7`
Runner: `vitest`

Written from develop `362e51fe0db7e73d5557924902763fe3f10fd8c7` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 04:1x on 2026-09-21, read verbs only; the tree that carries the six #1106-#1111 squashes, #1108 = KS-1234 included). The test file at that tip is **94 lines** (blob `3f85887f7268`), read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/api-gateway/src/index.ts` (blob `4e7fc1174d54`, **1279 lines**, read around the parsers): `proxyPaths` at `:400-412` (`'/api/documents'` at `:402`, `'/api/timestamp'` at `:403`), **`shouldParseBody` at `:413`** — the #1108 line, which judges the `/api/v1/` alias by the path the rewrite at `:561` will give it — the conditional `express.json` / `express.urlencoded` at `:416-417`, `sanitizeInput` on parsed bodies at `:458`, the `/api/v1/` -> `/api/` rewrite of `req.url` at `:560-563`, the proxy mount at `:1094`. The proxy (`routes/proxy.ts`) mounts `/api/timestamps` at `:898-901` (`authenticateToken(true)` then `proxy('timestamping', ...)`), and its `onProxyReq` re-streams a PARSED body (`:310-314`, `proxyBodyToWrite`) while an unparsed proxyPaths route pipes the raw stream natively (`:307-309`); `sanitizeInput` (`middleware/security.ts:87-92`) HTML-encodes every string of `req.body` when it is an object — `<` becomes `&lt;` (`:66-73`). This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest ^4.1.9`, `vitest.config.ts` with `globals: true` and `vitest.setup.ts`; no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `index.ts`, `routes/proxy.ts`, `middleware/security.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1234 (#1108) fixed `shouldParseBody` so the `/api/v1/` alias of ANY `proxyPaths` route is judged by its rewritten path and left unparsed — the fix is a regex over the whole `/api/v1/` prefix (`:413`), not over `documents` alone. The #1106-#1111 gate planted ALIASWIDENINGOTHERROUTES — the regex NARROWED to `^/api/v1/documents` — and measured **0 red of 681 at #1108's head**: the file's own red cell drives `/api/v1/documents` only, and its `GET /api/v1/signatories` control carries no body, so the widening to every other alias is unpinned. The gate's proposed cell (`POST /api/v1/signatories` -> 200) does NOT hold at the tip — the gateway has only a `GET /api/signatories` handler (`proxy.ts:670`), so that POST answers **404 `Route POST /api/signatories not found`** with no upstream hit (measured, `ks1234-shared/probe_tip_405_404_bodies.out`); a cell asserting 200 there would be red at the tip, so the row is RE-TARGETED to a proxyPaths alias that IS routed: `POST /api/v1/timestamps` (`proxyPaths` `'/api/timestamp'`, proxied to the timestamping service with the connector key). The observable that separates "parsed" from "unparsed" is the sanitizer: a parsed body passes `sanitizeInput` (`:458`) and is re-streamed encoded (`<b>` -> `&lt;b&gt;`), an unparsed body pipes through byte for byte — measured at the tip over 36 `/api/v1/*` aliases: every proxyPaths alias delivers `<b>ks1234</b>` intact, and under the narrowing tamper every non-documents one delivers `&lt;b&gt;ks1234&lt;/b&gt;` (`ks1234-shared/probe_tip_routes.out` vs `probe_under_413narrow.out`). This change adds ONE cell that sends `POST /api/v1/timestamps` as `application/json` with `{ title: '<b>ks1234</b>', contentHash: 'b' x 64 }` through the file's own `send` (the real gateway over loopback, the file's fake upstream recording `"<METHOD> <url> <title>"`), and asserts `[status, titles]` equals `[200, ['<b>ks1234</b>']]` — the title is the THIRD space-separated field of each recorded hit, so the upstream URL is deliberately NOT pinned (see Notes: an HPM-proxied alias reaches the upstream at its `/api/v1/...` URL today). Every existing cell is unchanged. **It pins TODAY's alias-wide unparsed treatment and decides nothing about KS-1234's remaining questions.**

## The exact change — ONE hunk in the test file

The new cell goes inside the `describe('KS-1234: ...', ...)` block opened at `:84`, directly above its second control (`:88`, `  it('control: the /api/v1 alias itself is live - GET /api/v1/signatories answers 200 and reaches originate at /api/signatories', async () => {`, the ONE trailing context line — it occurs exactly once in the file and is ASCII). There is NO leading context: the line above (`:87`, `  }, 15000);`) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts`.**

```
@@ -88,1 +88,5 @@
+  it('RED KS-1234: POST /api/v1/timestamps as application/json - the alias of a proxyPaths route OTHER than documents - answers 200 and the upstream receives the body unparsed, a title the sanitizer would rewrite arriving byte-equal', async () => {
+    const [status, upstreamHits] = await send('POST', '/api/v1/timestamps', JSON.stringify({ title: '<b>ks1234</b>', contentHash: 'b'.repeat(64) }));
+    expect([status, upstreamHits.map((h) => h.split(' ')[2])]).toEqual([200, ['<b>ks1234</b>']]);
+  }, 15000);
   it('control: the /api/v1 alias itself is live - GET /api/v1/signatories answers 200 and reaches originate at /api/signatories', async () => {
```

`describe`, `it` and `expect` are already imported by the file at `:9`, and `send` (`:74-83`) is the file's own helper (the real gateway on `127.0.0.1:0`, `x-api-key` = the file's `CREATE_KEY`, a 3 s bound) — you add NO import, NO helper and NO constant (the body is built inline; the file's `BODY` at `:22` is deliberately not reused, because its plain `ks1234` title is invisible to the sanitizer). The cell's timeout argument `15000` matches the file's three existing cells. The cell needs no port of its own (the harness's `listen` binds `127.0.0.1:0`, `:30`; nothing connects to a fixed port), no database (`../db` is mocked at `:14-17`) and no real upstream (the fake at `:41-56` answers 200 to any unhandled URL and records the hit).

## Cells

- `otherroute` = `RED KS-1234: POST /api/v1/timestamps as application/json - the alias of a proxyPaths route OTHER than documents - answers 200 and the upstream receives the body unparsed, a title the sanitizer would rewrite arriving byte-equal`

## Red cells

The cell below is a GENUINE assertion-red: it fails under the tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1234: POST /api/v1/timestamps as application/json - the alias of a proxyPaths route OTHER than documents - answers 200 and the upstream receives the body unparsed, a title the sanitizer would rewrite arriving byte-equal

## Tampers

ONE single-line tamper on `index.ts:413` (the #1108 line; it occurs EXACTLY ONCE in the file — `grep -c -F -x`, 1; positive control `grep -c -i shouldparsebody` over the same file: 5 — `:413` the definition and `:416`, `:417`, `:458`, `:459` the four readers). It is the gate's own ALIASWIDENINGOTHERROUTES: the alias regex narrowed to `documents`, so every OTHER proxyPaths alias is parsed again. `From` is the tip's line at that number, byte for byte; `To` is valid TypeScript (a regex literal and a string, the same shape). The checker plants it and restores the file by bytes. The file's existing red cell (`/api/v1/documents`) stays green under it (the narrowed regex still rewrites `documents`), which is exactly why the gate could not see this tamper.

### ALIASNARROWED — the alias rule narrowed to documents, every other proxyPaths alias parsed again
File: `Blockchain/Dev/services/api-gateway/src/index.ts`
Line: 413
From:
```
const shouldParseBody = (req: Request): boolean => !proxyPaths.some(p => req.path.replace(/^\/api\/v1\//, '/api/').startsWith(p)); // KS-1234: judge the /api/v1 alias by the path the rewrite below gives it
```
To:
```
const shouldParseBody = (req: Request): boolean => !proxyPaths.some(p => req.path.replace(/^\/api\/v1\/documents/, '/api/documents').startsWith(p)); // KS-1234: judge the /api/v1 alias by the path the rewrite below gives it
```
Reds: `otherroute`

## Controls

- `control: POST /api/documents as application/json answers 200 and originate receives the body`
- `control: the /api/v1 alias itself is live - GET /api/v1/signatories answers 200 and reaches originate at /api/signatories`
- `🔴 KS-1234: POST /api/v1/documents as application/json answers 200 within the bound and originate receives the same body`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:85`, `:88` and `:91` before this hunk; `:85`, `:92` and `:95` after it — each occurs exactly once in the file and none is a prefix of any other title. The third carries the file's own red glyph; it is a CONTROL NAME for the checker, not a `+` line. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix. The `:85` control proves the loopback harness and the connector-key exchange are live; the `:88` control proves the alias rewrite itself; the `:91` cell is #1108's own pin, green under the tamper because the narrowed regex still covers `documents` — its greenness under ALIASNARROWED is the gate's finding, restated as a control.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: `send` POSTs to `/api/v1/timestamps` with `x-api-key`; `:413` rewrites the path to `/api/timestamps` for the judgement, `'/api/timestamp'` is a `proxyPaths` prefix, so `shouldParseBody` is false and `:416-417` and `:458-459` all `next()` without touching the stream; `:561` rewrites `req.url`; the spec method gate lets `POST` through; the proxy mount validates the key against the fake upstream (`/api/keys/validate`, `:45-49`), exchanges it (`/internal/connector-token`, `:50-53`) and proxies to the fake upstream, piping the raw stream (`req.body` undefined, `proxyBodyToWrite` null); the upstream reads `{"title":"<b>ks1234</b>",...}`, records `POST <url> <b>ks1234</b>` and answers 200. `[status, titles]` is `[200, ['<b>ks1234</b>']]` (measured: 4/4).

Under **ALIASNARROWED** `:413` rewrites only `/api/v1/documents...`, so `/api/v1/timestamps` is judged as itself, matches no prefix, and `shouldParseBody` is true: `express.json` consumes the stream into `req.body`, `sanitizeInput` encodes the title to `&lt;b&gt;ks1234&lt;/b&gt;`, the proxy re-streams the encoded body, the upstream records that title: `[200, ['&lt;b&gt;ks1234&lt;/b&gt;']]` — assertion red (`expected [ Array(2) ] to deeply equal [ 200, [ '<b>ks1234</b>' ] ]`, measured). Every existing cell stays green: the two `documents` cells are still rewritten by the narrowed regex, and the GET control carries no body.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` line.** `index.ts` at `362e51fe0`, line 413 is the `shouldParseBody` line quoted above (no indent, a trailing `// KS-1234:` comment included), byte for byte; it occurs **exactly once** in the file (`grep -c -F -x`, 1). The checker plants and restores it (T8 by sha256 after; tip blob `4e7fc1174d54`, file sha256 `9c57fc946261faa8` measured before the plant and after the restore). `git blame` at the tip: `:413` last touched by `97576e8a5` (#1108, 2026-09-21); `git log` on `index.ts` and on the test file: both `97576e8a5`.
- **Premise: the gate's claim, re-derived and corrected.** The gate's row: tamper `:413` narrowed to `documents`, "MEASURED 0 of 681 at the head", proposed cell `POST /api/v1/signatories` -> `[200, ['POST /api/signatories ks1234']]`. Re-derived at the tip: the whole api-gateway suite is **683** cells here (the gate's 681 was at #1108's own head), and the proposed cell is RED at the tip — `POST /api/signatories` answers 404 (`proxy.ts:670` mounts GET only; the catch-all at `index.ts:1113-1121` answers `Route POST /api/signatories not found`; measured with the same harness). The re-target keeps the gate's tamper and the gate's file and moves the drive to a routed alias.
- **Premise: the anchor.** The test file is **94** lines; `:88` is the second control's `it(` line (2-space indent, ASCII, occurs exactly once) and `:87` is `  }, 15000);`. The trailing context line is non-blank and unique, and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: the loopback harness.** `beforeAll` (`:40-67`) starts the fake upstream on `127.0.0.1:0`, points EVERY `*_SERVICE_URL` at it (`:58-59`, `TIME04:20ING` included), stubs `NODE_ENV=test`, empties `GATEWAY_VOUCH_SECRET`, imports the real `../index` and listens on `127.0.0.1:0`; `afterAll` closes both. `send` (`:74-83`) returns `[status, hits since the mark]`; each hit is `"<METHOD> <url> <title>"` (`:54`, `titleOf` at `:33-35`), so `h.split(' ')[2]` is the title (`<b>ks1234</b>` carries no space). The db is mocked at `:14-17`. No port is fixed; nothing is connected to but the two ephemeral loopback listeners the file itself opens (`lsof -nP -iTCP -sTCP:LISTEN` between runs: no node or vitest listener at all — 0 lines matching either name; the writing seat's first count of 1 was the header's NODE column, caught and corrected).
- **Premise: the observable.** `sanitizeInput` (`security.ts:87-92`) rewrites `req.body` only when it is an object — i.e. only after a parser ran; on an unparsed proxyPaths route `req.body` is undefined and the raw stream pipes natively (`proxy.ts:307-309`). So "title arrives byte-equal" is exactly "the alias was not parsed", and the gate's `<b>ks1234</b>` marker (its SECURITYMIDDLEWARESKIPUNPINNED row) is the right probe body.
- **Premise: `+` lines that also occur at the tip.** One, added by this brief (so T4 accepts it): `  }, 15000);` (`:87`, `:90`, `:93` — the file's own cell close). The other three `+` lines do not occur at the tip. No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick). The title uses `:`, `/`, `,` and `-`, no em dash; `<b>ks1234</b>` appears inside single-quoted strings.
- **Premise: the runner.** `services/api-gateway/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9`, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this cell.
- **Premise: no live-lane collision.** The product file IS the api-gateway `index.ts` (a live-lane name) and the tamper line `:413` is the #1108 line — but the tamper is planted-and-restored by the checker, never raised; the ONE READY naming this test file or `api-gateway/src/index.ts` as a `+++ b/` path is `READY_KS-1234_..._2026-09-20` (the code_patch that MERGED as #1108 and is in this tip — a spent hold). None of the FIFTEEN banked READYs being raised names this test file (their api-gateway files are `ks501-enforcement-non-string-doctype`, `ks480-org-provisioner-gate` and `auth.test.ts`).
- **Premise: the surface.** The real gateway over loopback with the file's fake upstream and mocked db; a connector key validated and exchanged against the fake. No user store, no session, no real JWT key beyond the harness's `__TEST_JWT_PRIVATE_PEM`, no product bytes. GATEWAY body-parsing surface, test-only pin (allowed).

## Collision

**No unmerged hunk on this file anywhere on disk** (the KS-1234 READY merged as #1108). The two sibling rows of the gate on this same file — ALIASUPLOADPARSERASYMMETRY and SECURITYMIDDLEWARESKIPUNPINNED — were measured NOT BRIEFABLE by the writing seat (see the run's report), so this is the ONLY hunk on this file in this round; no permutation to measure. Tamper file `index.ts:413` shared with nobody's raise. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 04:1x-04:2x, `--shared` scratch clone at `362e51fe0`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck/ALIASWIDENINGOTHERROUTES/` and the shared probes under `../ks1234-shared/`)

- Whole api-gateway suite at the bare tip: **70 files, 683/683** (`full_suite_before.out`; the gate's count was 681 at #1108's head). This file with the cell at the tip: **4/4 green**. Whole suite with the cell: **684/684** (`full_suite_after.out`).
- Probe of 36 `/api/v1/*` POST aliases with the `<b>ks1234</b>` body at the tip (`ks1234-shared/probe_tip_routes.out`): every proxyPaths alias that is routed answers 200 with the title byte-equal; `/api/v1/signatories` 404 (no POST route), `/api/v1/documents/upload` and `/api/documents/upload` 405 (the spec gate matches `/api/documents/{id}`, GET only). Under the narrowing tamper (`probe_under_413narrow.out`): every non-documents alias arrives `&lt;b&gt;ks1234&lt;/b&gt;` — 19 of the 36 probe lines differ, all in that one way (the other 17 are the 404/405/403/502 answers and the non-proxyPaths `/api/v1/metering`, parsed at the tip too).
- Tamper planted by bytes: ALIASNARROWED -> this file **1 failed / 3 passed of 4**, the red = `otherroute` (`tamper_ALIASNARROWED.out`); whole 684-cell suite under it **1 failed / 683 passed** — the ONE red is this cell (`whole_under_ALIASNARROWED.out`). `index.ts` restored (`git checkout`, sha256 `9c57fc946261faa8` before and after).
- (the golden checker run is appended below after the run)

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts`, then the hunk above exactly as shown (`@@ -88,1 +88,5 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (gateway body-parsing on the /api/v1 alias, loopback with a fake upstream — allowed; the gate asked for this file). Refs KS-1234. NEVER Closes.**
- **From the #1106-#1111 batch gate's NOT-PINNED table** (report `2026-09-21-batch1106-1111-tier1-r1/report.md`, row ALIASWIDENINGOTHERROUTES), **RE-TARGETED**: the gate's `POST /api/v1/signatories` -> 200 is red at the tip (404 — no POST route at the gateway), so the drive moved to `/api/v1/timestamps`, and the body carries the gate's own `<b>ks1234</b>` marker because a plain body is re-streamed unchanged by the proxy even when parsed (the gate's proposed plain-body cell would NOT red under its own tamper: measured, `probe_under_413narrow.out` shows the difference only in the sanitizer-visible title).
- **Finding for the owners, NOT pinned here on purpose:** an HPM-proxied alias reaches the upstream at its ORIGINAL `/api/v1/...` URL (`POST /api/v1/timestamps` is recorded upstream as `/api/v1/timestamps`, `probe_tip_routes.out`) — the `:561` rewrite changes `req.url` but http-proxy-middleware forwards `req.originalUrl`; only the gateway's own handlers (`verification.ts` for `/api/documents`, the `GET /api/signatories` shim) forward the rewritten path. The cell reads the title field only, so it neither pins nor decides that.
- **Not pinned here, said plainly:** the upload alias (`/api/v1/documents/upload` answers 405 for JSON at the spec gate, same as its twin — the gate's ALIASUPLOADPARSERASYMMETRY row is moot at the tip); the sanitizer skip on unparsed routes (the gate's `:458` tamper is behaviourally inert on this harness — 44 probes identical — so SECURITYMIDDLEWARESKIPUNPINNED is not briefable).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1234 night/inputs/test_only_1234ALIASOTHERROUTES-1.json night/briefs/KS-1234-ALIASOTHERROUTES-1.md ctx=65536
```

## MEASURED — appended after the golden run (artefacts `runs/2026-09-21_gate1106rows-drafter-precheck/ALIASWIDENINGOTHERROUTES/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md` = the brief's own hunk, fresh `--shared` clone at `362e51fe0`, `g1106_clone_4`, farmed by the harness's `prepare_clone.sh`): **RESULT: PASS (8/8)** — T1 one fenced block; T2 touched set == this test file only; T3 strict apply; T4 every `+` line byte-exact; T5 green at the tip 4/4; T6 ALIASNARROWED red set == {otherroute}, an assertion failure; T7 all three controls green; T8 `index.ts` restored to sha256 `9c57fc946261`. Source tracked-modified count 0 before and after (`prepare.log`, `checker.log`).
