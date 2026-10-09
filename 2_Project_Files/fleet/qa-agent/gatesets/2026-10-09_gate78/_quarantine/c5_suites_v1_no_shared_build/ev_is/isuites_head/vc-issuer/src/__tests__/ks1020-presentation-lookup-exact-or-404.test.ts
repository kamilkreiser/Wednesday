/**
 * KS-1020 — GET /api/presentations/:id is an EXACT lookup or a 404.
 *
 * The defect (routes/presentations.ts, getPresentation): when the exact lookup
 * found nothing, the function fell back to `WHERE id LIKE '%<id>%' LIMIT 1` on
 * the DB path and to a `key.includes(id)` scan on the in-memory path, so an id
 * that names nothing (`0`, `abc`, `..`, `1`, `a`, `e`) resolved to an arbitrary
 * stored presentation with no ownership check. Ticket recommendation item 1,
 * verbatim: "Delete the LIKE fallback and the includes() scan. An id lookup is
 * exact or it is 404. There is no legitimate caller who knows a fragment of an
 * id and not the id."
 *
 * Two describes, one per storage path, on the ks444 harness (real
 * presentationRoutes router + real shared errorHandler, hand-rolled req/res).
 * Every cell title starts with its id (P1, N1, M1…, F1…, Q1, P2, D1…, C1, S1)
 * so a tamper run can be scored cell by cell.
 *
 *  - MEMORY path (isDbAvailable() false): one row is seeded through the real
 *    POST / (id shape `${VC_BASE_URL}/presentations/<uuid>`). VC_BASE_URL is
 *    pinned to `https://abc0.issuer1.example` so that five of the ticket's six
 *    ids (`0`, `abc`, `1`, `a`, `e`) are substrings of the stored id whatever
 *    the random uuid is — with the default `https://secuura.io` base only `a`
 *    and `e` are certain; `0` and `1` depend on the uuid's hex (measured: `0`
 *    flipped between two runs). `..` can never occur in a minted id, so that
 *    cell is green on both sides of the fix. Partials taken FROM the stored id
 *    (`presentations`, the host fragment, the uuid's first four hex, the bare
 *    uuid) are red at base by construction. The exact id, URL-encoded because
 *    it carries `/` and `:`, is the 200 control.
 *  - DB path (isDbAvailable() true, `query` mocked with a model of `=` and of
 *    a `%`-wrapped substring LIKE over one fixed row; `_`, interior `%` and
 *    escapes are not modelled): an unknown id must cost
 *    exactly ONE query whose SQL is the exact `WHERE id = $1` and never a LIKE,
 *    and answer 404. Those two cells (C1, S1) cannot be satisfied by a lucky
 *    id.
 *
 * Item 2 of the ticket (an ownership/tenant check) is NOT covered here.
 */

import { describe, it, expect, beforeAll, beforeEach, vi } from 'vitest';

// Controllable stand-ins for ../db — each describe scripts its own behaviour.
// vi.hoisted so the mock factory (hoisted above imports) can reach them.
const dbMock = vi.hoisted(() => ({
  isDbAvailable: vi.fn<() => boolean>(() => false),
  query: vi.fn<(sql: string, params?: unknown[]) => Promise<{ rows: any[] }>>(),
}));

vi.mock('../db', () => ({
  isDbAvailable: () => dbMock.isDbAvailable(),
  query: (sql: string, params?: unknown[]) => dbMock.query(sql, params),
}));

// Silence the winston logger the way db.retry.test.ts does.
vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
}));

type Router = (rq: any, rs: any, nx: (e?: unknown) => void) => void;
type Mods = { router: Router; errorHandler: any };

/** Fresh router + errorHandler per describe, so memPresentationStore starts empty. */
async function freshModules(): Promise<Mods> {
  vi.resetModules();
  const { presentationRoutes } = await import('../routes/presentations');
  const { errorHandler } = await import('../middleware/errorHandler');
  return { router: presentationRoutes as unknown as Router, errorHandler };
}

/**
 * Dispatch through the real Express router with a mocked req/res pair; route
 * errors flow into the real shared errorHandler exactly as in index.ts
 * (same shape as ks444.requestSchema.test.ts).
 */
function dispatch(mods: Mods, method: string, url: string, body?: unknown): Promise<{ status: number; body: any }> {
  return new Promise((resolve, reject) => {
    const req: any = { method, url, baseUrl: '', originalUrl: url, headers: {}, body };
    const res: any = {
      statusCode: 200,
      status(code: number) {
        this.statusCode = code;
        return this;
      },
      json(payload: unknown) {
        resolve({ status: this.statusCode, body: payload });
        return this;
      },
    };
    const next = (err?: unknown) => {
      if (err) mods.errorHandler(err as Error, req, res, () => {});
      else reject(new Error(`route did not match ${method} ${url}`));
    };
    mods.router(req, res, next);
  });
}

/** GET /:id with the id URL-encoded (Express decodes route params). */
function getById(mods: Mods, id: string) {
  return dispatch(mods, 'GET', `/${encodeURIComponent(id)}`);
}

/** A minimal spec-complete W3C VC item for the create-presentation payload. */
function baseCredential(): Record<string, unknown> {
  return {
    '@context': ['https://www.w3.org/2018/credentials/v1'],
    id: 'urn:uuid:ks1020-test-credential',
    type: ['VerifiableCredential'],
    issuer: 'did:prism:secuura_test_issuer',
    issuanceDate: '2026-01-01T00:00:00Z',
    credentialSubject: { documentHash: 'ab'.repeat(32) },
  };
}

const NOT_FOUND = { status: 404, code: 'NOT_FOUND', message: 'Presentation not found' };

function expectNotFound(r: { status: number; body: any }) {
  expect(r.status).toBe(NOT_FOUND.status);
  expect(r.body?.error?.code).toBe(NOT_FOUND.code);
  expect(r.body?.error?.message).toBe(NOT_FOUND.message);
  expect(r.body?.presentation).toBeUndefined();
}

describe('KS-1020 — memory path (isDbAvailable() false): exact id or 404', () => {
  // See the header: five of the six ticket ids are substrings of this base
  // whatever uuid POST / mints, so the base-red outcome does not depend on hex luck.
  const VC_BASE_URL = 'https://abc0.issuer1.example';
  let mods: Mods;
  let storedId: string;
  let uuid: string;

  beforeAll(async () => {
    process.env.VC_BASE_URL = VC_BASE_URL;
    dbMock.isDbAvailable.mockReturnValue(false);
    dbMock.query.mockReset();
    mods = await freshModules();
    // Seed one real row through the real POST / (no holderDID → no signing gate).
    const created = await dispatch(mods, 'POST', '/', { credentials: [baseCredential()] });
    expect(created.status).toBe(201);
    storedId = created.body.presentation.id;
    expect(storedId).toMatch(new RegExp(`^${VC_BASE_URL.replace(/[.]/g, '\\.')}/presentations/[0-9a-f-]{36}$`));
    uuid = storedId.slice(storedId.lastIndexOf('/') + 1);
  });

  it('P1 positive control: the exact stored id (URL-encoded) → 200 with that presentation', async () => {
    const r = await getById(mods, storedId);
    expect(r.status).toBe(200);
    expect(r.body?.presentation?.id).toBe(storedId);
  });

  it('N1 negative control: an id in neither store → 404 "Presentation not found"', async () => {
    const absent = `${VC_BASE_URL}/presentations/00000000-0000-4000-8000-000000000000`;
    expect(absent).not.toBe(storedId);
    expectNotFound(await getById(mods, absent));
  });

  it.each([
    ['M1', '0'],
    ['M2', 'abc'],
    ['M3', '..'],
    ['M4', '1'],
    ['M5', 'a'],
    ['M6', 'e'],
  ])('%s ticket id %j → 404, never the stored presentation', async (_cell, id) => {
    // Every ticket id but `..` is a substring of the stored id (a fragment, not the id).
    expect(storedId.includes(id)).toBe(id !== '..');
    expectNotFound(await getById(mods, id));
  });

  it.each([
    ['F1', 'path segment', () => 'presentations'],
    ['F2', 'host fragment', () => 'issuer1'],
    ['F3', 'uuid first four hex', () => uuid.slice(0, 4)],
    ['F4', 'bare uuid', () => uuid],
  ])('%s partial taken from the stored id (%s) → 404', async (_cell, _label, pick) => {
    const id = pick();
    expect(storedId.includes(id)).toBe(true); // the partial really is a fragment of the stored id
    expect(id).not.toBe(storedId);
    expectNotFound(await getById(mods, id));
  });

  // KS-1120 F-1 (QA-966 F-1). Every partial above is a SUFFIX or a MIDDLE of the
  // stored id; none is a PREFIX. So a `startsWith` scan re-inserted after the exact
  // get runs this whole file green while `GET /https%3A%2F%2Fabc0.issuer1.example`
  // answers 200 again. This is the prefix arm. It is red under the gate's tamper T4
  // and under nothing else here, because no other id in this file is a prefix of the
  // stored id. The startsWith assertion is the input check: without it the cell could
  // pass on an id that is not a prefix at all, which would pin nothing.
  it('X1 a PREFIX of the stored id (the VC base URL) -> 404, never the stored presentation', async () => {
    const id = VC_BASE_URL;
    expect(storedId.startsWith(id)).toBe(true);
    expect(id).not.toBe(storedId);
    expectNotFound(await getById(mods, id));
  });

  it('Q1 the DB is never queried on the memory path', () => {
    expect(dbMock.query).not.toHaveBeenCalled();
  });
});

describe('KS-1020 — DB path (isDbAvailable() true): one exact query, never a LIKE, 404', () => {
  const STORED_ID = 'https://secuura.io/presentations/0abc1e2d-4f5a-4b6c-8d7e-9f0a1b2c3d4e';
  const ROW = { presentation: { id: STORED_ID, type: ['VerifiablePresentation'], verifiableCredential: [] } };
  let mods: Mods;

  /**
   * A model of `=` and of a `%`-wrapped substring LIKE over the one stored row;
   * `_`, interior `%` and escapes are not modelled. Here `%` at either
   * end of the pattern is a wildcard, no `%` means an exact comparison — so a
   * `LIKE '%0%'` matches the row and a `LIKE '0'` does not.
   */
  function pgModel(sql: string, params?: unknown[]): Promise<{ rows: any[] }> {
    const p = String(params?.[0] ?? '');
    let hit: boolean;
    if (/\bLIKE\b/i.test(sql)) {
      const open = p.startsWith('%');
      const close = p.endsWith('%');
      const needle = p.slice(open ? 1 : 0, close ? -1 : undefined);
      hit = open && close ? STORED_ID.includes(needle)
        : open ? STORED_ID.endsWith(needle)
        : close ? STORED_ID.startsWith(needle)
        : STORED_ID === needle;
    } else {
      hit = p === STORED_ID;
    }
    return Promise.resolve({ rows: hit ? [ROW] : [] });
  }

  beforeAll(async () => {
    dbMock.isDbAvailable.mockReturnValue(true);
    mods = await freshModules(); // memPresentationStore empty: nothing to fall back to
  });

  beforeEach(() => {
    dbMock.query.mockReset();
    dbMock.query.mockImplementation(pgModel);
  });

  it('P2 positive control: the exact stored id → 200 from a single exact query', async () => {
    const r = await getById(mods, STORED_ID);
    expect(r.status).toBe(200);
    expect(r.body?.presentation?.id).toBe(STORED_ID);
    expect(dbMock.query).toHaveBeenCalledTimes(1);
  });

  it.each([
    ['D1', '0'],
    ['D2', 'abc'],
    ['D3', '..'],
    ['D4', '1'],
    ['D5', 'a'],
    ['D6', 'e'],
  ])('%s ticket id %j → 404 (the model answers a wildcard LIKE, so a LIKE is the only way to 200)', async (_cell, id) => {
    expect(STORED_ID.includes(id)).toBe(id !== '..');
    expectNotFound(await getById(mods, id));
  });

  it('C1 an unknown id costs exactly ONE query', async () => {
    expectNotFound(await getById(mods, '0'));
    expect(dbMock.query).toHaveBeenCalledTimes(1);
  });

  it('S1 every SQL issued for an unknown id is the exact lookup: "WHERE id = $1", never LIKE, the id itself as the parameter', async () => {
    await getById(mods, '0');
    const calls = dbMock.query.mock.calls;
    expect(calls.length).toBeGreaterThan(0);
    for (const [sql, params] of calls) {
      expect(String(sql)).toMatch(/WHERE id = \$1/);
      expect(String(sql)).not.toMatch(/\bLIKE\b/i);
      expect(params).toEqual(['0']);
    }
  });

  // KS-1120 F-2 (QA-966 F-2). No cell here constructs a row that is PRESENT in memory
  // and ABSENT from the DB, so `return undefined` after the DB miss -- skipping the
  // memory get -- runs this whole file green while a memory-only row flips 200 -> 404.
  // The row is made memory-only by rejecting the INSERT, which is storePresentation's
  // real catch at routes/presentations.ts:104-106, not a contrived state. Red under
  // the gate's tamper T5 and under nothing else here: every other DB cell either hits
  // the DB row before that point (P2) or expects the 404 that T5 produces.
  it('X2 a row in memory and absent from the DB -> 200 from the memory get, at the cost of one exact query', async () => {
    dbMock.query.mockImplementation((sql: string, params?: unknown[]) =>
      /INSERT\s+INTO\s+vc_presentations_store/i.test(String(sql))
        ? Promise.reject(new Error('KS-1120 F-2: INSERT rejected, so the row is memory-only'))
        : pgModel(String(sql), params));

    const created = await dispatch(mods, 'POST', '/', { credentials: [baseCredential()] });
    expect(created.status).toBe(201);
    const memoryOnlyId: string = created.body.presentation.id;
    expect(typeof memoryOnlyId).toBe('string');
    expect(memoryOnlyId.length).toBeGreaterThan(0);

    // The INSERT really was attempted and really was rejected; without this the cell
    // could be measuring a row the DB never refused.
    const inserts = dbMock.query.mock.calls.filter((c) =>
      /INSERT\s+INTO\s+vc_presentations_store/i.test(String(c[0])));
    expect(inserts.length).toBe(1);
    // ...and the row really is absent from the DB model, so 200 can only come from memory.
    await expect(
      pgModel('SELECT presentation FROM vc_presentations_store WHERE id = $1', [memoryOnlyId]),
    ).resolves.toEqual({ rows: [] });

    dbMock.query.mockClear();
    const r = await getById(mods, memoryOnlyId);
    expect(r.status).toBe(200);
    expect(r.body?.presentation?.id).toBe(memoryOnlyId);
    expect(dbMock.query).toHaveBeenCalledTimes(1);
    const [sql, params] = dbMock.query.mock.calls[0];
    expect(String(sql)).toMatch(/WHERE id = \$1/);
    expect(String(sql)).not.toMatch(/\bLIKE\b/i);
    expect(params).toEqual([memoryOnlyId]);
  });
});
