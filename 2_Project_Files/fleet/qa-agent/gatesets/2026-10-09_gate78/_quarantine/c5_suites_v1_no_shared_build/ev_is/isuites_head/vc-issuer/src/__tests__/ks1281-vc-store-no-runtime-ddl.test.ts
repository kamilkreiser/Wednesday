/**
 * KS-1281: credentialRepo.ensureTable() ran CREATE TABLE IF NOT EXISTS vc_credentials_store at runtime. The
 * runtime role has no CREATE on schema public (least privilege), so every vc-issuer boot logged a WARN, and
 * migration 001 already owns the table. The db module is mocked in the credentialRepo.test.ts shape, with the
 * database reported AVAILABLE, and every statement the repository sends is read back from the query mock.
 */
import { describe, it, expect, vi } from 'vitest';

vi.mock('../db', () => ({
  isDbAvailable: vi.fn(() => true),
  query: vi.fn(async () => ({ rows: [], rowCount: 0 })),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
}));

import * as db from '../db';
import * as repo from '../repositories/credentialRepo';

const sentSql = (): string[] => (db.query as any).mock.calls.map((c: unknown[]) => String(c[0]));

function credential(id: string) {
  return {
    '@context': ['https://www.w3.org/2018/credentials/v1'],
    id,
    type: ['VerifiableCredential', 'SecuuraCredential'],
    issuer: { id: 'did:secuura:issuer-1281', name: 'Issuer' },
    issuanceDate: '2026-09-25T00:00:00.000Z',
    credentialSubject: { id: 'did:secuura:holder-1281', documentHash: 'sha256:ks1281' },
    credentialStatus: { id: 'urn:status:1281', type: 'StatusList2021', revoked: false },
    proof: { type: 'Ed25519Signature2020', created: '2026-09-25', verificationMethod: 'did:secuura:issuer-1281#k', proofPurpose: 'assertionMethod', proofValue: 'z1281' },
  } as any;
}

describe('KS-1281: the VC store issues no DDL at runtime', () => {
  it('RED KS-1281 - storing a credential sends no CREATE TABLE statement to the database', async () => {
    await repo.store(credential('urn:vc:ks1281-a'));
    expect(sentSql().filter((s) => s.toUpperCase().includes('CREATE TABLE'))).toEqual([]);
  });

  it('CONTROL - the credential row itself still reaches vc_credentials_store', async () => {
    await repo.store(credential('urn:vc:ks1281-b'));
    expect(sentSql().some((s) => s.includes('INSERT INTO vc_credentials_store'))).toBe(true);
  });
});
