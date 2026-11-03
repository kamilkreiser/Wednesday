// G161 route driver (gate scratch, NOT for the repo; copied into the clone's __tests__ only for the run, then removed).
// Drives POST /register and POST /forgot-password through the REAL router + error handler with the REAL email.ts
// (base or head, swapped in by the gate), nodemailer replaced so sendMail rejects with each kind. Repository, jwt,
// session, password hashing and events mocked as in ks1868-auth-register-publish-event-unreadable-throw.test.ts.
import { describe, it, beforeAll, afterAll } from 'vitest';
import { vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import fs from 'node:fs';
import express from 'express';

const h = vi.hoisted(() => {
  process.env.SMTP_ENABLED = 'true';
  process.env.SMTP_HOST = 'smtp.stub.invalid';
  process.env.SMTP_FROM = 'no-reply@stub.invalid';
  delete process.env.ACS_CONNECTION_STRING;
  delete process.env.EMAIL_RECIPIENT_ALLOWLIST;
  return { toThrow: undefined as unknown, fail: false, calls: [] as string[] };
});
vi.mock('nodemailer', () => {
  const t = { createTransport: () => ({ sendMail: async () => { h.calls.push('sendMail'); if (h.fail) throw h.toThrow; return { messageId: 'm' }; } }) };
  return { default: t, ...t };
});
vi.mock('../repositories/userRepo', () => {
  const repoMock = {
    getUserByEmail: vi.fn(async (e: string) => (e === 'exists@example.com' ? { id: 'u-exists', email: e, status: 'ACTIVE' } : null)),
    createUser: vi.fn(async (user: Record<string, unknown>) => { h.calls.push('createUser'); return user; }),
    updateUser: vi.fn(async () => null),
    updateUserOrThrow: vi.fn(async () => null),
    storeEmailToken: vi.fn(async () => { h.calls.push('storeEmailToken'); }),
    storeResetToken: vi.fn(async () => { h.calls.push('storeResetToken'); }),
    seedDemoUsers: vi.fn(async () => undefined),
  };
  return { default: repoMock, __esModule: true, ...repoMock };
});
vi.mock('../services/password', async (importOriginal) => ({
  ...(await importOriginal<Record<string, unknown>>()),
  hashPassword: vi.fn(async () => 'hashed'),
}));
vi.mock('../services/jwt', async (importOriginal) => ({
  ...(await importOriginal<Record<string, unknown>>()),
  generateTokenPair: vi.fn(() => ({ accessToken: 'access', refreshToken: 'refresh', expiresIn: 900 })),
}));
vi.mock('../services/session', () => ({
  createSession: vi.fn(async () => { h.calls.push('createSession'); return { id: 'session-g161' }; }),
}));
vi.mock('../events', () => ({ publishEvent: () => Promise.resolve(undefined), EventTypes: { USER_REGISTERED: 'user.registered' } }));
vi.mock('../db', () => ({ isDbAvailable: () => false, query: vi.fn(async () => ({ rows: [] })) }));

import { authRoutes } from '../routes/auth';
import { errorHandler } from '../middleware/errorHandler';

const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMessage = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const KINDS: Record<string, () => unknown> = {
  none: () => undefined,
  ordinaryError: () => new Error('g161 boom'),
  null: () => null,
  undefined: () => undefined,
  revokedProxy: revoked,
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  symbolMessage: () => withMessage(Symbol('g161')),
  messageIsRevokedProxy: () => withMessage(revoked()),
  nullProtoMessage: () => withMessage(Object.create(null)),
};
let server: Server; let baseUrl = '';
const results: unknown[] = [];
beforeAll(async () => {
  const app = express(); app.use(express.json()); app.use('/', authRoutes); app.use(errorHandler);
  server = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => server.once('listening', () => r()));
  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
});
afterAll(async () => {
  await new Promise<void>((r) => server.close(() => r()));
  fs.writeFileSync(process.env.G161_ROUTE_OUT as string, JSON.stringify(results, null, 1));
});
async function post(p: string, body: unknown) {
  const res = await fetch(baseUrl + p, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const text = await res.text(); let code: unknown; try { const j = JSON.parse(text); code = j.error?.code ?? j.code ?? (j.success === true ? 'success' : j.accessToken ? 'tokens' : undefined); } catch { code = 'non-json'; }
  return { status: res.status, code, bodyLen: text.length };
}
describe('G161 route driver', () => {
  for (const kind of Object.keys(KINDS)) {
    it('register ' + kind, async () => {
      h.calls.length = 0; h.fail = kind !== 'none'; h.toThrow = KINDS[kind]();
      const r = await post('/register', { email: 'g161-new@example.com', password: 'Tr0ub4dor&3-horse-staple', name: 'Ann Lee' });
      results.push({ route: 'register', kind, ...r, calls: [...h.calls] });
    });
    for (const email of ['exists@example.com', 'nobody@example.com']) {
      it('forgot ' + email + ' ' + kind, async () => {
        h.calls.length = 0; h.fail = kind !== 'none'; h.toThrow = KINDS[kind]();
        const r = await post('/forgot-password', { email });
        results.push({ route: 'forgot', email, kind, ...r, calls: [...h.calls] });
      });
    }
  }
});
