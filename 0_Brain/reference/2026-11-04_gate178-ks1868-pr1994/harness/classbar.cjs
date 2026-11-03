// Gate 178 class-bar harness. Usage: node classbar.cjs <tree: base|head> <out.json>
// Drives the REAL compiled app (dist_gate_<tree>/app.js: helmet, cors, boundedJson, rejectControlBytes,
// the shared jwt authenticate with publicOps, the router, 404, the shared errorHandler) over a real
// listening socket with fetch. Each handler's dependency (the real singleton's method) is replaced by
// one that throws / rejects the cell's value. The real winston logger runs; its output is captured.
'use strict';
const path = require('node:path');
const crypto = require('node:crypto');
const util = require('node:util');

const TREE = process.argv[2];
const OUT = process.argv[3];
const SVC = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate178-ks1868-pr1994/repo/Blockchain/Dev/services/nft-certificate';
const DIST = path.join(SVC, `dist_gate_${TREE}`);
const SENT = 'SNTL178';

// RS256 key pair generated in memory only; the public half goes to the env the shared verifier reads.
const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' })).toString('base64');
process.env.NODE_ENV = 'development';
const b64u = (o) => Buffer.from(typeof o === 'string' ? o : JSON.stringify(o)).toString('base64url');
function token() {
  const h = b64u({ alg: 'RS256', typ: 'JWT' });
  const p = b64u({ userId: 'u-gate178', role: 'user', iat: Math.floor(Date.now() / 1000), exp: Math.floor(Date.now() / 1000) + 3600 });
  const s = crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), privateKey).toString('base64url');
  return `${h}.${p}.${s}`;
}
const TOKEN = token();

// ---- capture of every output channel (winston Console writes to console._stdout/_stderr or console.*) ----
let LINES = null;
const safe = (a) => { try { return typeof a === 'string' ? a : util.inspect(a, { depth: 6 }); } catch { return '<uninspectable>'; } };
const ow = process.stdout.write.bind(process.stdout);
const ew = process.stderr.write.bind(process.stderr);
process.stdout.write = (c, ...r) => (LINES ? (LINES.push('stdout: ' + safe(String(c))), true) : ow(c, ...r));
process.stderr.write = (c, ...r) => (LINES ? (LINES.push('stderr: ' + safe(String(c))), true) : ew(c, ...r));
for (const m of ['log', 'warn', 'error', 'info', 'debug']) {
  const o = console[m].bind(console);
  console[m] = (...a) => (LINES ? LINES.push(`console.${m}: ` + a.map(safe).join(' ')) : o(...a));
}

// ---- unhandled rejections / exceptions (process health) ----
const UNH = [];
process.on('unhandledRejection', (r) => { let t; try { t = typeof r; } catch { t = '?'; } UNH.push({ kind: 'unhandledRejection', type: t }); });
process.on('uncaughtException', (e) => { UNH.push({ kind: 'uncaughtException', type: typeof e }); });

const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const VALUES = [
  ['V01 ordinary Error', () => new Error(`${SENT}-ord`)],
  ['V02 Error, message getter throws', () => Object.create(Error.prototype, { message: { get() { throw new Error(`${SENT}-getter`); } } })],
  ['V03 revoked Proxy', () => revoked()],
  ['V04 null', () => null],
  ['V05 undefined', () => undefined],
  ['V06 string', () => `${SENT}-str`],
  ['V07 number', () => 178],
  ['V08 Object.create(null)', () => Object.create(null)],
  ['V09 {message: Symbol}', () => ({ message: Symbol(`${SENT}-sym`) })],
  ['V10 {message: BigInt}', () => ({ message: BigInt(178) })],
  ['V11 {message: revoked Proxy}', () => ({ message: revoked() })],
  ['V12 {message: obj whose toString throws}', () => ({ message: { toString() { throw new Error(`${SENT}-ts`); } } })],
  ['V13 Proxy whose get trap throws', () => new Proxy({}, { get() { throw new Error(`${SENT}-trap`); } })],
  ['V14 thrown Symbol', () => Symbol(`${SENT}-thrownsym`)],
  ['V15 Error, name getter throws (message readable)', () => { const e = new Error(`${SENT}-namegetter`); Object.defineProperty(e, 'name', { get() { throw new Error('name boom'); } }); return e; }],
  ['V16 {message readable, toString throws}', () => ({ message: `${SENT}-msgok`, toString() { throw new Error('ts boom'); } })],
  ['V17 plain {message}', () => ({ message: `${SENT}-plain` })],
];

const app = require(path.join(DIST, 'app.js')).default;
const { nftMintingService } = require(path.join(DIST, 'services/minting.service.js'));
const { blockchainVerifier } = require(path.join(DIST, 'services/blockchain-verifier.service.js'));
const { ipfsService } = require(path.join(DIST, 'services/ipfs.service.js'));
const { logger } = require(path.join(DIST, 'utils/logger.js'));

// Record the logged meta's `error` field TYPE (never its value) on every logger.error call.
const LOGGED = [];
const origErr = logger.error.bind(logger);
logger.error = (msg, meta) => { let t; try { t = meta && typeof meta.error; } catch { t = '?'; } LOGGED.push({ msg: String(msg), errorType: t }); return origErr(msg, meta); };

let CUR = () => new Error('unset');
const rejecter = () => Promise.reject(CUR());
const thrower = () => { throw CUR(); };
const HANDLERS = [
  { id: 'GET /certificates/:id', m: 'GET', p: '/api/nft/certificates/abc', auth: true, stub: () => (nftMintingService.getNFTCertificate = rejecter) },
  { id: 'GET /certificates', m: 'GET', p: '/api/nft/certificates', auth: true, stub: () => (nftMintingService.getUserNFTCertificates = rejecter) },
  { id: 'GET /tiers', m: 'GET', p: '/api/nft/tiers', auth: true, stub: () => (nftMintingService.getQuickEstimate = thrower) },
  { id: 'POST /estimate', m: 'POST', p: '/api/nft/estimate', auth: true, body: { storageTier: 'basic', chain: 'cardano' }, stub: () => (nftMintingService.estimateCost = thrower) },
  { id: 'POST /verify/transaction', m: 'POST', p: '/api/nft/verify/transaction', auth: false, body: { txHash: 'a'.repeat(64) }, stub: () => (blockchainVerifier.verifyTransaction = rejecter) },
  { id: 'POST /verify/asset', m: 'POST', p: '/api/nft/verify/asset', auth: false, body: { policyId: 'p1', assetNameHex: '6162' }, stub: () => (blockchainVerifier.verifyAsset = rejecter) },
  { id: 'POST /ipfs/pin', m: 'POST', p: '/api/nft/ipfs/pin', auth: true, body: { cid: 'bafy' }, stub: () => (ipfsService.pin = rejecter) },
  { id: 'POST /ipfs/unpin', m: 'POST', p: '/api/nft/ipfs/unpin', auth: true, body: { cid: 'bafy' }, stub: () => (ipfsService.unpin = rejecter) },
];

async function req(base, h, { withToken, timeoutMs }) {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), timeoutMs);
  const headers = { 'content-type': 'application/json' };
  if (withToken) headers.authorization = `Bearer ${TOKEN}`;
  try {
    const r = await fetch(base + h.p, { method: h.m, headers, body: h.body ? JSON.stringify(h.body) : undefined, signal: ac.signal });
    const text = await r.text();
    return { replied: true, status: r.status, body: text, headerNames: [...r.headers.keys()].sort().join(',') };
  } catch (e) {
    return { replied: false, status: null, body: null, why: e && e.name };
  } finally {
    clearTimeout(t);
  }
}

async function health(base) {
  try { const r = await fetch(base + '/health', { signal: AbortSignal.timeout(5000) }); return r.status; } catch { return 'DOWN'; }
}

async function cell(base, h, v, opts) {
  CUR = v[1];
  LOGGED.length = 0;
  const unh0 = UNH.length;
  LINES = [];
  const r = await req(base, h, opts);
  await new Promise((s) => setTimeout(s, 50)); // let a pending rejection surface
  const lines = LINES; LINES = null;
  return {
    handler: h.id, cls: v[0], ...r,
    bodySentinel: r.body ? (r.body.match(new RegExp(SENT, 'g')) || []).length : 0,
    logLinesSentinel: lines.filter((l) => l.includes(SENT)).length,
    logLines: lines.length,
    logged: LOGGED.map((x) => `${x.msg}|${x.errorType}`),
    unhandled: UNH.slice(unh0).map((x) => `${x.kind}:${x.type}`),
    healthAfter: await health(base),
  };
}

(async () => {
  const server = app.listen(0, '127.0.0.1');
  await new Promise((s) => server.once('listening', s));
  const base = `http://127.0.0.1:${server.address().port}`;
  const out = { tree: TREE, express: require(require.resolve('express/package.json', { paths: [SVC] })).version, node: process.version, cells: [], rerun: [], auth: [], q8: [] };
  for (const h of HANDLERS) {
    h.stub();
    for (const v of VALUES) out.cells.push(await cell(base, h, v, { withToken: true, timeoutMs: 2500 }));
  }
  // Re-run every no-reply cell ALONE with a long timeout (host load guard).
  for (const c of out.cells.filter((c) => !c.replied)) {
    const h = HANDLERS.find((x) => x.id === c.handler); h.stub();
    const v = VALUES.find((x) => x[0] === c.cls);
    const r = await cell(base, h, v, { withToken: true, timeoutMs: 10000 });
    out.rerun.push({ handler: c.handler, cls: c.cls, replied: r.replied, status: r.status, unhandled: r.unhandled });
  }
  // Q2: who can reach each handler. No token: public ops must reach the handler (ordinary Error -> 500),
  // every other op must stop at auth (401). Also a bad token on a public op.
  for (const h of HANDLERS) {
    h.stub();
    const v = VALUES[0];
    const noTok = await cell(base, h, v, { withToken: false, timeoutMs: 5000 });
    out.auth.push({ handler: h.id, mode: 'no token', status: noTok.status, reachedHandler: noTok.logged.length > 0, body: noTok.body });
  }
  server.close();
  server.closeAllConnections && server.closeAllConnections();

  // Q8 control: the same express module, an async handler that rejects vs a sync handler that throws.
  const express = require(require.resolve('express', { paths: [SVC] }));
  const a2 = express();
  a2.get('/async-reject', async () => { throw new Error('ctl'); });
  a2.get('/sync-throw', () => { throw new Error('ctl'); });
  a2.get('/async-next', async (_q, _s, next) => { try { throw new Error('ctl'); } catch (e) { next(e); } });
  a2.use((err, _q, res, _n) => res.status(500).json({ handled: true }));
  const s2 = a2.listen(0, '127.0.0.1');
  await new Promise((s) => s2.once('listening', s));
  const b2 = `http://127.0.0.1:${s2.address().port}`;
  for (const p of ['/async-reject', '/sync-throw', '/async-next']) {
    const u0 = UNH.length;
    const r = await req(b2, { m: 'GET', p }, { withToken: false, timeoutMs: 3000 });
    await new Promise((s) => setTimeout(s, 50));
    out.q8.push({ path: p, replied: r.replied, status: r.status, unhandled: UNH.slice(u0).map((x) => x.kind) });
  }
  s2.close(); s2.closeAllConnections && s2.closeAllConnections();
  require('node:fs').writeFileSync(OUT, JSON.stringify(out, null, 1));
  ow(`done ${TREE}: cells ${out.cells.length}, noReply ${out.cells.filter((c) => !c.replied).length}, unhandledTotal ${UNH.length}\n`);
  process.exit(0);
})().catch((e) => { ew('HARNESS FAIL ' + safe(e) + '\n'); process.exit(3); });
