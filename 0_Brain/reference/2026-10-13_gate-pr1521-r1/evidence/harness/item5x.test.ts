/**
 * Gate harness for PR #1521 (KS-1533 arm 1). Lives ONLY in the gate's scratch clone.
 * Drives the REAL security app over real HTTP (express.json, shared authenticate RS256, router).
 * Mode: GATE_DB=1 -> real local PostgreSQL (svc_api_keys read back with SQL); else in-memory store.
 * Writes every observation to GATE_OUT (JSON) so the verdict can cite it.
 */
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import crypto from 'crypto';
import fs from 'fs';
import type { Server } from 'http';
import type { AddressInfo } from 'net';

process.env.SECURITY_DISABLE_BOOT = '1';
const USE_DB = process.env.GATE_DB === '1';
if (USE_DB) process.env.DATABASE_URL = 'postgresql://gate@127.0.0.1:55434/gate';
else delete process.env.DATABASE_URL;

const TA = 'a0000000-0000-4000-8000-0000000000aa';
const TB = 'b0000000-0000-4000-8000-0000000000bb';
const A1 = '11111111-1111-4111-8111-111111111111';
const A2 = '22222222-2222-4222-8222-222222222222';
const B1 = '33333333-3333-4333-8333-333333333333';
const CONN_A1 = 'platform-s:a1-ref';
const OA = 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee';
const OB = 'abcdefab-cdef-4abc-8def-abcdefabcdef';
const CONN_A2 = 'platform-s:a2-ref';

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIV = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUB = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64u = (b: Buffer) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function tok(claims: Record<string, unknown>): string {
  const h = b64u(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const p = b64u(Buffer.from(JSON.stringify({ sub: 'gate', iat: now, exp: now + 600, ...claims })));
  const s = b64u(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), PRIV));
  return `${h}.${p}.${s}`;
}

const ROLES: Record<string, Record<string, unknown>> = {
  ADMIN: { role: 'ADMIN', tenantId: TA, organizationId: A1 },
  platform_admin: { role: 'platform_admin', tenantId: TA, organizationId: A1 },
  ORG_ADMIN: { role: 'ORG_ADMIN', tenantId: TA, organizationId: A1 },
  org_admin_lc: { role: 'org_admin', tenantId: TA, organizationId: A1 },
  ISSUER_ADMIN: { role: 'ISSUER_ADMIN', tenantId: TA, organizationId: A1 },
  orgless_issuer_admin: { role: 'issuer_admin', tenantId: TA },
  user: { role: 'user', tenantId: TA, organizationId: A1 },
  // exact shape auth's generateConnectorToken mints for a validated sk_ key (services/auth/src/services/jwt.ts:288)
  provisioner: { userId: `connector:${CONN_A1}`, email: 'connector@secuura.io', role: 'connector', organizationId: A1,
    verificationLevel: 'api_key', type: 'connector', tenantId: TA, scopes: ['organizations:register'] },
  scopeless_connector: { userId: `connector:${CONN_A1}`, role: 'connector', type: 'connector', tenantId: TA, organizationId: A1, scopes: ['documents:read'] },
  super_admin: { role: 'super_admin' },
};
const TARGETS: Record<string, Record<string, unknown>> = {
  own_org: { tenantId: TA, organizationId: A1 },
  other_org: { tenantId: TA, organizationId: A2 },
  other_tenant: { tenantId: TB, organizationId: B1 },
  orgless: { tenantId: TA },
};
const CONNECTORS: Record<string, unknown> = {
  absent: undefined, own: CONN_A1, other: CONN_A2, malformed_empty: '', malformed_case: CONN_A2.toUpperCase(),
  malformed_array: [CONN_A2], malformed_obj: { id: CONN_A2 },
};

let server: Server; let base: string; let pool: any; let mem: Map<string, any>;
const out: any = { mode: USE_DB ? 'postgres' : 'memory', cells: [], smuggle: [], orgvariants: [], race: {}, gatewayShape: [] };

async function list(t: string, org: string) {
  const r = await fetch(`${base}/api/keys?organizationId=${encodeURIComponent(org)}`, { headers: { Authorization: `Bearer ${t}` } });
  const j: any = await r.json().catch(() => null);
  return { status: r.status, ids: (j?.data ?? []).map((k: any) => k.id) as string[] };
}

async function call(t: string | null, body: unknown, extra: { query?: string; headers?: Record<string, string>; raw?: string } = {}) {
  const res = await fetch(`${base}/api/keys${extra.query ?? ''}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(t ? { Authorization: `Bearer ${t}` } : {}), ...(extra.headers ?? {}) },
    body: extra.raw ?? JSON.stringify(body),
  });
  const text = await res.text();
  let j: any = null; try { j = JSON.parse(text); } catch { /* */ }
  return { status: res.status, body: j, text };
}

/** The STORE, read back independently of the route: SQL in DB mode, the module map otherwise. */
async function rows(): Promise<Array<{ id: string; org: string | null; tenant: string; connector: string | null; active: boolean }>> {
  if (USE_DB) {
    const r = await pool.query('SELECT id, organization_id, tenant_id::text, connector_id, is_active FROM svc_api_keys');
    const sq = r.rows.map((x: any) => ({ id: x.id, org: x.organization_id, tenant: x.tenant_id, connector: x.connector_id, active: x.is_active }));
    // cross-check: the module map must agree with SQL on every row both hold (the list route reads the map)
    for (const k of mem.values()) { const q = sq.find((y: any) => y.id === k.id); if (q && ((k.organizationId ?? null) !== q.org || k.isActive !== q.active)) out.memSqlDisagree = (out.memSqlDisagree ?? 0) + 1; }
    return sq;
  }
  return [...mem.values()].map((k: any) => ({ id: k.id, org: k.organizationId ?? null, tenant: k.tenantId, connector: k.connectorId ?? null, active: k.isActive }));
}

async function seedVictim(): Promise<string> {
  const r = await call(tok(ROLES.super_admin), { name: 'victim', tenantId: TA, organizationId: A2, connectorId: CONN_A2 });
  if (r.status !== 201) throw new Error(`seed failed ${r.status} ${r.text}`);
  return r.body.data.id;
}

beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUB, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
  const mod = await import('../index');
  mem = (mod as any).memApiKeys;
  if (USE_DB) {
    const db = await import('../db');
    const ok = await (db as any).initDb();
    if (!ok || !(db as any).isDbAvailable()) throw new Error('GATE: DB mode requested but DB not available — refusing to run a memory test labelled postgres');
    const { Pool } = await import('pg');
    pool = new Pool({ connectionString: process.env.DATABASE_URL });
    await pool.query('TRUNCATE svc_api_keys');
    await pool.query('TRUNCATE organizations');
    await pool.query('INSERT INTO organizations (id, tenant_id) VALUES ($1,$2),($3,$2),($4,$2),($5,$6)', [A1, TA, A2, OA, B1, TB]);
  }
  await new Promise<void>((r) => { server = (mod as any).default.listen(0, '127.0.0.1', r); });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});

afterAll(async () => {
  fs.writeFileSync(process.env.GATE_OUT ?? '/dev/null', JSON.stringify(out, null, 1));
  await new Promise<void>((r) => server.close(() => r()));
  if (pool) await pool.end();
});

describe('item5 explicit-tenant control', () => {
  it('ADMIN / provisioner of A1 naming B1 (a TB org) with tenantId TA sent explicitly, unpadded', async () => {
    out.item5explicit = [];
    for (const rn of ['ADMIN', 'provisioner', 'ISSUER_ADMIN']) {
      const before = await rows();
      const r = await call(tok(ROLES[rn]), { name: `x ${rn}`, tenantId: TA, organizationId: B1 });
      const after = await rows();
      out.item5explicit.push({ role: rn, status: r.status, msg: r.body?.error?.message ?? null, stored: after.filter((a) => !before.some((b) => b.id === a.id)).map((a) => ({ tenant: a.tenant, org: a.org })) });
    }
    expect(out.item5explicit.length).toBe(3);
  });
});
