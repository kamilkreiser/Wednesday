/**
 * Gate 192 (KS-1986, PR 2004): PostgreSQL 15 harness. Uncommitted gate evidence.
 * LINEAGE: Seat F 32nd's ks1986-pg15.harness.test.ts (seam, HTTP drive, seat's ten cells re-typed here) plus the gate's own cells
 * (G-*). Drives the REAL verificationRouter / verificationV2Router over HTTP; only the DB seam is swapped (prisma.$queryRaw sends the
 * route's own tagged-template SQL as $n placeholders to PG15; tenant pools are real pg Pools, one DB per tenant; the platform pool is a
 * real Pool wrapped only to count statements). The chain (anchoring service) is global fetch, stubbed: rejected by default, or a canned
 * "verified" answer in the CHAIN cells. Records the WHOLE response body (minus verifiedAt) and headers per (cell, path); no assertions:
 * the comparison is done afterwards by ../tools/compare.py over base / head / mutant runs.
 * Own cluster: socket /private/tmp/g192/s, port 55492, listen_addresses empty. Invented ids and hashes only.
 */
process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = 'postgresql://unused-by-the-seam/x';

const SRC = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/repo/Blockchain/Dev/services/originate/src';
const mockPools: Record<string, any> = {};
const mockPoolFor = (db: string) => {
  const { Pool } = require('pg');
  return (mockPools[db] ||= new Pool({ host: '/private/tmp/g192/s', port: 55492, user: 'g192', database: db, max: 2 }));
};
const mockState: { tm: any; sql: string[] } = { tm: null, sql: [] };
const mockLog = { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() };

jest.mock('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/repo/Blockchain/Dev/services/originate/src/db', () => ({
  prisma: {
    $queryRaw: async (strings: TemplateStringsArray, ...values: unknown[]) => {
      const text = Array.from(strings).reduce((acc, s, i) => acc + s + (i < values.length ? `$${i + 1}` : ''), '');
      mockState.sql.push('LOCAL:' + text);
      return (await mockPoolFor('g_ten').query(text, values)).rows;
    },
  },
  getTenantManager: () => mockState.tm,
}));
jest.mock('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/repo/Blockchain/Dev/services/originate/src/middleware/auth', () => ({
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));
jest.mock('@secuura/shared', () =>
  require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/repo/Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock').makeSharedMock({
    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
    queryWithTenantGuc: async (pool: any, sql: string, params: unknown[]) => { mockState.sql.push('TENANT:' + (pool.__db || '?') + ':' + sql); return pool.query(sql, params); },
  }),
);
jest.mock('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/repo/Blockchain/Dev/services/originate/src/repositories/documentRepo', () => ({
  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
  MAX_LINEAGE_DEPTH: 10,
  writeAnchorBlobIf: jest.fn(async () => 1),
  getDocument: jest.fn(),
}));
jest.mock('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate192-ks1986-pr2004/repo/Blockchain/Dev/services/originate/src/utils/logger', () => ({ logger: mockLog }));

import * as fs from 'fs';
import * as crypto from 'crypto';
import express from 'express';
// eslint-disable-next-line @typescript-eslint/no-var-requires
const { verificationRouter } = require(SRC + '/routes/verification');
// eslint-disable-next-line @typescript-eslint/no-var-requires
const { verificationV2Router } = require(SRC + '/routes/verificationV2');

const VERSION = process.env.VERSION || '?';
const OUT = process.env.OUT as string;
const FILE = Buffer.from('gate192-pg15 invented file bytes');
const H = crypto.createHash('sha256').update(FILE).digest('hex');
const CALLER = 'a0000000-0000-4000-8000-0000000000aa';
const T = (n: number) => `10000000-0000-4000-8000-0000000000${String(n).padStart(2, '0')}`;
const DB: Record<string, string> = { [CALLER]: 'g_ten' };
for (let n = 2; n <= 10; n++) DB[T(n)] = `g_t${String(n).padStart(2, '0')}`;
const T2 = T(2); const T3 = T(3);
const U_A = 'aaaaaaaa-0000-4000-8000-00000000000a';
const U_B = 'bbbbbbbb-0000-4000-8000-00000000000b';
const U_Y = 'dddddddd-0000-4000-8000-00000000000d';
const U_Z = 'cccccccc-0000-4000-8000-00000000000c';
const B_ID = 'b1986000-0000-4000-8000-0000000000b1';
const B_EXT = 'doc-g192-B-original';
const CANARY_ORG_NAME = 'QQG192-CANARY-ORG-NAME';
const CANARY_TITLE = 'QQG192-CANARY-TITLE';
const CANARY_OWNER = 'eeeeeeee-0000-4000-8000-0000000c0de1';
const CANARY_ORG_UUID = 'ffffffff-0000-4000-8000-0000000c0de2';
const CANARY_ISSUER = 'QQG192-CANARY-ISSUERNAME';
const CANARIES = [CANARY_ORG_NAME, CANARY_TITLE, CANARY_OWNER, CANARY_ORG_UUID, CANARY_ISSUER];
const T0 = Date.parse('2026-08-01T00:00:00.000Z');
const at = (m: number) => new Date(T0 + m * 60_000).toISOString();

interface Doc {
  id: string; ext: string; owner: string; created: string; status: string; certifiedAt: string | null; certId?: string;
  title?: string; issuerId?: string; issuerOrg?: string | null; meta?: Record<string, unknown>; issuerName?: string;
}
const bOrig = (over: Partial<Doc> = {}): Doc => ({ id: B_ID, ext: B_EXT, owner: U_B, created: at(0), status: 'anchored', certifiedAt: null, ...over });
const certDoc = (id: string, ext: string, owner: string, createdMin: number, certMin: number, certId: string, over: Partial<Doc> = {}): Doc =>
  ({ id, ext, owner, created: at(createdMin), status: 'certified', certifiedAt: at(certMin), certId, ...over });
const aLater = (n: number, over: Partial<Doc> = {}): Doc =>
  certDoc(`a1986000-0000-4000-8000-${String(n).padStart(12, '0')}`, `doc-cert-a-${n}`, U_A, 30 + n, 120 + n, `cert-a-${n}`, over);
const yDoc = (n: number, createdMin: number, over: Partial<Doc> = {}): Doc =>
  certDoc(`d1986000-0000-4000-8000-${String(n).padStart(12, '0')}`, `doc-cert-y-${n}`, U_Y, createdMin, 200 + n, `cert-y-${n}`, over);

const plantedOrgs = new Set<string>();
async function seed(tenant: string, docs: Doc[]) {
  const pool = mockPoolFor(DB[tenant]);
  for (const d of docs) {
    if (d.issuerOrg) {
      await pool.query(`INSERT INTO organizations (id, name, slug, type) VALUES ($1, $2, $3, 'issuer') ON CONFLICT (id) DO NOTHING`,
        [d.issuerOrg, CANARY_ORG_NAME, 'qqg192-canary-org-' + d.issuerOrg.slice(-4)]);
      plantedOrgs.add(d.issuerOrg);
    }
    const cm = d.certId
      ? { issuerName: d.issuerName ?? 'G192-PLANTED-ISSUER', issuerId: d.issuerId ?? d.owner, certificationId: d.certId,
          certificationType: 'verification_certificate', certifiedAt: d.certifiedAt }
      : {};
    await pool.query(
      `INSERT INTO documents (id, external_id, title, document_type, content_hash, status, certification_metadata, metadata,
                              created_at, certified_at, owner_user_id, tenant_id, issuer_organization_id)
       VALUES ($1, $2, $3, 'DOCUMENT', $4, $5, $6::jsonb, $7::jsonb, $8, $9, $10, $11, $12)`,
      [d.id, d.ext, d.title ?? 'same bytes', H, d.status, JSON.stringify(cm), JSON.stringify(d.meta ?? {}), d.created, d.certifiedAt,
       d.owner, tenant, d.issuerOrg ?? null]);
  }
}
async function registry(rows: Array<{ tenant: string; docId: string; created: string; hash?: string }>) {
  const plat = mockPoolFor('g_plat');
  for (const r of rows) {
    await plat.query(`INSERT INTO tenants (id, name, slug) VALUES ($1, $2, $2) ON CONFLICT (id) DO NOTHING`, [r.tenant, `t-${r.tenant.slice(-2)}`]);
    await plat.query(`INSERT INTO platform_document_registry (content_hash, document_id, tenant_id, tenant_slug, created_at)
                      VALUES ($1, $2, $3, $4, $5)`, [r.hash ?? H, r.docId, r.tenant, `t-${r.tenant.slice(-2)}`, r.created]);
  }
}
function manager(opts: { platformDb?: string; downTenant?: string; throwTenant?: string } = {}) {
  const realPlat = mockPoolFor(opts.platformDb ?? 'g_plat');
  const plat = { query: (sql: string, params?: unknown[]) => { mockState.sql.push('PLAT:' + sql); return realPlat.query(sql, params); } };
  mockState.tm = {
    getPlatformPool: () => plat,
    getPool: (t: string) => {
      if (t === opts.throwTenant) throw new Error('No pool configured for tenant');
      const db = t === opts.downTenant ? 'g_nodb' : DB[t];
      const p = mockPoolFor(db);
      p.__db = db;
      return p;
    },
  };
}
async function resetAll() {
  for (const db of Object.values(DB)) {
    await mockPoolFor(db).query('DELETE FROM documents WHERE content_hash = $1', [H]);
    for (const o of plantedOrgs) await mockPoolFor(db).query('DELETE FROM organizations WHERE id = $1', [o]);
  }
  await mockPoolFor('g_plat').query('DELETE FROM platform_document_registry WHERE content_hash IN ($1, $2)', [H, 'sha256:' + H]);
  mockState.tm = null; mockState.sql = []; mockLog.warn.mockClear();
}

const app = express();
app.use((req: any, _res: unknown, next: () => void) => { req.tenantId = CALLER; next(); });
app.use(express.json());
app.use('/api/verification', verificationRouter);
app.use('/api/v2/verification', verificationV2Router);
let base = ''; let server: any;
const realFetch: typeof fetch = (globalThis as any).__realFetch || fetch;
(globalThis as any).__realFetch = realFetch;
beforeAll(async () => {
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  base = `http://127.0.0.1:${server.address().port}`;
});
afterAll(async () => { server?.close(); await resetAll(); for (const p of Object.values(mockPools)) await p.end().catch(() => undefined); });
let chainCalls = 0;
beforeEach(async () => { await resetAll(); chainCalls = 0; global.fetch = jest.fn(async () => { chainCalls++; throw new Error('chain down'); }) as any; });
function chainUp(meta: Record<string, unknown>) {
  global.fetch = jest.fn(async () => {
    chainCalls++;
    return { ok: true, json: async () => ({ verified: true, source: 'chain', network: 'preview', txHash: 'a'.repeat(64), blockNumber: 7, confirmedAt: at(1), metadata: meta }) };
  }) as any;
}

async function post(path: string, body: any, type: string) {
  const r = await realFetch(`${base}${path}`, { method: 'POST', headers: { 'Content-Type': type }, body });
  const headers: Record<string, string> = {};
  r.headers.forEach((v, k) => { if (k !== 'date' && k !== 'etag' && k !== 'content-length') headers[k] = v; });
  return { status: r.status, headers, body: await r.json() };
}
const PATHS: Array<[string, () => Promise<any>]> = [
  ['/verify', () => post('/api/verification/verify', JSON.stringify({ contentHash: H }), 'application/json')],
  ['verify-file', () => post('/api/verification/verify-file', FILE, 'application/octet-stream')],
];
const v2 = () => post('/api/v2/verification/verify', JSON.stringify({ contentHash: H }), 'application/json');

function rec(cell: string, path: string, r: any) {
  const body = { ...(r.body || {}) };
  delete body.verifiedAt;
  const text = JSON.stringify(body) + JSON.stringify(r.headers);
  const sql = mockState.sql;
  const row = {
    version: VERSION, cell, path, http: r.status, body, headers: r.headers,
    leaks: CANARIES.filter((c) => text.includes(c)),
    q: { plat: sql.filter((s) => s.startsWith('PLAT:')).length, tenant: sql.filter((s) => s.startsWith('TENANT:')).length,
         local: sql.filter((s) => s.startsWith('LOCAL:')).length,
         registryEnum: sql.filter((s) => s.startsWith('PLAT:') && /GROUP BY tenant_id, tenant_slug/.test(s)).length,
         tenantsRead: sql.filter((s) => s.startsWith('TENANT:') && /MIN\(e\.created_at\)/.test(s)).map((s) => s.split(':')[1]) },
    chainCalls,
    warnKS1986: mockLog.warn.mock.calls.filter((c) => String(c[0]).includes('KS-1986')).length,
    errors: mockLog.error.mock.calls.length,
  };
  fs.appendFileSync(OUT, JSON.stringify(row) + '\n');
  mockState.sql = []; chainCalls = 0;
  mockLog.warn.mockClear(); mockLog.error.mockClear();
}
async function both(cell: string, withV2 = true) {
  for (const [p, f] of PATHS) rec(cell, p, await f());
  if (withV2) rec(cell, 'v2', await v2());
}

describe(`gate 192 PG15 (${VERSION})`, () => {
  // ---- the seat's ten cells (F 32nd), re-typed ----
  it('S N-SPLIT', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('S-N-SPLIT');
  });
  it('S LEAK-CANARY', async () => {
    await seed(CALLER, [aLater(1)]);
    await seed(T2, [bOrig({ title: CANARY_TITLE, owner: CANARY_OWNER, issuerOrg: CANARY_ORG_UUID, meta: { issuerName: CANARY_ISSUER, issuedBy: CANARY_ISSUER } })]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('S-LEAK-CANARY');
  });
  it('S FOREIGN-ORIGINAL-CERTIFIED', async () => {
    await seed(CALLER, [aLater(1)]);
    await seed(T2, [certDoc(B_ID, B_EXT, CANARY_OWNER, 0, 5, 'cert-b-own', { title: CANARY_TITLE, issuerId: CANARY_ORG_UUID, issuerOrg: CANARY_ORG_UUID, issuerName: CANARY_ISSUER })]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('S-FOREIGN-ORIGINAL-CERTIFIED');
  });
  it('S 24-LATER-COPIES', async () => {
    await seed(CALLER, [aLater(1)]);
    await seed(T2, [bOrig(), ...Array.from({ length: 24 }, (_v, i) => yDoc(i + 1, 31 + i))]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('S-24-LATER-COPIES');
  });
  it('S ORIGINAL-LOCAL', async () => {
    await seed(CALLER, [bOrig({ ext: 'doc-B-local-original' }), aLater(1, { owner: U_B, certId: 'cert-b-later', ext: 'doc-cert-b-later' })]);
    await seed(T2, [aLater(2)]);
    await registry([{ tenant: CALLER, docId: 'doc-B-local-original', created: at(0) }, { tenant: T2, docId: 'doc-cert-a-2', created: at(32) }]); manager();
    await both('S-ORIGINAL-LOCAL');
  });
  it('S TIED-ACROSS-TENANTS', async () => {
    await seed(CALLER, [{ id: 'a1986000-0000-4000-8000-0000000000a0', ext: 'doc-local-original', owner: U_A, created: at(0), status: 'anchored', certifiedAt: null },
      certDoc('a1986000-0000-4000-8000-0000000000c1', 'doc-cert-collide', U_B, 40, 140, 'cert-collide')]);
    await seed(T2, [bOrig()]);
    await registry([{ tenant: CALLER, docId: 'doc-local-original', created: at(0) }, { tenant: T2, docId: B_EXT, created: at(0) }]); manager();
    await both('S-TIED-ACROSS-TENANTS');
  });
  it('S NO-LOCAL-ROW', async () => {
    await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }]); manager();
    await both('S-NO-LOCAL-ROW');
  });
  it('S LOOKUP-FAILURE-REGISTRY', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]);
    manager({ platformDb: 'g_nodb' });
    await both('S-LOOKUP-FAILURE-REGISTRY', false);
  });
  it('S LOOKUP-FAILURE-TENANT', async () => {
    await seed(CALLER, [{ id: 'a1986000-0000-4000-8000-0000000000e0', ext: 'doc-local-uncertified', owner: U_A, created: at(10), status: 'anchored', certifiedAt: null }, aLater(1)]);
    await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-local-uncertified', created: at(10) }]);
    manager({ downTenant: T2 });
    await both('S-LOOKUP-FAILURE-TENANT', false);
  });
  it('S SINGLE-TENANT', async () => {
    await seed(CALLER, [aLater(1)]);
    await both('S-SINGLE-TENANT', false);
  });

  // ---- the gate's own cells ----
  it('G THREE-TENANTS-TIED: originals tied in T2 (uncertified) and T3 (certified by Y); A later certified in the caller', async () => {
    await seed(CALLER, [aLater(1)]);
    await seed(T2, [bOrig({ title: CANARY_TITLE, owner: CANARY_OWNER })]);
    await seed(T3, [yDoc(1, 0, { title: CANARY_TITLE, issuerOrg: CANARY_ORG_UUID, issuerId: CANARY_ORG_UUID, issuerName: CANARY_ISSUER })]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: T3, docId: 'doc-cert-y-1', created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('G-THREE-TENANTS-TIED');
  });
  it('G CERTIFIED-AND-UNCERTIFIED-LOCAL: caller holds certified latecomer A AND an uncertified later copy Z; B original in T2', async () => {
    await seed(CALLER, [aLater(1), { id: 'a1986000-0000-4000-8000-0000000000f0', ext: 'doc-local-z', owner: U_Z, created: at(40), status: 'anchored', certifiedAt: null }]);
    await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('G-CERTIFIED-AND-UNCERTIFIED-LOCAL');
  });
  it('G REVOKED-FOREIGN-ORIGINAL: B original in T2 has status revoked; A later certified in the caller', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T2, [bOrig({ status: 'revoked' })]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('G-REVOKED-FOREIGN-ORIGINAL');
  });
  it('G ORIGINAL-UNREGISTERED: B original in T2 has NO registry row; Y (T3) certified at t20 registered; A (caller) certified at t31', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T2, [bOrig()]); await seed(T3, [yDoc(1, 20)]);
    await registry([{ tenant: T3, docId: 'doc-cert-y-1', created: at(20) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('G-ORIGINAL-UNREGISTERED');
  });
  it('G CAP-9-NATURAL: B original in T10 registered first; T2..T9 later certified copies; A in the caller (10 tenants hold the hash)', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T(10), [bOrig()]);
    for (let n = 2; n <= 9; n++) await seed(T(n), [yDoc(n, 31 + n)]);
    const reg = [{ tenant: T(10), docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }];
    for (let n = 2; n <= 9; n++) reg.push({ tenant: T(n), docId: `doc-cert-y-${n}`, created: at(31 + n) });
    await registry(reg); manager();
    await both('G-CAP-9-NATURAL');
  });
  it('G CAP-9-SKEWED: as above but B\'s registry row is the LATEST (created_at t100) and T2..T9 are certified copies at t2..t9', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T(10), [bOrig()]);
    for (let n = 2; n <= 9; n++) await seed(T(n), [yDoc(n, n)]);
    const reg = [{ tenant: T(10), docId: B_EXT, created: at(100) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }];
    for (let n = 2; n <= 9; n++) reg.push({ tenant: T(n), docId: `doc-cert-y-${n}`, created: at(n) });
    await registry(reg); manager();
    await both('G-CAP-9-SKEWED');
  });
  it('G CAP-9-SKEWED-NOCERT: B original in T10 (registry latest); T2..T9 hold UNCERTIFIED copies at t2..t9; A in the caller', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T(10), [bOrig()]);
    for (let n = 2; n <= 9; n++) await seed(T(n), [{ id: `d1986000-0000-4000-8000-${String(n).padStart(12, '0')}`, ext: `doc-y-${n}`, owner: U_Y, created: at(n), status: 'anchored', certifiedAt: null }]);
    const reg = [{ tenant: T(10), docId: B_EXT, created: at(100) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }];
    for (let n = 2; n <= 9; n++) reg.push({ tenant: T(n), docId: `doc-y-${n}`, created: at(n) });
    await registry(reg); manager();
    await both('G-CAP-9-SKEWED-NOCERT');
  });
  it('G CHAIN-UP-REGISTRY-DOWN: registry down, A certified alone in the caller; the chain answers verified with metadata naming an org', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T2, [bOrig()]);
    manager({ platformDb: 'g_nodb' });
    chainUp({ certId: 'cert-chain-x', certificationType: 'verification_certificate', issuerName: CANARY_ISSUER, issuerOrgId: CANARY_ORG_UUID, documentId: 'doc-chain-x', contentHash: H });
    await both('G-CHAIN-UP-REGISTRY-DOWN', false);
  });
  it('G CHAIN-UP-FOREIGN-ORIGINAL (registry up): A certified in caller, B original in T2; the chain answers verified', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    chainUp({ certId: 'cert-chain-x', issuerName: CANARY_ISSUER, issuerOrgId: CANARY_ORG_UUID, documentId: 'doc-chain-x', contentHash: H });
    await both('G-CHAIN-UP-FOREIGN-ORIGINAL', false);
  });
  it('G TENANT-POOL-THROWS: getPool throws for T2 (no pool configured); local uncertified original-in-tenant + certified A', async () => {
    await seed(CALLER, [{ id: 'a1986000-0000-4000-8000-0000000000e0', ext: 'doc-local-uncertified', owner: U_A, created: at(10), status: 'anchored', certifiedAt: null }, aLater(1)]);
    await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-local-uncertified', created: at(10) }]);
    manager({ throwTenant: T2 });
    await both('G-TENANT-POOL-THROWS', false);
  });
  it('G TENANT-POOL-THROWS-ALL-CERTIFIED: getPool throws for T2; A certified alone in the caller (D-B4 all-certified branch)', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]);
    manager({ throwTenant: T2 });
    await both('G-TENANT-POOL-THROWS-ALL-CERTIFIED', false);
  });
  it('G REGISTRY-PREFIXED-FORM: B original in T2 registered as sha256:<hex>; A certified in caller', async () => {
    await seed(CALLER, [aLater(1)]); await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0), hash: 'sha256:' + H }, { tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('G-REGISTRY-PREFIXED-FORM');
  });
  it('G NO-LOCAL-ROW-PREFIXED-REGISTRY (candidate c, other form): B in T2 only, registered as sha256:<hex>', async () => {
    await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0), hash: 'sha256:' + H }]); manager();
    await both('G-NO-LOCAL-ROW-PREFIXED-REGISTRY');
  });
  it('G 26-TIES-CALLER (m4 probe): 26 certified rows tied at t0 in the caller (distinct owners), B at t0 in T2; more ties than ORIGINAL_ROWS_LIMIT', async () => {
    await seed(CALLER, Array.from({ length: 26 }, (_v, i) =>
      certDoc(`a1986000-0000-4000-8001-${String(i + 1).padStart(12, '0')}`, `doc-tie-${i + 1}`, `aaaaaaaa-0000-4000-8001-${String(i + 1).padStart(12, '0')}`, 0, 100 + i, `cert-tie-${i + 1}`)));
    await seed(T2, [bOrig()]);
    await registry([{ tenant: CALLER, docId: 'doc-tie-1', created: at(0) }, { tenant: T2, docId: B_EXT, created: at(0) }]); manager();
    await both('G-26-TIES-CALLER');
  });
  it('G 26-TIES-CALLER-LATE (m4 probe): 26 certified rows tied at t5 in the caller, B original at t0 in T2', async () => {
    await seed(CALLER, Array.from({ length: 26 }, (_v, i) =>
      certDoc(`a1986000-0000-4000-8001-${String(i + 1).padStart(12, '0')}`, `doc-tie-${i + 1}`, `aaaaaaaa-0000-4000-8001-${String(i + 1).padStart(12, '0')}`, 5, 100 + i, `cert-tie-${i + 1}`)));
    await seed(T2, [bOrig()]);
    await registry([{ tenant: T2, docId: B_EXT, created: at(0) }, { tenant: CALLER, docId: 'doc-tie-1', created: at(5) }]); manager();
    await both('G-26-TIES-CALLER-LATE');
  });
  it('G CONTROL-LOCAL-CANARY: the canaries planted on the CALLER\'s own row (same tenant: not scoped) must be found by the search', async () => {
    await seed(CALLER, [aLater(1, { title: CANARY_TITLE, issuerOrg: CANARY_ORG_UUID, issuerId: CANARY_ORG_UUID, issuerName: CANARY_ISSUER })]);
    await registry([{ tenant: CALLER, docId: 'doc-cert-a-1', created: at(31) }]); manager();
    await both('G-CONTROL-LOCAL-CANARY', false);
  });
  it('G CONTROL-NO-LOCAL-CHAIN-UP: no rows anywhere; the chain answers (base behaviour of the chain branch, for the leak search)', async () => {
    manager();
    chainUp({ certId: 'cert-chain-x', issuerName: CANARY_ISSUER, issuerOrgId: CANARY_ORG_UUID, documentId: 'doc-chain-x', contentHash: H });
    await both('G-CONTROL-NO-LOCAL-CHAIN-UP', false);
  });
});
