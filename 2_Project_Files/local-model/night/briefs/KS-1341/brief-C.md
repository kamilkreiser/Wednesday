# KS-1341-C WEBHOOKS500-C — route the POST /:id/test and GET /:id/deliveries 500s in routes/webhooks.ts through fail500, and pin all seven by source

File: `Blockchain/Dev/services/originate/src/routes/webhooks.ts`  (product, modified in place)
Test file: `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts`  (NEW)
Tip: `3f70224a069b944334480478ad5d16a5ed33eeae` (origin develop; contains brief A's merge #1288 = `a2a2b4c50d64` AND brief B's merge #1290 = `4857187ad`). **REV C (2026-09-26 20:3x): every line quoted here was RE-READ at that sha** — `webhooks.ts` there is 567 lines, blob `a2ad9e05162688ba83917363c942dfa4c7ede911`, byte-identical to the scratch golden `webhooks.AB.ts`; `fail500` is declared at `:562` (docblock `:549-:561`), `export default webhooksRouter;` is `:567`; the two remaining SITE lines are still `:391` and `:416`.
Runner: `jest` (ts-jest 29, `Blockchain/Dev/services/originate/package.json` `"test": "jest"`)

Written 2026-09-26 15:03:36 AEST (shell `date`) from `e080174c86c671349c508560744644fc0ef33388`, `webhooks.ts` read WHOLE (549 lines, ends with one `\n`, blob sha1 of `git show` output `c86b6344664f41bd6b12f4e7dc74aa37c76a52dd`, last changed at `408821134` KS-1160 #1186). **Brief C of 3 — THIRD of three (A → B → C). Needs A merged (helper) and B merged (its SOURCE cell counts all seven sites) — BOTH ARE MERGED at `3f70224a` (#1288, #1290).** Rev C re-read at `3f70224a` (see Tip); the only change from rev 1 is the C1 cell's per-environment logger clear (gate 28 finding N-1288-2, the same fix brief B carried), the test's line count (166 → 169), the `## Red cells` section and Arm R3.

## The mode — read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `Blockchain/Dev/services/originate/src/routes/webhooks.ts` — modified in place, `--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts` / `+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts`, EXACTLY the 2 hunk(s) given in `## The exact change`, byte for byte.
2. `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` — a NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts`, ONE hunk `@@ -0,0 +1,169 @@`, every line `+`, the text given in `## The test` byte for byte (169 lines).

You never touch any other file. In particular you do NOT edit any existing test, `routes/gdpr.ts`, `routes/systemErrors.ts`, `routes/adminConfig.ts`, `utils/pgErrors.ts`, `utils/logger.ts` or `__tests__/helpers/sharedModuleMock.ts`. Apply on develop `3f70224a` (A and B merged). The checker applies the TEST FILE ALONE first (every 🔴 cell must FAIL by assertion, every 🟢 control must PASS), then your product hunks on top (every cell must PASS).

## What is wrong (one paragraph)

`routes/webhooks.ts` (mounted at `/api/webhooks`) has seven catch blocks whose 500 answer is the byte-identical line `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });` at `:200, :267, :325, :337, :352, :391, :416` — with NO `NODE_ENV` guard, so the thrown error's own text reaches the client in every environment, production included. The 2026-09-26 QA gate MEASURED it under `NODE_ENV=production` (`Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1280-t1/report.md` lines 372-374, finding F-730-1, High): `DELETE /api/webhooks/:id` answered the gate's sentinel verbatim, and `POST /api/webhooks/:id/rotate-secret` answered the field-encryption layer's internal configuration message ("PII encryption is not initialised — call registerKey() + setActiveVersion()…"). None of the seven catch blocks logs the error, so simply deleting the text would destroy the only diagnostic. KS-730 fixed the same class in three sibling files, merged today as #1282/#1283/#1284, with a local helper that logs the thrown text server-side with the route named and answers a constant body — `routes/gdpr.ts:210-213`, `routes/systemErrors.ts:93-96` at the tip. This change applies that helper here, unchanged except for 2-space indentation (this file's style).

**This brief:** convert `:391` (POST /:id/test) and `:416` (GET /:id/deliveries), the last two; its SOURCE cell proves all seven are converted.

## Secret handling — does this edit change it? NO

The ONLY lines this brief changes in `webhooks.ts` are `:391`, `:416` — each the response line of a `catch` block — plus nothing else (the helper is A's). No line on
the secret path changes: `newSecret` generation (`:345`), `encryptWebhookSecret(newSecret, req.params.id)` (`:348`, body `:42-:44`),
the `UPDATE svc_webhooks SET secret_v2 = ${encrypted}` (`:349`), the one-time `res.json({ success: true, secret: newSecret })`
(`:350`), `decryptWebhookSecret` (`:46-:62`) and the HMAC signing in `deliverWebhook` (`:433`) are all byte-identical before and
after. What changes is where the THROWN TEXT goes: from the client's 500 body to `logger.error`. That text cannot carry the
plaintext secret — `encryptField` (`packages/shared/src/crypto/encryptedField.ts:315`) throws only key-state and context messages
(`:286`, `:293`, `:301`, `:318`), `plaintext` appears only at `:315/:316/:328` and in none of them, and the `UPDATE` binds the
ciphertext, never `newSecret`. So this is an error-BODY change on a route that handles a secret, not a change to secret handling.
This brief does not touch the rotate-secret route at all (that is brief B, `:352`).

## Before queueing (the builder, not the model)

This brief was first written against `e080174c86c671349c508560744644fc0ef33388` and applies on the develop commit that contains A and B (`3f70224a`). By construction the line numbers do not move: A replaces `:200`/`:267` one line for one line and inserts its helper (docblock `:549-:561`, declaration `:562`) just ABOVE `export default webhooksRouter;` (now `:567`) — README rev 3 — and B replaces `:325/:337/:352` one for one. **Measured at `3f70224a` (rev C):** the file there IS the golden `webhooks.AB.ts` byte for byte, and this brief's C.golden.diff applies to it strictly (`patch -p1 -F0` and `git apply`, no `--recount`), producing `webhooks.ABC.ts` byte for byte. Before queueing, re-read at the new tip:

```
git show <new-develop-sha>:Blockchain/Dev/services/originate/src/routes/webhooks.ts | sed -n '391p;416p'   # each must print the SITE line quoted in ## The exact change
git show <new-develop-sha>:Blockchain/Dev/services/originate/src/routes/webhooks.ts | grep -c '^function fail500('                 # must print 1
```
If either check fails, the brief is stale: do NOT queue it, rebuild it at the new tip.

**Rev C, measured at `3f70224a069b` (2026-09-26 20:3x):** `sed -n '391p;416p'` prints the SITE line twice; `grep -c '^function fail500('` → 1 (`:562`); `grep -c -i webhooksrouter` → 10 (positive control); literal SITE-line count in the file → 2. `patch -p1 -F0 --dry-run` of this brief's 2 product hunks on that file → rc 0; on a copy whose `:416` was tampered → rc 1. `ks1341c-…test.ts` does not exist at that sha (`git cat-file` → path does not exist).

## The exact change

Every `-` line below is the same SITE line — the SAME bytes at all seven sites (literal line-equality count 7 at the tip), so the context lines and the header are what place each hunk. Copy the hunks EXACTLY, headers included. The context lines are ASCII (the only non-ASCII line near a site, `:264`, is deliberately outside the 2-line context).

Edit 1 — line `:391` (POST /:id/test), replacement of ONE line by ONE line. Context: `:389` is `    });`, `:390` is `  } catch (err: any) {`, `:392` is `  }`, `:393` is `});` — copy all four as context.

```diff
@@ -389,5 +389,5 @@
     });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook test send failed (POST /api/webhooks/:id/test)', err);
   }
 });
```

Edit 2 — line `:416` (GET /:id/deliveries), replacement of ONE line by ONE line. Context: `:414` is `    res.json({ success: true, deliveries: rows });`, `:415` is `  } catch (err: any) {`, `:417` is `  }`, `:418` is `});` — copy all four as context.

```diff
@@ -414,5 +414,5 @@
     res.json({ success: true, deliveries: rows });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)', err);
   }
 });
```

**Do NOT touch:**

- every line of `webhooks.ts` other than the 2 `-` line(s) above;
- `encryptWebhookSecret` / `decryptWebhookSecret` (`:42-:62`), the rotate-secret secret path (`:345-:350`: `newSecret`
  generation, `encryptWebhookSecret`, the `UPDATE ... secret_v2`, the one-time `res.json({ success: true, secret: newSecret })`),
  `deliverWebhook` (`:427-:497`), `dispatchEvent` (`:503-:547`) — including its own `logger.warn('Webhook dispatch failed', { ..., error: err.message })`
  at `:544`, which is a LOG line, not a response;
- the `fail500` helper and its docblock (`:549-:565`, added by part A) and `export default webhooksRouter;` (`:567`);
- the two swallowing `.catch(...)` branches at `:196` and `:412` and the PATCH SQLSTATE→400 branch at `:318-:324` (pre-existing,
  pinned by controls);
- the imports (`:11-:19`) — add NONE; `Response` (`:11`) and `logger` (`:16`) are already imported;
- every other file: `routes/gdpr.ts`, `routes/systemErrors.ts`, `routes/adminConfig.ts`, `utils/pgErrors.ts`, the six existing
  webhooks suites (`ks1160`, `ks423`, `ks431`, `ks444`, `ks445`, `ks914`), and `__tests__/helpers/sharedModuleMock.ts`.

The helper's context string for each site is DISTINCT and names the route; do not shorten, merge or reword them.

## The test

File: `Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (NEW, 169 lines).
This service runs **jest** (ts-jest preset, `testEnvironment: 'node'`, `testMatch: ['**/__tests__/**/*.test.ts']` — read at
`Blockchain/Dev/services/originate/jest.config.js`), NOT vitest: `jest.mock`, `jest.fn`, `jest.requireMock`; `expect` takes ONE
argument. There is no database, no network beyond a loopback listener on 127.0.0.1, and no app boot: `../db`,
`../middleware/auth`, `@secuura/shared` (through `./helpers/sharedModuleMock`) and `../utils/logger` are all mocked, exactly as
in `ks1160-webhooks-post-persists-normalised-url.test.ts` lines 7-60 (the shape copied). To run the file alone, from
`Blockchain/Dev/services/originate`: `npx jest src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts`.

The cell shape (LEAK string · four NODE_ENVs · constant body · logger received the route context · REACHED) is copied from `ks730c-adminconfig-500-never-answers-err-message.test.ts` lines 58-127, including its lesson (the KS-730 PR3 trap): a LEAK containing `does not exist` was routed into a benign 200 branch there, so a clean body alone proved nothing. Here the LEAK contains neither `does not exist` nor any SQLSTATE that `utils/pgErrors.ts:36` (`KNOWN_PG_CODES`) would classify, and every red cell asserts the logger received THIS route's context with the thrown text — which only the converted catch does.

**REACHED is pinned PER ENVIRONMENT (gate 28, N-1288-2, MEASURED on part A; brief B carries the same fix).** Part A's A1 read `mockLoggerError.mock.calls.at(-1)` with no clear inside its NODE_ENV loop, so the production iteration's log call satisfied the development/test/unset iterations: a helper that logged only under `NODE_ENV==='production'` kept A1 green while a real probe went red 18 times. C1 therefore calls `mockLoggerError.mockClear()` at the TOP of each loop iteration and asserts the WHOLE call list for that environment is exactly `[[route.context, { error: LEAK }]]` (with `nodeEnv` in the compared object, so a failure names the environment). Do not "simplify" it back to `.at(-1)`.

**This file's own trap:** `GET /:id/deliveries` chains `.catch(...)` onto its query (`webhooks.ts:406-:412`), so a REJECTED `$queryRaw` is swallowed into a 200 and never reaches the catch under test. Its cell makes `$queryRaw` THROW SYNCHRONOUSLY (`mockImplementationOnce(() => { throw ... })`); the 🟢 control `C0` pins the swallowing branch.

Emit this text as the new-file hunk `@@ -0,0 +1,169 @@`, every line prefixed `+`, nothing added or dropped:

```ts
// KS-1341 part C (originate routes/webhooks.ts, POST /:id/test and GET /:id/deliveries): the last two
// of the seven catch blocks that answered a 500 whose body carried the thrown error's own text in
// every NODE_ENV. Parts A and B added the fail500 helper and converted the other five. This part
// also carries the whole-file SOURCE cell, which is RED until all seven are converted.
// Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
//
// THE DELIVERIES TRAP. GET /:id/deliveries chains .catch(() => []) onto its query, so a REJECTED
// $queryRaw is swallowed into a 200 with an empty list and never reaches the catch under test. That
// cell therefore makes $queryRaw THROW SYNCHRONOUSLY; control C0 pins the swallowing branch.
// POST /:id/test awaits its query with no .catch, so a rejection reaches its catch directly.
const mockQueryRaw = jest.fn();
const mockLoggerError = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: mockQueryRaw,
    $executeRaw: jest.fn(),
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
import { readFileSync } from 'fs';
import path from 'path';
import { webhooksRouter } from '../routes/webhooks';

// THE FIXTURE IS LOAD-BEARING. It must not contain 'does not exist' (the KS-730 PR3 trap) and must
// carry no Postgres SQLSTATE token that utils/pgErrors.ts would classify.
const LEAK = 'canceling statement due to statement timeout on svc_webhook_deliveries ks1341c-private-detail';
const NODE_ENVS = ['production', 'development', 'test', undefined];
const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ORIGINAL_NODE_ENV = process.env.NODE_ENV;
const WEBHOOK_ID = 'a1b2c3d4-5678-4abc-9def-0123456789ab';

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

// Each route is driven by making ITS OWN query throw, so a cell cannot pass because another handler
// answered.
const ROUTES = [
  {
    label: 'POST /:id/test',
    method: 'POST',
    path: '/' + WEBHOOK_ID + '/test',
    arm: () => mockQueryRaw.mockRejectedValueOnce(new Error(LEAK)),
    context: 'Webhook test send failed (POST /api/webhooks/:id/test)',
  },
  {
    label: 'GET /:id/deliveries',
    method: 'GET',
    path: '/' + WEBHOOK_ID + '/deliveries',
    arm: () => mockQueryRaw.mockImplementationOnce(() => { throw new Error(LEAK); }),
    context: 'Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)',
  },
];

async function call(route: (typeof ROUTES)[number], nodeEnv: string | undefined): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  route.arm();
  const res = await fetch(baseUrl + '/api/webhooks' + route.path, { method: route.method });
  return { status: res.status, text: await res.text() };
}

describe('KS-1341 part C: test-send and delivery history never answer a 500 with the thrown text', () => {
  it.each(ROUTES)('RED KS-1341 C1 $label: the thrown message is not in the 500 body under production, development, test or unset', async (route) => {
    for (const nodeEnv of NODE_ENVS) {
      // Cleared PER ENVIRONMENT: without it the production call satisfies every later iteration,
      // so a helper that logged only under production would stay green (gate 28, N-1288-2).
      mockLoggerError.mockClear();
      const reply = await call(route, nodeEnv);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      // REACHED in THIS environment, not merely clean: exactly one call, this route's context, the thrown text.
      expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: LEAK }]] });
    }
  });

  it.each(ROUTES)('RED KS-1341 C2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
    const reply = await call(route, 'production');
    expect(reply.status).toBe(500);
    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
  });

  it('RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts', () => {
    // Weaker than the behavioural cells, and deliberately so: it reads the file, not the behaviour.
    // It is what proves the seven sites of parts A, B and C are all converted, and that nobody
    // re-adds the shape. Comment lines are skipped so the helper's docblock cannot be counted.
    const src = readFileSync(path.join(__dirname, '..', 'routes', 'webhooks.ts'), 'utf8');
    const lines = src.split('\n').filter((l) => !l.trim().startsWith('*') && !l.trim().startsWith('//'));
    const leaks = lines.filter((l) => /message: *err\??\.?message/.test(l));
    const helperCalls = lines.filter((l) => l.includes('fail500(res,'));
    const contexts = helperCalls.map((l) => (l.match(/fail500\(res, '([^']+)'/) ?? [])[1]);
    const definitions = lines.filter((l) => l.startsWith('function fail500('));
    expect({ leaks: leaks.length, helperCalls: helperCalls.length, distinctContexts: new Set(contexts).size, definitions: definitions.length })
      .toEqual({ leaks: 0, helperCalls: 7, distinctContexts: 7, definitions: 1 });
    expect(contexts.filter((c) => !c)).toEqual([]);
  });

  it('control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch', async () => {
    // PRE-EXISTING behaviour this change must NOT alter, and the reason the deliveries cell throws
    // synchronously: same route, same message, a rejected promise instead, a different answer.
    setNodeEnv('production');
    mockQueryRaw.mockRejectedValueOnce(new Error(LEAK));
    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID + '/deliveries');
    expect(res.status).toBe(200);
    expect(JSON.parse(await res.text())).toEqual({ success: true, deliveries: [] });
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 C: a test-send for an unknown webhook keeps its authored 404 and logs nothing', async () => {
    // Without this, every "not leaked" pass above is consistent with the router answering 500 always,
    // and it proves the helper did not flatten a message the route MEANT to return.
    setNodeEnv('production');
    mockQueryRaw.mockResolvedValueOnce([]);
    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID + '/test', { method: 'POST' });
    expect(res.status).toBe(404);
    expect(JSON.parse(await res.text()).error.message).toBe('Webhook not found');
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 C: the LEAK string is the thrown text and dodges every benign branch', () => {
    // If LEAK were absent from the thrown error, every leaked: false above would hold trivially.
    expect(new Error(LEAK).message).toBe(LEAK);
    expect(LEAK.length).toBeGreaterThan(20);
    expect(LEAK).not.toContain('does not exist');
    expect(LEAK).not.toMatch(/\b(22P02|22001|22007|22008|22021|22P05|23502|23503|23505|23514|42804)\b/);
  });
});
```

## Red cells
- RED KS-1341 C1
- RED KS-1341 C2
- RED KS-1341 C3

(Title SUBSTRINGS. C1 and C2 are `it.each` row families, each matching the POST /:id/test and GET /:id/deliveries rows; C3 is the single SOURCE cell. These five cells go RED at the tip (`3f70224a`, parts A and B merged: C1/C2 because the two bodies carry LEAK and nothing is logged, C3 because the file has 2 leaking lines and 5 helper calls) and GREEN with the fix; the three `control KS-1341 C…` cells are green at both. The builder's undeclared-red gate cannot see `it.each` titles, so this section is load-bearing.)

## Cells and controls

- 🔴 `RED KS-1341 C1 POST /:id/test: the thrown message is not in the 500 body under production, development, test or unset` — RED at the tip (the body carries LEAK)
- 🔴 `RED KS-1341 C1 GET /:id/deliveries: the thrown message is not in the 500 body under production, development, test or unset` — RED at the tip (the body carries LEAK)
- 🔴 `RED KS-1341 C2 POST /:id/test: the thrown message is logged once, server-side, with this route named` — RED at the tip (nothing is logged)
- 🔴 `RED KS-1341 C2 GET /:id/deliveries: the thrown message is logged once, server-side, with this route named` — RED at the tip (nothing is logged)
- 🔴 `RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts` — RED at the A+B tip `3f70224a` (2 leaking lines, 5 helper calls; measured on the file at that sha)
- 🟢 `control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch`
- 🟢 `control KS-1341 C: a test-send for an unknown webhook keeps its authored 404 and logs nothing`  ← the positive control
- 🟢 `control KS-1341 C: the LEAK string is the thrown text and dodges every benign branch`

(`it.each` expands each 🔴 row into one test per route, named with the route label as shown.)

## The failing case (the "tamper")

After your change, in `Blockchain/Dev/services/originate/src/routes/webhooks.ts` line `:416` (GET /:id/deliveries) reads `    fail500(res, 'Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)', err);` — byte-unique in the post-change file (literal line-equality count 1, measured on the golden). Tamper: replace it with the original SITE line `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });` (4 leading spaces). Expected: `C1 GET /:id/deliveries` and `C2 GET /:id/deliveries` go RED and `C3 SOURCE` goes RED; every 🟢 control stays GREEN. Restore → all GREEN.

**Arm R3 — production-only logging (rev C; the N-1288-2 regression arm, REQUIRED).** In the post-change file, line `:563` (inside `fail500`, unchanged by this brief) reads `  logger.error(context, { error: err instanceof Error ? err.message : String(err) });` — byte-unique (count 1 in the golden `webhooks.ABC.ts`). Tamper: replace it with `  if (process.env.NODE_ENV === 'production') logger.error(context, { error: err instanceof Error ? err.message : String(err) });` (2 leading spaces). Expected: both `C1` rows go RED (each fails at its `development` iteration: `calls: []` where one call is expected, and the failure names `nodeEnv: 'development'`); both `C2` rows stay GREEN (they drive production only); `C3 SOURCE` stays GREEN (the call sites are unchanged); every 🟢 control stays GREEN. **If any `C1` row stays green under this arm, the per-environment clear has been lost and the cell has regressed to part A's blindness — that is a FAIL of this brief, not a pass.** Restore → all GREEN.

## Premises (each one measured, with where)

- **Rev C:** origin develop = `3f70224a069b944334480478ad5d16a5ed33eeae` (`git ls-remote`, 2026-09-26 20:3x; log: `3f70224a0` KS-1337 #1291 → `4857187ad` KS-1341 part B #1290 → `179a4f32e` KS-1318 #1289 → `a2a2b4c50` KS-1341 part A #1288). The object is NOT in the Blockchain checkout's store, so it was read from a scratchpad clone (`git clone --no-local` of that checkout + `fetch origin develop` INTO THE CLONE; nothing written in the Secuura folder). At that sha `webhooks.ts` = golden `webhooks.AB.ts` byte for byte (blob `a2ad9e05`), `ks1341b-…test.ts` = the golden B test byte for byte, and `sharedModuleMock.ts`, `utils/pgErrors.ts`, `utils/logger.ts`, `jest.config.js`, `services/originate/package.json`, `tsconfig.json`, `Blockchain/Dev/package.json`, `package-lock.json` and `ks1160-…test.ts` have the same blob as at `e080174c` (the harness this test copies is unchanged).
- **Rev C golden, MEASURED through the checker** (`tasks/code_patch/spark_checker.sh` on `golden/C.golden.diff` in a scratch clone at `3f70224a`, 2026-09-26 20:39): A1-A7 PASS 7/7 + A2a; A4 test-only at the tip = 5 failed / 8 run, exactly the declared `C1`×2, `C2`×2, `C3` as assertion reds, 3 controls green; A5 8/8; A6 originate suite 962 → 970, 0 new reds; A7 tsc rc 0.
- **Rev C lint, MEASURED:** originate's own `lint` script is `eslint src` (config `Blockchain/Dev/eslint.config.mjs`, eslint v10.7.0). `npx eslint --max-warnings 0` on the golden's new test, `routes/webhooks.ts` after C and the merged B test → rc 0, 0 problems; positive control (a file with an unused `const`) → rc 1, 1 warning.
- **N-1288-1 is closed by this brief without an edit point:** the helper docblock (`:550`) says "the only place in this router that turns a caught error into a 500". At `3f70224a` that is false (`:391`, `:416` still answer their own 500); after C it is true, and `C3 SOURCE` pins it (0 leaking lines, 7 helper calls).

- (rev 1, historical) origin develop = `e080174c86c671349c508560744644fc0ef33388` — `git ls-remote origin refs/heads/develop` re-read at 2026-09-26 15:03:13 AEST (first read earlier this session, same sha); the object is in the local store (`git cat-file -t` → commit).
- The seven SITE lines, byte-identical, at `:200, :267, :325, :337, :352, :391, :416` — python line-equality count 7 on `git show e080174c86c6:Blockchain/Dev/services/originate/src/routes/webhooks.ts`; the gate lists the same seven (`report.md:372`).
- No catch in the file logs before answering: `webhooks.ts:199-201, :266-268, :314-326, :336-338, :351-353, :390-392, :415-417` read whole.
- (rev 1, at `e080174c`) `fail500` did not exist in the file — `grep -c -i fail500` → 0 (positive control: `grep -c -i webhooksrouter` → 10). `does not exist` occurs 0 times in the file (same instrument, `-i`).
- The helper text is copied from `routes/gdpr.ts:210-213` at the tip (2-space body; `systemErrors.ts:93-96` has the same body at 4-space).
- A function declaration used above its declaration is already the pattern in this file: `deliverWebhook` is called at `:378` and declared at `:427`. The lint config (`Blockchain/Dev/eslint.config.mjs:24-50, :78-96`) has no `no-use-before-define` rule; `js.configs.recommended` + `tseslint.configs.recommended` do not enable it (UNMEASURED by a lint run — see below).
- `Response` is the express type imported at `:11`; `logger` is imported at `:16`.
- `extractPgCode` (`utils/pgErrors.ts:48-72`) reads `err.code`, `err.meta.code`, then `KNOWN_PG_CODES` (`:36`) in the message — the LEAK strings match none (asserted by each file's last control).
- The six existing webhooks suites all mock `logger` WITH an `error` fn (`ks1160:33-35`, `ks423:42-44`, `ks431:21-23`, `ks444:61-63`, `ks445:28-30`, `ks914:25-27`), and none asserts a 500 body's message text; `ks445` "keeps 500 for genuinely unclassified failures" (`:136-141`) asserts status only, so it stays green.
- The golden (`golden/webhooks.A.ts`, `.AB.ts`, `.ABC.ts` and the three test files in the run directory) was BUILT and APPLIED: A → B → C apply with `git apply` strict (no `--recount`), reproduce the goldens byte for byte, and `typescript@5.9.3` `transpileModule` reports 0 syntactic diagnostics on all four files. The golden is for the checker, not shown to the model.
- After A+B+C, over non-comment lines: 0 lines match `/message: *err\??\.?message/`, 7 `fail500(res,` calls, 7 distinct contexts, 1 definition (measured on the golden; at A+B: 2 leaking, 5 calls).

## UNMEASURED — stated rather than glossed

- **Rev C:** Arm R3 and the tamper were NOT executed before this brief was queued (reasoned from the cell; the same arms were MEASURED on part B). What WAS measured at rev C is listed under Premises: the golden through the checker (jest RED at tip / GREEN after, the whole originate suite, tsc) and originate's eslint.
- The rev-1 lines below saying "no jest / no lint" are superseded for THIS brief by the rev-C measurements; the rest stands.

- **The new test file was NOT run**, at the tip or after the fix — no jest, no type-check (`tsc`/ts-jest diagnostics), no lint. RED-at-tip and GREEN-after are REASONED from the source. The first checker run is the first execution.
- Type-level risks I could not rule out without ts-jest: the `it.each` row type inferred from a non-`as const` array with a union `body` field; `mock.calls.at(-1)` needs lib ES2022 (it is used by the merged `ks730c`, so probably fine).
- Setting `process.env.NODE_ENV = 'production'` inside a running jest worker is assumed to have no side effect on express or the mocks (the ks730 files do the same for development/demo/test; production is new here).
- The rest of the originate suite was not run, before or after; "no worse" is for the checker to measure.
- Whether the eslint run passes with the helper declared after its callers (reasoned from the config, not run).
- Open PRs were not listed through the GitHub API; only `git ls-remote` branch names were searched (see Collision).
- Whether deployed environments set `NODE_ENV`; irrelevant to the fix (it is unconditional) but the gate measured production only.

## Collision

- **Rev C:** KS-1341 is In Progress (parts A #1288 and B #1290 merged); this brief is part C's round counter 0 (this + ONE rebrief, then Opus 5.5). The builder needs `started_ok=` because the ticket is started.
- (rev 1) KS-1341: Backlog, priority 2 (High), assignee kamil.kreiser@secuura.ai, no attachments, no relations, created 2026-09-26 02:50Z (Linear re-read at 2026-09-26 15:03:18 AEST). Round 0 — this is the first brief; the counter allows this + ONE rebrief, then Opus 5.5.
- `git ls-remote origin` branch names matching `1341|webhook`: `feature/ks-1160-…` (`8d3c5c96`, the pre-squash head of #1186, which is merged into develop as `408821134`), `feature/ks-927-webhooks-description-guard-mock` (`542492c4`: `git log {SHA[:9]}..542492c4 -- {P}` → no commits, so it does not touch this file), and `refs/pull/372/head`. None in flight on this file.
- Wednesday's `local-model/night/queue.md` and `done.md`: 0 rows for KS-1341.
- Adjacent, NOT this file: KS-1334 (adminConfig.ts unconditional leaks).
- Sequencing: A → B → C, one at a time (the Spark runs one request at a time). This is brief C.

## Scope

With A and B merged, this closes KS-1341: all seven sites converted, pinned by `C3 SOURCE`. **Closes KS-1341** (A and B are merged at `3f70224a`).

## Output

Exactly ONE fenced ```diff block, nothing outside it. First the product file (`--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts` / `+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts`, the 2 hunk(s) exactly as given, in file order), then the new test file (`--- /dev/null` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts`, `@@ -0,0 +1,169 @@`). Paths exactly as written here. Every `+` line on its own physical line. Every context line keeps its leading space. Do not add, reorder, reword or reindent anything.
