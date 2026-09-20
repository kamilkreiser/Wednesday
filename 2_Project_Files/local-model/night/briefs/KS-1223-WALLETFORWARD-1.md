# KS-1223 WALLETFORWARD-1 PIN THAT THE GATEWAY'S HAND-PARSING POST /api/documents FORWARDS AN INBOUND x-wallet-address TO ORIGINATE TODAY — the FORWARD half of the wallet header, driven through the REAL gateway over loopback with a fake originate that records the header (the ks1234 idiom) — Wednesday's task for Ornith, TEST_ONLY, **ONE NEW vitest test file, no product file** (written 04:25 on 2026-09-21, the #1106-#1111 batch gate's NOT-PINNED row WALLETFORWARDUNPINNED)

File: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1223-wallet-forwarded-to-originate.test.ts`
Tip: `362e51fe0db7e73d5557924902763fe3f10fd8c7`
Runner: `vitest`

Written from develop `362e51fe0db7e73d5557924902763fe3f10fd8c7` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 04:2x on 2026-09-21, read verbs only; the tree that carries the six #1106-#1111 squashes, #1111 = KS-1223 WALLET-1 included). The test file does NOT exist at that tip: you CREATE it (`git ls-tree` of `src/__tests__/`: 70 files, none by this name). The product the cells drive is `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` (blob `f888e8cd0bd1`, **1489 lines**, read around the create): `router.post('/api/documents', authenticateToken(true), ...)` at `:1128-1330` — the hand-parsing create (`req.on('data')` / `req.on('end')`, `:1129-1137`), the `// --- No workflow needed: forward to originate service ---` block at `:1283-1320`, `forwardHeaders` built at `:1287-1305` with **`      if (req.headers['x-wallet-address']) forwardHeaders['x-wallet-address'] = req.headers['x-wallet-address'] as string;` at `:1296`** (the ONE place `x-wallet-address` occurs in the file), the forward itself at `:1307-1320`. The harness it copies is `src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts` (94 lines at the tip): the db mock, the fake upstream answering `/api/keys/validate` and `/internal/connector-token`, every `*_SERVICE_URL` pointed at it, the real `../index` on `127.0.0.1:0`. This service runs **VITEST** (`package.json` `"test": "vitest"`, `vitest ^4.1.9`, `vitest.config.ts` with `globals: true` and `vitest.setup.ts`, which provisions `__TEST_JWT_PRIVATE_PEM`; no jest).

## THE MODE — read this twice

**TEST_ONLY, NEW FILE.** Your diff touches EXACTLY ONE file: the new test file above (`--- /dev/null` / `+++ b/<path>`, the path exactly as written above, ONE hunk `@@ -0,0 +1,82 @@`). You never touch `routes/verification.ts`, `index.ts` or any other product file, and you never touch an existing test file: the behaviour is already what it is at the tip, and these cells PIN it.

## What the cells pin (one paragraph)

KS-1223 asks whether a caller-supplied `x-wallet-address` header should decide a document's wallet at all (the merged #1111 WALLET-1 cell pins the gateway's `trustHeaders` half in `ks1041-vouch-header-strip.test.ts`). The #1106-#1111 gate then planted WALLETFORWARDUNPINNED — `verification.ts:1296` deleted, so the gateway's own create no longer copies the inbound header onto the request it forwards to originate — and measured **0 red of 679**: `x-wallet-address` occurs in ONE api-gateway test file (`ks1041-vouch-header-strip`, a unit test of `trustHeaders`, which never drives the create), so the forward is unpinned in either direction. This file drives the REAL gateway over loopback exactly as the ks1234 harness does (db mocked, a fake upstream that validates the connector key and mints the exchange token, the real `../index` imported with every service URL pointed at the fake) and adds ONE recorder: for every `POST /api/documents` the fake upstream receives, it records the `x-wallet-address` header it saw, or `'-'` when none. The RED cell sends a JSON create with `x-wallet-address: addr_client` and asserts `[status, wallets seen]` equals `[200, ['addr_client']]`; the CONTROL sends the same create WITHOUT the header and asserts `[200, ['-']]` — green under the tamper too, proving the loopback create still reaches originate while the RED cell reds on the header alone. **It pins TODAY's forward as a characterisation, not an endorsement**: if the owners decide the wallet must come from the authenticated principal instead, this cell goes red on purpose and is rewritten with that decision.

## The exact change — ONE new file

Copy every line byte for byte. All 82 `+` lines are ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- /dev/null` then `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1223-wallet-forwarded-to-originate.test.ts`.**

```
@@ -0,0 +1,82 @@
+/**
+ * KS-1223 - the FORWARD half of the wallet header: the gateway's hand-parsing POST /api/documents (routes/verification.ts,
+ * the "No workflow needed: forward to originate service" block) copies an inbound x-wallet-address onto the request it
+ * forwards to originate. The #1106-#1111 gate planted that line deleted and measured 0 red of 679: nothing pins the
+ * forward. The REAL gateway is driven over loopback with a fake originate that records the header it receives (the
+ * ks1234 idiom). A characterisation pin of TODAY's forward - whether the wallet should come from the caller's header
+ * at all is KS-1223's question for the owners, not this file's.
+ */
+import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
+import http from 'http';
+import jwt from 'jsonwebtoken';
+import type { AddressInfo } from 'net';
+vi.mock('../db', async (orig) => {
+  const real = (await orig()) as Record<string, unknown>;
+  return { ...real, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }) };
+});
+const PRIV = process.env.__TEST_JWT_PRIVATE_PEM as string;
+const CREATE_KEY = 'sk_ks1223_create_00000001';
+const BODY = JSON.stringify({ title: 'ks1223', contentHash: 'c'.repeat(64) });
+/** Every originate document create: the x-wallet-address header it received, or '-' when none */
+const walletsSeen: string[] = [];
+function readBody(req: http.IncomingMessage): Promise<string> {
+  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
+}
+async function listen(server: http.Server): Promise<string> {
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  return 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+}
+let upstream: http.Server | undefined;
+let gateway: http.Server | undefined;
+let gatewayUrl = '';
+beforeAll(async () => {
+  upstream = http.createServer(async (req, res) => {
+    const body = await readBody(req);
+    const json = (status: number, payload: unknown) => { res.writeHead(status, { 'content-type': 'application/json' }); res.end(JSON.stringify(payload)); };
+    const url = req.url || '';
+    if (url === '/api/keys/validate') {
+      const key = JSON.parse(body || '{}').key as string;
+      if (key === CREATE_KEY) return json(200, { data: { valid: true, connectorId: 'ks1223-create', scopes: ['documents:write'], organizationId: 'org-ks1223', tenantId: 'a0000000-0000-4000-8000-000000000001', rateLimit: 1000, rateLimitWindow: 60 } });
+      return json(200, { data: { valid: false } });
+    }
+    if (url === '/internal/connector-token') {
+      const token = jwt.sign({ userId: 'connector:ks1223-create', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector' }, PRIV, { algorithm: 'RS256', expiresIn: 600 });
+      return json(200, { success: true, data: { token, expiresIn: 600 } });
+    }
+    if (req.method === 'POST' && url === '/api/documents') walletsSeen.push(String(req.headers['x-wallet-address'] ?? '-'));
+    return json(200, { success: true, data: [] });
+  });
+  const upstreamUrl = await listen(upstream);
+  for (const name of ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM',
+    'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET']) vi.stubEnv(name + '_SERVICE_URL', upstreamUrl);
+  vi.stubEnv('NODE_ENV', 'test');
+  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
+  delete process.env.JWT_JWKS_URL;
+  vi.resetModules();
+  const app = (await import('../index')).default;
+  gateway = http.createServer(app as http.RequestListener);
+  gatewayUrl = await listen(gateway);
+}, 60000);
+afterAll(async () => {
+  for (const s of [gateway, upstream]) if (s) { s.closeAllConnections(); await new Promise<void>((r) => s.close(() => r())); }
+  vi.unstubAllEnvs();
+});
+/** POST /api/documents through the real gateway with the given extra headers, 3 s bound; returns [status or 'no-answer', wallets originate saw since the mark] */
+async function create(extra: Record<string, string>): Promise<[number | string, string[]]> {
+  const mark = walletsSeen.length;
+  let status: number | string = 'no-answer';
+  try {
+    const res = await fetch(gatewayUrl + '/api/documents', { method: 'POST', headers: { 'content-type': 'application/json', 'x-api-key': CREATE_KEY, ...extra }, body: BODY, signal: AbortSignal.timeout(3000) });
+    await res.text();
+    status = res.status;
+  } catch { status = 'no-answer'; }
+  return [status, walletsSeen.slice(mark)];
+}
+describe('KS-1223: the gateway forwards an inbound x-wallet-address to originate on POST /api/documents today', () => {
+  it('RED KS-1223: POST /api/documents with x-wallet-address: addr_client answers 200 and originate receives x-wallet-address: addr_client', async () => {
+    expect(await create({ 'x-wallet-address': 'addr_client' })).toEqual([200, ['addr_client']]);
+  }, 15000);
+  it('CONTROL: POST /api/documents without the header answers 200 and originate receives no x-wallet-address', async () => {
+    expect(await create({})).toEqual([200, ['-']]);
+  }, 15000);
+});
```

`vi.mock('../db', ...)` is hoisted by vitest above the imports, so `../index`'s own db import resolves to the factory (the real module spread, `isDbAvailable` true, `query` answering no rows) — byte for byte the ks1234 harness's mock. `jwt` (`jsonwebtoken`) and `__TEST_JWT_PRIVATE_PEM` are what that harness uses to mint the exchange token (`vitest.setup.ts` provisions the pair and `JWT_PUBLIC_KEY`). `listen` binds `127.0.0.1:0` twice (the fake upstream, then the real gateway); nothing connects to a fixed port. `create` mirrors the harness's `send` (a 3 s `AbortSignal.timeout`, `x-api-key` = the file's own `CREATE_KEY`, which the fake upstream validates with `documents:write`), spreading the cell's extra headers over the fixed ones. The cells need no database, no real upstream, no key file and no product bytes.

## Cells

- `forwarded` = `RED KS-1223: POST /api/documents with x-wallet-address: addr_client answers 200 and originate receives x-wallet-address: addr_client`
- `control` = `CONTROL: POST /api/documents without the header answers 200 and originate receives no x-wallet-address`

## Red cells

The cell below is a GENUINE assertion-red: it fails under the tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1223: POST /api/documents with x-wallet-address: addr_client answers 200 and originate receives x-wallet-address: addr_client

## Tampers

One single-line tamper on `verification.ts:1296` (the ONE `x-wallet-address` line in the file — `grep -c -F -x`, 1; `grep -c -i 'x-wallet-address'` over the same file: 1, this line; positive control `grep -c -i forwardheaders` over the same file: 11). It is the gate's own WALLETFORWARDUNPINNED — "the line deleted" — expressed as the harness's one-line From/To requires: the statement replaced by a comment, so the header is never copied and the file still parses (a comment is valid TypeScript; measured: the file loads and runs 2 cells under it). `From` is the tip's line at that number, byte for byte. The checker plants it and restores the file by bytes.

### WALLETNOTFORWARDED — the inbound x-wallet-address is no longer copied onto the originate request
File: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts`
Line: 1296
From:
```
      if (req.headers['x-wallet-address']) forwardHeaders['x-wallet-address'] = req.headers['x-wallet-address'] as string;
```
To:
```
      // KS-1223 tamper: the inbound x-wallet-address is NOT forwarded to originate
```
Reds: `forwarded`

## Controls

- `CONTROL: POST /api/documents without the header answers 200 and originate receives no x-wallet-address`

*(The FULL `it(...)` title of the file's second cell, byte for byte. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix; no title is a prefix of another. Under the tamper the control's create carries no wallet header, so originate records `'-'` exactly as at the tip — the control proves the loopback create, the key validation, the exchange and the forward all still run while the RED cell reds on the one header.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip both cells pass: `beforeAll` starts the fake upstream and the real gateway; the RED cell POSTs `/api/documents` as `application/json` with `x-api-key` and `x-wallet-address: addr_client`; `shouldParseBody` leaves the stream alone (`'/api/documents'` is a proxyPaths prefix), `authenticateToken(true)` validates the key against the fake (`/api/keys/validate`) and exchanges it (`/internal/connector-token`), the hand-parsing create reads the body, finds no workflow, builds `forwardHeaders` — `:1296` copies `addr_client` — and forwards to the fake upstream at `/api/documents`, which records `'addr_client'` and answers 200; the gateway relays 200. `[200, ['addr_client']]` (measured). The CONTROL's create carries no wallet header, `:1296`'s guard is false, the fake records `'-'`: `[200, ['-']]` (measured).

Under **WALLETNOTFORWARDED** `:1296` is a comment: the RED cell's create still forwards and answers 200, but the fake records `'-'` — `expected [ 200, [ '-' ] ] to deeply equal [ 200, [ 'addr_client' ] ]`, an assertion red (measured). The CONTROL is unchanged (measured). No other file in the suite drives this create with the header (measured: whole suite under the tamper, 1 red of 686 — this cell).

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From line.** `verification.ts` at `362e51fe0`, line 1296 is `      if (req.headers['x-wallet-address']) forwardHeaders['x-wallet-address'] = req.headers['x-wallet-address'] as string;` (6-space indent), byte for byte; it occurs **exactly once** (`grep -c -F -x`, 1) and is the only `x-wallet-address` in the file. The checker plants and restores it (T8 by sha256 after; tip blob `f888e8cd0bd1`, file sha256 `43d29242eda12cdd` measured before the plant and after the restore). `git blame` at the tip: `:1296` last touched by `29033ce47` (2026-03-22); `git log` on the file: last change `34cdcfb26` (#1035, KS-1204).
- **Premise: the gate's claim, re-derived.** The gate's row: "MEASURED 0 of 679 at the head ... `ks1041-vouch-header-strip.test.ts` is the wrong file (unit-level); a loopback cell in a NEW `ks1223-wallet-forwarded-to-originate.test.ts` built on the ks1234 harness". Re-read at the tip: `git grep -l x-wallet-address` over `api-gateway/src/__tests__`: ONE file, `ks1041-vouch-header-strip.test.ts` (it drives `trustHeaders`, never the create). The whole api-gateway suite is 683 cells at this tip (the gate's 679 was at #1111's head).
- **Premise: the harness copy is complete.** The file-scope declarations mirror the ks1234 harness one for one: the `../db` mock (`:14-17` there), `PRIV`, the connector key and body, `readBody`, `listen`, the three `let`s, `beforeAll` with the fake upstream's two special URLs and the seventeen `*_SERVICE_URL` stubs (`:58-59` there), `NODE_ENV=test`, `GATEWAY_VOUCH_SECRET=''`, `JWT_JWKS_URL` deleted, `vi.resetModules()` then the real import; `afterAll` closing both servers and unstubbing. What differs: `hits`/`titleOf` are replaced by `walletsSeen` and a recorder keyed on `POST /api/documents`, and `send` is replaced by `create(extra)`.
- **Premise: new file.** The path is absent at the tip, so the input's `test_mode` is `new` and the headers are `--- /dev/null` / `+++ b/<path>`. No `-` line anywhere.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick — every URL is built with `+`). **No blank line** (0, counted). The doc comment's double quotes (`"No workflow needed: ..."`) sit inside a `/** */` block.
- **Premise: the runner.** `services/api-gateway/package.json` at the tip has `"test": "vitest"` and `vitest ^4.1.9`, no `jest` / `ts-jest` — the builder auto-detects vitest and the `Runner:` line above agrees with it. The checker runs `npx vitest run src/__tests__/ks1223-wallet-forwarded-to-originate.test.ts` from `Blockchain/Dev/services/api-gateway`. `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this file.
- **Premise: ports.** Never connected to from outside: the file's own two listeners bind `127.0.0.1:0` and are closed in `afterAll`; `lsof -nP -iTCP -sTCP:LISTEN` between runs shows no node or vitest listener. The db is mocked. The rate limiter logs a `DEGRADED — redis-not-ready` warning once per run (in-memory counting; the harness has always done this) — a log line, not a failure.
- **Premise: no live-lane collision.** NEW file, so no hunk overlap with anything is possible. The product file `routes/verification.ts` is named as a `+++ b/` path by five OLD READYs (`KS-1072`, `KS-1073`, `KS-1087` of 09-15, `KS-1118-F3a`, `KS-1185-F1` of 09-17 — product fixes, none among the FIFTEEN banked being raised); this brief raises no product bytes and its tamper is planted-and-restored by the checker, so none of them is touched or sequenced. None of the fifteen banked READYs names this test file or `verification.ts`.
- **Premise: the surface.** The real gateway over loopback with a fake upstream and mocked db; a connector key validated and exchanged against the fake; one caller-supplied header observed on the forward. No user store, no session, no real JWT key beyond the harness's test pair, no product bytes. GATEWAY forward surface, test-only pin (allowed).

## Collision

**NEW file — no hunk overlap is possible with anything.** The sibling brief of this round on the api-gateway (`KS-1234-ALIASOTHERROUTES-1`) modifies `ks1234-v1-documents-json-create-never-answers.test.ts`, a different file, and plants `index.ts:413`; this brief plants `verification.ts:1296` — no shared line, no shared file. Both applied together on the tip: 71 files, **686/686** (`full_suite_after.out`). Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 04:2x, `--shared` scratch clone at `362e51fe0`, node_modules farmed from the source checkout via the harness's `prepare_clone.sh`, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_gate1106rows-drafter-precheck/WALLETFORWARDUNPINNED/`)

- This file at the tip: **2/2 green** (`file_tip.out`). Whole api-gateway suite at the bare tip: 70 files, **683/683** (`../ALIASWIDENINGOTHERROUTES/full_suite_before.out`); with this file AND the sibling ks1234 cell: 71 files, **686/686** (`full_suite_after.out`).
- Tamper planted by bytes: WALLETNOTFORWARDED -> this file **1 failed / 1 passed of 2**, the red = `forwarded` (`AssertionError: expected [ 200, [ '-' ] ] to deeply equal [ 200, [ 'addr_client' ] ]`, `tamper_WALLETNOTFORWARDED.out`); whole 686-cell suite under it **1 failed / 685 passed** — the ONE red is this cell (`whole_under_WALLETNOTFORWARDED.out`). `verification.ts` restored (`git checkout`, sha256 `43d29242eda12cdd` before and after).
- (the golden checker run is appended below after the run)

## Output

Exactly ONE ```diff block, nothing outside it: `--- /dev/null` / `+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1223-wallet-forwarded-to-originate.test.ts`, then the ONE hunk above exactly as shown (`@@ -0,0 +1,82 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes, new file. **Raise tier: TIER 1 at the gate (gateway create forward, loopback with a fake upstream — allowed; the gate asked for this file by name). Refs KS-1223** (and KS-1041 for the harness's vouch-secret stub). **NEVER Closes** — KS-1223's question (the wallet's source of truth) is the owners'; this cell pins today's forward and will be rewritten on purpose if they change it.
- **From the #1106-#1111 batch gate's NOT-PINNED table** (report `2026-09-21-batch1106-1111-tier1-r1/report.md`, row WALLETFORWARDUNPINNED; its tamper "the line deleted" is WALLETNOTFORWARDED here, as a comment line, planted and measured).
- **Not pinned here, said plainly:** originate's use of the header (the fake upstream answers 200 to anything); the referral service's own header fallback (the gate's REFERRALFALLBACKUNPINNED row, a different service); the `trustHeaders` half (the merged #1111 cell).
- **Size, said plainly:** 82 `+` lines — the largest new file briefed for Ornith so far (the passed T12/T13 files are 43); the harness is copied rather than imported because the ks1234 file exports nothing. If the model slips on a line, T4 names it.

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1223 night/inputs/test_only_1223WALLETFORWARD-1.json night/briefs/KS-1223-WALLETFORWARD-1.md ctx=65536
```

## MEASURED — appended after the golden run (artefacts `runs/2026-09-21_gate1106rows-drafter-precheck/WALLETFORWARDUNPINNED/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md` = the brief's own file, fresh `--shared` clone at `362e51fe0`, `g1106_clone_5`, farmed by the harness's `prepare_clone.sh`): **RESULT: PASS (8/8)** — T1 one fenced block; T2 touched set == the new file only; T3 strict apply of the `--- /dev/null` diff; T4 every `+` line byte-exact; T5 green at the tip 2/2; T6 WALLETNOTFORWARDED red set == {forwarded}, an assertion failure; T7 the control green; T8 `verification.ts` restored to sha256 `43d29242eda1`. Source tracked-modified count 0 before and after (`prepare.log`, `checker.log`).
