// gate 122 probe (NOT part of the PR). The REAL verificationRouter (POST /api/verification/verify, the public verify route) on a loopback listener.
// Replaced: the db ($queryRaw / $executeRaw: a recorder that answers canned rows and logs EVERY statement), the heal (write counter, writes only
// with a bearer, as the real one), the lineage repo, the logger. Everything in routes/verification.ts runs for real.
import * as fs from 'fs';
import type { AddressInfo } from 'net';
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:9';
const OUT = process.env.PROBE_OUT as string;
const emit = (o: unknown) => fs.appendFileSync(OUT, JSON.stringify(o) + '\n');

let mode: { kind: string; v?: () => unknown } = { kind: 'none' };
const HASH = 'f'.repeat(64);
const TX = 'a'.repeat(64);
const ROW_HASH = {
  id: '44444444-4444-4444-8444-444444444444', external_id: 'DOC-HOLDERX', title: 'HolderBob Deed', document_type: 'deed', content_hash: 'sha256:' + HASH,
  status: 'certified', certification_metadata: { issuerName: 'AcmeOrgX', blockchain: { txHash: TX, status: 'pending', anchorId: 'anc-1', network: 'preprod' } },
  metadata: {}, created_at: '2026-01-01T00:00:00.000Z', certified_at: '2026-01-02T00:00:00.000Z', tenant_id: 'tenant-owner-x', parent_document_id: null, owner_user_id: 'u-holder', organization_name: 'AcmeOrgX',
};
// strategy 2's SELECT carries no tenant_id (verification.ts strategy 2), so the by-id row has none
const ROW_ID = (() => { const r: any = JSON.parse(JSON.stringify(ROW_HASH)); delete r.tenant_id; delete r.parent_document_id; delete r.owner_user_id; return r; })();
const state = { queries: 0, writeStmts: 0, execRaw: 0, heals: 0, healWrites: 0, updateDocument: 0 };
const stmts: string[] = [];
const logs: any[] = [];
let unhandled: string[] = [];
process.on('unhandledRejection', (r: any) => { let s = 'unreadable'; try { s = String(r instanceof Error ? r.message : r); } catch { /* */ } unhandled.push(s); });
function thrownFor(): never { const v = mode.v as () => unknown; throw v(); }
function getterErr(): Error { const v = mode.v as () => unknown; const e = new Error('outer'); Object.defineProperty(e, 'message', { get() { throw v(); } }); return e; }

async function q(strings: TemplateStringsArray, ...vals: unknown[]): Promise<any[]> {
  state.queries++;
  const s = strings.join('?').replace(/\s+/g, ' ').trim();
  stmts.push(s.slice(0, 90));
  if (/\b(INSERT|UPDATE|DELETE|MERGE|UPSERT|TRUNCATE)\b/i.test(s)) state.writeStmts++;
  const main = /FROM documents d/.test(s) && /(d\.content_hash =|d\.external_id =|SELECT 1 AS found)/.test(s);
  if (main && mode.kind === 'dbpre') thrownFor();
  if (main && mode.kind === 'dbgetter') throw getterErr();
  if (/^SELECT external_id, tenant_id FROM documents/.test(s) && mode.kind === 'lineageq') thrownFor();
  if (/FROM documents d/.test(s) && /d\.content_hash =/.test(s)) return [JSON.parse(JSON.stringify(ROW_HASH))];
  if (/FROM documents d/.test(s) && /d\.external_id =/.test(s)) {
    if (vals[0] === 'MISSING') return [];
    const r = JSON.parse(JSON.stringify(ROW_ID));
    if (mode.kind === 'rowgetter') Object.defineProperty(r, 'status', { get() { return thrownFor(); }, enumerable: true });
    return [r];
  }
  if (/SELECT 1 AS found/.test(s)) return vals[0] === 'MISSING' ? [] : [{ found: 1 }];
  if (/^SELECT external_id, tenant_id FROM documents/.test(s)) return [{ external_id: 'DOC-HOLDERX', tenant_id: 'tenant-owner-x' }];
  return [];
}
jest.mock('../db', () => ({ prisma: { $queryRaw: (s: any, ...v: any[]) => q(s, ...v), $executeRaw: (s: any, ...v: any[]) => { state.execRaw++; state.writeStmts++; return q(s, ...v).then(() => 1); } }, getTenantManager: () => null }));
jest.mock('@secuura/shared', () => require('./helpers/sharedModuleMock').makeSharedMock({
  runWithTenantId: (_t: unknown, fn: () => unknown) => fn(), queryWithTenantGuc: jest.fn(), isSessionActive: jest.fn().mockResolvedValue(true),
}));
jest.mock('../repositories/documentRepo', () => ({
  walkAncestors: async () => { if (mode.kind === 'walk') thrownFor(); return { lineage: [{ documentId: 'DOC-PARENT', title: 'p', status: 'certified', depth: 1 }], truncated: false }; },
  walkDescendants: async () => ({ descendants: [], truncated: false }),
  updateDocument: async () => { state.updateDocument++; }, MAX_LINEAGE_DEPTH: 10,
}));
jest.mock('../services/anchorStateSync', () => ({
  ...jest.requireActual('../services/anchorStateSync'),
  healAnchorForVerify: async (input: any) => {
    state.heals++;
    if (input.write && input.authHeader) state.healWrites++;
    if (mode.kind === 'healapplied') thrownFor();
    return { ...input.blob, status: 'confirmed', anchored: true, blockHeight: 7 };
  },
}));
jest.mock('../utils/logger', () => ({
  logger: { info: (...a: any[]) => logs.push(['info', ...a]), warn: (...a: any[]) => logs.push(['warn', ...a]), error: (...a: any[]) => logs.push(['error', ...a]), debug: () => {} },
}));

// eslint-disable-next-line @typescript-eslint/no-var-requires
const express = require('express');
const { verificationRouter } = require('../routes/verification');
let escaped: string[] = [];
function describe0(e: any): string { try { return 'escaped:' + (e instanceof Error ? e.constructor.name + ':' + e.message : typeof e + ':' + String(e)); } catch { return 'escaped:UNREADABLE'; } }
for (const l of verificationRouter.stack) if (l.route) for (const h of l.route.stack) {
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
let who = 'anon';
beforeAll((done) => {
  const app = express();
  app.use((req: any, res: any, n: any) => {
    if (who === 'owner') req.tenantId = 'tenant-owner-x';
    const m = mode;
    if (m.kind === 'json' || m.kind === 'jsonaftersend') {
      const real = res.json.bind(res); let first = true;
      res.json = (b: unknown) => { if (first) { first = false; if (m.kind === 'jsonaftersend') real(b); throw (m.v as () => unknown)(); } return real(b); };
    }
    n();
  });
  app.use('/api/verification', express.json(), verificationRouter);
  server = app.listen(0, '127.0.0.1', () => { base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port; done(); });
});
afterAll((done) => { server.closeAllConnections?.(); server.close(() => done()); });

type Cell = { route: string; body: unknown; modes: string[] };
const CELLS: Cell[] = [
  { route: 'byId', body: { documentId: 'DOC-HOLDERX' }, modes: ['dbpre', 'dbgetter', 'rowgetter', 'json', 'jsonaftersend', 'lineageq', 'walk'] },
  { route: 'byIdMissing', body: { documentId: 'MISSING' }, modes: ['json'] },
  { route: 'hash', body: { hash: HASH }, modes: ['dbpre', 'dbgetter', 'healapplied', 'json', 'lineageq', 'walk'] },
  { route: 'title', body: { title: 'HolderBob Deed' }, modes: ['dbpre', 'dbgetter', 'json'] },
  { route: 'titleMissing', body: { title: 'MISSING' }, modes: ['json'] },
];
const CALLERS: Record<string, string | undefined> = { anon: undefined, owner: 'Bearer good-owner' };
const LEAK = ['SECRETVAL', 'tenant-owner-x', 'HolderBob', 'AcmeOrgX', 'u-holder', 'getter', 'proxy', 'revoked', 'stack', 'TypeError', 'outer', 'db down'];

async function call(c: Cell, auth?: string) {
  const headers: Record<string, string> = { 'content-type': 'application/json' };
  if (auth) headers.authorization = auth;
  try {
    const r = await fetch(base + '/api/verification/verify', { method: 'POST', headers, body: JSON.stringify(c.body), signal: AbortSignal.timeout(1500) });
    return { status: r.status as number | string, ctype: r.headers.get('content-type'), body: await r.text() };
  } catch (e: any) { return { status: 'NO ANSWER', ctype: null, body: '', fetchErr: String(e?.name) }; }
}

const plan: Array<{ c: Cell; m: string; k: string; who: string }> = [];
for (const c of CELLS) for (const w of Object.keys(CALLERS)) {
  plan.push({ c, m: 'none', k: 'none', who: w });
  for (const m of c.modes) for (const k of Object.keys(KINDS)) plan.push({ c, m, k, who: w });
}
test.each(plan.map((p) => [`${p.c.route} ${p.m} ${p.k} ${p.who}`, p]))('%s', async (_n, p: any) => {
  for (const k of Object.keys(state)) (state as any)[k] = 0;
  stmts.length = 0; logs.length = 0; unhandled = []; escaped = [];
  who = p.who;
  mode = p.m === 'none' ? { kind: 'none' } : { kind: p.m, v: KINDS[p.k] };
  const r = await call(p.c, CALLERS[p.who]);
  await new Promise((s) => setTimeout(s, 40));
  mode = { kind: 'none' }; who = 'anon';
  const leak: string[] = LEAK.filter((w) => r.body.includes(w));
  const safe = (x: unknown) => { try { return JSON.parse(JSON.stringify(x)); } catch { return 'UNSERIALISABLE'; } };
  emit({ route: p.c.route, mode: p.m, kind: p.k, who: p.who, ...r, state: { ...state }, stmts: [...stmts],
    warnLines: logs.filter((l) => l[0] === 'warn').map((l) => safe([l[1], l[2]])), errLines: logs.filter((l) => l[0] === 'error').map((l) => safe([l[1], l[2]])),
    unhandled: [...unhandled], escaped: [...escaped], leak });
});
