// @ts-nocheck
/* Gate 105 probe (PR 1924, KS-1868 originate certifications). The REAL certificationsRouter, the REAL
 * certificationRepo and the REAL chargeEvents run; only ../db (a STATEFUL stand-in that classifies each SQL
 * statement and applies it to in-memory tables), auth, logger, notificationClient, events and documentRepo are
 * replaced. The repo / charge functions are wrapped so a fault can be injected RAW at the repo boundary, before
 * or AFTER the real call has applied its writes. Faults: repo (pre/post), db statement (pre/post), logger.info
 * throws (after the line is recorded), notify throws synchronously, anchoring fetch rejects. Each cell appends
 * one JSON line to PROBE_OUT. */
/* eslint-disable */
const mockG: any = ((globalThis as any).__g105 = { fault: null as any, counts: {} as Record<string, number>, logs: [] as any[], db: null as any, sql: [] as string[], anchorCalls: 0, notifies: [] as any[] });

function mockFire(kind: string, key: string, when: string): void {
  const f = mockG.fault;
  if (!f || f.kind !== kind || f.key !== key || f.when !== when) return;
  if ((mockG.counts[kind + ':' + key] || 0) !== f.nth) return;
  if (f.fired) return;
  f.fired = true;
  throw f.value();
}
function mockBump(kind: string, key: string): void { mockG.counts[kind + ':' + key] = (mockG.counts[kind + ':' + key] || 0) + 1; }

function mockSql(strings: TemplateStringsArray, values: any[]): any {
  const s = strings.join('?').replace(/\s+/g, ' ').trim();
  let key = 'other';
  if (/^SELECT \* FROM documents WHERE id/.test(s)) key = 'SEL documents by id';
  else if (/^SELECT \* FROM documents WHERE tenant_id/.test(s)) key = 'SEL documents list';
  else if (/^INSERT INTO documents/.test(s)) key = 'INS documents';
  else if (/^INSERT INTO certification_events/.test(s)) key = 'INS certification_events';
  else if (/^INSERT INTO share_records/.test(s)) key = 'INS share_records';
  else if (/^SELECT \* FROM share_records/.test(s)) key = 'SEL share_records';
  else if (/^SELECT \* FROM certification_events/.test(s)) key = 'SEL certification_events';
  else if (/^INSERT INTO charge_events/.test(s)) key = 'INS charge_events';
  else if (/^SELECT \* FROM charge_events/.test(s)) key = 'SEL charge_events';
  else if (/^SELECT 1/.test(s)) key = 'SELECT 1';
  else key = 'other: ' + s.slice(0, 40);
  return { key, run: () => mockApply(key, values) };
}
function mockApply(key: string, v: any[]): any {
  const D = mockG.db;
  switch (key) {
    case 'SEL documents by id': { const r = D.documents.get(v[0]); return r && r.tenant_id === v[1] ? [{ ...r }] : []; }
    case 'SEL documents list': return [...D.documents.values()].filter((r: any) => r.tenant_id === v[0]).map((r: any) => ({ ...r }));
    case 'INS documents': {
      const [id, tenant, title, type, hash, , status, issuer, owner, ownerDid, , certMeta, certifiedAt, expiresAt, createdAt, updatedAt] = v;
      const prev = D.documents.get(id);
      if (prev) { if (prev.tenant_id === v[16]) { prev.status = status; prev.certification_metadata = JSON.parse(certMeta); prev.updated_at = new Date(); } return 1; }
      D.documents.set(id, { id, tenant_id: tenant, title, document_type: type, content_hash: hash, status, issuer_user_id: issuer, owner_user_id: owner, owner_did: ownerDid, metadata: {}, certification_metadata: JSON.parse(certMeta), certified_at: certifiedAt, expires_at: expiresAt, created_at: createdAt, updated_at: updatedAt });
      return 1;
    }
    case 'INS certification_events': D.events.push({ id: v[0], document_id: v[1], event_type: v[2], actor_user_id: v[4], details: JSON.parse(v[5]), created_at: v[6] }); return 1;
    case 'INS share_records': D.shares.push({ id: v[0], document_id: v[1], to_email: v[2], to_name: v[3], share_type: v[4], shared_by_id: v[5], status: v[6], timestamp: v[7], created_at: v[8] }); return 1;
    case 'SEL share_records': return D.shares.filter((r: any) => r.document_id === v[0]);
    case 'SEL certification_events': return D.events.filter((r: any) => r.document_id === v[0]);
    case 'INS charge_events': D.charges.push({ id: v[0], event_type: v[1], certification_id: v[2], initiated_by: v[3], tenant_id: v[4], amount: v[5], currency: v[6], status: v[7], fee_status: v[8], typical_payer: v[9], metadata: JSON.parse(v[10]), created_at: v[11] }); return 1;
    case 'SEL charge_events': return D.charges.filter((r: any) => r.certification_id === v[0] && r.tenant_id === v[1]);
    default: return key.startsWith('other') ? [] : 1;
  }
}
async function mockDb(strings: TemplateStringsArray, ...values: any[]): Promise<any> {
  const c = mockSql(strings, values);
  mockG.sql.push(c.key);
  mockBump('db', c.key);
  mockFire('db', c.key, 'pre');
  const r = c.run();
  mockFire('db', c.key, 'post');
  return r;
}
jest.mock('../db', () => ({
  prisma: { $queryRaw: mockDb, $executeRaw: mockDb, $queryRawUnsafe: async () => [], $executeRawUnsafe: async () => 0, $disconnect: async () => undefined },
  withTenant: async (_t: string, fn: any) => fn({ $executeRaw: mockDb, $queryRaw: mockDb }),
  getRequestPrisma: () => ({ $queryRaw: mockDb, $executeRaw: mockDb }),
  getTenantManager: () => null,
}));
function mockWrap(name: string, real: any) {
  return async (...a: any[]) => {
    mockBump('repo', name);
    mockFire('repo', name, 'pre');
    const r = await real(...a);
    mockFire('repo', name, 'post');
    return r;
  };
}
jest.mock('../repositories/certificationRepo', () => {
  const real = jest.requireActual('../repositories/certificationRepo');
  const out: any = { ...real };
  for (const n of ['getCertification', 'saveCertification', 'listCertifications', 'saveShare', 'getSharesByCertification', 'getLineageEvents']) out[n] = mockWrap(n, real[n]);
  return out;
});
jest.mock('../services/chargeEvents', () => {
  const real = jest.requireActual('../services/chargeEvents');
  return { ...real, createChargeEvent: mockWrap('createChargeEvent', real.createChargeEvent), getChargeEventsByCertification: mockWrap('getChargeEventsByCertification', real.getChargeEventsByCertification) };
});
jest.mock('../utils/notificationClient', () => {
  const n = (name: string) => (..._a: any[]) => { mockG.notifies.push(name); mockBump('notify', name); mockFire('notify', name, 'pre'); return Promise.resolve(undefined); };
  return { notifyDocumentCertified: n('certified'), notifyDocumentRevoked: n('revoked'), notifyDocumentShared: n('shared') };
});
jest.mock('../events', () => ({ publishEvent: jest.fn(async () => undefined), EventTypes: { CERTIFICATION_ISSUED: 'certification.issued' } }));
jest.mock('../repositories/documentRepo', () => ({ getDocument: jest.fn(), saveDocument: jest.fn(async () => undefined), assertNoCycle: jest.fn(async () => undefined), generateContentHash: jest.fn(() => 'hash') }));
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _r: unknown, next: () => void) => { req.user = { userId: '11111111-2222-4333-8444-555555555555', email: 'issuer.g105@example.test', role: 'user' }; next(); },
}));
import crypto from 'crypto';
import fs from 'fs';
// eslint-disable-next-line @typescript-eslint/no-var-requires
const express = require('express');
import { certificationsRouter } from '../routes/certifications';
import { logger as realLogger } from '../utils/logger';
for (const lvl of ['info', 'warn', 'error']) {
  const orig = (realLogger as any)[lvl].bind(realLogger);
  (realLogger as any)[lvl] = (msg: string, ctx?: any) => {
    let c: any; try { c = JSON.parse(JSON.stringify(ctx ?? null)); } catch { c = '<<unserialisable>>'; }
    mockG.logs.push([lvl, msg, c]);
    return orig(msg, ctx);
  };
}

const OUT = process.env.PROBE_OUT as string;
const TENANT = 'a0000000-0000-4000-8000-0000000000aa';
const CERT = 'aaaaaaaa-1111-4111-8111-111111111111';
const USER = '11111111-2222-4333-8444-555555555555';
const HOLDER = '99999999-2222-4333-8444-555555555555';
const DATA = { title: 'G105 certificate', name: 'g105', score: 7 };
const hashOf = (d: Record<string, unknown>) => crypto.createHash('sha256').update(JSON.stringify(d, Object.keys(d).sort())).digest('hex');

function seed(): void {
  mockG.db = { documents: new Map(), events: [] as any[], shares: [] as any[], charges: [] as any[] };
  mockG.db.documents.set(CERT, {
    id: CERT, tenant_id: TENANT, title: 'G105 certificate', document_type: 'professional_certification', content_hash: hashOf(DATA), status: 'certified',
    issuer_user_id: USER, owner_user_id: HOLDER, owner_did: null, metadata: {},
    certification_metadata: { certificationType: 'professional_certification', certificationData: DATA, issuerId: USER, holderId: HOLDER, issuerName: 'issuer', holderName: 'holder' },
    certified_at: new Date('2026-01-01T00:00:00Z'), expires_at: null, created_at: new Date('2026-01-01T00:00:00Z'), updated_at: new Date('2026-01-01T00:00:00Z'),
  });
  mockG.db.charges.push({ id: 'ce_seed', event_type: 'issuance', certification_id: CERT, initiated_by: USER, tenant_id: TENANT, amount: 0, currency: 'ADA', status: 'completed', fee_status: 'free', typical_payer: null, metadata: {}, created_at: new Date('2026-01-01T00:00:00Z') });
  mockG.db.events.push({ id: 'bbbbbbbb-1111-4111-8111-111111111111', document_id: CERT, event_type: 'ISSUE', actor_user_id: USER, details: {}, created_at: new Date('2026-01-01T00:00:00Z') });
  mockG.db.shares.push({ id: 'cccccccc-1111-4111-8111-111111111111', document_id: CERT, to_email: 'seed.share@example.test', to_name: 'Seed', share_type: 'view', shared_by_id: USER, status: 'active', timestamp: new Date('2026-01-02T00:00:00Z'), created_at: new Date('2026-01-02T00:00:00Z') });
}
function snapshot(): any {
  const docs = [...mockG.db.documents.values()].map((r: any) => ({ id: r.id === CERT ? 'CERT' : 'NEW', type: r.document_type, status: r.status, revoked: !!r.certification_metadata?.revokedAt, revocationReason: r.certification_metadata?.revocationReason ?? null }));
  return {
    documents: docs, events: mockG.db.events.map((e: any) => e.event_type), shares: mockG.db.shares.map((s: any) => s.to_email),
    charges: mockG.db.charges.map((c: any) => c.event_type),
  };
}
// replace generated ids and timestamps with stable tokens (order of appearance)
function norm(x: any): any {
  const map = new Map<string, string>();
  const s = JSON.stringify(x ?? null).replace(/(ce_)?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z/g, (m) => {
    if (m === CERT) return 'CERT'; if (m === USER) return 'USER'; if (m === HOLDER) return 'HOLDER'; if (m === TENANT) return 'TENANT';
    if (m.startsWith('2026-01-0')) return m;
    if (!map.has(m)) map.set(m, (m.startsWith('ce_') ? 'CE' : /T\d/.test(m) ? 'TS' : 'ID') + map.size);
    return map.get(m) as string;
  });
  return JSON.parse(s);
}

const realFetch = globalThis.fetch;
let anchorBase = '';
const app = express();
app.use((req: any, _r: unknown, next: () => void) => { req.tenantId = TENANT; next(); });
app.use('/api/certifications', express.json(), certificationsRouter);
const anchor = express();
anchor.post('/api/anchors', (_q: any, r: any) => r.status(201).json({ data: { id: 'anchor-g105' } }));
let base = ''; let s1: any; let s2: any;
beforeAll(async () => {
  await new Promise<void>((ok) => { s1 = app.listen(0, '127.0.0.1', () => ok()); });
  await new Promise<void>((ok) => { s2 = anchor.listen(0, '127.0.0.1', () => ok()); });
  base = `http://127.0.0.1:${s1.address().port}`;
  anchorBase = `http://127.0.0.1:${s2.address().port}`;
  process.env.ANCHORING_SERVICE_URL = anchorBase;
  (globalThis as any).fetch = (url: any, init: any) => {
    if (String(url).startsWith(anchorBase)) {
      mockG.anchorCalls++;
      const f = mockG.fault;
      if (f && f.kind === 'fetch' && !f.fired) { f.fired = true; return Promise.reject(f.value()); }
    }
    return realFetch(url, init);
  };
  await new Promise((r) => setTimeout(r, 50)); // let initRepo settle
});
afterAll(() => { s1?.close(); s2?.close(); (globalThis as any).fetch = realFetch; });

const VALUES: Record<string, () => unknown> = {
  ord: () => new Error('g105 ordinary SECRETVAL'),
  str: () => 'g105 plain string',
  rp: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  msgproxy: () => Object.defineProperty(new Error('g105 hidden'), 'message', { get() { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; } }),
  msgobj: () => Object.defineProperty(new Error('g105 hidden'), 'message', { get() { return { toJSON() { throw new Error('g105 toJSON threw'); } }; } }),
  tg: () => Object.defineProperty(new Error('g105 hidden'), 'message', { get() { throw new Error('g105 message getter threw'); } }),
};
const R: Record<string, { method: string; path: string; body?: any; ctx: string }> = {
  list: { method: 'GET', path: '/', ctx: 'Failed to list certifications' },
  revoke: { method: 'POST', path: `/${CERT}/revoke`, body: { reason: 'g105 reason HOLDERSECRET' }, ctx: 'Failed to revoke certification' },
  verify: { method: 'POST', path: `/${CERT}/verify`, body: {}, ctx: 'Failed to verify certification' },
  share: { method: 'POST', path: `/${CERT}/share`, body: { recipients: [{ email: 'r1.g105@example.test', shareType: 'view' }, { email: 'r2.g105@example.test', shareType: 'verify' }] }, ctx: 'Failed to share certification' },
  recertify: { method: 'POST', path: `/${CERT}/recertify`, body: { note: 'g105 note' }, ctx: 'Failed to issue verification certificate' },
  lineage: { method: 'GET', path: `/${CERT}/lineage`, ctx: 'Failed to get lineage' },
  bundle: { method: 'GET', path: `/${CERT}/evidence-bundle`, ctx: 'Failed to generate evidence bundle' },
};
type F = { kind: string; key: string; when: string; nth: number } | null;
const f = (kind: string, key: string, when: string, nth = 1): F => ({ kind, key, when, nth });
const FAULTS: Record<string, Record<string, F>> = {
  list: { 'repo list pre': f('repo', 'listCertifications', 'pre') },
  revoke: { 'repo get pre': f('repo', 'getCertification', 'pre'), 'repo save post': f('repo', 'saveCertification', 'post') },
  verify: { 'charge post': f('repo', 'createChargeEvent', 'post') },
  share: { 'saveShare#1 post': f('repo', 'saveShare', 'post') },
  recertify: { 'repo save post': f('repo', 'saveCertification', 'post'), 'charge post': f('repo', 'createChargeEvent', 'post') },
  lineage: { 'repo get pre': f('repo', 'getCertification', 'pre') },
  bundle: { 'charge post': f('repo', 'createChargeEvent', 'post') },
};
const cells: [string, string, string][] = [];
for (const route of Object.keys(FAULTS)) for (const fault of Object.keys(FAULTS[route])) for (const v of FAULTS[route][fault] ? Object.keys(VALUES) : ['none']) cells.push([route, fault, v]);

describe('gate105 probe', () => {
  it.each(cells)('%s | %s | %s', async (route, fault, v) => {
    seed(); mockG.counts = {}; mockG.logs = []; mockG.sql = []; mockG.anchorCalls = 0; mockG.notifies = [];
    const spec = FAULTS[route][fault];
    mockG.fault = spec ? { ...spec, value: VALUES[v], fired: false } : null;
    const c = R[route];
    let status: any; let body: any; let headers: any = null;
    try {
      const res = await realFetch(`${base}/api/certifications${c.path}`, { method: c.method, headers: { 'content-type': 'application/json' }, body: c.body ? JSON.stringify(c.body) : undefined, signal: AbortSignal.timeout(1500) });
      status = res.status; headers = res.headers.get('content-disposition'); body = await res.json();
    } catch { status = 'NO ANSWER'; }
    await new Promise((r) => setTimeout(r, 30));
    const errLines = mockG.logs.filter((l: any) => l[0] === 'error');
    const rec = {
      route, fault, v, fired: mockG.fault ? mockG.fault.fired : null, status, body: norm(body), disposition: headers, state: norm(snapshot()), sql: mockG.sql, anchorCalls: mockG.anchorCalls, notifies: mockG.notifies,
      routeErr: errLines.filter((l: any) => l[1] === c.ctx).map((l: any) => l[2]), allLogs: norm(mockG.logs),
    };
    fs.appendFileSync(OUT, JSON.stringify(rec) + '\n');
    mockG.fault = null;
  });
});
