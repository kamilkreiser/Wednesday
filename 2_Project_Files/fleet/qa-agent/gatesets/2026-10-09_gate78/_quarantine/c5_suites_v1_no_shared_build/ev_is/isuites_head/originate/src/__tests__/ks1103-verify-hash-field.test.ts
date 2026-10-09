/**
 * =============================================================================
 * KS-1103 — POST /api/verification/verify reads the published `hash` field
 * =============================================================================
 * The served spec's `VerifyRequest` publishes `documentId`, `hash`, `title` and
 * `contentHash`. KS-222 made the validator chain check `hash` as a string, but
 * the handler never read it: `hashToVerify` was built from `providedHash`,
 * `contentHash` and `documentHash` only, so a spec-valid body carrying only
 * `hash` was refused with 400 "Please provide a content hash…" while the same
 * value sent as `contentHash` answered 200 (found by the kintsugi deploy gate on
 * 4554b25e2, finding F-4).
 *
 * These cells pin the fix:
 *   - `hash` alone answers exactly as `contentHash` alone does (H1/H2 vs C1/C2);
 *   - `hash` is read LAST in the alias chain, so a body carrying a pre-existing alias
 *     keeps its answer — the lookup sees the pre-existing alias, never `hash`,
 *     when both are present (P1/P2);
 *   - narrowed (KS-1118 F-3): every body carrying a pre-existing alias keeps its
 *     lookup value; documentId-only, documentData-only and alias bodies are
 *     unchanged; a body pairing `hash` with `documentId` or `documentData` now
 *     takes the hash strategy, as v2 already does -- no caller in the repo sends
 *     that pairing;
 *   - both 400 messages now name every field they accept (V1, E4);
 *   - a malformed `hash` value now reaches the lookup like any other alias and
 *     answers 200 verified:false — measured on the after-model before the fix
 *     (a malformed `contentHash` on develop b1cb8466f), not a prediction (E2);
 *   - the empty string is falsy in the chain, so `{hash:''}` stays 400 (E1).
 *
 * Harness: ks584-verify-row-selection's (NODE_ENV=development, DATABASE_URL shim,
 * `../db` mocked to `$queryRaw`, auth passthrough, the hand-written
 * `@secuura/shared` mock, `documentRepo` mocked, `global.fetch` rejected).
 * =============================================================================
 */

process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw },
  getTenantManager: () => null,
}));

jest.mock('../middleware/auth', () => ({
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
    queryWithTenantGuc: jest.fn(),
  }),
);

jest.mock('../repositories/documentRepo', () => ({
  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
  MAX_LINEAGE_DEPTH: 10,
}));

import express from 'express';
import { verificationRouter } from '../routes/verification';

const HASH = 'f'.repeat(64);
const OTHER = 'e'.repeat(64);
const REAL_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
const DOC_ID = 'doc-1754000000000-original';

/** The messages the fix introduces. Both keep the word "hash" (e2e-v2 matches on it). */
const MSG_MISSING =
  'Please provide a documentId, a content hash (hash, contentHash, providedHash or documentHash), or documentData.';
const MSG_INVALID =
  'Invalid request body: documentId, hash, title, contentHash, providedHash and documentHash must be strings; documentData must be an object.';
const MSG_NOT_REGISTERED = 'This document hash is not registered.';

/** A registration with a real confirmed anchor. */
function anchoredRow(): Record<string, unknown> {
  return {
    id: '11111111-1111-1111-1111-111111111111',
    external_id: DOC_ID,
    title: 'Grad cert',
    document_type: 'DOCUMENT',
    content_hash: HASH,
    status: 'anchored',
    certification_metadata: { blockchain: { txHash: REAL_TX, status: 'confirmed', blockHeight: 4547897 } },
    metadata: {},
    created_at: '2026-08-01T00:00:00.000Z',
    certified_at: null,
    organization_name: 'Acme Ltd',
  };
}

const app = express();
app.use(express.json());
app.use('/api/verification', verificationRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen> | undefined;
const realFetch = global.fetch;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server?.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => {
  if (server) server.close();
  global.fetch = realFetch;
});

beforeEach(() => {
  mockQueryRaw.mockReset();
  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
});

interface Answer {
  status: number;
  json: Record<string, unknown>;
  lookups: number;
  sawHASH: boolean;
  sawOTHER: boolean;
}

/** POST a body with the DB returning `rows`; report the answer and what the lookup saw. */
async function verify(body: unknown, rows: 'none' | 'anchored'): Promise<Answer> {
  mockQueryRaw.mockReset();
  mockQueryRaw.mockResolvedValue(rows === 'anchored' ? [anchoredRow()] : []);
  const res = await realFetch(`${baseUrl}/api/verification/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const json = (await res.json()) as Record<string, unknown>;
  const values = mockQueryRaw.mock.calls.flatMap((c: unknown[]) => c.slice(1)).map((v: unknown) => String(v));
  return {
    status: res.status,
    json,
    lookups: mockQueryRaw.mock.calls.length,
    sawHASH: values.some((v) => v.includes(HASH)),
    sawOTHER: values.some((v) => v.includes(OTHER)),
  };
}

/** The fields H1/H2 must share with C1/C2. */
function compared(a: Answer) {
  return {
    status: a.status,
    verified: a.json.verified,
    checks: a.json.checks,
    documentId: a.json.documentId,
    error: a.json.error,
  };
}

describe('KS-1103 — /verify reads the published hash field', () => {
  // ---------------------------------------------------------------------------
  // RED at base, GREEN after the fix
  // ---------------------------------------------------------------------------
  it('H1 {hash} with no rows answers exactly as {contentHash} does and the lookup saw the hash', async () => {
    const c1 = await verify({ contentHash: HASH }, 'none');
    const h1 = await verify({ hash: HASH }, 'none');
    expect(compared(h1)).toEqual(compared(c1));
    expect(h1.status).toBe(200);
    expect(h1.lookups).toBe(1);
    expect(h1.sawHASH).toBe(true);
  });

  it('H2 {hash} with an anchored row answers exactly as {contentHash} does', async () => {
    const c2 = await verify({ contentHash: HASH }, 'anchored');
    const h2 = await verify({ hash: HASH }, 'anchored');
    expect(compared(h2)).toEqual(compared(c2));
    expect(h2.status).toBe(200);
    expect(h2.json.verified).toBe(true);
    expect(h2.json.documentId).toBe(DOC_ID);
    expect(h2.sawHASH).toBe(true);
  });

  it('V1 {hash:{}} is refused with 400 naming every string field', async () => {
    const v1 = await verify({ hash: {} }, 'none');
    expect(v1.status).toBe(400);
    expect(v1.json.verified).toBe(false);
    expect(v1.json.error).toBe(MSG_INVALID);
    expect(v1.lookups).toBe(0);
  });

  it('E4 {} is refused with 400 naming every accepted hash field', async () => {
    const e4 = await verify({}, 'none');
    expect(e4.status).toBe(400);
    expect(e4.json.verified).toBe(false);
    expect(e4.json.error).toBe(MSG_MISSING);
    expect(e4.lookups).toBe(0);
  });

  it('E2 a malformed {hash} reaches the lookup and answers 200 verified:false (the measured after-model)', async () => {
    const e2 = await verify({ hash: '!!! not a hash !!!' }, 'none');
    expect(e2.status).toBe(200);
    expect(e2.json.verified).toBe(false);
    expect(e2.lookups).toBe(1);
    expect(String(e2.json.error)).toContain(MSG_NOT_REGISTERED);
  });

  // ---------------------------------------------------------------------------
  // GREEN on both sides -- every body carrying a pre-existing alias keeps its answer
  // ---------------------------------------------------------------------------
  it('C1 {contentHash} with no rows answers 200 verified:false from one lookup', async () => {
    const c1 = await verify({ contentHash: HASH }, 'none');
    expect(c1.status).toBe(200);
    expect(c1.json.verified).toBe(false);
    expect(String(c1.json.error)).toContain(MSG_NOT_REGISTERED);
    expect(c1.lookups).toBe(1);
    expect(c1.sawHASH).toBe(true);
  });

  it('C2 {contentHash} with an anchored row answers 200 verified:true', async () => {
    const c2 = await verify({ contentHash: HASH }, 'anchored');
    expect(c2.status).toBe(200);
    expect(c2.json.verified).toBe(true);
    expect(c2.json.documentId).toBe(DOC_ID);
  });

  it('C3 {providedHash} with no rows answers 200 verified:false', async () => {
    const c3 = await verify({ providedHash: HASH }, 'none');
    expect(c3.status).toBe(200);
    expect(c3.json.verified).toBe(false);
    expect(c3.sawHASH).toBe(true);
  });

  it('C4 {documentHash} with no rows answers 200 verified:false', async () => {
    const c4 = await verify({ documentHash: HASH }, 'none');
    expect(c4.status).toBe(200);
    expect(c4.json.verified).toBe(false);
    expect(c4.sawHASH).toBe(true);
  });

  it('I1 {documentId} with no rows answers 200 "Document not found in the registry"', async () => {
    const i1 = await verify({ documentId: DOC_ID }, 'none');
    expect(i1.status).toBe(200);
    expect(i1.json.verified).toBe(false);
    expect(i1.json.error).toBe('Document not found in the registry');
  });

  it('P1 {contentHash:A, hash:B} — the lookup sees A only (hash is read last)', async () => {
    const p1 = await verify({ contentHash: HASH, hash: OTHER }, 'none');
    expect(p1.status).toBe(200);
    expect(p1.sawHASH).toBe(true);
    expect(p1.sawOTHER).toBe(false);
  });

  it('P2 {providedHash:A, hash:B} — the lookup sees A only (hash is read last)', async () => {
    const p2 = await verify({ providedHash: HASH, hash: OTHER }, 'none');
    expect(p2.status).toBe(200);
    expect(p2.sawHASH).toBe(true);
    expect(p2.sawOTHER).toBe(false);
  });

  it('E1 {hash:""} stays 400 with no lookup (the empty string is falsy in the chain)', async () => {
    const e1 = await verify({ hash: '' }, 'none');
    expect(e1.status).toBe(400);
    expect(e1.lookups).toBe(0);
  });

  it('E3 {title} alone stays 400 (status only — the title-only contract is a separate ticket)', async () => {
    const e3 = await verify({ title: 'x' }, 'none');
    expect(e3.status).toBe(400);
  });
});
