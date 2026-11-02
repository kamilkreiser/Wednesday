/* Gate 121 real-PostgreSQL proof (NOT part of the PR). Real routes + real errorHandler; ../db replaced by a real pg Pool
 * on a throwaway postgres:15-alpine (gate121-pg) whose schema is the repo's init.sql governance DDL; only the chosen
 * participant SELECTs are made to throw before reaching the server. */
import express from 'express';
import type { Server } from 'http';
import * as fs from 'fs';
const F: any = { byId: [] as boolean[], byAddress: [] as boolean[], all: false, value: null as null | (() => unknown), stmts: [] as string[] };
jest.mock('../db', () => {
  const { Pool } = require('pg');
  const pool = new Pool({ host: '127.0.0.1', port: 55121, user: 'postgres', password: 'g121local', database: 'g121', max: 2 });
  (global as any).__g121pool = pool;
  return { isDbAvailable: () => true, query: async (t: string, p?: unknown[]) => {
    const sql = String(t).replace(/\s+/g, ' ').trim();
    const m = /^SELECT \* FROM svc_governance_participants WHERE (id|wallet_address) = \$1$/.exec(sql);
    if (m && F.value) { const k = m[1] === 'id' ? 'byId' : 'byAddress'; const qd = F[k].length ? F[k].shift() : false; if (F.all || qd) { F.stmts.push('FAILED ' + k); throw F.value(); } }
    F.stmts.push(sql.slice(0, 60));
    return pool.query(t, p);
  } };
});
jest.mock('../utils/logger', () => ({ logger: { info: () => undefined, warn: () => undefined, debug: () => undefined, error: () => undefined } }));
import { errorHandler } from '@secuura/shared';
import { governanceRoutes } from '../routes/governance';
const app = express(); app.use(express.json());
app.use((req, _r, n) => { (req as any).user = { userId: String(req.headers['x-u']), tenantId: 't' }; n(); });
app.use('/api/governance', governanceRoutes); app.use(errorHandler);
let server: Server; let base = '';
const pool = () => (global as any).__g121pool;
beforeAll(async () => {
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { base = `http://127.0.0.1:${(server.address() as any).port}`; r(); }); });
  await pool().query('DROP TABLE IF EXISTS svc_proposals, svc_governance_participants, svc_vote_delegations');
  await pool().query(fs.readFileSync(process.env.G121_DDL as string, 'utf8'));
});
afterAll(async () => { server.closeAllConnections(); await new Promise<void>((r) => server.close(() => r())); await pool().end(); });
async function seed() {
  await pool().query('TRUNCATE svc_proposals, svc_governance_participants, svc_vote_delegations');
  const ins = `INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power, is_drep, is_constitutional_committee, proposals_created, votes_cast, joined_at) VALUES ($1,$2,$3,$4,$5,true,$6,4,7,'2026-01-01T00:00:00Z')`;
  await pool().query(ins, ['u-1', 'addr_u1', 100000, 'partner', 200000, false]);
  await pool().query(ins, ['u-2', 'u-2', 50000, 'validator', 75000, false]);
  await pool().query(ins, ['u-cc', 'addr_cc', 20000, 'validator', 30000, true]);
}
const dump = async () => ({
  participants: (await pool().query('SELECT id, wallet_address, staked_amount::text, tier, vote_power::text, is_drep, is_constitutional_committee, proposals_created, votes_cast, joined_at FROM svc_governance_participants ORDER BY id')).rows.map((r: any) => ({ ...r, id: /^[0-9a-f-]{36}$/.test(r.id) ? '<uuid>' : r.id, joined_at: new Date(r.joined_at).toISOString().startsWith('2026-01-01') ? 'seeded' : 'NEW' })),
  proposals: Number((await pool().query('SELECT count(*) FROM svc_proposals')).rows[0].count),
  maxNum: Number((await pool().query('SELECT COALESCE(MAX(proposal_number),0) AS m FROM svc_proposals')).rows[0].m),
});
const NP = { title: 'g121 real pg proposal', description: 'a description long enough for the create schema g121', category: 'general' };
const VAL: Record<string, null | (() => unknown)> = { none: null, error: () => new Error('g121 pg stand-in read failure'), revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; } };
const CELLS: any[] = [
  { name: 'create_u1_byId_once', m: 'POST', p: '/api/governance/proposals', u: 'u-1', b: NP, byId: [true] },
  { name: 'create_u1_all_reads', m: 'POST', p: '/api/governance/proposals', u: 'u-1', b: NP, all: true },
  { name: 'create_u2_walletIsId_byId_once', m: 'POST', p: '/api/governance/proposals', u: 'u-2', b: NP, byId: [true] },
  { name: 'create_unregistered', m: 'POST', p: '/api/governance/proposals', u: 'u-new', b: NP, byAddress: [true] },
  { name: 'register_existing_wallet', m: 'POST', p: '/api/governance/participants/register', u: 'u-1', b: { walletAddress: 'addr_u1', stakedAmount: 5000 }, byAddress: [true] },
  { name: 'register_new_wallet', m: 'POST', p: '/api/governance/participants/register', u: 'u-1', b: { walletAddress: 'addr_new', stakedAmount: 5000 }, byAddress: [true] },
  { name: 'get_u1', m: 'GET', p: '/api/governance/participants/u-1', u: 'u-1', byId: [true] },
  { name: 'get_absent', m: 'GET', p: '/api/governance/participants/u-nobody', u: 'u-1' },
];
for (const c of CELLS) for (const [vn, vf] of Object.entries(VAL)) {
  it(`${c.name} ${vn}`, async () => {
    await seed(); F.stmts = []; F.value = vf; F.all = !!c.all && !!vf; F.byId = vf ? [...(c.byId || [])] : []; F.byAddress = vf ? [...(c.byAddress || [])] : [];
    let status: unknown, body: unknown;
    try { const r = await fetch(base + c.p, { method: c.m, headers: { 'content-type': 'application/json', 'x-u': c.u }, body: c.b ? JSON.stringify(c.b) : undefined, signal: AbortSignal.timeout(2500) }); status = r.status; body = await r.json(); } catch { status = 'NO_ANSWER'; }
    F.value = null;
    fs.appendFileSync(process.env.PROBE_OUT as string, JSON.stringify({ cell: c.name, value: vn, status, code: (body as any)?.error?.code ?? ((body as any)?.success ? 'ok' : null), stmts: F.stmts, state: await dump() }) + '\n');
  });
}
