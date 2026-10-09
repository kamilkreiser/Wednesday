/**
 * =============================================================================
 * KS-1129 — the KS-584 heal must PERSIST a number, not the raw pg BIGINT string
 * =============================================================================
 * `block_number` is a BIGINT and `pg` returns int8 as a STRING by default; there is no int8 parser
 * anywhere in Blockchain/Dev. #1220 fixed the anchoring side so its verify body reports a number,
 * but the heal path in originate must not depend on that: whatever `confirmStalePendingAnchor`
 * composes is handed to `persistHealedAnchor`, which WRITES it to the document blob. The gateway's
 * tier-1 read then refuses a string (`typeof persistedBlockHeight === 'number'`), so a healed
 * document answers off-chain-only for a document that IS on chain.
 *
 * WHY THIS FILE EXISTS AT ALL, and it is the thing to read before trusting any cell here:
 * NO test file in this suite names `persistHealedAnchor`, and the closest sibling
 * (`ks584-p3-verify-list.test.ts`) cannot reach the write — its row fixture carries no `tenant_id`,
 * so `persistHealedAnchor` returns at `if (!docId || !tenant) return;` before calling
 * `updateDocument`. That is why its incomplete `documentRepo` mock never blows up. A cell copied from
 * it would assert a property of a write THAT NEVER HAPPENED, and would pass for that reason.
 *
 * So every cell below asserts the write was REACHED before it asserts anything about its content,
 * and the last cell is the CONTROL for exactly that: with `tenant_id` removed, `updateDocument` is
 * not called at all — which is what makes "called exactly once" load-bearing rather than decorative.
 * =============================================================================
 */

process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();
const mockUpdateDocument = jest.fn().mockResolvedValue(undefined);

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
  updateDocument: mockUpdateDocument,
}));

import express from 'express';
import type { Server } from 'http';
import { verificationV2Router } from '../routes/verificationV2';
import { verificationRouter, toBlockHeight } from '../routes/verification';

const HASH = 'f'.repeat(64);
const REAL_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
const TENANT = '11111111-2222-4333-8444-555555555555';

/** A registration whose blob is STALE 'pending' with a REAL tx — the heal precondition. */
function staleRow(over: Record<string, unknown> = {}) {
  return {
    id: '11111111-1111-1111-1111-111111111111',
    external_id: 'doc-1754000000000-original',
    // tenant_id is REQUIRED for persistHealedAnchor to reach updateDocument. The sibling fixture
    // omits it, which is precisely why the sibling cannot observe the write.
    tenant_id: TENANT,
    title: 'Grad cert',
    document_type: 'DOCUMENT',
    content_hash: HASH,
    status: 'anchored',
    certification_metadata: { blockchain: { txHash: REAL_TX, status: 'pending' } },
    metadata: {},
    created_at: '2026-08-01T00:00:00.000Z',
    certified_at: null,
    organization_name: 'Acme Ltd',
    ...over,
  };
}

const app = express();
app.use(express.json());
app.use('/api/v2/verification', verificationV2Router);
// BOTH routers are mounted on purpose. v1 heals through `confirmStalePendingAnchor` and v2 through
// `healBlobWithChainFact` - two near-duplicate compositions, each feeding `persistHealedAnchor`. A
// cell on one says nothing about the other, and the ticket names only v1's.
app.use('/api/verification', verificationRouter);

const realFetch = global.fetch;
let server: Server;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(async () => {
  global.fetch = realFetch;
  await new Promise<void>((resolve) => server.close(() => resolve()));
});

beforeEach(() => {
  mockQueryRaw.mockReset();
  mockUpdateDocument.mockReset().mockResolvedValue(undefined);
  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
});

async function verifyV1(body: Record<string, unknown>): Promise<{ status: number; body: any }> {
  const res = await realFetch(`${baseUrl}/api/verification/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return { status: res.status, body: await res.json() };
}

async function verifyV2(body: Record<string, unknown>): Promise<{ status: number; body: any }> {
  const res = await realFetch(`${baseUrl}/api/v2/verification/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return { status: res.status, body: await res.json() };
}

/** The blob handed to updateDocument on its single call. */
function persistedBlob(): Record<string, unknown> {
  expect(mockUpdateDocument).toHaveBeenCalledTimes(1);
  const [, , updates] = mockUpdateDocument.mock.calls[0];
  return (updates as { blockchain: Record<string, unknown> }).blockchain;
}

describe('KS-1129 — what the heal path PERSISTS', () => {
  it('KS-1129 PERSISTSANUMBER: a stale pending blob healed through a STRING blockNumber persists a number', async () => {
    mockQueryRaw.mockResolvedValue([staleRow()]);
    const fetchMock = jest.fn().mockResolvedValue({
      ok: true,
      // the shape anchoring's DB leg produces when pg hands back a raw int8: a STRING
      json: async () => ({ verified: true, txHash: REAL_TX, blockNumber: '4242', network: 'preview' }),
    });
    global.fetch = fetchMock as unknown as typeof fetch;

    const { body } = await verifyV2({ contentHash: HASH });

    // THE WRITE WAS REACHED, and the stub was CONSUMED. Both come before the content assertion:
    // without them, "blockHeight is a number" is satisfied by a write that never happened.
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const blob = persistedBlob();
    expect([
      typeof blob.blockHeight,
      blob.blockHeight,
      blob.status,
      body.matches[0].blockchain.status,
    ]).toEqual(['number', 4242, 'confirmed', 'confirmed']);
  });

  it('KS-1129 CONTROL-REACHED: with tenant_id absent the write is NOT reached, so "called once" is load-bearing', async () => {
    // The sibling fixture's shape. If this cell ever passes with updateDocument called, the
    // precondition above has stopped discriminating and PERSISTSANUMBER has gone vacuous.
    const noTenant = staleRow();
    delete (noTenant as Record<string, unknown>).tenant_id;
    mockQueryRaw.mockResolvedValue([noTenant]);
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ verified: true, txHash: REAL_TX, blockNumber: '4242', network: 'preview' }),
    }) as unknown as typeof fetch;

    const { body } = await verifyV2({ contentHash: HASH });
    // The heal still PRESENTS as confirmed — it is only the write that is skipped.
    expect([mockUpdateDocument.mock.calls.length, body.matches[0].blockchain.status])
      .toEqual([0, 'confirmed']);
  });

  it('KS-1129 V1PERSISTSANUMBER: the v1 heal path also persists a number — a SEPARATE composition from v2', async () => {
    mockQueryRaw.mockResolvedValue([staleRow()]);
    const fetchMock = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ verified: true, txHash: REAL_TX, blockNumber: '4242', network: 'preview' }),
    });
    global.fetch = fetchMock as unknown as typeof fetch;

    const { body } = await verifyV1({ contentHash: HASH });

    expect(fetchMock).toHaveBeenCalledTimes(1);
    const blob = persistedBlob();
    expect([typeof blob.blockHeight, blob.blockHeight, blob.status, body.blockchain.status])
      .toEqual(['number', 4242, 'confirmed', 'confirmed']);
  });

  it('KS-1129 COERCION: toBlockHeight refuses what would otherwise be persisted, and preserves a real 0', () => {
    expect([
      toBlockHeight('4242'),      // the raw pg int8 string — the defect
      toBlockHeight(4242),        // already a number — unchanged
      toBlockHeight(0),           // a legitimate height, NOT dropped
      toBlockHeight('0'),
      toBlockHeight(''),          // never Number('') === 0
      toBlockHeight('   '),
      toBlockHeight('abc'),       // never NaN
      toBlockHeight(null),
      toBlockHeight(undefined),
      toBlockHeight({}),
      toBlockHeight(NaN),
      toBlockHeight(Infinity),
    ]).toEqual([4242, 4242, 0, 0, null, null, null, null, null, null, null, null]);
  });

  it('KS-1129 FALLTHROUGH: an unusable chain height falls through to the STORED height rather than fabricating 0', async () => {
    mockQueryRaw.mockResolvedValue([
      staleRow({ certification_metadata: { blockchain: { txHash: REAL_TX, status: 'pending', blockHeight: 99 } } }),
    ]);
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ verified: true, txHash: REAL_TX, blockNumber: '', network: 'preview' }),
    }) as unknown as typeof fetch;

    await verifyV2({ contentHash: HASH });
    const blob = persistedBlob();
    expect([typeof blob.blockHeight, blob.blockHeight]).toEqual(['number', 99]);
  });
});
