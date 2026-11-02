// KS-1868 (QA gate 114, G114-F1): three read-side catches of the anchoring service log `error: <reason>` where `reason` is whatever
// `err?.message` returned. PR 1932 guards the READ; a message that is readable but not a string (a revoked Proxy, an object whose
// toString throws, a null-prototype object, a Symbol) is passed to `log()` as is, and its `JSON.stringify` throws on a revoked
// Proxy inside the catch (the tx route then never answers). Cells: GET /api/anchors/tx/:txHash (`dbGetAnchorByTx` logs and returns
// undefined, 404), GET /api/anchors/verify/:hash (the local lookup logs and falls to the chain step; with no Cardano credentials
// 404) and POST /api/anchors/verify (the content-hash lookup logs, verified false). The cells reject with an Error whose `message`
// getter RETURNS such a value and assert the logged reason is text (the constant when it cannot be turned into text) and the
// answer an ordinary Error gets. Controls pin a thrown plain string (no message: logged with no `error` key, not the text
// undefined). Harness: the ks1868 anchoring read-route test (real index.ts app, real RS256 bearer, `../db` mocked, plain-function
// rejections). Every statement the cells reject is a SELECT: nothing is submitted, signed or written.
import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import crypto from 'crypto';
import http from 'http';
import type { AddressInfo } from 'net';
import express from 'express';

const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  rejectPattern: null as RegExp | null,
  writes: 0,
  unhandled: 0,
}));

vi.mock('../db', async (importOriginal) => {
  const real = await importOriginal<typeof import('../db')>();
  return {
    ...real,
    isDbAvailable: () => true,
    query: async (sql: string) => {
      if (sql.includes('to_regclass')) return { rows: [{ s: 'anchor_store', b: 'anchor_batches' }], rowCount: 1 };
      if (/^\s*(INSERT|UPDATE|DELETE|CREATE|ALTER)/i.test(sql)) h.writes += 1;
      if (h.rejectPattern && h.rejectPattern.test(sql)) return Promise.reject(h.toThrow);
      return { rows: [], rowCount: 0 };
    },
    transaction: async () => {
      throw new Error('KS-1868 test: no transaction expected');
    },
  };
});

const TENANT_A = 'a1868000-0000-4000-8000-00000000000a';
const ORG_A = 'c1868000-0000-4000-8000-0000000000ca';
const TX = 'ab'.repeat(32);
const HASH = 'cd'.repeat(32);
const LOOKUP_DOWN = 'lookup down';
const UNREADABLE = 'unreadable thrown value';

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64url = (b: Buffer): string => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function bearer(): string {
  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const claims = { userId: '2a186800-0000-4000-8000-0000000018a2', role: 'user', organizationId: ORG_A, tenantId: TENANT_A };
  const payload = b64url(Buffer.from(JSON.stringify({ iat: now, exp: now + 600, ...claims })));
  return `${header}.${payload}.${b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM))}`;
}

const SAVED_LISTENERS = process.listeners('unhandledRejection');
const onUnhandled = () => {
  h.unhandled += 1;
};

let server: http.Server;
let base = '';
const logLines: string[] = [];

type Wire = { status: number; body: string } | null;
async function send(method: 'GET' | 'POST', path: string, body?: unknown): Promise<Wire> {
  try {
    const res = await fetch(`${base}${path}`, {
      method,
      headers: { Authorization: `Bearer ${bearer()}`, 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: AbortSignal.timeout(1500),
    });
    return { status: res.status, body: await res.text() };
  } catch {
    return null;
  }
}
/** index.ts `log()` writes one JSON object per console.log line; those whose `message` is `message`. */
function lines(message: string): Array<Record<string, unknown>> {
  return logLines
    .filter((l) => l.startsWith('{') && l.includes(message))
    .map((l) => JSON.parse(l) as Record<string, unknown>)
    .filter((o) => o.message === message);
}

beforeAll(async () => {
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL;
  delete process.env.AUTH_SERVICE_URL;
  delete process.env.PLATFORM_WALLET_MNEMONIC;
  delete process.env.BLOCKFROST_API_KEY;
  delete process.env.DATABASE_URL;
  process.env.CARDANO_NETWORK = 'preview';
  vi.spyOn(console, 'log').mockImplementation((...args: unknown[]) => {
    logLines.push(args.map(String).join(' '));
  });
  vi.spyOn(express.application, 'listen').mockReturnValue(
    { keepAliveTimeout: 0, headersTimeout: 0, close: () => undefined } as unknown as http.Server,
  );
  const app = (await import('../index')).default;
  server = http.createServer(app);
  await new Promise<void>((resolve) => { server.listen(0, '127.0.0.1', resolve); });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}, 60000);

afterAll(async () => {
  (server as any)?.closeAllConnections?.();
  await new Promise<void>((resolve) => (server ? server.close(() => resolve()) : resolve()));
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
  vi.restoreAllMocks();
});

beforeEach(() => {
  h.toThrow = undefined;
  h.rejectPattern = null;
  h.writes = 0;
  h.unhandled = 0;
  logLines.length = 0;
});

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
/** The logged `error` key of a JSON log line as a string; the type name when it is not one. */
const reasonOf = (o: Record<string, unknown> | undefined): string => (typeof o?.error === 'string' ? o.error : '<' + typeof o?.error + '>');
const SHAPES: Array<[string, () => unknown, string]> = [
  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
  ['an object whose toString throws', toStringThrows, 'unreadable thrown value'],
  ['a null-prototype object', () => Object.create(null), 'unreadable thrown value'],
  ['a Symbol', () => Symbol('ks1868'), 'Symbol(ks1868)'],
];
const TX_MSG = 'DB lookup anchor by tx failed';
const HASH_MSG = 'verify-by-hash: local DB lookup failed';
const VERIFY_MSG = 'DB lookup anchor by content hash failed';

const byTx = () => {
  h.rejectPattern = /WHERE transaction_hash = \$1/;
  return send('GET', `/api/anchors/tx/${TX}`);
};
const byHash = () => {
  h.rejectPattern = /LOWER\(content_hash\) = \$1/;
  return send('GET', `/api/anchors/verify/${HASH}`);
};
const verify = () => {
  h.rejectPattern = /content_hash = \$1 AND status = 'confirmed'/;
  return send('POST', '/api/anchors/verify', { contentHash: HASH });
};

const TX_ANSWER = { success: false, error: { code: 'NOT_FOUND', message: 'Anchor not found for transaction' } };
const HASH_ANSWER = { verified: false, hash: HASH, reason: 'Not found in local DB and Blockfrost not configured.' };
const VERIFY_ANSWER = { success: true, data: { verified: false, reason: 'No confirmed anchor found for this hash', contentHash: HASH } };

function expectAnswer(w: Wire, status: number, answer: unknown): void {
  expect(w).not.toBeNull();
  expect(w?.status, `received body: ${w?.body}`).toBe(status);
  expect(JSON.parse(w?.body ?? 'null')).toEqual(answer);
}


async function tx(thrown: unknown, reason: string): Promise<void> {
  h.toThrow = thrown;
  expectAnswer(await byTx(), 404, TX_ANSWER);
  expect(h.unhandled).toBe(0);
  expect(lines(TX_MSG)).toHaveLength(1);
  expect(reasonOf(lines(TX_MSG)[0])).toBe(reason);
  expect(h.writes).toBe(0);
}
async function hash(thrown: unknown, reason: string): Promise<void> {
  h.toThrow = thrown;
  expectAnswer(await byHash(), 404, HASH_ANSWER);
  expect(h.unhandled).toBe(0);
  expect(lines(HASH_MSG)).toHaveLength(1);
  expect(reasonOf(lines(HASH_MSG)[0])).toBe(reason);
  expect(h.writes).toBe(0);
}
async function verifyHash(thrown: unknown, reason: string): Promise<void> {
  h.toThrow = thrown;
  expectAnswer(await verify(), 200, VERIFY_ANSWER);
  expect(h.unhandled).toBe(0);
  expect(lines(VERIFY_MSG)).toHaveLength(1);
  expect(reasonOf(lines(VERIFY_MSG)[0])).toBe(reason);
  expect(h.writes).toBe(0);
}

describe('KS-1868 the anchoring read-route catches log text for a hostile non-string message', () => {
  it('control ks1868 C1 tx lookup: an ordinary Error is logged with its own message and the route answers 404', async () => {
    await tx(new Error(LOOKUP_DOWN), LOOKUP_DOWN);
  });

  it('control ks1868 C2 verify-by-hash: an ordinary Error is logged with its own message and the chain step answers 404', async () => {
    await hash(new Error(LOOKUP_DOWN), LOOKUP_DOWN);
  });

  it('control ks1868 C3 content-hash verify: an ordinary Error is logged with its own message and the route answers verified false', async () => {
    await verifyHash(new Error(LOOKUP_DOWN), LOOKUP_DOWN);
  });

  it('control ks1868 C4 tx lookup: a thrown plain string has no message and is logged with no error key (not the text undefined)', async () => {
    await tx('plain boom', '<undefined>');
  });

  it('control ks1868 C5 verify-by-hash: a thrown plain string has no message and is logged with no error key (not the text undefined)', async () => {
    await hash('plain boom', '<undefined>');
  });

  it('RED ks1868 R1 tx lookup: a rejection whose message is a revoked Proxy logs the constant reason and the answer is the ordinary one', async () => {
    await tx(withMessage(SHAPES[0][1]()), SHAPES[0][2]);
  });

  it('RED ks1868 R2 tx lookup: a rejection whose message is an object whose toString throws logs the constant reason and the answer is the ordinary one', async () => {
    await tx(withMessage(SHAPES[1][1]()), SHAPES[1][2]);
  });

  it('RED ks1868 R3 tx lookup: a rejection whose message is a null-prototype object logs the constant reason and the answer is the ordinary one', async () => {
    await tx(withMessage(SHAPES[2][1]()), SHAPES[2][2]);
  });

  it('RED ks1868 R4 tx lookup: a rejection whose message is a Symbol logs the Symbol text and the answer is the ordinary one', async () => {
    await tx(withMessage(SHAPES[3][1]()), SHAPES[3][2]);
  });

  it('RED ks1868 R5 verify-by-hash: a rejection whose message is a revoked Proxy logs the constant reason and the answer is the ordinary one', async () => {
    await hash(withMessage(SHAPES[0][1]()), SHAPES[0][2]);
  });

  it('RED ks1868 R6 verify-by-hash: a rejection whose message is an object whose toString throws logs the constant reason and the answer is the ordinary one', async () => {
    await hash(withMessage(SHAPES[1][1]()), SHAPES[1][2]);
  });

  it('RED ks1868 R7 verify-by-hash: a rejection whose message is a null-prototype object logs the constant reason and the answer is the ordinary one', async () => {
    await hash(withMessage(SHAPES[2][1]()), SHAPES[2][2]);
  });

  it('RED ks1868 R8 verify-by-hash: a rejection whose message is a Symbol logs the Symbol text and the answer is the ordinary one', async () => {
    await hash(withMessage(SHAPES[3][1]()), SHAPES[3][2]);
  });

  it('RED ks1868 R9 content-hash verify: a rejection whose message is a revoked Proxy logs the constant reason and the answer is the ordinary one', async () => {
    await verifyHash(withMessage(SHAPES[0][1]()), SHAPES[0][2]);
  });

  it('RED ks1868 R10 content-hash verify: a rejection whose message is an object whose toString throws logs the constant reason and the answer is the ordinary one', async () => {
    await verifyHash(withMessage(SHAPES[1][1]()), SHAPES[1][2]);
  });

  it('RED ks1868 R11 content-hash verify: a rejection whose message is a null-prototype object logs the constant reason and the answer is the ordinary one', async () => {
    await verifyHash(withMessage(SHAPES[2][1]()), SHAPES[2][2]);
  });

  it('RED ks1868 R12 content-hash verify: a rejection whose message is a Symbol logs the Symbol text and the answer is the ordinary one', async () => {
    await verifyHash(withMessage(SHAPES[3][1]()), SHAPES[3][2]);
  });
});

describe('G137 witness', () => {
  it('W1 the unhandledRejection counter sees a deliberate unhandled rejection', async () => {
    h.unhandled = 0;
    void Promise.reject(new Error('g137 witness rejection'));
    await new Promise((r) => setTimeout(r, 100));
    expect(h.unhandled).toBe(1);
  });
});
