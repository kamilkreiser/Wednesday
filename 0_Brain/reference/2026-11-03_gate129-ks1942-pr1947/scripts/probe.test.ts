// @ts-nocheck
// QA GATE 129 probe (NOT part of the PR). Copied into the clone's src/__tests__ for a run, then moved to logs/_quarantine.
// Drives the REAL governance router (POST /participants/register, POST /proposals) behind the REAL shared
// jwtAuthenticate (RS256 tokens signed with a key generated here) and the REAL shared errorHandler, over the REAL
// services/governance db.ts, against a REAL PostgreSQL 15.19 (throwaway container gate129-pg): governance tables from
// docker/init/04-sprint2-service-tables.sql verbatim (wallet_address UNIQUE), users under migration 039's fail-closed
// tenant_isolation policy with ENABLE + FORCE RLS, connected as gate_app (NOSUPERUSER, NOBYPASSRLS).
// The only thing replaced: pg.Client.prototype.query is wrapped so a cell can make ONE named statement reject
// (ordinary Error or a revoked Proxy) or run a hook before it; every other statement goes to the real server.
import crypto from 'crypto';
import express from 'express';
import { appendFileSync } from 'fs';

const OUT = process.env.PROBE_OUT;
const PGURL = 'postgres://gate_app:gate129local@127.0.0.1:55129/postgres';
const SUPERURL = 'postgres://postgres:gate129super@127.0.0.1:55129/postgres';
process.env.DATABASE_URL = PGURL;
const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' })).toString('base64');
delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;

const pg = require('pg');
const jwt = require('jsonwebtoken');
const H = { faults: [], hooks: [], sql: [] };
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
const label = (s) => {
  const n = norm(s);
  if (/^SELECT \* FROM svc_governance_participants WHERE id = \$1/i.test(n)) return 'byId';
  if (/^SELECT \* FROM svc_governance_participants WHERE wallet_address = \$1/i.test(n)) return 'byAddress';
  if (/FROM users WHERE/i.test(n)) return 'users';
  if (/^INSERT INTO svc_governance_participants/i.test(n)) return 'SAVE participant';
  if (/^INSERT INTO svc_proposals/i.test(n)) return 'SAVE proposal';
  if (/^DELETE FROM svc_governance_participants/i.test(n)) return 'DELETE participant';
  if (/set_config\('app.current_tenant_id'/i.test(n)) return 'GUC';
  return n.slice(0, 40);
};
const orig = pg.Client.prototype.query;
pg.Client.prototype.query = function (text, values, cb) {
  if (this.__gateAdmin) return orig.apply(this, arguments);
  const sql = typeof text === 'string' ? text : text && text.text;
  const l = label(sql);
  H.sql.push(l);
  const callback = typeof values === 'function' ? values : cb;
  const hook = H.hooks.find((h) => h.label === l && h.times > 0);
  const fault = H.faults.find((f) => f.label === l && f.times > 0);
  if (fault) {
    fault.times -= 1;
    const v = fault.value();
    if (callback) { process.nextTick(() => callback(v)); return undefined; }
    return Promise.reject(v);
  }
  if (hook) {
    hook.times -= 1;
    const self = this, args = arguments;
    const p = hook.run().then(() => orig.apply(self, args));
    if (callback) return undefined; // pool.query path: orig with callback already wired via args
    return p;
  }
  return orig.apply(this, arguments);
};

const ordinary = () => new Error('gate129 planted ordinary failure');
const revoked = () => { const r = Proxy.revocable(new Error('x'), {}); r.revoke(); return r.proxy; };

const T1 = 'a1000000-0000-4000-8000-000000000001';
const T2 = 'a2000000-0000-4000-8000-000000000002';
const U1 = '11111111-1111-4111-8111-111111111111'; // linked W1, no participant row
const U2 = '22222222-2222-4222-8222-222222222222'; // linked W2, participant row: staked 50000, DRep, committee
const U3 = '33333333-3333-4333-8333-333333333333'; // no linked wallet
const U4 = '44444444-4444-4444-8444-444444444444'; // tenant T2, linked W4
const UA = 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'; // admin user, T1
const W1 = 'addr_test1_gate129_w1', W2 = 'addr_test1_gate129_w2', W4 = 'addr_test1_gate129_w4', WX = 'addr_test1_gate129_unregistered';

let admin; let server; let base;
const tok = (userId, role = 'user', tenantId = T1) =>
  jwt.sign({ userId, email: 'g@example.test', role, ...(tenantId === null ? {} : { tenantId }) }, privateKey, { algorithm: 'RS256', expiresIn: 600 });

async function reset(extra = []) {
  await admin.query('TRUNCATE svc_governance_participants, svc_proposals, svc_vote_delegations, users');
  for (const [id, t, w] of [[U1, T1, W1], [U2, T1, W2], [U3, T1, null], [U4, T2, W4], [UA, T1, 'addr_test1_gate129_admin']])
    await admin.query('INSERT INTO users (id, tenant_id, email, wallet_address) VALUES ($1,$2,$3,$4)', [id, t, `${id.slice(0, 4)}@example.test`, w]);
  await admin.query(`INSERT INTO svc_governance_participants (id, wallet_address, did, staked_amount, tier, vote_power, is_drep, is_constitutional_committee, proposals_created, votes_cast, last_active_at, joined_at)
    VALUES ($1,$2,'did:gate129:u2',50000,'whale',75000,true,true,2,3,'2026-01-01T00:00:00Z','2026-01-01T00:00:00Z')`, [U2, W2]);
  for (const sql of extra) await admin.query(sql[0], sql[1]);
  H.faults = []; H.hooks = []; H.sql = [];
}
async function snap() {
  const p = await admin.query('SELECT id, wallet_address, did, staked_amount::text AS stake, tier, vote_power::text AS vp, is_drep, is_constitutional_committee AS cc, proposals_created AS pc, votes_cast AS vc, joined_at FROM svc_governance_participants ORDER BY id');
  const q = await admin.query('SELECT count(*)::int AS n FROM svc_proposals');
  return { participants: p.rows.map((r) => ({ ...r, joined_at: r.joined_at && r.joined_at.toISOString() })), proposals: q.rows[0].n };
}
async function call(path, token, body) {
  const res = await fetch(base + path, { method: 'POST', headers: { 'content-type': 'application/json', authorization: `Bearer ${token}` }, body: JSON.stringify(body), signal: AbortSignal.timeout(8000) });
  let j = null; try { j = await res.json(); } catch {}
  return { status: res.status, body: j };
}
const unhandled = [];
process.on('unhandledRejection', (e) => unhandled.push(String(typeof e)));

async function cell(id, path, token, body, setup = {}) {
  await reset(setup.seed || []);
  (setup.faults || []).forEach((f) => H.faults.push({ ...f }));
  (setup.hooks || []).forEach((h) => H.hooks.push({ ...h }));
  const before = await snap();
  const u0 = unhandled.length;
  const r = await call(path, token, body);
  const after = await snap();
  const d = r.body && r.body.data;
  const rec = { cell: id, status: r.status, message: r.body && r.body.error ? r.body.error.message : undefined,
    data: d ? { id: d.id, walletAddress: d.walletAddress, stakedAmount: d.stakedAmount, tier: d.tier, votePower: d.votePower, isDRep: d.isDRep, isConstitutionalCommittee: d.isConstitutionalCommittee, did: d.did } : undefined,
    before, after, unchanged: JSON.stringify(before) === JSON.stringify(after), sql: H.sql.slice(), unhandled: unhandled.length - u0 };
  appendFileSync(OUT, JSON.stringify(rec) + '\n');
}

beforeAll(async () => {
  admin = new pg.Client({ connectionString: SUPERURL }); admin.__gateAdmin = true; await admin.connect();
  const db = require('../db');
  const ok = await db.initDb();
  appendFileSync(OUT, JSON.stringify({ cell: 'initDb', ok, available: db.isDbAvailable(), hasLinkedRead: typeof db.getLinkedWalletAddress }) + '\n');
  const { authenticate, errorHandler, rejectNulBytes } = require('@secuura/shared');
  const { governanceRoutes } = require('../routes/governance');
  const app = express();
  app.use(express.json()); app.use(rejectNulBytes()); app.use('/api', authenticate()); app.use('/api/governance', governanceRoutes); app.use(errorHandler);
  await new Promise((ok2) => { server = app.listen(0, '127.0.0.1', ok2); });
  base = `http://127.0.0.1:${server.address().port}/api/governance`;
}, 30000);
afterAll(async () => { await new Promise((ok) => server.close(ok)); await admin.end(); await require('../db').closeDb(); });

const REG = '/participants/register';
const PROP = '/proposals';
const proposal = { title: 'Gate 129 probe proposal title', description: 'D'.repeat(80), category: 'general' };
const legacy = ['INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power, is_drep) VALUES ($1,$2,7000,$3,7000,true)', ['legacy-uuid-row', W1, 'staker']];
const legacySelf = ['INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power, is_drep) VALUES ($1,$1,1000,$2,1000,false)', [U1, 'staker']];

it('gate129 probe', async () => {
  // (a) non-admin, own linked wallet; every field the base handler accepted (walletAddress, stakedAmount, did, isDRep, isConstitutionalCommittee) + stripped extras
  await cell('a0 own wallet stake 0', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 });
  await cell('a1 own wallet stake 1e6', REG, tok(U1), { walletAddress: W1, stakedAmount: 1000000 });
  await cell('a2 own wallet isDRep true', REG, tok(U1), { walletAddress: W1, stakedAmount: 0, isDRep: true });
  await cell('a3 own wallet committee true', REG, tok(U1), { walletAddress: W1, stakedAmount: 0, isConstitutionalCommittee: true });
  await cell('a4 own wallet extras tier/votePower/id/role', REG, tok(U1), { walletAddress: W1, stakedAmount: 0, tier: 'whale', votePower: 1e9, id: 'forged', role: 'SUPER_ADMIN', proposalsCreated: 9 });
  await cell('a5 own wallet did + explicit false flags', REG, tok(U1), { walletAddress: W1, stakedAmount: 0, did: 'did:gate129:u1', isDRep: false, isConstitutionalCommittee: false });
  await cell('a6 role "admin" (not platform) stake 1e6', REG, tok(U1, 'admin'), { walletAddress: W1, stakedAmount: 1000000 });
  // (b) another wallet / no linked wallet
  await cell('b1 names U2 wallet W2 stake 0', REG, tok(U1), { walletAddress: W2, stakedAmount: 0 });
  await cell('b2 names unregistered wallet', REG, tok(U1), { walletAddress: WX, stakedAmount: 1000000, isDRep: true });
  await cell('b3 no linked wallet', REG, tok(U3), { walletAddress: WX, stakedAmount: 0 });
  await cell('b4 token without tenantId', REG, tok(U1, 'user', null), { walletAddress: W1, stakedAmount: 0 });
  await cell('b5 T2 user, token tenant T1 (cross-tenant)', REG, tok(U4, 'user', T1), { walletAddress: W4, stakedAmount: 0 });
  await cell('b6 non-uuid userId', REG, tok('not-a-uuid'), { walletAddress: W1, stakedAmount: 0 });
  await cell('b7 long-s role "ſuper_admin" names W2 stake 1e6', REG, tok(U1, 'ſuper_admin'), { walletAddress: W2, stakedAmount: 1000000 });
  await cell('b8 dotless-i role "super_admın" names W2 stake 1e6', REG, tok(U1, 'super_admın'), { walletAddress: W2, stakedAmount: 1000000 });
  await cell('b9 T2 user own wallet, own tenant T2 (control)', REG, tok(U4, 'user', T2), { walletAddress: W4, stakedAmount: 0 });
  // (c) duplicates
  await cell('c1 U2 re-registers own W2, stake 50000, flags omitted', REG, tok(U2), { walletAddress: W2, stakedAmount: 50000 });
  await cell('c2 U2 re-registers own W2 stake 0', REG, tok(U2), { walletAddress: W2, stakedAmount: 0 });
  await cell('c3 U2 re-registers own W2 isDRep false', REG, tok(U2), { walletAddress: W2, stakedAmount: 50000, isDRep: false });
  await cell('c4 legacy row holds W1 under another id', REG, tok(U1), { walletAddress: W1, stakedAmount: 7000 }, { seed: [legacy] });
  await cell('c5 legacy self row (wallet=id, stake 1000) re-registers W1 stake 1000', REG, tok(U1), { walletAddress: W1, stakedAmount: 1000 }, { seed: [legacySelf] });
  await cell('c6 legacy self row re-registers W1 stake 0', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 }, { seed: [legacySelf] });
  // (d) admin paths
  await cell('d1 SUPER_ADMIN sets W2 stake 200000 isDRep false', REG, tok(UA, 'SUPER_ADMIN'), { walletAddress: W2, stakedAmount: 200000, isDRep: false });
  await cell('d2 SYSTEM_ADMIN new wallet WX stake 5000 committee', REG, tok(UA, 'SYSTEM_ADMIN'), { walletAddress: WX, stakedAmount: 5000, isConstitutionalCommittee: true });
  await cell('d3 super_admin re-registers W2 flags omitted', REG, tok(UA, 'super_admin'), { walletAddress: W2, stakedAmount: 50000 });
  await cell('d4 SUPER_ADMIN registers W1 (U1 linked) stake 3000', REG, tok(UA, 'SUPER_ADMIN'), { walletAddress: W1, stakedAmount: 3000 });
  // (e) KS-1940 failed lookups -> 503 nothing written, admin and non-admin
  for (const [k, v] of [['ordinary', ordinary], ['revokedProxy', revoked]]) {
    await cell(`e1 admin byAddress fails (${k})`, REG, tok(UA, 'SUPER_ADMIN'), { walletAddress: W2, stakedAmount: 1 }, { faults: [{ label: 'byAddress', times: 1, value: v }] });
    await cell(`e2 non-admin byAddress fails (${k})`, REG, tok(U2), { walletAddress: W2, stakedAmount: 50000 }, { faults: [{ label: 'byAddress', times: 1, value: v }] });
    await cell(`e3 non-admin new user byId fails (${k})`, REG, tok(U1), { walletAddress: W1, stakedAmount: 0 }, { faults: [{ label: 'byId', times: 1, value: v }] });
    await cell(`e4 non-admin users read fails (${k})`, REG, tok(U1), { walletAddress: W1, stakedAmount: 0 }, { faults: [{ label: 'users', times: 1, value: v }] });
    await cell(`e5 non-admin legacy-self byAddress fails (${k})`, REG, tok(U1), { walletAddress: W1, stakedAmount: 1000 }, { seed: [legacySelf], faults: [{ label: 'byAddress', times: 1, value: v }] });
  }
  // (f) createProposal
  await cell('f1 unregistered U1 proposes', PROP, tok(U1), proposal);
  await cell('f2 staked U2 proposes (control)', PROP, tok(U2), proposal);
  await cell('f3 U3 (no linked wallet, unregistered) proposes', PROP, tok(U3), proposal);
  await cell('f4 U1 proposes, legacy row holds W1', PROP, tok(U1), proposal, { seed: [legacy] });
  for (const [k, v] of [['ordinary', ordinary], ['revokedProxy', revoked]]) {
    await cell(`f5 U2 proposes, byId fails (${k})`, PROP, tok(U2), proposal, { faults: [{ label: 'byId', times: 1, value: v }] });
    await cell(`f6 U1 proposes, users read fails (${k})`, PROP, tok(U1), proposal, { faults: [{ label: 'users', times: 1, value: v }] });
    await cell(`f7 U1 proposes, byAddress fails (${k})`, PROP, tok(U1), proposal, { faults: [{ label: 'byAddress', times: 1, value: v }] });
  }
  // (f) stale write-back: an admin sets U2's stake to 0 and revokes DRep between createProposal's read and its stats save
  await cell('f8 admin de-stakes U2 while U2 proposes (race)', PROP, tok(U2), proposal, { hooks: [{ label: 'SAVE proposal', times: 1,
    run: () => admin.query("UPDATE svc_governance_participants SET staked_amount = 0, tier = 'basic', vote_power = 0, is_drep = false, is_constitutional_committee = false WHERE id = $1", [U2]) }] });
  // (g) the only road to an admin-set stake that castVote / createProposal can find: order matters
  async function seq(id, steps) {
    await reset([]);
    const before = await snap(); const out = [];
    for (const [path, token, body] of steps) { const r = await call(path, token, body); out.push(r.status + (r.body && r.body.error ? ' ' + r.body.error.message.slice(0, 40) : '')); }
    const after = await snap();
    appendFileSync(OUT, JSON.stringify({ cell: id, status: out.join(' -> '), before, after, unchanged: JSON.stringify(before) === JSON.stringify(after), sql: [], unhandled: 0 }) + '\n');
  }
  await seq('g1 U1 self-registers, THEN admin stakes W1, then U1 proposes', [[REG, tok(U1), { walletAddress: W1, stakedAmount: 0 }], [REG, tok(UA, 'SUPER_ADMIN'), { walletAddress: W1, stakedAmount: 5000, isDRep: true }], [PROP, tok(U1), proposal]]);
  await seq('g2 admin stakes W1 FIRST, then U1 self-registers, then U1 proposes', [[REG, tok(UA, 'SUPER_ADMIN'), { walletAddress: W1, stakedAmount: 5000, isDRep: true }], [REG, tok(U1), { walletAddress: W1, stakedAmount: 5000, isDRep: true }], [PROP, tok(U1), proposal]]);
}, 120000);
