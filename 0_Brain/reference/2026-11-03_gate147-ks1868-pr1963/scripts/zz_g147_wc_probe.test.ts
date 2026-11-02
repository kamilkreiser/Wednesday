// Gate 147 probe (wallet-connector): the REAL server.ts (real userErasedSubscriber wiring and real winston logger, in the
// format PROBE_FMT=dev|prod) and the REAL shared EventBus subscribe loop. Replaced: ../db (in-memory svc_wallet_sessions,
// records statements), the bus's Redis client (recording fake), initDb never settles (no listen).
import { describe, it, expect, vi, afterAll } from 'vitest';
import fs from 'fs';

process.env.REDIS_URL = 'redis://stub.invalid:6379';

const h = vi.hoisted(() => {
  const st: any = { sessions: [] as any[], stmts: [] as string[], failLeft: 0, toThrow: undefined as unknown, bus: null as any,
    xadds: [] as unknown[][], xacks: [] as string[], queue: [] as any[], handlerOutcomes: [] as any[], logs: [] as string[] };
  st.redis = {
    status: 'ready', on() { return this; }, disconnect() {}, connect: async () => undefined, xgroup: async () => 'OK',
    xreadgroup: async () => { if (st.queue.length) return [['secuura:events:user.erased', st.queue.splice(0)]]; await new Promise((r) => setTimeout(r, 3)); return null; },
    xack: async (_s: string, _g: string, id: string) => { st.xacks.push(id); return 1; },
    xadd: async (...a: unknown[]) => { st.xadds.push(a); return 'dl-1'; },
  };
  return st;
});
vi.mock('../db', () => ({
  initDb: () => new Promise<boolean>(() => {}),
  isDbAvailable: () => true,
  query: async (sql: string, params?: any[]) => {
    const s = String(sql).replace(/\s+/g, ' ').trim();
    if (/svc_wallet_sessions/.test(s)) h.stmts.push(s.slice(0, 60));
    if (/^DELETE FROM svc_wallet_sessions WHERE address/.test(s)) {
      if (h.failLeft > 0) { h.failLeft--; throw h.toThrow; }
      let n = 0; for (let i = h.sessions.length - 1; i >= 0; i--) if (h.sessions[i].address === params![0]) { h.sessions.splice(i, 1); n++; }
      return { rows: [], rowCount: n };
    }
    return { rows: [], rowCount: 0 };
  },
}));
vi.mock('../utils/logger', async (importOriginal) => {
  const actual: any = await importOriginal();
  const prev = process.env.NODE_ENV;
  process.env.NODE_ENV = process.env.PROBE_FMT === 'prod' ? 'production' : 'test';
  const logger = actual.createLogger('wallet-connector');
  process.env.NODE_ENV = prev;
  for (const t of logger.transports) {
    t.log = (info: any, cb: () => void) => { const s = String(info[Symbol.for('message')]); if (s.includes('[cascade]')) h.logs.push(s); cb?.(); };
  }
  return { ...actual, logger };
});
vi.mock('@secuura/shared', async (importOriginal) => {
  const actual: any = await importOriginal();
  return {
    ...actual,
    initEventBus: (url: string, name: string) => {
      const bus = new actual.EventBus(url, name);
      try { bus.redis.disconnect(); } catch { /* never connected */ }
      bus.redis = h.redis;
      const realSubscribe = bus.subscribe.bind(bus);
      bus.subscribe = (types: any, group: any, handler: any, opts: any) => realSubscribe(types, group, async (ev: any) => {
        try { await handler(ev); h.handlerOutcomes.push({ ok: true }); } catch (e) { h.handlerOutcomes.push({ ok: false, sameAsThrown: Object.is(e, h.toThrow), kind: kindOf(e) }); throw e; }
      }, opts);
      h.bus = bus;
    },
    getEventBus: () => h.bus,
  };
  function kindOf(v: unknown): string { try { if (v === null) return 'null'; if (typeof v !== 'object') return typeof v; return Object.prototype.toString.call(v) + ':' + (v instanceof TypeError ? 'TypeError' : v instanceof Error ? 'Error' : 'other'); } catch { return 'unreadable'; } }
});

await import('../server');

const ADDR = 'addr_test1_g147_subject';
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMsg = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const VALUES: Array<[string, () => unknown]> = [
  ['ordinaryError', () => new Error('connection terminated unexpectedly')],
  ['string', () => 'plain boom'],
  ['null', () => null],
  ['bigintThrown', () => BigInt(10)],
  ['revokedProxy', revoked],
  ['getterThrows', () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } })],
  ['msgBigInt', () => withMsg(BigInt(10))],
  ['msgSymbol', () => withMsg(Symbol('ks1868'))],
  ['msgObjectWithPii', () => withMsg({ email: 'subject@example.test' })],
];
const FAILS: Array<[string, number]> = [['none', 0], ['delete-always', 99], ['delete-once', 1]];
let n = 0;
async function runCase(f: [string, number], v: [string, () => unknown]) {
  h.sessions = [{ id: 's1', address: ADDR, wallet_type: 'nami' }, { id: 's2', address: ADDR, wallet_type: 'eternl' }, { id: 's3', address: 'addr_other' }];
  h.stmts = []; h.xadds = []; h.handlerOutcomes = []; h.logs = []; h.failLeft = f[1]; h.toThrow = v[1]();
  const msgId = `1-${++n}`;
  h.queue.push([msgId, ['event', JSON.stringify({ type: 'user.erased', payload: { userId: 'g147-subject', dsrId: 'dsr-g147', walletAddress: ADDR }, timestamp: 'x', source: 'originate' })]]);
  for (let i = 0; i < 400 && !h.xacks.includes(msgId); i++) await new Promise((r) => setTimeout(r, 5));
  const rec = { ver: process.env.PROBE_VER, fmt: process.env.PROBE_FMT, fail: f[0], value: v[0], acked: h.xacks.includes(msgId), attempts: h.handlerOutcomes.length,
    outcomes: h.handlerOutcomes, deadLetter: h.xadds.map((a) => ({ stream: a[0], error: a[a.length - 1] })),
    subjectSessionsLeft: h.sessions.filter((s: any) => s.address === ADDR).map((s: any) => s.id), otherLeft: h.sessions.some((s: any) => s.id === 's3'),
    stmts: h.stmts.length, logs: h.logs };
  fs.appendFileSync(process.env.PROBE_OUT!, JSON.stringify(rec) + '\n');
  return rec;
}
describe('g147 wallet-connector probe', () => {
  for (const f of FAILS) for (const v of (f[0] === 'none' ? VALUES.slice(0, 1) : VALUES)) it(`${f[0]} / ${v[0]}`, async () => { expect((await runCase(f, v)).acked).toBe(true); });
});
afterAll(async () => { await h.bus?.shutdown(); });
