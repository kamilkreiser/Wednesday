/**
 * Gate 188 ROUND 2: PostgreSQL 15 harness. Started from a COPY of Seat F 30th's pgcell template (DB seam, seed shape),
 * re-pointed at my clone and my own cluster (127.0.0.1:55488, no unix socket), and extended with my own cells:
 * the 22/23-row trigger edge with per-request query counts, 24/25 tied originals (incl. an owner-sensitive tie cut),
 * the cap ranking cells and the cap cells built to look for a head-more-permissive-than-base outcome.
 * Drives the REAL verificationRouter / verificationV2Router over HTTP; prisma.$queryRaw sends the route's own SQL to PG15.
 * VERSION names the route blobs in the clone; OUT gets one JSON line per path per cell; EXPECT=r2 asserts the ruled outcome.
 */
process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = 'postgresql://unused-by-the-seam/x';

const mockPools: Record<string, any> = {};
const mockPoolFor = (db: string) => {
  const { Pool } = require('pg');
  return (mockPools[db] ||= new Pool({ host: '127.0.0.1', port: 55488, user: 'g188', database: db, max: 2 }));
};
const mockState: { localDb: string; tm: any; sql: string[] } = { localDb: 'g_ten', tm: null, sql: [] };
const mockLog = { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() };

jest.mock('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/repo/Blockchain/Dev/services/originate/src/db', () => ({
  prisma: {
    $queryRaw: async (strings: TemplateStringsArray, ...values: unknown[]) => {
      const text = Array.from(strings).reduce((acc, s, i) => acc + s + (i < values.length ? `$${i + 1}` : ''), '');
      mockState.sql.push(text);
      return (await mockPoolFor(mockState.localDb).query(text, values)).rows;
    },
  },
  getTenantManager: () => mockState.tm,
}));
jest.mock('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/repo/Blockchain/Dev/services/originate/src/middleware/auth', () => ({
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
}));
jest.mock('@secuura/shared', () =>
  require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/repo/Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock').makeSharedMock({
    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
    queryWithTenantGuc: async (pool: any, sql: string, params: unknown[]) => { mockState.sql.push(sql); return pool.query(sql, params); },
  }),
);
jest.mock('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/repo/Blockchain/Dev/services/originate/src/repositories/documentRepo', () => ({
  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
  MAX_LINEAGE_DEPTH: 10,
  writeAnchorBlobIf: jest.fn(async () => 1),
  getDocument: jest.fn(),
}));
jest.mock('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/repo/Blockchain/Dev/services/originate/src/utils/logger', () => ({ logger: mockLog }));

import * as fs from 'fs';
import * as crypto from 'crypto';
import express from 'express';
import { verificationRouter } from '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/repo/Blockchain/Dev/services/originate/src/routes/verification';
import { verificationV2Router } from '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/repo/Blockchain/Dev/services/originate/src/routes/verificationV2';

const VERSION = process.env.VERSION || '?';
const OUT = process.env.OUT || '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000/runs_r2/unnamed.jsonl';
const EXPECT = process.env.EXPECT || '';
const FILE = Buffer.from('gate188-r2 pg15 bytes');
const H = crypto.createHash('sha256').update(FILE).digest('hex');
const CALLER = 'c0000000-0000-4000-8000-0000000000cc';
const tid = (k: number) => `20000000-0000-4000-8000-0000000000${String(k).padStart(2, '0')}`;
const dbOf = (k: number) => `g_t${String(k).padStart(2, '0')}`;
const U_A = 'aaaaaaaa-1111-4000-8000-00000000000a';
const U_B = 'bbbbbbbb-1111-4000-8000-00000000000b';
const uTie = (k: number) => `dddddddd-1111-4000-8000-0000000000${String(k).padStart(2, '0')}`;
const B_ID = 'b0188000-0000-4000-8000-0000000000b1';
const T0 = Date.parse('2026-09-01T00:00:00.000Z');
const at = (m: number) => new Date(T0 + m * 60_000).toISOString();

interface Doc { id: string; ext: string; owner: string; created: string; status: string; certifiedAt: string | null; certId?: string }
const bOrig = (over: Partial<Doc> = {}): Doc => ({ id: B_ID, ext: 'g-B-original', owner: U_B, created: at(0), status: 'anchored', certifiedAt: null, ...over });
const aCopy = (i: number, over: Partial<Doc> = {}): Doc => ({ id: `a0188000-0000-4000-8000-${String(i).padStart(12, '0')}`, ext: `g-a-${i}`, owner: U_A,
  created: at(30 + i), status: 'certified', certifiedAt: at(200 + i), certId: `gcert-a-${i}`, ...over });
const aCopies = (n: number) => Array.from({ length: n }, (_v, i) => aCopy(i + 1));
const tieOrig = (k: number, owner?: string): Doc => ({ id: `e0188000-0000-4000-8000-0000000000${String(k).padStart(2, '0')}`, ext: `g-tie-${String(k).padStart(2, '0')}`,
  owner: owner || uTie(k), created: at(0), status: 'anchored', certifiedAt: null });

async function seed(db: string, tenant: string, docs: Doc[]) {
  for (const d of docs) {
    const cm = d.certId
      ? { issuerName: 'ZQX-G188R2-ISSUER', issuerId: d.owner, certificationId: d.certId, certificationType: 'verification_certificate', certifiedAt: d.certifiedAt }
      : {};
    await mockPoolFor(db).query(
      `INSERT INTO documents (id, external_id, title, document_type, content_hash, status, certification_metadata, metadata,
                              created_at, certified_at, owner_user_id, tenant_id)
       VALUES ($1, $2, 'same bytes', 'DOCUMENT', $3, $4, $5::jsonb, '{}'::jsonb, $6, $7, $8, $9)`,
      [d.id, d.ext, H, d.status, JSON.stringify(cm), d.created, d.certifiedAt, d.owner, tenant]);
  }
}
async function registry(rows: Array<{ k: number; created: string }>) {
  const plat = mockPoolFor('g_plat');
  await plat.query('DELETE FROM platform_document_registry WHERE content_hash = $1', [H]);
  for (const r of rows) {
    await plat.query(`INSERT INTO tenants (id, name, slug) VALUES ($1, $2, $2) ON CONFLICT (id) DO NOTHING`, [tid(r.k), `g${r.k}`]);
    await plat.query(`INSERT INTO platform_document_registry (content_hash, document_id, tenant_id, tenant_slug, created_at)
                      VALUES ($1, $2, $3, $4, $5)`, [H, `reg-${r.k}`, tid(r.k), `g${r.k}`, r.created]);
  }
  mockState.tm = { getPlatformPool: () => plat, getPool: (t: string) => mockPoolFor(dbOf(Number(t.slice(-2)))) };
}
async function resetAll() {
  for (const db of ['g_ten', ...Array.from({ length: 10 }, (_v, i) => dbOf(i + 1))]) await mockPoolFor(db).query('DELETE FROM documents WHERE content_hash = $1', [H]);
  await mockPoolFor('g_plat').query('DELETE FROM platform_document_registry WHERE content_hash = $1', [H]);
  mockState.tm = null; mockState.localDb = 'g_ten'; mockState.sql = []; mockLog.warn.mockClear();
}

const app = express();
app.use((req: any, _res: unknown, next: () => void) => { req.tenantId = CALLER; next(); });
app.use(express.json());
app.use('/api/verification', verificationRouter);
app.use('/api/v2/verification', verificationV2Router);
let base = ''; let server: any;
beforeAll(async () => {
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  base = `http://127.0.0.1:${server.address().port}`;
});
afterAll(async () => { server?.close(); await resetAll(); for (const p of Object.values(mockPools)) await p.end(); });
beforeEach(async () => { await resetAll(); global.fetch = jest.fn().mockRejectedValue(new Error('chain down')) as any; });

const realFetch: typeof fetch = (globalThis as any).__realFetch || fetch;
(globalThis as any).__realFetch = realFetch;
async function post(path: string, body: any, type: string) {
  mockState.sql = []; mockLog.warn.mockClear();
  const r = await realFetch(`${base}${path}`, { method: 'POST', headers: { 'Content-Type': type }, body });
  return r.json();
}
const v1 = () => post('/api/verification/verify', JSON.stringify({ contentHash: H }), 'application/json');
const vfile = () => post('/api/verification/verify-file', FILE, 'application/octet-stream');
const v2 = () => post('/api/v2/verification/verify', JSON.stringify({ contentHash: H }), 'application/json');

function rec(cell: string, path: string, n: number | null, body: any, isV2: boolean) {
  const originalsReads = mockState.sql.filter((s) => /MIN\(e\.created_at\)/.test(s)).length;
  const rowsetReads = mockState.sql.filter((s) => /ORDER BY (d\.)?certified_at DESC NULLS LAST/.test(s)).length;
  const o = isV2
    ? { winner: (body.matches || []).map((m: any) => m.documentId), count: body.count,
        certIds: (body.matches || []).map((m: any) => m.certification?.certificationId ?? null),
        presentsCert: (body.matches || []).some((m: any) => m.certification || m.status === 'certified' || m.isCertified === true) }
    : { winner: body.documentId, isCertified: body.checks?.isCertified, certId: body.certification?.certificationId ?? null, verified: body.verified,
        presentsCert: body.checks?.isCertified === true || !!body.certification };
  fs.appendFileSync(OUT, JSON.stringify({ version: VERSION, cell, path, n, ...o, originalsReads, rowsetReads,
    warnKS1561: mockLog.warn.mock.calls.some((c) => String(c[0]).includes('KS-1561')) }) + '\n');
  return { ...o, originalsReads } as any;
}

describe(`G188r2 F1 matrix (${VERSION})`, () => {
  for (const n of [22, 23, 24, 25]) {
    it(`local paths, B + ${n} later certified copies (${n + 1} rows)`, async () => {
      await seed('g_ten', CALLER, [bOrig(), ...aCopies(n)]);
      const a = rec('F1', '/verify', n, await v1(), false);
      const b = rec('F1', 'verify-file', n, await vfile(), false);
      const c = rec('F1', 'v2-local', n, await v2(), true);
      if (EXPECT === 'r2') {
        expect([a.winner, a.isCertified, a.certId]).toEqual(['g-B-original', false, null]);
        expect([b.winner, b.isCertified, b.certId]).toEqual(['g-B-original', false, null]);
        expect([c.winner, c.count]).toEqual([['g-B-original'], 1]);
        const want = n + 1 >= 24 ? 1 : 0; // trigger only when a read returned 24 rows
        expect([a.originalsReads, b.originalsReads, c.originalsReads]).toEqual([want, want, want]);
      }
    });
    it(`cross-tenant paths, B + ${n} later certified copies in tenant 2`, async () => {
      await seed(dbOf(2), tid(2), [bOrig(), ...aCopies(n)]);
      await registry([{ k: 2, created: at(0) }]);
      const a = rec('F1', 'cross-tenant', n, await v1(), false);
      const c = rec('F1', 'v2-cross', n, await v2(), true);
      if (EXPECT === 'r2') {
        expect([a.winner, a.isCertified, a.certId]).toEqual(['g-B-original', false, null]);
        expect([c.winner, c.count]).toEqual([['g-B-original'], 1]);
      }
    });
  }
});

describe(`G188r2 bounds and edges (${VERSION})`, () => {
  for (const k of [24, 25]) {
    it(`${k} tied uncertified originals (distinct owners) + 24 later certified A copies`, async () => {
      await seed('g_ten', CALLER, [...Array.from({ length: k }, (_v, i) => tieOrig(i + 1)), ...aCopies(24)]);
      const a = rec(`TIE${k}`, '/verify', k, await v1(), false);
      const c = rec(`TIE${k}`, 'v2-local', k, await v2(), true);
      if (EXPECT === 'r2') {
        expect([a.isCertified, a.certId]).toEqual([false, null]);
        expect(c.count).toBe(24);
        expect(c.winner.every((w: string) => w.startsWith('g-tie-'))).toBe(true);
        if (k === 25) expect(c.winner).not.toContain('g-tie-25'); // first 24 by id
      }
    });
  }
  it('TIE25-OWNER-LAST: 25 tied originals, the 25th by id held by A; 24 later A copies certified (cut narrows)', async () => {
    await seed('g_ten', CALLER, [...Array.from({ length: 25 }, (_v, i) => tieOrig(i + 1, i === 24 ? U_A : undefined)), ...aCopies(24)]);
    rec('TIE25-OWNER-LAST', '/verify', 25, await v1(), false);
    rec('TIE25-OWNER-LAST', 'v2-local', 25, await v2(), true);
  });
  it('TIE25-OWNER-FIRST: 25 tied originals, the 1st by id held by A; 24 later A copies certified (same owner: P side)', async () => {
    await seed('g_ten', CALLER, [...Array.from({ length: 25 }, (_v, i) => tieOrig(i + 1, i === 0 ? U_A : undefined)), ...aCopies(24)]);
    const a = rec('TIE25-OWNER-FIRST', '/verify', 25, await v1(), false);
    if (EXPECT === 'r2') expect(a.isCertified).toBe(true);
  });
  it('OLDCERT: the original certified its own row before every later copy, 25 later copies', async () => {
    await seed('g_ten', CALLER, [bOrig({ status: 'certified', certifiedAt: at(10), certId: 'gcert-b-old' }), ...aCopies(25)]);
    const a = rec('OLDCERT', '/verify', 25, await v1(), false);
    const b = rec('OLDCERT', 'verify-file', 25, await vfile(), false);
    const c = rec('OLDCERT', 'v2-local', 25, await v2(), true);
    if (EXPECT === 'r2') { expect(a.certId).toBe('gcert-b-old'); expect(b.certId).toBe('gcert-b-old'); expect(c.certIds).toEqual(['gcert-b-old']); }
  });
  it('INSIDE: B + 3 later copies, no originals read', async () => {
    await seed('g_ten', CALLER, [bOrig(), ...aCopies(3)]);
    const a = rec('INSIDE', '/verify', 3, await v1(), false);
    if (EXPECT === 'r2') { expect([a.winner, a.isCertified, a.originalsReads]).toEqual(['g-B-original', false, 0]); }
  });
});

describe(`G188r2 v2 tenant cap (${VERSION})`, () => {
  // B (uncertified original) in tenant kB; A's later certified copy in every other tenant; registry created_at follows registration.
  const cap = async (cell: string, tenants: number, kB: number, bRegAt: number, bOver: Partial<Doc> = {}, others: (k: number) => Partial<Doc> = () => ({})) => {
    const reg: Array<{ k: number; created: string }> = [];
    for (let k = 1; k <= tenants; k++) {
      if (k === kB) { await seed(dbOf(k), tid(k), [bOrig(bOver)]); reg.push({ k, created: at(bRegAt) }); }
      else { const d = aCopy(k, others(k)); await seed(dbOf(k), tid(k), [d]); reg.push({ k, created: d.created }); }
    }
    await registry(reg);
    const c = rec(cell, 'v2-cross', tenants, await v2(), true);
    const a = rec(cell, 'cross-tenant', tenants, await v1(), false);
    return { a, c };
  };
  it('CAP-8 control', async () => { const { c } = await cap('CAP-8', 8, 8, 0); if (EXPECT === 'r2') expect([c.winner, c.count]).toEqual([['g-B-original'], 1]); });
  it('CAP-9 (B 9th by id)', async () => { const { c } = await cap('CAP-9', 9, 9, 0); if (EXPECT === 'r2') expect([c.winner, c.count]).toEqual([['g-B-original'], 1]); });
  it('CAP-10 (B 9th of 10 by id)', async () => { const { c } = await cap('CAP-10', 10, 9, 0); if (EXPECT === 'r2') expect([c.winner, c.count]).toEqual([['g-B-original'], 1]); });
  it('CAP-LATE (B 9th by id, registry row written last): stated residual', async () => { await cap('CAP-LATE', 9, 9, 500); });
  it('CAP-LATE-LOWID (B 1st by id, registry row written last): does the new rank drop what tenant_id order kept?', async () => { await cap('CAP-LATE-LOWID', 9, 1, 500); });
  it('CAP-ORIGCERT (B 9th by id, certified its own row, the 8 others UNCERTIFIED later rows)', async () => {
    await cap('CAP-ORIGCERT', 9, 9, 0, { status: 'certified', certifiedAt: at(10), certId: 'gcert-b-own' }, () => ({ status: 'anchored', certifiedAt: null, certId: undefined }));
  });
});
