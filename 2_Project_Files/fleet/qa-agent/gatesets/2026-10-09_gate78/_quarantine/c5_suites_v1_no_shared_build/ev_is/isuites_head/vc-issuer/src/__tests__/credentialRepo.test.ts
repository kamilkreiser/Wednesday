/**
 * T2-D unit tests for credentialRepo. Mocks the db module so the
 * memory-fallback paths are tested without a real Postgres.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock the db module BEFORE importing the repo so the import-time
// references resolve to the mocks.
vi.mock('../db', () => ({
  isDbAvailable: vi.fn(() => false), // force memory-fallback path
  query: vi.fn(),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
}));

import * as repo from '../repositories/credentialRepo';

function makeCredential(overrides: Record<string, unknown> = {}) {
  return {
    '@context': ['https://www.w3.org/2018/credentials/v1'],
    id: `urn:vc:${Math.random().toString(36).slice(2, 8)}`,
    type: ['VerifiableCredential', 'SecuuraCredential'],
    issuer: { id: 'did:secuura:issuer-1', name: 'Issuer' },
    issuanceDate: new Date().toISOString(),
    credentialSubject: {
      id: 'did:secuura:holder-1',
      documentHash: 'sha256:abc',
    },
    credentialStatus: { id: 'urn:status:1', type: 'StatusList2021', revoked: false },
    proof: { type: 'Ed25519Signature2020', created: '2026-01-01', verificationMethod: 'did:secuura:issuer-1#k', proofPurpose: 'assertionMethod', proofValue: 'z...' },
    ...overrides,
  } as any;
}

describe('credentialRepo (memory-only mode)', () => {
  beforeEach(async () => {
    // Drain memory store between tests by listing then deleting via the
    // module's internal Map. There's no public clear; we hack by
    // re-requiring is fine because we just bulk-revoke via the test.
    const { credentials } = await repo.list({ limit: 9999 });
    for (const c of credentials) {
      // overwrite with same id so subsequent test sees only fresh data —
      // not perfect isolation but adequate for these focused tests.
      await repo.store({ ...c, _drained: true } as any);
    }
  });

  it('store + getById round-trips a credential', async () => {
    const c = makeCredential();
    await repo.store(c);
    const got = await repo.getById(c.id);
    expect(got).toBeDefined();
    expect(got!.id).toBe(c.id);
  });

  it('RED KS-1121 A: getById resolves a credential by its EXACT id only - every fragment is undefined', async () => {
    const stored = makeCredential({ id: 'urn:vc:abcdef-1234' });
    await repo.store(stored);
    expect((await repo.getById(stored.id))?.id).toBe('urn:vc:abcdef-1234');
    for (const fragment of ['abcdef', 'urn:vc:abc', '1234', 'bcde', 'urn:vc:abcdef-123', '%', '_']) {
      expect(await repo.getById(fragment), 'fragment ' + fragment).toBeUndefined();
    }
  });

  it('RED KS-1121 B: revoke on a fragment returns undefined and mutates nothing', async () => {
    const target = makeCredential({ id: 'urn:vc:revoke-target-5678' });
    await repo.store(target);
    expect(await repo.revoke('revoke-target', 'fragment')).toBeUndefined();
    expect((await repo.getById(target.id))?.credentialStatus?.revoked).toBe(false);
  });

  it('RED KS-1121 C: DB path - an unknown id costs exactly ONE lookup query, and it is never a LIKE', async () => {
    const db = await import('../db');
    vi.mocked(db.isDbAvailable).mockReturnValue(true);
    vi.mocked(db.query).mockResolvedValue({ rows: [] } as any);
    try {
      expect(await repo.getById('abcdef')).toBeUndefined();
      const lookups = vi.mocked(db.query).mock.calls.map((call) => String(call[0])).filter((sql) => /SELECT credential/i.test(sql));
      expect(lookups).toHaveLength(1);
      expect(lookups[0]).not.toMatch(/ LIKE /i);
    } finally {
      vi.mocked(db.isDbAvailable).mockReturnValue(false);
      vi.mocked(db.query).mockReset();
    }
  });

  it('getById returns undefined for a totally absent id', async () => {
    const got = await repo.getById('urn:vc:no-such-thing-9999');
    expect(got).toBeUndefined();
  });

  it('getByHash finds a credential whose subject documentHash matches', async () => {
    const c = makeCredential({
      id: 'urn:vc:hash-1',
      credentialSubject: { id: 'did:secuura:holder-2', documentHash: 'sha256:deadbeef' },
    });
    await repo.store(c);
    const got = await repo.getByHash('sha256:deadbeef');
    expect(got?.id).toBe('urn:vc:hash-1');
  });

  it('list with no filters returns all stored credentials', async () => {
    const a = makeCredential({ id: 'urn:vc:list-a' });
    const b = makeCredential({ id: 'urn:vc:list-b' });
    await repo.store(a);
    await repo.store(b);
    const out = await repo.list();
    const ids = out.credentials.map((c) => c.id);
    expect(ids).toEqual(expect.arrayContaining(['urn:vc:list-a', 'urn:vc:list-b']));
  });

  it('list filters by issuer id', async () => {
    const a = makeCredential({ id: 'urn:vc:f-a', issuer: { id: 'did:secuura:i-A' } });
    const b = makeCredential({ id: 'urn:vc:f-b', issuer: { id: 'did:secuura:i-B' } });
    await repo.store(a);
    await repo.store(b);
    const out = await repo.list({ issuer: 'did:secuura:i-A' });
    const ids = out.credentials.map((c) => c.id);
    expect(ids).toContain('urn:vc:f-a');
    expect(ids).not.toContain('urn:vc:f-b');
  });

  it('list paginates via limit + offset', async () => {
    for (let i = 0; i < 5; i++) {
      await repo.store(makeCredential({ id: `urn:vc:page-${i}` }));
    }
    const page1 = await repo.list({ limit: 2, offset: 0 });
    const page2 = await repo.list({ limit: 2, offset: 2 });
    expect(page1.credentials.length).toBe(2);
    expect(page2.credentials.length).toBe(2);
    // total reflects all matching, not just the page
    expect(page1.total).toBeGreaterThanOrEqual(5);
  });

  it('revoke marks the credential as revoked + records reason + timestamp', async () => {
    const c = makeCredential({ id: 'urn:vc:rev-1' });
    await repo.store(c);
    const revoked = await repo.revoke('urn:vc:rev-1', 'compromised key');
    expect(revoked?.credentialStatus?.revoked).toBe(true);
    expect(revoked?.credentialStatus?.revocationReason).toBe('compromised key');
    expect(revoked?.credentialStatus?.revokedAt).toBeTruthy();
  });

  it('revoke on an unknown id returns undefined', async () => {
    const r = await repo.revoke('urn:vc:no-such-revoke');
    expect(r).toBeUndefined();
  });
});
