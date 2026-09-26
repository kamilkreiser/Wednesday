# KS-1341-B WEBHOOKS500-B — route the PATCH /:id, DELETE /:id and POST /:id/rotate-secret 500s in routes/webhooks.ts through fail500

File: `Blockchain/Dev/services/originate/src/routes/webhooks.ts`  (product, modified in place)
Test file: `Blockchain/Dev/services/originate/src/__tests__/ks1341b-webhooks-500-never-answers-err-message.test.ts`  (NEW)
Tip: `179a4f32ec0643689b55a8d7207e63f6ec3d3831` (origin develop, contains brief A's merge #1288 = squash `a2a2b4c50d64`). **REV B (2026-09-26 18:1x): every line quoted here was RE-READ at that sha** — `webhooks.ts` there is 567 lines, blob `275dcec47b5da263614a54aa1fad9710d169cc4c`, byte-identical to the scratch golden `webhooks.A.ts`; `fail500` is declared at `:562` (docblock `:549-:561`), `export default webhooksRouter;` is `:567`. The three sites did not move.
Runner: `jest` (ts-jest 29, `Blockchain/Dev/services/originate/package.json` `"test": "jest"`)

Written 2026-09-26 15:03:36 AEST (shell `date`) from `e080174c86c671349c508560744644fc0ef33388`, `webhooks.ts` read WHOLE (549 lines, ends with one `\n`, blob sha1 of `git show` output `c86b6344664f41bd6b12f4e7dc74aa37c76a52dd`, last changed at `408821134` KS-1160 #1186). **Brief B of 3 — SECOND of three (A → B → C). Needs A merged (it calls `fail500`, which A adds) — A IS merged at `179a4f32` (#1288).** Rev B re-read at `179a4f32` (see Tip); the only change from rev 1 is the B1 cell's per-environment logger clear (gate 28 finding N-1288-2) and the test's line count (197 → 200).

## The mode — read this twice

CODE+TEST. Your diff touches EXACTLY 2 files, in this order:
1. `Blockchain/Dev/services/originate/src/routes/webhooks.ts` — modified in place, `--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts` / `+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts`, EXACTLY the 3 hunk(s) given in `## The exact change`, byte for byte.
2. `Blockchain/Dev/services/originate/src/__tests__/ks1341b-webhooks-500-never-answers-err-message.test.ts` — a NEW file: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341b-webhooks-500-never-answers-err-message.test.ts`, ONE hunk `@@ -0,0 +1,200 @@`, every line `+`, the text given in `## The test` byte for byte (200 lines).

You never touch any other file. In particular you do NOT edit any existing test, `routes/gdpr.ts`, `routes/systemErrors.ts`, `routes/adminConfig.ts`, `utils/pgErrors.ts`, `utils/logger.ts` or `__tests__/helpers/sharedModuleMock.ts`. Apply on develop AFTER brief A is merged. The checker applies the TEST FILE ALONE first (every 🔴 cell must FAIL by assertion, every 🟢 control must PASS), then your product hunks on top (every cell must PASS).

## What is wrong (one paragraph)

`routes/webhooks.ts` (mounted at `/api/webhooks`) has seven catch blocks whose 500 answer is the byte-identical line `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });` at `:200, :267, :325, :337, :352, :391, :416` — with NO `NODE_ENV` guard, so the thrown error's own text reaches the client in every environment, production included. The 2026-09-26 QA gate MEASURED it under `NODE_ENV=production` (`Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1280-t1/report.md` lines 372-374, finding F-730-1, High): `DELETE /api/webhooks/:id` answered the gate's sentinel verbatim, and `POST /api/webhooks/:id/rotate-secret` answered the field-encryption layer's internal configuration message ("PII encryption is not initialised — call registerKey() + setActiveVersion()…"). None of the seven catch blocks logs the error, so simply deleting the text would destroy the only diagnostic. KS-730 fixed the same class in three sibling files, merged today as #1282/#1283/#1284, with a local helper that logs the thrown text server-side with the route named and answers a constant body — `routes/gdpr.ts:210-213`, `routes/systemErrors.ts:93-96` at the tip. This change applies that helper here, unchanged except for 2-space indentation (this file's style).

**This brief:** convert `:325` (PATCH /:id), `:337` (DELETE /:id — the MEASURED production leak) and `:352` (POST /:id/rotate-secret — the MEASURED configuration-text leak).

## Secret handling — does this edit change it? NO

The ONLY lines this brief changes in `webhooks.ts` are `:325`, `:337`, `:352` — each the response line of a `catch` block — plus nothing else (the helper is A's). No line on
the secret path changes: `newSecret` generation (`:345`), `encryptWebhookSecret(newSecret, req.params.id)` (`:348`, body `:42-:44`),
the `UPDATE svc_webhooks SET secret_v2 = ${encrypted}` (`:349`), the one-time `res.json({ success: true, secret: newSecret })`
(`:350`), `decryptWebhookSecret` (`:46-:62`) and the HMAC signing in `deliverWebhook` (`:433`) are all byte-identical before and
after. What changes is where the THROWN TEXT goes: from the client's 500 body to `logger.error`. That text cannot carry the
plaintext secret — `encryptField` (`packages/shared/src/crypto/encryptedField.ts:315`) throws only key-state and context messages
(`:286`, `:293`, `:301`, `:318`), `plaintext` appears only at `:315/:316/:328` and in none of them, and the `UPDATE` binds the
ciphertext, never `newSecret`. So this is an error-BODY change on a route that handles a secret, not a change to secret handling.
The rotate-secret catch (`:352`) is in THIS brief; the 🟢 rotate-secret control (`a rotate-secret that does NOT throw ...`) pins the secret path end to end (fresh `whsec_` secret, encrypted with this row's AAD, stored once, returned once, nothing logged).

## Before queueing (the builder, not the model)

This brief is written against `e080174c86c671349c508560744644fc0ef33388` and applies on the develop commit that contains A. By construction the line numbers do not move: A replaces `:200`/`:267` one line for one line and inserts its helper (docblock `:549-:561`, declaration `:562`) just ABOVE `export default webhooksRouter;` (now `:567`) — README rev 3 — and B replaces `:325/:337/:352` one for one. **Verified in the scratch golden** (`golden/assemble_and_check.sh`): A → B → C apply strict with `git apply` (no `--recount`) and reproduce the golden files byte for byte. Before queueing, re-read at the new tip:

```
git show <new-develop-sha>:Blockchain/Dev/services/originate/src/routes/webhooks.ts | sed -n '325p;337p;352p'   # each must print the SITE line quoted in ## The exact change
git show <new-develop-sha>:Blockchain/Dev/services/originate/src/routes/webhooks.ts | grep -c '^function fail500('                 # must print 1
```
If either check fails, the brief is stale: do NOT queue it, rebuild it at the new tip.

**Rev B, measured at `179a4f32ec06` (2026-09-26 18:1x):** `sed -n '325p;337p;352p'` prints the SITE line three times; `grep -c '^function fail500('` → 1 (`:562`); `grep -c -i webhooksrouter` → 10 (positive control). `patch -p1 -F0 --dry-run` of this brief's 3 product hunks on that file → rc 0; on a copy whose `:337` was tampered → rc 1. `ks1341b-…test.ts` does not exist at that sha (`git cat-file` → path does not exist).

## The exact change

Every `-` line below is the same SITE line — the SAME bytes at all seven sites (literal line-equality count 7 at the tip), so the context lines and the header are what place each hunk. Copy the hunks EXACTLY, headers included. The context lines are ASCII (the only non-ASCII line near a site, `:264`, is deliberately outside the 2-line context).

Edit 1 — line `:325` (PATCH /:id), replacement of ONE line by ONE line. Context: `:323` is `      });`, `:324` is `    }`, `:326` is `  }`, `:327` is `});` — copy all four as context.

```diff
@@ -323,5 +323,5 @@
       });
     }
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook update failed (PATCH /api/webhooks/:id)', err);
   }
 });
```

Edit 2 — line `:337` (DELETE /:id), replacement of ONE line by ONE line. Context: `:335` is `    res.json({ success: true });`, `:336` is `  } catch (err: any) {`, `:338` is `  }`, `:339` is `});` — copy all four as context.

```diff
@@ -335,5 +335,5 @@
     res.json({ success: true });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook delete failed (DELETE /api/webhooks/:id)', err);
   }
 });
```

Edit 3 — line `:352` (POST /:id/rotate-secret), replacement of ONE line by ONE line. Context: `:350` is `    res.json({ success: true, secret: newSecret });`, `:351` is `  } catch (err: any) {`, `:353` is `  }`, `:354` is `});` — copy all four as context.

```diff
@@ -350,5 +350,5 @@
     res.json({ success: true, secret: newSecret });
   } catch (err: any) {
-    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });
+    fail500(res, 'Webhook secret rotation failed (POST /api/webhooks/:id/rotate-secret)', err);
   }
 });
```

**Do NOT touch:**

- every line of `webhooks.ts` other than the 3 `-` line(s) above;
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

File: `Blockchain/Dev/services/originate/src/__tests__/ks1341b-webhooks-500-never-answers-err-message.test.ts` (NEW, 200 lines).
This service runs **jest** (ts-jest preset, `testEnvironment: 'node'`, `testMatch: ['**/__tests__/**/*.test.ts']` — read at
`Blockchain/Dev/services/originate/jest.config.js`), NOT vitest: `jest.mock`, `jest.fn`, `jest.requireMock`; `expect` takes ONE
argument. There is no database, no network beyond a loopback listener on 127.0.0.1, and no app boot: `../db`,
`../middleware/auth`, `@secuura/shared` (through `./helpers/sharedModuleMock`) and `../utils/logger` are all mocked, exactly as
in `ks1160-webhooks-post-persists-normalised-url.test.ts` lines 7-60 (the shape copied). To run the file alone, from
`Blockchain/Dev/services/originate`: `npx jest src/__tests__/ks1341b-webhooks-500-never-answers-err-message.test.ts`.

The cell shape (LEAK string · four NODE_ENVs · constant body · logger received the route context · REACHED) is copied from `ks730c-adminconfig-500-never-answers-err-message.test.ts` lines 58-127, including its lesson (the KS-730 PR3 trap): a LEAK containing `does not exist` was routed into a benign 200 branch there, so a clean body alone proved nothing. Here the LEAK contains neither `does not exist` nor any SQLSTATE that `utils/pgErrors.ts:36` (`KNOWN_PG_CODES`) would classify, and every red cell asserts the logger received THIS route's context with the thrown text — which only the converted catch does.

**REACHED is pinned PER ENVIRONMENT (gate 28, N-1288-2, MEASURED on part A).** Part A's A1 read `mockLoggerError.mock.calls.at(-1)` with no clear inside its NODE_ENV loop, so the production iteration's log call satisfied the development/test/unset iterations: a helper that logged only under `NODE_ENV==='production'` kept A1 green while a real probe went red 18 times. B1 therefore calls `mockLoggerError.mockClear()` at the TOP of each loop iteration and asserts the WHOLE call list for that environment is exactly `[[route.context, { error: LEAK }]]` (with `nodeEnv` in the compared object, so a failure names the environment). Do not "simplify" it back to `.at(-1)`.

**This file's own trap:** PATCH's catch (`webhooks.ts:318-:324`) sends a classified SQLSTATE to an honest 400 BEFORE the 500 line, so the LEAK carries no SQLSTATE and no `code`; 🟢 `B0` pins that branch. rotate-secret is driven by making `encryptField` throw (the shape the gate measured), so its cell never reaches the database.

Emit this text as the new-file hunk `@@ -0,0 +1,200 @@`, every line prefixed `+`, nothing added or dropped:

```ts
// KS-1341 part B (originate routes/webhooks.ts, PATCH /:id, DELETE /:id, POST /:id/rotate-secret):
// the three write routes answered a 500 whose body carried the thrown error's own text in every
// NODE_ENV. The 2026-09-26 gate MEASURED two of them in production: DELETE /:id returned the thrown
// text, and rotate-secret returned the field-encryption layer's internal configuration message.
// Part A added the fail500 helper; this part converts these three catch blocks to it and changes
// NOTHING on the secret path (generation, encryption, storage, the one-time return) - the last
// rotate-secret control pins that path end to end.
// Harness copied from ks1160-webhooks-post-persists-normalised-url.test.ts; cell shape from ks730c.
const mockExecuteRaw = jest.fn();
const mockExecuteRawUnsafe = jest.fn();
const mockLoggerError = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: jest.fn(),
    $executeRaw: mockExecuteRaw,
    $executeRawUnsafe: mockExecuteRawUnsafe,
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

const shared = jest.requireMock('@secuura/shared') as { encryptField: jest.Mock };

// THE FIXTURE IS LOAD-BEARING. It must not contain 'does not exist' (the KS-730 PR3 trap) and must
// carry no Postgres SQLSTATE token: PATCH's catch sends a classified SQLSTATE to an honest 400
// BEFORE the 500 line, so a LEAK carrying one would never reach the site under test.
const LEAK = 'PII encryption is not initialised: call registerKey() first ks1341b-private-detail';
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

// Each route is driven by making ITS OWN call throw, so a cell cannot pass because another handler
// answered. rotate-secret throws from encryptField, the shape the gate measured in production.
const ROUTES = [
  {
    label: 'PATCH /:id',
    method: 'PATCH',
    path: '/' + WEBHOOK_ID,
    body: { description: 'ks1341b' },
    arm: () => mockExecuteRawUnsafe.mockRejectedValueOnce(new Error(LEAK)),
    context: 'Webhook update failed (PATCH /api/webhooks/:id)',
  },
  {
    label: 'DELETE /:id',
    method: 'DELETE',
    path: '/' + WEBHOOK_ID,
    body: undefined,
    arm: () => mockExecuteRaw.mockRejectedValueOnce(new Error(LEAK)),
    context: 'Webhook delete failed (DELETE /api/webhooks/:id)',
  },
  {
    label: 'POST /:id/rotate-secret',
    method: 'POST',
    path: '/' + WEBHOOK_ID + '/rotate-secret',
    body: undefined,
    arm: () => shared.encryptField.mockImplementationOnce(() => { throw new Error(LEAK); }),
    context: 'Webhook secret rotation failed (POST /api/webhooks/:id/rotate-secret)',
  },
];

async function call(route: (typeof ROUTES)[number], nodeEnv: string | undefined): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  route.arm();
  const res = await fetch(baseUrl + '/api/webhooks' + route.path, {
    method: route.method,
    headers: { 'content-type': 'application/json' },
    ...(route.body === undefined ? {} : { body: JSON.stringify(route.body) }),
  });
  return { status: res.status, text: await res.text() };
}

describe('KS-1341 part B: PATCH, DELETE and rotate-secret never answer a 500 with the thrown text', () => {
  it.each(ROUTES)('RED KS-1341 B1 $label: the thrown message is not in the 500 body under production, development, test or unset', async (route) => {
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

  it.each(ROUTES)('RED KS-1341 B2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
    const reply = await call(route, 'production');
    expect(reply.status).toBe(500);
    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
  });

  it('control KS-1341 B0: a classified Postgres cast failure on PATCH still answers 400 and never reaches fail500', async () => {
    // PRE-EXISTING KS-445 branch this change must NOT alter (same error shape as ks445's own cell).
    setNodeEnv('production');
    mockExecuteRawUnsafe.mockRejectedValueOnce(
      Object.assign(new Error('Raw query failed. Code: `42804`. Message: `datatype mismatch`'), {
        code: 'P2010',
        meta: { code: '42804' },
      }),
    );
    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID, {
      method: 'PATCH',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ isActive: true }),
    });
    expect(res.status).toBe(400);
    expect(JSON.parse(await res.text()).error.code).toBe('VALIDATION_ERROR');
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 B: a rotate-secret that does NOT throw still encrypts, stores and returns the new secret once', async () => {
    // The secret path is OUT of scope and must be byte-for-byte unchanged: a fresh whsec_ secret,
    // encrypted with this row's AAD, stored, returned in the 200 body, and nothing logged.
    setNodeEnv('production');
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID + '/rotate-secret', { method: 'POST' });
    expect(res.status).toBe(200);
    const body = JSON.parse(await res.text());
    expect(body.success).toBe(true);
    expect(body.secret).toMatch(/^whsec_[0-9a-f]{48}$/);
    expect(shared.encryptField).toHaveBeenCalledWith(body.secret, 'svc_webhooks.secret.' + WEBHOOK_ID);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 B: a DELETE that does NOT throw answers 200 and logs nothing', async () => {
    // Without this, every "not leaked" pass above is consistent with the router answering 500 always.
    setNodeEnv('production');
    mockExecuteRaw.mockResolvedValueOnce(1);
    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID, { method: 'DELETE' });
    expect(res.status).toBe(200);
    expect(JSON.parse(await res.text())).toEqual({ success: true });
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 B: an authored 400 keeps its own text and logs nothing', async () => {
    // A pattern-malformed id is refused by the KS-431 guard with its own message, before any query.
    setNodeEnv('production');
    const res = await fetch(baseUrl + '/api/webhooks/bad%20id', { method: 'DELETE' });
    expect(res.status).toBe(400);
    expect(JSON.parse(await res.text()).error.message).toBe('Invalid webhook id format');
    expect(mockExecuteRaw).not.toHaveBeenCalled();
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1341 B: the LEAK string is the thrown text and dodges every benign branch', () => {
    // If LEAK were absent from the thrown error, every leaked: false above would hold trivially.
    expect(new Error(LEAK).message).toBe(LEAK);
    expect(LEAK.length).toBeGreaterThan(20);
    expect(LEAK).not.toContain('does not exist');
    expect(LEAK).not.toMatch(/\b(22P02|22001|22007|22008|22021|22P05|23502|23503|23505|23514|42804)\b/);
  });
});
```

## Red cells
- RED KS-1341 B1
- RED KS-1341 B2

(Title SUBSTRINGS, one per `it.each` row family: each matches the PATCH /:id, DELETE /:id and POST /:id/rotate-secret rows. These six cells go RED at the tip (`179a4f32`, part A merged) and GREEN with the fix; the five `control KS-1341 B…` cells are green at both. The builder's undeclared-red gate cannot see `it.each` titles, so this section is load-bearing.)

## Cells and controls

- 🔴 `RED KS-1341 B1 PATCH /:id: the thrown message is not in the 500 body under production, development, test or unset` — RED at the tip (the body carries LEAK)
- 🔴 `RED KS-1341 B1 DELETE /:id: the thrown message is not in the 500 body under production, development, test or unset` — RED at the tip (the body carries LEAK)
- 🔴 `RED KS-1341 B1 POST /:id/rotate-secret: the thrown message is not in the 500 body under production, development, test or unset` — RED at the tip (the body carries LEAK)
- 🔴 `RED KS-1341 B2 PATCH /:id: the thrown message is logged once, server-side, with this route named` — RED at the tip (nothing is logged)
- 🔴 `RED KS-1341 B2 DELETE /:id: the thrown message is logged once, server-side, with this route named` — RED at the tip (nothing is logged)
- 🔴 `RED KS-1341 B2 POST /:id/rotate-secret: the thrown message is logged once, server-side, with this route named` — RED at the tip (nothing is logged)
- 🟢 `control KS-1341 B0: a classified Postgres cast failure on PATCH still answers 400 and never reaches fail500`
- 🟢 `control KS-1341 B: a rotate-secret that does NOT throw still encrypts, stores and returns the new secret once`  ← the positive control, and the proof the secret path is unchanged
- 🟢 `control KS-1341 B: a DELETE that does NOT throw answers 200 and logs nothing`
- 🟢 `control KS-1341 B: an authored 400 keeps its own text and logs nothing`
- 🟢 `control KS-1341 B: the LEAK string is the thrown text and dodges every benign branch`

(`it.each` expands each 🔴 row into one test per route, named with the route label as shown.)

## The failing case (the "tamper")

After your change, in `Blockchain/Dev/services/originate/src/routes/webhooks.ts` line `:337` (DELETE /:id) reads `    fail500(res, 'Webhook delete failed (DELETE /api/webhooks/:id)', err);` — byte-unique in the post-change file (literal line-equality count 1, measured on the golden). Tamper: replace it with the original SITE line `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });` (4 leading spaces). Expected: `B1 DELETE /:id` and `B2 DELETE /:id` go RED; every 🟢 control stays GREEN. Restore → all GREEN.

**Arm R3 — production-only logging (rev B; the N-1288-2 regression arm, REQUIRED).** In the post-change file, line `:563` (inside `fail500`, unchanged by this brief) reads `  logger.error(context, { error: err instanceof Error ? err.message : String(err) });` — byte-unique (count 1 in the golden `webhooks.AB.ts`). Tamper: replace it with `  if (process.env.NODE_ENV === 'production') logger.error(context, { error: err instanceof Error ? err.message : String(err) });` (2 leading spaces). Expected: all three `B1` rows go RED (each fails at its `development` iteration: `calls: []` where one call is expected, and the failure names `nodeEnv: 'development'`); the three `B2` rows stay GREEN (they drive production only); every 🟢 control stays GREEN. **If any `B1` row stays green under this arm, the per-environment clear has been lost and the cell has regressed to part A's blindness — that is a FAIL of this brief, not a pass.** Restore → all GREEN.

## Premises (each one measured, with where)

- **Rev B:** origin develop = `179a4f32ec0643689b55a8d7207e63f6ec3d3831` (`git ls-remote`, 2026-09-26 18:1x; parent `a2a2b4c50d64` = #1288, part A). The object is NOT in the Blockchain checkout's store (that checkout's `origin/develop` is still `e080174c`), so it was read from a scratch bare repo shallow-fetched from the same remote (nothing written in the Secuura folder). At that sha `webhooks.ts` = golden `webhooks.A.ts` byte for byte, `ks1341a-…test.ts` = the golden A test byte for byte, and `sharedModuleMock.ts`, `utils/pgErrors.ts`, `utils/logger.ts`, `jest.config.js`, `package.json`, `encryptedField.ts` and `ks1160-…test.ts` have the same blob as at `e080174c` (the harness this test copies is unchanged).
- origin develop (rev 1) = `e080174c86c671349c508560744644fc0ef33388` — `git ls-remote origin refs/heads/develop` re-read at 2026-09-26 15:03:13 AEST (first read earlier this session, same sha); the object is in the local store (`git cat-file -t` → commit).
- The seven SITE lines, byte-identical, at `:200, :267, :325, :337, :352, :391, :416` — python line-equality count 7 on `git show e080174c86c6:Blockchain/Dev/services/originate/src/routes/webhooks.ts`; the gate lists the same seven (`report.md:372`).
- No catch in the file logs before answering: `webhooks.ts:199-201, :266-268, :314-326, :336-338, :351-353, :390-392, :415-417` read whole.
- `fail500` does not exist in the file at the tip — `grep -c -i fail500` → 0 (positive control: `grep -c -i webhooksrouter` → 10). `does not exist` occurs 0 times in the file (same instrument, `-i`).
- The helper text is copied from `routes/gdpr.ts:210-213` at the tip (2-space body; `systemErrors.ts:93-96` has the same body at 4-space).
- A function declaration used above its declaration is already the pattern in this file: `deliverWebhook` is called at `:378` and declared at `:427`. The lint config (`Blockchain/Dev/eslint.config.mjs:24-50, :78-96`) has no `no-use-before-define` rule; `js.configs.recommended` + `tseslint.configs.recommended` do not enable it (UNMEASURED by a lint run — see below).
- `Response` is the express type imported at `:11`; `logger` is imported at `:16`.
- `extractPgCode` (`utils/pgErrors.ts:48-72`) reads `err.code`, `err.meta.code`, then `KNOWN_PG_CODES` (`:36`) in the message — the LEAK strings match none (asserted by each file's last control).
- The six existing webhooks suites all mock `logger` WITH an `error` fn (`ks1160:33-35`, `ks423:42-44`, `ks431:21-23`, `ks444:61-63`, `ks445:28-30`, `ks914:25-27`), and none asserts a 500 body's message text; `ks445` "keeps 500 for genuinely unclassified failures" (`:136-141`) asserts status only, so it stays green.
- `encryptField` (`packages/shared/src/crypto/encryptedField.ts:315`) throws only key-state and context messages (`:286`, `:293`, `:301`, `:318`); `plaintext` appears at `:315`, `:316` and `:328` and in NONE of the thrown messages — so the text now LOGGED from rotate-secret's catch cannot carry the plaintext secret. The `UPDATE` at `:349` binds the ciphertext (`encrypted`), never `newSecret`.
- The golden (`golden/webhooks.A.ts`, `.AB.ts`, `.ABC.ts` and the three test files in the run directory) was BUILT and APPLIED: A → B → C apply with `git apply` strict (no `--recount`), reproduce the goldens byte for byte, and `typescript@5.9.3` `transpileModule` reports 0 syntactic diagnostics on all four files. The golden is for the checker, not shown to the model.
- After A+B+C, over non-comment lines: 0 lines match `/message: *err\??\.?message/`, 7 `fail500(res,` calls, 7 distinct contexts, 1 definition (measured on the golden; at A+B: 2 leaking, 5 calls).

## UNMEASURED — stated rather than glossed

- **The new test file was NOT run**, at the tip or after the fix — no jest, no type-check (`tsc`/ts-jest diagnostics), no lint. RED-at-tip and GREEN-after are REASONED from the source. The first checker run is the first execution.
- Type-level risks I could not rule out without ts-jest: the `it.each` row type inferred from a non-`as const` array with a union `body` field. (Rev B removed `mock.calls.at(-1)`; B1 now compares `{ nodeEnv, calls: mockLoggerError.mock.calls }`.)
- **Arm R3 was NOT executed.** That B1 reds and B2 stays green under production-only logging is REASONED from the cell (clear per iteration → an empty call list at `development`); the analogous blindness in part A's A1 was MEASURED by gate 28 (report `2026-09-26-batch1286-g28/report.md:281-290`).
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
- Sequencing: A → B → C, one at a time (the Spark runs one request at a time). This is brief B.

## Scope

Closes 3 of 7 sites. **Refs KS-1341, does NOT close it.** The ticket closes with brief C.

## Output

Exactly ONE fenced ```diff block, nothing outside it. First the product file (`--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts` / `+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts`, the 3 hunk(s) exactly as given, in file order), then the new test file (`--- /dev/null` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1341b-webhooks-500-never-answers-err-message.test.ts`, `@@ -0,0 +1,200 @@`). Paths exactly as written here. Every `+` line on its own physical line. Every context line keeps its leading space. Do not add, reorder, reword or reindent anything.
