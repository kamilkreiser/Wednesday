// GATE 137 probe (adapted from gate 114) (anchoring). The REAL index.ts app (real routes, real shared errorHandler, real log()), served on
// loopback with a real RS256 bearer (as the ks1822/ks1868 harness). Replaced: ../db (stateful anchor_store stand-in,
// writes counted), ../cardano (readiness/wallet switchable; submitAnchor a counting witness) and
// ../cardano/provider getProvider (a chain stand-in; no Blockfrost). Env: G137_OUT, G137_STAGE.
/* eslint-disable */
import { test, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import http from 'http';
import net from 'net';
import fs from 'fs';
import express from 'express';

const h = vi.hoisted(() => ({
  rows: [] as any[], reject: null as RegExp | null, value: undefined as unknown,
  writes: [] as string[], submits: 0, providerCalls: [] as string[],
  cardano: false, chainHash: '' as string, getterReads: 0,
}));
vi.mock('../db', async (orig) => {
  const real: any = await orig();
  return {
    ...real,
    isDbAvailable: () => true,
    query: async (sql: string, params: any[] = []) => {
      if (sql.includes('to_regclass')) return { rows: [{ s: 'anchor_store', b: 'anchor_batches' }], rowCount: 1 };
      if (/^\s*(INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|TRUNCATE)/i.test(sql)) h.writes.push(sql.trim().slice(0, 60));
      if (h.reject && h.reject.test(sql)) return Promise.reject(h.value);
      let rows: any[] = [];
      if (/WHERE transaction_hash = \$1/.test(sql)) rows = h.rows.filter((r) => r.transaction_hash === params[0]);
      else if (/LOWER\(content_hash\) = \$1/.test(sql)) rows = h.rows.filter((r) => r.content_hash.toLowerCase() === params[0] && ['submitting','submitted','confirmed'].includes(r.status));
      else if (/content_hash = \$1 AND status = 'confirmed'/.test(sql)) rows = h.rows.filter((r) => r.content_hash === params[0] && r.status === 'confirmed');
      return { rows, rowCount: rows.length };
    },
    transaction: async () => { h.writes.push('TRANSACTION'); throw new Error('g137: no transaction expected'); },
  };
});
vi.mock('../cardano', async (orig) => {
  const real: any = await orig();
  return {
    ...real,
    isCardanoReady: () => h.cardano,
    getWalletAddress: () => (h.cardano ? 'addr_test1g137wallet' : null),
    submitAnchor: async () => { h.submits += 1; throw new Error('g137: no submit expected'); },
    submitAndConfirmAnchor: async () => { h.submits += 1; throw new Error('g137: no submit expected'); },
  };
});
vi.mock('../cardano/provider', async (orig) => {
  const real: any = await orig();
  const bf = {
    addressesTransactions: async (addr: string) => { h.providerCalls.push(`addressesTransactions ${addr}`); return [{ tx_hash: '11'.repeat(32) }, { tx_hash: '22'.repeat(32) }]; },
    txsMetadata: async (tx: string) => { h.providerCalls.push(`txsMetadata ${tx.slice(0, 4)}`); return tx === '11'.repeat(32) ? [{ label: '674', json_metadata: { secuura: { hash: h.chainHash, documentId: 'chain-doc' } } }] : []; },
    txs: async (tx: string) => { h.providerCalls.push(`txs ${tx.slice(0, 4)}`); return { block_height: 77, block_time: 1700000000 }; },
  };
  return {
    ...real,
    getProvider: () => (h.cardano ? bf : null),
    submitTransaction: async () => { h.submits += 1; throw new Error('g137: no submitTransaction expected'); },
  };
});

const OUT = process.env.G137_OUT as string;
const STAGE = process.env.G137_STAGE || '?';
const connects: string[] = []; const outbound: string[] = [];
const origConnect = net.Socket.prototype.connect;
(net.Socket.prototype as any).connect = function (...args: any[]) {
  const o = args[0];
  const host = typeof o === 'object' && o ? (o.host ?? o.path ?? 'localhost') : (typeof args[1] === 'string' ? args[1] : 'localhost');
  const port = typeof o === 'object' && o ? o.port : o;
  connects.push(`${host}:${port}`);
  if (!/^(127\.0\.0\.1|localhost|::1|\/)/.test(String(host))) outbound.push(`${host}:${port}`);
  return (origConnect as any).apply(this, args);
};
const origFetch = globalThis.fetch;
const fetchUrls: string[] = [];
globalThis.fetch = (async (u: any, init?: any) => { const s = String(u?.url ?? u); fetchUrls.push(s.replace(/\/\/127\.0\.0\.1:\d+/, '//127.0.0.1:PORT').slice(0, 80)); if (!/^http:\/\/127\.0\.0\.1:/.test(s)) outbound.push(`fetch ${s}`); return origFetch(u, init); }) as any;

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIV = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUB = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64 = (b: Buffer) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function bearer() {
  const hd = b64(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const pl = b64(Buffer.from(JSON.stringify({ iat: now, exp: now + 600, userId: '2a186800-0000-4000-8000-0000000018a2', role: 'user', organizationId: 'c1868000-0000-4000-8000-0000000000ca', tenantId: 'a1868000-0000-4000-8000-00000000000a' })));
  return `${hd}.${pl}.${b64(crypto.sign('RSA-SHA256', Buffer.from(`${hd}.${pl}`), PRIV))}`;
}
let server: http.Server; let base = ''; let unhandled = 0; let uncaught = 0;
const logLines: string[] = [];
const SAVED = process.listeners('unhandledRejection');
const onUnh = () => { unhandled += 1; };
const onUnc = () => { uncaught += 1; };

beforeAll(async () => {
  process.removeAllListeners('unhandledRejection'); process.on('unhandledRejection', onUnh);
  process.on('uncaughtException', onUnc);
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUB, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL; delete process.env.PLATFORM_WALLET_MNEMONIC;
  delete process.env.BLOCKFROST_API_KEY; delete process.env.DATABASE_URL;
  process.env.CARDANO_NETWORK = 'preview';
  vi.spyOn(console, 'log').mockImplementation((...a: unknown[]) => { logLines.push(a.map(String).join(' ')); });
  vi.spyOn(console, 'error').mockImplementation((...a: unknown[]) => { logLines.push('[console.error] ' + a.map((x) => { try { return String(x); } catch { return '<unprintable>'; } }).join(' ')); });
  vi.spyOn(express.application, 'listen').mockReturnValue({ keepAliveTimeout: 0, headersTimeout: 0, close: () => undefined } as any);
  const app = (await import('../index')).default;
  server = http.createServer(app);
  await new Promise<void>((r) => server.listen(0, '127.0.0.1', r));
  base = `http://127.0.0.1:${(server.address() as any).port}`;
}, 60000);
afterAll(async () => {
  (server as any)?.closeAllConnections?.(); await new Promise<void>((r) => server.close(() => r()));
  process.removeListener('unhandledRejection', onUnh); process.removeListener('uncaughtException', onUnc);
  for (const l of SAVED) process.on('unhandledRejection', l as any);
  globalThis.fetch = origFetch;
});

const revokedProxy = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const errWithMsg = (get: () => unknown) => Object.create(Error.prototype, { message: { get } });
const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('lookup down at 10.0.0.7 password=hunter2'),
  revokedProxy,
  getterThrows: () => errWithMsg(() => { throw new Error('getter boom'); }),
  nullProto: () => Object.create(null),
  symbol: () => Symbol('sym-thrown'),
  plainString: () => 'plain string thrown',
  msgRevokedProxy: () => errWithMsg(() => revokedProxy()),
  msgBigInt: () => errWithMsg(() => BigInt(7)),
  msgSymbol: () => errWithMsg(() => Symbol('m')),
  msgToStringThrows: () => errWithMsg(() => ({ secretField: 's3cr3t', toString() { throw new Error('ts boom'); } })),
  msgNullProto: () => errWithMsg(() => Object.create(null)),
  // gate 137 additions
  msgUndefined: () => { const e: any = new Error('x'); e.message = undefined; return e; },
  msgNull: () => { const e: any = new Error('x'); e.message = null; return e; },
  msgNumber: () => errWithMsg(() => 42),
  msgPlainObject: () => errWithMsg(() => ({ secretField: 's3cr3t' })),
  msgCustomToString: () => errWithMsg(() => ({ secretField: 's3cr3t', toString() { return 'custom text'; } })),
  msgNonIdempotent: () => { let n = 0; return errWithMsg(() => { n += 1; h.getterReads += 1; return n === 1 ? 'first read text' : revokedProxy(); }); },
  plainObjectNoMsg: () => ({ code: 'E1' }),
  emptyMsgError: () => new Error(),
};
let n = 0;
const uniqHash = () => crypto.createHash('sha256').update(`g137-${STAGE}-${n++}`).digest('hex');
const TX_SEEDED = 'ab'.repeat(32);

function reset(seedHash: string) {
  h.rows = [{ id: 'anc-1', document_id: 'doc-1', content_hash: seedHash, transaction_hash: TX_SEEDED, status: 'confirmed', anchor_type: 'single', block_number: 5, block_hash: null, confirmed_at: new Date(0), created_at: new Date(0), metadata_payload: { secuura: { hash: seedHash } }, network: 'preview', tenant_id: 'a1868000-0000-4000-8000-00000000000a', organization_id: 'c1868000-0000-4000-8000-0000000000ca' }];
  h.reject = null; h.value = undefined; h.writes = []; h.submits = 0; h.providerCalls = []; h.cardano = false; h.chainHash = ''; h.getterReads = 0;
  unhandled = 0; uncaught = 0; logLines.length = 0;
}
async function send(method: string, path: string, body?: unknown, anon = false) {
  try {
    const hdr: any = anon ? { 'Content-Type': 'application/json' } : { Authorization: `Bearer ${bearer()}`, 'Content-Type': 'application/json' };
    const r = await fetch(`${base}${path}`, { method, headers: hdr, body: body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(1500) });
    return { status: r.status, body: await r.text() };
  } catch (e: any) { return { status: 'NO_RESPONSE', err: String(e?.name) }; }
}
const settle = () => new Promise((r) => setTimeout(r, 60));
function rec(o: any) { fs.appendFileSync(OUT, JSON.stringify({ stage: STAGE, ...o }) + '\n'); }
const snap = () => ({ getterReads: h.getterReads, writes: h.writes.slice(), submits: h.submits, providerCalls: h.providerCalls.slice(), unhandled, uncaught, logs: logLines.filter((l) => /lookup|verify-by-hash|Request error|Unhandled|console\.error/i.test(l)).map((l) => l.replace(/"timestamp":"[^"]+",?/, '')) });

const CELLS: Record<string, (hash: string) => Promise<any>> = {
  tx: async () => { h.reject = /WHERE transaction_hash = \$1/; return send('GET', `/api/anchors/tx/${TX_SEEDED}`); },
  hash_nochain: async (hs) => { h.reject = /LOWER\(content_hash\) = \$1/; return send('GET', `/api/anchors/verify/${hs}`, undefined, true); },
  hash_chain_miss: async (hs) => { h.reject = /LOWER\(content_hash\) = \$1/; h.cardano = true; h.chainHash = 'ee'.repeat(32); return send('GET', `/api/anchors/verify/${hs}`, undefined, true); },
  hash_chain_hit: async (hs) => { h.reject = /LOWER\(content_hash\) = \$1/; h.cardano = true; h.chainHash = hs; return send('GET', `/api/anchors/verify/${hs}`, undefined, true); },
  verify_post: async (hs) => { h.reject = /content_hash = \$1 AND status = 'confirmed'/; return send('POST', '/api/anchors/verify', { contentHash: hs }); },
};

test('g137 anchoring probe', async () => {
  { const hs = uniqHash(); reset(hs); const res = await send('GET', `/api/anchors/tx/${TX_SEEDED}`, undefined, true); await settle(); rec({ cell: 'anon_control_tx_requires_auth', kind: 'none', res, ...snap() }); }
  { const hs = uniqHash(); reset(hs); const res = await send('GET', `/api/anchors/verify/${hs}`, undefined, true); await settle(); rec({ cell: 'anon_control_hash_db_hit', kind: 'none', res, ...snap() }); }
  // positive controls: the stand-in returns the seeded row when nothing throws
  for (const [cell, fn] of Object.entries(CELLS)) {
    const hs = uniqHash(); reset(hs);
    const run = async () => { const pat = h.reject; return fn(hs); };
    // run with reject disabled: call the cell then clear its pattern before the request is not possible, so emulate
    h.value = undefined;
    const saved = fn; void saved;
    let res: any;
    if (cell === 'tx') res = await send('GET', `/api/anchors/tx/${TX_SEEDED}`);
    else if (cell === 'verify_post') res = await send('POST', '/api/anchors/verify', { contentHash: hs });
    else { if (cell !== 'hash_nochain') { h.cardano = true; h.chainHash = cell === 'hash_chain_hit' ? hs : 'ee'.repeat(32); } res = await send('GET', `/api/anchors/verify/${hs}`, undefined, true); }
    await settle(); void run;
    rec({ cell, kind: 'none(seeded row readable)', res, ...snap() });
  }
  for (const [kind, mk] of Object.entries(KINDS)) {
    for (const [cell, fn] of Object.entries(CELLS)) {
      const hs = uniqHash(); reset(hs); h.value = mk();
      const res = await fn(hs); await settle();
      rec({ cell, kind, res, ...snap() });
    }
  }
  rec({ cell: 'network', connects: Array.from(new Set(connects)), outbound, fetchUrls: Array.from(new Set(fetchUrls)) });
}, 300000);
