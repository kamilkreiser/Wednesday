/* Gate 111 probe (KS-1868 PR 1929). Real db.ts (initDb/runDbReadyHook), real governanceService,
 * real governance router + real @secuura/shared errorHandler over a loopback socket, REAL winston
 * logger (call-through wrapper on logger.error/warn/info records arguments, then calls the real one).
 * Replaced: the `pg` Pool (stateful fake), console.log (dbLog capture), net connect (guard: records
 * every target; anything not loopback is refused and counted). */
import * as fs from 'fs';
import * as net from 'net';

const OUT = process.env.PROBE_OUT as string;
const VER = process.env.PROBE_VER as string;
const NODEENV = process.env.PROBE_NODE_ENV || 'test';

// ---------- network guard ----------
const netTargets: string[] = [];
const origConnect = (net.Socket.prototype as any).connect;
(net.Socket.prototype as any).connect = function (...args: any[]) {
  let host = 'unknown';
  const a0 = args[0];
  if (a0 && typeof a0 === 'object') host = String(a0.host ?? a0.path ?? 'localhost');
  else if (typeof a0 === 'number') host = typeof args[1] === 'string' ? args[1] : 'localhost';
  else if (typeof a0 === 'string') host = 'ipc:' + a0;
  netTargets.push(host);
  if (!/^(127\.0\.0\.1|localhost|::1|::ffff:127\.0\.0\.1)$/.test(host)) {
    throw new Error('G111 network guard: refused outbound connect to ' + host);
  }
  return origConnect.apply(this, args);
};

// ---------- fake pg ----------
type Row = Record<string, any>;
const fake: {
  participants: Row[];
  proposals: Row[];
  ops: string[];
  seedThrow: { on: boolean; value: unknown };
  lookupThrow: { on: boolean; value: unknown };
  maxNum: number;
} = { participants: [], proposals: [], ops: [], seedThrow: { on: false, value: undefined }, lookupThrow: { on: false, value: undefined }, maxNum: 7 };
(globalThis as any).__g111fake = fake;

jest.mock('pg', () => {
  class Pool {
    on() { return this; }
    async query(text: string, params?: any[]) {
      const f = (globalThis as any).__g111fake;
      const s = String(text).replace(/\s+/g, ' ').trim();
      const head = s.slice(0, 60);
      f.ops.push(head + ' | ' + JSON.stringify((params || []).map((p: any) => (p instanceof Date ? '<date>' : p))));
      if (/^SELECT 1 AS ok/i.test(s)) return { rows: [{ ok: 1 }] };
      if (/MAX\(proposal_number\)/i.test(s)) {
        if (f.seedThrow.on) throw f.seedThrow.value;
        return { rows: [{ max_num: f.maxNum }] };
      }
      if (/^SELECT \* FROM svc_governance_participants WHERE id = \$1/i.test(s)) {
        if (f.lookupThrow.on) throw f.lookupThrow.value;
        return { rows: f.participants.filter((r: Row) => r.id === params![0]).map((r: Row) => ({ ...r })) };
      }
      if (/^SELECT \* FROM svc_governance_participants WHERE wallet_address = \$1/i.test(s)) {
        return { rows: f.participants.filter((r: Row) => r.wallet_address === params![0]).map((r: Row) => ({ ...r })) };
      }
      if (/^SELECT \* FROM svc_governance_participants/i.test(s)) return { rows: f.participants.map((r: Row) => ({ ...r })) };
      if (/^INSERT INTO svc_governance_participants/i.test(s)) {
        const p = params!;
        const row: Row = { id: p[0], wallet_address: p[1], did: p[2], staked_amount: p[3], tier: p[4], vote_power: p[5],
          is_drep: p[6], is_constitutional_committee: p[7], proposals_created: p[8], votes_cast: p[9], last_active_at: '<date>', joined_at: '<date>' };
        const i = f.participants.findIndex((r: Row) => r.id === row.id);
        if (i >= 0) {
          const o = f.participants[i];
          f.participants[i] = { ...o, staked_amount: row.staked_amount, tier: row.tier, vote_power: row.vote_power, is_drep: row.is_drep,
            proposals_created: row.proposals_created, votes_cast: row.votes_cast, last_active_at: '<date>' };
        } else f.participants.push(row);
        return { rows: [], rowCount: 1 };
      }
      if (/^DELETE FROM svc_governance_participants WHERE id = \$1/i.test(s)) {
        const n = f.participants.length;
        f.participants = f.participants.filter((r: Row) => r.id !== params![0]);
        return { rows: [], rowCount: n - f.participants.length };
      }
      if (/^SELECT \* FROM svc_proposals/i.test(s)) return { rows: [] };
      if (/^SELECT \* FROM svc_vote_delegations/i.test(s)) return { rows: [] };
      if (/^INSERT INTO svc_proposals/i.test(s)) {
        f.proposals.push({ id: params![0], proposer_id: params![4], proposer_address: params![5], status: params![6] });
        return { rows: [], rowCount: 1 };
      }
      return { rows: [], rowCount: 0 };
    }
    async connect() { throw new Error('G111: connect not supported'); }
    async end() {}
  }
  return { Pool };
});

// ---------- thrown values ----------
function revoked(): any { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function errWithMsgGetter(get: () => any): any { return Object.create(Error.prototype, { message: { get } }); }
const VALUES: Record<string, () => unknown> = {
  none: () => undefined,
  ordinary: () => new Error('db down at 10.0.0.7 password=hunter2'),
  revoked: () => revoked(),
  getterThrows: () => errWithMsgGetter(() => { throw new Error('getter boom'); }),
  nullProto: () => Object.create(null),
  plainString: () => 'plain string reason',
  undef: () => undefined,
  msgRevoked: () => errWithMsgGetter(() => revoked()),
  msgSymbol: () => errWithMsgGetter(() => Symbol('sym')),
  msgToStrThrows: () => errWithMsgGetter(() => ({ toString() { throw new Error('toString boom'); } })),
  msgNullProto: () => errWithMsgGetter(() => Object.create(null)),
};

function safeDesc(v: unknown): string {
  try {
    if (v === undefined) return 'undefined';
    if (v === null) return 'null';
    const t = typeof v;
    if (t === 'string') return 'str:' + (v as string);
    if (t === 'symbol') return 'symbol';
    if (t === 'object') {
      try { return 'object:' + JSON.stringify(v); } catch (e) { return 'object:<unserialisable>'; }
    }
    return t + ':' + String(v);
  } catch { return '<undescribable>'; }
}
function errName(e: unknown): string {
  try { return (e as any)?.constructor?.name + ':' + String((e as any)?.message).slice(0, 80); } catch { return '<unreadable rejection>'; }
}

function maskAll(x: any): any {
  const s = JSON.stringify(x);
  const map = new Map<string, string>();
  return JSON.parse(
    s.replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/g, (m) => {
      if (!map.has(m)) map.set(m, '<uuid' + map.size + '>');
      return map.get(m)!;
    }).replace(/\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+Z/g, '<date>')
  );
}

const unhandled: string[] = [];
process.on('unhandledRejection', (r) => { unhandled.push(errName(r)); });

const records: any[] = [];
function rec(r: any) { records.push(maskAll({ ver: VER, nodeEnv: NODEENV, ...r })); }

describe('g111 probe', () => {
  afterAll(() => { fs.appendFileSync(OUT, records.map((r) => JSON.stringify(r)).join('\n') + '\n'); });

  for (const scen of Object.keys(VALUES)) {
    it('scenario ' + scen, async () => {
      fake.participants = []; fake.proposals = []; fake.ops = [];
      fake.seedThrow = { on: scen !== 'none', value: undefined };
      fake.lookupThrow = { on: false, value: undefined };
      process.env.DATABASE_URL = 'postgres://g111:stub@127.0.0.1:1/none';
      process.env.NODE_ENV = NODEENV;
      const logs: any[] = [];
      const consoleLines: string[] = [];
      const origLog = console.log;
      console.log = (...a: any[]) => { consoleLines.push(a.map((x) => (typeof x === 'string' ? x : '<obj>')).join(' ')); };
      const u0 = unhandled.length;
      let mods: any;
      jest.isolateModules(() => {
        const db = require('../db');
        const loggerMod = require('../utils/logger');
        const svc = require('../services/governanceService');
        const { governanceRoutes } = require('../routes/governance');
        const { errorHandler } = require('@secuura/shared');
        mods = { db, loggerMod, svc, governanceRoutes, errorHandler };
      });
      const L = mods.loggerMod.logger;
      for (const lvl of ['error', 'warn', 'info']) {
        const orig = L[lvl].bind(L);
        L[lvl] = (msg: any, meta?: any) => {
          const entry: any = { lvl, msg: typeof msg === 'string' ? msg : '<non-string>' };
          if (meta && typeof meta === 'object') {
            entry.keys = Object.keys(meta);
            entry.errorType = typeof meta.error;
            entry.error = safeDesc(meta.error);
          }
          try { const r = orig(msg, meta); entry.loggerThrew = false; logs.push(entry); return r; }
          catch (e) { entry.loggerThrew = errName(e); logs.push(entry); throw e; }
        };
      }
      try {
        // 1. real boot path: initDb(() => verifyDbReady()), as index.ts wires it
        fake.seedThrow.value = VALUES[scen]();
        let initOut: any;
        try { initOut = { resolved: await mods.db.initDb(() => mods.svc.verifyDbReady()) }; } catch (e) { initOut = { rejected: errName(e) }; }
        const bootLogs = logs.splice(0); const bootConsole = consoleLines.splice(0);
        await new Promise((r) => setTimeout(r, 20));
        rec({ scen, kind: 'boot', initOut, logs: bootLogs, dbLog: bootConsole, opsCount: fake.ops.length, writes: fake.ops.filter((o) => /^(INSERT|UPDATE|DELETE)/i.test(o)).length, unhandled: unhandled.length - u0 });

        // 2. direct verifyDbReady call (db flagged available by initDb)
        fake.ops = [];
        fake.seedThrow.value = VALUES[scen]();
        let direct: any;
        try { direct = { resolved: String(await mods.svc.verifyDbReady()) }; } catch (e) { direct = { rejected: errName(e) }; }
        const dLogs = logs.splice(0);
        rec({ scen, kind: 'direct', direct, logs: dLogs, ops: fake.ops.slice(), writes: fake.ops.filter((o) => /^(INSERT|UPDATE|DELETE)/i.test(o)).length });

        // 3. routes (KS-1940 path), seed stays as in this scenario
        const express = require('express');
        const app = express();
        app.use(express.json());
        app.use((req: any, _res: any, next: any) => { req.user = { userId: req.headers['x-g111-user'] || 'user-A', tenantId: 't1' }; next(); });
        app.use('/api/governance', mods.governanceRoutes);
        app.use(mods.errorHandler);
        const server: any = await new Promise((res) => { const s = app.listen(0, '127.0.0.1', () => res(s)); });
        const base = 'http://127.0.0.1:' + server.address().port;
        const prop = { title: 'Gate 111 probe proposal', description: 'x'.repeat(60), category: 'general' };
        const step = async (name: string, method: string, path: string, user: string, body?: any) => {
          fake.ops = [];
          const ub = unhandled.length;
          const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 1500);
          let r: any;
          try {
            const resp = await fetch(base + path, { method, headers: { 'content-type': 'application/json', 'x-g111-user': user }, body: body ? JSON.stringify(body) : undefined, signal: ctl.signal });
            const txt = await resp.text(); let j: any = txt; try { j = JSON.parse(txt); } catch { /**/ }
            r = { status: resp.status, body: j };
          } catch (e: any) { r = { status: 'NO_RESPONSE', body: String(e?.name) }; } finally { clearTimeout(t); }
          await new Promise((res) => setTimeout(res, 20));
          rec({ scen, kind: 'route', step: name, res: r, ops: fake.ops.slice(), logs: logs.splice(0), participants: fake.participants.map((x) => ({ ...x })), proposals: fake.proposals.map((x) => ({ ...x })), unhandled: unhandled.length - ub });
        };
        fake.seedThrow.on = false; // routes do not re-seed
        await step('R1 register new wallet', 'POST', '/api/governance/participants/register', 'user-A', { walletAddress: 'addr_new', stakedAmount: 5000 });
        await step('R2 get by wallet', 'GET', '/api/governance/participants/addr_new', 'user-A');
        await step('R3 createProposal unknown proposer (auto-register)', 'POST', '/api/governance/proposals', 'user-A', prop);
        await step('R4 get user-A', 'GET', '/api/governance/participants/user-A', 'user-A');
        fake.participants.push({ id: 'user-B', wallet_address: 'addr_B', did: null, staked_amount: 99999, tier: 'whale', vote_power: 777, is_drep: true, is_constitutional_committee: false, proposals_created: 3, votes_cast: 9, last_active_at: '<date>', joined_at: '<date>' });
        fake.lookupThrow = { on: true, value: new Error('lookup down') };
        await step('R5 createProposal user-B, lookup ordinary Error (KS-1940)', 'POST', '/api/governance/proposals', 'user-B', prop);
        fake.lookupThrow = { on: true, value: revoked() };
        await step('R6 createProposal user-B, lookup revoked Proxy (KS-1940/O73-P1 held)', 'POST', '/api/governance/proposals', 'user-B', prop);
        fake.lookupThrow = { on: true, value: new Error('lookup down') };
        await step('R7 GET user-B, lookup ordinary Error', 'GET', '/api/governance/participants/user-B', 'user-B');
        fake.lookupThrow = { on: true, value: revoked() };
        await step('R8 GET user-B, lookup revoked Proxy (no route catch)', 'GET', '/api/governance/participants/user-B', 'user-B');
        fake.lookupThrow = { on: false, value: undefined };
        await step('R9 register addr_B again (duplicate-row check)', 'POST', '/api/governance/participants/register', 'user-B', { walletAddress: 'addr_B', stakedAmount: 10 });
        await new Promise((res) => server.close(res));
      } finally {
        console.log = origLog;
      }
    });
  }

  it('network guard summary', () => {
    const outbound = netTargets.filter((h) => !/^(127\.0\.0\.1|localhost|::1|::ffff:127\.0\.0\.1)$/.test(h));
    rec({ kind: 'net', targets: Array.from(new Set(netTargets)), connects: netTargets.length, outbound });
  });
});
