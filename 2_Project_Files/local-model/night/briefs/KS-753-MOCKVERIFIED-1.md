# KS-753 MOCKVERIFIED-1 PIN THAT POST /api/timestamps AND /api/timestamps/batch ANSWER 201 WITH verified:true FOR THE MOCK TSA FALLBACK (no TSA reachable) — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 2026-09-21, widened sweep — KS-753 judged)

File: `Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts`
Tip: `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa`
Runner: `vitest`

Written from develop `dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` on 2026-09-21, read verbs only; the #1101 merge). The test file at that tip is **122 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/timestamping/src/index.ts` (**884 lines**, read whole): `createTimestamp` at `:437-550`, the `rfc3161` branch at `:458-477` (the TSA module's mock fallback lands as `tsaResult.token` with `eidasQualified:false` and a `(mock)`-suffixed `tsaName`, `:466-471`), and the line the cell pins at `:516` (`    verified: true, // Mock timestamps are pre-verified` — unconditional, for every timestamp type). This service runs **VITEST** (`package.json` `"test": "vitest run"`, `vitest ^4.1.11`, no jest).

**What this brief does NOT decide.** KS-753's open design question — refuse the write (503, as `requireEidas` does today) or persist it with `verified: false` per entry — is Kam's ruling, not this cell's. The cell pins ONLY what is true at the tip: with no TSA reachable, both create routes answer 201 and report the mock token as `verified: true`. When the ruling lands (either shape), this cell goes red on purpose and gets rewritten to the ruled answer; until then it makes the defect visible to the suite instead of invisible. The cell is a TEST-ONLY pin of TODAY's behaviour; it takes no part of the fix and closes nothing.

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `index.ts`, `qualified-tsa.ts`, `db.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-753 reports (Peter, re-measuring KS-740 against a working TSA: 6 of 360 requests fell back, each 201 / `verified: true`) that `POST /api/timestamps` and `POST /api/timestamps/batch` return 201 with `verified: true` when the RFC-3161 call fails and the code falls back to the locally generated mock token. The mock is honestly labelled everywhere else (`eidasQualified: false`, `tsaName: "... (mock)"`, `"mock": true` inside the token) — only `verified` at `index.ts:516` does not carry the signal, because it is the literal `true`. The suite pins none of it: `verified` occurs in **0** test files of the service, and no test drives either create route (the only test importing `../index` is this file, for `mapWithConcurrency`). This change adds ONE cell to this file that stubs `fetch` to fail (the file's own `vi.stubGlobal('fetch', ...)` shape at `:92` / `:107`, so the REAL `qualified-tsa` module takes its REAL mock fallback), mocks the service's own `../db` so the INSERT resolves (the `vi.doMock` + `vi.resetModules()` + `await import(...)` idiom the file already uses at `:84-98`), mints a throwaway RS256 keypair so the REAL `@secuura/shared` `authenticate()` on `/api` verifies a real bearer (no auth mock: `JWT_PUBLIC_KEY` is read lazily as a base64 SPKI PEM), imports the REAL app (`export default app`, `index.ts:884`) with `PORT=0` so its `app.listen` binds an ephemeral port instead of colliding with the file's top-level import on 4006, and drives BOTH routes IN PROCESS as `app(req, res, next)` with a fake req/res (no HTTP client, no port touched, no database). It asserts, for the single response and both batch entries, `[eidasQualified, decodedProof.mock, verified]` equals `[false, true, true]` beside status 201 — `eidasQualified:false` and `mock:true` are the liveness elements (they prove the answer IS the fallback path), `verified:true` is the pinned defect. Every existing cell is unchanged.

## The exact change — ONE hunk in the test file

The new cell goes at the end of the `describe('KS-740 — the TSA request carries a deadline', ...)` block opened at `:82` (its `afterEach` at `:83-86` runs `vi.unstubAllGlobals()` and `vi.resetModules()` after the new cell too — the file's own hygiene), directly above that block's closing line `});` (`:122`, the file's LAST line and the ONE trailing context line). There is NO leading context: the line above (`:121`, `  });`) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts` then `+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts`.**

```
@@ -122,1 +122,32 @@
+  it('RED KS-753: POST /api/timestamps and /api/timestamps/batch answer 201 with verified true for the mock TSA fallback when no TSA is reachable - the mock is reported as verified today', async () => {
+    vi.stubGlobal('fetch', async () => ({ ok: false, status: 503, statusText: 'unavailable' } as Response));
+    const nodeCrypto = await import('crypto');
+    const { privateKey, publicKey } = nodeCrypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+    const b64url = (s: string | Buffer) => Buffer.from(s).toString('base64url');
+    const signingInput = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' })) + '.' + b64url(JSON.stringify({ userId: 'u-ks753', email: 'ks753@secuura.io', role: 'user', verificationLevel: 'email', exp: Math.floor(Date.now() / 1000) + 300 }));
+    const bearer = 'Bearer ' + signingInput + '.' + b64url(nodeCrypto.sign('sha256', Buffer.from(signingInput), privateKey));
+    const savedEnv = { JWT_PUBLIC_KEY: process.env.JWT_PUBLIC_KEY, PORT: process.env.PORT };
+    process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
+    process.env.PORT = '0';
+    vi.doMock('../db', () => ({ initDb: async () => false, isDbAvailable: () => false, query: async () => ({ rows: [], rowCount: 0 }), closeDb: async () => undefined }));
+    vi.resetModules();
+    const { default: app } = await import('../index');
+    const drive = (url: string, body: unknown) => new Promise<any>((resolve) => {
+      const headers: Record<string, unknown> = {};
+      const req: any = { method: 'POST', url, headers: { authorization: bearer }, body };
+      const res: any = { statusCode: 200, locals: {}, on: () => res, status: (c: number) => { res.statusCode = c; return res; }, json: (b: unknown) => { resolve({ status: res.statusCode, body: b }); return res; } };
+      res.send = res.json;
+      res.end = () => res.json(null);
+      res.setHeader = (k: string, v: unknown) => { headers[k.toLowerCase()] = v; return res; };
+      res.getHeader = (k: string) => headers[k.toLowerCase()];
+      res.removeHeader = (k: string) => { delete headers[k.toLowerCase()]; };
+      app(req, res, () => resolve({ status: -1, body: null }));
+    });
+    const single = await drive('/api/timestamps', { hash: 'a'.repeat(64), timestampType: 'rfc3161' });
+    const batch = await drive('/api/timestamps/batch', { hashes: [{ hash: 'b'.repeat(64) }, { hash: 'c'.repeat(64) }], timestampType: 'rfc3161' });
+    for (const k of ['JWT_PUBLIC_KEY', 'PORT'] as const) { if (savedEnv[k] === undefined) delete process.env[k]; else process.env[k] = savedEnv[k]; }
+    const shape = (t: any) => [t.eidasQualified, JSON.parse(Buffer.from(t.proof, 'base64').toString()).mock, t.verified];
+    expect([single.status, single.body.error, batch.status, batch.body.error]).toEqual([201, undefined, 201, undefined]);
+    expect([shape(single.body.data), batch.body.data.timestamps.map(shape)]).toEqual([[false, true, true], [[false, true, true], [false, true, true]]]);
+  });
 });
```

`describe`, `expect`, `it`, `vi` and `afterEach` are already imported by the file at `:14` — you add NO import. Node's `crypto` is loaded by the dynamic `await import('crypto')` INSIDE the cell and the app by `await import('../index')` INSIDE the cell (the file's top-level imports are untouched; `:98` and `:113` already use the same `await import(...)` idiom). The cell needs no HTTP client, no port of its own, no database and no TSA: `fetch` is stubbed exactly as `:92-96` stubs it, `../db` is a four-function stand-in for the service's own module, and the app is called as a function with a fake req/res.

## Cells

- `mockverified` = `RED KS-753: POST /api/timestamps and /api/timestamps/batch answer 201 with verified true for the mock TSA fallback when no TSA is reachable - the mock is reported as verified today`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-753: POST /api/timestamps and /api/timestamps/batch answer 201 with verified true for the mock TSA fallback when no TSA is reachable - the mock is reported as verified today

## Tampers

Two single-line tampers on the SAME line of `index.ts` (`:516`, which occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1; the other three `verified: true,` lines at `:573`, `:603`, `:612` are the verify path, different bytes, different indent). They are the two shapes the ticket's fix can take at this line: carry the qualification signal (the ticket's "fix shape 1"), or read the `(mock)` label the TSA module already puts on the name. Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript (`eidasQualified` is the `let` at `:453`, `tsaName` the `let` at `:454`, both in scope at `:516`), so nothing fails to load and no cell reds for the wrong reason.

### VERIFIEDEQEIDAS — verified carries the qualification signal: a mock fallback is not verified
File: `Blockchain/Dev/services/timestamping/src/index.ts`
Line: 516
From:
```
    verified: true, // Mock timestamps are pre-verified
```
To:
```
    verified: eidasQualified, // KS-753: only a qualified token is reported as verified
```
Reds: `mockverified`

### VERIFIEDNOTMOCK — verified reads the (mock) label the TSA module already puts on the name
File: `Blockchain/Dev/services/timestamping/src/index.ts`
Line: 516
From:
```
    verified: true, // Mock timestamps are pre-verified
```
To:
```
    verified: !(tsaName || '').endsWith('(mock)'), // KS-753: a mock-labelled token is not verified
```
Reds: `mockverified`

## Controls

- `never exceeds the limit, and that is measured at the peak, not inferred`
- `reports a timeout AS a timeout, not as a generic failure`

*(Both are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:19` and `:106` — each occurs exactly once in the file and neither is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; the prefix rule in `build_test_only_input.sh`'s header is for BASH suites only. The file's other five cells (`:42`, `:53`, `:68`, `:77`, `:88`) are also green under both tampers but are left undeclared. The `:106` control is the liveness proof for the idiom the new cell rides: it stubs `fetch` and dynamic-imports a product module after `vi.resetModules()`, in the same `describe` as the new cell.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: the fresh `../index` import (with `../db` mocked and `PORT=0`) builds the real app; for each POST the fake req carries a bearer the REAL `authenticate()` verifies against the base64 SPKI PEM in `JWT_PUBLIC_KEY` (no `JWT_JWKS_URL` / `AUTH_SERVICE_URL` means the static-key path; if either were set, the stubbed `fetch` answers `ok:false` and `resolveVerifyKey` falls back to the static key anyway); `helmet`, `cors`, `express.json()` (the fake req has no `content-length`, so the parser leaves the preset `body` alone), `rejectNulBytes()` and the request logger pass through on the fake res's own `setHeader` / `getHeader` / `removeHeader` / `on`; the route parses the body through the shipped zod schema, `createTimestamp` calls the REAL `qualified-tsa.createTimestamp`, whose `rfc3161Request` hits the stubbed `fetch` (`ok:false` → `success:false`) and falls back to the mock token (`mock:true` inside, `eidasQualified:false`, `tsaName` ending `(mock)`); `index.ts:466-471` carries the signal, `:516` writes `verified: true`, `ensureTable()` returns at once (`isDbAvailable()` is false), the INSERT hits the mocked `query`, and the route answers `201` with `formatTimestampResponse(...)`. The batch route does the same for two hashes through `mapWithConcurrency`. `shape(...)` reads `[false, true, true]` for all three, beside two `201`s — exactly what the cell asserts.

Under **VERIFIEDEQEIDAS** `verified` is `eidasQualified`, which the fallback sets `false`: `shape` reads `[false, true, false]` for all three — assertion red. Under **VERIFIEDNOTMOCK** the `tsaName` ends with `(mock)`, so `verified` is `false` — the same `[false, true, false]` — assertion red. Under BOTH, every existing cell stays green: `:19-79` exercise `mapWithConcurrency` alone, `:88-121` exercise `rfc3161-client` alone; none reaches `createTimestamp` or `:516`.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the `From` line.** `index.ts` at `dc061f2bb`, line 516 is `    verified: true, // Mock timestamps are pre-verified`, byte for byte; it occurs **exactly once** in the file (`grep -c -F -x`, 1; positive control `verified: true` matches 4 lines: 516, 573, 603, 612). Both tampers name the same line: the checker plants and restores them one at a time (T8 by sha256 after each).
- **Premise: the ticket's claim, re-derived.** `qualified-tsa.ts:305-328`: the fallback returns `success:true` with a base64 JSON `token` carrying `mock: true`, `eidasQualified: false` and `tsaName: "<provider> (mock)"`. `index.ts:466-471` carries `eidasQualified` and `tsaName` from it; `:516` is the literal `true`. So a fallback answer is `eidasQualified:false` + `verified:true` — the contradiction the ticket names.
- **Premise: the anchor.** The test file is **122** lines; `:122` is `});` (column 0, the file's last line, one of exactly TWO column-0 `});` lines — the other closes the first `describe` at `:80` — so the hunk header's line number, not the bytes alone, places the insertion) and `:121` is `  });`. The trailing context line is non-blank and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: nothing pins this today.** `KS-753`, `verified`, `/api/timestamps` and `createTimestamp` occur **0** times in the service's test files at the tip (`git grep` over `src/__tests__`; the one `/api/timestamps/batch` hit is a doc comment in `ks611-batch-strict.test.ts:2`, which parses schemas only). The only test that imports `../index` is this file (`:16`, for `mapWithConcurrency`).
- **Premise: the in-process app call.** `index.ts:884` is `export default app`; an express app is callable as `app(req, res, next)`. The file's top-level `import { mapWithConcurrency } from '../index'` (`:16`) already executes `index.ts` — including `app.listen(4006)` — in the vitest worker at the tip; the cell's second, fresh import binds `PORT=0` (Node treats the string `'0'` as port 0 = ephemeral) so the two instances never collide. `dotenv.config()` never overrides a variable that is already set, so `PORT=0` and `JWT_PUBLIC_KEY` survive it.
- **Premise: the auth gate is REAL, not mocked.** `packages/shared/src/crypto/jwks.ts:80-88` decodes `JWT_PUBLIC_KEY` from base64 to PEM lazily per verification; `registry.ts:116-121` accepts `RS256` by default (`JWT_ACCEPTED_ALGS` unset). The bearer is a hand-built compact JWT (`RS256` header, 300 s `exp`) signed with Node's `crypto.sign('sha256', ...)` over the signing input — PKCS#1 v1.5 = RS256, what `jsonwebtoken` verifies. No `jsonwebtoken` import in the test (it is not a dependency of this service).
- **Premise: the db stand-in.** `index.ts:19` imports exactly `initDb`, `isDbAvailable`, `query`, `closeDb` from `./db`; the stand-in provides all four. `createTimestamp` calls `query(INSERT ...)` unconditionally (`:525`), so without the stand-in the route 500s (`getPool()` throws with no `DATABASE_URL`) and no 201 exists to pin. `db.ts` also runs a `require('@secuura/shared')` at load — not reached, the module is replaced whole.
- **Premise: no `+` line re-adds a tip line.** The only `+` line that also occurs at the tip is the closing `  });` (unavoidable for a new cell).
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). The title uses `-`, not an em dash.
- **Premise: the runner.** `timestamping/package.json` at the tip has `"test": "vitest run"` and `vitest ^4.1.11` in devDependencies, with no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this cell's loose `any`s. `vitest.config.ts` sets `globals: true`, `environment: 'node'`.
- **Premise: no live-lane collision.** `index.ts` here is the TIMESTAMPING service's entry, not the api-gateway's; it is not `enforcement.ts`, `startup-migrations.ts` or `trustHeaders.ts`, and is not under `services/anchoring/**`. Neither held `READY_*` that mentions "timestamping" (`READY_KS-1090-R2-3…`, `READY_KS-1234…`) touches `services/timestamping/**` (both are api-gateway files, the word appears in a service-name list). `git log` on `index.ts` at the tip: last change #787 (KS-740, 2026-09-02); on the test file: #787 too. No brief in `night/briefs/` names `ks740-bounded-fanout`.
- **Premise: the surface.** The cell mints a throwaway keypair in-process, sets and RESTORES two env vars, mocks the service's own db module, and drives two POSTs through the real middleware chain. No user, no session, no MFA state, no product bytes, no network (fetch is stubbed before the app is imported).

## Collision

None on the product line. `index.ts:516` has not moved since #787 (2026-09-02). Sequencing needed: none. KS-753 itself is in Backlog, assigned to `kamil.kreiser@secuura.ai`, 0 comments — nobody is working the product fix at the tip.

## MEASURED by the writing seat (2026-09-21, `--shared` scratch clone at `dc061f2bb`, node_modules farmed from the source checkout, source tracked-modified count 0 before and after)

- REAL `tasks/test_only/checker.sh` on this brief's own diff: **RESULT: PASS (8/8)**, `apply=strict` (header counts right: 31 `+` and 1 context = 32). T5 green at the tip 8/8 cells in the file; T6 VERIFIEDEQEIDAS reds exactly `mockverified`, T6 VERIFIEDNOTMOCK reds exactly `mockverified`, every red an assertion failure — both read `AssertionError: expected [ [ false, true, false ], ... ] to deeply equal [ [ false, true, true ], ... ]` (the `verified` element alone flips, single and both batch entries); T7 both controls green under both; T8 `index.ts` restored by bytes (sha256 e4f525efcb43 == tip blob) after each.
- The path is REAL, not a mock echo: with the console intercept off, one run of the file prints `[TSA] RFC-3161 request failed {"error":"TSA returned HTTP 503: unavailable"}` and `[TSA] Falling back to mock timestamp token` **3 times** (1 single + 2 batch), `Timestamp created` once, `Batch timestamps created","count":2` once, and TWO `Timestamping Service started` lines — `"port":4006` (the file's top-level import at `:16`, tip behaviour) and `"port":"0"` (the cell's fresh import). No `EADDRINUSE`, no unhandled error. `lsof -nP -iTCP:4006 -sTCP:LISTEN` on the measuring machine: nothing listening (so the tip's own 4006 bind is free here; a live timestamping container on 4006 would break the FILE at the tip, before this cell — pre-existing, not introduced).
- The auth gate is REAL (scratch-only sanity, not in the brief): the same cell with the bearer's signature replaced by `b64url('not-a-signature')` never reaches the route (`body.data` undefined) — 1 failed, 7 passed. That run is also why the final assertion is split in two: status + `body.error` first, so a non-201 reads as an assertion with the error code, not a TypeError.
- Three WRONG variants refused at the named gates: a control declared as the PREFIX `reports a timeout AS a timeout` -> **FAIL T5** `DECLARED CELL NOT IN THE RUN`; the first tamper at `Line: 515` (off by one) -> **builder REFUSED rc 2** naming the tip's `:515` (`    transactionHash,`); a weakened cell whose `shape` ignores `t.verified` -> **FAIL T6** `reds NOTHING (0 of 8 cells failed)` under both tampers.
- Whole timestamping vitest suite: bare tip **5 files, 42/42 green**; with the cell applied **43/43** (+1 = this cell; ks740 file 7 -> 8 cells). `tsc` not run: `tsconfig.json` excludes `src/__tests__`.
- Input key set identical to `night/inputs/test_only_1232INFOEMPTY-1.json` (both directions empty). Source checkout tracked-modified count 0 before prepare, after prepare, after every checker run.
- Artefacts: `local-model/runs/2026-09-21_ks753-drafter-precheck/` (build.log, prepare.log, checker.log, out.md, out.md.checker/, direct_tip*.out/json, sanity_badbearer/, var1/, var2/, var3/, full_suite_tip.json, full_suite.json).
- NOT measured: the persisted row's `verified` column (db is a stand-in), the GET read-back, the `requireEidas: true` 503 control, `opentimestamps` / `blockchain`; no live stack was booted and no port was touched by any shell instrument (the cell calls the app as a function; the ephemeral bind is the app's own `listen`, inside the vitest worker).

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts` / `+++ b/Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts`, then the hunk above exactly as shown (`@@ -122,1 +122,32 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2. Refs KS-753** (and KS-523, whose fail-closed path this cell walks past; KS-740, where Peter found it). **NEVER Closes** — KS-753 is an open design question for Kam (503 vs `verified:false`); this brief takes no part of that decision and pins TODAY's answer so the ruling arrives as a deliberate red, not a silent change.
- **Not from a gate cell.** Found by the 2026-09-20 widened test-only sweep; queue.md's header line for KS-753 (`timestamping mock-TSA fallback — open design question (503 vs verified:false), 2 files`) describes the PRODUCT ticket; this brief is a pin only.
- **Not pinned here, said plainly:** the persisted row (`ts_timestamps.verified`, `index.ts:539`) — the db is a stand-in, so the INSERT's `$10` is not asserted; the GET read-back; the `requireEidas: true` 503 control (KS-523's own suite would own it); `opentimestamps` / `blockchain` (mock by design, the ticket says they keep today's semantics).
- **Collision: none** (measured above).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-753 night/inputs/test_only_753MOCKVERIFIED-1.json night/briefs/KS-753-MOCKVERIFIED-1.md ctx=65536
```
