// QA GATE 93 Q2 probe (NOT part of the PR): the PR test harness, recording full responses.
import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import express from 'express';

// KS-1868: POST /login publishes user.login fire-and-forget; when that publish REJECTS, the route's `.catch`
// handler must still log its line `Failed to publish event` even if the rejection value cannot be read (a
// revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`). Today such
// a value makes the `.catch` handler itself throw, so the derived promise rejects with nothing attached and Node
// sees an UNHANDLED REJECTION (the login response was already sent). The cells count unhandled rejections
// themselves instead of letting the runner report them. Harness: the ks1157 route test (real router and error
// handler; repository, password, session, jwt, lockout, mail and event bus mocked). The event bus stand-in
// rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could itself fail on a
// revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  publishRejects: false,
  toThrow: undefined as unknown,
  logged: [] as unknown[][],
  unhandled: 0,
}));

const capture = vi.hoisted(() => ({
  debug: () => undefined,
  info: () => undefined,
  warn: () => undefined,
  error: (...args: unknown[]) => {
    h.logged.push(args);
  },
  log: () => undefined,
}));
vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
vi.mock('@secuura/shared/utils/logger', () => ({ logger: capture, createLogger: () => capture }));

const LOGIN_EMAIL = 'ks1868-login@secuura.local';
const ACTIVE_USER = {
  id: 'user-1868-login', email: LOGIN_EMAIL, status: 'ACTIVE', role: 'OWNER',
  verificationLevel: 'BASIC', mfaEnabled: false, mfaSecret: null, mfaBackupCodes: null,
  passwordHash: '$argon2id$stub', tenantId: 'ten-1', organizationId: 'org-1',
};

vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [], rowCount: 0 })) }));

vi.mock('../repositories/userRepo', () => ({
  getPlatformAdmin: vi.fn(async () => null),
  getUserByEmail: vi.fn(async (email: string) =>
    email.toLowerCase().trim() === LOGIN_EMAIL ? { ...ACTIVE_USER } : null),
  getUserById: vi.fn(async () => null),
  getUserByIdPreAuth: vi.fn(async () => ({ ...ACTIVE_USER })),
  getUserBySocialId: vi.fn(async () => null),
  createUser: vi.fn(async () => null),
  updateUser: vi.fn(async () => ({ ...ACTIVE_USER })),
  updateUserOrThrow: vi.fn(async () => ({ ...ACTIVE_USER })),
  updateUserPlatformScope: vi.fn(async () => null),
  updatePlatformAdminPassword: vi.fn(async () => undefined),
  reencryptMfaSecretIfLegacy: vi.fn(async () => undefined),
  reencryptPlatformAdminMfaSecretIfLegacy: vi.fn(async () => undefined),
}));

vi.mock('../services/password', () => ({
  verifyPassword: vi.fn(async () => true),
  hashPassword: vi.fn(async () => '$argon2id$stub'),
  checkPasswordStrength: vi.fn(() => ({ ok: true })),
  generateResetToken: vi.fn(() => 'tok'),
  shouldRehashAfterVerify: vi.fn(() => false),
}));

vi.mock('../services/session', () => ({
  createSession: vi.fn(async () => ({ id: 'sess-1868-login' })),
  revokeSession: vi.fn(async () => undefined),
  revokeAllUserSessions: vi.fn(async () => 0),
  getSession: vi.fn(async () => null),
  rotateSessionRefreshToken: vi.fn(async () => undefined),
  getRedisClient: vi.fn(() => null),
  validateSession: vi.fn(async () => true),
  updateSessionActivity: vi.fn(async () => undefined),
  isRedisAvailable: vi.fn(() => true),
}));

vi.mock('../services/jwt', () => ({
  generateTokenPair: vi.fn(() => ({ accessToken: 'MINTED_1868_LOGIN', refreshToken: 'MINTED_1868_LOGIN_R', expiresIn: 900 })),
  verifyRefreshToken: vi.fn(() => ({})),
  decodeToken: vi.fn(() => ({})),
}));

vi.mock('../services/refreshDenylist', () => ({ isRefreshJtiDenylisted: vi.fn(async () => false) }));
vi.mock('../services/accountLockout', () => ({
  isLockedOut: vi.fn(async () => false), recordFailure: vi.fn(async () => 1),
  recordSuccess: vi.fn(async () => undefined), clearFailures: vi.fn(async () => undefined),
}));
vi.mock('../services/email', () => ({
  sendVerificationEmail: vi.fn(async () => undefined),
  sendPasswordResetEmail: vi.fn(async () => undefined),
}));

// Used BOTH as mounted middleware and as a factory across the route tree; this stub detects which shape it was
// given (the ks781 / ks1157 harness pattern).
const passThrough = (...args: unknown[]) => {
  if (args.length >= 3 && typeof args[2] === 'function') return (args[2] as () => void)();
  return (_r: unknown, _s: unknown, n: () => void) => n();
};
vi.mock('../middleware/authenticate', () => ({
  authenticate: passThrough, authenticateToken: passThrough,
  authenticateAccessOrConnector: passThrough, optionalAuthenticate: passThrough,
  requireRole: passThrough,
}));
vi.mock('../middleware/tenantGuc', () => ({ seedTenantGuc: (_r: unknown, _s: unknown, n: () => void) => n() }));
vi.mock('../events', () => ({
  publishEvent: () => (h.publishRejects ? Promise.reject(h.toThrow) : Promise.resolve(undefined)),
  EventTypes: { USER_LOGIN: 'user.login' },
}));

const SAVED_LISTENERS = process.listeners('unhandledRejection');
const onUnhandled = () => {
  h.unhandled += 1;
};

let server: Server;
let baseUrl = '';
beforeAll(async () => {
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  const { authRoutes } = await import('../routes/auth');
  const { errorHandler } = await import('../middleware/errorHandler');
  const app = express();
  app.use(express.json());
  app.use('/api/auth', authRoutes);
  app.use(errorHandler);
  server = app.listen(0, '127.0.0.1');
  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
});
afterAll(async () => {
  await new Promise<void>((resolve) => server.close(() => resolve()));
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
});
beforeEach(() => {
  h.publishRejects = false;
  h.toThrow = undefined;
  h.logged.length = 0;
  h.unhandled = 0;
});

const LINES = () => h.logged.filter((c) => c[0] === 'Failed to publish event');

async function login(): Promise<{ status: number; minted: boolean }> {
  const res = await fetch(baseUrl + '/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: LOGIN_EMAIL, password: 'pw-correct-horse' }),
  });
  const text = await res.text();
  return { status: res.status, minted: text.includes('MINTED_1868_LOGIN') };
}

/** The publish is fire-and-forget: wait until its outcome shows (a log line or an unhandled rejection), then a little longer. */
async function settled(): Promise<void> {
  const deadline = Date.now() + 1500;
  while (Date.now() < deadline && LINES().length === 0 && h.unhandled === 0) {
    await new Promise((resolve) => setTimeout(resolve, 10));
  }
  await new Promise((resolve) => setTimeout(resolve, 60));
}

const PATH = '/api/auth/login';
const BODY = JSON.stringify({ email: LOGIN_EMAIL, password: 'pw-correct-horse' });

import { appendFileSync } from 'fs';
const KINDS: Record<string, () => unknown> = {
  none: () => undefined,
  ordinary: () => new Error('bus down'),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  throwingGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
};
describe('gate93 q2 probe', () => {
  for (const k of Object.keys(KINDS)) {
    it(k, async () => {
      h.publishRejects = k !== 'none'; h.toThrow = KINDS[k]();
      const res = await fetch(baseUrl + PATH, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: BODY });
      const text = await res.text();
      await settled();
      const sc = res.headers.get('set-cookie');
      appendFileSync(process.env.PROBE_OUT as string, JSON.stringify({ case: k, status: res.status, body: text,
        setCookie: sc ? sc.replace(/=[^;]*/g, '=<v>') : null, unhandled: h.unhandled, lines: LINES().map((c) => c[1]) }) + '\n');
    });
  }
});
