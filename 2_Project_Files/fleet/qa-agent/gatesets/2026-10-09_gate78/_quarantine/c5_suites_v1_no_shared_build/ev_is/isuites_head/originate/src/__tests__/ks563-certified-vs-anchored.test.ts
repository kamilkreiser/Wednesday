/**
 * =============================================================================
 * KS-563 — `isCertified` must mean CERTIFIED, not merely anchored
 * =============================================================================
 * The verify API reported `checks.isCertified: true` for any document whose
 * status was `certified | anchored | signed`, so a document that was only
 * uploaded (originate → auto-anchor → status `anchored`) came back certified.
 * Platform S rendered that as a green "Certified by issuer" tick in front of
 * end users.
 *
 * These tests pin the ruled contract (Kam, 2026-08-06 — Option B):
 *   - `checks.isCertified` is true ONLY for status `certified` ('signed' and
 *     'anchored' do NOT count);
 *   - `checks.isAnchored` carries chain presence, and a KS-522 simulated
 *     anchor never sets it;
 *   - top-level `verified` / `integrityVerified` keep the OLD broad set, so
 *     upload-only documents stay verified (no consumer breakage);
 *   - a `certification` object is present ONLY when a certification happened —
 *     its absence is the honest signal.
 * =============================================================================
 */

process.env.NODE_ENV = 'development';
// routes/verification imports ../db (via the logger), whose config demands
// DATABASE_URL at module load — same shim the other unit suites here use.
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

// The lineage walks are best-effort and not under test here.
jest.mock('../repositories/documentRepo', () => ({
  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
  MAX_LINEAGE_DEPTH: 10,
}));

import express from 'express';
import { verificationRouter } from '../routes/verification';

const HASH = 'a'.repeat(64);

/** A document row as the verify SELECTs return it. */
function docRow(over: Record<string, unknown> = {}) {
  return {
    id: '11111111-1111-1111-1111-111111111111',
    external_id: 'doc-1754000000000-abcdef12',
    title: 'Employment contract',
    document_type: 'DOCUMENT',
    content_hash: HASH,
    status: 'anchored',
    certification_metadata: {},
    metadata: {},
    created_at: '2026-08-01T00:00:00.000Z',
    certified_at: null,
    organization_name: 'Acme Ltd',
    ...over,
  };
}

// Same harness as the other route tests here: mount the real router on a real
// listener and drive it over HTTP (this service has no supertest, and adding a
// test-only dep would break the Docker build, which compiles __tests__).
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

/**
 * POST /verify by hash, with the chain-first lookup forced to miss.
 * The route reads `providedHash | contentHash | documentHash` — not `hash`.
 */
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
  // Chain-first lookup is not part of these cases — force the DB path. The
  // router calls the global fetch; the harness above keeps the real one.
  global.fetch = jest.fn().mockRejectedValue(new Error('chain lookup disabled in test')) as unknown as typeof fetch;
});

describe('KS-563 — merely-anchored documents are not certified', () => {
  it('reports isCertified FALSE for an anchored (upload-only) document', async () => {
    mockQueryRaw.mockResolvedValue([docRow({ status: 'anchored' })]);

    const res = await verifyByHash();

    expect(res.status).toBe(200);
    expect(res.body.checks.isCertified).toBe(false);
    expect(res.body.certification).toBeUndefined();
  });

  it('keeps `verified` and `integrityVerified` TRUE for that same document', async () => {
    // The defect was the certification flag alone; narrowing `verified` too
    // would flip every Platform S upload to unverified.
    mockQueryRaw.mockResolvedValue([docRow({ status: 'anchored' })]);

    const res = await verifyByHash();

    expect(res.body.verified).toBe(true);
    expect(res.body.checks.integrityVerified).toBe(true);
  });

  it('reports isCertified FALSE for a signed document', async () => {
    mockQueryRaw.mockResolvedValue([docRow({ status: 'signed' })]);

    const res = await verifyByHash();

    expect(res.body.checks.isCertified).toBe(false);
    expect(res.body.verified).toBe(true);
  });

  it('reports isCertified TRUE only for a certified document', async () => {
    mockQueryRaw.mockResolvedValue([
      docRow({
        status: 'certified',
        certified_at: '2026-08-02T09:00:00.000Z',
        certification_metadata: {
          certificationId: 'cert-1754000000000-11112222',
          certificationType: 'AUTHENTICITY',
          certifiedAt: '2026-08-02T09:00:00.000Z',
          issuerName: 'Oxford University',
          issuerId: '22222222-2222-2222-2222-222222222222',
        },
      }),
    ]);

    const res = await verifyByHash();

    expect(res.body.checks.isCertified).toBe(true);
    expect(res.body.certification).toEqual({
      certificationId: 'cert-1754000000000-11112222',
      certificationType: 'AUTHENTICITY',
      certifiedAt: '2026-08-02T09:00:00.000Z',
      certifiedBy: 'Oxford University',
      certifierOrganizationId: '22222222-2222-2222-2222-222222222222',
    });
  });
});

describe('KS-563 — isAnchored is honest about chain presence', () => {
  it('is TRUE for a real on-chain anchor in the STORED shape (status confirmed, no `anchored` key)', async () => {
    // The shape a real row actually has — caught on the demo VM, where a
    // genuinely confirmed preview-testnet anchor reported isAnchored FALSE
    // because the first cut required an `anchored: true` boolean that the
    // stored blob has never carried. Anchoring's vocabulary is
    // pending | submitted | confirmed | failed.
    mockQueryRaw.mockResolvedValue([
      docRow({
        certification_metadata: {
          blockchain: {
            status: 'confirmed',
            txHash: '65963d143c3b3798540c574a8c2cae91a9b27efe90e970c76f397b5e369ae08e',
            network: 'preview',
            anchorId: 'anchor_6c66a134',
            blockHeight: 4544575,
          },
        },
      }),
    ]);

    const res = await verifyByHash();

    expect(res.body.checks.isAnchored).toBe(true);
  });

  it('is TRUE for the chain-first shape (`anchored: true`)', async () => {
    mockQueryRaw.mockResolvedValue([
      docRow({
        certification_metadata: {
          blockchain: { anchored: true, txHash: 'f'.repeat(64), network: 'preview' },
        },
      }),
    ]);

    const res = await verifyByHash();

    expect(res.body.checks.isAnchored).toBe(true);
  });

  it('is FALSE while the tx is only SUBMITTED — in flight can still fail (KS-535 class)', async () => {
    mockQueryRaw.mockResolvedValue([
      docRow({
        certification_metadata: {
          blockchain: { status: 'submitted', txHash: 'a'.repeat(64), network: 'preview' },
        },
      }),
    ]);

    const res = await verifyByHash();

    expect(res.body.checks.isAnchored).toBe(false);
  });

  it('is FALSE while the anchor is still PENDING, even though status is already anchored', async () => {
    // `documents.status` flips to 'anchored' on SUBMISSION, so the status alone
    // must never be read as on-chain presence — caught on the local live proof.
    mockQueryRaw.mockResolvedValue([
      docRow({
        status: 'anchored',
        certification_metadata: {
          blockchain: { status: 'pending', txHash: null, anchorId: 'anchor_x', blockHeight: 0 },
        },
      }),
    ]);

    const res = await verifyByHash();

    expect(res.body.checks.isAnchored).toBe(false);
    // Still registry-valid — only the chain claim is withheld.
    expect(res.body.verified).toBe(true);
  });

  it('falls back to document status only when there is NO chain blob at all', async () => {
    mockQueryRaw.mockResolvedValue([docRow({ status: 'anchored', certification_metadata: {} })]);

    const res = await verifyByHash();

    expect(res.body.checks.isAnchored).toBe(true);
  });

  it('is FALSE for a KS-522 simulated anchor, which makes no on-chain claim', async () => {
    mockQueryRaw.mockResolvedValue([
      docRow({
        certification_metadata: {
          blockchain: { anchored: true, txHash: 'tx_sim_deadbeef', network: 'preview' },
        },
      }),
    ]);

    const res = await verifyByHash();

    expect(res.body.checks.isAnchored).toBe(false);
    expect(res.body.blockchain.txHash).toBeNull();
    expect(res.body.simulated).toBe(true);
  });
});

describe('KS-563 — a revoked document is neither certified nor verified', () => {
  it('keeps revocation dominant over the narrowed flag', async () => {
    mockQueryRaw.mockResolvedValue([docRow({ status: 'revoked' })]);

    const res = await verifyByHash();

    expect(res.body.checks.isRevoked).toBe(true);
    expect(res.body.checks.isCertified).toBe(false);
    expect(res.body.verified).toBe(false);
  });
});
