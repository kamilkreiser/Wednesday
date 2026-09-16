// qa1013-drafter-probe.test.ts — DRAFTER PROBE (recording, not pass/fail). REAL userRepo + REAL routers + REAL errorHandler on 127.0.0.1:0;
// db.query, subjectDeks.getDek, @secuura/shared crypto, authenticate, logger stubbed. Conditions a..e per route. Rows -> QA1013_ROWS json.
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import express from 'express';
import { writeFileSync } from 'node:fs';

const S = vi.hoisted(() => ({ cond: 'a', hits: { query: 0, getDek: 0 }, logs: [] as Array<{ level: string; msg: string; meta: unknown }> }));
const UID = 'aaaaaaaa-1111-4111-8111-aaaaaaaaaaaa';
vi.mock('@secuura/shared', async (importOriginal) => {
  const actual = await importOriginal<Record<string, unknown>>();
  return { ...actual, encryptField: (v: string) => v, decryptField: (v: string) => v, encryptFieldWithDek: (v: string) => v,
    decryptFieldWithDek: (v: string) => v.replace(/^sdek:/, ''), isSubjectDekCiphertext: (v: unknown) => typeof v === 'string' && v.startsWith('sdek:'),
    isEncryptedPii: (v: unknown) => typeof v === 'string' && v.startsWith('sdek:'), lookupHash: (v: string) => `hash:${v}` };
});
vi.mock('../services/subjectDeks', () => ({ subjectDeks: {
  getDek: vi.fn(async () => { S.hits.getDek++; if (S.cond === 'b') { const e: any = new Error('connection terminated unexpectedly'); throw e; } return Buffer.from('k'); }),
  getOrCreateDek: vi.fn(async () => Buffer.from('k')), evict: vi.fn() } }));
vi.mock('../utils/logger', () => ({ logger: {
  info: (msg: string, meta: unknown) => S.logs.push({ level: 'info', msg, meta }), warn: (msg: string, meta: unknown) => S.logs.push({ level: 'warn', msg, meta }),
  error: (msg: string, meta: unknown) => S.logs.push({ level: 'error', msg, meta }), debug: () => {} } }));
vi.mock('../db', () => ({ isDbAvailable: () => true, getPool: () => ({}),
  query: vi.fn(async (sql: string, params: unknown[] = []) => {
    S.hits.query++;
    if (S.cond === 'e') { throw new Error('connection terminated unexpectedly'); }
    if (/from\s+(users|auth_find_user_by_id)/i.test(sql) && String(params[0]) === UID) {
      if (S.cond === 'd') return { rows: [], rowCount: 0 };
      const email = S.cond === 'c' ? 'plain@example.invalid' : 'sdek:enc@example.invalid';
      return { rows: [{ id: UID, email, status: 'active', role: 'user', mfa_enabled: false, wallet_address: '0xabc', created_at: '2026-01-01T00:00:00Z', updated_at: '2026-01-01T00:00:00Z' }], rowCount: 1 };
    }
    return { rows: [], rowCount: 0 };
  }) }));
vi.mock('../middleware/authenticate', () => {
  const inject = () => (req: any, _res: any, next: any) => { req.user = { userId: UID, role: 'OWNER', tenantId: 'tenant-default' }; next(); };
  return { authenticate: inject, authenticateAccessOrConnector: inject };
});

import { userRoutes } from '../routes/users';
import { mfaRoutes } from '../routes/mfa';
import { walletRoutes } from '../routes/wallet';
import { errorHandler } from '../middleware/errorHandler';
import * as repo from '../repositories/userRepo';

let server: Server; let base = '';
beforeAll(async () => {
  const app = express(); app.use(express.json());
  app.use('/api/users', userRoutes); app.use('/api/auth/mfa', mfaRoutes); app.use('/api/auth/wallet', walletRoutes); app.use(errorHandler);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`; r(); }); });
});
afterAll(async () => { server.closeAllConnections(); await new Promise<void>((r) => server.close(() => r())); });

const ROUTES: Array<[string, string]> = [['GET', '/api/users/me'], ['GET', '/api/auth/mfa/status'], ['DELETE', '/api/auth/wallet/unlink'], ['POST', '/api/auth/mfa/backup-codes/regenerate']];
describe('qa1013 drafter probe', () => {
  it('records rows', async () => {
    const rows: unknown[] = [];
    for (const cond of ['a', 'b', 'c', 'd', 'e']) {
      for (const [m, p] of ROUTES) {
        S.cond = cond; S.hits = { query: 0, getDek: 0 }; S.logs = [];
        const savedEnv = process.env.NODE_ENV; if (cond === 'c') process.env.NODE_ENV = 'production';
        let status = 0; let body = ''; let retryAfter: string | null = null;
        try { const r = await fetch(base + p, { method: m, headers: { 'content-type': 'application/json' }, body: m === 'GET' ? undefined : '{}' }); status = r.status; retryAfter = r.headers.get('retry-after'); body = await r.text(); }
        finally { process.env.NODE_ENV = savedEnv; }
        rows.push({ cond, route: `${m} ${p}`, status, retryAfter, body: body.slice(0, 240), hits: { ...S.hits }, errorLogs: S.logs.filter((l) => l.level === 'error').map((l) => ({ msg: l.msg, meta: JSON.stringify(l.meta).slice(0, 400) })), bodyHasUid: body.includes(UID), logsHaveUid: JSON.stringify(S.logs).includes(UID), logsHaveStack: JSON.stringify(S.logs).includes('    at ') });
      }
    }
    // sibling direct calls under (b): getUserByIdWithPasswordHash (:446 head) and getUserByIdPreAuth (:512 head; /oauth/token's read)
    for (const fn of ['getUserByIdWithPasswordHash', 'getUserByIdPreAuth', 'getUserById'] as const) {
      S.cond = 'b'; S.logs = [];
      let outcome = '';
      try { await (repo as any)[fn](UID); outcome = 'resolved'; } catch (e: any) { outcome = `${e?.constructor?.name} ${e?.statusCode ?? '-'} ${e?.message}`; }
      rows.push({ cond: 'b-direct', route: fn, outcome, errorLogs: S.logs.filter((l) => l.level === 'error').map((l) => l.msg) });
    }
    writeFileSync(process.env.QA1013_ROWS as string, JSON.stringify(rows, null, 1));
    expect(rows.length).toBeGreaterThan(0);
  }, 30000);
});
