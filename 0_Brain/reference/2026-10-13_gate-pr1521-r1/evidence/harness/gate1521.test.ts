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

describe('gate #1521', () => {
  it('controls: the store instrument sees a write, and no-token is 401', async () => {
    const before = (await rows()).length;
    const v = await seedVictim();
    const after = await rows();
    expect(after.length, 'read-back instrument must see a platform mint').toBe(before + 1);
    expect(after.find((x) => x.id === v)?.connector).toBe(CONN_A2);
    const n = await call(null, { name: 'x', tenantId: TA });
    expect(n.status).toBe(401);
    out.controls = { seededVisible: true, noToken: n.status };
  });

  it('matrix: role x target x connectorId x rotate', async () => {
    for (const [rn, claims] of Object.entries(ROLES)) {
      for (const [tn, tgt] of Object.entries(TARGETS)) {
        for (const [cn, cid] of Object.entries(CONNECTORS)) {
          for (const rotate of [false, true]) {
            const victim = await seedVictim();
            const before = await rows();
            const body: any = { name: `m ${rn} ${tn} ${cn} ${rotate}`, scopes: ['documents:read'], ...tgt, rotate };
            if (cid !== undefined) body.connectorId = cid;
            const r = await call(tok(claims), body);
            const after = await rows();
            const added = after.filter((a) => !before.some((b) => b.id === a.id));
            const newlyInactive = after.filter((a) => a.active === false && before.find((b) => b.id === a.id)?.active === true);
            out.cells.push({ role: rn, target: tn, connector: cn, rotate, status: r.status,
              msg: r.body?.error?.message ?? null, added: added.map((a) => ({ org: a.org, tenant: a.tenant, connector: a.connector })),
              victimActive: after.find((a) => a.id === victim)?.active, retired: newlyInactive.length,
              retiredOrgs: [...new Set(newlyInactive.map((a) => a.org))] });
            // invariant: a non-2xx writes nothing and retires nothing
            if (r.status >= 300) {
              expect(added.length, `${rn}/${tn}/${cn}/${rotate}: refused but wrote`).toBe(0);
              expect(newlyInactive.length, `${rn}/${tn}/${cn}/${rotate}: refused but retired`).toBe(0);
            }
          }
        }
      }
    }
  }, 300_000);

  it('smuggling shapes for an ISSUER_ADMIN of A1 against connector A2 with rotate', async () => {
    const t = tok(ROLES.ISSUER_ADMIN);
    const shapes: Array<[string, any, any]> = [
      ['query', { name: 's', tenantId: TA, organizationId: A1 }, { query: `?connectorId=${encodeURIComponent(CONN_A2)}&rotate=true` }],
      ['header x-connector-id', { name: 's', tenantId: TA, organizationId: A1, rotate: true }, { headers: { 'x-connector-id': CONN_A2 } }],
      ['body ConnectorId', { name: 's', tenantId: TA, organizationId: A1, ConnectorId: CONN_A2, rotate: true }, {}],
      ['body connectorid', { name: 's', tenantId: TA, organizationId: A1, connectorid: CONN_A2, rotate: true }, {}],
      ['body connector_id', { name: 's', tenantId: TA, organizationId: A1, connector_id: CONN_A2, rotate: true }, {}],
      ['body " connectorId"', { name: 's', tenantId: TA, organizationId: A1, ' connectorId': CONN_A2, rotate: true }, {}],
      ['__proto__ key', null, { raw: `{"name":"s","tenantId":"${TA}","organizationId":"${A1}","rotate":true,"__proto__":{"connectorId":"${CONN_A2}"}}` }],
      ['constructor.prototype', null, { raw: `{"name":"s","tenantId":"${TA}","organizationId":"${A1}","rotate":true,"constructor":{"prototype":{"connectorId":"${CONN_A2}"}}}` }],
      ['duplicate key (own then other)', null, { raw: `{"name":"s","tenantId":"${TA}","organizationId":"${A1}","rotate":true,"connectorId":"${CONN_A1}","connectorId":"${CONN_A2}"}` }],
      ['connectorId null', { name: 's', tenantId: TA, organizationId: A1, connectorId: null, rotate: true }, {}],
      ['connectorId whitespace', { name: 's', tenantId: TA, organizationId: A1, connectorId: '   ', rotate: true }, {}],
      ['connectorId trailing space', { name: 's', tenantId: TA, organizationId: A1, connectorId: `${CONN_A2} `, rotate: true }, {}],
      ['rotate "true" string', { name: 's', tenantId: TA, organizationId: A1, connectorId: CONN_A2, rotate: 'true' }, {}],
      ['nested data wrapper', { name: 's', tenantId: TA, organizationId: A1, data: { connectorId: CONN_A2, rotate: true } }, {}],
      ['x-tenant-id header other tenant, no body tenant', { name: 's', organizationId: A1 }, { headers: { 'x-tenant-id': TB } }],
      ['urlencoded body', null, { raw: `name=s&tenantId=${TA}&connectorId=${CONN_A2}&rotate=true`, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }],
    ];
    for (const [label, body, extra] of shapes) {
      const victim = await seedVictim();
      const before = await rows();
      const r = await call(t, body, extra);
      const after = await rows();
      const added = after.filter((a) => !before.some((b) => b.id === a.id));
      out.smuggle.push({ label, status: r.status, msg: r.body?.error?.message ?? null,
        victimActive: after.find((a) => a.id === victim)?.active, added: added.map((a) => ({ org: a.org, tenant: a.tenant, connector: a.connector })) });
      expect(after.find((a) => a.id === victim)?.active, `${label}: victim retired`).toBe(true);
      expect(added.every((a) => a.connector === null), `${label}: stored a connectorId`).toBe(true);
    }
  });

  it('organizationId variants for an ISSUER_ADMIN of A1', async () => {
    const t = tok(ROLES.ISSUER_ADMIN);
    const vs: Record<string, unknown> = { A2_upper: A2.toUpperCase(), A2_padded: ` ${A2} `, empty: '', spaces: '   ', A1_upper: A1.toUpperCase(),
      A1_padded: ` ${A1} `, A1_tab: `\t${A1}`, not_uuid: 'org-b', number: 7, array: [A1] };
    for (const [label, org] of Object.entries(vs)) {
      const before = await rows();
      const r = await call(t, { name: 'o', tenantId: TA, organizationId: org });
      const after = await rows();
      const added = after.filter((a) => !before.some((b) => b.id === a.id));
      out.orgvariants.push({ label, sent: org, status: r.status, msg: r.body?.error?.message ?? null, storedOrg: added.map((a) => a.org) });
    }
  });

  it('organisation CASE variants with hex-letter ids (the digit-only ids above cannot test case)', async () => {
    const t = tok({ role: 'ISSUER_ADMIN', tenantId: TA, organizationId: OA });
    const vs: Record<string, string> = { own_upper: OA.toUpperCase(), other_upper: OB.toUpperCase(), other_lower: OB, own_lower: OA };
    out.orgcase = [];
    for (const [label, org] of Object.entries(vs)) {
      if (label.endsWith('upper')) expect(org, 'control: the variant really differs in case').not.toBe(org.toLowerCase());
      const before = await rows();
      const r = await call(t, { name: 'c', tenantId: TA, organizationId: org });
      const after = await rows();
      const added = after.filter((a) => !before.some((b) => b.id === a.id));
      out.orgcase.push({ label, sent: org, status: r.status, msg: r.body?.error?.message ?? null, storedOrg: added.map((a) => a.org) });
    }
  });

  it('race: 20 concurrent platform rotates on one connector leave >=1 active key', async () => {
    const C = 'platform-s:race-ref';
    const first = await call(tok(ROLES.super_admin), { name: 'r0', tenantId: TA, organizationId: A2, connectorId: C });
    expect(first.status).toBe(201);
    const N = 20;
    const rs = await Promise.all(Array.from({ length: N }, (_, i) =>
      call(tok(ROLES.super_admin), { name: `r${i + 1}`, tenantId: TA, organizationId: A2, connectorId: C, rotate: true })));
    const after = (await rows()).filter((a) => a.connector === C);
    out.race = { n: N, statuses: [...new Set(rs.map((r) => r.status))], keysOnConnector: after.length,
      activeOnConnector: after.filter((a) => a.active).length, priorKeysRevoked: rs.map((r) => r.body?.data?.priorKeysRevoked) };
  });

  it('race CONTROL: 20 SEQUENTIAL platform rotates on one connector', async () => {
    const C = 'platform-s:seq-ref';
    const first = await call(tok(ROLES.super_admin), { name: 's0', tenantId: TA, organizationId: A2, connectorId: C });
    expect(first.status).toBe(201);
    const pr: unknown[] = [];
    for (let i = 0; i < 20; i++) {
      const r = await call(tok(ROLES.super_admin), { name: `s${i + 1}`, tenantId: TA, organizationId: A2, connectorId: C, rotate: true });
      pr.push(r.body?.data?.priorKeysRevoked);
    }
    const after = (await rows()).filter((a) => a.connector === C);
    out.raceSeq = { keysOnConnector: after.length, activeOnConnector: after.filter((a) => a.active).length, priorKeysRevoked: pr };
  });

  it('race N=2: a double-submitted rotate, 10 trials', async () => {
    const res: number[] = [];
    for (let t = 0; t < 10; t++) {
      const C = `platform-s:pair-${t}`;
      await call(tok(ROLES.super_admin), { name: 'p0', tenantId: TA, organizationId: A2, connectorId: C });
      await Promise.all([1, 2].map((i) => call(tok(ROLES.super_admin), { name: `p${i}`, tenantId: TA, organizationId: A2, connectorId: C, rotate: true })));
      res.push((await rows()).filter((a) => a.connector === C && a.active).length);
    }
    out.racePair = res;
  });

  it('race: attacker rotate concurrent with a legitimate provisioner rotate', async () => {
    const C = 'platform-s:race2-ref';
    await call(tok(ROLES.super_admin), { name: 'v', tenantId: TA, organizationId: A2, connectorId: C });
    const [atk, legit] = await Promise.all([
      call(tok(ROLES.ISSUER_ADMIN), { name: 'atk', tenantId: TA, organizationId: A1, connectorId: C, rotate: true }),
      call(tok(ROLES.super_admin), { name: 'legit', tenantId: TA, organizationId: A2, connectorId: C, rotate: true }),
    ]);
    const after = (await rows()).filter((a) => a.connector === C);
    out.race2 = { atk: atk.status, legit: legit.status, active: after.filter((a) => a.active).length, total: after.length };
    expect(atk.status).toBe(403);
  });
  it('R1 battery: every non-platform role x every rotate shape against connector A2 (victim must stay active)', async () => {
    out.rotshapes = [];
    const R: Array<[string, (b: any) => [any, any]]> = [
      ['rotate true', (b) => [{ ...b, rotate: true }, {}]],
      ['rotate "true"', (b) => [{ ...b, rotate: 'true' }, {}]],
      ['rotate 1', (b) => [{ ...b, rotate: 1 }, {}]],
      ['rotate "1"', (b) => [{ ...b, rotate: '1' }, {}]],
      ['rotate [true]', (b) => [{ ...b, rotate: [true] }, {}]],
      ['rotate {}', (b) => [{ ...b, rotate: {} }, {}]],
      ['rotate null', (b) => [{ ...b, rotate: null }, {}]],
      ['query ?rotate=true', (b) => [b, { query: '?rotate=true' }]],
      ['header x-rotate', (b) => [b, { headers: { 'x-rotate': 'true' } }]],
      ['body Rotate', (b) => [{ ...b, Rotate: true }, {}]],
      ['nested data.rotate', (b) => [{ ...b, data: { rotate: true } }, {}]],
      ['dup key false,true', (b) => [null, { raw: JSON.stringify(b).slice(0, -1) + ',"rotate":false,"rotate":true}' }]],
      ['dup key true,false', (b) => [null, { raw: JSON.stringify(b).slice(0, -1) + ',"rotate":true,"rotate":false}' }]],
      ['__proto__.rotate', (b) => [null, { raw: JSON.stringify(b).slice(0, -1) + ',"__proto__":{"rotate":true}}' }]],
      ['constructor.prototype.rotate', (b) => [null, { raw: JSON.stringify(b).slice(0, -1) + ',"constructor":{"prototype":{"rotate":true}}}' }]],
      ['rotate true + connectorId trailing space', (b) => [{ ...b, connectorId: `${CONN_A2} `, rotate: true }, {}]],
      ['rotate true + connectorId upper', (b) => [{ ...b, connectorId: CONN_A2.toUpperCase(), rotate: true }, {}]],
      ['rotate true + connectorId empty', (b) => [{ ...b, connectorId: '', rotate: true }, {}]],
      ['rotate true + connectorId in query only', (b) => { const { connectorId, ...rest } = b; void connectorId; return [{ ...rest, rotate: true }, { query: `?connectorId=${encodeURIComponent(CONN_A2)}` }]; }],
    ];
    const orgs: Record<string, Record<string, unknown>> = { own: { tenantId: TA, organizationId: A1 }, victim: { tenantId: TA, organizationId: A2 }, none: { tenantId: TA } };
    for (const rn of ['provisioner', 'ADMIN', 'ORG_ADMIN', 'org_admin_lc', 'ISSUER_ADMIN', 'orgless_issuer_admin', 'platform_admin', 'user', 'scopeless_connector']) {
      for (const [on, op] of Object.entries(orgs)) {
        for (const [label, mk] of R) {
          const victim = await seedVictim();
          const before = await rows();
          const [body, extra] = mk({ name: `rs ${rn} ${label}`, ...op, connectorId: CONN_A2 });
          const r = await call(tok(ROLES[rn]), body, extra);
          const after = await rows();
          const added = after.filter((a) => !before.some((b) => b.id === a.id));
          const newlyInactive = after.filter((a) => a.active === false && before.find((b) => b.id === a.id)?.active === true);
          out.rotshapes.push({ role: rn, org: on, label, status: r.status, msg: r.body?.error?.message ?? null,
            victimActive: after.find((a) => a.id === victim)?.active, retired: newlyInactive.length,
            added: added.map((a) => ({ org: a.org, connector: a.connector })), priorKeysRevoked: r.body?.data?.priorKeysRevoked });
          expect(after.find((a) => a.id === victim)?.active, `${rn}/${on}/${label}: victim retired`).toBe(true);
          expect(newlyInactive.length, `${rn}/${on}/${label}: something retired`).toBe(0);
        }
      }
    }
  }, 300_000);

  it('PLATFORM rotate CONTROL (the battery above must be able to see a retirement)', async () => {
    const victim = await seedVictim();
    const r = await call(tok(ROLES.super_admin), { name: 'ctl', tenantId: TA, organizationId: A2, connectorId: CONN_A2, rotate: true });
    const after = await rows();
    out.platformRotateControl = { status: r.status, victimActive: after.find((a) => a.id === victim)?.active, priorKeysRevoked: r.body?.data?.priorKeysRevoked };
    expect(r.status).toBe(201);
    expect(after.find((a) => a.id === victim)?.active, 'control: a platform rotate must retire the victim').toBe(false);
  });

  it('m1 battery: stored form per caller x organisation variant, and what GET /api/keys lists', async () => {
    out.m1 = [];
    const callers: Record<string, Record<string, unknown>> = {
      super_admin: ROLES.super_admin,
      ISSUER_ADMIN_OA: { role: 'ISSUER_ADMIN', tenantId: TA, organizationId: OA },
      ISSUER_ADMIN_OA_upperclaim: { role: 'ISSUER_ADMIN', tenantId: TA, organizationId: OA.toUpperCase() },
      ADMIN_OA: { role: 'ADMIN', tenantId: TA, organizationId: OA },
      provisioner_OA: { role: 'connector', type: 'connector', tenantId: TA, organizationId: OA, scopes: ['organizations:register'] },
      orgless_issuer_admin: ROLES.orgless_issuer_admin,
    };
    const vs: Record<string, string> = { canonical: OA, upper: OA.toUpperCase(), padded_upper: `  ${OA.toUpperCase()} `, tab: `\t${OA}`,
      nbsp: ` ${OA}`, zwsp: `​${OA}`, empty: '', spaces: '   ', tabnl: '\t\n', braces: `{${OA}}`, nohyphen: OA.replace(/-/g, ''),
      foreign_upper: OB.toUpperCase(), foreign_padded: ` ${OB} ` };
    expect(OA.toUpperCase(), 'control: OA has letters').not.toBe(OA);
    for (const [cn, claims] of Object.entries(callers)) {
      for (const [vn, v] of Object.entries(vs)) {
        const before = await rows();
        const r = await call(tok(claims), { name: `m1 ${cn} ${vn}`, tenantId: TA, organizationId: v });
        const after = await rows();
        const added = after.filter((a) => !before.some((b) => b.id === a.id));
        const id = r.body?.data?.id ?? null;
        const viaCanonical = id ? (await list(tok(ROLES.super_admin), OA)).ids.includes(id) : null;
        const viaUpper = id ? (await list(tok(ROLES.super_admin), OA.toUpperCase())).ids.includes(id) : null;
        const viaSent = id ? (await list(tok(ROLES.super_admin), v)).ids.includes(id) : null;
        const memOrg = id ? (mem.get(id)?.organizationId ?? null) : null;
        out.m1.push({ caller: cn, variant: vn, sent: v, status: r.status, msg: r.body?.error?.message ?? null,
          stored: added.map((a) => a.org), memOrg, listedCanonical: viaCanonical, listedUpper: viaUpper, listedAsSent: viaSent });
      }
    }
    // the org's own admin listing (non-platform list path) with the canonical and upper query
    const own = tok(callers.ISSUER_ADMIN_OA);
    out.m1list = { ownCanonical: (await list(own, OA)), ownUpper: (await list(own, OA.toUpperCase())), ownPadded: (await list(own, ` ${OA} `)) };
  }, 300_000);

  it('item 5: tenant resolved from the RAW organisation id when no tenant is sent', async () => {
    out.item5 = [];
    const callers: Record<string, Record<string, unknown>> = {
      ISSUER_ADMIN_A1: ROLES.ISSUER_ADMIN, ADMIN_A1: ROLES.ADMIN, ORG_ADMIN_A1: ROLES.ORG_ADMIN, provisioner_A1: ROLES.provisioner,
      orgless_issuer_admin: ROLES.orgless_issuer_admin, super_admin: ROLES.super_admin,
    };
    const U = '99999999-9999-4999-8999-999999999999';
    const vs: Record<string, string> = { B1: B1, B1_upper: B1.toUpperCase(), B1_padded: ` ${B1} `, B1_braces: `{${B1}}`, B1_nohyphen: B1.replace(/-/g, ''),
      A1: A1, A1_padded: ` ${A1} `, A1_braces: `{${A1}}`, OA_upper: OA.toUpperCase(), OA_padded: ` ${OA.toUpperCase()} `, unknown: U };
    for (const [cn, claims] of Object.entries(callers)) {
      for (const [vn, v] of Object.entries(vs)) {
        const before = await rows();
        const r = await call(tok(claims), { name: `i5 ${cn} ${vn}`, organizationId: v });
        const after = await rows();
        const added = after.filter((a) => !before.some((b) => b.id === a.id));
        out.item5.push({ caller: cn, variant: vn, sent: v, status: r.status, msg: r.body?.error?.message ?? null,
          stored: added.map((a) => ({ tenant: a.tenant, org: a.org })) });
      }
    }
  }, 300_000);
});
