import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import express from 'express';

// KS-1868: GET /api/issuer-certs (list) and POST /api/issuer-certs/:id/revoke answer a constant 500 INTERNAL_ERROR
// when the repository call REJECTS, after logging their line. The catch must still do both even if the rejection
// value cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on
// `.message`). Today such a value makes the catch itself throw inside an async Express 4 handler: no response is
// sent (the request hangs) and Node sees an UNHANDLED REJECTION. The cells count unhandled rejections themselves
// and give the client a short timeout, so a hang shows as a failed assertion. Harness: the ks1536 issuer-certs
// route test (real router; the repository, auth middleware and event bus mocked; the caller is an ORG_ADMIN with a
// tenant). The repository stand-ins reject with a plain function, not a vi.fn(): a spy inspects what it rejects
// with and could itself fail on a revoked Proxy before the code under test saw it. On the revoke path the cert is
// found active and the revoke UPDATE is the call that rejects: no cert is revoked and no event is published.
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
vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
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

const getterThrows = () =>
  Object.create(Error.prototype, {
    message: {
      get() {
        throw new Error('getter boom');
      },
    },
  });

describe('KS-1868 the issuer-cert list and revoke catches read the rejection value safely', () => {
  it('control ks1868 C1 list: an ordinary Error still logs its message and the route answers the constant 500', async () => {
    h.toThrow = new Error('db down');
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(LIST_LINES()[0][1]).toEqual({ error: 'db down' });
  });

  it('control ks1868 C2 revoke: an ordinary Error still logs its message, the route answers the constant 500 and no event is published', async () => {
    h.toThrow = new Error('db down');
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.revokeCalls).toBe(1);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(REVOKE_LINES()[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 list: a revoked Proxy rejection logs a constant reason and the route answers the constant 500', async () => {
    const { proxy, revoke: revokeProxy } = Proxy.revocable({}, {});
    revokeProxy();
    h.toThrow = proxy;
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(LIST_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 list: an Error whose message getter throws logs a constant reason and the route answers the constant 500', async () => {
    h.toThrow = getterThrows();
    expect(await list()).toEqual(LIST_500);
    expect(h.unhandled).toBe(0);
    expect(LIST_LINES()).toHaveLength(1);
    expect(LIST_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R3 revoke: a revoked Proxy rejection logs a constant reason, the route answers the constant 500 and no event is published', async () => {
    const { proxy, revoke: revokeProxy } = Proxy.revocable({}, {});
    revokeProxy();
    h.toThrow = proxy;
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.revokeCalls).toBe(1);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(REVOKE_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R4 revoke: an Error whose message getter throws logs a constant reason, the route answers the constant 500 and no event is published', async () => {
    h.toThrow = getterThrows();
    expect(await revoke()).toEqual(REVOKE_500);
    expect(h.unhandled).toBe(0);
    expect(h.revokeCalls).toBe(1);
    expect(h.published).toBe(0);
    expect(REVOKE_LINES()).toHaveLength(1);
    expect(REVOKE_LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
