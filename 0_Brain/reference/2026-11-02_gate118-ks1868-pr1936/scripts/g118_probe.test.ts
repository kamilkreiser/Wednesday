// Gate 118 probe (NOT part of PR 1936). Runs the REAL signatories nominate route and the REAL
// thirdPartyVerifiers register + approve routes on a real loopback listener. Only prisma is replaced
// by a statement recorder; auth and the logger are stubbed; uuid is fixed so statements compare.
import * as fs from 'fs';
import * as crypto from 'crypto';

type Stmt = { sql: string; values: string; failed: boolean };
const st: { point: string; thrown: unknown; stmts: Stmt[]; errs: string[]; infos: number; rowcount: number } = { point: 'none', thrown: undefined, stmts: [], errs: [], infos: 0, rowcount: 1 };

function norm(s: string): string {
  return s.replace(/\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+Z/g, '<T>').replace(/\b[0-9a-f]{64}\b/g, '<H>');
}
async function rec(strings: TemplateStringsArray, values: unknown[]): Promise<unknown> {
  const sql = strings.join('$?').replace(/\s+/g, ' ').trim();
  const failed = st.point === 'db';
  st.stmts.push({ sql, values: JSON.stringify(values), failed });
  if (failed) throw st.thrown;
  return st.rowcount;
}
jest.mock('../db', () => ({
  prisma: {
    $executeRaw: (s: TemplateStringsArray, ...v: unknown[]) => rec(s, v),
    $queryRaw: (s: TemplateStringsArray, ...v: unknown[]) => rec(s, v),
  },
}));
jest.mock('uuid', () => ({ v4: () => '44444444-4444-4444-8444-444444444444' }));
function safe(x: unknown): string { try { return JSON.stringify(x); } catch { return '<unserialisable>'; } }
jest.mock('../utils/logger', () => ({
  logger: {
    info: () => { st.infos += 1; if (st.point === 'after') throw st.thrown; },
    warn: () => undefined, debug: () => undefined,
    error: (...a: unknown[]) => { st.errs.push(safe(a)); },
  },
}));
jest.mock('../middleware/auth', () => ({ authenticate: () => (_q: unknown, _r: unknown, n: () => void) => n() }));

import express from 'express';
import type { AddressInfo } from 'net';
import { signatoriesRouter } from '../routes/signatories';
import { thirdPartyVerifiersRouter } from '../routes/thirdPartyVerifiers';

const rp = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const THROWN: Record<string, () => unknown> = {
  error: () => new Error('db down'),
  error23505: () => Object.assign(new Error('db down'), { code: '23505' }),
  errorOtherCode: () => Object.assign(new Error('db down'), { code: '23503' }),
  string: () => 'db down string',
  nullValue: () => null,
  revokedProxy: rp,
  msgGetterThrows: () => { const e = new Error('hidden'); Object.defineProperty(e, 'message', { get() { throw new Error('getter boom'); } }); return e; },
  msgGetterThrowsRevoked: () => { const e = new Error('hidden'); Object.defineProperty(e, 'message', { get() { throw rp(); } }); return e; },
  codeGetterThrows: () => { const e = new Error('db down'); Object.defineProperty(e, 'code', { get() { throw new Error('code boom'); } }); return e; },
  codeGetterThrowsRevoked: () => { const e = new Error('db down'); Object.defineProperty(e, 'code', { get() { throw rp(); } }); return e; },
  code23505MsgThrows: () => { const e = Object.assign(new Error('hidden'), { code: '23505' }); Object.defineProperty(e, 'message', { get() { throw new Error('getter boom'); } }); return e; },
  toPrimitiveThrows: () => ({ [Symbol.toPrimitive]() { throw new Error('prim boom'); } }),
};
const ROUTES = [
  { name: 'nominate', url: '/api/signatories/', body: { organizationId: '22222222-2222-4222-8222-222222222222', userId: '33333333-3333-4333-8333-333333333333', displayName: 'Ks Name' } },
  { name: 'register', url: '/api/third-party-verifiers/register', body: { organizationName: 'Ks Org', contactEmail: 'ks1868@example.test' } },
  { name: 'approve', url: '/api/third-party-verifiers/55555555-5555-4555-8555-555555555555/approve', body: {} },
];
const POINTS = ['none', 'db', 'after', 'rowcount0'];

const out: unknown[] = [];
let unhandled = 0;
const onUnh = () => { unhandled += 1; };
// Express 4 ignores the promise a handler returns. Observe it (no behaviour change): a rejected handler
// promise is what production sees as an unhandledRejection; jest-circus cannot format a revoked-Proxy reason,
// so the probe attaches the observer and counts it instead of letting it go global.
for (const router of [signatoriesRouter, thirdPartyVerifiersRouter] as any[]) {
  for (const layer of router.stack) {
    if (!layer.route) continue;
    for (const l of layer.route.stack) {
      const orig = l.handle;
      if (orig.length > 3) continue;
      l.handle = function (this: unknown, ...a: unknown[]) {
        const r = orig.apply(this, a);
        if (r && typeof r.then === 'function') r.then(undefined, () => { unhandled += 1; });
        return r;
      };
    }
  }
}
const app = express();
app.use(express.json());
app.use((req, _res, next) => { (req as any).user = { userId: '11111111-1111-4111-8111-111111111111', email: 'g118@example.test' }; next(); });
app.use('/api/signatories', signatoriesRouter);
app.use('/api/third-party-verifiers', thirdPartyVerifiersRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';
let saved: Array<(...a: any[]) => void> = [];
beforeAll(async () => {
  // jest's own unhandledRejection listener cannot format a revoked Proxy reason; park it during the grid.
  saved = process.listeners('unhandledRejection') as any;
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnh);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => {
  process.off('unhandledRejection', onUnh);
  for (const l of saved) process.on('unhandledRejection', l);
  server?.close();
  fs.writeFileSync(process.env.G118_OUT as string, JSON.stringify({ unhandled, cells: out }, null, 1));
});

test('g118 grid', async () => {
  for (const r of ROUTES) {
    for (const kind of Object.keys(THROWN)) {
      for (const point of POINTS) {
        if ((point === 'none' || point === 'rowcount0') && kind !== 'error') continue;
        if (point === 'rowcount0' && r.name !== 'approve') continue;
        st.point = point; st.thrown = THROWN[kind](); st.stmts = []; st.errs = []; st.infos = 0; st.rowcount = point === 'rowcount0' ? 0 : 1;
        const before = unhandled;
        let status: number | string; let body = ''; let keyIssued = false; let keyMatchesHash: boolean | null = null;
        try {
          const res = await fetch(baseUrl + r.url, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(r.body), signal: AbortSignal.timeout(1200) });
          status = res.status; const text = await res.text();
          try {
            const j = JSON.parse(text);
            if (typeof j.apiKey === 'string') {
              keyIssued = true;
              const h = crypto.createHash('sha256').update(j.apiKey).digest('hex');
              keyMatchesHash = st.stmts.some((s) => s.values.includes(h));
              j.apiKey = '<key>';
            }
            body = norm(JSON.stringify(j));
          } catch { body = norm(text); }
        } catch { status = 'NO ANSWER'; }
        await new Promise((res) => setTimeout(res, 20));
        out.push({ route: r.name, kind, point, status, body, keyIssued, keyMatchesHash, stmts: st.stmts.map((s) => ({ sql: s.sql, values: norm(s.values), failed: s.failed })), errs: st.errs, infos: st.infos, unhandled: unhandled - before });
      }
    }
  }
  expect(out.length).toBeGreaterThan(0);
}, 300000);
