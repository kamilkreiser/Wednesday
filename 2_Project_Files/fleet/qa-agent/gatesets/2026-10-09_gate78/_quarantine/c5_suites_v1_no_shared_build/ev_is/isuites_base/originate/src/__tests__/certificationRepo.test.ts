/**
 * =============================================================================
 * CERTIFICATION REPOSITORY — UNIT TESTS
 * =============================================================================
 * KS-12: rewritten. The repo no longer has an in-memory certification store —
 * originate's "certifications" are persisted as rows in the `documents` table
 * (DB-only), so the old "in-memory fallback" tests were exercising behaviour
 * that was removed.
 *
 * What these tests cover instead, with `prisma.$queryRaw` / `$executeRaw`
 * mocked at the unit boundary:
 *   - `verifyDbReady` / `initRepo` — throw when the DB is unreachable
 *   - `fromDbRow` mapping via `getCertification` (row → domain object,
 *     including privacy settings & blockchain metadata pulled out of
 *     `certification_metadata`, and the DB→domain status map)
 *   - `listCertifications` mapping + total
 *   - the write paths (`saveCertification`, `saveShare`) — number of
 *     `$executeRaw` statements issued, returned value, error propagation
 *   - `getSharesByCertification` row mapping + empty case
 *
 * Actual SQL correctness against Postgres is integration-test territory.
 * =============================================================================
 */

// ---------------------------------------------------------------------------
// Mocks (must precede the import of the module under test)
// ---------------------------------------------------------------------------

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: mockQueryRaw,
    $executeRaw: mockExecuteRaw,
  },
}));

jest.mock('../utils/logger', () => ({
  logger: {
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
    debug: jest.fn(),
  },
}));

jest.mock('../config', () => ({
  config: {
    nodeEnv: 'test',
    databaseUrl: '',
    port: 4000,
    redisUrl: '',
    jwtSecret: 'test-secret',
    jwtExpiresIn: '1d',
    cardanoNodeUrl: '',
    cardanoNetwork: 'devnet',
    rateLimitWindowMs: 60000,
    rateLimitMaxRequests: 100,
    corsOrigins: [],
    features: {
      documentCertification: false,
      walletIntegration: false,
      basicDid: false,
    },
  },
}));

import {
  verifyDbReady,
  getCertification,
  listCertifications,
  saveCertification,
  saveShare,
  getSharesByCertification,
  initRepo,
  Certification,
  ShareRecord,
} from '../repositories/certificationRepo';

// KS-22 (KS-4 phase 5b): tenant-scoped repo functions — tests pin to a
// fixed test tenant (same UUID as originate's default tenant).
const TEST_TENANT = 'a0000000-0000-4000-8000-000000000001';

/**
 * A `documents`-table row shaped the way the certification repo's
 * `fromDbRow` expects it. `certMeta` overrides the `certification_metadata`
 * jsonb column.
 */
function makeDbRow(
  overrides: Record<string, unknown> = {},
  certMeta: Record<string, unknown> = {},
): Record<string, unknown> {
  return {
    id: 'cert-create-001',
    document_type: 'certificate',
    status: 'certified',
    issuer_user_id: 'issuer-001',
    owner_user_id: 'holder-001',
    owner_did: null,
    title: 'BSc Computer Science',
    content_hash: 'sha256:cert-create-001',
    metadata: {},
    certification_metadata: {
      certificationType: 'certificate',
      certificationData: { title: 'BSc Computer Science' },
      issuerName: 'University of Oxford',
      holderName: 'Alice',
      ...certMeta,
    },
    certified_at: new Date('2026-01-01T00:00:00.000Z'),
    expires_at: null,
    created_at: new Date('2026-01-01T00:00:00.000Z'),
    updated_at: new Date('2026-01-01T00:00:00.000Z'),
    ...overrides,
  };
}

function makeCert(overrides: Partial<Certification> = {}): Certification {
  const id = `cert-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  return {
    id,
    type: 'degree',
    status: 'issued',
    issuer: { id: 'issuer-001', name: 'University of Oxford' },
    holder: { id: 'holder-001', name: 'Alice' },
    data: { title: 'BSc Computer Science' },
    issuedAt: new Date().toISOString(),
    contentHash: `sha256:${id}`,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    ...overrides,
  };
}

function makeShare(certId: string, overrides: Partial<ShareRecord> = {}): ShareRecord {
  return {
    id: `share-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    certificationId: certId,
    toEmail: 'verifier@example.com',
    toName: 'Bob',
    shareType: 'full',
    sharedBy: 'holder-001',
    timestamp: new Date().toISOString(),
    status: 'sent',
    ...overrides,
  };
}

beforeEach(() => {
  mockQueryRaw.mockReset();
  mockExecuteRaw.mockReset();
});

// ===========================================================================
// verifyDbReady / initRepo
// ===========================================================================
describe('verifyDbReady / initRepo', () => {
  it('resolves when the DB responds', async () => {
    mockQueryRaw.mockResolvedValue([{ '?column?': 1 }]);
    await expect(verifyDbReady()).resolves.toBeUndefined();
    await expect(initRepo()).resolves.toBeUndefined();
  });

  it('throws "Database is required" when the DB is unreachable', async () => {
    mockQueryRaw.mockRejectedValue(new Error('ECONNREFUSED'));
    await expect(verifyDbReady()).rejects.toThrow(/Database is required/i);
    await expect(initRepo()).rejects.toThrow(/Database is required/i);
  });
});

// ===========================================================================
// getCertification
// ===========================================================================
describe('getCertification', () => {
  it('maps a row to the domain certification', async () => {
    mockQueryRaw.mockResolvedValueOnce([makeDbRow({ id: 'cert-create-001' })]);
    const cert = await getCertification('cert-create-001', TEST_TENANT);

    expect(cert).not.toBeNull();
    expect(cert!.id).toBe('cert-create-001');
    expect(cert!.type).toBe('certificate');
    expect(cert!.status).toBe('issued'); // 'certified' (DB) → 'issued' (domain)
    expect(cert!.issuer.name).toBe('University of Oxford');
    expect(cert!.holder.name).toBe('Alice');
    expect(cert!.contentHash).toBe('sha256:cert-create-001');
  });

  it('returns null when no row matches', async () => {
    mockQueryRaw.mockResolvedValueOnce([]);
    expect(await getCertification('cert-missing-xyz', TEST_TENANT)).toBeNull();
  });

  it('propagates a database error', async () => {
    mockQueryRaw.mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
    await expect(getCertification('cert-create-001', TEST_TENANT)).rejects.toThrow(/connection terminated/);
  });

  it('surfaces a revoked certification with its reason', async () => {
    mockQueryRaw.mockResolvedValueOnce([
      makeDbRow({ status: 'revoked' }, { revokedAt: '2026-02-01T00:00:00Z', revocationReason: 'Issued in error' }),
    ]);
    const cert = await getCertification('cert-revoke-001', TEST_TENANT);
    expect(cert!.status).toBe('revoked');
    expect(cert!.revocationReason).toBe('Issued in error');
    expect(cert!.revokedAt).toBe('2026-02-01T00:00:00Z');
  });

  it('extracts privacy settings from certification_metadata', async () => {
    mockQueryRaw.mockResolvedValueOnce([
      makeDbRow({}, {
        privacySettings: {
          defaultVisibility: 'authorized',
          fieldOverrides: [{ field: 'grade', visibility: 'private' }],
        },
      }),
    ]);
    const cert = await getCertification('cert-privacy-001', TEST_TENANT);
    expect(cert!.privacySettings).toBeDefined();
    expect(cert!.privacySettings!.defaultVisibility).toBe('authorized');
    expect(cert!.privacySettings!.fieldOverrides).toHaveLength(1);
    expect(cert!.privacySettings!.fieldOverrides![0].field).toBe('grade');
  });

  it('extracts blockchain anchoring metadata', async () => {
    mockQueryRaw.mockResolvedValueOnce([
      makeDbRow({}, { blockchain: { txHash: 'tx_abc123', blockHeight: 1_000_000, anchoredAt: '2026-01-05T00:00:00Z' } }),
    ]);
    const cert = await getCertification('cert-blockchain-001', TEST_TENANT);
    expect(cert!.blockchain).toBeDefined();
    expect(cert!.blockchain!.txHash).toBe('tx_abc123');
    expect(cert!.blockchain!.blockHeight).toBe(1_000_000);
  });
});

// ===========================================================================
// listCertifications
// ===========================================================================
describe('listCertifications', () => {
  it('maps every row and reports total == items.length', async () => {
    mockQueryRaw.mockResolvedValueOnce([
      makeDbRow({ id: 'cert-A-1' }, { issuerName: 'Issuer A' }),
      makeDbRow({ id: 'cert-A-2' }, { issuerName: 'Issuer A' }),
      makeDbRow({ id: 'cert-B-1' }, { issuerName: 'Issuer B' }),
    ]);
    const result = await listCertifications(TEST_TENANT);
    expect(result.items).toHaveLength(3);
    expect(result.total).toBe(result.items.length);
    expect(result.items.map((c) => c.id)).toEqual(['cert-A-1', 'cert-A-2', 'cert-B-1']);
  });

  it('returns an empty list when there are no rows', async () => {
    mockQueryRaw.mockResolvedValueOnce([]);
    const result = await listCertifications(TEST_TENANT);
    expect(result.items).toHaveLength(0);
    expect(result.total).toBe(0);
  });

  it('propagates a database error', async () => {
    mockQueryRaw.mockRejectedValueOnce(new Error('relation "documents" does not exist'));
    await expect(listCertifications(TEST_TENANT)).rejects.toThrow(/does not exist/);
  });
});

// ===========================================================================
// saveCertification
// ===========================================================================
describe('saveCertification', () => {
  it('returns the input certification and writes the document + a provenance event', async () => {
    mockExecuteRaw.mockResolvedValue(undefined);
    // IDs must be valid UUIDs so the ::uuid casts in the INSERT don't throw
    const cert = makeCert({
      id: 'a1111111-0000-4000-8000-000000000001',
      issuer: { id: 'a2222222-0000-4000-8000-000000000002', name: 'Oxford' },
      holder: { id: 'a3333333-0000-4000-8000-000000000003', name: 'Alice' },
      type: 'transcript',
    });
    const saved = await saveCertification(cert, TEST_TENANT);

    expect(saved).toBe(cert);
    expect(saved.type).toBe('transcript');
    // one INSERT into documents + one INSERT into certification_events
    expect(mockExecuteRaw).toHaveBeenCalledTimes(2);
  });

  it('propagates a database error', async () => {
    mockExecuteRaw.mockRejectedValueOnce(new Error('disk full'));
    const cert = makeCert({
      id: 'a4444444-0000-4000-8000-000000000004',
      issuer: { id: 'a5555555-0000-4000-8000-000000000005' },
      holder: { id: 'a6666666-0000-4000-8000-000000000006' },
    });
    await expect(saveCertification(cert, TEST_TENANT)).rejects.toThrow(/disk full/);
  });
});

// ===========================================================================
// saveShare / getSharesByCertification
// ===========================================================================
describe('share records', () => {
  it('saveShare returns the input and writes the share row + a provenance event', async () => {
    mockExecuteRaw.mockResolvedValue(undefined);
    const share = makeShare('c1111111-0000-4000-8000-000000000001', {
      id: 'c2222222-0000-4000-8000-000000000002',
      sharedBy: 'c3333333-0000-4000-8000-000000000003',
      toEmail: 'alice@example.com',
    });
    const saved = await saveShare(share);
    expect(saved).toBe(share);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(2);
  });

  it('getSharesByCertification maps share_records rows', async () => {
    mockQueryRaw.mockResolvedValueOnce([
      {
        id: 's1', document_id: 'cert-share-parent', to_email: 'alice@example.com',
        to_name: 'Alice', share_type: 'full', shared_by_id: 'holder-001',
        timestamp: new Date('2026-01-01T00:00:00Z'), status: 'sent', created_at: new Date('2026-01-01T00:00:00Z'),
      },
      {
        id: 's2', document_id: 'cert-share-parent', to_email: 'bob@example.com',
        to_name: 'Bob', share_type: 'redacted', shared_by_id: 'holder-001',
        timestamp: new Date('2026-01-02T00:00:00Z'), status: 'sent', created_at: new Date('2026-01-02T00:00:00Z'),
      },
    ]);
    const shares = await getSharesByCertification('cert-share-parent');
    expect(shares).toHaveLength(2);
    expect(shares.map((s) => s.toEmail)).toEqual(['alice@example.com', 'bob@example.com']);
    expect(shares[0].certificationId).toBe('cert-share-parent');
  });

  it('getSharesByCertification returns [] when there are no shares', async () => {
    mockQueryRaw.mockResolvedValueOnce([]);
    expect(await getSharesByCertification('cert-no-shares')).toHaveLength(0);
  });
});
