/**
 * =============================================================================
 * DOCUMENT REPOSITORY — UNIT TESTS
 * =============================================================================
 * KS-12: rewritten. The repo no longer has an in-memory document store — it
 * is DB-only (see the file header in repositories/documentRepo.ts), so the
 * old "in-memory fallback" tests were exercising behaviour that was removed.
 *
 * What these tests cover instead, with `prisma.$queryRaw` / `$executeRaw`
 * mocked at the unit boundary:
 *   - pure helpers (`generateContentHash`)
 *   - the in-memory signing-request nonces (still genuinely in-memory)
 *   - `verifyDbReady` — throws when the DB is unreachable
 *   - the mapping / filtering / pagination / error-propagation logic the
 *     repo layers on top of the raw SQL (row → domain object, status
 *     filter, page/limit, "not found" → null, rejection re-thrown)
 *
 * Actual SQL correctness against Postgres is integration-test territory and
 * is covered by the end-to-end document flow, not here.
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
  getDocument,
  listDocuments,
  saveDocument,
  updateDocument,
  generateContentHash,
  getSigningRequest,
  saveSigningRequest,
  deleteSigningRequest,
  walkAncestors,
  walkDescendants,
  assertNoCycle,
  MAX_LINEAGE_DEPTH,
  DocumentRecord,
  SigningRequest,
} from '../repositories/documentRepo';

// KS-4: the repo functions are tenant-scoped — tests pass a fixed test
// tenant (same UUID as originate's default tenant).
const TEST_TENANT = 'a0000000-0000-4000-8000-000000000001';
const TEST_OWNER_UUID = 'b0000000-0000-4000-8000-0000000000ff';

/** A `documents`-table row shaped the way `fromDbRow` expects it. */
function makeDbRow(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    id: 'd0000000-0000-4000-8000-000000000001',
    external_id: 'doc-001',
    document_type: 'certificate',
    status: 'draft',
    owner_user_id: TEST_OWNER_UUID,
    issuer_user_id: null,
    rights_holder_id: null,
    title: 'Test Document',
    description: null,
    content_hash: 'sha256:doc-001',
    metadata: {},
    certification_metadata: {},
    created_at: new Date('2026-01-01T00:00:00.000Z'),
    updated_at: new Date('2026-01-01T00:00:00.000Z'),
    ...overrides,
  };
}

function makeDoc(overrides: Partial<DocumentRecord> = {}): DocumentRecord {
  const id = `doc-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  return {
    id,
    type: 'degree',
    status: 'draft',
    owner: { id: 'owner-not-a-uuid' },
    data: { title: 'Test Document' },
    contentHash: `sha256:${id}`,
    signatures: [],
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    ...overrides,
  };
}

beforeEach(() => {
  mockQueryRaw.mockReset();
  mockExecuteRaw.mockReset();
});

// ===========================================================================
// generateContentHash (pure)
// ===========================================================================
describe('generateContentHash', () => {
  it('produces a consistent SHA-256 hex string', () => {
    const data = { name: 'test', value: 123 };
    expect(generateContentHash(data)).toBe(generateContentHash(data));
    expect(generateContentHash(data)).toMatch(/^[a-f0-9]{64}$/);
  });

  it('produces different hashes for different data', () => {
    expect(generateContentHash({ a: 1 })).not.toBe(generateContentHash({ b: 2 }));
  });

  it('produces the same hash regardless of key order', () => {
    expect(generateContentHash({ x: 1, y: 2 })).toBe(generateContentHash({ y: 2, x: 1 }));
  });
});

// ===========================================================================
// Signing requests (in-memory nonces)
// ===========================================================================
describe('signing requests (in-memory)', () => {
  it('saves, retrieves, and deletes a signing request', () => {
    const req: SigningRequest = {
      documentId: 'doc-sr-001',
      walletAddress: 'addr_test1abc',
      hash: 'sha256:request_hash',
      nonce: 'nonce-12345',
      expiresAt: new Date(Date.now() + 60_000).toISOString(),
    };

    saveSigningRequest(req.nonce, req);
    const retrieved = getSigningRequest('nonce-12345');
    expect(retrieved).toBeDefined();
    expect(retrieved!.documentId).toBe('doc-sr-001');

    deleteSigningRequest('nonce-12345');
    expect(getSigningRequest('nonce-12345')).toBeUndefined();
  });

  it('returns undefined for an unknown nonce', () => {
    expect(getSigningRequest('no-such-nonce')).toBeUndefined();
  });
});

// ===========================================================================
// verifyDbReady
// ===========================================================================
describe('verifyDbReady', () => {
  it('resolves when the DB responds', async () => {
    mockQueryRaw.mockResolvedValueOnce([{ '?column?': 1 }]);
    await expect(verifyDbReady()).resolves.toBeUndefined();
  });

  it('throws "Database is required" when the DB is unreachable', async () => {
    mockQueryRaw.mockRejectedValueOnce(new Error('ECONNREFUSED'));
    await expect(verifyDbReady()).rejects.toThrow(/Database is required/i);
  });
});

// ===========================================================================
// getDocument
// ===========================================================================
describe('getDocument', () => {
  it('returns the mapped record when the row exists', async () => {
    mockQueryRaw.mockResolvedValueOnce([makeDbRow({ external_id: 'doc-001', document_type: 'certificate' })]);
    const doc = await getDocument('doc-001', TEST_TENANT);

    expect(doc).not.toBeNull();
    expect(doc!.id).toBe('doc-001');
    expect(doc!.type).toBe('certificate');
    expect(doc!.status).toBe('draft');
    expect(doc!.owner.id).toBe(TEST_OWNER_UUID);
    expect(doc!.data.title).toBe('Test Document');
    expect(doc!.contentHash).toBe('sha256:doc-001');
  });

  it('returns null when no row matches', async () => {
    mockQueryRaw.mockResolvedValue([]); // external_id (and uuid, if attempted) lookups both empty
    expect(await getDocument('doc-missing', TEST_TENANT)).toBeNull();
  });

  it('propagates a database error', async () => {
    mockQueryRaw.mockRejectedValueOnce(new Error('connection terminated unexpectedly'));
    await expect(getDocument('doc-001', TEST_TENANT)).rejects.toThrow(/connection terminated/);
  });

  it('maps DB status values to the domain status', async () => {
    mockQueryRaw.mockResolvedValueOnce([makeDbRow({ status: 'certified' })]);
    const doc = await getDocument('doc-001', TEST_TENANT);
    expect(doc!.status).toBe('signed'); // 'certified' → 'signed'
  });
});

// ===========================================================================
// listDocuments
// ===========================================================================
describe('listDocuments', () => {
  it('maps rows to domain objects and reports the total', async () => {
    mockQueryRaw.mockResolvedValueOnce([
      makeDbRow({ external_id: 'a', created_at: new Date('2026-01-03T00:00:00Z') }),
      makeDbRow({ external_id: 'b', created_at: new Date('2026-01-02T00:00:00Z') }),
      makeDbRow({ external_id: 'c', created_at: new Date('2026-01-01T00:00:00Z') }),
    ]);
    const { items, total } = await listDocuments(TEST_TENANT, { limit: 100 });
    expect(total).toBe(3);
    expect(items.map((d) => d.id)).toEqual(['a', 'b', 'c']); // already newest-first
  });

  it('sorts newest-first regardless of row order', async () => {
    mockQueryRaw.mockResolvedValueOnce([
      makeDbRow({ external_id: 'old', created_at: new Date('2026-01-01T00:00:00Z') }),
      makeDbRow({ external_id: 'new', created_at: new Date('2026-01-09T00:00:00Z') }),
      makeDbRow({ external_id: 'mid', created_at: new Date('2026-01-05T00:00:00Z') }),
    ]);
    const { items } = await listDocuments(TEST_TENANT);
    expect(items.map((d) => d.id)).toEqual(['new', 'mid', 'old']);
  });

  it('applies the status filter', async () => {
    mockQueryRaw.mockResolvedValueOnce([
      makeDbRow({ external_id: 'd', status: 'draft' }),
      makeDbRow({ external_id: 's', status: 'signed' }),
    ]);
    const { items } = await listDocuments(TEST_TENANT, { status: 'signed' });
    expect(items).toHaveLength(1);
    expect(items[0].id).toBe('s');
  });

  it('paginates with page/limit and returns non-overlapping pages', async () => {
    const rows = Array.from({ length: 5 }, (_, i) =>
      makeDbRow({ external_id: `p${i}`, created_at: new Date(2026, 0, 10 - i) }),
    );
    mockQueryRaw.mockResolvedValue(rows);

    const page1 = await listDocuments(TEST_TENANT, { page: 1, limit: 3 });
    const page2 = await listDocuments(TEST_TENANT, { page: 2, limit: 3 });

    expect(page1.items.length).toBe(3);
    expect(page2.items.length).toBe(2);
    expect(page1.total).toBe(5);
    const overlap = page1.items.map((d) => d.id).filter((id) => page2.items.map((d) => d.id).includes(id));
    expect(overlap).toHaveLength(0);
  });

  it('propagates a database error', async () => {
    mockQueryRaw.mockRejectedValueOnce(new Error('relation "documents" does not exist'));
    await expect(listDocuments(TEST_TENANT)).rejects.toThrow(/does not exist/);
  });
});

// ===========================================================================
// saveDocument
// ===========================================================================
describe('saveDocument', () => {
  it('issues a single INSERT for a non-FK-conflicting owner', async () => {
    mockExecuteRaw.mockResolvedValueOnce(undefined);
    await saveDocument(makeDoc({ id: 'doc-save-001' }), TEST_TENANT);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });

  it('retries with a null owner when the owner FK is violated', async () => {
    mockExecuteRaw
      .mockRejectedValueOnce(new Error('insert or update on table "documents" violates foreign key constraint'))
      .mockResolvedValueOnce(undefined);
    // owner.id must be a valid UUID for the FK-retry branch to engage
    await saveDocument(makeDoc({ id: 'doc-save-fk', owner: { id: TEST_OWNER_UUID } }), TEST_TENANT);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(2);
  });

  it('propagates a non-FK database error', async () => {
    mockExecuteRaw.mockRejectedValueOnce(new Error('disk full'));
    await expect(saveDocument(makeDoc(), TEST_TENANT)).rejects.toThrow(/disk full/);
  });
});

// ===========================================================================
// updateDocument
// ===========================================================================
describe('updateDocument', () => {
  it('returns null (and does not write) when the document is not found', async () => {
    mockQueryRaw.mockResolvedValue([]); // getDocument → null
    const result = await updateDocument('doc-missing', TEST_TENANT, { status: 'signed' });
    expect(result).toBeNull();
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it('merges the updates, writes once, and returns the new record', async () => {
    mockQueryRaw.mockResolvedValueOnce([makeDbRow({ external_id: 'doc-upd', status: 'draft' })]);
    mockExecuteRaw.mockResolvedValueOnce(undefined);

    const before = Date.now();
    const updated = await updateDocument('doc-upd', TEST_TENANT, { status: 'signed' });

    expect(updated).not.toBeNull();
    expect(updated!.status).toBe('signed');
    expect(new Date(updated!.updatedAt).getTime()).toBeGreaterThanOrEqual(before);
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });

  it('propagates a database error from the UPDATE', async () => {
    mockQueryRaw.mockResolvedValueOnce([makeDbRow({ external_id: 'doc-upd-err' })]);
    mockExecuteRaw.mockRejectedValueOnce(new Error('deadlock detected'));
    await expect(updateDocument('doc-upd-err', TEST_TENANT, { status: 'anchored' })).rejects.toThrow(/deadlock/);
  });

  // KS-550: fromDbRow spreads the stored metadata blob into `data`, so the
  // read-back document carries the PREVIOUS blockchain under data.blockchain.
  // The metadata written by updateDocument must take the update's blockchain,
  // not the stale copy riding in the data spread — before the fix, every
  // KS-535 poll/reconcile write was silently lost in `metadata` (while
  // certification_metadata got the truth, so the two blobs diverged).
  it('persists the fresh blockchain block into metadata, not the stale copy from data (KS-550)', async () => {
    const staleBlockchain = { status: 'pending', txHash: null, anchorId: 'anchor-1', blockHeight: 0 };
    mockQueryRaw.mockResolvedValueOnce([
      makeDbRow({
        external_id: 'doc-ks550',
        status: 'anchored',
        metadata: { title: 'Test Document', blockchain: staleBlockchain, signatures: [] },
        certification_metadata: { blockchain: staleBlockchain, signatures: [] },
      }),
    ]);
    mockExecuteRaw.mockResolvedValueOnce(undefined);

    const freshBlockchain = {
      status: 'confirmed',
      txHash: 'a'.repeat(64),
      anchorId: 'anchor-1',
      blockHeight: 4531884,
    };
    await updateDocument('doc-ks550', TEST_TENANT, { blockchain: freshBlockchain, status: 'anchored' });

    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    // Tagged-template call: [strings, preserveTerminal, status, metadata, certMeta, id, tenantId]
    const values = mockExecuteRaw.mock.calls[0].slice(1);
    const metadataJson = values.find(
      (v: unknown) => typeof v === 'string' && (v as string).includes('"blockchain"'),
    ) as string;
    const certMetaJson = values.filter(
      (v: unknown) => typeof v === 'string' && (v as string).includes('"blockchain"'),
    )[1] as string;

    expect(JSON.parse(metadataJson).blockchain).toEqual(freshBlockchain);
    expect(JSON.parse(certMetaJson).blockchain).toEqual(freshBlockchain);
    // The stale copy must not survive anywhere in the metadata blob.
    expect(metadataJson).not.toContain('"status":"pending"');
    // Non-reserved data keys still round-trip.
    expect(JSON.parse(metadataJson).title).toBe('Test Document');
  });

  it('a non-blockchain update re-persists the authoritative blockchain, healing a stale metadata copy (KS-550)', async () => {
    const staleBlockchain = { status: 'pending', txHash: null, anchorId: 'anchor-2', blockHeight: 0 };
    const truthBlockchain = { status: 'confirmed', txHash: 'b'.repeat(64), anchorId: 'anchor-2', blockHeight: 100 };
    mockQueryRaw.mockResolvedValueOnce([
      makeDbRow({
        external_id: 'doc-ks550-heal',
        metadata: { title: 'Test Document', blockchain: staleBlockchain },
        // fromDbRow prefers certification_metadata.blockchain — the truth.
        certification_metadata: { blockchain: truthBlockchain, signatures: [] },
      }),
    ]);
    mockExecuteRaw.mockResolvedValueOnce(undefined);

    await updateDocument('doc-ks550-heal', TEST_TENANT, { status: 'signed' });

    const values = mockExecuteRaw.mock.calls[0].slice(1);
    const metadataJson = values.find(
      (v: unknown) => typeof v === 'string' && (v as string).includes('"blockchain"'),
    ) as string;
    expect(JSON.parse(metadataJson).blockchain).toEqual(truthBlockchain);
  });
});

// =============================================================================
// KS-70 — parent_document_id lineage walks
// =============================================================================
//
// walkAncestors runs an n-step Postgres recursive read. Each step calls
// $queryRaw exactly once with the current cursor — the mock returns rows
// shaped like the SQL projection in the implementation:
//   { id, external_id, content_hash, document_type, status, created_at,
//     parent_external_id }
// We control the chain by queueing the mock responses in order.

function makeLineageRow(externalId: string, parentExternalId: string | null): Record<string, unknown> {
  return {
    id: 'uuid-' + externalId,
    external_id: externalId,
    content_hash: 'hash-' + externalId,
    document_type: 'certificate',
    status: 'signed',
    created_at: new Date('2026-05-14T12:00:00Z'),
    parent_external_id: parentExternalId,
  };
}

describe('walkAncestors (KS-70)', () => {
  beforeEach(() => {
    mockQueryRaw.mockReset();
    mockExecuteRaw.mockReset();
  });

  it('returns just the starting doc when it has no parent', async () => {
    mockQueryRaw.mockResolvedValueOnce([makeLineageRow('A', null)]);
    const { lineage, truncated } = await walkAncestors('A', TEST_TENANT);
    expect(lineage.map((e) => e.id)).toEqual(['A']);
    expect(truncated).toBe(false);
    expect(mockQueryRaw).toHaveBeenCalledTimes(1);
  });

  it('walks a 3-step chain newest-first and terminates at the root', async () => {
    mockQueryRaw
      .mockResolvedValueOnce([makeLineageRow('C', 'B')])
      .mockResolvedValueOnce([makeLineageRow('B', 'A')])
      .mockResolvedValueOnce([makeLineageRow('A', null)]);
    const { lineage, truncated } = await walkAncestors('C', TEST_TENANT);
    expect(lineage.map((e) => e.id)).toEqual(['C', 'B', 'A']);
    expect(truncated).toBe(false);
  });

  it('truncates at MAX_LINEAGE_DEPTH and reports truncated=true', async () => {
    // Build a chain longer than the cap. Each step's "parent" points at
    // the next entry by name, never reaching null until depth > cap.
    for (let i = 0; i < MAX_LINEAGE_DEPTH; i++) {
      mockQueryRaw.mockResolvedValueOnce([makeLineageRow(`step-${i}`, `step-${i + 1}`)]);
    }
    const { lineage, truncated } = await walkAncestors('step-0', TEST_TENANT);
    expect(lineage).toHaveLength(MAX_LINEAGE_DEPTH);
    expect(truncated).toBe(true);
  });

  it('stops at a cross-tenant parent (LEFT JOIN returns null parent_external_id)', async () => {
    mockQueryRaw
      .mockResolvedValueOnce([makeLineageRow('child', 'parent-in-other-tenant')])
      .mockResolvedValueOnce([{ ...makeLineageRow('parent-in-other-tenant', null), parent_external_id: null }]);
    const { lineage } = await walkAncestors('child', TEST_TENANT);
    expect(lineage.map((e) => e.id)).toEqual(['child', 'parent-in-other-tenant']);
  });

  it('returns empty lineage if the starting doc does not exist', async () => {
    mockQueryRaw.mockResolvedValueOnce([]);
    const { lineage, truncated } = await walkAncestors('ghost', TEST_TENANT);
    expect(lineage).toEqual([]);
    expect(truncated).toBe(false);
  });

  it('breaks on cycle (defensive — visited set short-circuits revisit)', async () => {
    // A → B → A would loop forever without the seen-set guard.
    mockQueryRaw
      .mockResolvedValueOnce([makeLineageRow('A', 'B')])
      .mockResolvedValueOnce([makeLineageRow('B', 'A')]);
    const { lineage } = await walkAncestors('A', TEST_TENANT);
    expect(lineage.map((e) => e.id)).toEqual(['A', 'B']);
    // No third call — the loop terminated.
    expect(mockQueryRaw).toHaveBeenCalledTimes(2);
  });

  it('honours an explicit maxDepth override', async () => {
    mockQueryRaw
      .mockResolvedValueOnce([makeLineageRow('one', 'two')])
      .mockResolvedValueOnce([makeLineageRow('two', 'three')]);
    const { lineage, truncated } = await walkAncestors('one', TEST_TENANT, { maxDepth: 2 });
    expect(lineage).toHaveLength(2);
    expect(truncated).toBe(true);
  });
});

describe('assertNoCycle (KS-70)', () => {
  beforeEach(() => {
    mockQueryRaw.mockReset();
    mockExecuteRaw.mockReset();
  });

  it('resolves with the parent\'s ancestor chain when no cycle is present', async () => {
    mockQueryRaw
      .mockResolvedValueOnce([makeLineageRow('parent', 'grandparent')])
      .mockResolvedValueOnce([makeLineageRow('grandparent', null)]);
    const chain = await assertNoCycle('new-id', 'parent', TEST_TENANT);
    expect(chain.map((e) => e.id)).toEqual(['parent', 'grandparent']);
  });

  it('throws LINEAGE_CYCLE when the new doc appears in the parent\'s chain', async () => {
    // Caller is trying to make new-id a child of "B" — but B's chain
    // already includes new-id, so adopting it would create a cycle.
    mockQueryRaw
      .mockResolvedValueOnce([makeLineageRow('B', 'new-id')])
      .mockResolvedValueOnce([makeLineageRow('new-id', null)]);
    await expect(assertNoCycle('new-id', 'B', TEST_TENANT)).rejects.toMatchObject({
      code: 'LINEAGE_CYCLE',
    });
  });

  it('does not throw for an unrelated long chain (truncated but acyclic)', async () => {
    for (let i = 0; i < MAX_LINEAGE_DEPTH; i++) {
      mockQueryRaw.mockResolvedValueOnce([makeLineageRow(`p-${i}`, `p-${i + 1}`)]);
    }
    await expect(assertNoCycle('new-id', 'p-0', TEST_TENANT)).resolves.toBeDefined();
  });
});

// =============================================================================
// walkDescendants (KS-280) — forward (descendant) lineage tree walk.
// First $queryRaw resolves the start doc's internal id; then one query per
// queued node returns its children (shape: { id, external_id, content_hash,
// document_type, status, created_at } — no parent_external_id).
// =============================================================================

function makeStartIdRow(externalId: string): Record<string, unknown> {
  return { id: 'uuid-' + externalId };
}

function makeChildRow(externalId: string, status = 'draft'): Record<string, unknown> {
  return {
    id: 'uuid-' + externalId,
    external_id: externalId,
    content_hash: 'hash-' + externalId,
    document_type: 'certificate',
    status,
    created_at: new Date('2026-05-15T12:00:00Z'),
  };
}

describe('walkDescendants (KS-280)', () => {
  beforeEach(() => {
    mockQueryRaw.mockReset();
    mockExecuteRaw.mockReset();
  });

  it('returns no descendants for a leaf document', async () => {
    mockQueryRaw
      .mockResolvedValueOnce([makeStartIdRow('v1')]) // resolve start id
      .mockResolvedValueOnce([]); // v1 has no children
    const { descendants, truncated } = await walkDescendants('v1', TEST_TENANT);
    expect(descendants).toEqual([]);
    expect(truncated).toBe(false);
  });

  it('returns empty when the starting doc does not exist', async () => {
    mockQueryRaw.mockResolvedValueOnce([]); // start id not found
    const { descendants, truncated } = await walkDescendants('ghost', TEST_TENANT);
    expect(descendants).toEqual([]);
    expect(truncated).toBe(false);
    expect(mockQueryRaw).toHaveBeenCalledTimes(1);
  });

  it('surfaces a single newer version with its certification status (will v1→v2)', async () => {
    mockQueryRaw
      .mockResolvedValueOnce([makeStartIdRow('v1')])
      .mockResolvedValueOnce([makeChildRow('v2', 'certified')]) // children of v1
      .mockResolvedValueOnce([]); // children of v2
    const { descendants, truncated } = await walkDescendants('v1', TEST_TENANT);
    expect(descendants.map((d) => d.id)).toEqual(['v2']);
    expect(descendants[0].status).toBe('certified');
    expect(truncated).toBe(false);
  });

  it('walks a branching tree breadth-first', async () => {
    mockQueryRaw
      .mockResolvedValueOnce([makeStartIdRow('v1')])
      .mockResolvedValueOnce([makeChildRow('v2a'), makeChildRow('v2b')]) // children of v1
      .mockResolvedValueOnce([makeChildRow('v3')]) // children of v2a
      .mockResolvedValueOnce([]) // children of v2b
      .mockResolvedValueOnce([]); // children of v3
    const { descendants } = await walkDescendants('v1', TEST_TENANT);
    expect(descendants.map((d) => d.id)).toEqual(['v2a', 'v2b', 'v3']);
  });

  it('caps at maxNodes and reports truncated=true', async () => {
    mockQueryRaw
      .mockResolvedValueOnce([makeStartIdRow('v1')])
      .mockResolvedValueOnce([makeChildRow('a'), makeChildRow('b'), makeChildRow('c')]);
    const { descendants, truncated } = await walkDescendants('v1', TEST_TENANT, { maxNodes: 2 });
    expect(descendants).toHaveLength(2);
    expect(truncated).toBe(true);
  });

  it('breaks on a cyclic parent pointer (visited-set guard)', async () => {
    mockQueryRaw
      .mockResolvedValueOnce([makeStartIdRow('v1')])
      .mockResolvedValueOnce([makeChildRow('v2')]) // children of v1
      .mockResolvedValueOnce([makeChildRow('v1')]); // children of v2 point back at v1 → skipped
    const { descendants } = await walkDescendants('v1', TEST_TENANT);
    expect(descendants.map((d) => d.id)).toEqual(['v2']);
    expect(mockQueryRaw).toHaveBeenCalledTimes(3); // resolve + 2 child queries, no loop
  });
});
