/**
 * KS-1295 — credentialRepo.store() must not fall back to memory SILENTLY.
 *
 * The defect: `store()` writes the in-memory map and then `if (!isDbAvailable())
 * return;` with no log at all. The caller is told the credential was stored, nothing
 * reached PostgreSQL, and on restart the credential is gone — leaving no line to grep
 * and no artefact, so the event cannot be investigated after the fact. #1231 made the
 * sibling *table-absent* path loud (two WARNs per store); this is the path it did not
 * touch, raised as P-1 by that PR's gate.
 *
 * Shape (1) of the ticket only: LOG it. Refusing the write is a behaviour change with
 * its own decision and is deliberately not built here.
 *
 * A separate file rather than cells in `credentialRepo.test.ts`, for one reason: that
 * file mocks `isDbAvailable` as a module-scope `vi.fn(() => false)`, so it cannot
 * produce the database-AVAILABLE arm — and without that arm "the WARN does not fire"
 * would be untested. It also carries 3 pre-existing TS2339 (a KS-1090 residue) that
 * are not this ticket's to disturb.
 *
 * Every cell that asserts an ABSENCE here is paired with a control proving the thing
 * could have been present: W2 asserts no WARN, and in the same cell asserts the DB
 * path really was taken (the INSERT was issued). Without that, W2 would pass on a
 * `store()` that did nothing at all.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';

const dbMock = vi.hoisted(() => ({
  isDbAvailable: vi.fn<() => boolean>(() => false),
  query: vi.fn<(sql: string, params?: unknown[]) => Promise<{ rows: any[] }>>(),
}));

vi.mock('../db', () => ({
  isDbAvailable: () => dbMock.isDbAvailable(),
  query: (sql: string, params?: unknown[]) => dbMock.query(sql, params),
}));

const logMock = vi.hoisted(() => ({
  info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn(),
}));
vi.mock('../utils/logger', () => ({ logger: logMock }));

import * as repo from '../repositories/credentialRepo';

let n = 0;
function makeCredential() {
  n += 1;
  return {
    '@context': ['https://www.w3.org/2018/credentials/v1'],
    id: `urn:vc:ks1295-${n}`,
    type: ['VerifiableCredential', 'SecuuraCredential'],
    issuer: { id: 'did:secuura:issuer-1', name: 'Issuer' },
    issuanceDate: '2026-01-01T00:00:00Z',
    credentialSubject: { id: 'did:secuura:holder-1', documentHash: 'sha256:abc' },
  } as any;
}

/** The WARN this ticket is about, identified by its meta rather than by prose alone. */
const UNAVAILABLE_WARNS = () =>
  logMock.warn.mock.calls.filter(
    (c) => String(c[0]).includes('database is unavailable'),
  );

describe('KS-1295 — store() logs when it keeps a credential in memory only', () => {
  beforeEach(() => {
    logMock.warn.mockReset();
    dbMock.query.mockReset();
    dbMock.isDbAvailable.mockReset();
  });

  it('W1 the database is unavailable: exactly one WARN, naming the credential id and the reason', async () => {
    dbMock.isDbAvailable.mockReturnValue(false);
    const c = makeCredential();

    await repo.store(c);

    const warns = UNAVAILABLE_WARNS();
    expect(warns.length).toBe(1);
    const [message, meta] = warns[0] as [string, Record<string, unknown>];
    expect(message).toMatch(/memory only/i);
    expect(meta).toMatchObject({ credentialId: c.id });
    expect(String(meta.reason).length).toBeGreaterThan(0);
    // the fallback really was the path taken, so the WARN is not being produced by
    // some other branch: no SQL was issued at all.
    expect(dbMock.query).not.toHaveBeenCalled();
    // and the credential really is retrievable from memory — the WARN describes a
    // fallback that happened, not a failure.
    expect((await repo.getById(c.id))?.id).toBe(c.id);
  });

  it('W2 the database is available: NO such WARN — and the DB path is proven to have run', async () => {
    dbMock.isDbAvailable.mockReturnValue(true);
    dbMock.query.mockResolvedValue({ rows: [] });
    const c = makeCredential();

    await repo.store(c);

    expect(UNAVAILABLE_WARNS().length).toBe(0);
    // THE CONTROL. Without it this cell would also pass if store() had done nothing,
    // or if the WARN text had simply been misspelled out of existence.
    const inserts = dbMock.query.mock.calls.filter(
      (call) => /INSERT\s+INTO\s+vc_credentials_store/i.test(String(call[0])),
    );
    expect(inserts.length).toBe(1);
    expect(inserts[0][1]).toEqual([c.id, JSON.stringify(c)]);
  });

  it('W3 the WARN is once PER STORE, not once per process', async () => {
    dbMock.isDbAvailable.mockReturnValue(false);
    const a = makeCredential();
    const b = makeCredential();

    await repo.store(a);
    await repo.store(b);

    const warns = UNAVAILABLE_WARNS();
    expect(warns.length).toBe(2);
    expect(warns.map((w) => (w[1] as Record<string, unknown>).credentialId)).toEqual([a.id, b.id]);
  });
});
