/**
 * QA gate 30 PROBE (not for commit): the backup-code burn under concurrency, over a STATEFUL db stub that applies
 * `UPDATE users SET mfa_backup_codes = $1 ... WHERE id = $n` last-write-wins, as Postgres does for a plain UPDATE
 * with no row lock and no compare-and-swap. Each "request" snapshots the row first, as the login route does
 * (the user object is read before the gate runs).
 */
import { describe, it, expect, vi, beforeAll, beforeEach } from 'vitest';

const db = vi.hoisted(() => ({ codes: [] as string[], updates: [] as Array<{ sql: string; values: unknown[] }> }));
const silent = vi.hoisted(() => ({ debug: () => {}, info: () => {}, warn: () => {}, error: () => {}, log: () => {} }));
vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent, validateEnv: vi.fn() }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: silent, createLogger: () => silent }));

const USER_ID = 'c1000000-0000-4000-8000-000000000030';
const TENANT_ID = 'b1000000-0000-4000-8000-000000000030';
function row() {
  return {
    id: USER_ID, email: 'g30@example.test', first_name: null, last_name: null, display_name: null,
    role: 'user', status: 'active', email_verified: true, phone_number: null, phone_verified: false,
    mfa_enabled: true, mfa_secret: null, mfa_backup_codes: [...db.codes], verification_level: 'basic',
    organization_id: null, tenant_id: TENANT_ID, tenant_slug: null, wallet_address: null, auth_method: 'password',
    external_provider: null, external_id: null, google_id: null, linkedin_id: null, facebook_id: null,
    apple_id: null, github_id: null, microsoft_personal_id: null, metadata: null,
    created_at: new Date(), updated_at: new Date(), last_login_at: null,
  };
}
vi.mock('../db', () => ({
  isDbAvailable: () => true,
  getPool: () => ({}),
  query: vi.fn(async (sql: string, values: unknown[] = []) => {
    if (/^\s*UPDATE\s+users/i.test(sql)) {
      db.updates.push({ sql, values });
      if (/mfa_backup_codes\s*=\s*\$1/.test(sql)) db.codes = [...(values[0] as string[])];
      return { rows: [], rowCount: 1 };
    }
    if (/auth_find_user_by_id/i.test(sql) || /FROM\s+users\s+WHERE\s+id/i.test(sql)) return { rows: [row()], rowCount: 1 };
    return { rows: [], rowCount: 0 };
  }),
}));
vi.mock('../services/accountLockout', () => ({ isLockedOut: vi.fn(async () => false), recordFailure: vi.fn(async () => {}), recordSuccess: vi.fn(async () => {}) }));
vi.mock('../services/session', () => ({ getRedisClient: vi.fn(() => null), createSession: vi.fn(), revokeSession: vi.fn(), getSession: vi.fn(async () => null), rotateSessionRefreshToken: vi.fn() }));

import { assertAccountMayReceiveCredential } from '../services/passwordLoginGate';
import type { User } from '../types';

const A = 'ABCD2345', B = 'EFGH6789';
let HA: string, HB: string;
beforeAll(async () => { const t = await import('../services/totp'); HA = await t.hashBackupCode(A); HB = await t.hashBackupCode(B); });
beforeEach(() => { db.updates = []; });
const snapshot = (): User => ({ id: USER_ID, email: 'g30@example.test', role: 'USER', status: 'ACTIVE', mfaEnabled: true,
  mfaSecret: 'JBSWY3DPEHPK3PXP', mfaBackupCodes: [...db.codes], tenantId: TENANT_ID } as unknown as User);
const inp = (c: string) => ({ mfaCode: c, sourceIp: '127.0.0.1', route: 'g30-probe', lockoutAlreadyChecked: true });

describe('G30 probe - backup-code burn under concurrency', () => {
  it('P0 CONTROL sequential: the same code twice -> ok then refused (the stub models single-use)', async () => {
    db.codes = [HA];
    const r1 = await assertAccountMayReceiveCredential(snapshot(), inp(A));
    const r2 = await assertAccountMayReceiveCredential(snapshot(), inp(A));
    console.log('G30 P0', JSON.stringify([r1, r2]), 'codes left', db.codes.length);
    expect(r1).toEqual({ ok: true });
    expect(r2).toEqual({ ok: false, reason: 'refused' });
  });

  it('P1 two concurrent sign-ins with the SAME code, both snapshotted before either burn', async () => {
    db.codes = [HA];
    const s1 = snapshot(), s2 = snapshot();
    const rs = await Promise.all([assertAccountMayReceiveCredential(s1, inp(A)), assertAccountMayReceiveCredential(s2, inp(A))]);
    console.log('G30 P1', JSON.stringify(rs), 'UPDATEs', db.updates.length, 'codes left', db.codes.length);
    expect(rs.filter((r) => r.ok).length).toBe(2); // measured outcome recorded, not a desired behaviour
  });

  it('P2 two concurrent sign-ins with DIFFERENT codes A and B: lost update resurrects one spent code', async () => {
    db.codes = [HA, HB];
    const s1 = snapshot(), s2 = snapshot();
    const rs = await Promise.all([assertAccountMayReceiveCredential(s1, inp(A)), assertAccountMayReceiveCredential(s2, inp(B))]);
    const survivors = db.codes.map((h) => (h === HA ? 'A' : h === HB ? 'B' : '?'));
    console.log('G30 P2', JSON.stringify(rs), 'UPDATEs', db.updates.length, 'codes left', JSON.stringify(survivors));
    expect(rs.every((r) => r.ok)).toBe(true);
    expect(survivors.length).toBe(1); // one of the two spent codes is still stored
    const again = await assertAccountMayReceiveCredential(snapshot(), inp(survivors[0] === 'A' ? A : B));
    console.log('G30 P2 reuse of the resurrected spent code ->', JSON.stringify(again));
    expect(again).toEqual({ ok: true });
  });
});
