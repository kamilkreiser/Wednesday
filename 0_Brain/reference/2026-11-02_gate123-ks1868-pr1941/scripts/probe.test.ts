// gate 123 probe (NOT part of the PR). Real verificationRouter + verificationV2Router (v2 behind the REAL authenticate({required:false}))
// and the REAL winston logger (formats run; each transport's log() is captured instead of written). Loopback listener.
// Replaced: db ($queryRaw / $executeRaw counters), the JWKS verifier, the heal (write counter), the lineage repo, and the
// anchoring service fetch (globalThis.fetch for /api/anchors/verify/ only).
import * as fs from 'fs';
import type { AddressInfo } from 'net';
process.env.NODE_ENV = 'development';
process.env.ANCHORING_SERVICE_URL = 'http://anchoring.invalid:4005';
const OUT = process.env.PROBE_OUT as string;
const emit = (o: unknown) => fs.appendFileSync(OUT, JSON.stringify(o) + '\n');

type Mode = { kind: 'none' | 'nomatch' | 'chainok' | 'chain503' } | { kind: 'dbpre' | 'reqdb' | 'json' | 'chain'; v: () => unknown };
let mode: Mode = { kind: 'none' };
const TX = 'a'.repeat(64);
const ROW = {
  id: '44444444-4444-4444-8444-444444444444', external_id: 'DOC-HOLDERX', title: 'HolderBob Deed', document_type: 'deed', content_hash: 'sha256:' + 'f'.repeat(64),
  status: 'certified', certification_metadata: { issuerName: 'AcmeOrgX', blockchain: { txHash: TX, status: 'confirmed', anchorId: 'anc-1', network: 'preprod' } },
  metadata: {}, created_at: '2026-01-01T00:00:00.000Z', certified_at: '2026-01-02T00:00:00.000Z', tenant_id: 'tenant-owner-x', parent_document_id: null, owner_user_id: 'u-holder', organization_name: 'AcmeOrgX',
};
const state = { heals: 0, healWrites: 0, queries: 0, executes: 0, chainFetches: 0, errorHandler: 0 };
let unhandled: string[] = [];
process.on('unhandledRejection', (r: any) => { let s = 'unreadable'; try { s = String(r instanceof Error ? r.message : r); } catch { /* */ } unhandled.push(s); });

async function q(strings: TemplateStringsArray): Promise<any[]> {
  state.queries++;
  const s = strings.join('?').replace(/\s+/g, ' ');
  if (mode.kind === 'dbpre') throw (mode as any).v();
  if (mode.kind === 'nomatch' || mode.kind === 'chain' || mode.kind === 'chainok' || mode.kind === 'chain503') return [];
  if (/FROM documents d/.test(s) && /(content_hash|external_id) =/.test(s)) return [JSON.parse(JSON.stringify(ROW))];
  return [];
}
jest.mock('../db', () => ({ prisma: { $queryRaw: (s: any) => q(s), $executeRaw: async () => { state.executes++; return 0; } }, getTenantManager: () => null }));
jest.mock('@secuura/shared/crypto/jwks', () => ({
  verifyJwtRs256: async (t: string) => {
    if (t === 'good-owner') return { userId: 'u-holder', email: 'holder@example.test', role: 'user', tenantId: 'tenant-owner-x' };
    const e = new Error('jwt malformed'); e.name = 'JsonWebTokenError'; throw e;
  },
}));
jest.mock('@secuura/shared', () => require('./helpers/sharedModuleMock').makeSharedMock({
  runWithTenantId: (_t: unknown, fn: () => unknown) => fn(), queryWithTenantGuc: jest.fn(), isSessionActive: jest.fn().mockResolvedValue(true),
}));
jest.mock('../repositories/documentRepo', () => ({
  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
  updateDocument: jest.fn().mockResolvedValue(undefined), MAX_LINEAGE_DEPTH: 10,
}));
jest.mock('../services/anchorStateSync', () => ({
  ...jest.requireActual('../services/anchorStateSync'),
  healAnchorForVerify: async (input: any) => {
    state.heals++;
    if (input.write && input.authHeader) state.healWrites++;
    return { ...input.blob, status: 'confirmed', anchored: true, blockHeight: 7 };
  },
}));

// eslint-disable-next-line @typescript-eslint/no-var-requires
const express = require('express');
const { logger } = require('../utils/logger');
const MESSAGE = Symbol.for('message');
const logs: any[] = [];
for (const t of logger.transports) {
  t.log = (info: any, next: () => void) => {
    let line = ''; try { line = String(info[MESSAGE]).replace(/\u001b\[[0-9;]*m/g, ''); } catch { line = 'UNPRINTABLE'; }
    let err: string; try { err = typeof info.error === 'string' ? info.error : 'NONSTRING:' + typeof info.error; } catch { err = 'UNREADABLE'; }
    logs.push({ level: String(info.level).replace(/\u001b\[[0-9;]*m/g, ''), message: String(info.message), error: err, line });
    next();
  };
}
const { verificationRouter } = require('../routes/verification');
const { verificationV2Router } = require('../routes/verificationV2');
let escaped: string[] = [];
function describe0(e: any): string { try { return 'escaped:' + (e instanceof Error ? e.constructor.name + ':' + e.message : typeof e + ':' + String(e)); } catch { return 'escaped:UNREADABLE'; } }
for (const r of [verificationRouter, verificationV2Router]) for (const l of r.stack) if (l.route) for (const h of l.route.stack) {
  const orig = h.handle;
  h.handle = function (req: any, res: any, next: any) { const p = orig(req, res, next); if (p && typeof p.catch === 'function') p.catch((e: any) => escaped.push(describe0(e))); return p; };
}

const realFetch = globalThis.fetch;
(globalThis as any).fetch = async (input: any, init?: any) => {
  if (!String(input).includes('/api/anchors/verify/')) return realFetch(input, init);
  state.chainFetches++;
  if (mode.kind === 'chain') throw (mode as any).v();
  if (mode.kind === 'chainok') return new Response(JSON.stringify({ verified: true, source: 'chain', network: 'preprod', txHash: TX, blockNumber: 9, confirmedAt: '2026-01-03T00:00:00.000Z', metadata: { documentId: 'DOC-CHAIN' } }), { status: 200, headers: { 'content-type': 'application/json' } });
  return new Response(null, { status: 503 });
};

function revokedProxy(): object { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function msgErr(get: () => unknown): Error { const e = new Error('hidden SECRETVAL'); Object.defineProperty(e, 'message', { get }); return e; }
const KINDS: Record<string, () => unknown> = {
  ordinaryError: () => new Error('db down SECRETVAL tenant-owner-x HolderBob'),
  string: () => 'plain SECRETVAL',
  revokedProxy,
  throwingGetter: () => msgErr(() => { throw new Error('getter SECRETVAL'); }),
  getterThrowsProxy: () => msgErr(() => { throw revokedProxy(); }),
  msgRevokedProxy: () => msgErr(() => revokedProxy()),
  msgThrowToJson: () => msgErr(() => ({ toJSON() { throw new Error('toJSON SECRETVAL'); } })),
  msgObject: () => msgErr(() => ({ field: 'SECRETVAL', tenant: 'tenant-owner-x' })),
  msgNullProto: () => msgErr(() => Object.assign(Object.create(null), { field: 'SECRETVAL' })),
  msgToString: () => msgErr(() => ({ toString() { return 'custom SECRETVAL'; } })),
  msgNumber: () => { const e = new Error('x'); Object.defineProperty(e, 'message', { value: 42 }); return e; },
};

let server: any; let base = '';
beforeAll((done) => {
  const app = express();
  app.use((req: any, res: any, n: any) => {
    const m: any = mode;
    if (m.kind === 'reqdb') Object.defineProperty(req, 'db', { get() { throw m.v(); } });
    if (m.kind === 'json') { const real = res.json.bind(res); let first = true; res.json = (b: unknown) => { if (first) { first = false; throw m.v(); } return real(b); }; }
    n();
  });
  app.use('/api/verification', (req: any, _r: any, n: any) => (req.path.startsWith('/verify-file') ? n() : express.json()(req, _r, n)), verificationRouter);
  app.use('/api/v2/verification', (req: any, _r: any, n: any) => (req.path.startsWith('/verify-file') ? n() : express.json()(req, _r, n)), verificationV2Router);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  app.use((_e: any, _q: any, res: any, _n: any) => { state.errorHandler++; res.status(599).json({ probe: 'errorHandler' }); });
  server = app.listen(0, '127.0.0.1', () => { base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port; done(); });
});
afterAll((done) => { (globalThis as any).fetch = realFetch; server.closeAllConnections?.(); server.close(() => done()); });

type Cell = { route: string; method: string; path: string; body?: string; json?: boolean; modes: string[]; site: string };
const H = JSON.stringify({ hash: 'f'.repeat(64) });
const CELLS: Cell[] = [
  { site: 'B2 v1 :758', route: 'v1 POST /verify-file', method: 'POST', path: '/api/verification/verify-file', body: 'file bytes', modes: ['dbpre', 'json'] },
  { site: 'v1 :698 chain (not in PR)', route: 'v1 POST /verify-file', method: 'POST', path: '/api/verification/verify-file', body: 'file bytes', modes: ['chain'] },
  { site: 'B1 v1 :1443', route: 'v1 POST /verify', method: 'POST', path: '/api/verification/verify', body: H, json: true, modes: ['reqdb'] },
  { site: 'v1 :1243 chain (not in PR)', route: 'v1 POST /verify', method: 'POST', path: '/api/verification/verify', body: H, json: true, modes: ['chain'] },
  { site: 'B1 v1 :1478', route: 'v1 POST /hash', method: 'POST', path: '/api/verification/hash', body: JSON.stringify({ data: 'x' }), json: true, modes: ['json'] },
  { site: 'B1 v1 :1506', route: 'v1 GET /status', method: 'GET', path: '/api/verification/status/DOC-HOLDERX', modes: ['json'] },
  { site: 'B3 v2 :446', route: 'v2 POST /verify (hash)', method: 'POST', path: '/api/v2/verification/verify', body: H, json: true, modes: ['reqdb', 'dbpre', 'json'] },
  { site: 'B3 v2 :446', route: 'v2 POST /verify (documentId)', method: 'POST', path: '/api/v2/verification/verify', body: JSON.stringify({ documentId: 'DOC-HOLDERX' }), json: true, modes: ['reqdb', 'dbpre', 'json'] },
  { site: 'P3 v2 :111 via /verify', route: 'v2 POST /verify (hash)', method: 'POST', path: '/api/v2/verification/verify', body: H, json: true, modes: ['chain'] },
  { site: 'B3 v2 :488', route: 'v2 POST /verify-file', method: 'POST', path: '/api/v2/verification/verify-file', body: 'file bytes', modes: ['dbpre', 'json'] },
  { site: 'P3 v2 :111 via /verify-file', route: 'v2 POST /verify-file', method: 'POST', path: '/api/v2/verification/verify-file', body: 'file bytes', modes: ['chain'] },
];
const CALLERS: Record<string, string | undefined> = { anon: undefined, owner: 'Bearer good-owner' };
const LEAK = ['SECRETVAL', 'tenant-owner-x', 'HolderBob', 'AcmeOrgX', 'u-holder', 'getter', 'proxy', 'revoked', 'toJSON', 'stack', 'object Object', '42'];

async function call(c: Cell, auth?: string) {
  const headers: Record<string, string> = { 'content-type': c.json ? 'application/json' : 'application/octet-stream' };
  if (auth) headers.authorization = auth;
  try {
    const r = await realFetch(base + c.path, { method: c.method, headers, body: c.body, signal: AbortSignal.timeout(1500) });
    return { status: r.status as number | string, ctype: r.headers.get('content-type'), body: await r.text() };
  } catch { return { status: 'NO ANSWER', ctype: null, body: '' }; }
}

const plan: Array<{ c: Cell; m: string; k: string; who: string }> = [];
for (const c of CELLS) for (const who of Object.keys(CALLERS)) {
  const controls = c.modes.includes('chain') ? ['nomatch', 'chainok', 'chain503'] : ['none'];
  for (const m of controls) plan.push({ c, m, k: 'none', who });
  for (const m of c.modes) for (const k of Object.keys(KINDS)) plan.push({ c, m, k, who });
}
test.each(plan.map((p) => [`${p.c.site} | ${p.c.route} ${p.m} ${p.k} ${p.who}`, p]))('%s', async (_n, p: any) => {
  for (const k of Object.keys(state)) (state as any)[k] = 0;
  logs.length = 0; unhandled = []; escaped = [];
  mode = (['none', 'nomatch', 'chainok', 'chain503'].includes(p.m) ? { kind: p.m } : { kind: p.m, v: KINDS[p.k] }) as Mode;
  const r = await call(p.c, CALLERS[p.who]);
  await new Promise((s) => setTimeout(s, 30));
  mode = { kind: 'none' };
  const leak: string[] = LEAK.filter((w) => r.body.includes(w));
  emit({ site: p.c.site, route: p.c.route, mode: p.m, kind: p.k, who: p.who, ...r, state: { ...state }, logs: logs.filter((l) => l.level !== 'info').map((l) => ({ ...l })), unhandled: [...unhandled], escaped: [...escaped], leak });
});
