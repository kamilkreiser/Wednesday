/**
 * GATE 66 probe (QA, not part of the PR). Real PostgreSQL 15 behind the real vc-issuer routes.
 * '../db' is replaced by a real pg Pool (G66_DB), so READABLE_BY_CALLER, NULLIF and IS NOT DISTINCT FROM run in Postgres,
 * not in the PR's JS pgModel. Oracle: Kam's option (A) as stated in the brief, written independently below (SPEC),
 * NOT the product's own predicate.
 * FAIL condition for every cell: the route's answer (status / ids / total / revoked flag in the DB) differs from SPEC,
 * or the SQL and the JS backstop disagree (any "owner filter returned row(s) ... refuses" warning).
 */
import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import crypto from 'crypto';
import { Pool } from 'pg';
import fs from 'fs';
const out = (o: unknown) => { if (process.env.G66_OUT) fs.appendFileSync(process.env.G66_OUT, JSON.stringify(o) + '\n'); };

const pool = vi.hoisted(() => ({ p: null as any }));
const warns = vi.hoisted(() => ({ list: [] as string[] }));
vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: (sql: string, params?: unknown[]) => pool.p.query(sql, params),
}));
vi.mock('../utils/logger', () => ({
  logger: { info: () => {}, error: () => {}, debug: () => {}, warn: (m: string) => { warns.list.push(String(m)); } },
}));

const T1 = 'g66-tenant-1';
const T2 = 'g66-tenant-2';
type P = Record<string, unknown> | undefined;
const mk = (userId: string | undefined, tenantId: string | undefined, role: unknown): Record<string, unknown> => {
  const o: Record<string, unknown> = { role, email: 'x@g66.test', verificationLevel: 'BASIC' };
  if (userId !== undefined) o.userId = userId;
  if (tenantId !== undefined) o.tenantId = tenantId;
  return o;
};
const PRINCIPALS: Array<[string, P]> = [
  ['SYSTEM_ADMIN T1', mk('g66-sys', T1, 'SYSTEM_ADMIN')],
  ['SUPER_ADMIN T1', mk('g66-su', T1, 'SUPER_ADMIN')],
  ['super_admin T1', mk('g66-su', T1, 'super_admin')],
  ['Super_Admin T1 (mixed case)', mk('g66-su', T1, 'Super_Admin')],
  ['system_admin T1 (lower)', mk('g66-sys', T1, 'system_admin')],
  ['platform_admin T1 (platform_admins.role; gateway SUPER_ADMIN_ROLES has it)', mk('g66-pa', T1, 'platform_admin')],
  ['platform_viewer T1', mk('g66-pv', T1, 'platform_viewer')],
  ['" SUPER_ADMIN" T1 (leading space)', mk('g66-su', T1, ' SUPER_ADMIN')],
  ['ORG_ADMIN T1', mk('g66-oa', T1, 'ORG_ADMIN')],
  ['OWNER T1 (bob)', mk('g66-bob', T1, 'OWNER')],
  ['connector T1', mk('connector:g66', T1, 'connector')],
  ['SUPER_ADMIN no tenant (platform-admin login shape)', mk('g66-su', undefined, 'super_admin')],
  ['SUPER_ADMIN tenant "" ', mk('g66-su', '', 'SUPER_ADMIN')],
  ['SUPER_ADMIN T2', mk('g66-su', T2, 'SUPER_ADMIN')],
  ['SUPER_ADMIN tenant upper-cased T1', mk('g66-su', T1.toUpperCase(), 'SUPER_ADMIN')],
  ['SUPER_ADMIN tenant T1 + trailing space', mk('g66-su', T1 + ' ', 'SUPER_ADMIN')],
  ['SUPER_ADMIN T1, userId ""', mk('', T1, 'SUPER_ADMIN')],
  ['alice T1 (owner of A2)', mk('g66-alice', T1, 'OWNER')],
  ['tenant-less user X (owner of N8)', mk('g66-x', undefined, 'OWNER')],
  ['SUPER_ADMIN no tenant, userId g66-x (same userId as N8 owner)', mk('g66-x', undefined, 'SUPER_ADMIN')],
  ['anonymous', undefined],
];
// rows: [key, user, tenant]
const ROWS: Array<[string, string | null, string | null]> = [
  ['O1', null, T1], ['A2', 'g66-alice', T1], ['L3', null, null], ['O4', null, T2], ['E5', '', ''],
  ['E6', '', T1], ['E7', null, ''], ['N8', 'g66-x', null], ['U9', null, T1.toUpperCase()],
];
const cid = (k: string) => `https://secuura.io/credentials/g66-${k}`;
const hash = (k: string) => `g66hash-${k}`;

// ---- independent SPEC oracle (option A as briefed) ----
const str = (v: unknown) => (typeof v === 'string' && v.length > 0 ? v : null);
const PLATFORM = new Set(['SYSTEM_ADMIN', 'SUPER_ADMIN']);
const asciiUpper = (s: string) => s.replace(/[a-z]/g, (c) => c.toUpperCase());
function SPEC(p: P, ru: string | null, rt: string | null): boolean {
  if (!p) return false;
  const uid = str(p.userId); if (uid === null) return false;
  const tid = str(p.tenantId);
  const ou = str(ru), ot = str(rt);
  if (ou !== null) return ou === uid && ot === tid;
  const role = p.role;
  if (typeof role !== 'string' || !PLATFORM.has(asciiUpper(role))) return false;
  return ot !== null && tid === ot;
}

type Reply = { status: number; body: any };
let mods: any;
function dispatch(router: any, user: P, method: string, url: string, body?: unknown): Promise<Reply> {
  return new Promise((resolve, reject) => {
    const req: any = { method, url, baseUrl: '', originalUrl: url, headers: {}, body, params: {}, query: {}, user };
    const res: any = { statusCode: 200, status(c: number) { this.statusCode = c; return this; }, json(b: unknown) { resolve({ status: this.statusCode, body: b }); return this; } };
    router(req, res, (err?: unknown) => { if (err) mods.errorHandler(err, req, res, () => {}); else reject(new Error('no route')); });
  });
}
async function seed() {
  await pool.p.query('DELETE FROM vc_credentials_store');
  let i = 0;
  for (const [k, u, t] of ROWS) {
    i += 1;
    const cred = { '@context': ['https://www.w3.org/2018/credentials/v1'], id: cid(k), type: ['VerifiableCredential'], issuer: { id: 'did:prism:g66' }, issuanceDate: '2026-01-01T00:00:00Z', credentialSubject: { documentHash: hash(k) } };
    await pool.p.query(`INSERT INTO vc_credentials_store (id, credential, created_by_user_id, created_by_tenant_id, created_at) VALUES ($1,$2,$3,$4, now() - ($5 || ' seconds')::interval)`, [cid(k), JSON.stringify(cred), u, t, String(100 - i)]);
  }
}
const revokedInDb = async (k: string) => (await pool.p.query(`SELECT credential->'credentialStatus'->>'revoked' AS r FROM vc_credentials_store WHERE id=$1`, [cid(k)])).rows[0]?.r === 'true';

beforeAll(async () => {
  const { privateKey } = crypto.generateKeyPairSync('ed25519');
  process.env.VC_SIGNING_KEY = privateKey.export({ type: 'pkcs8', format: 'der' }).toString('hex');
  pool.p = new Pool({ connectionString: process.env.G66_DB });
  const who = await pool.p.query('SELECT current_user AS u, current_database() AS d');
  out({ cell: 'DB', who: who.rows[0] });
  await pool.p.query('SELECT 1 FROM vc_credentials_store LIMIT 0');
  vi.resetModules();
  const c = await import('../routes/credentials');
  const { errorHandler } = await import('../middleware/errorHandler');
  mods = { credentials: c.credentialRoutes, errorHandler };
  await seed();
}, 120_000);
afterAll(async () => { await pool.p.query('DELETE FROM vc_credentials_store'); await pool.p.end(); });
beforeEach(() => { warns.list.length = 0; });

it('R0 CONTROL: the seed is really in Postgres (9 rows) and alice reads A2 by id', async () => {
  expect((await pool.p.query('SELECT count(*)::int AS n FROM vc_credentials_store')).rows[0].n).toBe(9);
  expect((await dispatch(mods.credentials, PRINCIPALS[17][1], 'GET', `/${encodeURIComponent(cid('A2'))}`)).status).toBe(200);
});

describe('real PG: by id, by hash, list vs SPEC', () => {
  for (const [label, p] of PRINCIPALS) {
    it(`R1 ${label}`, async () => {
      const got: Record<string, unknown> = {}, want: Record<string, unknown> = {};
      for (const [k, u, t] of ROWS) {
        const s = SPEC(p, u, t);
        const r1 = await dispatch(mods.credentials, p, 'GET', `/${encodeURIComponent(cid(k))}`);
        const r2 = await dispatch(mods.credentials, p, 'GET', `/by-hash/${encodeURIComponent(hash(k))}`);
        got[`id:${k}`] = r1.status; want[`id:${k}`] = s ? 200 : 404;
        got[`hash:${k}`] = r2.status; want[`hash:${k}`] = s ? 200 : 404;
      }
      const l = await dispatch(mods.credentials, p, 'GET', '/');
      const ids = l.status === 200 ? (l.body.credentials as any[]).map((c) => c.id).sort() : [];
      got.list = ids; want.list = ROWS.filter(([, u, t]) => SPEC(p, u, t)).map(([k]) => cid(k)).sort();
      got.total = l.status === 200 ? l.body.pagination.total : null; want.total = (want.list as string[]).length;
      if (p === undefined || str((p as any).userId) === null) { want.total = 0; }
      out({ cell: 'R1', label, got, want, warns: warns.list });
      expect(got).toEqual(want);
      expect(warns.list.filter((w) => /refuses/.test(w))).toEqual([]);
    });
  }
});

describe('real PG: revoke vs SPEC, with the DB row read back', () => {
  for (const [label, p] of PRINCIPALS) {
    it(`R2 ${label}`, async () => {
      const got: Record<string, unknown> = {}, want: Record<string, unknown> = {};
      for (const [k, u, t] of ROWS) {
        await seed();
        const s = SPEC(p, u, t);
        const r = await dispatch(mods.credentials, p, 'POST', `/${encodeURIComponent(cid(k))}/revoke`, { reason: 'g66' });
        got[k] = [r.status, await revokedInDb(k)]; want[k] = s ? [200, true] : [404, false];
      }
      out({ cell: 'R2', label, got, want });
      expect(got).toEqual(want);
    });
  }
});
