/**
 * =============================================================================
 * KS-584 P3 — the /v2 verify-list contract
 * =============================================================================
 * v1 collapses the same-hash registration set to ONE row (deterministically,
 * since the interim). v2 dissolves the selection problem: every registration
 * answers as its own match, and anchor truth is CALLER-INDEPENDENT — the
 * chain-fact read forwards NO caller bearer (QA finding 2026-08-11: v1's heal
 * forwarded the caller's Authorization to anchoring's authed endpoint, so
 * anonymous/invalid-token callers got a false-negative isAnchored while
 * authenticated callers got the truth; Kam ruled anonymous verify a supported
 * public path).
 *
 * These tests pin:
 *   - multiplicity: every same-hash registration is returned, each standing
 *     on its own evidence (no sibling certification smear);
 *   - presentation order: certified → confirmed on-chain → in-flight →
 *     oldest, so matches[0] is v1's answer for the same hash;
 *   - KS-522: a simulated anchor makes no on-chain claim in any match;
 *   - caller-independent heal: the chain-fact request carries NO
 *     Authorization header, whatever the caller sent;
 *   - heal attribution: same-tx OR same-registration confirms; a confirmed
 *     tx for a DIFFERENT registration never heals this one;
 *   - chain economy (KS-252): no chain call when every anchor is settled;
 *   - chain-only fallback and the honest count:0 "never registered" answer;
 *   - KS-584 tenant scoping with the explicit fieldsWithheld marker;
 *   - auth wiring: the router mounts authenticate({required:false}) —
 *     ABSENT token → anonymous pass-through, PRESENT-but-invalid → 401
 *     (the middleware's own contract, live-proven on the stack).
 * =============================================================================
 */

process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();
const mockAuthenticateCalls: unknown[] = [];

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw },
  getTenantManager: () => null,
}));

jest.mock('../middleware/auth', () => ({
  authenticate: (opts?: unknown) => {
    mockAuthenticateCalls.push(opts);
    return (_req: unknown, _res: unknown, next: () => void) => next();
  },
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
  updateDocument: jest.fn().mockResolvedValue(undefined),
  MAX_LINEAGE_DEPTH: 10,
}));

import express from 'express';
import { verificationV2Router } from '../routes/verificationV2';

const HASH = 'f'.repeat(64);
const REAL_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';
const LATER_TX = '6c66c24ed00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';

/** The original registration — real confirmed anchor, no certification. */
function anchoredRow(over: Record<string, unknown> = {}) {
  return {
    id: '11111111-1111-1111-1111-111111111111',
    external_id: 'doc-1754000000000-original',
    title: 'Grad cert',
    document_type: 'DOCUMENT',
    content_hash: HASH,
    status: 'anchored',
    certification_metadata: { blockchain: { txHash: REAL_TX, status: 'confirmed', blockHeight: 4547897 } },
    metadata: {},
    created_at: '2026-08-01T00:00:00.000Z',
    certified_at: null,
    organization_name: 'Acme Ltd',
    ...over,
  };
}

/** The certification's derived signed_document row — the certify lineage path
 *  stamps certificationId into its metadata blob. */
function signedCertRow(over: Record<string, unknown> = {}) {
  return {
    id: '22222222-2222-2222-2222-222222222222',
    external_id: 'doc-1754000099999-signedcopy',
    title: 'Certification signed_document',
    document_type: 'verification_certificate',
    content_hash: HASH,
    status: 'signed',
    certification_metadata: {},
    metadata: { certificationId: 'cert-abc', issuerName: 'Oxford University', certifiedAt: '2026-08-02T00:00:00.000Z' },
    created_at: '2026-08-01T00:02:00.000Z',
    certified_at: null,
    organization_name: 'Acme Ltd',
    ...over,
  };
}

const app = express();
app.use(express.json());
app.use('/api/v2/verification', verificationV2Router);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;
const realFetch = global.fetch;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => {
  server?.close();
  global.fetch = realFetch;
});

async function verifyV2(body: Record<string, unknown>, headers: Record<string, string> = {}): Promise<{ status: number; body: any }> {
  const res = await realFetch(`${baseUrl}/api/v2/verification/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...headers },
    body: JSON.stringify(body),
  });
  return { status: res.status, body: await res.json() };
}

beforeEach(() => {
  jest.clearAllMocks();
  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
});

describe('KS-584 P3 — multiplicity (the list contract)', () => {
  it('returns EVERY same-hash registration, each standing on its own evidence', async () => {
    mockQueryRaw.mockResolvedValue([signedCertRow(), anchoredRow()]);
    const { status, body } = await verifyV2({ contentHash: HASH });
    expect(status).toBe(200);
    expect(body.count).toBe(2);
    expect(body.matches).toHaveLength(2);
    const ids = body.matches.map((m: any) => m.documentId);
    expect(ids).toContain('doc-1754000000000-original');
    expect(ids).toContain('doc-1754000099999-signedcopy');
  });

  it('does NOT smear the sibling certification onto the anchored original — the cert-act row carries it', async () => {
    mockQueryRaw.mockResolvedValue([signedCertRow(), anchoredRow()]);
    const { body } = await verifyV2({ contentHash: HASH });
    const original = body.matches.find((m: any) => m.documentId === 'doc-1754000000000-original');
    const certRow = body.matches.find((m: any) => m.documentId === 'doc-1754000099999-signedcopy');
    expect(original.certification).toBeUndefined();
    expect(original.checks.isCertified).toBe(false);
    expect(original.checks.isAnchored).toBe(true);
    expect(certRow.certification).toEqual(expect.objectContaining({ certificationId: 'cert-abc', certifiedBy: 'Oxford University' }));
    expect(certRow.checks.isCertified).toBe(true);
    expect(certRow.checks.isAnchored).toBe(false);
  });

  it('orders matches certified → confirmed-tx → oldest, so matches[0] is v1’s answer', async () => {
    const certified = anchoredRow({
      id: '33333333-3333-3333-3333-333333333333',
      external_id: 'doc-1754000050000-certified',
      status: 'certified',
      certification_metadata: { certificationId: 'cert-123', issuerName: 'Oxford University', certifiedAt: '2026-08-02T00:00:00.000Z' },
      certified_at: '2026-08-02T00:00:00.000Z',
      created_at: '2026-08-01T00:05:00.000Z',
    });
    // Present the worst input order; the response must still lead with the
    // certified row (v1's selection), then the anchored original.
    mockQueryRaw.mockResolvedValue([signedCertRow(), anchoredRow(), certified]);
    const { body } = await verifyV2({ contentHash: HASH });
    expect(body.matches[0].documentId).toBe('doc-1754000050000-certified');
    expect(body.matches[1].documentId).toBe('doc-1754000000000-original');
    expect(body.matches[2].documentId).toBe('doc-1754000099999-signedcopy');
  });

  it('orders certified rows by MILLISECOND-precise certified_at (Prisma Dates — the 576-row sweep catch)', async () => {
    // Prisma returns Date objects; Date.parse(String(date)) truncates to whole
    // seconds, so rows certified milliseconds apart tie and the wrong tiebreak
    // (oldest created_at) wins. Caught live by the parity sweep.
    const older = anchoredRow({
      id: '77777777-7777-7777-7777-777777777777',
      external_id: 'doc-cert-older-ms',
      status: 'certified',
      certification_metadata: { certificationId: 'cert-older' },
      certified_at: new Date('2026-06-10T07:14:08.479Z'),
      created_at: new Date('2026-06-10T07:14:08.485Z'), // OLDER creation — the wrong tiebreak favours it
    });
    const newer = anchoredRow({
      id: '88888888-8888-8888-8888-888888888888',
      external_id: 'doc-cert-newer-ms',
      status: 'certified',
      certification_metadata: { certificationId: 'cert-newer' },
      certified_at: new Date('2026-06-10T07:14:08.485Z'), // 6 ms later — must win
      created_at: new Date('2026-06-10T07:14:08.489Z'),
    });
    mockQueryRaw.mockResolvedValue([older, newer]);
    const { body } = await verifyV2({ contentHash: HASH });
    expect(body.matches[0].documentId).toBe('doc-cert-newer-ms');
  });

  it('reports the KS-596 dual identifiers on every match', async () => {
    const uuidRegistered = anchoredRow({
      id: '44444444-4444-4444-4444-444444444444',
      external_id: '2f1c8a9e-6d4b-4f7a-9c2e-8b5d3a1f7e60', // S-supplied documentUuid
    });
    mockQueryRaw.mockResolvedValue([uuidRegistered, anchoredRow()]);
    const { body } = await verifyV2({ contentHash: HASH });
    const sSupplied = body.matches.find((m: any) => m.documentId === '2f1c8a9e-6d4b-4f7a-9c2e-8b5d3a1f7e60');
    const legacy = body.matches.find((m: any) => m.documentId === 'doc-1754000000000-original');
    expect(sSupplied.documentUuid).toBe('2f1c8a9e-6d4b-4f7a-9c2e-8b5d3a1f7e60');
    // Legacy external_id is not a UUID — the pkey serves as documentUuid.
    expect(legacy.documentUuid).toBe('11111111-1111-1111-1111-111111111111');
  });
});

describe('KS-584 P3 — caller-independent anchor truth', () => {
  it('the chain-fact read carries NO Authorization header, whatever the caller sent (the QA-High regression)', async () => {
    const stale = anchoredRow({
      certification_metadata: { blockchain: { txHash: REAL_TX, status: 'pending' } },
    });
    mockQueryRaw.mockResolvedValue([stale]);
    const fetchMock = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ verified: true, txHash: REAL_TX, blockNumber: 4556727, network: 'preview' }),
    });
    global.fetch = fetchMock as unknown as typeof fetch;

    const { body } = await verifyV2({ contentHash: HASH }, { Authorization: 'Bearer caller-token-must-not-be-forwarded' });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    const [, init] = fetchMock.mock.calls[0];
    expect(init?.headers?.Authorization ?? init?.headers?.authorization).toBeUndefined();
    // And the heal landed: stale 'pending' presented as confirmed.
    expect(body.matches[0].blockchain.status).toBe('confirmed');
    expect(body.matches[0].checks.isAnchored).toBe(true);
  });

  it('heals via same-registration attribution when the chain answers a LATER re-anchor tx', async () => {
    const stale = anchoredRow({
      certification_metadata: { blockchain: { txHash: REAL_TX, status: 'pending' } },
    });
    mockQueryRaw.mockResolvedValue([stale]);
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        verified: true,
        txHash: LATER_TX,
        blockNumber: 4556727,
        network: 'preview',
        metadata: { documentId: 'doc-1754000000000-original' },
      }),
    }) as unknown as typeof fetch;
    const { body } = await verifyV2({ contentHash: HASH });
    expect(body.matches[0].blockchain.txHash).toBe(LATER_TX);
    expect(body.matches[0].checks.isAnchored).toBe(true);
  });

  it('does NOT heal from a confirmed tx that belongs to a DIFFERENT registration', async () => {
    const stale = anchoredRow({
      certification_metadata: { blockchain: { txHash: REAL_TX, status: 'pending' } },
    });
    mockQueryRaw.mockResolvedValue([stale]);
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        verified: true,
        txHash: LATER_TX,
        blockNumber: 4556727,
        metadata: { documentId: 'doc-somebody-else-entirely' },
      }),
    }) as unknown as typeof fetch;
    const { body } = await verifyV2({ contentHash: HASH });
    expect(body.matches[0].blockchain.status).toBe('pending');
    expect(body.matches[0].checks.isAnchored).toBe(false);
  });

  it('makes NO chain call when every anchor is settled (KS-252 chain economy)', async () => {
    mockQueryRaw.mockResolvedValue([anchoredRow(), signedCertRow()]);
    const fetchMock = jest.fn();
    global.fetch = fetchMock as unknown as typeof fetch;
    const { status } = await verifyV2({ contentHash: HASH });
    expect(status).toBe(200);
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('fails CLOSED and still answers 200 when the chain index is down mid-heal', async () => {
    const stale = anchoredRow({
      certification_metadata: { blockchain: { txHash: REAL_TX, status: 'pending' } },
    });
    mockQueryRaw.mockResolvedValue([stale]);
    // beforeEach default: fetch rejects.
    const { status, body } = await verifyV2({ contentHash: HASH });
    expect(status).toBe(200);
    expect(body.matches[0].blockchain.status).toBe('pending');
    expect(body.matches[0].checks.isAnchored).toBe(false);
  });
});

describe('KS-584 P3 — honesty rules carry over per match', () => {
  it('KS-522: a simulated anchor makes no on-chain claim in any match', async () => {
    const simulated = anchoredRow({
      id: '55555555-5555-5555-5555-555555555555',
      external_id: 'doc-1754000000001-simulated',
      certification_metadata: { blockchain: { txHash: 'mock_tx_abc123', status: 'confirmed' } },
    });
    mockQueryRaw.mockResolvedValue([simulated]);
    const { body } = await verifyV2({ contentHash: HASH });
    const m = body.matches[0];
    expect(m.simulated).toBe(true);
    expect(m.blockchain.txHash).toBeNull();
    expect(m.blockchain.simulatedTxRef).toBe('mock_tx_abc123');
    expect(m.checks.isAnchored).toBe(false);
  });

  it('KS-584 scoping: a cross-tenant match withholds tenant-owned naming and says so', async () => {
    const foreign = anchoredRow({ tenant_id: 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee' });
    mockQueryRaw.mockResolvedValue([foreign]);
    // Anonymous caller (no token) → no caller tenant → scoped.
    const { body } = await verifyV2({ contentHash: HASH });
    const m = body.matches[0];
    expect(m.fieldsWithheld).toBe(true);
    expect(m.title).toBeNull();
    expect(m.issuer).toBeNull();
    // The service facts survive scoping.
    expect(m.checks.isAnchored).toBe(true);
    expect(m.contentHash).toBe(HASH);
  });

  it('a revoked registration reports itself honestly in the list', async () => {
    const revoked = anchoredRow({
      id: '66666666-6666-6666-6666-666666666666',
      external_id: 'doc-1754000000002-revoked',
      status: 'revoked',
    });
    mockQueryRaw.mockResolvedValue([revoked, signedCertRow()]);
    const { body } = await verifyV2({ contentHash: HASH });
    const m = body.matches.find((x: any) => x.documentId === 'doc-1754000000002-revoked');
    expect(m.checks.isRevoked).toBe(true);
    expect(m.checks.integrityVerified).toBe(false);
  });
});

describe('KS-584 P3 — fallbacks and inputs', () => {
  it('chain-only fallback: a hash known only to the chain index answers as one honest match', async () => {
    mockQueryRaw.mockResolvedValue([]);
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        verified: true,
        source: 'chain',
        txHash: REAL_TX,
        blockNumber: 4547897,
        network: 'preview',
        confirmedAt: '2026-08-01T00:30:00.000Z',
        metadata: { documentId: 'doc-cross-env', certId: 'cert-xyz' },
      }),
    }) as unknown as typeof fetch;
    const { body } = await verifyV2({ contentHash: HASH });
    expect(body.count).toBe(1);
    const m = body.matches[0];
    expect(m.source).toBe('blockchain');
    expect(m.checks.isAnchored).toBe(true);
    expect(m.checks.isCertified).toBe(true);
    expect(m.certification.certificationId).toBe('cert-xyz');
  });

  it('count:0 with empty matches is the honest "never registered" answer (still 200)', async () => {
    mockQueryRaw.mockResolvedValue([]);
    const { status, body } = await verifyV2({ contentHash: HASH });
    expect(status).toBe(200);
    expect(body.count).toBe(0);
    expect(body.matches).toEqual([]);
    expect(body.hash).toBe(`sha256:${HASH}`);
  });

  it('documentId-only lookup answers existence, not integrity', async () => {
    mockQueryRaw.mockResolvedValueOnce([anchoredRow()]);
    const { body } = await verifyV2({ documentId: 'doc-1754000000000-original' });
    expect(body.count).toBe(1);
    expect(body.hash).toBeNull();
    expect(body.matches[0].checks.hashValid).toBe(false);
    expect(body.matches[0].checks.integrityVerified).toBe(false);
  });

  it('no verifiable input → 400 in the canonical error envelope (not v1’s legacy shape)', async () => {
    const { status, body } = await verifyV2({});
    expect(status).toBe(400);
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('BAD_REQUEST');
    expect(body.verified).toBeUndefined();
  });

  it('wrong-typed hash → 400', async () => {
    const { status } = await verifyV2({ contentHash: { nope: true } as unknown as string });
    expect(status).toBe(400);
  });

  it('verify-file hashes the raw bytes server-side and answers the list', async () => {
    mockQueryRaw.mockResolvedValue([anchoredRow()]);
    const bytes = Buffer.from('the document bytes');
    const expected = require('crypto').createHash('sha256').update(bytes).digest('hex');
    const res = await realFetch(`${baseUrl}/api/v2/verification/verify-file`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/octet-stream' },
      body: bytes,
    });
    const body: any = await res.json();
    expect(res.status).toBe(200);
    expect(body.hash).toBe(`sha256:${expected}`);
    expect(body.fileSize).toBe(bytes.length);
    expect(body.count).toBe(1);
  });
});

describe('KS-584 P3 — auth wiring', () => {
  it('mounts authenticate({required:false}): absent token → anonymous, present-but-invalid → 401 by the middleware contract', () => {
    expect(mockAuthenticateCalls).toContainEqual({ required: false });
  });
});
