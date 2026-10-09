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

import { saveDocument, DocumentRecord } from '../repositories/documentRepo';

const TEST_TENANT = 'a0000000-0000-4000-8000-000000000001';
const ORG_UUID = 'c0000000-0000-4000-8000-00000000000a';

function makeDoc(id: string): DocumentRecord {
  return {
    id,
    type: 'degree',
    status: 'draft',
    owner: { id: 'issuer-1', walletAddress: 'addr_test1qexample' },
    data: { title: 'Test Document' },
    contentHash: 'a'.repeat(64),
    signatures: [],
    createdAt: new Date('2026-01-01T00:00:00.000Z'),
    updatedAt: new Date('2026-01-01T00:00:00.000Z'),
  } as unknown as DocumentRecord;
}

/**
 * `$executeRaw` is a tagged template: the mock receives
 * (TemplateStringsArray, ...interpolated values). Joining the strings gives the
 * SQL shape; the values array gives what was bound, in order.
 *
 * The value is read BY POSITION -- the fragment that immediately precedes it --
 * and not by asking whether a uuid appears anywhere in the list. That matters
 * here: the tenant id is bound three times in this statement, so a naive
 * `toContain` would pass while pointing at the wrong binding.
 */
function lastCall() {
  const call = mockExecuteRaw.mock.calls[mockExecuteRaw.mock.calls.length - 1];
  const strings = call[0] as unknown as string[];
  const values = call.slice(1);
  const sql = strings.join(' ');
  const idx = strings.findIndex((s) => /SELECT id FROM organizations WHERE id = $/.test(s));
  return { sql, values, orgIdx: idx, orgValue: idx >= 0 ? values[idx] : undefined };
}

describe('KS-597 -- the issuing organisation is persisted at registration', () => {
  beforeEach(() => {
    mockExecuteRaw.mockReset();
    mockExecuteRaw.mockResolvedValue(1);
  });

  it('writes issuer_organization_id in the INSERT column list', async () => {
    await saveDocument(makeDoc('doc-ks597-a'), TEST_TENANT, undefined, {
      sIdentity: { organizationUuid: ORG_UUID },
    });
    const { sql } = lastCall();
    expect(sql).toContain('issuer_organization_id');
    expect(sql).toMatch(/owner_user_id, issuer_organization_id, metadata/);
  });

  it('resolves the org through a SELECT so an unknown id folds to NULL rather than failing the insert', async () => {
    await saveDocument(makeDoc('doc-ks597-b'), TEST_TENANT, undefined, {
      sIdentity: { organizationUuid: ORG_UUID },
    });
    const { sql, values, orgIdx } = lastCall();
    expect(sql).toContain('SELECT id FROM organizations WHERE id = ');

    // QA Finding 2 (round 1 gate): the assertion here USED to be a bare
    // `expect(sql).toContain('AND tenant_id = ')`, and that is a check that
    // cannot fail. The statement binds the tenant three times, and the
    // pre-existing `parent_document_id` subquery supplies that exact substring
    // on its own -- so with the tenancy predicate deleted from BOTH
    // `organizations` subqueries the assertion still passed, and the gate
    // measured 8/8 cells green against a tree that attributed documents across
    // tenants. The suite was blind to the one property it was written to
    // protect.
    //
    // Pinned two ways, and ROUND 2 OF THE GATE CORRECTED THE FIRST ONE.
    //
    //   1. the organizations subquery matched as ONE UNIT. The first version of
    //      this used `[\s\S]*?` between the two fragments, and that was INERT:
    //      `.` spans newlines and statement boundaries, so the match ran from
    //      the organizations subquery straight into the `parent_document_id`
    //      one and found ITS `AND tenant_id = `. Measured: with the predicate
    //      deleted from both org subqueries and the binding asserts below
    //      neutered, all 8 cells passed. That is the SAME "satisfied by
    //      neighbouring text" defect this cell exists to close, reproduced
    //      inside its own fix. `[^)]` is the bound that fixes it: the org
    //      subquery's closing paren cannot be crossed, so the match can only be
    //      satisfied from inside that subquery.
    //   2. by BINDING POSITION -- the value bound immediately after the org id
    //      inside that same subquery is the tenant. Position is what the rest of
    //      this file already uses (see `lastCall`) precisely because a uuid
    //      appearing somewhere in the list proves nothing about where. This one
    //      was doing all the work while the regex claimed half the credit.
    expect(sql).toMatch(/SELECT id FROM organizations WHERE id = [^)]*?AND tenant_id = /);
    expect(orgIdx).toBeGreaterThanOrEqual(0);
    expect(values[orgIdx + 1]).toBe(TEST_TENANT);
  });

  it('the SKIP-CONFLICT statement carries the tenancy predicate too, not only the upsert one', async () => {
    // Round-2 gate, R2-F1: there are TWO organizations subqueries -- one per
    // conflict tail -- and every cell above drives only the upsert. Deleting the
    // predicate from the skip-conflict subquery ALONE left all 8 cells green,
    // so that statement had no protection at all. The sibling cell below pins
    // that the COLUMN is present on this statement; nothing pinned the
    // PREDICATE, which is the property that stops cross-tenant attribution.
    await saveDocument(makeDoc('doc-ks597-skip-tenancy'), TEST_TENANT, undefined, {
      sIdentity: { organizationUuid: ORG_UUID },
      conflictMode: 'skip',
    });
    const { sql, values, orgIdx } = lastCall();
    // Guard that we are looking at the right statement: if this ever stops being
    // the skip tail, the assertions below would silently be re-testing the upsert.
    expect(sql).toContain('ON CONFLICT (external_id) DO NOTHING');
    expect(sql).toMatch(/SELECT id FROM organizations WHERE id = [^)]*?AND tenant_id = /);
    expect(orgIdx).toBeGreaterThanOrEqual(0);
    expect(values[orgIdx + 1]).toBe(TEST_TENANT);
  });

  it('binds the ROUTE-BOUND issuer org at the org position', async () => {
    await saveDocument(makeDoc('doc-ks597-c'), TEST_TENANT, undefined, {
      issuerOrganizationId: ORG_UUID,
    });
    const { orgIdx, orgValue } = lastCall();
    expect(orgIdx).toBeGreaterThanOrEqual(0);
    expect(orgValue).toBe(ORG_UUID);
  });

  // Kam's "bind the issuer to the actor" ruling (2026-09-07) split these two
  // apart: `sIdentity.organizationUuid` is the caller's RAW CLAIM and belongs
  // only in the metadata, while the column may carry only what the route could
  // bind to the acting Organisation. Before the split this cell would have
  // passed with the claim alone, which is precisely the attribution the ruling
  // refuses -- so it is the regression guard for the separation itself.
  it('does NOT bind the column from the raw sIdentity claim alone -- the route must bind it', async () => {
    await saveDocument(makeDoc('doc-ks597-c2'), TEST_TENANT, undefined, {
      sIdentity: { organizationUuid: ORG_UUID },
    });
    const { orgIdx, orgValue } = lastCall();
    expect(orgIdx).toBeGreaterThanOrEqual(0);
    expect(orgValue).toBeNull();
  });

  // The other half of the same split: an unbindable claim must still be
  // recoverable, so a NULL column is never also a data loss.
  it('still records the raw claim in metadata when the column folds to NULL', async () => {
    await saveDocument(makeDoc('doc-ks597-c3'), TEST_TENANT, undefined, {
      sIdentity: { organizationUuid: ORG_UUID },
    });
    const { values, orgValue } = lastCall();
    expect(orgValue).toBeNull();
    const meta = values.find((v: any) => typeof v === 'string' && v.includes('sIdentity'));
    expect(JSON.parse(meta as string).sIdentity.organizationUuid).toBe(ORG_UUID);
  });

  it('binds NULL at the org position when the caller supplies no organizationUuid', async () => {
    await saveDocument(makeDoc('doc-ks597-d'), TEST_TENANT);
    const { orgIdx, orgValue } = lastCall();
    expect(orgIdx).toBeGreaterThanOrEqual(0);
    expect(orgValue).toBeNull();
  });

  it('binds NULL when organizationUuid is present but not a UUID -- never the raw string', async () => {
    await saveDocument(makeDoc('doc-ks597-e'), TEST_TENANT, undefined, {
      issuerOrganizationId: 'not-a-uuid',
      sIdentity: { organizationUuid: 'not-a-uuid' },
    });
    const { orgValue, values } = lastCall();
    expect(orgValue).toBeNull();
    expect(values).not.toContain('not-a-uuid');
  });

  it('does NOT re-attribute an existing document on the upsert tail', async () => {
    await saveDocument(makeDoc('doc-ks597-f'), TEST_TENANT, undefined, {
      issuerOrganizationId: ORG_UUID,
    });
    const { sql } = lastCall();
    const tail = sql.slice(sql.indexOf('ON CONFLICT'));
    expect(tail).toContain('DO UPDATE SET');
    expect(tail).not.toMatch(/issuer_organization_id\s*=\s*EXCLUDED/);
  });

  it('carries the column on the skip-conflict statement too, not only the upsert one', async () => {
    await saveDocument(makeDoc('doc-ks597-g'), TEST_TENANT, undefined, {
      conflictMode: 'skip',
      issuerOrganizationId: ORG_UUID,
    });
    const { sql, orgValue } = lastCall();
    expect(sql).toContain('ON CONFLICT (external_id) DO NOTHING');
    expect(sql).toContain('issuer_organization_id');
    expect(orgValue).toBe(ORG_UUID);
  });

  it('keeps the caller raw value in metadata as well as in the column', async () => {
    await saveDocument(makeDoc('doc-ks597-h'), TEST_TENANT, undefined, {
      issuerOrganizationId: ORG_UUID,
      sIdentity: { organizationUuid: ORG_UUID },
    });
    const { values } = lastCall();
    const meta = values.find((v: any) => typeof v === 'string' && v.includes('sIdentity'));
    expect(meta).toBeDefined();
    expect(JSON.parse(meta as string).sIdentity.organizationUuid).toBe(ORG_UUID);
  });
});
