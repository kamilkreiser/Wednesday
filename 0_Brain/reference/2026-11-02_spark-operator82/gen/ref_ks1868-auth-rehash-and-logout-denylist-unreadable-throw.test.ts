import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import express from 'express';

// KS-1868: two non-fatal catch handlers in routes/auth.ts read the rejection value unguarded: (1) POST /login, the
// UPGRADE-ON-VERIFY rehash catch (`logger.warn(..., { userId, error: err?.message })`), and (2) POST /logout, the
// `.catch` on the refresh-JTI denylist write (`logger.warn('Logout denylist failed (non-fatal)', { error: err?.message })`).
// Both are meant to log and carry on: the login still answers 200 with tokens, the logout still clears the cookie and
// answers 200. When the rejection value cannot be read (a revoked Proxy throws on property reads; an Error whose
// `message` getter throws, throws on `.message`) the handler itself throws: the login ends in the error handler as a
// 500 with NO tokens, the logout ends as a 500 with the cookie NOT cleared (its session was already revoked). The cells
// assert the outcome an ordinary Error already gets. Harness: the ks1868 login publish-event test (real router and
// error handler; repository, password, session, jwt, lockout, mail and event bus mocked). The stand-ins reject with a
// plain function, not a vi.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy before
// the code under test saw it.
const h = vi.hoisted(() => ({
  rehashRejects: false,
  denylistRejects: false,
  toThrow: undefined as unknown,
  logged: [] as unknown[][],
  unhandled: 0,
}));

const capture = vi.hoisted(() => ({
  debug: () => undefined,
  info: () => undefined,
  warn: (...args: unknown[]) => {
    h.logged.push(args);
  },
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
  updateUser: (_id: string, patch: Record<string, unknown>) =>
    patch && 'passwordHash' in patch && h.rehashRejects ? Promise.reject(h.toThrow) : Promise.resolve({ ...ACTIVE_USER }),
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
  shouldRehashAfterVerify: vi.fn(() => true),
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
  decodeToken: vi.fn(() => ({ jti: 'jti-1868', exp: Math.floor(Date.now() / 1000) + 3600 })),
}));

vi.mock('../services/refreshDenylist', () => ({
  isRefreshJtiDenylisted: vi.fn(async () => false),
  denylistRefreshJti: (_jti: string, _ttl: number) => (h.denylistRejects ? Promise.reject(h.toThrow) : Promise.resolve(undefined)),
}));
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
  publishEvent: () => Promise.resolve(undefined),
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
  app.use((req, _res, next) => {
    (req as unknown as { cookies: Record<string, string> }).cookies = { refresh_token: 'RT_1868' };
    next();
  });
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
  h.rehashRejects = false;
  h.denylistRejects = false;
  h.toThrow = undefined;
  h.logged = [];
  h.unhandled = 0;
});

const REHASH_LINES = () => h.logged.filter((c) => c[0] === 'UPGRADE-ON-VERIFY rehash failed (non-fatal)');
const LOGOUT_LINES = () => h.logged.filter((c) => c[0] === 'Logout denylist failed (non-fatal)');

async function login(): Promise<{ status: number; minted: boolean } | null> {
  try {
    const res = await fetch(baseUrl + '/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: LOGIN_EMAIL, password: 'pw-correct-horse' }),
      signal: AbortSignal.timeout(2000),
    });
    const text = await res.text();
    return { status: res.status, minted: text.includes('MINTED_1868_LOGIN') };
  } catch {
    return null;
  }
}

async function logout(): Promise<{ status: number; clearedCookie: boolean; ok: boolean } | null> {
  try {
    const res = await fetch(baseUrl + '/api/auth/logout', { method: 'POST', signal: AbortSignal.timeout(2000) });
    const text = await res.text();
    return {
      status: res.status,
      clearedCookie: (res.headers.get('set-cookie') || '').includes('refresh_token=;'),
      ok: text.includes('Logged out successfully'),
    };
  } catch {
    return null;
  }
}

const LOGIN_OK = { status: 200, minted: true };
const LOGOUT_OK = { status: 200, clearedCookie: true, ok: true };
const getterThrows = () =>
  Object.create(Error.prototype, {
    message: {
      get() {
        throw new Error('getter boom');
      },
    },
  });

describe('KS-1868 the login rehash catch and the logout denylist catch read the rejection value safely', () => {
  it('control ks1868 C1 login: an ordinary Error from the rehash write is logged with its message and the login still answers 200 with tokens', async () => {
    h.rehashRejects = true;
    h.toThrow = new Error('db down');
    expect(await login()).toEqual(LOGIN_OK);
    expect(REHASH_LINES()).toHaveLength(1);
    expect(REHASH_LINES()[0][1]).toEqual({ userId: 'user-1868-login', error: 'db down' });
  });

  it('control ks1868 C2 logout: an ordinary Error from the denylist write is logged with its message and the logout still answers 200 and clears the cookie', async () => {
    h.denylistRejects = true;
    h.toThrow = new Error('redis down');
    expect(await logout()).toEqual(LOGOUT_OK);
    expect(LOGOUT_LINES()).toHaveLength(1);
    expect(LOGOUT_LINES()[0][1]).toEqual({ error: 'redis down' });
  });

  it('RED ks1868 R1 login: a revoked Proxy rejection logs a constant reason and the login still answers 200 with tokens', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.rehashRejects = true;
    h.toThrow = proxy;
    expect(await login()).toEqual(LOGIN_OK);
    expect(REHASH_LINES()).toHaveLength(1);
    expect(REHASH_LINES()[0][1]).toEqual({ userId: 'user-1868-login', error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 login: an Error whose message getter throws logs a constant reason and the login still answers 200 with tokens', async () => {
    h.rehashRejects = true;
    h.toThrow = getterThrows();
    expect(await login()).toEqual(LOGIN_OK);
    expect(REHASH_LINES()).toHaveLength(1);
    expect(REHASH_LINES()[0][1]).toEqual({ userId: 'user-1868-login', error: 'unreadable thrown value' });
  });

  it('RED ks1868 R3 logout: a revoked Proxy rejection logs a constant reason and the logout still answers 200 and clears the cookie', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.denylistRejects = true;
    h.toThrow = proxy;
    expect(await logout()).toEqual(LOGOUT_OK);
    expect(LOGOUT_LINES()).toHaveLength(1);
    expect(LOGOUT_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R4 logout: an Error whose message getter throws logs a constant reason and the logout still answers 200 and clears the cookie', async () => {
    h.denylistRejects = true;
    h.toThrow = getterThrows();
    expect(await logout()).toEqual(LOGOUT_OK);
    expect(LOGOUT_LINES()).toHaveLength(1);
    expect(LOGOUT_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
