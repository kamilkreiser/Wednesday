// gate 101 probe (NOT part of the PR). Real systemErrors router + real trackError + real fail500; prisma and logger are stand-ins that record.
import * as fs from 'fs';
import * as http from 'http';
import express from 'express';

const OUT = process.env.PROBE_OUT as string;
const emit = (o: unknown) => fs.appendFileSync(OUT, JSON.stringify(o) + '\n');

const rows: any[] = [];
let nextExec: { kind: 'ok' } | { kind: 'throw'; v: unknown } = { kind: 'ok' };
const logs: any[] = [];
const mockExecuteRaw = jest.fn(async (_strings: any, ...vals: any[]) => {
  if (nextExec.kind === 'throw') throw nextExec.v;
  rows.push({ service: vals[0], errorType: vals[1], message: vals[2] });
  return 1;
});
jest.mock('../db', () => ({ prisma: { $executeRaw: (...a: any[]) => (mockExecuteRaw as any)(...a), $queryRaw: jest.fn() } }));
jest.mock('../utils/logger', () => ({
  logger: {
    info: (...a: any[]) => logs.push(['info', ...a]),
    warn: (...a: any[]) => logs.push(['warn', ...a]),
    error: (...a: any[]) => logs.push(['error', ...a]),
    debug: () => {},
  },
}));
jest.mock('../middleware/auth', () => ({ authenticate: () => (_q: any, _s: any, n: any) => n(), requireRole: () => (_q: any, _s: any, n: any) => n() }));

import { systemErrorsRouter } from '../routes/systemErrors';
import * as tracking from '../services/errorTrackingService';

const unhandled: any[] = [];
process.on('unhandledRejection', (r) => unhandled.push(String((() => { try { return (r as any)?.message ?? 'x'; } catch { return 'unreadable'; } })())));

function revokedProxy(): object { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function throwingGetter(): Error { const e = new Error('hidden'); Object.defineProperty(e, 'message', { get() { throw new Error('getter'); } }); return e; }

let server: http.Server; let port: number;
beforeAll((done) => {
  const app = express(); app.use(express.json()); app.use('/api/system-errors', systemErrorsRouter);
  server = app.listen(0, () => { port = (server.address() as any).port; done(); });
});
afterAll((done) => { (server as any).closeAllConnections?.(); server.close(() => done()); });

async function post(path: string, body: any) {
  const r = await fetch(`http://127.0.0.1:${port}/api/system-errors${path}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body), signal: AbortSignal.timeout(2500) }).catch(() => null);
  if (!r) return { status: 0, body: 'NO ANSWER' };
  let txt = await r.text();
  return { status: r.status, body: txt };
}

const KINDS: Record<string, () => unknown> = {
  ordinaryError: () => new Error('db down'),
  string: () => 'plain string',
  revokedProxy,
  throwingGetter,
};

describe('probe A: real route + real trackError, insert rejects', () => {
  for (const route of ['/ingest', '/client-errors']) {
    for (const k of Object.keys(KINDS)) {
      it(`${route} ${k}`, async () => {
        rows.length = 0; logs.length = 0; unhandled.length = 0;
        nextExec = { kind: 'throw', v: KINDS[k]() };
        const body = route === '/ingest' ? { service: 's', message: 'm' } : { error: 'm', source: 's' };
        const res = await post(route, body);
        await new Promise((r) => setTimeout(r, 20));
        emit({ probe: 'A', route, kind: k, status: res.status, body: res.body, rows: rows.length, logs, unhandled: unhandled.length });
      });
    }
    it(`${route} control ok`, async () => {
      rows.length = 0; logs.length = 0; nextExec = { kind: 'ok' };
      const body = route === '/ingest' ? { service: 's', message: 'm' } : { error: 'm', source: 's' };
      const res = await post(route, body);
      emit({ probe: 'A', route, kind: 'ok', status: res.status, body: res.body, rows: rows.length, logs });
    });
  }
});

describe('probe C: ingest catch sees a thrown non-Error (trackError itself rejects)', () => {
  const SECRET = 'SECRET-VALUE-9f3a';
  const vals: Record<string, () => unknown> = {
    objWithSecret: () => ({ code: 'X', secret: SECRET }),
    classInstance: () => new (class Custom { code = 'X'; secret = SECRET; })(),
    number: () => 5, nul: () => null, undef: () => undefined,
    revokedProxy, throwingGetter, ordinaryError: () => new Error('ord'), string: () => 'str',
  };
  for (const route of ['/ingest', '/client-errors']) {
    for (const k of Object.keys(vals)) {
      it(`${route} ${k}`, async () => {
        logs.length = 0; unhandled.length = 0;
        const spy = jest.spyOn(tracking, 'trackError').mockRejectedValueOnce(vals[k]() as any);
        const body = route === '/ingest' ? { service: 's', message: 'm' } : { error: 'm', source: 's' };
        const res = await post(route, body);
        await new Promise((r) => setTimeout(r, 20));
        const logText = JSON.stringify(logs, (_k, v) => v);
        emit({ probe: 'C', route, kind: k, status: res.status, body: res.body, logs, secretInLog: logText.includes(SECRET), unhandled: unhandled.length });
        spy.mockRestore();
      });
    }
  }
});
