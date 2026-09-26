# KS-1341-A WEBHOOKS500-A — add the fail500 helper to routes/webhooks.ts and route GET / and POST / 500s through it

File: `Blockchain/Dev/services/originate/src/routes/webhooks.ts`  (product, modified in place)
Test file: `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts`  (NEW)
Tip: `e080174c86c671349c508560744644fc0ef33388` (origin develop, `git ls-remote origin refs/heads/develop`, re-read at 2026-09-26 15:03:13 AEST)
Runner: `jest` (ts-jest 29, `Blockchain/Dev/services/originate/package.json` `"test": "jest"`)

Written 2026-09-26 15:03:36 AEST (shell `date`) from `e080174c86c671349c508560744644fc0ef33388`, `webhooks.ts` read WHOLE (549 lines, ends with one `\n`, blob sha1 of `git show` output `c86b6344664f41bd6b12f4e7dc74aa37c76a52dd`, last changed at `408821134` KS-1160 #1186). **Brief A of 3 — FIRST of three (A → B → C). B and C both call the helper this brief adds.**

## The mode — read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `Blockchain/Dev/services/originate/src/routes/webhooks.ts` — modified in place, `--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts` / `+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts`, EXACTLY the 3 hunk(s) given in `## The exact change`, byte for byte.
2. `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` — a NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts`, ONE hunk `@@ -0,0 +1,173 @@`, every line `+`, the text given in `## The test` byte for byte (173 lines).

You never touch any other file. In particular you do NOT edit any existing test, `routes/gdpr.ts`, `routes/systemErrors.ts`, `routes/adminConfig.ts`, `utils/pgErrors.ts`, `utils/logger.ts` or `__tests__/helpers/sharedModuleMock.ts`. Apply at the tip above. Nothing precedes this brief. The checker applies the TEST FILE ALONE first (every 🔴 cell must FAIL by assertion, every 🟢 control must PASS), then your product hunks on top (every cell must PASS).

## What is wrong (one paragraph)

`routes/webhooks.ts` (mounted at `/api/webhooks`) has seven catch blocks whose 500 answer is the byte-identical line `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });` at `:200, :267, :325, :337, :352, :391, :416` — with NO `NODE_ENV` guard, so the thrown error's own text reaches the client in every environment, production included. The 2026-09-26 QA gate MEASURED it under `NODE_ENV=production` (`Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1280-t1/report.md` lines 372-374, finding F-730-1, High): `DELETE /api/webhooks/:id` answered the gate's sentinel verbatim, and `POST /api/webhooks/:id/rotate-secret` answered the field-encryption layer's internal configuration message ("PII encryption is not initialised — call registerKey() + setActiveVersion()…"). None of the seven catch blocks logs the error, so simply deleting the text would destroy the only diagnostic. KS-730 fixed the same class in three sibling files, merged today as #1282/#1283/#1284, with a local helper that logs the thrown text server-side with the route named and answers a constant body — `routes/gdpr.ts:210-213`, `routes/systemErrors.ts:93-96` at the tip. This change applies that helper here, unchanged except for 2-space indentation (this file's style).

**This brief:** add the helper (at the END of the file, so no line above it moves — B and C quote the same line numbers) and convert `:200` (GET /) and `:267` (POST /).

## Secret handling — does this edit change it? NO

The ONLY lines this brief changes in `webhooks.ts` are `:200`, `:267` — each the response line of a `catch` block — plus the 18-line helper inserted after `:548`. No line on
the secret path changes: `newSecret` generation (`:345`), `encryptWebhookSecret(newSecret, req.params.id)` (`:348`, body `:42-:44`),
the `UPDATE svc_webhooks SET secret_v2 = ${encrypted}` (`:349`), the one-time `res.json({ success: true, secret: newSecret })`
(`:350`), `decryptWebhookSecret` (`:46-:62`) and the HMAC signing in `deliverWebhook` (`:433`) are all byte-identical before and
after. What changes is where the THROWN TEXT goes: from the client's 500 body to `logger.error`. That text cannot carry the
plaintext secret — `encryptField` (`packages/shared/src/crypto/encryptedField.ts:315`) throws only key-state and context messages
(`:286`, `:293`, `:301`, `:318`), `plaintext` appears only at `:315/:316/:328` and in none of them, and the `UPDATE` binds the
ciphertext, never `newSecret`. So this is an error-BODY change on a route that handles a secret, not a change to secret handling.
This brief does not touch the rotate-secret route at all (that is brief B, `:352`).

## The exact change

Every `-` line below is the same SITE line — the SAME bytes at all seven sites (literal line-equality count 7 at the tip), so the context lines and the header are what place each hunk. Copy the hunks EXACTLY, headers included. The context lines are ASCII (the only non-ASCII line near a site, `:264`, is deliberately outside the 2-line context).

Edit 1 — line `:200` (GET /), replacement of ONE line by ONE line. Context: `:198` is `    res.json({ success: true, webhooks: rows });`, `:199` is `  } catch (err: any) {`, `:201` is `  }`, `:202` is `});` — copy all four as context.

```diff
@@ -198,5 +198,5 @@
     res.json({ success: true, webhooks: rows });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook list failed (GET /api/webhooks)', err);
   }
 });
```

Edit 2 — line `:267` (POST /), replacement of ONE line by ONE line. Context: `:265` is `    });`, `:266` is `  } catch (err: any) {`, `:268` is `  }`, `:269` is `});` — copy all four as context.

```diff
@@ -265,5 +265,5 @@
     });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook create failed (POST /api/webhooks)', err);
   }
 });
```

Edit 3 — PURE INSERTION of 18 lines after `:548` (the empty line after `dispatchEvent`'s closing `}` at `:547`), before `:549` `export default webhooksRouter;` (byte-unique, count 1). The inserted block is the helper's docblock, the helper, and ONE empty line after its closing `}`. Context: `:546` `  }`, `:547` `}`, `:548` empty.

```diff
@@ -546,4 +546,22 @@
   }
 }
 
+/**
+ * KS-1341: the only place in this router that turns a caught error into a 500.
+ *
+ * Seven catch blocks above put the thrown error's own text in the 500 body with NO NODE_ENV
+ * guard, so it reached the client in every environment, production included (measured by the
+ * 2026-09-26 gate: DELETE /:id returned the thrown text, rotate-secret returned internal
+ * encryption-configuration text). Same helper as routes/gdpr.ts and routes/systemErrors.ts
+ * (KS-730): log the thrown text server-side with the route named, answer the constant body.
+ *
+ * Declared at the END of the file on purpose: a function declaration is hoisted, and the
+ * handlers above only call it at request time (deliverWebhook is called above its own
+ * declaration the same way). Placing it here leaves every line above it where it was.
+ */
+function fail500(res: Response, context: string, err: unknown): void {
+  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
+  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
+}
+
 export default webhooksRouter;
```

**Do NOT touch:**

- every line of `webhooks.ts` other than the 2 `-` line(s) above and the 18 inserted lines;
- `encryptWebhookSecret` / `decryptWebhookSecret` (`:42-:62`), the rotate-secret secret path (`:345-:350`: `newSecret`
  generation, `encryptWebhookSecret`, the `UPDATE ... secret_v2`, the one-time `res.json({ success: true, secret: newSecret })`),
  `deliverWebhook` (`:427-:497`), `dispatchEvent` (`:503-:547`) — including its own `logger.warn('Webhook dispatch failed', { ..., error: err.message })`
  at `:544`, which is a LOG line, not a response;
- the two swallowing `.catch(...)` branches at `:196` and `:412` and the PATCH SQLSTATE→400 branch at `:318-:324` (pre-existing,
  pinned by controls);
- the imports (`:11-:19`) — add NONE; `Response` (`:11`) and `logger` (`:16`) are already imported;
- every other file: `routes/gdpr.ts`, `routes/systemErrors.ts`, `routes/adminConfig.ts`, `utils/pgErrors.ts`, the six existing
  webhooks suites (`ks1160`, `ks423`, `ks431`, `ks444`, `ks445`, `ks914`), and `__tests__/helpers/sharedModuleMock.ts`.

The helper's context string for each site is DISTINCT and names the route; do not shorten, merge or reword them.

## The test

File: `Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` (NEW, 173 lines).
This service runs **jest** (ts-jest preset, `testEnvironment: 'node'`, `testMatch: ['**/__tests__/**/*.test.ts']` — read at
`Blockchain/Dev/services/originate/jest.config.js`), NOT vitest: `jest.mock`, `jest.fn`, `jest.requireMock`; `expect` takes ONE
argument. There is no database, no network beyond a loopback listener on 127.0.0.1, and no app boot: `../db`,
`../middleware/auth`, `@secuura/shared` (through `./helpers/sharedModuleMock`) and `../utils/logger` are all mocked, exactly as
in `ks1160-webhooks-post-persists-normalised-url.test.ts` lines 7-60 (the shape copied). To run the file alone, from
`Blockchain/Dev/services/originate`: `npx jest src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts`.

The cell shape (LEAK string · four NODE_ENVs · constant body · logger received the route context · REACHED) is copied from `ks730c-adminconfig-500-never-answers-err-message.test.ts` lines 58-127, including its lesson (the KS-730 PR3 trap): a LEAK containing `does not exist` was routed into a benign 200 branch there, so a clean body alone proved nothing. Here the LEAK contains neither `does not exist` nor any SQLSTATE that `utils/pgErrors.ts:36` (`KNOWN_PG_CODES`) would classify, and every red cell asserts the logger received THIS route's context with the thrown text — which only the converted catch does.

**This file's own trap:** `GET /` chains `.catch(...)` onto its query (`webhooks.ts:191-:196`), so a REJECTED `$queryRaw` is swallowed into a 200 and never reaches the catch under test. Its cell makes `$queryRaw` THROW SYNCHRONOUSLY (`mockImplementationOnce(() => { throw ... })`); the 🟢 control `A0` pins the swallowing branch.

Emit this text as the new-file hunk `@@ -0,0 +1,173 @@`, every line prefixed `+`, nothing added or dropped:

```ts
// KS-1341 part A (originate routes/webhooks.ts, GET / and POST /): seven catch blocks answered a 500
// whose body carried the thrown error's own text, with NO NODE_ENV guard, so it reached the client in
// every environment, production included (measured by the 2026-09-26 batch1280 gate). Part A adds the
// file's fail500 helper and converts the first two sites; parts B and C convert the other five.
// Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
//
// THE GET / TRAP. GET / chains .catch() onto its list query, so a REJECTED $queryRaw is swallowed into
// a 200 with an empty list and never reaches the catch under test. The GET / cell therefore makes
// $queryRaw THROW SYNCHRONOUSLY, and every red cell asserts the catch was REACHED (the logger received
// this route's context with the thrown text), not only that the body is clean. control A0 pins the
// swallowing branch so the trap cannot come back silently.
const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();
const mockLoggerError = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: mockQueryRaw,
    $executeRaw: mockExecuteRaw,
    $executeRawUnsafe: jest.fn(),
  },
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { userId: '11111111-2222-4333-8444-555555555555' };
    next();
  },
}));

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    encryptField: jest.fn(() => 'v1:mock-ciphertext'),
    decryptField: jest.fn(() => ''),
    runWithTenantId: jest.fn(async (_tenantId: unknown, fn: () => unknown) => fn()),
    assertSafeOutboundUrl: jest.fn(async (raw: unknown) => ({ ok: true as const, url: String(raw) })),
  }),
);

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { webhooksRouter } from '../routes/webhooks';

// THE FIXTURE IS LOAD-BEARING. It must not contain 'does not exist' (the KS-730 PR3 trap) and must
// carry no Postgres SQLSTATE token that utils/pgErrors.ts would classify, so no benign or 4xx branch
// can claim it. The last control below pins both properties.
const LEAK = 'connect ECONNREFUSED 10.0.4.17:5432 ks1341a-private-detail';
const NODE_ENVS = ['production', 'development', 'test', undefined];
const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
const CREATE_BODY = { url: 'https://partner.example.com/hooks', events: ['certification.issued'] };

const app = express();
app.use('/api/webhooks', express.json(), webhooksRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => {
  if (ORIGINAL_NODE_ENV === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = ORIGINAL_NODE_ENV;
  server?.close();
});
beforeEach(() => jest.clearAllMocks());

function setNodeEnv(v: string | undefined): void {
  if (v === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = v;
}

// Each route is driven by making ITS OWN db call throw, so a cell cannot pass because another
// handler answered.
const ROUTES = [
  {
    label: 'GET /',
    method: 'GET',
    body: undefined,
    arm: () => mockQueryRaw.mockImplementationOnce(() => { throw new Error(LEAK); }),
    context: 'Webhook list failed (GET /api/webhooks)',
  },
  {
    label: 'POST /',
    method: 'POST',
    body: CREATE_BODY,
    arm: () => mockExecuteRaw.mockRejectedValueOnce(new Error(LEAK)),
    context: 'Webhook create failed (POST /api/webhooks)',
  },
];

async function call(route: (typeof ROUTES)[number], nodeEnv: string | undefined): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  route.arm();
  const res = await fetch(baseUrl + '/api/webhooks', {
    method: route.method,
    headers: { 'content-type': 'application/json' },
    ...(route.body === undefined ? {} : { body: JSON.stringify(route.body) }),
  });
  return { status: res.status, text: await res.text() };
}

describe('KS-1341 part A: GET / and POST / never answer a 500 with the thrown text', () => {
  it.each(ROUTES)('RED KS-1341 A1 $label: the thrown message is not in the 500 body under production, development, test or unset', async (route) => {
    for (const nodeEnv of NODE_ENVS) {
      const reply = await call(route, nodeEnv);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      // REACHED, not merely clean: only fail500 logs this route's context with the thrown text.
      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
    }
  });

  it.each(ROUTES)('RED KS-1341 A2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
    const reply = await call(route, 'production');
    expect(reply.status).toBe(500);
    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
  });

  it('control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch', async () => {
    // PRE-EXISTING behaviour this change must NOT alter, and the reason the GET / cell throws
    // synchronously: same route, same message, a rejected promise instead, a different answer.
    setNodeEnv('production');
    mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
    const res = await fetch(baseUrl + '/api/webhooks');
    expect(res.status).toBe(200);
    expect(JSON.parse(await res.text())).toEqual({ success: true, webhooks: [] });
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 A: a create that does NOT throw answers 201 and logs nothing', async () => {
    // Without this, every "not leaked" pass above is consistent with the router answering 500 always.
    setNodeEnv('production');
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await fetch(baseUrl + '/api/webhooks', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(CREATE_BODY),
    });
    expect(res.status).toBe(201);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 A: an authored 400 keeps its own text and logs nothing', async () => {
    // The risk of a blanket helper is that it swallows messages a route MEANT to return.
    setNodeEnv('production');
    const res = await fetch(baseUrl + '/api/webhooks', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ url: 'https://partner.example.com/hooks' }),
    });
    expect(res.status).toBe(400);
    expect(JSON.parse(await res.text()).error.message).toBe('url and events (array) are required');
    expect(mockExecuteRaw).not.toHaveBeenCalled();
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 A: the LEAK string is the thrown text and dodges every benign branch', () => {
    // If LEAK were absent from the thrown error, every leaked: false above would hold trivially.
    expect(new Error(LEAK).message).toBe(LEAK);
    expect(LEAK.length).toBeGreaterThan(20);
    expect(LEAK).not.toContain('does not exist');
    expect(LEAK).not.toMatch(/\b(22P02|22001|22007|22008|22021|22P05|23502|23503|23505|23514|42804)\b/);
  });
});
```

## Cells and controls

- 🔴 `RED KS-1341 A1 GET /: the thrown message is not in the 500 body under production, development, test or unset` — RED at the tip (the body carries LEAK)
- 🔴 `RED KS-1341 A1 POST /: the thrown message is not in the 500 body under production, development, test or unset` — RED at the tip (the body carries LEAK)
- 🔴 `RED KS-1341 A2 GET /: the thrown message is logged once, server-side, with this route named` — RED at the tip (nothing is logged)
- 🔴 `RED KS-1341 A2 POST /: the thrown message is logged once, server-side, with this route named` — RED at the tip (nothing is logged)
- 🟢 `control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch`
- 🟢 `control KS-1341 A: a create that does NOT throw answers 201 and logs nothing`  ← the positive control
- 🟢 `control KS-1341 A: an authored 400 keeps its own text and logs nothing`
- 🟢 `control KS-1341 A: the LEAK string is the thrown text and dodges every benign branch`

(`it.each` expands each 🔴 row into one test per route, named with the route label as shown.)

## The failing case (the "tamper")

After your change, in `Blockchain/Dev/services/originate/src/routes/webhooks.ts` line `:200` (GET /) reads `    fail500(res, 'Webhook list failed (GET /api/webhooks)', err);` — byte-unique in the post-change file (literal line-equality count 1, measured on the golden). Tamper: replace it with the original SITE line `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });` (4 leading spaces). Expected: `A1 GET /` and `A2 GET /` go RED; every 🟢 control stays GREEN. Restore → all GREEN.

## Premises (each one measured, with where)

- origin develop = `e080174c86c671349c508560744644fc0ef33388` — `git ls-remote origin refs/heads/develop` re-read at 2026-09-26 15:03:13 AEST (first read earlier this session, same sha); the object is in the local store (`git cat-file -t` → commit).
- The seven SITE lines, byte-identical, at `:200, :267, :325, :337, :352, :391, :416` — python line-equality count 7 on `git show e080174c86c6:Blockchain/Dev/services/originate/src/routes/webhooks.ts`; the gate lists the same seven (`report.md:372`).
- No catch in the file logs before answering: `webhooks.ts:199-201, :266-268, :314-326, :336-338, :351-353, :390-392, :415-417` read whole.
- `fail500` does not exist in the file at the tip — `grep -c -i fail500` → 0 (positive control: `grep -c -i webhooksrouter` → 10). `does not exist` occurs 0 times in the file (same instrument, `-i`).
- The helper text is copied from `routes/gdpr.ts:210-213` at the tip (2-space body; `systemErrors.ts:93-96` has the same body at 4-space).
- A function declaration used above its declaration is already the pattern in this file: `deliverWebhook` is called at `:378` and declared at `:427`. The lint config (`Blockchain/Dev/eslint.config.mjs:24-50, :78-96`) has no `no-use-before-define` rule; `js.configs.recommended` + `tseslint.configs.recommended` do not enable it (UNMEASURED by a lint run — see below).
- `Response` is the express type imported at `:11`; `logger` is imported at `:16`.
- `extractPgCode` (`utils/pgErrors.ts:48-72`) reads `err.code`, `err.meta.code`, then `KNOWN_PG_CODES` (`:36`) in the message — the LEAK strings match none (asserted by each file's last control).
- The six existing webhooks suites all mock `logger` WITH an `error` fn (`ks1160:33-35`, `ks423:42-44`, `ks431:21-23`, `ks444:61-63`, `ks445:28-30`, `ks914:25-27`), and none asserts a 500 body's message text; `ks445` "keeps 500 for genuinely unclassified failures" (`:136-141`) asserts status only, so it stays green.
- The golden (`golden/webhooks.A.ts`, `.AB.ts`, `.ABC.ts` and the three test files in the run directory) was BUILT and APPLIED: A → B → C apply with `git apply` strict (no `--recount`), reproduce the goldens byte for byte, and `typescript@5.9.3` `transpileModule` reports 0 syntactic diagnostics on all four files. The golden is for the checker, not shown to the model.
- After A+B+C, over non-comment lines: 0 lines match `/message: *err\??\.?message/`, 7 `fail500(res,` calls, 7 distinct contexts, 1 definition (measured on the golden; at A+B: 2 leaking, 5 calls).

## UNMEASURED — stated rather than glossed

- **The new test file was NOT run**, at the tip or after the fix — no jest, no type-check (`tsc`/ts-jest diagnostics), no lint. RED-at-tip and GREEN-after are REASONED from the source. The first checker run is the first execution.
- Type-level risks I could not rule out without ts-jest: the `it.each` row type inferred from a non-`as const` array with a union `body` field; `mock.calls.at(-1)` needs lib ES2022 (it is used by the merged `ks730c`, so probably fine).
- Setting `process.env.NODE_ENV = 'production'` inside a running jest worker is assumed to have no side effect on express or the mocks (the ks730 files do the same for development/demo/test; production is new here).
- The rest of the originate suite was not run, before or after; "no worse" is for the checker to measure.
- Whether the eslint run passes with the helper declared after its callers (reasoned from the config, not run).
- Open PRs were not listed through the GitHub API; only `git ls-remote` branch names were searched (see Collision).
- Whether deployed environments set `NODE_ENV`; irrelevant to the fix (it is unconditional) but the gate measured production only.

## Collision

- KS-1341: Backlog, priority 2 (High), assignee kamil.kreiser@secuura.ai, no attachments, no relations, created 2026-09-26 02:50Z (Linear re-read at 2026-09-26 15:03:18 AEST). Round 0 — this is the first brief; the counter allows this + ONE rebrief, then Opus 5.5.
- `git ls-remote origin` branch names matching `1341|webhook`: `feature/ks-1160-…` (`8d3c5c96`, the pre-squash head of #1186, which is merged into develop as `408821134`), `feature/ks-927-webhooks-description-guard-mock` (`542492c4`: `git log {SHA[:9]}..542492c4 -- {P}` → no commits, so it does not touch this file), and `refs/pull/372/head`. None in flight on this file.
- Wednesday's `local-model/night/queue.md` and `done.md`: 0 rows for KS-1341.
- Adjacent, NOT this file: KS-1334 (adminConfig.ts unconditional leaks).
- Sequencing: A → B → C, one at a time (the Spark runs one request at a time). This is brief A.

## Scope

Closes 2 of 7 sites. **Refs KS-1341, does NOT close it.** The ticket closes with brief C.

## Output

Exactly ONE fenced ```diff block, nothing outside it. First the product file (`--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts` / `+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts`, the 3 hunk(s) exactly as given, in file order), then the new test file (`--- /dev/null` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts`, `@@ -0,0 +1,173 @@`). Paths exactly as written here. Every `+` line on its own physical line. Every context line keeps its leading space. Do not add, reorder, reword or reindent anything.
