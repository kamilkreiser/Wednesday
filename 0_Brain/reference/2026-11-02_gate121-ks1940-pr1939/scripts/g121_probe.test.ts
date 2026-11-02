/* Gate 121 probe (NOT part of the PR). Real governance routes + real shared errorHandler over a real socket,
 * a stateful stand-in for ../db that journals every write and applies ON CONFLICT (id) DO UPDATE SET <cols>.
 * One JSON record per cell to PROBE_OUT. Written independently of the author's harness. */
import express from 'express';
import type { Server } from 'http';
import * as fs from 'fs';

type Row = Record<string, unknown>;
type T = 'svc_proposals' | 'svc_governance_participants' | 'svc_vote_delegations';
const H: any = {
  tables: { svc_proposals: new Map(), svc_governance_participants: new Map(), svc_vote_delegations: new Map() },
  writes: [] as string[], reads: [] as string[], unknown: [] as string[], logs: [] as unknown[][],
  fail: { byId: [] as boolean[], byAddress: [] as boolean[] }, // per-call queue: true = throw
  failAll: { byId: false, byAddress: false }, value: null as null | (() => unknown), unique: true,
};
async function q(text: string, params: unknown[] = []): Promise<any> {
  const sql = String(text).replace(/\s+/g, ' ').trim();
  let m: RegExpExecArray | null;
  if ((m = /^SELECT \* FROM svc_governance_participants WHERE (id|wallet_address) = \$1$/.exec(sql))) {
    const k = m[1] === 'id' ? 'byId' : 'byAddress';
    H.reads.push(k);
    const queued = H.fail[k].length ? H.fail[k].shift() : false;
    if ((H.failAll[k] || queued) && H.value) throw H.value();
    const col = m[1];
    const rows = [...H.tables.svc_governance_participants.values()].filter((r: Row) => r[col] === params[0]);
    return { rows: rows.map((r: Row) => ({ ...r })), rowCount: rows.length };
  }
  if ((m = /^INSERT INTO (\w+) \(([^)]*)\) VALUES \([^)]*\) ON CONFLICT \(id\) DO UPDATE SET (.*)$/.exec(sql))) {
    const t = m[1] as T; const cols = m[2].split(',').map((c) => c.trim());
    const upd = m[3].split(',').map((c) => c.trim().split(/\s*=\s*/)[0]);
    const row: Row = {}; cols.forEach((c, i) => { const v = params[i]; row[c] = v instanceof Date ? v.toISOString() : v; });
    const tbl = H.tables[t];
    const ex = tbl.get(String(row.id));
    if (ex) { H.writes.push(`UPSERT-UPDATE ${t} id=${row.id}`); for (const c of upd) ex[c] = row[c]; return { rows: [], rowCount: 1 }; }
    if (t === 'svc_governance_participants' && H.unique && [...tbl.values()].some((r: Row) => r.wallet_address === row.wallet_address)) {
      H.writes.push(`INSERT-REFUSED-23505 ${t} id=${row.id}`);
      const e: any = new Error('duplicate key value violates unique constraint "svc_governance_participants_wallet_address_key"'); e.code = '23505'; throw e;
    }
    H.writes.push(`INSERT ${t} id=${row.id}`); tbl.set(String(row.id), row); return { rows: [], rowCount: 1 };
  }
  if ((m = /^DELETE FROM (\w+) WHERE id = \$1$/.exec(sql))) {
    H.writes.push(`DELETE ${m[1]} id=${params[0]} existed=${H.tables[m[1]].has(String(params[0]))}`);
    H.tables[m[1]].delete(String(params[0])); return { rows: [], rowCount: 1 };
  }
  if (/^SELECT \* FROM svc_proposals WHERE id = \$1$/.test(sql)) {
    const r = H.tables.svc_proposals.get(String(params[0])); return { rows: r ? [{ ...r }] : [], rowCount: r ? 1 : 0 };
  }
  if (/^SELECT \* FROM svc_proposals WHERE status = ANY\(\$1\) ORDER BY created_at DESC$/.test(sql)) {
    const want = params[0] as string[]; const rows = [...H.tables.svc_proposals.values()].filter((r: Row) => want.includes(String(r.status)));
    return { rows: rows.map((r: Row) => ({ ...r })), rowCount: rows.length };
  }
  if ((m = /^SELECT \* FROM svc_vote_delegations WHERE revoked_at IS NULL AND \(expires_at IS NULL OR expires_at > NOW\(\)\) AND (delegate_id|delegator_id) = \$1$/.exec(sql))) {
    const col = m[1]; const rows = [...H.tables.svc_vote_delegations.values()].filter((r: Row) => r[col] === params[0] && !r.revoked_at);
    return { rows: rows.map((r: Row) => ({ ...r })), rowCount: rows.length };
  }
  H.unknown.push(sql.slice(0, 140));
  return { rows: [], rowCount: 0 };
}
jest.mock('../db', () => ({ isDbAvailable: () => true, query: (t: string, p?: unknown[]) => q(t, p) }));
jest.mock('../utils/logger', () => ({ logger: { info: () => undefined, warn: () => undefined, debug: () => undefined,
  error: (...a: unknown[]) => { let s: string; try { s = JSON.stringify(a); } catch { s = '[unserialisable]'; } H.logs.push([s]); } } }));

import { errorHandler } from '@secuura/shared';
import { governanceRoutes } from '../routes/governance';
const app = express(); app.use(express.json());
app.use((req, _res, next) => { (req as any).user = { userId: String(req.headers['x-u'] || 'u-1'), tenantId: 't-1' }; next(); });
app.use('/api/governance', governanceRoutes); app.use(errorHandler);
let server: Server; let base = '';
beforeAll(async () => { await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => { const a: any = server.address(); base = `http://127.0.0.1:${a.port}`; r(); }); }); });
afterAll(async () => { server.closeAllConnections(); await new Promise<void>((r) => server.close(() => r())); });

async function call(method: string, path: string, u: string, body?: unknown) {
  try {
    const res = await fetch(base + path, { method, headers: { 'content-type': 'application/json', 'x-u': u }, body: body === undefined ? undefined : JSON.stringify(body), signal: AbortSignal.timeout(1500) });
    const t = await res.text(); let j: unknown; try { j = JSON.parse(t); } catch { j = { raw: t }; }
    return { status: res.status as number | string, body: j };
  } catch { return { status: 'NO_ANSWER', body: null }; }
}
const PLANTED = 'g121-planted-secret';
function P(id: string, w: string, s: number, tier: string, vp: number, x: Row = {}): Row {
  return { id, wallet_address: w, did: null, staked_amount: s, tier, vote_power: vp, is_drep: true, is_constitutional_committee: false,
    proposals_created: 4, votes_cast: 7, last_active_at: '2026-10-01T00:00:00.000Z', joined_at: '2026-01-01T00:00:00.000Z', ...x };
}
function PR(id: string, by: string, st: string, x: Row = {}): Row {
  return { id, proposal_number: 0, title: 't ' + id, description: 'seeded proposal description for g121', category: 'general', proposer_id: by,
    proposer_address: 'a_' + by, status: st, voting_config: {}, actions: [], votes_for: 0, votes_against: 0, votes_abstain: 0,
    total_vote_power: 1000000, voter_count: 0, votes: [], created_at: '2026-10-01T00:00:00.000Z', ...x };
}
function seed() {
  const p = H.tables.svc_governance_participants, r = H.tables.svc_proposals; p.clear(); r.clear(); H.tables.svc_vote_delegations.clear();
  p.set('u-1', P('u-1', 'addr_u1', 100000, 'partner', 200000));
  p.set('u-2', P('u-2', 'u-2', 50000, 'validator', 75000));
  p.set('u-cc', P('u-cc', 'addr_cc', 20000, 'validator', 30000, { is_constitutional_committee: true }));
  p.set('u-3', P('u-3', 'addr_u3', 10000, 'validator', 15000));
  r.set('p-draft', PR('p-draft', 'u-1', 'draft'));
  r.set('p-active', PR('p-active', 'u-3', 'active', { voting_starts_at: '2026-10-01T00:00:00.000Z', voting_ends_at: '2099-01-01T00:00:00.000Z' }));
}
const snap = () => { const o: any = {}; for (const n of Object.keys(H.tables)) o[n] = [...H.tables[n].values()].map((r: Row) => JSON.parse(JSON.stringify(r))).sort((a: Row, b: Row) => String(a.id).localeCompare(String(b.id))); return o; };

const VALUES: Record<string, null | (() => unknown)> = {
  none: null,
  error: () => new Error('g121 stand-in: connection terminated'),
  string: () => 'g121 stand-in string',
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  getterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } }, detail: { value: PLANTED, enumerable: true } }),
  protoTrap: () => new Proxy({}, { getPrototypeOf() { throw new Error('proto trap'); } }),
  toStringThrows: () => ({ toString() { throw new Error('toString boom'); }, secret: PLANTED }),
  nullProto: () => Object.assign(Object.create(null), { secret: PLANTED }),
};
const NP = { title: 'g121 probe proposal title', description: 'a description long enough for the create schema g121', category: 'general' };
type Cell = { name: string; method: string; path: string; u: string; body?: unknown; fail?: { byId?: boolean[]; byAddress?: boolean[] }; failAll?: { byId?: boolean; byAddress?: boolean }; unique?: boolean };
const CELLS: Cell[] = [
  { name: 'create_u1_byId1', method: 'POST', path: '/api/governance/proposals', u: 'u-1', body: NP, fail: { byId: [true] } },
  { name: 'create_u1_allReads', method: 'POST', path: '/api/governance/proposals', u: 'u-1', body: NP, failAll: { byId: true, byAddress: true } },
  { name: 'create_u2_walletIsId_byId1', method: 'POST', path: '/api/governance/proposals', u: 'u-2', body: NP, fail: { byId: [true] } },
  { name: 'create_unreg_byAddr1', method: 'POST', path: '/api/governance/proposals', u: 'u-new', body: NP, fail: { byAddress: [true] } },
  { name: 'register_existing_byAddr_unique', method: 'POST', path: '/api/governance/participants/register', u: 'u-1', body: { walletAddress: 'addr_u1', stakedAmount: 5000 }, fail: { byAddress: [true] } },
  { name: 'register_existing_byAddr_nounique', method: 'POST', path: '/api/governance/participants/register', u: 'u-1', body: { walletAddress: 'addr_u1', stakedAmount: 5000 }, fail: { byAddress: [true] }, unique: false },
  { name: 'register_new_byAddr', method: 'POST', path: '/api/governance/participants/register', u: 'u-1', body: { walletAddress: 'addr_brand_new', stakedAmount: 5000 }, fail: { byAddress: [true] } },
  { name: 'get_byId_fail_id', method: 'GET', path: '/api/governance/participants/u-1', u: 'u-1', fail: { byId: [true] } },
  { name: 'get_T8_byId_fail_addr', method: 'GET', path: '/api/governance/participants/addr_u1', u: 'u-1', fail: { byId: [true] } },
  { name: 'get_byAddr_fail_addr', method: 'GET', path: '/api/governance/participants/addr_u1', u: 'u-1', fail: { byAddress: [true] } },
  { name: 'get_absent', method: 'GET', path: '/api/governance/participants/u-nobody', u: 'u-1' },
  { name: 'vote_u1', method: 'POST', path: '/api/governance/proposals/p-active/vote', u: 'u-1', body: { vote: 'for' }, fail: { byId: [true] } },
  { name: 'vote_unreg', method: 'POST', path: '/api/governance/proposals/p-active/vote', u: 'u-zz', body: { vote: 'for' }, fail: { byId: [true] } },
  { name: 'cancel_proposer', method: 'POST', path: '/api/governance/proposals/p-draft/cancel', u: 'u-1', fail: { byId: [true] } },
  { name: 'cancel_committee', method: 'POST', path: '/api/governance/proposals/p-draft/cancel', u: 'u-cc', fail: { byId: [true] } },
  { name: 'cancel_stranger', method: 'POST', path: '/api/governance/proposals/p-draft/cancel', u: 'u-3', fail: { byId: [true] } },
  { name: 'delegate_first', method: 'POST', path: '/api/governance/delegate', u: 'u-1', body: { delegateId: 'u-3', allProposals: true }, fail: { byId: [true] } },
  { name: 'delegate_second', method: 'POST', path: '/api/governance/delegate', u: 'u-1', body: { delegateId: 'u-3', allProposals: true }, fail: { byId: [false, true] } },
];
const OUT = process.env.PROBE_OUT as string;
for (const c of CELLS) for (const [vn, vf] of Object.entries(VALUES)) {
  it(`${c.name} ${vn}`, async () => {
    seed(); H.unknown = []; H.logs = []; H.fail = { byId: [], byAddress: [] }; H.failAll = { byId: false, byAddress: false }; H.value = null; H.unique = c.unique ?? true;
    const pre = await call('POST', '/api/governance/proposals', 'u-cc', NP); // counter reference (healthy)
    const n0 = Number((pre.body as any)?.data?.proposalNumber);
    seed(); H.writes = []; H.reads = [];
    const before = snap();
    if (vf) { H.value = vf; H.fail = { byId: [...(c.fail?.byId || [])], byAddress: [...(c.fail?.byAddress || [])] }; H.failAll = { byId: !!c.failAll?.byId, byAddress: !!c.failAll?.byAddress }; }
    const r = await call(c.method, c.path, c.u, c.body);
    const writes = [...H.writes]; const reads = [...H.reads]; const after = snap(); const logs = [...H.logs];
    H.value = null; H.fail = { byId: [], byAddress: [] }; H.failAll = { byId: false, byAddress: false };
    seed(); H.writes = [];
    const post = await call('POST', '/api/governance/proposals', 'u-cc', NP);
    const counterDelta = Number((post.body as any)?.data?.proposalNumber) - n0;
    fs.appendFileSync(OUT, JSON.stringify({ cell: c.name, value: vn, status: r.status, body: r.body, writes, reads, unchanged: JSON.stringify(after) === JSON.stringify(before), before, after, counterDelta, logs, unknown: H.unknown, plantedInLogs: JSON.stringify(logs).includes(PLANTED) }) + '\n');
  });
}
