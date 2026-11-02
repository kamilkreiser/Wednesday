import { describe, it, expect, vi, beforeAll, afterAll, beforeEach, afterEach } from 'vitest';
import crypto from 'crypto';
import type { Server } from 'http';
import type { AddressInfo } from 'net';

process.env.SECURITY_DISABLE_BOOT = '1';

// KS-1868: the catch of the admin-scopes write route (PUT /api/keys/admin-scopes/:userId) must still answer when
// the scope transaction rejects with a value that cannot be read (a revoked Proxy throws on `instanceof` and on
// any property read; an Error whose `message` getter throws, throws on `.message`). Today the catch itself throws
// in an async handler, so no answer is sent. After the fix such a value is handed to the error handler as an
// ordinary Error, which is exactly what an ordinary non-infrastructure Error gets (500 INTERNAL_ERROR).
// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could
// itself fail on a revoked Proxy before the code under test saw it. The route runs on a real loopback listener
// with a real RS256 token, as in ks888. The service logs through console.log (JSON lines).
const ctl = vi.hoisted(() => ({
  boom: undefined as unknown,
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  initDb: async () => true,
  query: async (statement: string) => {
    if (/^\s*SELECT\s+1\s+FROM\s+users/i.test(String(statement))) return { rows: [{ one: 1 }], rowCount: 1 };
    return { rows: [], rowCount: 0 };
  },
  transaction: async (run: (client: unknown) => Promise<unknown>) =>
    run({
      query: (statement: string) => {
        if (/^\s*DELETE\s+FROM\s+admin_organisation_scopes/i.test(String(statement)) && ctl.boom !== undefined) return Promise.reject(ctl.boom);
        return Promise.resolve({ rows: [], rowCount: 0 });
      },
    }),
}));

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const SIGNING_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const VERIFY_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();

const USER_ID = '18680000-0000-4000-8000-000000000056';
const TENANT_ID = 'c0000000-0000-4000-8000-000000001868';
const captured: string[] = [];
const infraLines = () => captured.filter((s) => s.includes('Admin organisation scope write failed on infrastructure'));

let listener: Server;
let root = '';

function platformToken(): string {
  const now = Math.floor(Date.now() / 1000);
  const head = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64url');
  const claims = Buffer.from(JSON.stringify({ sub: 'ks1868-test', iat: now, exp: now + 300, role: 'super_admin' })).toString('base64url');
  const sig = crypto.sign('RSA-SHA256', Buffer.from(head + '.' + claims), SIGNING_PEM).toString('base64url');
  return head + '.' + claims + '.' + sig;
}

async function putScopes(payload: unknown = { tenantId: TENANT_ID, organizationIds: [] }): Promise<{ status: number; text: string; body: any }> {
  try {
    const res = await fetch(root + '/api/keys/admin-scopes/' + USER_ID, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + platformToken() },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(3000),
    });
    const text = await res.text();
    let body: any;
    try {
      body = JSON.parse(text);
    } catch {
      body = undefined;
    }
    return { status: res.status, text, body };
  } catch {
    return { status: 0, text: '', body: undefined };
  }
}

const summary = (r: { status: number; body: any }) => ({ status: r.status, code: r.body?.error?.code });

beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(VERIFY_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL;
  delete process.env.AUTH_SERVICE_URL;
  const app = (await import('../index')).default;
  await new Promise<void>((resolve) => {
    listener = app.listen(0, '127.0.0.1', resolve);
  });
  root = 'http://127.0.0.1:' + (listener.address() as AddressInfo).port;
});

afterAll(async () => {
  await new Promise<void>((resolve) => listener.close(() => resolve()));
});

beforeEach(() => {
  ctl.boom = undefined;
  captured.length = 0;
  vi.spyOn(console, 'log').mockImplementation((...args: unknown[]) => {
    captured.push(String(args[0]));
  });
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('KS-1868 the catch of the admin-scopes write route reads the thrown value safely', () => {
  it('control ks1868 C1 an ordinary Error from the transaction answers 500 INTERNAL_ERROR', async () => {
    ctl.boom = new Error('db down');
    const r = await putScopes();
    expect(summary(r)).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
    expect(infraLines()).toHaveLength(0);
  });

  it('control ks1868 C2 a write whose transaction lands answers 200', async () => {
    const r = await putScopes();
    expect({ status: r.status, success: r.body?.success }).toEqual({ status: 200, success: true });
    expect(infraLines()).toHaveLength(0);
  });

  it('control ks1868 C3 an infrastructure Error still answers 503 and logs the infrastructure line', async () => {
    ctl.boom = Object.assign(new Error('connect failed'), { code: 'ECONNREFUSED' });
    const r = await putScopes();
    expect(summary(r)).toEqual({ status: 503, code: 'SERVICE_UNAVAILABLE' });
    expect(infraLines()).toHaveLength(1);
  });

  // Gate 94 G94-F2. The catch now decides whether the thrown value is a ZodError before it decides anything else, and no
  // other cell pinned the route's own 400 for a body the schema refuses: with the Zod probe or the Zod branch removed
  // this cell goes red and the other five stay green.
  it('control ks1868 C4 a body the schema refuses (a ZodError) still answers 400 BAD_REQUEST with the validation body', async () => {
    const r = await putScopes({ tenantId: 'not-a-uuid', organizationIds: [] });
    expect(summary(r)).toEqual({ status: 400, code: 'BAD_REQUEST' });
    expect(r.body?.success).toBe(false);
    expect(r.body?.error?.message).toBe('Validation failed');
    expect(r.body?.error?.details).toEqual(expect.arrayContaining([expect.objectContaining({ path: ['tenantId'] })]));
    expect(infraLines()).toHaveLength(0);
  });

  it('RED ks1868 R1 a revoked Proxy from the transaction answers 500 INTERNAL_ERROR', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    ctl.boom = proxy;
    const r = await putScopes();
    expect(summary(r)).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
    expect(infraLines()).toHaveLength(0);
  });

  it('RED ks1868 R2 an Error whose message getter throws answers 500 INTERNAL_ERROR', async () => {
    ctl.boom = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    const r = await putScopes();
    expect(summary(r)).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
    expect(infraLines()).toHaveLength(0);
  });
});
