// @ts-nocheck
// QA GATE 136 (delta, round 2) probe, ported from gate 134's (NOT part of the PR). Copied into the clone's src/__tests__ for a run, then moved to logs/_quarantine.
// Drives the REAL governance router (register, POST /proposals, POST /proposals/:id/vote) behind the REAL shared
// authenticate (RS256 tokens signed with a key generated here) and the REAL shared errorHandler, over the REAL
// services/governance db.ts, against a REAL PostgreSQL 15.19 (throwaway container gate136-pg): governance tables from
// docker/init/04-sprint2-service-tables.sql verbatim (wallet_address UNIQUE), users under migration 039's fail-closed
// tenant_isolation policy with ENABLE + FORCE RLS, connected as gate_app (NOSUPERUSER, NOBYPASSRLS).
// The only thing replaced: pg.Client.prototype.query is wrapped so a cell can run a hook (on a REAL SECOND
// connection, `second`, also gate_app) just before ONE labelled statement, or make one statement reject.
import crypto from 'crypto';
import express from 'express';
import { appendFileSync } from 'fs';

const OUT = process.env.PROBE_OUT;
const RACE_N = Number(process.env.RACE_N || 150);
const PGURL = 'postgres://gate_app:gate136local@127.0.0.1:55136/postgres';
const SUPERURL = 'postgres://postgres:gate136super@127.0.0.1:55136/postgres';
process.env.DATABASE_URL = PGURL;
const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' })).toString('base64');
delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;

const pg = require('pg');
const jwt = require('jsonwebtoken');
const H = { faults: [], hooks: [], sql: [], pwrites: [] };
const norm = (s) => String(s).replace(/\s+/g, ' ').trim();
const label = (s) => {
  const n = norm(s);
  if (/^SELECT \* FROM svc_governance_participants WHERE id = \$1/i.test(n)) return 'byId';
  if (/^SELECT \* FROM svc_governance_participants WHERE wallet_address = \$1/i.test(n)) return 'byAddress';
  if (/FROM users WHERE/i.test(n)) return 'users';
  if (/^INSERT INTO svc_governance_participants.*DO NOTHING/i.test(n)) return 'INSERT-IF-ABSENT';
  if (/^INSERT INTO svc_governance_participants.*DO UPDATE/i.test(n)) return 'UPSERT participant';
  if (/^UPDATE svc_governance_participants SET wallet_address/i.test(n)) return 'REFRESH';
  if (/^UPDATE svc_governance_participants SET proposals_created/i.test(n)) return 'BUMP pc';
  if (/^UPDATE svc_governance_participants SET votes_cast/i.test(n)) return 'BUMP vc';
  if (/^(UPDATE|DELETE FROM|INSERT INTO) svc_governance_participants/i.test(n)) return 'OTHER participant write';
  if (/^INSERT INTO svc_proposals/i.test(n)) return 'SAVE proposal';
  if (/set_config\('app.current_tenant_id'/i.test(n)) return 'GUC';
  return n.slice(0, 40);
};
const isPWrite = (l) => ['INSERT-IF-ABSENT', 'UPSERT participant', 'REFRESH', 'BUMP pc', 'BUMP vc', 'OTHER participant write'].includes(l);
const orig = pg.Client.prototype.query;
pg.Client.prototype.query = function (text, values, cb) {
  if (this.__gateAdmin) return orig.apply(this, arguments);
  const sql = typeof text === 'string' ? text : text && text.text;
  const l = label(sql);
  H.sql.push(l);
  if (isPWrite(l)) H.pwrites.push(norm(sql));
  const callback = typeof values === 'function' ? values : cb;
  const match = (x) => x.times > 0 && (x.label === l || (x.label === 'PWRITE' && isPWrite(l)));
  const hook = H.hooks.find(match);
  const fault = H.faults.find(match);
  if (fault) {
    fault.times -= 1;
    fault.fired = l;
    const p = (fault.pre ? fault.pre() : Promise.resolve()).then(() => { throw fault.value(); });
    if (callback) { p.then(null, (v) => callback(v)); return undefined; }
    return p;
  }
  if (hook) {
    hook.times -= 1;
    hook.fired = l;
    const self = this, args = arguments;
    const p = hook.run().then(() => orig.apply(self, args));
    if (callback) return undefined;
    return p;
  }
  return orig.apply(this, arguments);
};

const T1 = 'a1000000-0000-4000-8000-000000000001';
const T2 = 'a2000000-0000-4000-8000-000000000002';
const U1 = '11111111-1111-4111-8111-111111111111'; // linked W1, no participant row
const U2 = '22222222-2222-4222-8222-222222222222'; // linked W2, row: 50000 / whale / 75000 / DRep / committee / did, pc 2 vc 3
const U3 = '33333333-3333-4333-8333-333333333333'; // no linked wallet
const U4 = '44444444-4444-4444-8444-444444444444'; // tenant T2, linked W4
const U5 = '55555555-5555-4555-8555-555555555555'; // linked W5; row (U5, W5old) unstaked
const UA = 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa'; // admin user, T1
const P1 = 'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb'; // an active proposal
const W1 = 'addr_test1_gate134_w1', W2 = 'addr_test1_gate134_w2', W4 = 'addr_test1_gate134_w4', W5 = 'addr_test1_gate134_w5', WX = 'addr_test1_gate134_unregistered';

let admin; let second; let server; let base; let logSpy = [];
const tok = (userId, role = 'user', tenantId = T1) =>
  jwt.sign({ userId, email: 'g@example.test', role, ...(tenantId === null ? {} : { tenantId }) }, privateKey, { algorithm: 'RS256', expiresIn: 600 });

async function reset(extra = []) {
  await admin.query('TRUNCATE svc_governance_participants, svc_proposals, svc_vote_delegations, users');
  for (const [id, t, w] of [[U1, T1, W1], [U2, T1, W2], [U3, T1, null], [U4, T2, W4], [U5, T1, W5], [UA, T1, 'addr_test1_gate134_admin']])
    await admin.query('INSERT INTO users (id, tenant_id, email, wallet_address) VALUES ($1,$2,$3,$4)', [id, t, `${id.slice(0, 4)}@example.test`, w]);
  await admin.query(`INSERT INTO svc_governance_participants (id, wallet_address, did, staked_amount, tier, vote_power, is_drep, is_constitutional_committee, proposals_created, votes_cast, last_active_at, joined_at)
    VALUES ($1,$2,'did:gate134:u2',50000,'whale',75000,true,true,2,3,'2026-01-01T00:00:00Z','2026-01-01T00:00:00Z')`, [U2, W2]);
  await admin.query(`INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power) VALUES ($1,'addr_test1_gate134_w5old',0,'basic',0)`, [U5]);
  await admin.query(`INSERT INTO svc_proposals (id, title, description, category, proposer_id, proposer_address, status, voting_config, voting_starts_at, voting_ends_at, votes)
    VALUES ($1,'Gate 134 active proposal','D','general',$2,'addr_test1_gate134_admin','active','{}', now() - interval '1 hour', now() + interval '1 day','[]')`, [P1, UA]);
  for (const sql of extra) await admin.query(sql[0], sql[1]);
  H.faults = []; H.hooks = []; H.sql = []; H.pwrites = []; logSpy = [];
}
async function snap() {
  const p = await admin.query('SELECT id, wallet_address, did, staked_amount::text AS stake, tier, vote_power::text AS vp, is_drep, is_constitutional_committee AS cc, proposals_created AS pc, votes_cast AS vc, joined_at FROM svc_governance_participants ORDER BY id');
  const q = await admin.query('SELECT count(*)::int AS n FROM svc_proposals');
  return { participants: p.rows.map((r) => ({ ...r, joined_at: r.joined_at && r.joined_at.toISOString() })), proposals: q.rows[0].n };
}
async function call(path, token, body) {
  const res = await fetch(base + path, { method: 'POST', headers: { 'content-type': 'application/json', authorization: `Bearer ${token}` }, body: JSON.stringify(body), signal: AbortSignal.timeout(15000) });
  let j = null; try { j = await res.json(); } catch {}
  return { status: res.status, body: j };
}
const unhandled = [];
process.on('unhandledRejection', (e) => unhandled.push(String(typeof e)));
const pick = (d) => d ? { id: d.id, walletAddress: d.walletAddress, stakedAmount: d.stakedAmount, tier: d.tier, votePower: d.votePower, isDRep: d.isDRep, isConstitutionalCommittee: d.isConstitutionalCommittee, did: d.did, proposalsCreated: d.proposalsCreated, votesCast: d.votesCast } : undefined;

async function cell(id, path, token, body, setup = {}) {
  await reset(setup.seed || []);
  const faults = (setup.faults || []).map((f) => ({ ...f }));
  faults.forEach((f) => H.faults.push(f));
  const hooks = (setup.hooks || []).map((h) => ({ ...h }));
  hooks.forEach((h) => H.hooks.push(h));
  const before = await snap();
  const u0 = unhandled.length;
  const r = await call(path, token, body);
  const after = await snap();
  const rec = { cell: id, status: r.status, message: r.body && r.body.error ? r.body.error.message : undefined,
    data: pick(r.body && r.body.data), hookFiredBefore: hooks.map((h) => h.fired || 'NOT FIRED').concat(faults.map((f) => 'FAULT@' + (f.fired || 'NOT FIRED'))),
    before, after, unchanged: JSON.stringify(before) === JSON.stringify(after), sql: H.sql.slice(), pwrites: H.pwrites.slice(),
    logs: logSpy.slice(), unhandled: unhandled.length - u0 };
  appendFileSync(OUT, JSON.stringify(rec) + '\n');
  return rec;
}

beforeAll(async () => {
  admin = new pg.Client({ connectionString: SUPERURL }); admin.__gateAdmin = true; await admin.connect();
  second = new pg.Client({ connectionString: PGURL }); second.__gateAdmin = true; await second.connect();
  const db = require('../db');
  const ok = await db.initDb();
  const { logger } = require('../utils/logger');
  for (const lv of ['warn', 'error', 'info']) {
    const origLv = logger[lv].bind(logger);
    logger[lv] = (msg, meta) => { logSpy.push({ lv, msg, meta }); return origLv(msg, meta); };
  }
  appendFileSync(OUT, JSON.stringify({ cell: 'initDb', ok, available: db.isDbAvailable(), secondRole: (await second.query('select current_user u, pg_backend_pid() p')).rows[0] }) + '\n');
  const { authenticate, errorHandler, rejectNulBytes } = require('@secuura/shared');
  const { governanceRoutes } = require('../routes/governance');
  const app = express();
  app.use(express.json()); app.use(rejectNulBytes()); app.use('/api', authenticate()); app.use('/api/governance', governanceRoutes); app.use(errorHandler);
  await new Promise((ok2) => { server = app.listen(0, '127.0.0.1', ok2); });
  base = `http://127.0.0.1:${server.address().port}/api/governance`;
}, 30000);
afterAll(async () => { await new Promise((ok) => server.close(ok)); await admin.end(); await second.end(); await require('../db').closeDb(); });

const REG = '/participants/register';
const PROP = '/proposals';
const VOTE = `/proposals/${P1}/vote`;
const proposal = { title: 'Gate 134 probe proposal title', description: 'D'.repeat(80), category: 'general' };
const legacy = ['INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power, is_drep) VALUES ($1,$2,7000,$3,7000,true)', ['legacy-uuid-row', W1, 'staker']];
const legacySelf = ['INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power, is_drep) VALUES ($1,$1,1000,$2,1000,false)', [U1, 'staker']];
const sec = (sql, params) => () => second.query(sql, params);

// The admin changes, each on the REAL second connection, each run just before the path's FIRST participant write
// (i.e. after the path's read). 'route' is the REAL admin route (SUPER_ADMIN, HTTP) instead of SQL.
const CHANGES = {
  destake: sec("UPDATE svc_governance_participants SET staked_amount = 0, tier = 'basic', vote_power = 0 WHERE id = $1", [U2]),
  drep: sec('UPDATE svc_governance_participants SET is_drep = false WHERE id = $1', [U2]),
  committee: sec('UPDATE svc_governance_participants SET is_constitutional_committee = false WHERE id = $1', [U2]),
  did: sec("UPDATE svc_governance_participants SET did = 'did:gate134:admin-set' WHERE id = $1", [U2]),
  wallet: sec("UPDATE svc_governance_participants SET wallet_address = 'addr_test1_gate134_w2_admin' WHERE id = $1", [U2]),
  restake: sec("UPDATE svc_governance_participants SET staked_amount = 200000, tier = 'partner', vote_power = 400000 WHERE id = $1", [U2]),
  route: async () => { const r = await call(REG, tok(UA, 'SUPER_ADMIN'), { walletAddress: W2, stakedAmount: 0, isDRep: false, isConstitutionalCommittee: false }); if (r.status !== 201) throw new Error('admin route ' + r.status); },
};

it('gate136 probe', async () => {
  // Q1 headline: three paths x seven admin changes, plus a no-change control per path.
  const PATHS = {
    propose: [PROP, tok(U2), proposal],
    vote: [VOTE, tok(U2), { vote: 'for' }],
    selfreg: [REG, tok(U2), { walletAddress: W2, stakedAmount: 50000 }],
    selfregDid: [REG, tok(U2), { walletAddress: W2, stakedAmount: 50000, did: 'did:gate134:body' }],
  };
  for (const [pn, [path, t, body]] of Object.entries(PATHS)) {
    await cell(`Q1 ${pn} control (no admin change)`, path, t, body);
    for (const [cn, run] of Object.entries(CHANGES)) {
      if (pn === 'selfregDid' && cn !== 'did') continue;
      await cell(`Q1 ${pn} x ${cn}`, path, t, body, { hooks: [{ label: 'PWRITE', times: 1, run }] });
    }
  }
  // D-4: the admin upsert no longer writes the counters back. A bump lands between the admin's read and its write.
  await cell('D4 admin route re-stakes W2 while a counter bump lands', REG, tok(UA, 'SUPER_ADMIN'), { walletAddress: W2, stakedAmount: 60000 },
    { hooks: [{ label: 'PWRITE', times: 1, run: sec('UPDATE svc_governance_participants SET proposals_created = 9, votes_cast = 9 WHERE id = $1', [U2]) }] });
  await cell('D4b admin route new wallet WX (insert path; counters 0)', REG, tok(UA, 'SUPER_ADMIN'), { walletAddress: WX, stakedAmount: 5000 });
  // Q3 edges
  // D-3: an admin (second connection) creates U1's own row, staked, between U1's reads and its insert.
  await cell('Q3a U1 self-register; U1 row (staked 5000, DRep) appears before the insert', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 },
    { hooks: [{ label: 'PWRITE', times: 1, run: sec("INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power, is_drep) VALUES ($1,$2,5000,'staker',5000,true)", [U1, W1]) }] });
  await cell('Q3a2 U1 proposes; U1 row (staked 5000) appears before the auto-register insert', PROP, tok(U1), proposal,
    { hooks: [{ label: 'PWRITE', times: 1, run: sec("INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power, is_drep) VALUES ($1,$2,5000,'staker',5000,true)", [U1, W1]) }] });
  // D-3b: another id takes the wallet between the 409 pre-check and the write.
  await cell('Q3b U1 self-register; another id takes W1 before the insert', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 },
    { hooks: [{ label: 'PWRITE', times: 1, run: sec("INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power) VALUES ('race-other-id',$1,7000,'staker',7000)", [W1]) }] });
  await cell('Q3b2 U1 proposes; another id takes W1 before the auto-register insert', PROP, tok(U1), proposal,
    { hooks: [{ label: 'PWRITE', times: 1, run: sec("INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power) VALUES ('race-other-id',$1,7000,'staker',7000)", [W1]) }] });
  await cell('Q3b3 U5 re-registers (refresh path, linked W5); another id takes W5 before the refresh', REG, tok(U5), { walletAddress: W5, stakedAmount: 0 },
    { hooks: [{ label: 'PWRITE', times: 1, run: sec("INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power) VALUES ('race-other-id',$1,7000,'staker',7000)", [W5]) }] });
  // Counter bump on a row deleted between the read and the bump.
  await cell('Q3c U2 proposes; U2 row deleted before the bump', PROP, tok(U2), proposal,
    { hooks: [{ label: 'PWRITE', times: 1, run: sec('DELETE FROM svc_governance_participants WHERE id = $1', [U2]) }] });
  await cell('Q3c2 U2 votes; U2 row deleted before the bump', VOTE, tok(U2), { vote: 'for' },
    { hooks: [{ label: 'PWRITE', times: 1, run: sec('DELETE FROM svc_governance_participants WHERE id = $1', [U2]) }] });
  await cell('Q3c3 U2 re-registers; U2 row deleted before the refresh', REG, tok(U2), { walletAddress: W2, stakedAmount: 50000 },
    { hooks: [{ label: 'PWRITE', times: 1, run: sec('DELETE FROM svc_governance_participants WHERE id = $1', [U2]) }] });
  // ---- gate 136 delta cells (G134-F1/F2/F3 as built), deterministic, on real PG ----
  const e23505 = (constraint) => () => { const e = new Error(`duplicate key value violates unique constraint "${constraint}"`); e.code = '23505'; e.constraint = constraint; return e; };
  const WK = 'svc_governance_participants_wallet_address_key';
  const insOwn = (w) => () => second.query("INSERT INTO svc_governance_participants (id, wallet_address, did, staked_amount, tier, vote_power) VALUES ($1,$2,'did:gate136:landed',0,'basic',0)", [U1, w]);
  await cell('G1 U1 self-register; own row (U1,W1) lands, then the insert raises the WALLET 23505 (F1 deterministic)', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 },
    { faults: [{ label: 'INSERT-IF-ABSENT', times: 1, pre: insOwn(W1), value: e23505(WK) }] });
  await cell('G2 U1 self-register; own row lands holding ANOTHER wallet, then the wallet 23505 (expect 409)', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 },
    { faults: [{ label: 'INSERT-IF-ABSENT', times: 1, pre: insOwn('addr_test1_gate136_w1_other'), value: e23505(WK) }] });
  await cell('G3 U1 self-register; wallet 23505 and NO own row (expect 409, nothing written)', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 },
    { faults: [{ label: 'INSERT-IF-ABSENT', times: 1, value: e23505(WK) }] });
  await cell('G4 U1 self-register; 23505 under the PKEY name (expect 500, nothing written) (F3)', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 },
    { faults: [{ label: 'INSERT-IF-ABSENT', times: 1, value: e23505('svc_governance_participants_pkey') }] });
  await cell('G5 U1 proposes; 23505 under ANOTHER name at the auto-register insert (expect 500) (F3)', PROP, tok(U1), proposal,
    { faults: [{ label: 'INSERT-IF-ABSENT', times: 1, value: e23505('some_other_unique_key') }] });
  await cell('G6 U1 proposes; U1 OWN row (staked 5000) lands before the wallet pre-check (F2: expect 201 on that row)', PROP, tok(U1), proposal,
    { hooks: [{ label: 'byAddress', times: 1, run: sec("INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power) VALUES ($1,$2,5000,'staker',5000)", [U1, W1]) }] });
  await cell('G7 U1 proposes; ANOTHER id (staked) takes W1 before the wallet pre-check (F2: expect 409, nothing written)', PROP, tok(U1), proposal,
    { hooks: [{ label: 'byAddress', times: 1, run: sec("INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power) VALUES ('race-other-id',$1,5000,'staker',5000)", [W1]) }] });
  await cell('G8 U1 proposes; U1 OWN row (unstaked) lands before the wallet pre-check (F2: expect 400 min stake, row kept)', PROP, tok(U1), proposal,
    { hooks: [{ label: 'byAddress', times: 1, run: sec("INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power) VALUES ($1,$2,0,'basic',0)", [U1, W1]) }] });
  // Concurrent self-registers of a NEW user (no hook): RACE_N rounds, two requests in flight together.
  for (const [nm, a, b] of [
    ['Q3d selfreg || selfreg', [REG, tok(U1), { walletAddress: W1, stakedAmount: 0 }], [REG, tok(U1), { walletAddress: W1, stakedAmount: 0 }]],
    ['Q3e selfreg || propose (auto-register)', [REG, tok(U1), { walletAddress: W1, stakedAmount: 0 }], [PROP, tok(U1), proposal]],
  ]) {
    const hist = {}; const bad = []; let rowsOk = 0; let errLogs = {};
    for (let i = 0; i < RACE_N; i += 1) {
      await reset([]);
      const [ra, rb] = await Promise.all([call(...a), call(...b)]);
      const k = `${ra.status}${ra.body && ra.body.error ? ':' + ra.body.error.message.slice(0, 50) : ''} | ${rb.status}${rb.body && rb.body.error ? ':' + rb.body.error.message.slice(0, 50) : ''}`;
      hist[k] = (hist[k] || 0) + 1;
      const s = await snap();
      const u1 = s.participants.filter((p) => p.id === U1 || p.wallet_address === W1);
      if (u1.length === 1 && u1[0].id === U1 && u1[0].stake === '0') rowsOk += 1; else bad.push(u1);
      for (const l of logSpy.filter((x) => x.lv === 'error')) errLogs[l.msg + ' ' + JSON.stringify(l.meta && l.meta.error)] = (errLogs[l.msg + ' ' + JSON.stringify(l.meta && l.meta.error)] || 0) + 1;
    }
    appendFileSync(OUT, JSON.stringify({ cell: nm, rounds: RACE_N, hist, rowsOk, bad: bad.slice(0, 3), errLogs }) + '\n');
  }
  {
    const nm = 'Q3k selfreg U1 || another id inserts W1 on the second connection'; const hist = {}; const bad = []; let coherent = 0;
    for (let i = 0; i < RACE_N; i += 1) {
      await reset([]);
      const [ra, rb] = await Promise.allSettled([call(REG, tok(U1), { walletAddress: W1, stakedAmount: 0 }),
        second.query("INSERT INTO svc_governance_participants (id, wallet_address, staked_amount, tier, vote_power) VALUES ('race-other-id',$1,7000,'staker',7000)", [W1])]);
      const a = ra.value; const otherOk = rb.status === 'fulfilled';
      const k = `${a.status}${a.body && a.body.error ? ':' + a.body.error.message.slice(0, 50) : ''} | other ${otherOk ? 'inserted' : 'ERR ' + (rb.reason.code + ' ' + rb.reason.constraint)}`;
      hist[k] = (hist[k] || 0) + 1;
      const s = await snap();
      const holders = s.participants.filter((p) => p.wallet_address === W1);
      const u1row = s.participants.find((p) => p.id === U1);
      // coherent: exactly one holder; if the app said 201 it holds W1 (U1); if 409 the other id holds W1 and U1 has no row
      const ok = holders.length === 1 && ((a.status === 201 && holders[0].id === U1 && !otherOk) || (a.status === 409 && holders[0].id === 'race-other-id' && otherOk && !u1row));
      if (ok) coherent += 1; else bad.push({ k, holders, u1row });
    }
    appendFileSync(OUT, JSON.stringify({ cell: nm, rounds: RACE_N, hist, rowsOk: coherent, bad: bad.slice(0, 3), errLogs: {} }) + '\n');
  }
  // Q4: gate 129's KS-1942 property cells (D1a / D2a / D3a), re-run.
  await cell('a0 own wallet stake 0', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 });
  await cell('a1 own wallet stake 1e6', REG, tok(U1), { walletAddress: W1, stakedAmount: 1000000 });
  await cell('a2 own wallet isDRep true', REG, tok(U1), { walletAddress: W1, stakedAmount: 0, isDRep: true });
  await cell('a3 own wallet committee true', REG, tok(U1), { walletAddress: W1, stakedAmount: 0, isConstitutionalCommittee: true });
  await cell('a4 own wallet extras tier/votePower/id/role', REG, tok(U1), { walletAddress: W1, stakedAmount: 0, tier: 'whale', votePower: 1e9, id: 'forged', role: 'SUPER_ADMIN', proposalsCreated: 9, votesCast: 9 });
  await cell('a5 own wallet did + explicit false flags', REG, tok(U1), { walletAddress: W1, stakedAmount: 0, did: 'did:gate134:u1', isDRep: false, isConstitutionalCommittee: false });
  await cell('a6 role "admin" (not platform) stake 1e6', REG, tok(U1, 'admin'), { walletAddress: W1, stakedAmount: 1000000 });
  await cell('b1 names U2 wallet W2 stake 0', REG, tok(U1), { walletAddress: W2, stakedAmount: 0 });
  await cell('b2 names unregistered wallet', REG, tok(U1), { walletAddress: WX, stakedAmount: 1000000, isDRep: true });
  await cell('b3 no linked wallet', REG, tok(U3), { walletAddress: WX, stakedAmount: 0 });
  await cell('b5 T2 user, token tenant T1 (cross-tenant)', REG, tok(U4, 'user', T1), { walletAddress: W4, stakedAmount: 0 });
  await cell('b7 long-s role "ſuper_admin" names W2 stake 1e6', REG, tok(U1, 'ſuper_admin'), { walletAddress: W2, stakedAmount: 1000000 });
  await cell('b9 T2 user own wallet, own tenant T2 (control)', REG, tok(U4, 'user', T2), { walletAddress: W4, stakedAmount: 0 });
  await cell('c1 U2 re-registers own W2, stake 50000, flags omitted', REG, tok(U2), { walletAddress: W2, stakedAmount: 50000 });
  await cell('c2 U2 re-registers own W2 stake 0', REG, tok(U2), { walletAddress: W2, stakedAmount: 0 });
  await cell('c3 U2 re-registers own W2 isDRep false', REG, tok(U2), { walletAddress: W2, stakedAmount: 50000, isDRep: false });
  await cell('c4 legacy row holds W1 under another id', REG, tok(U1), { walletAddress: W1, stakedAmount: 7000 }, { seed: [legacy] });
  await cell('c5 legacy self row re-registers W1 stake 1000', REG, tok(U1), { walletAddress: W1, stakedAmount: 1000 }, { seed: [legacySelf] });
  await cell('c6 legacy self row re-registers W1 stake 0', REG, tok(U1), { walletAddress: W1, stakedAmount: 0 }, { seed: [legacySelf] });
  await cell('d1 SUPER_ADMIN sets W2 stake 200000 isDRep false', REG, tok(UA, 'SUPER_ADMIN'), { walletAddress: W2, stakedAmount: 200000, isDRep: false });
  await cell('d3 super_admin re-registers W2 flags omitted', REG, tok(UA, 'super_admin'), { walletAddress: W2, stakedAmount: 50000 });
  await cell('f1 unregistered U1 proposes', PROP, tok(U1), proposal);
  await cell('f2 staked U2 proposes (control)', PROP, tok(U2), proposal);
  await cell('f3 U3 (no linked wallet) proposes', PROP, tok(U3), proposal);
  await cell('f4 U1 proposes, legacy row holds W1', PROP, tok(U1), proposal, { seed: [legacy] });
  await cell('v1 U2 votes (control)', VOTE, tok(U2), { vote: 'for' });
  await cell('v2 U1 (no row) votes', VOTE, tok(U1), { vote: 'for' });
  await cell('v3 U2 votes with body votePower/stake extras', VOTE, tok(U2), { vote: 'for', votePower: 1e12, stakedAmount: 1e12 });
}, 900000);
