// Gate 147 probe (kyc): the REAL kyc index.ts (real dbDeleteUserData, real `log`, real userErasedSubscriber) and the REAL
// shared EventBus subscribe loop (retry x3, dead-letter, ack). Replaced: ../db (an in-memory table store that answers the
// erasure SQL and records every statement), ioredis (the bus's private client swapped for a recording fake after the real
// EventBus is constructed), ../subjectDeks (records evict), express listen (no port). Output: JSON lines to PROBE_OUT.
import { describe, it, expect, vi, afterAll } from 'vitest';
import fs from 'fs';

process.env.KYC_PROVIDER = 'mock';
process.env.NODE_ENV = 'test';
process.env.REDIS_URL = 'redis://stub.invalid:6379';

const h = vi.hoisted(() => {
  const st: any = {
    tables: { images: [] as any[], consents: [] as any[], verifications: [] as any[] },
    stmts: [] as string[], failRe: null as RegExp | null, failLeft: 0, toThrow: undefined as unknown,
    evicted: [] as string[], bus: null as any, xadds: [] as unknown[][], xacks: [] as string[], queue: [] as any[],
    handlerOutcomes: [] as any[], logs: [] as string[],
  };
  st.redis = {
    status: 'ready', on() { return this; }, disconnect() {}, connect: async () => undefined,
    xgroup: async () => 'OK',
    xreadgroup: async () => {
      if (st.queue.length) return [['secuura:events:user.erased', st.queue.splice(0)]];
      await new Promise((r) => setTimeout(r, 3));
      return null;
    },
    xack: async (_s: string, _g: string, id: string) => { st.xacks.push(id); return 1; },
    xadd: async (...a: unknown[]) => { st.xadds.push(a); return 'dl-1'; },
  };
  return st;
});

const del = (t: any[], pred: (r: any) => boolean) => { let n = 0; for (let i = t.length - 1; i >= 0; i--) if (pred(t[i])) { t.splice(i, 1); n++; } return n; };
vi.mock('../db', () => ({
  initDb: () => new Promise<boolean>(() => {}),
  isDbAvailable: () => true,
  query: (sql: string, params?: any[]) => {
    const s = String(sql).replace(/\s+/g, ' ').trim();
    if (/svc_kyc_/.test(s)) h.stmts.push(s);
    if (h.failRe && h.failRe.test(s) && h.failLeft > 0) { h.failLeft--; return Promise.reject(h.toThrow); }
    const T = h.tables;
    if (/^SELECT \* FROM svc_kyc_verifications WHERE user_id = \$1/.test(s)) return Promise.resolve({ rows: T.verifications.filter((r: any) => r.user_id === params![0]).map((r: any) => ({ ...r })), rowCount: 0 });
    if (/^DELETE FROM svc_kyc_images WHERE id = ANY/.test(s)) return Promise.resolve({ rows: [], rowCount: del(T.images, (r: any) => params![0].includes(r.id)) });
    if (/^DELETE FROM svc_kyc_images WHERE user_id/.test(s)) return Promise.resolve({ rows: [], rowCount: del(T.images, (r: any) => r.user_id === params![0]) });
    if (/^DELETE FROM svc_kyc_consents WHERE user_id/.test(s)) return Promise.resolve({ rows: [], rowCount: del(T.consents, (r: any) => r.user_id === params![0]) });
    if (/^DELETE FROM svc_kyc_verifications WHERE user_id/.test(s)) { const ids = T.verifications.filter((r: any) => r.user_id === params![0]).map((r: any) => r.id); del(T.consents, (c: any) => ids.includes(c.verification_id)); return Promise.resolve({ rows: [], rowCount: del(T.verifications, (r: any) => r.user_id === params![0]) }); }
    return Promise.resolve({ rows: [], rowCount: 0 });
  },
}));
vi.mock('../subjectDeks', () => ({
  subjectDeks: { getOrCreateDek: async () => Buffer.alloc(32, 7), getDek: async () => Buffer.alloc(32, 7), evict: (u: string) => { h.evicted.push(u); } },
}));
vi.mock('express', async (importOriginal) => {
  const actual: any = (await importOriginal<any>()).default ?? (await importOriginal<any>());
  const factory: any = (...args: any[]) => { const app = actual(...args); app.listen = () => ({ close: (cb?: () => void) => cb?.(), address: () => ({ port: 0 }), on() { return this; } }); return app; };
  Object.assign(factory, actual);
  return { ...actual, default: factory };
});
vi.mock('@secuura/shared', async (importOriginal) => {
  const actual: any = await importOriginal();
  return {
    ...actual,
    initEventBus: (url: string, name: string) => {
      const bus = new actual.EventBus(url, name);
      try { bus.redis.disconnect(); } catch { /* lazy, never connected */ }
      bus.redis = h.redis; // only the Redis client is replaced; subscribe() below is the real loop
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

const logSpy = vi.spyOn(console, 'log').mockImplementation((...a: unknown[]) => { const s = String(a[0]); if (s.includes('[cascade]')) h.logs.push(s); });

await import('../index');

const U = 'g147-subject', O = 'g147-other';
function seed() {
  h.tables.images = [{ id: 'img-legacy-front', user_id: null }, { id: 'img-legacy-back', user_id: null }, { id: 'img-new', user_id: U }, { id: 'img-other', user_id: O }];
  h.tables.verifications = [
    { id: 'v1', user_id: U, status: 'approved', provider: 'mock', provider_application_id: 'app-subject', documents: JSON.stringify([{ type: 'passport', frontImageId: 'img-legacy-front', backImageId: 'img-legacy-back' }]), checks: '[]', created_at: new Date(), updated_at: new Date() },
    { id: 'v2', user_id: O, status: 'approved', provider: 'mock', documents: '[]', checks: '[]', created_at: new Date(), updated_at: new Date() },
  ];
  h.tables.consents = [{ id: 'c1', user_id: U, verification_id: 'v1', ip_address: '203.0.113.7', user_agent: 'UA-subject' }, { id: 'c2', user_id: O, verification_id: 'v2' }];
}
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMsg = (m: unknown) => Object.create(Error.prototype, { message: { get() { return m; } } });
const VALUES: Array<[string, () => unknown]> = [
  ['ordinaryError', () => new Error('delete failed: relation "svc_kyc_consents" lock timeout')],
  ['string', () => 'plain boom'],
  ['null', () => null],
  ['bigintThrown', () => BigInt(10)],
  ['revokedProxy', revoked],
  ['getterThrows', () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } })],
  ['msgBigInt', () => withMsg(BigInt(10))],
  ['msgSymbol', () => withMsg(Symbol('ks1868'))],
  ['msgObjectWithPii', () => withMsg({ email: 'subject@example.test' })],
];
const FAILS: Array<[string, RegExp | null, number]> = [
  ['none', null, 0],
  ['imagesById-always', /^DELETE FROM svc_kyc_images WHERE id = ANY/, 99],
  ['consents-always', /^DELETE FROM svc_kyc_consents/, 99],
  ['verifications-always', /^DELETE FROM svc_kyc_verifications/, 99],
  ['consents-once', /^DELETE FROM svc_kyc_consents/, 1],
];
const OUT = process.env.PROBE_OUT!;
let n = 0;
async function runCase(fail: [string, RegExp | null, number], val: [string, () => unknown]) {
  seed(); h.stmts = []; h.evicted = []; h.xadds = []; h.handlerOutcomes = []; h.logs = [];
  h.failRe = fail[1]; h.failLeft = fail[2]; h.toThrow = val[1]();
  const msgId = `1-${++n}`;
  h.queue.push([msgId, ['event', JSON.stringify({ type: 'user.erased', payload: { userId: U, dsrId: 'dsr-g147' }, timestamp: 'x', source: 'originate' })]]);
  for (let i = 0; i < 400 && !h.xacks.includes(msgId); i++) await new Promise((r) => setTimeout(r, 5));
  const T = h.tables;
  const rec = {
    ver: process.env.PROBE_VER, fail: fail[0], value: val[0], acked: h.xacks.includes(msgId),
    attempts: h.handlerOutcomes.length, outcomes: h.handlerOutcomes,
    deadLetter: h.xadds.map((a) => ({ stream: a[0], fields: a.slice(2).filter((_, i) => i % 2 === 0), error: a[a.length - 1] })),
    subjectLeft: { images: T.images.filter((r: any) => r.id !== 'img-other').map((r: any) => r.id), consents: T.consents.filter((r: any) => r.user_id === U).map((r: any) => r.id), verifications: T.verifications.filter((r: any) => r.user_id === U).map((r: any) => r.id) },
    otherLeft: { images: T.images.some((r: any) => r.id === 'img-other'), consents: T.consents.some((r: any) => r.id === 'c2'), verifications: T.verifications.some((r: any) => r.id === 'v2') },
    evicted: h.evicted.length, stmts: h.stmts.map((s) => s.slice(0, 55)), logs: h.logs,
  };
  fs.appendFileSync(OUT, JSON.stringify(rec) + '\n');
  return rec;
}

describe('g147 kyc probe', () => {
  for (const f of FAILS) for (const v of (f[0] === 'none' ? VALUES.slice(0, 1) : VALUES)) {
    it(`${f[0]} / ${v[0]}`, async () => { const r = await runCase(f, v); expect(r.acked).toBe(true); });
  }
});
afterAll(async () => { await h.bus?.shutdown(); logSpy.mockRestore(); });
