// gate 104 probe (NOT part of the PR). Real signatories + thirdPartyVerifiers routers on a loopback listener; a stateful db stand-in.
import * as fs from 'fs';
import type { AddressInfo } from 'net';

const OUT = process.env.PROBE_OUT as string;
const emit = (o: unknown) => fs.appendFileSync(OUT, JSON.stringify(o) + '\n');

type Mode = { kind: 'none' } | { kind: 'pre'; v: () => unknown; at?: string } | { kind: 'applied'; v: () => unknown } | { kind: 'loginfo'; v: () => unknown };
let mode: Mode = { kind: 'none' };
const SIG = '22222222-2222-4222-8222-222222222222';
const VER = '33333333-3333-4333-8333-333333333333';
const store: { sig: Record<string, string>; ver: Record<string, string>; records: number } = { sig: {}, ver: {}, records: 0 };
const calls: string[] = [];
const logs: any[] = [];

function classify(sql: string): string {
  const s = sql.replace(/\s+/g, ' ');
  if (/UPDATE signatories SET status = 'revoked'/.test(s)) return 'sig.revoke';
  if (/UPDATE signatories SET status = 'active'/.test(s)) return 'sig.reinstate';
  if (/UPDATE signatories SET/.test(s)) return 'sig.patch';
  if (/UPDATE third_party_verifiers SET status = 'suspended'/.test(s)) return 'ver.suspend';
  if (/UPDATE third_party_verifiers SET status = 'active', suspended_at/.test(s)) return 'ver.reinstate';
  if (/INSERT INTO third_party_verification_records/.test(s)) return 'ver.record';
  if (/FROM third_party_verifiers WHERE api_key_hash/.test(s)) return 'ver.lookup';
  if (/FROM third_party_verification_records/.test(s)) return 'ver.records';
  if (/FROM third_party_verifiers/.test(s)) return 'ver.list';
  if (/FROM signatories s/.test(s)) return 'sig.select';
  if (/FROM signatories/.test(s)) return 'sig.check';
  return 'other:' + s.slice(0, 40);
}
function apply(op: string): any {
  switch (op) {
    case 'sig.revoke': if (store.sig[SIG] === 'active') { store.sig[SIG] = 'revoked'; return 1; } return 0;
    case 'sig.reinstate': if (store.sig[SIG] === 'revoked') { store.sig[SIG] = 'active'; return 1; } return 0;
    case 'sig.patch': return 1;
    case 'ver.suspend': if (store.ver[VER] === 'active') { store.ver[VER] = 'suspended'; return 1; } return 0;
    case 'ver.reinstate': if (store.ver[VER] === 'suspended') { store.ver[VER] = 'active'; return 1; } return 0;
    case 'ver.record': store.records++; return 1;
    case 'ver.lookup': return store.ver[VER] === 'active' ? [{ id: VER, organizationName: 'Org', tier: 'standard' }] : [];
    case 'sig.check': return [{ id: SIG, documentTypes: [], canDelegate: false }];
    default: return [];
  }
}
async function run(sql: string): Promise<any> {
  const op = classify(sql); calls.push(op);
  if (mode.kind === 'pre' && (!mode.at || mode.at === op)) throw mode.v();
  const r = apply(op);
  if (mode.kind === 'applied') throw mode.v();
  return r;
}
const tag = (strings: TemplateStringsArray) => run(strings.join('?'));
jest.mock('../db', () => ({ prisma: { $queryRaw: (s: any) => tag(s), $executeRaw: (s: any) => tag(s), $executeRawUnsafe: (sql: string) => run(sql) } }));
jest.mock('../middleware/auth', () => ({ authenticate: () => (_q: any, _s: any, n: any) => n() }));
jest.mock('../utils/logger', () => ({
  logger: {
    info: (...a: any[]) => { logs.push(['info', ...a]); if (mode.kind === 'loginfo') throw mode.v(); },
    warn: (...a: any[]) => logs.push(['warn', ...a]),
    error: (...a: any[]) => logs.push(['error', ...a]),
    debug: () => {},
  },
}));

// eslint-disable-next-line @typescript-eslint/no-var-requires
const express = require('express');
const { signatoriesRouter } = require('../routes/signatories');
const { thirdPartyVerifiersRouter } = require('../routes/thirdPartyVerifiers');

function revokedProxy(): object { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function throwingGetter(): Error { const e = new Error('hidden'); Object.defineProperty(e, 'message', { get() { throw new Error('getter'); } }); return e; }
const KINDS: Record<string, () => unknown> = { ordinaryError: () => new Error('db down SECRETVAL'), string: () => 'plain string', revokedProxy, throwingGetter };

let server: any; let base = '';
beforeAll((done) => {
  const app = express(); app.use(express.json());
  app.use((req: any, _r: any, n: any) => { req.user = { userId: '11111111-1111-4111-8111-111111111111', email: 'actor@example.test' }; n(); });
  app.use('/api/signatories', signatoriesRouter); app.use('/api/tpv', thirdPartyVerifiersRouter);
  server = app.listen(0, '127.0.0.1', () => { base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port; done(); });
});
afterAll((done) => { server.closeAllConnections?.(); server.close(() => done()); });

async function call(method: string, path: string, body?: any) {
  const r = await fetch(base + path, { method, headers: { 'content-type': 'application/json' }, body: body ? JSON.stringify(body) : undefined, signal: AbortSignal.timeout(1500) }).catch(() => null);
  if (!r) return { status: 'NO ANSWER', body: '' };
  return { status: r.status, body: await r.text() };
}

const ROUTES: Array<{ id: string; method: string; path: string; body?: any; seed: () => void; modes: string[] }> = [
  { id: 'sig GET /', method: 'GET', path: `/api/signatories?organizationId=${SIG}`, seed: () => {}, modes: ['pre'] },
  { id: 'sig GET /check', method: 'GET', path: `/api/signatories/check?organizationId=${SIG}&userId=${SIG}`, seed: () => {}, modes: ['pre'] },
  { id: 'sig GET /:id', method: 'GET', path: `/api/signatories/${SIG}`, seed: () => {}, modes: ['pre'] },
  { id: 'sig PATCH /:id', method: 'PATCH', path: `/api/signatories/${SIG}`, body: { displayName: 'N' }, seed: () => {}, modes: ['pre', 'applied', 'loginfo'] },
  { id: 'sig revoke', method: 'POST', path: `/api/signatories/${SIG}/revoke`, body: { reason: 'r' }, seed: () => { store.sig[SIG] = 'active'; }, modes: ['pre', 'applied', 'loginfo'] },
  { id: 'sig reinstate', method: 'POST', path: `/api/signatories/${SIG}/reinstate`, seed: () => { store.sig[SIG] = 'revoked'; }, modes: ['pre', 'applied', 'loginfo'] },
  { id: 'ver GET /', method: 'GET', path: '/api/tpv/', seed: () => {}, modes: ['pre'] },
  { id: 'ver suspend', method: 'POST', path: `/api/tpv/${VER}/suspend`, body: { reason: 'r' }, seed: () => { store.ver[VER] = 'active'; }, modes: ['pre', 'applied', 'loginfo'] },
  { id: 'ver reinstate', method: 'POST', path: `/api/tpv/${VER}/reinstate`, seed: () => { store.ver[VER] = 'suspended'; }, modes: ['pre', 'applied'] },
  { id: 'ver verify (lookup fails)', method: 'POST', path: '/api/tpv/verify', body: { certificationId: 'c1', apiKey: 'tpv_x' }, seed: () => { store.ver[VER] = 'active'; }, modes: ['pre@ver.lookup'] },
  { id: 'ver verify (insert fails)', method: 'POST', path: '/api/tpv/verify', body: { certificationId: 'c1', apiKey: 'tpv_x' }, seed: () => { store.ver[VER] = 'active'; }, modes: ['pre@ver.record', 'applied', 'loginfo'] },
  { id: 'ver GET /:id/records', method: 'GET', path: `/api/tpv/${VER}/records`, seed: () => {}, modes: ['pre'] },
];

describe('gate104 probe routes', () => {
  for (const r of ROUTES) {
    it(`${r.id} control ok`, async () => {
      store.sig = {}; store.ver = {}; store.records = 0; calls.length = 0; logs.length = 0; mode = { kind: 'none' }; r.seed();
      const res = await call(r.method, r.path, r.body);
      emit({ route: r.id, mode: 'ok', kind: 'none', ...res, state: { ...store }, calls: [...calls], logs: JSON.parse(JSON.stringify(logs)) });
    });
    for (const m of r.modes) {
      for (const k of Object.keys(KINDS)) {
        it(`${r.id} ${m} ${k}`, async () => {
          store.sig = {}; store.ver = {}; store.records = 0; calls.length = 0; logs.length = 0; r.seed();
          const [mk, at] = m.split('@');
          mode = mk === 'pre' ? { kind: 'pre', v: KINDS[k], at } : mk === 'applied' ? { kind: 'applied', v: KINDS[k] } : { kind: 'loginfo', v: KINDS[k] };
          const res = await call(r.method, r.path, r.body);
          await new Promise((s) => setTimeout(s, 30));
          mode = { kind: 'none' };
          const logText = JSON.stringify(logs);
          emit({ route: r.id, mode: m, kind: k, ...res, state: { ...store }, calls: [...calls], logs: JSON.parse(logText), leak: { secret: logText.includes('SECRETVAL'), actorEmail: logText.includes('actor@example.test'), sigId: (logs.filter((l) => l[0] === 'error').map((l) => JSON.stringify(l)).join('')).includes(SIG) || (logs.filter((l) => l[0] === 'error').map((l) => JSON.stringify(l)).join('')).includes(VER) } });
        });
      }
    }
  }
});
