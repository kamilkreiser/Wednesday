/**
 * =============================================================================
 * KS-584 (interim) — verify-by-hash answers from the row that evidences it
 * =============================================================================
 * Verify-by-hash resolved a content hash to ONE arbitrary row
 * (`ORDER BY certified_at DESC NULLS LAST LIMIT 1`). The normal certify flow
 * creates a SECOND row for the same bytes (the certification's
 * signed_document, no chain data), and `certified_at` is NULL across whole
 * row-sets in production, so a certified + on-chain-anchored document could
 * verify as neither (live UAT repro, 2026-08-07: hash f4fd83a9…).
 *
 * These tests pin the interim contract (Kam GO ruling, 2026-08-11):
 *   - the row with certification/chain evidence answers, never an arbitrary
 *     sibling;
 *   - certification evidence is read from the same-hash registration SET (the
 *     lineage certify path records the act on a derived 'signed' row);
 *   - KS-522 holds: a simulated anchor row never outranks a real one;
 *   - a stale 'pending' blob with a REAL tx is confirmed against the chain
 *     index before presentation, and fails CLOSED when the index is down;
 *   - tenant-owned fields (title/issuer) do not cross the tenant boundary.
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
const REAL_TX = '84fe214bd00257443c81e240a074763d476f9096b7e3525065bad06ec51c38c3';

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

/** The certification's derived signed_document row — later, no chain data. */
function signedDocumentRow(over: Record<string, unknown> = {}) {
  return {
    id: '22222222-2222-2222-2222-222222222222',
    external_id: 'doc-1754000099999-signedcopy',
    title: 'Certification signed_document',
    document_type: 'verification_certificate',
    content_hash: HASH,
    status: 'signed',
    certification_metadata: {},
    metadata: {},
    created_at: '2026-08-01T00:02:00.000Z',
    certified_at: null,
    organization_name: 'Acme Ltd',
    ...over,
  };
}

const app = express();
app.use(express.json());
app.use('/api/verification', verificationRouter);

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

async function verifyByHash(): Promise<{ status: number; body: any }> {
  const res = await realFetch(`${baseUrl}/api/verification/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contentHash: HASH }),
  });
  return { status: res.status, body: await res.json() };
}

beforeEach(() => {
  jest.clearAllMocks();
  // Chain lookups (chain-first fallback AND the KS-584 stale-anchor
  // confirmation) go through global.fetch; default them to down so every
  // case not explicitly about them exercises the fail-closed path.
  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
});

describe('KS-584 — row selection', () => {
  it('answers from the anchored original, not the later signed_document sibling (the UAT shape)', async () => {
    // certified_at DESC NULLS LAST leaves order arbitrary — present the BAD
    // order (signed copy first) and require selection to fix it.
    mockQueryRaw.mockResolvedValue([signedDocumentRow(), anchoredRow()]);
    const { body } = await verifyByHash();
    expect(body.documentId).toBe('doc-1754000000000-original');
    expect(body.checks.isAnchored).toBe(true);
    expect(body.blockchain.txHash).toBe(REAL_TX);
    expect(body.verified).toBe(true);
  });

  it('prefers a certified row over everything else', async () => {
    const certified = anchoredRow({
      id: '33333333-3333-3333-3333-333333333333',
      external_id: 'doc-1754000050000-certified',
      status: 'certified',
      certification_metadata: {
        certificationId: 'cert-123',
        issuerName: 'Oxford University',
        certifiedAt: '2026-08-02T00:00:00.000Z',
        blockchain: { txHash: REAL_TX, status: 'confirmed', blockHeight: 1 },
      },
      certified_at: '2026-08-02T00:00:00.000Z',
    });
    mockQueryRaw.mockResolvedValue([certified, anchoredRow(), signedDocumentRow()]);
    const { body } = await verifyByHash();
    expect(body.documentId).toBe('doc-1754000050000-certified');
    expect(body.checks.isCertified).toBe(true);
    expect(body.certification?.certificationId).toBe('cert-123');
  });

  it('never lets a simulated anchor outrank a real one (KS-522)', async () => {
    const simulated = anchoredRow({
      id: '44444444-4444-4444-4444-444444444444',
      external_id: 'doc-1754000010000-simulated',
      certification_metadata: { blockchain: { txHash: `tx_sim_${'b'.repeat(64)}`, status: 'confirmed' } },
      created_at: '2026-07-30T00:00:00.000Z', // older — would win a created_at tie-break
    });
    mockQueryRaw.mockResolvedValue([simulated, anchoredRow()]);
    const { body } = await verifyByHash();
    expect(body.documentId).toBe('doc-1754000000000-original');
    expect(body.checks.isAnchored).toBe(true);
    expect(body.simulated).toBeUndefined();
  });
});

describe('KS-584 — certification evidence from the registration set', () => {
  it('surfaces the lineage-path certification recorded on a signed sibling', async () => {
    const signedWithCert = signedDocumentRow({
      metadata: { certificationId: 'cert-uat-777', certifiedAt: '2026-08-07T04:16:06.964Z', issuerName: 'Borrower Org' },
    });
    mockQueryRaw.mockResolvedValue([signedWithCert, anchoredRow()]);
    const { body } = await verifyByHash();
    // The anchored original still answers…
    expect(body.documentId).toBe('doc-1754000000000-original');
    expect(body.checks.isAnchored).toBe(true);
    // …but the certification act evidenced on the sibling is not lost.
    expect(body.checks.isCertified).toBe(true);
    expect(body.certification?.certificationId).toBe('cert-uat-777');
  });

  it('does NOT claim certification from a merely-signed sibling without a certificationId', async () => {
    mockQueryRaw.mockResolvedValue([signedDocumentRow(), anchoredRow()]);
    const { body } = await verifyByHash();
    expect(body.checks.isCertified).toBe(false);
    expect(body.certification).toBeUndefined();
  });
});

describe('KS-584 — stale pending anchor confirmation', () => {
  const pendingRow = () => anchoredRow({
    certification_metadata: { blockchain: { txHash: REAL_TX, status: 'pending', blockHeight: 0 } },
  });

  it('confirms a stale pending blob against the chain index (same tx only)', async () => {
    mockQueryRaw.mockResolvedValue([signedDocumentRow(), pendingRow()]);
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ verified: true, txHash: REAL_TX, blockNumber: 4547897, confirmedAt: '2026-08-07T04:18:22.000Z' }),
    }) as unknown as typeof fetch;
    const { body } = await verifyByHash();
    expect(body.documentId).toBe('doc-1754000000000-original');
    expect(body.checks.isAnchored).toBe(true);
    expect(body.blockchain.status).toBe('confirmed');
    expect(body.blockchain.blockHeight).toBe(4547897);
  });

  it('fails CLOSED when the chain index is down — pending stays not-anchored', async () => {
    mockQueryRaw.mockResolvedValue([signedDocumentRow(), pendingRow()]);
    const { body } = await verifyByHash();
    expect(body.checks.isAnchored).toBe(false);
  });

  it('confirms from a LATER re-anchor tx when the chain index attributes it to this registration', async () => {
    // Observed live on the KS-584 UAT document: the blob holds the stale
    // in-flight tx while the chain index answers with a later CONFIRMED tx
    // for the same documentId. The confirmed tx supersedes the stale one.
    const reanchorTx = 'c'.repeat(64);
    mockQueryRaw.mockResolvedValue([pendingRow()]);
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ verified: true, txHash: reanchorTx, blockNumber: 4556727, metadata: { documentId: 'doc-1754000000000-original' } }),
    }) as unknown as typeof fetch;
    const { body } = await verifyByHash();
    expect(body.checks.isAnchored).toBe(true);
    expect(body.blockchain.txHash).toBe(reanchorTx);
    expect(body.blockchain.status).toBe('confirmed');
  });

  it('does not confirm from a different transaction attributed to a DIFFERENT registration', async () => {
    mockQueryRaw.mockResolvedValue([pendingRow()]);
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ verified: true, txHash: 'c'.repeat(64), blockNumber: 1, metadata: { documentId: 'doc-9999999999999-other' } }),
    }) as unknown as typeof fetch;
    const { body } = await verifyByHash();
    expect(body.checks.isAnchored).toBe(false);
  });
});

describe('KS-584 — tenant-owned fields do not cross the tenant boundary', () => {
  it('scrubs title/issuer for a caller with no tenant identity when the row carries one', async () => {
    mockQueryRaw.mockResolvedValue([anchoredRow({ tenant_id: 'a0000000-0000-0000-0000-000000000001' })]);
    const { body } = await verifyByHash();
    expect(body.title).toBeNull();
    expect(body.issuer).toBeNull();
    // The facts survive — only the tenant-owned naming is scoped.
    expect(body.verified).toBe(true);
    expect(body.checks.isAnchored).toBe(true);
    expect(body.lineage).toBeUndefined();
  });

  it('keeps tenant fields when the row carries no tenancy info (legacy rows)', async () => {
    mockQueryRaw.mockResolvedValue([anchoredRow()]);
    const { body } = await verifyByHash();
    expect(body.title).toBe('Grad cert');
  });
});
