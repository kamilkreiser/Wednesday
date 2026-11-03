import { it, vi } from 'vitest';
import * as fs from 'fs';
import express from 'express';
const h = vi.hoisted(() => ({ toThrow: undefined as unknown }));
vi.mock('../db', () => ({ isDbAvailable: () => true, query: (..._a: unknown[]) => Promise.reject(h.toThrow) }));
import { delegationRoutes } from '../routes/delegations';
import { logger } from '../utils/logger';

const rp = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const kinds: Record<string, () => unknown> = {
  ordinary: () => new Error('db boom'),
  revokedProxy: rp,
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('boom'); } } }),
  symbolMessage: () => ({ message: Symbol('s') }),
  nullThrown: () => null,
  undefinedThrown: () => undefined,
  bigintMessage: () => ({ message: 10n }),
  messageIsThrowingToString: () => ({ message: Object.freeze({ toString() { throw new Error('ts'); } }) }),
};
const unh: unknown[] = []; const unc: unknown[] = [];
process.on('unhandledRejection', (r) => unh.push(r));
it('route', async () => {
  const app = express(); app.use(express.json());
  app.use((req, _res, next) => { (req as any).user = { id: 'u1', role: (req.headers['x-role'] as string) || 'SYSTEM_ADMIN' }; next(); });
  app.use('/api/delegations', delegationRoutes);
  // next(error) sink so a non-Error rejection shows as a status
  app.use((err: any, _req: any, res: any, _next: any) => { res.status(599).json({ nextCalled: true }); });
  const srv = await new Promise<any>((r) => { const s = app.listen(0, () => r(s)); });
  const port = srv.address().port;
  const logs: any[] = []; const o = (logger as any).log; // record the real winston logger by wrapping its transport write
  const origWrite = (logger as any).write.bind(logger);
  (logger as any).write = (info: any) => { logs.push({ level: info.level, message: info.message, errorType: info.error === undefined ? 'undefined' : typeof info.error }); return origWrite(info); };
  const rows: string[] = [];
  const cw = console.warn, ce = console.error; const cons: unknown[][] = [];
  for (const [name, mk] of Object.entries(kinds)) {
    h.toThrow = mk(); logs.length = 0; cons.length = 0; unh.length = 0;
    console.error = (...a: unknown[]) => { cons.push(a); }; console.warn = console.error;
    const res = await fetch(`http://127.0.0.1:${port}/api/delegations/admin/process-expired`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: '{}' });
    const body = await res.text();
    await new Promise((r) => setImmediate(r));
    console.error = ce; console.warn = cw;
    rows.push(JSON.stringify({ mode: process.env.G158_MODE, kind: name, status: res.status, body, consoleCalls: cons.length, consoleArgType: cons.length ? typeof cons[0][1] : '-', winston: logs.map((l) => l.message.slice(0, 40) + '|' + l.errorType), unhandled: unh.length }));
  }
  // positive control: non-admin gets 403 (route really executed)
  const r403 = await fetch(`http://127.0.0.1:${port}/api/delegations/admin/process-expired`, { method: 'POST', headers: { 'x-role': 'USER' } });
  rows.push(JSON.stringify({ mode: process.env.G158_MODE, kind: 'CONTROL_non_admin', status: r403.status }));
  srv.close();
  fs.appendFileSync(process.env.G158_OUT as string, rows.join('\n') + '\n');
});
