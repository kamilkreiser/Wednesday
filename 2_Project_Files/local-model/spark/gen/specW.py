P='Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts'
TP='Blockchain/Dev/services/vc-issuer/src/__tests__/ks1684-revoke-keeps-the-creator-so-the-memory-fallback-still-serves-her.test.ts'
E1=("  const credential = await getById(id);\n  if (!credential) return undefined;\n",
    "  const record = await getRecordById(id);\n  if (!record) return undefined;\n  const credential = record.credential;\n")
E2=("  // Update memory\n  memoryStore.set(credential.id, revokedCredential);\n",
    "  // Update memory\n  memoryStore.set(credential.id, revokedCredential);\n  if (!memoryOwners.has(credential.id)) memoryOwners.set(credential.id, record.owner);\n")
TEST='''// KS-1684 (vc-issuer credentialRepo.revoke): revoke() read the row with getById (the database when it is available) and put the revoked copy into the in-memory store WITHOUT an owner entry,
// so with the database then unavailable the row reads as OWNERLESS and the credential's own creator is refused (the memory fallback fails closed for an owner-less row). The fix reads the record
// (credential + owner) and carries the owner into the in-memory owner map. The database is mocked: a row exists only in the "database" (never stored in this process), is revoked while the
// database is up, and is then read through getRecordById with the database down, which takes the memory path.
import { describe, it, expect, vi, beforeEach } from 'vitest';

const h = vi.hoisted(() => ({
  up: true,
  rows: new Map<string, { credential: any; created_by_user_id: string | null; created_by_tenant_id: string | null }>(),
}));

vi.mock('../db', () => ({
  isDbAvailable: vi.fn(() => h.up),
  query: vi.fn(async (sql: string, params: unknown[] = []) => {
    if (/FROM vc_credentials_store WHERE id = \\$1/.test(sql)) {
      const row = h.rows.get(String(params[0]));
      return { rows: row ? [row] : [] };
    }
    return { rows: [] };
  }),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
}));

import * as repo from '../repositories/credentialRepo';

function cred(id: string) {
  return {
    '@context': ['https://www.w3.org/2018/credentials/v1'],
    id,
    type: ['VerifiableCredential', 'SecuuraCredential'],
    issuer: { id: 'did:secuura:issuer-1', name: 'Issuer' },
    issuanceDate: '2026-10-28T00:00:00.000Z',
    credentialSubject: { id: 'did:secuura:holder-1', documentHash: 'sha256:ks1684' },
    credentialStatus: { id: 'urn:status:1', type: 'StatusList2021', revoked: false },
    proof: { type: 'Ed25519Signature2020', created: '2026-10-28', verificationMethod: 'did:secuura:issuer-1#k', proofPurpose: 'assertionMethod', proofValue: 'z' },
  } as any;
}

beforeEach(() => {
  h.up = true;
  h.rows.clear();
});

describe('KS-1684: revoke() carries the creator into the memory fallback', () => {
  it('RED KS-1684 R1 a database-only row revoked here keeps its creator when the database then goes down', async () => {
    h.rows.set('urn:vc:ks1684-a', { credential: cred('urn:vc:ks1684-a'), created_by_user_id: 'u-alice', created_by_tenant_id: 't-1' });
    const revoked = await repo.revoke('urn:vc:ks1684-a', 'test');
    expect(revoked?.credentialStatus.revoked).toBe(true);
    h.up = false;
    const rec = await repo.getRecordById('urn:vc:ks1684-a');
    expect(rec?.owner).toEqual({ userId: 'u-alice', tenantId: 't-1' });
  });

  it('RED KS-1684 R2 the memory copy is the revoked one and carries a creator owned by the second tenant too', async () => {
    h.rows.set('urn:vc:ks1684-b', { credential: cred('urn:vc:ks1684-b'), created_by_user_id: 'u-bob', created_by_tenant_id: 't-2' });
    await repo.revoke('urn:vc:ks1684-b');
    h.up = false;
    const rec = await repo.getRecordById('urn:vc:ks1684-b');
    expect([rec?.credential.credentialStatus.revoked, rec?.owner.userId, rec?.owner.tenantId]).toEqual([true, 'u-bob', 't-2']);
  });

  it('control KS-1684 C1 a row stored in this process with an owner keeps that owner through revoke', async () => {
    h.up = false;
    await repo.store(cred('urn:vc:ks1684-c'), { userId: 'u-carol', tenantId: 't-3' });
    await repo.revoke('urn:vc:ks1684-c');
    const rec = await repo.getRecordById('urn:vc:ks1684-c');
    expect([rec?.credential.credentialStatus.revoked, rec?.owner]).toEqual([true, { userId: 'u-carol', tenantId: 't-3' }]);
  });

  it('control KS-1684 C2 revoking an unknown id still answers undefined', async () => {
    expect(await repo.revoke('urn:vc:ks1684-missing')).toBeUndefined();
  });

  it('control KS-1684 C3 a database row with no recorded creator is still owner-less after revoke', async () => {
    h.rows.set('urn:vc:ks1684-d', { credential: cred('urn:vc:ks1684-d'), created_by_user_id: null, created_by_tenant_id: null });
    await repo.revoke('urn:vc:ks1684-d');
    h.up = false;
    const rec = await repo.getRecordById('urn:vc:ks1684-d');
    expect(rec?.owner).toEqual({ userId: null, tenantId: null });
  });
});
'''
S=dict(dir='ks_1684_p1',ticket='KS-1684',
 title='vc-issuer: after a revoke, the credential creator can be refused GET /api/credentials/:id on the memory fallback - revoke() stores the row with no owner entry (RUNG 2, code_patch: two hunks in one product + one NEW vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 5 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. The ticket names the fix shape (revoke carries the owner it read: getRecordById instead of getById, writing memoryOwners alongside memoryStore) and the cell that pins it; the failure is closed (availability, not a leak).",
 products=[(P,[E1,E2])],
 prodnote=['product, modified in place: TWO hunks (the read at the top of revoke(), the memory write)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 5 cells (2 red, 3 control; database module mocked, in-memory fallback exercised)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1684-revoke-keeps-the-creator-so-the-memory-fallback-still-serves-her.test.ts` from `Blockchain/Dev/services/vc-issuer',
 tier='code_patch', rung='2 (two hunks, five added lines byte-exact; the new test given whole)',
 pins='''# code_patch, 2 hunks in vc-issuer credentialRepo.ts revoke() + a NEW vitest file; ref = credentialRepo.test.ts (db-mocked memory-fallback shape); line = the first changed line.
tier=code_patch
ref=Blockchain/Dev/services/vc-issuer/src/__tests__/credentialRepo.test.ts
line=444
ctx=65536
''',
 wrong="`revoke()` in `services/vc-issuer/src/repositories/credentialRepo.ts` reads the row with `getById(id)` (from the database when it is available), builds the revoked copy and calls `memoryStore.set(credential.id, revokedCredential)` (`:458`). It never writes a `memoryOwners` entry. `getRecordById` takes the owner on the memory path from `memoryOwners.get(id) ?? OWNERLESS`, and `mayRead` refuses an owner-less row, so for a row this process did not itself `store()` (one created on another replica) that is then revoked here, the creator is refused with the unknown-id 404 whenever the database is unavailable afterwards. It fails closed: a foreign caller is refused too. The change: read the record with `getRecordById(id)` (credential plus owner), use `record.credential` where `credential` was used, and after the memory write add `if (!memoryOwners.has(credential.id)) memoryOwners.set(credential.id, record.owner);` (the same has-check `store()` uses at `:65`).",
 where="- `src/repositories/credentialRepo.ts:444-445` - **must change**: `const credential = await getById(id);` and `if (!credential) return undefined;` become `const record = await getRecordById(id);`, `if (!record) return undefined;`, and a new line `const credential = record.credential;`.\n- `src/repositories/credentialRepo.ts:458` - **must change**: directly after `memoryStore.set(credential.id, revokedCredential);` (under the `// Update memory` comment) one line is added: `if (!memoryOwners.has(credential.id)) memoryOwners.set(credential.id, record.owner);`.\n- `getById`, `getRecordById`, `store` and every other function are NOT touched.",
 exactnote="Two hunks in one file, in file order.\n",
 donot="**Do NOT touch** `getById` (the public verify path's revocation lookup calls it with no principal, by contract), `getRecordById`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await. It uses `vi.hoisted` for the mutable database state the `vi.mock('../db')` factory reads.",
 red=['RED KS-1684 R1','RED KS-1684 R2'],
 cells="- RED `R1`/`R2`: at the tip the row is revoked but the memory copy is owner-less (`{ userId: null, tenantId: null }`), so the owner assertions fail; after the edit the memory owner is the database row's creator.\n- CONTROL `C1` to `C3`: green at the tip AND after (a row stored here keeps its owner; an unknown id answers undefined; a database row with no creator stays owner-less).",
 premises="- `credentialRepo.ts:444-445` and `:458` are the lines quoted above and the only `getById(id)` / `memoryStore.set` in `revoke()` (read at the tip).\n- `getRecordById` (the database SELECT carries `created_by_user_id`, `created_by_tenant_id`) and `memoryOwners` exist at module level in the same file, so no import changes.\n- The service's test runner is vitest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The existing cell Q1 in `ks1116-presentation-and-credential-reads-bound-to-the-creator.test.ts` (a foreign caller is refused after a revoke on the memory path) should stay green: the owner now recorded is the creator, who is not the foreign caller; the whole-suite check (A6) is the measurement.\n- Open PRs touching this file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes KS-1684** (the fix shape and the pinning cell the ticket names). Link the PR as Refs KS-1684 until the QA gate has passed.",
)
