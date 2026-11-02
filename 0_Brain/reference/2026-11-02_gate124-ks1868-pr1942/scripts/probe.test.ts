// @ts-nocheck
/* Gate 124 probe (PR 1942, KS-1868 originate certifications issue + recertify). NOT part of the PR.
 * REAL certificationsRouter, REAL certificationRepo (reserveCertificationRow / saveCertification / deleteCertification / getCertification),
 * REAL chargeEvents, REAL winston logger (formats run; each transport's log() captured, nothing written).
 * Replaced: ../db by a STATEFUL stand-in (documents, certification_events, charge_events, users; legacy UPDATE and the compensating DELETE applied),
 * documentRepo by a stateful lineage store, auth, notifications, events, provenance writers, @secuura/shared (the repo's shared mock helper).
 * Faults are injected RAW: at a db statement (pre = before applying, post = after applying), at a repo boundary (wrapping the real function),
 * or as the anchoring fetch rejection. One JSON line per cell to PROBE_OUT. */
/* eslint-disable */
const mockG: any = ((globalThis as any).__g124 = { fault: null, counts: {}, db: null, sql: [], anchorCalls: 0, deletes: 0 });
function mockFire(kind: string, key: string, when: string): void {
  const f = mockG.fault;
  if (!f || f.fired || f.kind !== kind || f.key !== key || f.when !== when) return;
  if ((mockG.counts[kind + ':' + key] || 0) !== f.nth) return;
  f.fired = true;
  throw f.value();
}
function mockBump(kind: string, key: string): void { mockG.counts[kind + ':' + key] = (mockG.counts[kind + ':' + key] || 0) + 1; }
function mockClassify(strings: any): string {
  const s = Array.from(strings).join('?').replace(/\s+/g, ' ').trim();
  if (/^SELECT id FROM users/.test(s)) return 'SEL users';
  if (/^SELECT \* FROM documents WHERE id/.test(s)) return 'SEL documents by id';
  if (/^INSERT INTO documents/.test(s)) return 'INS documents';
  if (/^INSERT INTO certification_events/.test(s)) return 'INS certification_events';
  if (/^INSERT INTO charge_events/.test(s)) return 'INS charge_events';
  if (/^UPDATE documents SET status = 'certified'/.test(s)) return 'UPD legacy';
  if (/^DELETE FROM documents/.test(s)) return 'DEL documents';
  if (/^SELECT \* FROM certification_events/.test(s)) return 'SEL certification_events';
  if (/^SELECT \* FROM charge_events/.test(s)) return 'SEL charge_events';
  if (/^SELECT \* FROM share_records/.test(s)) return 'SEL share_records';
  return 'other: ' + s.slice(0, 50);
}
function mockApply(key: string, v: any[]): any {
  const D = mockG.db;
  switch (key) {
    case 'SEL users': return D.users.has(v[0]) ? [{ id: v[0] }] : [];
    case 'SEL documents by id': { const r = D.documents.get(v[0]); return r && r.tenant_id === v[1] ? [{ ...r }] : []; }
    case 'INS documents': {
      const [id, tenant, title, type, hash, , status, issuer, owner, ownerDid, , certMeta, certifiedAt, expiresAt, createdAt, updatedAt] = v;
      const prev = D.documents.get(id);
      if (prev) { if (prev.tenant_id === v[16]) { prev.status = status; prev.certification_metadata = JSON.parse(certMeta); } return 1; }
      D.documents.set(id, { id, tenant_id: tenant, title, document_type: type, content_hash: hash, status, issuer_user_id: issuer, owner_user_id: owner, owner_did: ownerDid, metadata: {}, certification_metadata: JSON.parse(certMeta), certified_at: certifiedAt, expires_at: expiresAt, created_at: createdAt, updated_at: updatedAt });
      return 1;
    }
    case 'INS certification_events': D.events.push({ id: v[0], document_id: v[1], event_type: v[2], details: JSON.parse(v[5]) }); return 1;
    case 'INS charge_events': D.charges.push({ id: v[0], event_type: v[1], certification_id: v[2], tenant_id: v[4] }); return 1;
    case 'UPD legacy': { const d = D.legacy.get(v[1]); if (d && ['draft', 'pending_signature', 'anchored', 'signed'].includes(d.status)) { d.status = 'certified'; return 1; } return 0; }
    case 'DEL documents': { const r = D.documents.get(v[0]); if (r && r.tenant_id === v[1]) { D.documents.delete(v[0]); D.events = D.events.filter((e: any) => e.document_id !== v[0]); return 1; } return 0; }
    case 'SEL certification_events': return D.events.filter((r: any) => r.document_id === v[0]);
    case 'SEL charge_events': return D.charges.filter((r: any) => r.certification_id === v[0]);
    case 'SEL share_records': return [];
    default: return key.startsWith('other') ? [] : 1;
  }
}
async function mockDb(strings: any, ...values: any[]): Promise<any> {
  const key = mockClassify(strings);
  mockG.sql.push(key);
  mockBump('db', key);
  if (key === 'DEL documents') mockG.deletes++;
  mockFire('db', key, 'pre');
  const r = mockApply(key, values);
  mockFire('db', key, 'post');
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
  for (const n of ['reserveCertificationRow', 'saveCertification', 'deleteCertification', 'getCertification']) out[n] = mockWrap(n, real[n]);
  return out;
});
jest.mock('../services/chargeEvents', () => {
  const real = jest.requireActual('../services/chargeEvents');
  return { ...real, createChargeEvent: mockWrap('createChargeEvent', real.createChargeEvent) };
});
jest.mock('../repositories/documentRepo', () => {
  const save = async (record: any) => { mockG.db.derived.push({ id: record.id, parent: record.parentDocumentId, status: record.status }); return { dbId: 'x', inserted: true }; };
  return {
    getDocument: jest.fn(async (id: string) => { const d = mockG.db.legacy.get(id); return d ? JSON.parse(JSON.stringify(d)) : null; }),
    saveDocument: (...a: any[]) => mockWrap('saveDocument', save)(...a),
    updateDocument: jest.fn(async () => undefined),
    generateContentHash: jest.fn(() => 'a'.repeat(64)),
    assertNoCycle: jest.fn(async () => undefined),
    getOrganizationExternalRef: jest.fn(async () => null),
  };
});
jest.mock('../utils/notificationClient', () => ({ notifyDocumentCertified: jest.fn(async () => undefined), notifyDocumentRevoked: jest.fn(async () => undefined), notifyDocumentShared: jest.fn(async () => undefined) }));
jest.mock('../repositories/shareRepo', () => ({ createShare: jest.fn() }));
jest.mock('../repositories/lifecycleEventRepo', () => ({ createLifecycleEvent: jest.fn(), setLifecycleEventAnchor: jest.fn(), listLifecycleEvents: jest.fn() }));
jest.mock('../events', () => ({ publishEvent: jest.fn(async () => undefined), EventTypes: { CERTIFICATION_ISSUED: 'certification.issued' } }));
jest.mock('../services/threadTokenClient', () => ({ mintAndRegisterThreadToken: jest.fn(async () => ({})) }));
jest.mock('../routes/verification', () => ({ registerInPlatformRegistry: jest.fn(async () => undefined) }));
jest.mock('../services/anchorStateSync', () => ({ pollAnchorUntilConfirmed: jest.fn(async () => undefined), reconcileDocumentAnchorState: jest.fn(async (d: any) => d) }));
jest.mock('../services/provenance', () => {
  const actual = jest.requireActual('../services/provenance');
  return { ...actual, recordActionProvenance: jest.fn(async () => undefined), getCreationProvenance: jest.fn(async () => null), wasCreatedByConnector: jest.fn(async () => true) };
});
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    hasNulByte: jest.requireActual('@secuura/shared').hasNulByte,
    runWithTenantId: jest.requireActual('@secuura/shared').runWithTenantId,
    encryptField: jest.requireActual('@secuura/shared').encryptField,
    decryptField: jest.requireActual('@secuura/shared').decryptField,
    lookupHash: jest.requireActual('@secuura/shared').lookupHash,
    verifyMessageSignature: jest.fn(() => true),
  }),
);
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => { req.user = JSON.parse(String(req.headers['x-probe-user'] || '{}')); next(); },
}));

import fs from 'fs';
// eslint-disable-next-line @typescript-eslint/no-var-requires
const express = require('express');
const { logger } = require('../utils/logger');
const MESSAGE = Symbol.for('message');
const logs: any[] = [];
for (const t of logger.transports) {
  t.log = (info: any, next: () => void) => {
    let line = ''; try { line = String(info[MESSAGE]).replace(/\u001b\[[0-9;]*m/g, ''); } catch { line = 'UNPRINTABLE'; }
    let err: any; try { err = typeof info.error === 'string' ? info.error : info.error === undefined ? '<<undefined>>' : 'NONSTRING:' + typeof info.error; } catch { err = 'UNREADABLE'; }
    logs.push({ level: String(info.level).replace(/\u001b\[[0-9;]*m/g, ''), message: String(info.message), error: err, line: line.slice(0, 400) });
    next();
  };
}
const { certificationsRouter } = require('../routes/certifications');
let escaped: string[] = [];
function describe0(e: any): string { try { return 'escaped:' + (e instanceof Error ? e.constructor.name + ':' + e.message : typeof e + ':' + String(e)); } catch { return 'escaped:UNREADABLE'; } }
for (const l of certificationsRouter.stack) if (l.route) for (const h of l.route.stack) {
  const orig = h.handle;
  h.handle = function (req: any, res: any, next: any) { const p = orig(req, res, next); if (p && typeof p.catch === 'function') p.catch((e: any) => escaped.push(describe0(e))); return p; };
}
let unhandled: string[] = [];
process.on('unhandledRejection', (r: any) => { let s = 'unreadable'; try { s = String(r instanceof Error ? r.message : r); } catch { /* */ } unhandled.push(s); });

const OUT = process.env.PROBE_OUT as string;
const TENANT = 'a0000000-0000-4000-8000-000000000001';
const ISSUER = { userId: '11111111-2222-4333-8444-555555551868', role: 'ISSUER_ADMIN', verificationLevel: 'none', tenantId: TENANT, email: 'issuer.g124@example.test' };
const HOLDER = '99999999-2222-4333-8444-555555555124';
const SRC = 'doc-src-g124';
const ORIG = 'aaaaaaaa-1111-4111-8111-111111111124';

function seed(): void {
  mockG.db = { documents: new Map(), events: [] as any[], charges: [] as any[], users: new Set([HOLDER, ISSUER.userId]), legacy: new Map(), derived: [] as any[] };
  mockG.db.legacy.set(SRC, { id: SRC, type: 'DOCUMENT', status: 'draft', owner: { id: ISSUER.userId }, data: { title: 'src' }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-10-01T00:00:00Z', updatedAt: '2026-10-01T00:00:00Z' });
  mockG.db.documents.set(ORIG, { id: ORIG, tenant_id: TENANT, title: 'orig', document_type: 'professional_certification', content_hash: 'h', status: 'certified', issuer_user_id: ISSUER.userId, owner_user_id: HOLDER, owner_did: null, metadata: {},
    certification_metadata: { certificationType: 'professional_certification', certificationData: { title: 'orig' }, issuerId: ISSUER.userId, holderId: HOLDER }, certified_at: new Date('2026-01-01T00:00:00Z'), expires_at: null, created_at: new Date('2026-01-01T00:00:00Z'), updated_at: new Date('2026-01-01T00:00:00Z') });
}
function snapshot(): any {
  const D = mockG.db;
  return {
    certRows: [...D.documents.values()].filter((r: any) => r.id !== ORIG).map((r: any) => ({ type: r.document_type, status: r.status, anchoringStatus: r.certification_metadata?.blockchain?.anchoringStatus ?? null, anchorId: r.certification_metadata?.blockchain?.anchorId ?? null })),
    events: D.events.filter((e: any) => e.document_id !== ORIG).map((e: any) => e.event_type),
    charges: D.charges.map((c: any) => c.event_type),
    derivedDocs: D.derived.length,
    legacyStatus: D.legacy.get(SRC).status,
  };
}
function norm(x: any): any {
  const map = new Map<string, string>();
  const s = JSON.stringify(x ?? null).replace(/(ce_)?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}|doc-\d+-[0-9a-f]{8}|\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z/g, (m) => {
    if (m === ORIG) return 'ORIG'; if (m === HOLDER) return 'HOLDER'; if (m === ISSUER.userId) return 'ISSUER'; if (m === TENANT) return 'TENANT';
    if (!map.has(m)) map.set(m, (m.startsWith('ce_') ? 'CE' : m.startsWith('doc-') ? 'DERIVED' : /T\d/.test(m) ? 'TS' : 'ID') + map.size);
    return map.get(m) as string;
  });
  return JSON.parse(s);
}

const realFetch = globalThis.fetch;
(globalThis as any).fetch = (url: any, init: any) => {
  if (!String(url).includes('/api/anchors')) return realFetch(url, init);
  mockG.anchorCalls++;
  const f = mockG.fault;
  if (f && f.kind === 'fetch' && !f.fired) { f.fired = true; return Promise.reject(f.value()); }
  return Promise.resolve(new Response(JSON.stringify({ success: true, data: { id: 'anchor-g124' } }), { status: 202, headers: { 'content-type': 'application/json' } }));
};
const app = express();
app.use((req: any, _r: unknown, next: () => void) => { req.tenantId = TENANT; next(); });
app.use('/api/certifications', express.json(), certificationsRouter);
let base = ''; let s1: any;
beforeAll(async () => {
  process.env.ANCHORING_SERVICE_URL = 'http://anchoring.invalid:4005';
  await new Promise<void>((ok) => { s1 = app.listen(0, '127.0.0.1', () => ok()); });
  base = `http://127.0.0.1:${s1.address().port}`;
  await new Promise((r) => setTimeout(r, 50));
});
afterAll(() => { s1?.close(); (globalThis as any).fetch = realFetch; });

function revokedProxy(): object { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function msgErr(get: () => unknown): Error { const e = new Error('hidden'); Object.defineProperty(e, 'message', { get }); return e; }
const VALUES: Record<string, () => unknown> = {
  ord: () => new Error('g124 ordinary SECRETVAL'),
  str: () => 'g124 plain string SECRETSTR',
  obj: () => ({ password: 'SECRETPW', token: 'SECRETTOK' }),
  rp: () => revokedProxy(),
  tg: () => msgErr(() => { throw new Error('g124 getter threw'); }),
  grp: () => msgErr(() => revokedProxy()),
  gtj: () => msgErr(() => ({ toJSON() { throw new Error('g124 toJSON threw'); } })),
};
const UNREAD = ['rp', 'tg', 'grp', 'gtj'];
const f = (kind: string, key: string, when: string, nth = 1) => ({ kind, key, when, nth });
const LINEAGE = { parentDocumentId: SRC };
const LEGACY = { documentId: SRC };
// site -> [request body extras, env, fault]
const SITES: Record<string, { route: 'issue' | 'recertify'; body?: any; prod?: boolean; pre?: any; fault: any }> = {
  'A4 holder SELECT users pre': { route: 'issue', body: { ...LINEAGE, holderId: HOLDER }, fault: f('db', 'SEL users', 'pre') },
  'A3 reserve pre (db INSERT#1 pre)': { route: 'issue', body: LINEAGE, fault: f('db', 'INS documents', 'pre', 1) },
  'A3 reserve post (row written, then throws)': { route: 'issue', body: LINEAGE, fault: f('db', 'INS documents', 'post', 1) },
  'A3 reserve post, PROD + anchor fails': { route: 'issue', body: LINEAGE, prod: true, pre: { kind: 'fetch2' }, fault: f('db', 'INS documents', 'post', 1) },
  'A2 issue anchor fetch rejects (dev)': { route: 'issue', body: LINEAGE, fault: f('fetch', 'anchor', 'pre') },
  'A2 issue anchor fetch rejects (PROD)': { route: 'issue', body: LINEAGE, prod: true, fault: f('fetch', 'anchor', 'pre') },
  'A2 issue anchor fetch rejects (dev, legacy)': { route: 'issue', body: LEGACY, fault: f('fetch', 'anchor', 'pre') },
  'A5 PROD anchor fails + delete repo pre': { route: 'issue', body: LINEAGE, prod: true, pre: { kind: 'fetch2' }, fault: f('repo', 'deleteCertification', 'pre') },
  'A5 PROD anchor fails + DELETE applied then throws': { route: 'issue', body: LINEAGE, prod: true, pre: { kind: 'fetch2' }, fault: f('db', 'DEL documents', 'post') },
  'A3 lineage saveDocument pre': { route: 'issue', body: LINEAGE, fault: f('repo', 'saveDocument', 'pre') },
  'A3 lineage saveDocument post': { route: 'issue', body: LINEAGE, fault: f('repo', 'saveDocument', 'post') },
  'A4 legacy UPDATE pre': { route: 'issue', body: LEGACY, fault: f('db', 'UPD legacy', 'pre') },
  'A4 legacy UPDATE post': { route: 'issue', body: LEGACY, fault: f('db', 'UPD legacy', 'post') },
  'A3 charge#1 pre': { route: 'issue', body: LINEAGE, fault: f('repo', 'createChargeEvent', 'pre', 1) },
  'A3 charge#1 post': { route: 'issue', body: LINEAGE, fault: f('repo', 'createChargeEvent', 'post', 1) },
  'A3 charge#2 pre': { route: 'issue', body: LINEAGE, fault: f('repo', 'createChargeEvent', 'pre', 2) },
  'A3 charge#2 post': { route: 'issue', body: LINEAGE, fault: f('repo', 'createChargeEvent', 'post', 2) },
  'A3 charge db INSERT#1 pre (through the real chargeEvents catch)': { route: 'issue', body: LINEAGE, fault: f('db', 'INS charge_events', 'pre', 1) },
  'A1 recertify anchor fetch rejects (dev)': { route: 'recertify', fault: f('fetch', 'anchor', 'pre') },
  'A1 recertify anchor fetch rejects (PROD)': { route: 'recertify', prod: true, fault: f('fetch', 'anchor', 'pre') },
};
const CONTROLS: Record<string, any> = {
  'control issue lineage ok': { route: 'issue', body: LINEAGE }, 'control issue legacy ok': { route: 'issue', body: LEGACY }, 'control issue holderId ok': { route: 'issue', body: { ...LINEAGE, holderId: HOLDER } },
  'control recertify ok': { route: 'recertify' }, 'control PROD anchor ordinary fail, delete ok': { route: 'issue', body: LINEAGE, prod: true, fault: f('fetch', 'anchor', 'pre'), ordinaryFetch: true },
};
const cells: [string, string][] = [];
for (const c of Object.keys(CONTROLS)) cells.push([c, 'none']);
for (const s of Object.keys(SITES)) for (const v of Object.keys(VALUES)) cells.push([s, v]);
const realEnv = process.env.NODE_ENV;

describe('gate124 probe', () => {
  it.each(cells)('%s | %s', async (site, v) => {
    seed(); mockG.counts = {}; mockG.sql = []; mockG.anchorCalls = 0; mockG.deletes = 0; logs.length = 0; escaped = []; unhandled = [];
    const spec = SITES[site] || CONTROLS[site];
    if (spec.fault && SITES[site]) mockG.fault = { ...spec.fault, value: VALUES[v], fired: false };
    else if (spec.ordinaryFetch) mockG.fault = { ...spec.fault, value: () => new Error('g124 anchoring down'), fired: false };
    else mockG.fault = null;
    // 'fetch2': the anchoring fetch also fails (ordinary Error) so the PROD compensation path runs; the armed fault is elsewhere
    const realF = (globalThis as any).fetch;
    if (spec.pre?.kind === 'fetch2') (globalThis as any).fetch = (url: any, init: any) => { if (String(url).includes('/api/anchors')) { mockG.anchorCalls++; return Promise.reject(new Error('g124 anchoring down')); } return realF(url, init); };
    if (spec.prod) process.env.NODE_ENV = 'production';
    const path = spec.route === 'issue' ? '/issue' : `/${ORIG}/recertify`;
    const body = spec.route === 'issue' ? { type: 'DOCUMENT', data: { title: 'g124 cert' }, ...(spec.body || {}) } : { note: 'g124 note' };
    let status: any; let rbody: any;
    try {
      const res = await realFetch(`${base}/api/certifications${path}`, { method: 'POST', headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(ISSUER) }, body: JSON.stringify(body), signal: AbortSignal.timeout(2000) });
      status = res.status; rbody = await res.json().catch(() => ({}));
    } catch { status = 'NO ANSWER'; }
    await new Promise((r) => setTimeout(r, 30));
    process.env.NODE_ENV = realEnv;
    (globalThis as any).fetch = realF;
    const rec = { site, v, fired: mockG.fault ? mockG.fault.fired : null, status, body: norm(rbody), state: snapshot(), sql: mockG.sql, anchorCalls: mockG.anchorCalls, deletes: mockG.deletes,
      logs: norm(logs.map((l) => ({ level: l.level, message: l.message, error: l.error }))), lines: logs.map((l) => l.line), escaped, unhandled: [...unhandled] };
    fs.appendFileSync(OUT, JSON.stringify(rec) + '\n');
    mockG.fault = null;
  });
});
