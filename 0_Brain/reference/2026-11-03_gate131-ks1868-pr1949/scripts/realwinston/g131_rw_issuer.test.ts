import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import express from 'express';

// KS-1868 (QA gate 113, G113-F1 and F2): the GET /api/issuer-certs (list) and POST /api/issuer-certs/:id/revoke catches in
// routes/issuerCerts.ts log `{ error: reason }` where `reason` is `err instanceof Error ? err.message : String(err)`. PR 1931 guards
// the READ; an Error whose message is readable but not a string (a revoked Proxy, an object whose toString throws, a null-prototype
// object, a Symbol) passes it to the logger as is, and the real winston throws while formatting it. The cells reject with an Error
// whose `message` getter RETURNS such a value and assert the logged reason is text (the constant when it cannot be turned into
// text), the constant 500, no unhandled rejection, and no event published (the outcome an ordinary Error gets). Controls pin the
// shapes a non-Error gets today: a thrown plain string is logged as its text and a thrown null-prototype object (String() throws)
// logs the constant. Harness: the ks1868 issuer-cert test (real router; repository, auth middleware and bus mocked).
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  logged: [] as unknown[][],
  unhandled: 0,
  revokeCalls: 0,
  published: 0,
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
vi.mock('../utils/logger', async () => {
  const real: any = await vi.importActual('../utils/logger');
  const c: any = capture;
  const wrap: any = {
    debug: (...a: any[]) => real.logger.debug(...a),
    info: (...a: any[]) => real.logger.info(...a),
    warn: (...a: any[]) => { c.warn(...a); real.logger.warn(...a); },
    error: (...a: any[]) => { c.error(...a); real.logger.error(...a); },
    log: (...a: any[]) => real.logger.log(...a),
  };
  return { logger: wrap, createLogger: () => wrap, validateEnv: () => undefined };
});
vi.mock('@secuura/shared/utils/logger', () => ({ logger: capture, createLogger: () => capture }));
vi.mock('../middleware/authenticate', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = { role: 'ORG_ADMIN', tenantId: 'ten-1868', userId: 'user-1868' };
    next();
  },
}));
vi.mock('../repositories/issuerCertRepo', () => ({
  createIssuerCert: vi.fn(), findIssuerCertByFingerprint: vi.fn(), findActiveIssuerCertForTenant: vi.fn(),
  rotateIssuerCert: vi.fn(), toSummary: (c: unknown) => c,
  listIssuerCerts: () => Promise.reject(h.toThrow),
  getIssuerCertById: async () => ({ id: 'cert-1868', status: 'active' }),
  revokeIssuerCert: () => {
    h.revokeCalls += 1;
    return Promise.reject(h.toThrow);
  },
}));
vi.mock('../events', () => ({
  publishEvent: () => {
    h.published += 1;
    return Promise.resolve(undefined);
  },
  EventTypes: {},
}));
vi.mock('../db', () => ({ query: vi.fn(async () => ({ rows: [] })) }));

const SAVED_LISTENERS = process.listeners('unhandledRejection');
const onUnhandled = () => {
  h.unhandled += 1;
};

let server: Server;
let baseUrl = '';
beforeAll(async () => {
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  const { issuerCertsRoutes } = await import('../routes/issuerCerts');
  const app = express();
  app.use(express.json());
  app.use('/api/issuer-certs', issuerCertsRoutes);
  server = app.listen(0, '127.0.0.1');
  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
});
afterAll(async () => {
  server.closeAllConnections();
  await new Promise<void>((resolve) => server.close(() => resolve()));
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
});
beforeEach(() => {
  h.toThrow = undefined;
  h.logged.length = 0;
  h.unhandled = 0;
  h.revokeCalls = 0;
  h.published = 0;
});

const LIST_LINES = () => h.logged.filter((c) => c[0] === 'Issuer cert list failed');
const REVOKE_LINES = () => h.logged.filter((c) => c[0] === 'Issuer cert revoke failed');

async function call(method: string, path: string): Promise<{ status: number; code: string | undefined; message: string | undefined } | null> {
  try {
    const res = await fetch(baseUrl + path, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: method === 'GET' ? undefined : '{}',
      signal: AbortSignal.timeout(1500),
    });
    const text = await res.text();
    let code: string | undefined;
    let message: string | undefined;
    try {
      const parsed = JSON.parse(text);
      code = parsed?.error?.code;
      message = parsed?.error?.message;
    } catch {
      code = undefined;
      message = undefined;
    }
    return { status: res.status, code, message };
  } catch {
    return null;
  }
}

const list = () => call('GET', '/api/issuer-certs');
const revoke = () => call('POST', '/api/issuer-certs/cert-1868/revoke');
const LIST_500 = { status: 500, code: 'INTERNAL_ERROR', message: 'Failed to list issuer certs' };
const REVOKE_500 = { status: 500, code: 'INTERNAL_ERROR', message: 'Failed to revoke issuer cert' };

const revokedProxy = (): unknown => {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
};
const toStringThrows = (): unknown => ({
  toString() {
    throw new Error('ts boom');
  },
});
/** An Error whose `message` getter succeeds and returns the (non-string) value m. */
const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
const reasonOf = (c: unknown[] | undefined): string => {
  const v = (c?.[1] as { error?: unknown } | undefined)?.error;
  return typeof v === 'string' ? v : '<' + typeof v + '>';
};
const SHAPES: Array<[string, () => unknown, string]> = [
  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
  ['an object whose toString throws', toStringThrows, 'unreadable thrown value'],
  ['a null-prototype object', () => Object.create(null), 'unreadable thrown value'],
  ['a Symbol', () => Symbol('ks1868'), 'Symbol(ks1868)'],
];

describe('KS-1868 the issuer-cert list and revoke catches log text for a hostile non-string message', () => {
  it('control ks1868 C1 list: an ordinary Error is logged with its message and the route answers the constant 500', async () => {
    h.toThrow = new Error('db down');
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(reasonOf(LIST_LINES()[0])).toBe('db down');
  });

  it('control ks1868 C2 revoke: an ordinary Error is logged with its message, the route answers the constant 500 and no event is published', async () => {
    h.toThrow = new Error('db down');
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(reasonOf(REVOKE_LINES()[0])).toBe('db down');
  });

  it('control ks1868 C3 list: a thrown null-prototype object cannot be turned into text and the constant reason is logged', async () => {
    h.toThrow = Object.create(null);
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(reasonOf(LIST_LINES()[0])).toBe('unreadable thrown value');
  });

  it('control ks1868 C4 revoke: a thrown plain string is logged as its own text', async () => {
    h.toThrow = 'plain boom';
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(reasonOf(REVOKE_LINES()[0])).toBe('plain boom');
  });

  it('RED ks1868 R1 list: a rejection whose message is a revoked Proxy logs the constant reason and the route answers the constant 500', async () => {
    h.toThrow = withMessage(SHAPES[0][1]());
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(reasonOf(LIST_LINES()[0])).toBe(SHAPES[0][2]);
  });

  it('RED ks1868 R2 list: a rejection whose message is an object whose toString throws logs the constant reason and the route answers the constant 500', async () => {
    h.toThrow = withMessage(SHAPES[1][1]());
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(reasonOf(LIST_LINES()[0])).toBe(SHAPES[1][2]);
  });

  it('RED ks1868 R3 list: a rejection whose message is a null-prototype object logs the constant reason and the route answers the constant 500', async () => {
    h.toThrow = withMessage(SHAPES[2][1]());
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(reasonOf(LIST_LINES()[0])).toBe(SHAPES[2][2]);
  });

  it('RED ks1868 R4 list: a rejection whose message is a Symbol logs the Symbol text and the route answers the constant 500', async () => {
    h.toThrow = withMessage(SHAPES[3][1]());
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(reasonOf(LIST_LINES()[0])).toBe(SHAPES[3][2]);
  });

  it('RED ks1868 R5 revoke: a rejection whose message is a revoked Proxy logs the constant reason and the route answers the constant 500 with no event', async () => {
    h.toThrow = withMessage(SHAPES[0][1]());
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(reasonOf(REVOKE_LINES()[0])).toBe(SHAPES[0][2]);
  });

  it('RED ks1868 R6 revoke: a rejection whose message is an object whose toString throws logs the constant reason and the route answers the constant 500 with no event', async () => {
    h.toThrow = withMessage(SHAPES[1][1]());
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(reasonOf(REVOKE_LINES()[0])).toBe(SHAPES[1][2]);
  });

  it('RED ks1868 R7 revoke: a rejection whose message is a null-prototype object logs the constant reason and the route answers the constant 500 with no event', async () => {
    h.toThrow = withMessage(SHAPES[2][1]());
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(reasonOf(REVOKE_LINES()[0])).toBe(SHAPES[2][2]);
  });

  it('RED ks1868 R8 revoke: a rejection whose message is a Symbol logs the Symbol text and the route answers the constant 500 with no event', async () => {
    h.toThrow = withMessage(SHAPES[3][1]());
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(reasonOf(REVOKE_LINES()[0])).toBe(SHAPES[3][2]);
  });
});
