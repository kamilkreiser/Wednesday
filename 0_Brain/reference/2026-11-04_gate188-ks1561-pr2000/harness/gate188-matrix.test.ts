/**
 * QA Gate 188 (KS-1561 / PR 2000) — the gate's OWN cells. Fixtures are written by the gate, not copied from the seat.
 * Every cell drives the real routers over HTTP (express on 127.0.0.1:0); only the DB, tenant manager and chain fetch are mocked.
 * The row-set mock MODELS the SQL the route sends: when a statement says `ORDER BY [d.]certified_at DESC NULLS LAST LIMIT n`,
 * the mock sorts the fixture that way and returns at most n rows (the real engine's semantics; checked separately on PG15).
 * Each cell records { path, certified, certId, documentId, count, ids } into GATE_OUT (JSON lines) for the base-vs-head diff,
 * and asserts the RULED outcome (so a cell may be RED at base by design, and RED at head where the gate found a gap).
 */
process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

import * as fs from 'fs';

const mockQueryRaw = jest.fn();
const mockGetTenantManager = jest.fn((): unknown => null);
const mockQueryWithTenantGuc = jest.fn();

jest.mock('../db', () => ({
  prisma: { $queryRaw: (...a: unknown[]) => mockQueryRaw(...a) },
  getTenantManager: () => mockGetTenantManager(),
}));
jest.mock('../middleware/auth', () => ({
  authenticate: () => (_q: unknown, _s: unknown, next: () => void) => next(),
  requireRole: () => (_q: unknown, _s: unknown, next: () => void) => next(),
}));
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
    queryWithTenantGuc: (...a: unknown[]) => mockQueryWithTenantGuc(...a),
  }),
);
jest.mock('../repositories/documentRepo', () => ({
  walkAncestors: jest.fn().mockResolvedValue({ lineage: [], truncated: false }),
  walkDescendants: jest.fn().mockResolvedValue({ descendants: [], truncated: false }),
  MAX_LINEAGE_DEPTH: 10,
  writeAnchorBlobIf: jest.fn(async () => 1),
  getDocument: jest.fn(),
}));

import express from 'express';
import { verificationRouter } from '../routes/verification';
import { verificationV2Router } from '../routes/verificationV2';

const OUT = process.env.GATE_OUT || '';
const record = (cell: string, path: string, o: Record<string, unknown>) => {
  if (OUT) fs.appendFileSync(OUT, JSON.stringify({ cell, path, ...o }) + '\n');
};

const H = '7c'.repeat(32);
const TEN_1 = 'd1000000-0000-4000-8000-000000000001';
const TEN_2 = 'd2000000-0000-4000-8000-000000000002';
const OWN_B = '0b0b0b0b-1111-4111-8111-000000000001';
const OWN_B_COLLEAGUE = '0b0b0b0b-1111-4111-8111-000000000002';
const OWN_A = '0a0a0a0a-2222-4222-8222-000000000001';
const ORG_SHARED = '05050505-3333-4333-8333-000000000001';
const PLANT = 'ZQX-PLANTED-ISSUER-A';
const LINEAGE_CERT = 'e1e1e1e1-4444-4444-8444-000000000001';
const TXB = 'b0'.repeat(32);
const TXA = 'a0'.repeat(32);
const at = (min: number) => new Date(Date.UTC(2026, 6, 15, 10, min, 0)).toISOString();

let seq = 0;
function reg(o: { who: string; owner?: string | null; org?: string | null; createdMin: number; certifiedMin?: number; certName?: string; certId?: string; tx?: string; extra?: Record<string, unknown> }) {
  seq += 1;
  const id = `${String(seq).padStart(8, '0')}-9999-4999-8999-${o.who.padEnd(12, '0').slice(0, 12).replace(/[^0-9a-f]/g, 'f')}`;
  const certified = o.certifiedMin !== undefined;
  return {
    id,
    external_id: `gate188-${o.who}`,
    title: `row ${o.who}`,
    document_type: 'DOCUMENT',
    content_hash: H,
    status: certified ? 'certified' : 'anchored',
    certification_metadata: certified
      ? { issuerName: o.certName ?? 'Issuer', issuerId: o.owner ?? null, certificationId: o.certId ?? `cert-${o.who}`, certificationType: 'verification_certificate',
          certifiedAt: at(o.certifiedMin!), blockchain: { txHash: o.tx ?? TXA, status: 'confirmed', blockHeight: 9 } }
      : { blockchain: { txHash: o.tx ?? TXB, status: 'confirmed', blockHeight: 5 } },
    metadata: {},
    created_at: at(o.createdMin),
    certified_at: certified ? at(o.certifiedMin!) : null,
    tenant_id: TEN_1,
    parent_document_id: null,
    owner_user_id: o.owner ?? null,
    issuer_organization_id: o.org ?? null,
    organization_name: certified && o.certName === PLANT ? PLANT : null,
    ...(o.extra || {}),
  };
}

/** A genuine-shaped KS-1557 lineage child (status signed, metadata.certificationId, external id doc-<ms>-<cert8>) of `parentId`, owned by the certifier. */
function lineage(parentId: string, owner: string, createdMin: number) {
  return {
    id: 'cafecafe-5555-4555-8555-000000000001',
    external_id: `doc-1752573600000-${LINEAGE_CERT.slice(0, 8)}`,
    title: 'lineage child', document_type: 'verification_certificate', content_hash: H, status: 'signed',
    certification_metadata: {}, metadata: { certificationId: LINEAGE_CERT, issuerName: 'Lineage Certifier' },
    created_at: at(createdMin), certified_at: null, tenant_id: TEN_1, parent_document_id: parentId,
    owner_user_id: owner, issuer_organization_id: null, organization_name: null,
  };
}
const lineageCertRow = (issuer: string) => ({
  id: LINEAGE_CERT, status: 'certified', document_type: 'verification_certificate', issuer_user_id: issuer,
  certified_at: new Date(at(50)), created_at: new Date(at(50)),
  certification_metadata: { certificationType: 'verification_certificate', holderId: OWN_B },
});

/** The SQL model: ORDER BY certified_at DESC NULLS LAST (stable on input order for ties) + LIMIT n. */
function asTheEngineWould(sql: string, rows: any[]): any[] {
  const m = /ORDER BY (?:d\.)?certified_at DESC NULLS LAST\s+LIMIT (\d+)/.exec(sql.replace(/\?/g, (_x) => '?'));
  const lim = /LIMIT\s+(\d+)/.exec(sql);
  if (!/certified_at DESC NULLS LAST/.test(sql)) return rows;
  const key = (r: any) => (r.certified_at ? Date.parse(r.certified_at) : -Infinity);
  const sorted = rows.map((r, i) => ({ r, i })).sort((a, b) => (key(b.r) - key(a.r)) || (a.i - b.i)).map((x) => x.r);
  const n = m ? Number(m[1]) : lim ? Number(lim[1]) : sorted.length;
  return sorted.slice(0, n);
}

/** LIMIT in a tagged template is a bound parameter: rebuild the statement with values to read it. */
function sqlWithValues(strings: TemplateStringsArray, values: unknown[]): string {
  let s = '';
  strings.forEach((part, i) => { s += part + (i < values.length ? String(values[i]) : ''); });
  return s;
}

let LOCAL: any[] = [];
let LINEAGE_ISSUER: string | null = null;
function installLocal(rows: any[], lineageIssuer: string | null = null) {
  LOCAL = rows; LINEAGE_ISSUER = lineageIssuer;
  mockQueryRaw.mockImplementation(async (strings: TemplateStringsArray, ...values: unknown[]) => {
    const sql = sqlWithValues(strings, values);
    if (/certification_metadata FROM documents WHERE id = /.test(sql)) return LINEAGE_ISSUER ? [lineageCertRow(LINEAGE_ISSUER)] : [];
    if (/SELECT content_hash FROM documents WHERE id/.test(sql)) return [{ content_hash: H }];
    if (/content_hash = /.test(sql)) return asTheEngineWould(sql, LOCAL);
    return [];
  });
}
/** Two-tenant world: `local` answers the caller's db; `byTenant` answers each other tenant through the tenant manager. */
function installTenants(local: any[], byTenant: Record<string, any[]>, registry: { tenant_id: string; created_at: string }[]) {
  installLocal(local);
  mockQueryWithTenantGuc.mockImplementation(async (_pool: any, sql: string) => {
    const t = _pool?.tenant as string;
    if (/certification_metadata FROM documents WHERE id = /.test(sql)) return { rows: [] };
    return { rows: asTheEngineWould(sql, (byTenant[t] || []).map((r) => ({ ...r, tenant_id: t }))) };
  });
  mockGetTenantManager.mockReturnValue({
    getPlatformPool: () => ({
      query: async (sql: string) => {
        let rows = registry.map((r) => ({ ...r, tenant_slug: r.tenant_id.slice(0, 2), content_hash: H, document_id: 'x', id: r.tenant_id }));
        if (/ORDER BY created_at ASC/.test(sql)) rows = [...rows].sort((a, b) => Date.parse(a.created_at) - Date.parse(b.created_at));
        if (/DISTINCT tenant_id/.test(sql)) rows = [...rows].sort((a, b) => a.tenant_id.localeCompare(b.tenant_id));
        return { rows };
      },
    }),
    getPool: (t: string) => ({ tenant: t }),
  });
}

const app = express();
app.use((req: any, _r: unknown, next: () => void) => { req.tenantId = TEN_1; next(); });
app.use(express.json());
app.use('/api/verification', verificationRouter);
app.use('/api/v2/verification', verificationV2Router);
let base = '';
let server: ReturnType<typeof app.listen>;
const realFetch = global.fetch;
beforeAll(async () => {
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  const a = server.address();
  base = `http://127.0.0.1:${typeof a === 'object' && a ? a.port : 0}`;
});
afterAll(() => { server?.close(); global.fetch = realFetch; });
beforeEach(() => {
  jest.clearAllMocks(); mockQueryRaw.mockReset(); mockQueryWithTenantGuc.mockReset();
  mockGetTenantManager.mockReset(); mockGetTenantManager.mockReturnValue(null);
  global.fetch = jest.fn().mockRejectedValue(new Error('chain down in gate')) as unknown as typeof fetch;
});

async function post(path: string, body: unknown, binary = false): Promise<{ json: any; raw: string }> {
  const res = await realFetch(`${base}${path}`, binary
    ? { method: 'POST', headers: { 'Content-Type': 'application/octet-stream' }, body: Buffer.from('gate188 bytes') }
    : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const raw = await res.text();
  expect(res.status).toBe(200);
  return { json: JSON.parse(raw), raw };
}

type Outcome = { certified: boolean; certId: string | null; documentId: string | null; raw: string; count?: number; ids?: string[] };
async function v1(cell: string, path: 'verify' | 'verify-file' | 'xtenant'): Promise<Outcome> {
  const { json, raw } = path === 'verify-file'
    ? await post('/api/verification/verify-file', null, true)
    : await post('/api/verification/verify', { contentHash: H });
  const o = { certified: Boolean(json.checks?.isCertified), certId: (json.certification?.certificationId as string) ?? null, documentId: json.documentId ?? null, raw };
  record(cell, path, { certified: o.certified, certId: o.certId, documentId: o.documentId });
  return o;
}
async function v2(cell: string): Promise<Outcome> {
  const { json, raw } = await post('/api/v2/verification/verify', { contentHash: H });
  const ids = (json.matches || []).map((m: any) => m.documentId);
  const anyCert = (json.matches || []).some((m: any) => m.checks?.isCertified || m.certification);
  const o = { certified: Boolean(json.matches?.[0]?.checks?.isCertified), certId: json.matches?.[0]?.certification?.certificationId ?? null,
    documentId: ids[0] ?? null, raw, count: json.count, ids };
  record(cell, 'v2', { certified: o.certified, certId: o.certId, documentId: o.documentId, count: json.count, ids, anyCert,
    certIds: (json.matches || []).map((m: any) => m.certification?.certificationId ?? null) });
  return o;
}

/** Run the same fixture on all four paths. `local` serves /verify, verify-file and v2; xtenant puts the same rows in another tenant. */
async function allPaths(cell: string, rows: () => any[], lineageIssuer: string | null = null) {
  installLocal(rows(), lineageIssuer); const verify = await v1(cell, 'verify');
  installLocal(rows(), lineageIssuer); const file = await v1(cell, 'verify-file');
  installLocal(rows(), lineageIssuer); const list = await v2(cell);
  installTenants([], { [TEN_2]: rows() }, [{ tenant_id: TEN_2, created_at: at(0) }]);
  const xt = await v1(cell, 'xtenant');
  return { verify, file, list, xt };
}

// ---------------------------------------------------------------------------------------------------------------- Q2
describe('G188 Q2 the ruled outcome (Seat J shape: B first, A later certifies, both org NULL, owners differ)', () => {
  const rows = () => [
    reg({ who: 'b0', owner: OWN_B, createdMin: 0 }),
    reg({ who: 'a0', owner: OWN_A, createdMin: 30, certifiedMin: 40, certName: PLANT, certId: 'cert-a-planted' }),
  ];
  it('J: every path presents B, not certified; v2 omits A entirely (count, ids, planted issuer)', async () => {
    const r = await allPaths('J', rows);
    for (const o of [r.verify, r.file, r.xt]) {
      expect(o.documentId).toBe('gate188-b0');
      expect(o.certified).toBe(false);
      expect(o.certId).toBeNull();
    }
    expect(r.list.ids).toEqual(['gate188-b0']);
    expect(r.list.count).toBe(1);
    expect(r.list.certified).toBe(false);
    for (const o of [r.verify, r.file, r.xt, r.list]) {
      expect(o.raw.includes(PLANT)).toBe(false);
      expect(o.raw.includes('cert-a-planted')).toBe(false);
      expect(o.raw.includes('gate188-a0')).toBe(false);
    }
  });
  it('J-CONTROL: the planted issuer IS visible when A holds the original (the grep instrument can fire)', async () => {
    const r = await allPaths('J-CONTROL', () => [
      reg({ who: 'b0', owner: OWN_B, createdMin: 30 }),
      reg({ who: 'a0', owner: OWN_A, createdMin: 0, certifiedMin: 40, certName: PLANT, certId: 'cert-a-planted' }),
    ]);
    const seen = { verify: r.verify.raw.includes(PLANT), file: r.file.raw.includes(PLANT), xt: r.xt.raw.includes(PLANT), v2: r.list.raw.includes(PLANT) };
    record('J-CONTROL', 'plant-visible', seen);
    for (const o of [r.verify, r.file, r.xt, r.list]) { if (!o.raw.includes(PLANT)) record('J-CONTROL', 'raw-miss', { raw: o.raw.slice(0, 1500) }); }
    // Measured: the cross-tenant answer scopes issuer/certifiedBy out (issuer null), so the planted NAME cannot fire there;
    // the planted certification ID is the instrument that can fire on all four paths.
    expect(seen).toEqual({ verify: true, file: true, xt: false, v2: true });
    for (const o of [r.verify, r.file, r.xt, r.list]) expect(o.raw.includes('cert-a-planted')).toBe(true);
  });
});

// ---------------------------------------------------------------------------------------------------------------- Q3
describe('G188 Q3 over-blocking: each must still present a certification on head', () => {
  const cases: Array<[string, () => any[], string, string | null]> = [
    ['P1-original-certifies-own', () => [reg({ who: 'b0', owner: OWN_B, createdMin: 0, certifiedMin: 10, certId: 'cert-b' }), reg({ who: 'a0', owner: OWN_A, createdMin: 30 })], 'cert-b', null],
    ['P2-same-owner-rereg', () => [reg({ who: 'b0', owner: OWN_B, createdMin: 0 }), reg({ who: 'b1', owner: OWN_B.toUpperCase(), createdMin: 30, certifiedMin: 40, certId: 'cert-b1' })], 'cert-b1', null],
    ['P3-same-org', () => [reg({ who: 'b0', owner: OWN_B, org: ORG_SHARED, createdMin: 0 }), reg({ who: 'b2', owner: OWN_B_COLLEAGUE, org: ORG_SHARED, createdMin: 30, certifiedMin: 40, certId: 'cert-b2' })], 'cert-b2', null],
    ['P5-tie-earliest', () => [reg({ who: 'b0', owner: OWN_B, createdMin: 0 }), reg({ who: 'a0', owner: OWN_A, createdMin: 0, certifiedMin: 40, certId: 'cert-a-tie' })], 'cert-a-tie', null],
    ['P6-single', () => [reg({ who: 'a0', owner: OWN_A, createdMin: 30, certifiedMin: 40, certId: 'cert-single' })], 'cert-single', null],
    ['P7-both-certified-original-wins', () => [reg({ who: 'b0', owner: OWN_B, createdMin: 0, certifiedMin: 10, certId: 'cert-b-old' }), reg({ who: 'a0', owner: OWN_A, createdMin: 30, certifiedMin: 50, certId: 'cert-a-new' })], 'cert-b-old', null],
  ];
  for (const [name, rows, want] of cases) {
    it(`${name}: certification ${want} presented on every v1 path and as v2 matches[0]`, async () => {
      const r = await allPaths(name, rows);
      for (const o of [r.verify, r.file, r.xt, r.list]) {
        expect(o.certified).toBe(true);
        expect(o.certId).toBe(want);
      }
    });
  }
  it('P4-lineage-child-of-original (certified by B\'s colleague via the KS-1557 path): presented on /verify, verify-file, v2', async () => {
    const b0 = reg({ who: 'b0', owner: OWN_B, createdMin: 0 });
    const rows = () => [ { ...b0 }, lineage(b0.id, OWN_B_COLLEAGUE, 50), reg({ who: 'a0', owner: OWN_A, createdMin: 30 }) ];
    installLocal(rows(), OWN_B_COLLEAGUE); const a = await v1('P4-lineage', 'verify');
    installLocal(rows(), OWN_B_COLLEAGUE); const f = await v1('P4-lineage', 'verify-file');
    installLocal(rows(), OWN_B_COLLEAGUE); const l = await v2('P4-lineage');
    for (const o of [a, f]) { expect(o.certified).toBe(true); expect(o.certId).toBe(LINEAGE_CERT); }
    const parsed = JSON.parse(l.raw);
    expect(parsed.matches.some((m: any) => m.certification?.certificationId === LINEAGE_CERT)).toBe(true);
  });
  it('N-lineage-child-of-LATER (A certifies its own later copy via lineage): not presented anywhere', async () => {
    const a0 = reg({ who: 'a0', owner: OWN_A, createdMin: 30 });
    const rows = () => [ reg({ who: 'b0', owner: OWN_B, createdMin: 0 }), { ...a0 }, lineage(a0.id, OWN_A, 50) ];
    installLocal(rows(), OWN_A); const a = await v1('N-lineage-later', 'verify');
    installLocal(rows(), OWN_A); const f = await v1('N-lineage-later', 'verify-file');
    installLocal(rows(), OWN_A); const l = await v2('N-lineage-later');
    for (const o of [a, f]) expect(o.certified).toBe(false);
    expect(JSON.parse(l.raw).matches.every((m: any) => !m.certification && !m.checks.isCertified)).toBe(true);
  });
});

// ---------------------------------------------------------------------------------------------------------------- probes
describe('G188 probes beyond the seat\'s table', () => {
  it('N-TRUNC: B registers first; A registers and certifies the same bytes 24 times -> the ruled outcome is still "not certified"', async () => {
    const rows = () => [
      reg({ who: 'b0', owner: OWN_B, createdMin: 0 }),
      ...Array.from({ length: 24 }, (_x, i) => reg({ who: `a${i + 1}`, owner: OWN_A, createdMin: 30 + i, certifiedMin: 100 + i, certName: PLANT, certId: `cert-a-${i + 1}` })),
    ];
    const r = await allPaths('N-TRUNC', rows);
    for (const o of [r.verify, r.file, r.xt, r.list]) {
      expect(o.raw.includes(PLANT)).toBe(false);
      expect(o.certified).toBe(false);
    }
  });
  it('N-TRUNC-23 (control): the same with 23 copies (B still inside the fetched 24) -> not certified', async () => {
    const rows = () => [
      reg({ who: 'b0', owner: OWN_B, createdMin: 0 }),
      ...Array.from({ length: 23 }, (_x, i) => reg({ who: `a${i + 1}`, owner: OWN_A, createdMin: 30 + i, certifiedMin: 100 + i, certName: PLANT, certId: `cert-a-${i + 1}` })),
    ];
    const r = await allPaths('N-TRUNC-23', rows);
    for (const o of [r.verify, r.file, r.xt, r.list]) expect(o.certified).toBe(false);
  });
  it('N-SPLIT: B (original) lives in tenant 2, A (later, certified) in the caller\'s tenant -> v1 and v2 agree on matches[0]', async () => {
    const bRows = [reg({ who: 'b0', owner: OWN_B, createdMin: 0 })];
    const aRows = [reg({ who: 'a0', owner: OWN_A, createdMin: 30, certifiedMin: 40, certId: 'cert-a-split' })];
    installTenants(aRows, { [TEN_2]: bRows }, [{ tenant_id: TEN_2, created_at: at(0) }, { tenant_id: TEN_1, created_at: at(30) }]);
    const one = await v1('N-SPLIT', 'verify');
    installTenants(aRows, { [TEN_2]: bRows }, [{ tenant_id: TEN_2, created_at: at(0) }, { tenant_id: TEN_1, created_at: at(30) }]);
    const two = await v2('N-SPLIT');
    expect(two.documentId).toBe(one.documentId);
  });
});
