
// ---- gate 154 probe: real index.ts routes, real oauthState.ts, REAL winston logger; only ./db, exchangeAuthCode, authenticate, express.listen, Graph fetch replaced
import fs from 'fs';
const OUT = process.env.G154_OUT as string;
const unhandled: string[] = [];
process.on('unhandledRejection', (r) => { let t = 'unreadable'; try { t = String((r as any)?.message ?? r); } catch { /* */ } unhandled.push(t); });

const revoked = (): unknown => { const rp = Proxy.revocable({}, {}); rp.revoke(); return rp.proxy; };
const getterThrows = (): unknown => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
const KINDS: Array<[string, () => unknown]> = [
  ['error', () => new Error('db boom')],
  ['revokedProxy', revoked],
  ['getterThrows', getterThrows],
  ['null', () => null],
  ['undefined', () => undefined],
  ['string', () => 'str boom'],
  ['number', () => 42],
  ['plainObjectMessage', () => ({ message: 'x' })],
  ['symbolMessage', () => new (class extends Error { constructor() { super('s'); Object.defineProperty(this, 'message', { value: Symbol('m') }); } })()],
  ['toStringThrows', () => ({ message: { toString() { throw new Error('ts boom'); } } })],
];

async function cbT(state: string, code: string, cookie = '') {
  try {
    const res = await realFetch(`${base}/api/callback?code=${encodeURIComponent(code)}&state=${encodeURIComponent(state)}`, { redirect: 'manual', headers: cookie ? { cookie } : {}, signal: AbortSignal.timeout(2500) });
    const loc = res.headers.get('location') || '';
    const u = new URL(loc || 'http://none.invalid/');
    return { answered: true, status: res.status, m365: u.searchParams.get('m365'), message: u.searchParams.get('message') };
  } catch { return { answered: false, status: 0, m365: null, message: null }; }
}
async function initT() {
  try {
    const res = await realFetch(`${base}/api/connections/init`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}', signal: AbortSignal.timeout(2500) });
    const body: any = await res.json().catch(() => ({}));
    const authUrl = new URL(body?.data?.authorizationUrl ?? 'http://none.invalid/');
    const pair = (res.headers.get('set-cookie') ?? '').split(';')[0] ?? '';
    return { answered: true, status: res.status, connId: String(body?.data?.connectionId), state: authUrl.searchParams.get('state') ?? '', cookie: pair.includes('=') ? pair : '' };
  } catch { return { answered: false, status: 0, connId: '', state: '', cookie: '' }; }
}
const warns: Array<{ msg: string; err: string }> = [];
describe('gate 154 probe', () => {
  beforeAll(async () => {
    const { logger } = await import('../utils/logger');
    const orig = logger.warn.bind(logger);
    (logger as any).warn = (msg: any, meta?: any) => {
      if (typeof msg === 'string' && /OAuth state failed/.test(msg)) { const e = meta?.error; warns.push({ msg, err: typeof e === 'string' ? e : '<' + typeof e + '>' }); }
      return (orig as any)(msg, meta);
    };
  });
  for (const [name, mk] of KINDS) {
    it(`consume ${name}`, async () => {
      as(ORG_A); const i = await initT();
      seen.exchanged.length = 0; warns.length = 0; const u0 = unhandled.length;
      seen.consumeThrow = { on: true, value: mk() };
      const r = await cbT(i.state, 'good-c', i.cookie);
      seen.consumeThrow = { on: false, value: undefined };
      const st = await statusOf(i.connId, ORG_A);
      const exchangedAfterThrow = seen.exchanged.length;
      const replay = await cbT(i.state, 'good-replay', i.cookie);
      fs.appendFileSync(OUT, JSON.stringify({ site: 'consume', kind: name, ...r, exchanged: exchangedAfterThrow, connStatus: st, unhandled: unhandled.length - u0, warn: warns.map((w) => w.err), replay: [replay.m365, replay.message], replayExchanged: seen.exchanged.length }) + '\n');
    });
    it(`save ${name}`, async () => {
      as(ORG_A);
      seen.exchanged.length = 0; warns.length = 0; const u0 = unhandled.length;
      seen.insertThrow = { on: true, value: mk() };
      const i = await initT();
      seen.insertThrow = { on: false, value: undefined };
      const w = warns.map((x) => x.err);
      const r = await cbT(i.state, 'good-s', i.cookie);
      const st = i.connId ? await statusOf(i.connId, ORG_A) : 'n/a';
      fs.appendFileSync(OUT, JSON.stringify({ site: 'save', kind: name, initAnswered: i.answered, initStatus: i.status, hasCookie: !!i.cookie, hasState: !!i.state, warn: w, unhandled: unhandled.length - u0, cb: [r.answered, r.m365, r.message], exchanged: seen.exchanged.length, connStatus: st }) + '\n');
    });
  }
});
