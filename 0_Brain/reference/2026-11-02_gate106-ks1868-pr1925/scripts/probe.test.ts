// gate 106 probe (NOT part of the PR). Real verificationRouter + verificationV2Router (with the REAL authenticate middleware) on a loopback listener.
// Replaced: db ($queryRaw, stateful row store), the JWKS verifier, the heal (stateful write counter), the lineage repo, the logger.
import * as fs from 'fs';
import type { AddressInfo } from 'net';
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:9';
const OUT = process.env.PROBE_OUT as string;
const emit = (o: unknown) => fs.appendFileSync(OUT, JSON.stringify(o) + '\n');

type Mode = { kind: 'none' } | { kind: 'dbpre'; v: () => unknown } | { kind: 'dbgetter'; v: () => unknown } | { kind: 'reqdb'; v: () => unknown }
  | { kind: 'healapplied'; v: () => unknown } | { kind: 'json'; v: () => unknown };
let mode: Mode = { kind: 'none' };
const TX = 'a'.repeat(64);
const ROW = {
  id: '44444444-4444-4444-8444-444444444444', external_id: 'DOC-HOLDERX', title: 'HolderBob Deed', document_type: 'deed', content_hash: 'sha256:' + 'f'.repeat(64),
  status: 'certified', certification_metadata: { issuerName: 'AcmeOrgX', blockchain: { txHash: TX, status: 'pending', anchorId: 'anc-1', network: 'preprod' } },
  metadata: {}, created_at: '2026-01-01T00:00:00.000Z', certified_at: '2026-01-02T00:00:00.000Z', tenant_id: 'tenant-owner-x', parent_document_id: null, owner_user_id: 'u-holder', organization_name: 'AcmeOrgX',
};
const state = { heals: 0, healWrites: 0, queries: 0 };
const logs: any[] = [];
let unhandled: string[] = [];
process.on('unhandledRejection', (r: any) => { let s = 'unreadable'; try { s = String(r instanceof Error ? r.message : r); } catch { /* */ } unhandled.push(s); });

async function q(strings: TemplateStringsArray): Promise<any[]> {
  state.queries++;
  const s = strings.join('?').replace(/\s+/g, ' ');
  if (mode.kind === 'dbpre') throw mode.v();
  if (mode.kind === 'dbgetter') { const v = (mode as any).v; const e = new Error('outer'); Object.defineProperty(e, 'message', { get() { throw v(); } }); throw e; }
  if (/FROM documents d/.test(s) && /(content_hash|external_id) =/.test(s)) return [JSON.parse(JSON.stringify(ROW))];
  return [];
}
jest.mock('../db', () => ({ prisma: { $queryRaw: (s: any) => q(s) }, getTenantManager: () => null }));
jest.mock('@secuura/shared/crypto/jwks', () => ({
  verifyJwtRs256: async (t: string) => {
    if (t === 'good-caller') return { userId: 'u-caller', email: 'caller@example.test', role: 'user', tenantId: 'tenant-caller-y' };
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
    if (input.write && input.authHeader) state.healWrites++; // the real heal writes only with a bearer and write=true
    if (mode.kind === 'healapplied') throw mode.v();
    return { ...input.blob, status: 'confirmed', anchored: true, blockHeight: 7 };
  },
}));
jest.mock('../utils/logger', () => ({
  logger: { info: (...a: any[]) => logs.push(['info', ...a]), warn: (...a: any[]) => logs.push(['warn', ...a]), error: (...a: any[]) => logs.push(['error', ...a]), debug: () => {} },
}));

// eslint-disable-next-line @typescript-eslint/no-var-requires
const express = require('express');
const { verificationRouter } = require('../routes/verification');
const { verificationV2Router } = require('../routes/verificationV2');
// Express 4 ignores a handler's returned promise. Record what ESCAPES a handler (the request still gets no answer, exactly as
// in production; this only stops jest from crashing on a revoked Proxy reaching its own formatter).
let escaped: string[] = [];
function describe0(e: any): string { try { return 'escaped:' + (e instanceof Error ? e.constructor.name + ':' + e.message : typeof e + ':' + String(e)); } catch { return 'escaped:UNREADABLE'; } }
for (const r of [verificationRouter, verificationV2Router]) for (const l of r.stack) if (l.route) for (const h of l.route.stack) {
  const orig = h.handle;
  h.handle = function (req: any, res: any, next: any) { const p = orig(req, res, next); if (p && typeof p.catch === 'function') p.catch((e: any) => escaped.push(describe0(e))); return p; };
}

function revokedProxy(): object { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function throwingGetter(): Error { const e = new Error('hidden SECRETVAL'); Object.defineProperty(e, 'message', { get() { throw new Error('getter SECRETVAL'); } }); return e; }
function getterThrowsProxy(): Error { const e = new Error('hidden SECRETVAL'); Object.defineProperty(e, 'message', { get() { throw revokedProxy(); } }); return e; }
const KINDS: Record<string, () => unknown> = {
  ordinaryError: () => new Error('db down SECRETVAL tenant-owner-x HolderBob'), string: () => 'plain SECRETVAL', revokedProxy, throwingGetter, getterThrowsProxy,
};

let server: any; let base = '';
beforeAll((done) => {
  const app = express();
  app.use((req: any, res: any, n: any) => {
    const m = mode;
    if (m.kind === 'reqdb') Object.defineProperty(req, 'db', { get() { throw m.v(); } });
    if (m.kind === 'json') { const real = res.json.bind(res); let first = true; res.json = (b: unknown) => { if (first) { first = false; throw m.v(); } return real(b); }; }
    n();
  });
  app.use('/api/verification', (req: any, _r: any, n: any) => (req.path.startsWith('/verify-file') ? n() : express.json()(req, _r, n)), verificationRouter);
  app.use('/api/v2/verification', (req: any, _r: any, n: any) => (req.path.startsWith('/verify-file') ? n() : express.json()(req, _r, n)), verificationV2Router);
  server = app.listen(0, '127.0.0.1', () => { base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port; done(); });
});
afterAll((done) => { server.closeAllConnections?.(); server.close(() => done()); });

type Cell = { route: string; method: string; path: string; body?: string; json?: boolean; modes: string[] };
const CELLS: Cell[] = [
  { route: 'v1 POST /verify-file', method: 'POST', path: '/api/verification/verify-file', body: 'file bytes', modes: ['dbpre', 'healapplied', 'json'] },
  { route: 'v1 POST /verify', method: 'POST', path: '/api/verification/verify', body: JSON.stringify({ hash: 'f'.repeat(64) }), json: true, modes: ['reqdb', 'dbpre', 'dbgetter', 'healapplied', 'json'] },
  { route: 'v1 POST /verify (documentId)', method: 'POST', path: '/api/verification/verify', body: JSON.stringify({ documentId: 'DOC-HOLDERX' }), json: true, modes: ['reqdb', 'dbpre', 'json'] },
  { route: 'v1 POST /hash', method: 'POST', path: '/api/verification/hash', body: JSON.stringify({ data: 'x' }), json: true, modes: ['json'] },
  { route: 'v1 GET /status', method: 'GET', path: '/api/verification/status/DOC-HOLDERX', modes: ['json'] },
  { route: 'v2 POST /verify (hash)', method: 'POST', path: '/api/v2/verification/verify', body: JSON.stringify({ hash: 'f'.repeat(64) }), json: true, modes: ['reqdb', 'dbpre', 'json'] },
  { route: 'v2 POST /verify (documentId)', method: 'POST', path: '/api/v2/verification/verify', body: JSON.stringify({ documentId: 'DOC-HOLDERX' }), json: true, modes: ['reqdb', 'dbpre', 'json'] },
  { route: 'v2 POST /verify-file', method: 'POST', path: '/api/v2/verification/verify-file', body: 'file bytes', modes: ['dbpre', 'json'] },
];
const CALLERS: Record<string, string | undefined> = { anon: undefined, caller: 'Bearer good-caller', owner: 'Bearer good-owner', badtoken: 'Bearer bad' };
const LEAK = ['SECRETVAL', 'tenant-owner-x', 'HolderBob', 'AcmeOrgX', 'u-holder', 'caller@example', 'getter', 'proxy', 'revoked'];

async function call(c: Cell, auth?: string) {
  const headers: Record<string, string> = { 'content-type': c.json ? 'application/json' : 'application/octet-stream' };
  if (auth) headers.authorization = auth;
  try {
    const r = await fetch(base + c.path, { method: c.method, headers, body: c.body, signal: AbortSignal.timeout(1500) });
    return { status: r.status as number | string, ctype: r.headers.get('content-type'), body: await r.text() };
  } catch { return { status: 'NO ANSWER', ctype: null, body: '' }; }
}

const plan: Array<{ c: Cell; m: string; k: string; who: string }> = [];
for (const c of CELLS) {
  const callers = c.route.startsWith('v2') ? Object.keys(CALLERS) : ['anon', 'owner'];
  for (const who of callers) {
    plan.push({ c, m: 'none', k: 'none', who });
    for (const m of c.modes) for (const k of Object.keys(KINDS)) if (!(who === 'badtoken' && m === 'json')) plan.push({ c, m, k, who });
  }
}
test.each(plan.map((p) => [`${p.c.route} ${p.m} ${p.k} ${p.who}`, p]))('%s', async (_n, p: any) => {
  state.heals = 0; state.healWrites = 0; state.queries = 0; logs.length = 0; unhandled = []; escaped = [];
  mode = p.m === 'none' ? { kind: 'none' } : ({ kind: p.m, v: KINDS[p.k] } as Mode);
  const r = await call(p.c, CALLERS[p.who]);
  await new Promise((s) => setTimeout(s, 30));
  mode = { kind: 'none' };
  const errLines = logs.filter((l) => l[0] === 'error').map((l) => [l[1], l[2]]);
  const allLogText = JSON.stringify(logs);
  const leak: Record<string, boolean> = {};
  for (const w of LEAK) leak[w] = r.body.includes(w);
  emit({ route: p.c.route, mode: p.m, kind: p.k, who: p.who, ...r, state: { ...state }, errLines, warnLines: logs.filter((l) => l[0] === 'warn').map((l) => [l[1], l[2]]), unhandled: [...unhandled], escaped: [...escaped], leak, logHasHolder: /HolderBob|AcmeOrgX|caller@example/.test(JSON.stringify(errLines)), logLen: allLogText.length });
});
